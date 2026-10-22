"""Synthetic probe: how learnable is string indexing s[i], in isolation, per output format?

Each example is `<bos> " c:.. " i± d.. op:[] => output <eos>` in the model's
encoding, trained with the same StepModel; loss on the output side.

  plain  " c:x "                               what the interpreter emits today
  walk   <work> c:h i+ 0 c:e i+ 1 ... c:x i+ k </work> " c:x "
         a scratch walk to the index, each character tagged with its index
         (from the end, i- 1, i- 2, ..., for negative i); every token is an
         easy copy, increment or comparison instead of one positional lookup

Strings are 1-48 characters, half from small alphabets (repetitive, like the
copy drill), half from all printable characters; i is uniform over [-len, len).

  uv run --extra train python scripts/index_probe.py --format walk --steps 3000
"""
import argparse
import queue
import threading
import time

import numpy as np
import torch
import torch.nn.functional as F

from bcvm import tokens
from bcvm.gen.common import PATTERN_ALPHABETS, PRINTABLE
from bcvm.train.model import ModelConfig, StepModel
from bcvm.train.train import cap_gpu_memory

T = tokens.TOKEN_ID


def int_toks(v):
    return [T["i-" if v < 0 else "i+"]] + [T[c] for c in str(abs(v))[::-1]]


def str_toks(s):
    return [T['"']] + [T[f"c:{c}"] for c in s] + [T['"']]


def sample(rng):
    n = int(rng.integers(1, 49))
    alphabet = PATTERN_ALPHABETS[rng.integers(len(PATTERN_ALPHABETS))] if rng.random() < 0.5 else PRINTABLE
    s = "".join(alphabet[k] for k in rng.integers(0, len(alphabet), n))
    return s, int(rng.integers(-n, n))


def encode(s, i, fmt):
    inp = [T["<bos>"]] + str_toks(s) + int_toks(i) + [T["op:[]"], T["=>"]]
    out = []
    if fmt == "walk":
        out.append(T["<work>"])
        idx = range(0, i + 1) if i >= 0 else range(-1, i - 1, -1)
        for k in idx:
            out += [T[f"c:{s[k]}"]] + int_toks(k)
        out.append(T["</work>"])
    return inp, out + str_toks(s[i]) + [T["<eos>"]]


def batch(rng, n, fmt, seq):
    ids = np.full((n, seq), T["<pad>"], np.int64)
    tgt = np.full((n, seq), -1, np.int64)
    meta = np.zeros((n, 2), np.int64)
    for r in range(n):
        s, i = sample(rng)
        inp, out = encode(s, i, fmt)
        x = inp + out
        ids[r, :len(x)] = x
        tgt[r, len(inp) - 1:len(x) - 1] = out
        meta[r] = len(s), i
    return ids, tgt, meta


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--format", default="plain", choices=["plain", "walk"])
    p.add_argument("--steps", type=int, default=3000)
    p.add_argument("--batch", type=int, default=512)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--eval-every", type=int, default=500)
    p.add_argument("--eval-n", type=int, default=50_000)
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args()
    seq = 64 if a.format == "plain" else 256

    torch.manual_seed(a.seed)
    cap_gpu_memory()
    model = StepModel(ModelConfig(max_pos=seq)).cuda()
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1, fused=True)
    cm = torch.compile(model)
    causal = torch.ones(seq, seq, dtype=torch.bool, device="cuda").tril()[None, None]
    pos = torch.arange(seq, device="cuda")[None]

    q = queue.Queue(maxsize=8)

    def producer(seed):
        rng = np.random.default_rng(seed)
        while True:
            q.put(batch(rng, a.batch, a.format, seq))

    for w in range(4):
        threading.Thread(target=producer, args=(a.seed * 100 + w + 1,), daemon=True).start()
    ev = batch(np.random.default_rng(10_000 + a.seed), a.eval_n, a.format, seq)

    def evaluate():
        ids, tgt, meta = ev
        wrong = np.zeros(len(ids), bool)
        with torch.no_grad(), torch.autocast("cuda", torch.bfloat16):
            for s in range(0, len(ids), a.batch):
                x = torch.from_numpy(ids[s:s + a.batch]).cuda()
                t = torch.from_numpy(tgt[s:s + a.batch]).cuda()
                pred = cm(x, pos.expand_as(x), causal).argmax(-1)
                wrong[s:s + a.batch] = (((pred != t) & (t >= 0)).any(-1)).cpu().numpy()
        n, i = meta[:, 0], meta[:, 1]
        k = np.where(i >= 0, i, -i - 1)   # distance walked
        parts = [f"|i|<8 {wrong[k < 8].mean():.2e}", f"8-23 {wrong[(k >= 8) & (k < 24)].mean():.2e}",
                 f"24+ {wrong[k >= 24].mean():.2e}", f"neg {wrong[i < 0].mean():.2e}"]
        return wrong.mean(), "  ".join(parts)

    t0 = time.time()
    for step in range(1, a.steps + 1):
        lr = a.lr * min(1, step / 100) * (0.1 + 0.9 * 0.5 * (1 + np.cos(np.pi * step / a.steps)))
        for g in opt.param_groups:
            g["lr"] = lr
        ids, tgt, _ = q.get()
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
            print(f"[{a.format}] step {step} | {step * a.batch / 1e6:.2f}M examples | loss {loss.item():.5f} | "
                  f"err {err:.2e} | {detail} | {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
