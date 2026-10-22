"""Teacher-forced BINARY_OP errors by operator, operand signs and operand sizes.

  uv run --extra train python scripts/binop_errors.py $BCVM_DATA/runs/a1/final.pt phaseA/eval_test
"""
import os
import sys
from collections import defaultdict

import torch

from bcvm import config, tokens
from bcvm.train.data import EvalSet
from bcvm.train.train import evaluate, load_model


def describe(v):
    if type(v) is int:
        return ("-" if v < 0 else "+"), len(str(abs(v)))
    return type(v).__name__, 0


def main(ckpt, name):
    model, _ = load_model(ckpt)
    model.eval()
    directory = os.path.join(config.DATA_DIR, name)
    r = evaluate(torch.compile(model), directory, 16384, 4, per_step=True)
    wrong = r["wrong"]
    ev = EvalSet(directory)
    by_sign, by_size = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
    for listing, steps, sid0 in ev.groups():
        for k, (toks, _) in enumerate(steps):
            kind = ev.opcode[sid0 + k]
            if not kind.startswith("BINARY_OP"):
                continue
            st, _ = tokens.parse_state(tokens.strs(toks.tolist()))
            (sa, da), (sb, db) = describe(st.stack[-2]), describe(st.stack[-1])
            op = kind.split()[1][3:]
            for d, key in ((by_sign, (op, sa + sb)), (by_size, (op, da, db))):
                d[key][0] += 1
                d[key][1] += bool(wrong[sid0 + k])
    print(f"{name}: {r['steps']} steps, step err {r['step_err']:.2e}")
    print("\nby operator and operand signs (a, b): wrong / n")
    for (op, s), (n, w) in sorted(by_sign.items()):
        print(f"  {op:>4} {s}  {w:6d} / {n:6d}  {w / n:.2%}")
    print("\nby operator and operand digits (a, b): wrong / n")
    for (op, da, db), (n, w) in sorted(by_size.items()):
        if w:
            print(f"  {op:>4} {da}x{db}  {w:6d} / {n:6d}  {w / n:.2%}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
