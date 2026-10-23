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


def test_edge_source_has_swaps_and_many_names():
    import random
    from collections import Counter
    from bcvm import pipeline
    from bcvm.gen import make
    rng = random.Random(8)
    swaps, names = Counter(), []
    for phase in "AB" * 40:
        src, _ = make(rng, phase, "edge")
        try:
            prog, _ = pipeline.prepare(src, phase)
        except pipeline.Skip:
            continue
        swaps.update(f"SWAP {ins.arg}" for ins in prog.instrs if ins.opname == "SWAP")
        names.append(len(prog.names))
    assert swaps["SWAP 3"] >= 10 and swaps["SWAP 2"] >= 5
    assert sum(n > 10 for n in names) >= 10 and max(names) >= 16


def test_edge_source_uses_bools_as_numbers():
    import random
    import re
    from bcvm import pipeline
    from bcvm.gen import make
    rng = random.Random(9)
    srcs = []
    for _ in range(150):
        src, _ = make(rng, "B", "edge")
        try:
            pipeline.prepare(src, "B")
        except pipeline.Skip:
            continue
        srcs.append(src)
    text = "\n".join(srcs)
    assert len(re.findall(r"\(not [^()]+\) [-+*]", text)) >= 3
    assert len(re.findall(r"(?m)^\s*\w+ [-+]= (not |\w+ [<>=!]=? )", text)) >= 3
    assert len(re.findall(r"(?m)^\s*\w+ = \w+ = ", text)) >= 3


def test_edge_source_walks_strings_in_phase_c():
    import random
    import re
    from collections import Counter
    from bcvm import pipeline
    from bcvm.gen import make
    rng = random.Random(10)
    kept, idx, skips = [], Counter(), Counter()
    for _ in range(100):
        src, _ = make(rng, "C", "edge")
        try:
            prog, trace = pipeline.prepare(src, "C")
        except pipeline.Skip as e:
            skips[str(e)] += 1
            continue
        kept.append(src)
        idx.update(re.findall(r"\w+\[([^\]]*[a-z][^\]]*)\]", src))
    assert len(kept) >= 60, skips   # long listings and strings are filtered, as for all edge scripts
    text = "\n".join(kept)
    assert re.search(r"for \w+ in range\(len\(\w+\)\):", text) and re.search(r"while \w+ < len\(\w+\):", text)
    assert sum(idx.values()) >= 100 and len(idx) >= 20


def test_edge_source_prints_pads_and_chains_in_phase_c():
    import random
    import re
    from bcvm import pipeline
    from bcvm.gen import make
    rng = random.Random(14)
    kept = []
    for _ in range(150):
        src, _ = make(rng, "C", "edge")
        try:
            pipeline.prepare(src, "C")
        except pipeline.Skip:
            continue
        kept.append(src)
    text = "\n".join(kept)
    assert len(set(re.findall(r"sep=('[^']*'|\"[^\"]*\")", text))) >= 8
    assert len(re.findall(r"\* \(\d+ - len\(\w+\)\)", text)) >= 10
    assert len(re.findall(r"(?m)^\s*(\w+ = ){3,}", text)) >= 5
    assert "''" in text


def test_edge_source_drills_what_c4_got_wrong_in_phase_c():
    """String ops with other strings below them on the stack (`print(label, a + b)`),
    near-identical strings compared, repeat counts past 6."""
    import random
    from collections import Counter
    from bcvm import pipeline
    from bcvm.gen import make
    rng = random.Random(15)
    seen = Counter()
    for _ in range(150):
        src, _ = make(rng, "C", "edge")
        try:
            prog, trace = pipeline.prepare(src, "C")
        except pipeline.Skip:
            continue
        for st in trace.states[:-1]:
            ins, stk = prog.instrs[st.ip], st.stack
            if ins.opname not in ("BINARY_OP", "COMPARE_OP") or len(stk) < 2:
                continue
            a, b = stk[-2], stk[-1]
            if type(a) is str and type(b) is str and len(stk) >= 3 and type(stk[-3]) is str:
                seen["str op, str below"] += 1
            if ins.arg == "*" and type(a) is str and type(b) is int and b > 6:
                seen["long repeat"] += 1
            if ins.opname == "COMPARE_OP" and type(a) is str and type(b) is str and a != b and len(a) == len(b) > 1:
                seen["near miss"] += 1
    assert seen["str op, str below"] >= 40 and seen["long repeat"] >= 100 and seen["near miss"] >= 20, seen


def test_edge_source_has_labels_differing_late():
    """'Hour 1: stove lit' and 'Hour 1: stove out' in one script: c4 copied the wrong one."""
    import random
    from bcvm import pipeline
    from bcvm.gen import make

    def common(x, y):
        return next((j for j in range(min(len(x), len(y))) if x[j] != y[j]), min(len(x), len(y)))

    rng = random.Random(16)
    pairs = 0
    for _ in range(40):
        src, _ = make(rng, "A", "edge")
        try:
            prog, _ = pipeline.prepare(src, "A")
        except pipeline.Skip:
            continue
        consts = sorted({ins.arg for ins in prog.instrs if ins.opname == "LOAD_CONST" and type(ins.arg) is str})
        pairs += sum(common(x, y) >= max(6, 0.6 * min(len(x), len(y)))
                     for i, x in enumerate(consts) for y in consts[i + 1:])
    assert pairs >= 40, pairs


def test_step_weight_favours_labels_and_strings_above_strings():
    from bcvm import pipeline, refvm
    from bcvm.program import Program
    prog = Program("a = 'ab'\nprint('Total', a + 'c')\nb = a + 'c'\n")
    trace = refvm.run(prog)
    w = {}
    for i in range(trace.steps):
        ins = prog.instrs[trace.states[i].ip]
        w.setdefault((ins.opname, ins.arg), []).append(pipeline.step_weight(prog, trace, i))
    assert w[("LOAD_CONST", "Total")] == [3.0] and w[("LOAD_CONST", "ab")] == [1.0]
    assert w[("BINARY_OP", "+")] == [4.0, 1.0]      # above 'Total', then alone
