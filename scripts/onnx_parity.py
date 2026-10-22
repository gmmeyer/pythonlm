"""Check an ONNX export against the PyTorch checkpoint on real steps: the
hand-written scripts, traced by the reference VM, each step teacher-forced
after a listing prefill through the cache (as the browser runs it). Reports
the largest logit difference, argmax agreement, and per-step exactness
(every output token's argmax right) for both.

  uv run --extra train --extra export python scripts/onnx_parity.py \
      $BCVM_DATA/runs/c2/final.pt out/c2.onnx --steps-per-script 8
"""
import argparse
import os
import random

import numpy as np
import torch

from bcvm import pipeline, refvm, tokens
from bcvm.train.export import CachedStep, empty_cache, ort_forward, ort_session
from bcvm.train.train import load_model

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ckpt")
    p.add_argument("onnx")
    p.add_argument("--phases", default="ABC")
    p.add_argument("--scripts-per-phase", type=int, default=40)
    p.add_argument("--steps-per-script", type=int, default=8)
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args()

    torch.set_num_threads(8)
    model, _ = load_model(a.ckpt, dev="cpu")
    step = CachedStep(model.float().eval().cpu())
    sess = ort_session(a.onnx)
    rng = random.Random(a.seed)
    worst, agree, total, exact_pt, exact_ort, n_steps = 0.0, 0, 0, 0, 0, 0
    for ph in a.phases:
        d = os.path.join(ROOT, "eval/handwritten", f"phase{ph}")
        names = sorted(f for f in os.listdir(d) if f.endswith(".py"))
        for name in rng.sample(names, min(a.scripts_per_phase, len(names))):
            with open(os.path.join(d, name)) as f:
                prog, trace = pipeline.prepare(f.read(), ph, max_steps=10_000)
            listing = tokens.ids(["<bos>"] + tokens.enc_listing(prog))
            L = len(listing)
            e = empty_cache(model.cfg)
            en = [x.numpy() for x in e]
            with torch.no_grad():
                _, k0, v0 = step(torch.tensor([listing]), torch.arange(L)[None], *e, *e)
            _, k1, v1 = ort_forward(sess, [listing], np.arange(L)[None], *en, *en)
            worst = max(worst, float(np.abs(k1 - k0.numpy()).max()))
            for i in sorted(rng.sample(range(trace.steps), min(a.steps_per_script, trace.steps))):
                st, nxt = trace.states[i], trace.states[i + 1]
                inp = tokens.ids(tokens.enc_state(st) + ["=>"])
                out = tokens.ids(tokens.enc_step(st, nxt, trace.outs[i], tokens.enc_work(prog.instrs[st.ip], st))
                                 [len(tokens.enc_state(st)) + 1:])
                seq = inp + out
                # the state and the first half of the output in one call, the
                # rest in a second, so the step cache is exercised as well
                cut = len(inp) + len(out) // 2
                pos = np.arange(L, L + len(seq))[None]
                with torch.no_grad():
                    la, ka, va = step(torch.tensor([seq[:cut]]), torch.tensor(pos[:, :cut]), k0, v0, *e)
                    lb = step(torch.tensor([seq[cut:]]), torch.tensor(pos[:, cut:]), k0, v0, ka, va)[0]
                lp = torch.cat([la, lb], 1)[0].numpy()
                oa, oka, ova = ort_forward(sess, [seq[:cut]], pos[:, :cut], k1, v1, *en)
                ob = ort_forward(sess, [seq[cut:]], pos[:, cut:], k1, v1, oka, ova)[0]
                lo = np.concatenate([oa, ob], 1)[0]
                sl = slice(len(inp) - 1, len(seq) - 1)      # positions predicting the output tokens
                worst = max(worst, float(np.abs(lo[sl] - lp[sl]).max()))
                ap, ao = lp[sl].argmax(-1), lo[sl].argmax(-1)
                agree += int((ap == ao).sum())
                total += len(out)
                exact_pt += bool((ap == np.array(out)).all())
                exact_ort += bool((ao == np.array(out)).all())
                n_steps += 1
    print(f"{n_steps} steps, {total} output tokens: max |logit diff| {worst:.2e}, "
          f"argmax agreement {agree}/{total}; steps exactly right: torch fp32 {exact_pt}, onnx {exact_ort}")


if __name__ == "__main__":
    main()
