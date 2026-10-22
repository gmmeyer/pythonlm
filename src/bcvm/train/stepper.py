"""The trained model behind harness.run's stepper interface, plus the gate.

Many scripts run at once, one harness.run per thread. Each thread owns a slot
of a shared KV cache; propose() hands the engine a request and blocks. When
every running thread is waiting, the engine serves them all as one batch:
prefill new listings (once per program), then the input states, then decode
each step's output token by token under decoding.OutputGrammar masks.
Candidate 1 is greedy; later candidates are sampled, and only decoded when
the validator rejected the earlier ones.

Cache index = RoPE position: the listing sits at [0, listing_len) and the
current step right after it, so a query at position p attends to [0, p].

  bcvm gate $BCVM_DATA/runs/a1/final.pt phaseA/eval_test
  bcvm run script.py --ckpt $BCVM_DATA/runs/a1/final.pt
"""
import json
import os
import re
import sys
import threading
import time
from collections import Counter

import numpy as np
import torch

from .. import config, harness, refvm, tokens
from ..decoding import OutputGrammar
from ..shards import list_shards

PAD = tokens.TOKEN_ID["<pad>"]
V = tokens.VOCAB_SIZE


class _LayerCache:
    def __init__(self, shape, dtype, dev):
        self.k = torch.zeros(shape, dtype=dtype, device=dev)
        self.v = torch.zeros(shape, dtype=dtype, device=dev)
        self.rows = self.at = self.span = None

    def update(self, k, v):
        """Write the new keys/values of batch rows `rows` at positions `at` [b, T];
        return what the queries attend to: the new tokens alone (listing
        prefill, span None) or the cache up to `span`."""
        idx = (self.rows[:, None], slice(None), self.at)
        self.k[idx] = k.transpose(1, 2).to(self.k.dtype)
        self.v[idx] = v.transpose(1, 2).to(self.v.dtype)
        if self.span is None:
            return k, v
        return self.k[:, :, :self.span], self.v[:, :, :self.span]


class _Request:
    __slots__ = ("slot", "prog", "listing", "state", "sample", "result", "done")

    def __init__(self, slot, prog, listing, state, sample):
        self.slot, self.prog, self.listing, self.state, self.sample = slot, prog, listing, state, sample
        self.result = None
        self.done = threading.Event()


class Engine:
    def __init__(self, model, n_slots, temperature=1.0, seed=0):
        self.model = model.eval()
        cfg = model.cfg
        self.dev = next(model.parameters()).device
        self.cuda = self.dev.type == "cuda"
        self.S = cfg.max_pos
        shape = (n_slots, cfg.n_heads, self.S, cfg.d_model // cfg.n_heads)
        dtype = torch.bfloat16 if self.cuda else torch.float32
        self.cache = [_LayerCache(shape, dtype, self.dev) for _ in range(cfg.n_layers)]
        self.n = n_slots
        self.all_rows = torch.arange(n_slots, device=self.dev)
        self.listing = [None] * n_slots     # the listing object each slot holds
        self.ll = np.zeros(n_slots, np.int64)
        self.temperature = temperature
        self.gen = torch.Generator(device=self.dev).manual_seed(seed)
        self.cv = threading.Condition()
        self.pending = []
        self.live = 0
        self.forwards = 0

    # ------------------------------------------------ called from script threads
    def request(self, slot, prog, listing, state, sample):
        r = _Request(slot, prog, listing, state, sample)
        with self.cv:
            self.pending.append(r)
            self.cv.notify_all()
        r.done.wait()
        if isinstance(r.result, BaseException):
            raise RuntimeError("engine failed") from r.result
        return r.result

    def run_all(self, jobs, fn):
        """fn(job, stepper) for every job, over up to n_slots threads; returns results in order."""
        jobs = list(jobs)
        results = [None] * len(jobs)
        it = iter(enumerate(jobs))
        lock = threading.Lock()

        def worker(slot):
            stepper = ModelStepper(self, slot)
            try:
                while True:
                    with lock:
                        nxt = next(it, None)
                    if nxt is None:
                        return
                    i, job = nxt
                    try:
                        results[i] = fn(job, stepper)
                    except Exception as e:  # noqa: BLE001
                        results[i] = e
            finally:
                with self.cv:
                    self.live -= 1
                    self.cv.notify_all()

        n = min(self.n, len(jobs))
        self.live = n
        threads = [threading.Thread(target=worker, args=(s,), daemon=True) for s in range(n)]
        for t in threads:
            t.start()
        self.serve()
        for t in threads:
            t.join()
        return results

    # ------------------------------------------------ the serving loop
    def serve(self):
        while True:
            with self.cv:
                self.cv.wait_for(lambda: len(self.pending) >= self.live)
                if not self.pending:
                    return
                reqs, self.pending = self.pending, []
            try:
                with torch.no_grad(), torch.autocast("cuda", torch.bfloat16, enabled=self.cuda):
                    self._serve(reqs)
            except BaseException as e:
                for r in reqs:
                    r.result = e
                raise
            finally:
                for r in reqs:
                    r.done.set()

    def _serve(self, reqs):
        new = [r for r in reqs if self.listing[r.slot] is not r.listing]
        if new:
            self._prefill_listings(new)
        self._decode(reqs)

    def _prefill_listings(self, reqs):
        L = max(len(r.listing) for r in reqs)
        ids = np.full((len(reqs), L), PAD, np.int64)
        for i, r in enumerate(reqs):
            ids[i, :len(r.listing)] = tokens.ids(r.listing)
        pos = torch.arange(L, device=self.dev).expand(len(reqs), L)
        rows = torch.tensor([r.slot for r in reqs], device=self.dev)
        for c in self.cache:
            c.rows, c.at, c.span = rows, pos, None
        causal = torch.ones(L, L, dtype=torch.bool, device=self.dev).tril()[None, None]
        self.model(torch.from_numpy(ids).to(self.dev), pos, causal, self.cache)
        self.forwards += 1
        for r in reqs:
            self.listing[r.slot] = r.listing
            self.ll[r.slot] = len(r.listing)

    def _forward(self, ids, pos):
        ids = torch.from_numpy(ids).to(self.dev, non_blocking=True)
        pos = torch.from_numpy(pos).to(self.dev, non_blocking=True)
        span = int(pos.max()) + 1
        for c in self.cache:
            c.rows, c.at, c.span = self.all_rows, pos, span
        mask = (torch.arange(span, device=self.dev) <= pos[:, :, None])[:, None]
        self.forwards += 1
        return self.model(ids, pos, mask, self.cache).float()

    def _decode(self, reqs):
        B, S = self.n, self.S
        states = {r.slot: tokens.ids(r.state) for r in reqs}
        lens = np.zeros(B, np.int64)
        for s, st in states.items():
            lens[s] = len(st)
        T = int(lens.max())
        ids = np.full((B, T), PAD, np.int64)
        for s, st in states.items():
            ids[s, :len(st)] = st
        pos = np.minimum(self.ll[:, None] + np.arange(T), S - 1)
        logits = self._forward(ids, pos)[self.all_rows, torch.from_numpy(np.maximum(lens - 1, 0)).to(self.dev)]
        cur = np.minimum(self.ll + lens, S - 1)
        grammar = {r.slot: OutputGrammar(len(r.prog.instrs), len(r.prog.names)) for r in reqs}
        out = {r.slot: [] for r in reqs}
        sample = torch.zeros(B, dtype=torch.bool)
        sample[[r.slot for r in reqs if r.sample]] = True
        sample = sample.to(self.dev)
        any_sample = any(r.sample for r in reqs)
        active = [r.slot for r in reqs]
        while active:
            allow = np.zeros((B, V), bool)
            allow[:, PAD] = True
            for s in active:
                allow[s, PAD] = False
                allow[s, list(grammar[s].allowed())] = True
            lg = logits.masked_fill(~torch.from_numpy(allow).to(self.dev), float("-inf"))
            tok = lg.argmax(-1)
            if any_sample:
                probs = torch.softmax(lg / self.temperature, -1)
                tok = torch.where(sample, torch.multinomial(probs, 1, generator=self.gen)[:, 0], tok)
            nxt = tok.tolist()
            still = []
            for s in active:
                grammar[s].feed_id(nxt[s])
                out[s].append(tokens.VOCAB[nxt[s]])
                if not grammar[s].done and cur[s] < S - 1:
                    still.append(s)
            active = still
            if active:
                logits = self._forward(np.array(nxt, np.int64)[:, None], cur[:, None].copy())[:, 0]
                cur[active] += 1
        for r in reqs:
            r.result = out[r.slot]


class ModelStepper:
    """harness.run's stepper for one engine slot. It also follows the true
    trace with the reference interpreter and records the first step whose
    accepted state is wrong, which gives a free-running per-step error."""

    def __init__(self, engine, slot):
        self.engine, self.slot = engine, slot
        self.reset(None)

    def reset(self, listing):
        self.listing = listing
        self.steps = 0
        self.expect = None
        self.prev_ip = None
        self.diverged = None    # (step, opcode) of the first wrong accepted state

    def propose(self, prog, listing_tokens, state_tokens, n):
        if listing_tokens is not self.listing:
            self.reset(listing_tokens)
        self._track(prog, state_tokens)
        return self._candidates(prog, listing_tokens, state_tokens, n)

    def _candidates(self, prog, listing, state, n):
        for k in range(n):
            yield self.engine.request(self.slot, prog, listing, state, sample=k > 0)

    def _track(self, prog, state_tokens):
        if self.diverged is None:
            st, _ = tokens.parse_state(state_tokens)
            if self.expect is not None and not st.same(self.expect):
                self.diverged = (self.steps - 1, _kind(prog.instrs[self.prev_ip]))
            else:
                self.expect, _ = refvm.step(prog, st)
                self.prev_ip = st.ip
        self.steps += 1


def _kind(ins):
    """Same labels as data.step_kind: the opcode, with its operator for BINARY_OP and COMPARE_OP."""
    if ins.opname == "BINARY_OP":
        return f"BINARY_OP op:{ins.arg}"
    if ins.opname == "COMPARE_OP":
        return f"COMPARE_OP cmp:{ins.arg}"
    return ins.opname


# ---------------------------------------------------------------- gate

def load_records(directory, limit=None):
    from compression import zstd
    recs = []
    for stem in list_shards(directory):
        with zstd.open(stem + ".records.jsonl.zst", "rt") as f:
            for line in f:
                recs.append(json.loads(line))
                if limit and len(recs) >= limit:
                    return recs
    return recs


def _phase_of(path):
    m = re.search(r"phase([A-Z])", path)
    if not m:
        raise SystemExit(f"can't tell the phase from {path}; pass --phase")
    return m.group(1)


def _run_one(rec, stepper, phase, candidates):
    stepper.reset(None)
    res = harness.run(rec["src"], phase, stepper, max_steps=max(10_000, 2 * rec["steps"]), candidates=candidates)
    return res, stepper.diverged, stepper.steps


def gate(a):
    from .train import load_model
    model, ck = load_model(a.ckpt)
    path = os.path.join(config.DATA_DIR, a.set)
    phase = a.phase or _phase_of(a.set)
    recs = load_records(path, a.limit)
    engine = Engine(model, min(a.slots, len(recs)), temperature=a.temperature, seed=a.seed)
    print(f"gate {a.set} (phase {phase}): {len(recs)} scripts, ckpt step {ck['step']}, {engine.n} slots", flush=True)
    t0 = time.time()
    results = engine.run_all(recs, lambda rec, st: _run_one(rec, st, phase, a.candidates))
    dt = time.time() - t0

    n = len(recs)
    match = refused = errors = crashed = rejected = rescued = steps = 0
    tracked = diverged = 0
    div_ops = Counter()
    buckets = {}
    failures = []
    for rec, out in zip(recs, results):
        if isinstance(out, Exception):
            crashed += 1
            failures.append(dict(src=rec["src"], crash=repr(out)))
            continue
        res, div, n_tracked = out
        ok = res.refused is None and res.error is None and res.stdout == rec["stdout"]
        match += ok
        refused += res.refused is not None
        errors += res.error is not None
        rejected += res.rejected
        rescued += res.rescued
        steps += res.steps
        tracked += div[0] + 1 if div else n_tracked
        if div:
            diverged += 1
            div_ops[div[1]] += 1
        b = 100 if rec["steps"] <= 100 else 1000 if rec["steps"] <= 1000 else 10_000
        buckets.setdefault(b, [0, 0])
        buckets[b][0] += 1
        buckets[b][1] += ok
        if not ok and len(failures) < a.keep_failures:
            failures.append(dict(src=rec["src"], want=rec["stdout"], got=res.stdout, refused=res.refused,
                                 error=res.error, diverged=div, rejections=res.rejections[:5]))
    step_err = diverged / max(1, tracked)
    summary = dict(set=a.set, ckpt=a.ckpt, ckpt_step=ck["step"], scripts=n, match=match, match_rate=match / n,
                   refused=refused, errors=errors, crashed=crashed, steps=steps, rejected=rejected, rescued=rescued,
                   safeguard_rate=rejected / max(1, steps), diverged=diverged, step_err=step_err,
                   divergence_by_opcode=dict(div_ops.most_common()),
                   by_length={f"<={k}": dict(n=v[0], match=v[1], rate=v[1] / v[0]) for k, v in sorted(buckets.items())},
                   seconds=dt, steps_per_s=steps / dt)
    print(f"stdout match {match}/{n} = {match / n:.4%} | refused {refused} | validator stops {errors} | crashed {crashed}")
    print(f"steps {steps} ({steps / dt:.0f}/s, {engine.forwards} forwards) | rejected {rejected} "
          f"(safeguard rate {rejected / max(1, steps):.2e}) | rescued {rescued}")
    print(f"free-running step error {step_err:.2e} ({diverged} divergences in {tracked} steps) "
          f"| by opcode {dict(div_ops.most_common(8))}")
    print("by length " + "  ".join(f"<={k}: {v[1]}/{v[0]}" for k, v in sorted(buckets.items())))
    if a.json:
        with open(a.json, "w") as f:
            json.dump(dict(summary, failures=failures), f, indent=1)
    return summary


def run_script(path, ckpt, phase=None):
    """bcvm run --ckpt: one script through the harness with the model, streaming stdout."""
    from ..cli import _phase_for
    from .train import load_model
    src = open(path).read()
    phase = phase or _phase_for(src) or "C"
    model, _ = load_model(ckpt)
    engine = Engine(model, 1)
    res = engine.run_all([src], lambda s, st: harness.run(s, phase, st, stream=sys.stdout))[0]
    if isinstance(res, Exception):
        raise res
    if res.refused:
        print(f"refused: {res.refused}", file=sys.stderr)
        return 2
    if res.error:
        print(f"error: {res.error}", file=sys.stderr)
        return 1
    if res.rejected:
        print(f"[{res.steps} steps, {res.rejected} candidates rejected, {res.rescued} rescued]", file=sys.stderr)
    return 0
