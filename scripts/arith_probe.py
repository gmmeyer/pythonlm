"""Synthetic probe: how learnable is one BINARY_OP result, in isolation, per output format?

Each example is `<bos> a b op => result <eos>` in the model's int encoding
(sign, digits least significant first), loss on the output side, trained with
the same StepModel. Formats for the output side:

  lsb    i± r(lsb)                         what the interpreter emits today
  msb    i± r(msb)                         result most significant digit first
  work   <r0> i± q(msb) <r1> i± r(lsb)     for // and %: the quotient MSB-first
                                           as scratch, then the usual result

Operands mimic the hard region of phase A: a in [-999, 999]; b with 1, 2 or 3
digits; products bounded by 999.

  uv run --extra train python scripts/arith_probe.py --format lsb --steps 2000
"""
import argparse
import queue
import threading
import time

import numpy as np
import torch
import torch.nn.functional as F

from bcvm import tokens
from bcvm.train.model import ModelConfig, StepModel
from bcvm.train.train import cap_gpu_memory

T = tokens.TOKEN_ID
OPS = ["//", "%", "*", "+"]
SEQ = 26
HARD_DIVISORS = {3, 6, 7, 8, 9}


def int_toks(v, msb=False):
    d = [T[c] for c in str(abs(v))]
    return [T["i-" if v < 0 else "i+"]] + (d if msb else d[::-1])


def sample(rng, n):
    ops = rng.integers(0, len(OPS), n)
    bdig = rng.choice([1, 2, 3], n, p=[0.45, 0.4, 0.15])
    b = rng.integers(np.where(bdig == 1, 1, np.where(bdig == 2, 10, 100)), np.array([10, 100, 1000])[bdig - 1])
    b = np.where(rng.random(n) < 0.2, -b, b)
    a = rng.integers(-999, 1000, n)
    mul = np.array(OPS)[ops] == "*"
    lim = 999 // np.abs(b)
    a = np.where(mul, rng.integers(-lim, lim + 1), a)
    return ops, a, b


def result(op, a, b):
    return {"//": a // b, "%": a % b, "*": a * b, "+": a + b}[op]


def encode(op, a, b, fmt):
    r = result(op, a, b)
    inp = [T["<bos>"]] + int_toks(a) + int_toks(b) + [T[f"op:{op}"], T["=>"]]
    if fmt == "msb":
        out = int_toks(r, msb=True)
    elif fmt == "work" and op in ("//", "%"):
        out = [T["<r0>"]] + int_toks(a // b, msb=True) + [T["<r1>"]] + int_toks(r)
    else:
        out = int_toks(r)
    return inp, out + [T["<eos>"]]


def batch(rng, n, fmt):
    ops, a, b = sample(rng, n)
    ids = np.full((n, SEQ), T["<pad>"], np.int64)
    tgt = np.full((n, SEQ), -1, np.int64)
    for i in range(n):
        inp, out = encode(OPS[ops[i]], int(a[i]), int(b[i]), fmt)
        seq = inp + out
        ids[i, :len(seq)] = seq
        tgt[i, len(inp) - 1:len(seq) - 1] = out
    return ids, tgt, ops, a, b


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--format", default="lsb", choices=["lsb", "msb", "work"])
    p.add_argument("--steps", type=int, default=2000)
    p.add_argument("--batch", type=int, default=2048)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--layers", type=int, default=8)
    p.add_argument("--d-model", type=int, default=512)
    p.add_argument("--eval-every", type=int, default=250)
    p.add_argument("--eval-n", type=int, default=200_000)
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args()

    torch.manual_seed(a.seed)
    cap_gpu_memory()
    model = StepModel(ModelConfig(d_model=a.d_model, n_layers=a.layers, n_heads=a.d_model // 64,
                                  d_ff=a.d_model * 11 // 4, max_pos=SEQ)).cuda()
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1, fused=True)
    cm = torch.compile(model)
    causal = torch.ones(SEQ, SEQ, dtype=torch.bool, device="cuda").tril()[None, None]
    pos = torch.arange(SEQ, device="cuda")[None]

    q = queue.Queue(maxsize=8)

    def producer(seed):
        rng = np.random.default_rng(seed)
        while True:
            q.put(batch(rng, a.batch, a.format))

    for w in range(3):
        threading.Thread(target=producer, args=(a.seed * 100 + w + 1,), daemon=True).start()
    ev = batch(np.random.default_rng(10_000 + a.seed), a.eval_n, a.format)

    def evaluate():
        ids, tgt, ops, xa, xb = ev
        wrong = np.zeros(len(ids), bool)
        with torch.no_grad(), torch.autocast("cuda", torch.bfloat16):
            for s in range(0, len(ids), a.batch):
                x = torch.from_numpy(ids[s:s + a.batch]).cuda()
                t = torch.from_numpy(tgt[s:s + a.batch]).cuda()
                pred = cm(x, pos.expand_as(x), causal).argmax(-1)
                wrong[s:s + a.batch] = (((pred != t) & (t >= 0)).any(-1)).cpu().numpy()
        parts = []
        for k, op in enumerate(OPS):
            sel = ops == k
            parts.append(f"{op} {wrong[sel].mean():.2e}")
            if op in ("//", "%"):
                hard = sel & (np.abs(xa) >= 100) & np.isin(np.abs(xb), list(HARD_DIVISORS))
                two = sel & (np.abs(xa) >= 100) & (np.abs(xb) >= 10) & (np.abs(xb) < 100)
                parts.append(f"[3-digit / 3,6-9: {wrong[hard].mean():.2e}, / 2-digit: {wrong[two].mean():.2e}]")
        return wrong.mean(), "  ".join(parts)

    t0 = time.time()
    for step in range(1, a.steps + 1):
        frac = step / a.steps
        lr = a.lr * min(1, step / 100) * (0.1 + 0.9 * 0.5 * (1 + np.cos(np.pi * frac)))
        for g in opt.param_groups:
            g["lr"] = lr
        ids, tgt, *_ = q.get()
        x, t = torch.from_numpy(ids).cuda(non_blocking=True), torch.from_numpy(tgt).cuda(non_blocking=True)
        with torch.autocast("cuda", torch.bfloat16):
            logits = cm(x, pos.expand_as(x), causal)
        loss = F.cross_entropy(logits.float().flatten(0, 1), t.flatten(), ignore_index=-1)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        opt.zero_grad(set_to_none=True)
        if step % a.eval_every == 0 or step == a.steps:
            err, detail = evaluate()
            per_op = step * a.batch / len(OPS)
            print(f"[{a.format}] step {step} | {per_op / 1e6:.2f}M examples/op | loss {loss.item():.5f} | "
                  f"err {err:.2e} | {detail} | {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
