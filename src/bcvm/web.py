"""The runner for the web demo: harness.run with an async model and exact
speculative decoding. Pure Python, so the same code runs natively (tests,
train/export.OrtModel) and in the browser under Pyodide (a JS model).

The model is any object with

    await prefill(ids)                  start a script: cache the listing, no step
    await forward(ids, masks, temperature=0) -> list[int]
        feed ids after the cached tokens and cache them; masks is a bytes-like
        of len(ids) * VOCAB_SIZE (1 = allowed). Returns, after each fed token,
        the masked argmax (or a sample at temperature > 0), -1 where a
        position's mask is all zeros
    truncate(n)                         keep the listing and the first n step tokens

Greedy decoding drafts the rest of a step by prompt lookup: find the newest
generated tokens in the input state (or the listing) and propose what follows
there. The draft is verified in one forward pass and kept only as far as it
equals the model's own masked argmax, so the result is exactly greedy
decoding, in a few passes per step instead of one per token. Nothing about
the draft comes from the reference interpreter.
"""
import copy

from . import harness, refvm, support, tokens
from .decoding import OutputGrammar
from .program import CompileError, Program

V = tokens.VOCAB_SIZE
EOS = tokens.TOKEN_ID["<eos>"]


def _masks(sets):
    """Pack allowed-id sets (None = don't care) into the forward() mask format."""
    buf = bytearray(len(sets) * V)
    for j, s in enumerate(sets):
        if s:
            base = j * V
            for t in s:
                buf[base + t] = 1
    return buf


_ANCHORS = {tokens.TOKEN_ID[t] for t in ["<state>", "ip", "stack", "names", "</state>"]
            + [t for t in tokens.VOCAB if t[:1] == "N" and t[1:].isdigit()]}


def _follow(src, tail, max_draft):
    """What follows the latest occurrence of `tail` in `src`."""
    n = len(tail)
    for i in range(len(src) - n, -1, -1):
        if src[i:i + n] == tail and i + n < len(src):
            return src[i + n:i + n + max_draft]
    return []


def _realign(out, state, max_draft):
    """Find the newest structural token of `out` (ip, stack, names, N<k>, ...) in
    the input state and assume the tokens since it replaced as many input
    tokens (a changed ip digit or a value of the same length)."""
    for back in range(len(out) - 1, -1, -1):
        if out[back] in _ANCHORS:
            if out[back] not in state:
                return []
            at = state.index(out[back]) + len(out) - back
            return state[at:at + max_draft]
    return []


_VALUE_START = {tokens.TOKEN_ID[t] for t in ("i+", "i-", '"')}


def _draft(out, sources, allowed, max_draft):
    """Prompt lookup over the step's sources: the input state (with the ip
    moved to the next instruction, the usual successor), the current
    instruction (its listing entry, then the input values of names it
    refers to: what a push copies), the whole listing. The first draft whose
    first token the grammar allows wins; a wrong draft costs no extra pass,
    since every pass yields at least the model's own next token."""
    state, ins, listing = sources
    tails = [out[-n:] for n in (3, 2) if len(out) >= n]
    from_ins = [_follow(ins, out[-n:], max_draft) for n in (2, 1) if len(out) >= n]
    cands = from_ins if out[-1] in _VALUE_START else []
    cands += [_follow(state, t, max_draft) for t in tails]
    cands.append(_realign(out, state, max_draft))
    cands += from_ins
    cands += [_follow(listing, t, max_draft) for t in tails]
    cands += [_follow(src, out[-1:], max_draft) for src in (state, listing)]
    for c in cands:
        if c and c[0] in allowed:
            return c
    return []


class Stats:
    def __init__(self):
        self.steps = self.forwards = self.tokens = self.drafted = self.accepted = 0


async def decode_greedy(model, state_ids, grammar, sources, stats, max_draft=48):
    """sources: (input state as a draft, current instruction's tokens, listing), see _draft."""
    model.truncate(0)
    res = await model.forward(state_ids, _masks([None] * (len(state_ids) - 1) + [grammar.allowed()]))
    stats.forwards += 1
    cached = len(state_ids)
    nxt, out = res[-1], []
    while True:
        grammar.feed_id(nxt)
        out.append(nxt)
        if grammar.done:
            break
        # walk a copy of the grammar along the draft: the mask after each fed token
        sets = [grammar.allowed()]
        draft = _draft(out, sources, sets[0], max_draft)
        g, kept = copy.deepcopy(grammar), []
        for d in draft:
            if d not in sets[-1]:
                break
            g.feed_id(d)
            kept.append(d)
            if g.done:
                break
            sets.append(g.allowed())
        feed = [nxt] + kept
        res = await model.forward(feed, _masks(sets + [None] * (len(feed) - len(sets))))
        stats.forwards += 1
        stats.drafted += len(kept)
        m = 0
        while m < len(kept) and res[m] == kept[m]:
            grammar.feed_id(kept[m])
            out.append(kept[m])
            m += 1
            if grammar.done:
                break
        stats.accepted += m
        if grammar.done:
            break
        cached += 1 + m
        model.truncate(cached)
        nxt = res[m]
    stats.tokens += len(out)
    return out


async def decode_sampled(model, state_ids, grammar, stats, temperature=1.0):
    model.truncate(0)
    res = await model.forward(state_ids, _masks([None] * (len(state_ids) - 1) + [grammar.allowed()]), temperature)
    stats.forwards += 1
    out = []
    while True:
        nxt = res[-1]
        grammar.feed_id(nxt)
        out.append(nxt)
        if grammar.done:
            break
        res = await model.forward([nxt], _masks([grammar.allowed()]), temperature)
        stats.forwards += 1
    stats.tokens += len(out)
    return out


async def run(src, phase, model, candidates=3, max_steps=10_000, on_step=None, stats=None):
    """harness.run with the model: refuse unsupported scripts, then step until
    the module returns. on_step(i, state, printed) is called for each accepted
    step (state is the refvm.State after it). Returns a harness.RunResult."""
    res = harness.RunResult()
    stats = stats if stats is not None else Stats()
    try:
        prog = Program(src)
        support.check(prog, phase)
    except (support.Refusal, CompileError) as e:
        res.refused = str(e)
        return res
    listing = tokens.ids(["<bos>"] + tokens.enc_listing(prog))
    await model.prefill(listing)
    st = refvm.State(0, (), {})
    while prog.instrs[st.ip].opname != "RETURN_VALUE":
        if res.steps >= max_steps:
            res.error = f"stopped after {max_steps} steps"
            return res
        state_ids = tokens.ids(tokens.enc_state(st) + ["=>"])
        work = tokens.work_kind(prog.instrs[st.ip], st)
        accepted = None
        for k in range(candidates):
            grammar = OutputGrammar(len(prog.instrs), len(prog.names), work=work)
            if k == 0:
                nxt_ip = st.ip + 1 if st.ip + 1 < len(prog.instrs) else st.ip
                guess = tokens.ids(tokens.enc_state(refvm.State(nxt_ip, st.stack, st.names)))
                ins = tokens.ids(tokens.enc_instr(prog.instrs[st.ip]))
                for t in [t for t in ins if t in _ANCHORS]:     # N<k>: append its input value
                    ins += _follow(state_ids, [t], 64)
                out = await decode_greedy(model, state_ids, grammar, (guess, ins, listing), stats)
            else:
                out = await decode_sampled(model, state_ids, grammar, stats)
            cand = [tokens.VOCAB[t] for t in out]
            try:
                nxt, printed, end = tokens.parse_step_output(cand)
                if end != len(cand):
                    raise tokens.ParseError("tokens after <eos>")
                reason = harness.validate(prog, st, nxt, printed)
            except tokens.ParseError as e:
                reason = f"malformed: {e}"
            if reason is None:
                accepted = (nxt, printed)
                if k:
                    res.rescued += 1
                break
            res.rejected += 1
            if len(res.rejections) < 20:
                res.rejections.append((res.steps, reason))
        if accepted is None:
            res.error = f"step {res.steps}: every candidate failed validation ({res.rejections[-1][1]})"
            return res
        st, printed = accepted
        res.stdout += printed
        if on_step is not None:
            on_step(res.steps, st, printed)
        res.steps += 1
        stats.steps += 1
    return res
