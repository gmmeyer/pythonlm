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
    for prog, trace in _traces():
        for i in range(trace.steps):
            out = tokens.enc_state(trace.states[i + 1]) + tokens.enc_out(trace.outs[i]) + ["<eos>"]
            g = decoding.OutputGrammar(len(prog.instrs), len(prog.names))
            for t in out:
                assert tokens.TOKEN_ID[t] in g.allowed(), (t, out)
                g.feed(t)
            assert g.done


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
