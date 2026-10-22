"""The web demo's runner (bcvm.web: async model, speculative decoding) on the
hand-written scripts, with the exported ONNX model on the CPU. Reports stdout
match, how many forward passes a step takes, and, given the PyTorch gate's
JSON for the same checkpoint, which scripts differ from it.

  uv run --extra train --extra export python scripts/web_gate.py out/c2.onnx \
      --per-phase 20 --torch-gate $BCVM_DATA/runs/c2/gate_handwritten_{A}.json
"""
import argparse
import asyncio
import json
import os
import random
import time

from bcvm import pipeline, web
from bcvm.train.export import OrtModel

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("onnx")
    p.add_argument("--phases", default="ABC")
    p.add_argument("--per-phase", type=int, default=20)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--torch-gate", default="", help="gate JSON path with {} for the phase letter")
    a = p.parse_args()

    model = OrtModel(a.onnx)
    rng = random.Random(a.seed)
    for ph in a.phases:
        d = os.path.join(ROOT, "eval/handwritten", f"phase{ph}")
        names = rng.sample(sorted(f for f in os.listdir(d) if f.endswith(".py")), a.per_phase)
        torch_fail = set()
        if a.torch_gate:
            with open(a.torch_gate.format(ph)) as f:
                torch_fail = {r["file"] for r in json.load(f)["failures"]}
        stats, ok, differ, t0 = web.Stats(), 0, [], time.time()
        for name in names:
            with open(os.path.join(d, name)) as f:
                src = f.read()
            _, trace = pipeline.prepare(src, ph, max_steps=10_000)
            res = await web.run(src, ph, model, max_steps=2 * trace.steps + 100, stats=stats)
            good = res.stdout == trace.stdout and not res.error
            ok += good
            if a.torch_gate and good == (name in torch_fail):
                differ.append((name, "passes" if good else "fails"))
        dt = time.time() - t0
        print(f"phase {ph}: {ok}/{len(names)} match; {stats.steps} steps, {stats.forwards / stats.steps:.2f} forwards "
              f"and {stats.tokens / stats.steps:.1f} output tokens per step, draft acceptance "
              f"{stats.accepted / max(1, stats.drafted):.0%}; {dt:.0f}s ({stats.steps / dt:.0f} steps/s)"
              + (f"; differs from the torch gate on {differ}" if a.torch_gate else ""), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
