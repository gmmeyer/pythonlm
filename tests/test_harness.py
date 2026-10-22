import random

from bcvm import harness, pipeline, refvm, tokens
from bcvm.gen import grammar


def test_oracle_runner_matches_cpython(natural_sample):
    for phase, path in natural_sample:
        src = open(path).read()
        try:
            _, trace = pipeline.prepare(src, phase)
        except pipeline.Skip:
            continue
        res = harness.run(src, phase, harness.OracleStepper())
        assert res.error is None and res.refused is None, (path, res)
        assert res.stdout == trace.stdout and res.rejected == 0


def test_refused_scripts_never_run():
    res = harness.run("import os\nprint(1)\n", "C", harness.OracleStepper())
    assert res.refused and res.steps == 0 and res.stdout == ""


def _swap_digit(toks):
    out = list(toks)
    for i, t in enumerate(out):
        if t in tokens.ADDR:
            out[i] = "@9" if t != "@9" else "@8"
            return out
    return out


def test_validator_rejects_and_resampling_rescues():
    src = "x = 4\nfor i in range(3):\n    x = x + i\n    print(x)\n"
    res = harness.run(src, "B", harness.OracleStepper(corrupt=_swap_digit))
    assert res.stdout == "4\n5\n7\n"
    assert res.rejected > 0 and res.rescued == res.rejected


def test_all_candidates_bad_stops_without_output():
    stepper = harness.OracleStepper(corrupt=_swap_digit)
    stepper.propose_orig = stepper.propose
    stepper.propose = lambda *a: [_swap_digit(c) for c in stepper.propose_orig(*a)]
    res = harness.run("print(1)\n", "A", stepper)
    assert res.error and res.stdout == ""


def test_validator_catches_value_copy_errors():
    rng = random.Random(3)
    caught = 0
    for _ in range(40):
        try:
            prog, trace = pipeline.prepare(grammar.generate(rng, "B"), "B")
        except pipeline.Skip:
            continue
        for i in range(trace.steps):
            st, nxt = trace.states[i], trace.states[i + 1]
            assert harness.validate(prog, st, nxt, trace.outs[i]) is None
            if nxt.names and prog.instrs[st.ip].opname != "STORE_NAME":
                k = next(iter(nxt.names))
                v = nxt.names[k]
                bad = refvm.State(nxt.ip, nxt.stack, {**nxt.names, k: (v + 1) if type(v) is int else 0})
                assert harness.validate(prog, st, bad, trace.outs[i]) is not None
                caught += 1
    assert caught > 50
