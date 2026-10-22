"""bcvm.web: the demo's runner with an async model and speculative decoding."""
import asyncio
import hashlib
import os

import pytest

from bcvm import pipeline, refvm, tokens, web
from bcvm.decoding import OutputGrammar

HANDWRITTEN = os.path.join(os.path.dirname(__file__), "..", "eval", "handwritten")
V = tokens.VOCAB_SIZE


class FakeModel:
    """Deterministic stand-in for the network with web.run's model interface.
    Its next token follows the reference trace, except at positions a hash of
    the history picks (rate `noise`), where it takes another allowed token, so
    drafts are both accepted and rejected."""

    def __init__(self, prog_of, noise=0.0):
        self.prog_of, self.noise = prog_of, noise
        self.forwards = 0

    async def prefill(self, ids):
        self.listing, self.step = list(ids), []
        self.prog = self.prog_of(tuple(ids))

    def truncate(self, n):
        del self.step[n:]

    def _truth(self):
        """The true output tokens for the state in self.step, or None."""
        try:
            end = self.step.index(tokens.TOKEN_ID["=>"])
        except ValueError:
            return None
        st, _ = tokens.parse_state([tokens.VOCAB[t] for t in self.step[:end]])
        nxt, out = refvm.step(self.prog, st)
        return self.step[end + 1:], tokens.ids(tokens.enc_work(self.prog.instrs[st.ip], st) + tokens.enc_state(nxt)
                                              + tokens.enc_out(out) + ["<eos>"])

    async def forward(self, ids, masks, temperature=0):
        self.forwards += 1
        res = []
        for j, t in enumerate(ids):
            self.step.append(t)
            allowed = [k for k in range(V) if masks[j * V + k]]
            if not allowed:
                res.append(-1)
                continue
            pick = allowed[0]
            truth = self._truth()
            if truth is not None:
                done, full = truth
                if full[:len(done)] == done and len(done) < len(full) and full[len(done)] in allowed:
                    pick = full[len(done)]
            h = int.from_bytes(hashlib.blake2b(bytes(str(self.listing + self.step), "ascii")).digest()[:4], "little")
            if h / 2 ** 32 < self.noise:
                pick = allowed[h % len(allowed)]
            res.append(pick)
        return res


def _scripts(phase, n):
    d = os.path.join(HANDWRITTEN, f"phase{phase}")
    return [open(os.path.join(d, f)).read() for f in sorted(os.listdir(d))[:n]]


def _progs(srcs, phase):
    progs = {}
    for src in srcs:
        prog, _ = pipeline.prepare(src, phase, max_steps=10_000)
        progs[tuple(tokens.ids(["<bos>"] + tokens.enc_listing(prog)))] = prog
    return progs.__getitem__


@pytest.mark.parametrize("phase", "ABC")
def test_runner_reproduces_stdout_with_a_perfect_model(phase):
    srcs = _scripts(phase, 6)
    model = FakeModel(_progs(srcs, phase))
    stats = web.Stats()
    for src in srcs:
        _, trace = pipeline.prepare(src, phase, max_steps=10_000)
        res = asyncio.run(web.run(src, phase, model, stats=stats))
        assert res.error is None and res.stdout == trace.stdout and res.steps == trace.steps
    assert stats.forwards < stats.tokens / 3      # speculation: a few passes per step, not one per token


@pytest.mark.parametrize("phase", "ABC")
def test_speculative_decoding_equals_plain_greedy(phase):
    """With drafts accepted and rejected (a noisy model), decode_greedy gives
    exactly what feeding one token at a time gives."""
    srcs = _scripts(phase, 3)
    progs = _progs(srcs, phase)
    for src in srcs:
        prog, trace = pipeline.prepare(src, phase, max_steps=10_000)
        listing = tokens.ids(["<bos>"] + tokens.enc_listing(prog))
        for st in trace.states[:-1][:40]:
            state_ids = tokens.ids(tokens.enc_state(st) + ["=>"])
            work = tokens.work_kind(prog.instrs[st.ip], st)
            guess = tokens.ids(tokens.enc_state(refvm.State(min(st.ip + 1, len(prog.instrs) - 1), st.stack, st.names)))
            ins = tokens.ids(tokens.enc_instr(prog.instrs[st.ip]))

            async def spec():
                m = FakeModel(progs, noise=0.15)
                await m.prefill(listing)
                g = OutputGrammar(len(prog.instrs), len(prog.names), work=work)
                return await web.decode_greedy(m, state_ids, g, (guess, ins, listing), web.Stats())

            async def plain():
                m = FakeModel(progs, noise=0.15)
                await m.prefill(listing)
                g = OutputGrammar(len(prog.instrs), len(prog.names), work=work)
                res = await m.forward(state_ids, web._masks([None] * (len(state_ids) - 1) + [g.allowed()]))
                out = []
                while True:
                    out.append(res[-1])
                    g.feed_id(res[-1])
                    if g.done:
                        return out
                    res = await m.forward([res[-1]], web._masks([g.allowed()]))

            assert asyncio.run(spec()) == asyncio.run(plain())


def test_refusal_needs_no_model():
    res = asyncio.run(web.run("xs = [1, 2]\nprint(xs)\n", "C", model=None))
    assert res.refused and res.steps == 0
