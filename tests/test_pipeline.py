import json

from bcvm import pipeline, tokens
from bcvm.shards import Shard


def test_build_and_read_shard(tmp_path):
    job = dict(phase="B", shard_id=0, seed=0, out_dir=str(tmp_path), target_tokens=200_000,
               mix=pipeline.DEFAULT_MIX["B"], steps_per_script=8, records="full")
    meta = pipeline.build_shard(job)
    assert meta["n_tokens"] >= 200_000 and meta["stats"]["kept"] > 0
    sh = Shard(str(tmp_path / "B_0000"))
    assert len(sh) == meta["n_steps"]
    for i in range(0, len(sh), max(1, len(sh) // 200)):
        ids, mask = sh.example(i)
        toks = tokens.strs(ids.tolist())
        assert toks[0] == "<bos>" and toks[-1] == "<eos>"
        first = int(mask.argmax())
        assert toks[first - 1] == "=>"
        st, end = tokens.parse_state(toks, toks.index("<state>"))
        nxt, out, end2 = tokens.parse_step_output(toks, first)
        assert end2 == len(toks)
    # packed groups cover every row exactly once
    assert sum(len(rows) for _, _, rows in sh.groups()) == len(sh)
    # resuming skips a finished shard
    assert pipeline.build_shard(job)["n_tokens"] == meta["n_tokens"]


def test_records_are_complete(tmp_path):
    from compression import zstd
    job = dict(phase="A", shard_id=1, seed=0, out_dir=str(tmp_path), target_tokens=50_000,
               mix={"grammar": 1.0}, steps_per_script=8, records="full")
    pipeline.build_shard(job)
    recs = [json.loads(line) for line in zstd.decompress(open(tmp_path / "A_0001.records.jsonl.zst", "rb").read()).splitlines()]
    assert recs and all(r["split"] == "train" for r in recs)
    r = recs[0]
    assert len(r["states"]) == r["steps"] + 1 and "".join(r["outs"]) == r["stdout"]


def test_splits_are_deterministic_and_held_out():
    ids = tokens.ids(["<bos>", "<code>", "</code>"])
    assert pipeline.split_of(ids, "grammar", None) == pipeline.split_of(ids, "grammar", None)
    held = sum(pipeline.split_of([], "natural", f"b{i}") == "test" for i in range(2000))
    assert 100 < held < 300


def test_arith_source_is_division_heavy():
    import random
    from bcvm.gen import make
    rng = random.Random(5)
    div = total = 0
    for _ in range(60):
        src, _ = make(rng, "A", "arith")
        try:
            prog, trace = pipeline.prepare(src, "A")
        except pipeline.Skip:
            continue
        for st in trace.states[:-1]:
            total += 1
            div += tokens.work_kind(prog.instrs[st.ip], st) is not None
    assert total > 500 and div / total > 0.08


def test_copy_source_has_repetitive_strings():
    import random
    from bcvm.gen import grammar, make
    rng = random.Random(9)
    srcs = [make(rng, "B", "copy")[0] for _ in range(80)]
    assert sum(any(p in s for p in ("0101", "1010", "abab", "baba", "0110", "1001")) for s in srcs) >= 5
    # the default generator is unchanged, so eval sets rebuild identically
    assert grammar.generate(random.Random(3), "B") == grammar.generate(random.Random(3), "B", copy=False)


def test_edge_source_has_value_logic_chains_and_steps():
    import random
    import re
    from bcvm.gen import grammar, make
    rng = random.Random(4)
    text = "\n".join(make(rng, "B", "edge")[0] for _ in range(150))
    assert re.search(r"print\([^)]*\b(and|or)\b", text)
    assert re.search(r"range\([^,]+,[^,]+,\s*-?(1[1-9]|2[0-5])\)", text)
    assert len(re.findall(r"(?m)^.*([<>]=?|[!=]=)[^<>=!\n]+([<>]=?|[!=]=)[^<>=!\n]+([<>]=?|[!=]=)", text)) >= 3
    assert grammar.generate(random.Random(3), "B") == grammar.generate(random.Random(3), "B", edge=False)


def test_edge_source_has_label_series_and_long_phase_a():
    import random
    from bcvm import pipeline, tokens
    from bcvm.gen import make
    rng = random.Random(6)
    lens, series = [], 0
    for _ in range(60):
        src, _ = make(rng, "A", "edge")
        series += any(f"'{w} " in src for w in ("Round", "Step", "Day", "Month", "Turn", "Level", "Customer", "tick"))
        try:
            prog, _ = pipeline.prepare(src, "A")
        except pipeline.Skip:
            continue
        lens.append(len(tokens.enc_listing(prog)))
    assert series >= 5 and max(lens) > 700
