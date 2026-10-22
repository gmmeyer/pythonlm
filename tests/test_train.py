import numpy as np
import pytest

torch = pytest.importorskip("torch")

from bcvm import pipeline, tokens  # noqa: E402
from bcvm.shards import Shard  # noqa: E402
from bcvm.train.data import EvalSet, LoadedShard, batches, pack  # noqa: E402
from bcvm.train.model import ModelConfig, StepModel, packed_dense_mask  # noqa: E402


@pytest.fixture(scope="module")
def shard(tmp_path_factory):
    out = tmp_path_factory.mktemp("shard")
    job = dict(phase="B", shard_id=0, seed=3, out_dir=str(out), target_tokens=60_000,
               mix=pipeline.DEFAULT_MIX["B"], steps_per_script=16, records="")
    pipeline.build_shard(job)
    return str(out / "B_0000")


def _groups(stem, sid=False):
    sh = LoadedShard(stem)
    first = 0
    for i in range(len(sh)):
        listing, steps = sh.group(i)
        yield listing, steps, first if sid else None
        first += len(steps)


def test_packed_targets_match_expanded(shard, seq_len=2048):
    """Every expanded example's loss tokens appear once, after the same context
    (the listing, then the step), at the same positions."""
    ref = Shard(shard)
    rows = list(pack(_groups(shard, sid=True), seq_len))
    seen = np.zeros(len(ref), int)
    for r in rows:
        assert len(r["ids"]) == seq_len
        for sid in np.unique(r["sid"][r["sid"] >= 0]):
            at = np.flatnonzero(r["sid"] == sid)
            ids, mask = ref.example(int(sid))
            ll = int(ref.index[sid, 1])
            first = int(mask.argmax())
            assert (r["tgt"][at] == ids[first:]).all()
            assert (r["pos"][at] == np.arange(first - 1, len(ids) - 1)).all()
            # the step's input tokens precede its targets in the same chunk, and the listing starts the chunk
            doc, step = r["doc"][at[0]], r["seg"][at[0]]
            own = np.flatnonzero((r["doc"] == doc) & (r["seg"] == step))
            lst = np.flatnonzero((r["doc"] == doc) & (r["seg"] == 0))
            assert (r["ids"][own] == ids[ll:]).all() and (r["ids"][lst] == ids[:ll]).all()
            seen[sid] += 1
    assert (seen == 1).all()


def test_split_groups_repeat_the_listing(shard):
    listing, steps = LoadedShard(shard).group(0)
    big = [(listing, steps * 6, 0)]
    seq_len = len(listing) + 3 * max(len(s) for s, _ in steps)
    rows = list(pack(iter(big), seq_len))
    assert len(rows) > 1
    for r in rows:
        assert (r["ids"][:len(listing)] == listing).all()
    assert sorted(np.concatenate([np.unique(r["sid"][r["sid"] >= 0]) for r in rows])) == list(range(len(steps) * 6))
    with pytest.raises(ValueError):
        list(pack(iter(big), len(listing) + 2))


def test_packed_forward_equals_expanded(shard):
    """The block mask + restarted positions give the same logits as one
    listing + step under plain causal attention (i.e. KV-cache inference)."""
    torch.manual_seed(0)
    model = StepModel(ModelConfig(d_model=64, n_layers=2, n_heads=4, d_ff=128)).eval()
    ref = Shard(shard)
    b = next(batches(pack(_groups(shard, sid=True), 2048), 2, 2048))
    with torch.no_grad():
        packed = model(b["ids"], b["pos"], packed_dense_mask(b["doc"], b["seg"]))
        for sid in torch.unique(b["sid"][b["sid"] >= 0])[::7].tolist():
            ids, mask = ref.example(sid)
            x = torch.from_numpy(ids.astype(np.int64))[None]
            exp = model(x, torch.arange(x.shape[1])[None], _causal(x.shape[1]))
            row, at = (b["sid"] == sid).nonzero(as_tuple=True)
            first = int(mask.argmax())
            torch.testing.assert_close(packed[row, at], exp[0, first - 1:-1], atol=1e-4, rtol=1e-4)


def _causal(n):
    return torch.ones(n, n, dtype=torch.bool).tril()[None, None]


def test_evalset_opcodes(shard, tmp_path):
    import os
    import shutil
    for ext in (".bin", ".idx.npy", ".json"):
        shutil.copy(shard + ext, os.path.join(tmp_path, "B_0000" + ext))
    ev = EvalSet(str(tmp_path))
    groups = list(ev.groups())
    assert len(ev.opcode) == ev.max_steps == len(Shard(shard))
    names = {tokens.VOCAB[o] for o in ev.opcode}
    assert names <= set(tokens.OPCODES) and "RETURN_VALUE" not in names
    assert sum(ev.prints) > 0
    assert sum(len(s) for _, s, _ in groups) == ev.max_steps


def test_engine_decode_matches_full_forward():
    """KV-cached, batched, grammar-masked decoding picks the same tokens as a
    plain forward over listing + state + output: slots hold listings of
    different lengths, a slot is reused for a new program, and each slot runs
    several steps over the same step region."""
    from bcvm import refvm
    from bcvm.decoding import OutputGrammar
    from bcvm.program import Program
    from bcvm.train.stepper import Engine

    from conftest import natural_files

    torch.manual_seed(0)
    model = StepModel(ModelConfig(d_model=64, n_layers=2, n_heads=4, d_ff=128, max_pos=1024))
    srcs = [open(f).read() for f in natural_files("A")[:3] + natural_files("B")[:2]]

    def fn(src, stepper):
        prog = Program(src)
        listing = ["<bos>"] + tokens.enc_listing(prog)
        st, outs = refvm.State(0, (), {}), []
        for _ in range(3):
            state = tokens.enc_state(st) + ["=>"]
            outs.append((state, next(iter(stepper.propose(prog, listing, state, 1)))))
            st, _ = refvm.step(prog, st)
        return prog, listing, outs

    engine = Engine(model, n_slots=3)
    results = engine.run_all(srcs, fn)
    for prog, listing, outs in results:
        for state, cand in outs:
            x = torch.tensor(tokens.ids(listing + state + cand))[None]
            with torch.no_grad():
                logits = model(x, torch.arange(x.shape[1])[None], _causal(x.shape[1]))[0]
            g = OutputGrammar(len(prog.instrs), len(prog.names))
            start = len(listing) + len(state)
            for j, t in enumerate(cand):
                allowed = sorted(g.allowed())
                row = logits[start - 1 + j]
                assert row[tokens.TOKEN_ID[t]] >= row[allowed].max() - 1e-4
                g.feed(t)
