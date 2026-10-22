import random

import pytest

from bcvm import decoding, pipeline, refvm, support, tokens
from bcvm.gen import grammar
from bcvm.values import RangeIter, RangeObj


def test_vocab_fits_uint16_and_is_stable():
    assert tokens.VOCAB_SIZE < 65536
    assert tokens.VOCAB[:3] == ["<pad>", "<bos>", "<eos>"]


@pytest.mark.parametrize("v,toks", [
    (0, ["i+", "0"]), (7, ["i+", "7"]), (120, ["i+", "0", "2", "1"]), (-45, ["i-", "5", "4"]),
    (True, ["True"]), (None, ["None"]), ("a b", ['"', "c:a", "c: ", "c:b", '"']), ("", ['"', '"']),
    (RangeIter(3, 10, -1), ["RANGE_IT", "i+", "3", "i+", "0", "1", "i-", "1"]),
])
def test_value_encoding(v, toks):
    assert tokens.enc_value(v) == toks


def test_addresses_are_fixed_width():
    assert tokens.addr(7) == ["@0", "@0", "@7"]
    assert tokens.addr(305) == ["@3", "@0", "@5"]


def _traces(n=150, seed=7):
    rng = random.Random(seed)
    for phase in "ABC":
        got = 0
        while got < n // 3:
            try:
                prog, trace = pipeline.prepare(grammar.generate(rng, phase), phase)
            except pipeline.Skip:
                continue
            got += 1
            yield prog, trace


def test_state_round_trip():
    for prog, trace in _traces():
        for st in trace.states:
            toks = tokens.enc_state(st)
            back, end = tokens.parse_state(toks)
            assert end == len(toks) and back.same(st)


def test_parser_rejects_non_canonical():
    base = ["<state>", "ip", "@0", "@0", "@1", "stack"]
    for bad in (["i+", "0", "0"], ["i-", "0"], ["i+"], ["N0"]):
        with pytest.raises(tokens.ParseError):
            tokens.parse_state(base + bad + ["names", "</state>"])
    with pytest.raises(tokens.ParseError):
        tokens.parse_state(base + ["names", "N1", "i+", "1", "N0", "i+", "2", "</state>"])


def test_grammar_accepts_every_gold_output_and_masks_allow_it():
    with_work = 0
    for prog, trace in _traces():
        for i in range(trace.steps):
            st = trace.states[i]
            ins = prog.instrs[st.ip]
            work = tokens.enc_work(ins, st)
            with_work += bool(work)
            out = work + tokens.enc_state(trace.states[i + 1]) + tokens.enc_out(trace.outs[i]) + ["<eos>"]
            g = decoding.OutputGrammar(len(prog.instrs), len(prog.names), work=tokens.work_kind(ins, st))
            for t in out:
                assert tokens.TOKEN_ID[t] in g.allowed(), (t, out)
                g.feed(t)
            assert g.done
            nxt, text, end = tokens.parse_step_output(out)
            assert end == len(out) and nxt.same(trace.states[i + 1]) and text == trace.outs[i]
    assert with_work > 10


def test_work_section():
    prog = support.check_source("a = 754\nb = 13\nprint(a // b)\nprint(a % b)\nc = -659\nc %= 22\nd = a // b * 9 // 9\n", "A")
    trace = refvm.run(prog)
    works = []
    for st in trace.states[:-1]:
        w = tokens.enc_work(prog.instrs[st.ip], st)
        if w:
            works.append(" ".join(w))
            (q, p), end = tokens.parse_work(w)
            a, b = st.stack[-2], st.stack[-1]
            assert end == len(w) and q == a // b and p in (None, b * q)
    assert works == ["<work> i+ 5 8 </work>", "<work> i+ 5 8 op:* i+ 4 5 7 </work>",
                     "<work> i- 3 0 op:* i- 0 6 6 </work>", "<work> i+ 5 8 </work>", "<work> i+ 5 8 </work>"]


def test_grammar_enforces_the_work_section():
    ids = lambda *ts: {tokens.TOKEN_ID[t] for t in ts}  # noqa: E731
    assert decoding.OutputGrammar(5, 1).allowed() == ids("<state>")
    g = decoding.OutputGrammar(5, 1, work="%")
    assert g.allowed() == ids("<work>")
    g.feed("<work>")
    g.feed("i-")
    assert tokens.TOKEN_ID["0"] not in g.allowed()          # no -0
    g = decoding.OutputGrammar(5, 1, work="%")
    for t in ("<work>", "i+", "0"):
        g.feed(t)
    assert g.allowed() == ids("op:*")                        # 0 has no more digits; % needs the product
    for t in ("op:*", "i+", "0"):
        g.feed(t)
    assert g.allowed() == ids("</work>", *tokens.DIGITS)     # the product is LSB-first: 0 5 is 50
    g.feed("</work>")
    assert g.allowed() == ids("<state>")
    g = decoding.OutputGrammar(5, 1, work="//")
    for t in ("<work>", "i+", "5", "8"):
        g.feed(t)
    assert tokens.TOKEN_ID["</work>"] in g.allowed() and tokens.TOKEN_ID["op:*"] not in g.allowed()


def test_grammar_blocks_malformed():
    g = decoding.OutputGrammar(n_instrs=12, n_names=2)
    for t in ["<state>", "ip", "@0"]:
        g.feed(t)
    assert tokens.TOKEN_ID["@2"] not in g.allowed()  # ip 2xx > 11
    g.feed("@1")
    assert tokens.TOKEN_ID["@2"] not in g.allowed()  # 012 > 11
    g.feed("@1")
    g.feed("stack")
    g.feed("i-")
    g.feed("0")
    assert tokens.TOKEN_ID["names"] not in g.allowed()  # -0 is not canonical
    g.feed("5")
    g.feed("names")
    assert tokens.TOKEN_ID["N2"] not in g.allowed()
    g.feed("N1")
    g.feed("None")
    assert tokens.TOKEN_ID["N0"] not in g.allowed()  # names in order


def test_listing_encodes_every_argument():
    prog = support.check_source("x = None\nprint(x)\n", "A")
    text = " ".join(tokens.enc_listing(prog))
    assert "LOAD_CONST None" in text and "STORE_NAME N0" in text and "LOAD_NAME print" in text
    assert text.endswith("LOAD_CONST None @0 @0 @9 RETURN_VALUE </code>")


@pytest.mark.parametrize("work", [None, "//", "%"])
def test_grammar_has_no_dead_ends(work):
    """Random walks through the output grammar always have a token to take
    until <eos>: a dead end would leave a decoder with nothing to emit.
    (Walks may run long without ending: tuple values, reserved for phase D,
    nest without a bound.)"""
    rng = random.Random(0)
    digits_first = [t for t in decoding._DIGITS]
    for walk in range(300):
        g = decoding.OutputGrammar(n_instrs=rng.randint(1, 999), n_names=rng.randint(0, 32), work=work)
        for _ in range(3000):
            allowed = sorted(g.allowed())
            assert allowed, f"dead end in walk {walk}"
            # lean towards digits and characters so ints and strings reach their limits
            pref = [t for t in allowed if tokens.VOCAB[t] in digits_first or tokens.VOCAB[t].startswith("c:")]
            g.feed_id(rng.choice(pref) if pref and rng.random() < 0.8 else rng.choice(allowed))
            if g.done:
                break
