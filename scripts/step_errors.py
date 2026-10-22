"""Teacher-forced step errors for one kind of step: where in the output the
first wrong token is (work, ip, stack, names, out), and examples with the
input state, the true output and the model's argmax around the mistake.

  uv run --extra train python scripts/step_errors.py $BCVM_DATA/runs/b1/final.pt phaseB/eval_test CALL
"""
import os
import sys
from collections import Counter

import numpy as np
import torch

from bcvm import config, tokens
from bcvm.train.data import EvalSet, batches, pack
from bcvm.train.train import forward, load_model, to_device

MARKS = {tokens.TOKEN_ID[t]: t for t in ("<work>", "ip", "stack", "names", "</state>", "<out>")}


def region(t, m):
    """The output section containing position m."""
    name = "work"
    for i in range(m + 1):
        mark = MARKS.get(int(t[i]))
        if mark is not None:
            name = {"</state>": "after state", "<work>": "work"}.get(mark, mark)
    return name


def main(ckpt, name, kind, n_examples=15, seq_len=16384, rows=4):
    model, _ = load_model(ckpt)
    model.eval()
    cm = torch.compile(model)
    ev = EvalSet(os.path.join(config.DATA_DIR, name))
    inputs = {}

    def groups():
        for listing, steps, sid0 in ev.groups():
            for k, (toks, loss_off) in enumerate(steps):
                if ev.opcode[sid0 + k].startswith(kind):
                    inputs[sid0 + k] = toks[:loss_off]
            yield listing, steps, sid0

    n = wrong = 0
    where, ops = Counter(), Counter()
    examples = []
    with torch.no_grad():
        for b in batches(pack(groups(), seq_len), rows, seq_len):
            sid = b["sid"].numpy().ravel()
            tgt = b["tgt"].numpy().ravel()
            pred = forward(cm, to_device(b, "cuda")).argmax(-1).cpu().numpy().ravel()
            keep = np.flatnonzero(sid >= 0)
            keep = keep[np.argsort(sid[keep], kind="stable")]
            for at in np.split(keep, np.flatnonzero(np.diff(sid[keep])) + 1):
                s = int(sid[at[0]])
                if s not in inputs:
                    continue
                inp = inputs.pop(s)
                n += 1
                t, p = tgt[at], pred[at]
                bad = np.flatnonzero(t != p)
                if not len(bad):
                    continue
                wrong += 1
                m = int(bad[0])
                where[region(t, m)] += 1
                ops[ev.opcode[s]] += 1
                if len(examples) < n_examples:
                    lo = max(0, m - 6)
                    examples.append((ev.opcode[s], " ".join(tokens.strs(inp.tolist()))[-220:],
                                     " ".join(tokens.strs(t[lo:m + 6].tolist())),
                                     " ".join(tokens.strs(p[lo:m + 6].tolist())), m))
    print(f"{name} {kind}: {wrong}/{n} steps wrong ({wrong / max(1, n):.2e})")
    print(f"first wrong token in: {dict(where.most_common())}")
    print(f"by kind: {dict(ops.most_common())}")
    for k, inp, t, p, m in examples:
        print(f"\n[{k}] input ...{inp}")
        print(f"   true   ...{t}")
        print(f"   argmax ...{p}   (first wrong at output token {m})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
