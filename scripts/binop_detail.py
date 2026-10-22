"""Where BINARY_OP steps go wrong, teacher-forced: which token of the output is
the first wrong one (stack copy, result sign/digit, names), error rate by
divisor for // and %, and how far off the first wrong result digit is.

  uv run --extra train python scripts/binop_detail.py $BCVM_DATA/runs/a1/final.pt phaseA/eval_test
"""
import os
import sys
from collections import Counter, defaultdict

import numpy as np
import torch

from bcvm import config, tokens
from bcvm.train.data import EvalSet, batches, pack
from bcvm.train.train import forward, load_model, to_device

NAMES = tokens.TOKEN_ID["names"]
STATE = tokens.TOKEN_ID["<state>"]
SIGNS = {tokens.TOKEN_ID["i+"], tokens.TOKEN_ID["i-"]}


def main(ckpt, name, seq_len=16384, rows=4):
    model, _ = load_model(ckpt)
    model.eval()
    cm = torch.compile(model)
    directory = os.path.join(config.DATA_DIR, name)
    ev = EvalSet(directory)
    inputs = {}

    def groups():
        for listing, steps, sid0 in ev.groups():
            for k, (toks, _) in enumerate(steps):
                if ev.opcode[sid0 + k].startswith("BINARY_OP"):
                    inputs[sid0 + k] = toks
            yield listing, steps, sid0

    n_by = defaultdict(lambda: [0, 0])      # (op, |b|) -> [n, wrong]
    where = defaultdict(Counter)            # op -> first wrong place
    miss = defaultdict(Counter)             # op -> predicted - true digit at the first wrong result digit
    examples = defaultdict(list)
    with torch.no_grad():
        for b in batches(pack(groups(), seq_len), rows, seq_len):
            sid = b["sid"].numpy().ravel()
            tgt = b["tgt"].numpy().ravel()
            pred = forward(cm, to_device(b, "cuda")).argmax(-1).cpu().numpy().ravel()
            keep = np.flatnonzero(sid >= 0)
            keep = keep[np.argsort(sid[keep], kind="stable")]
            s_sorted = sid[keep]
            cuts = np.flatnonzero(np.diff(s_sorted)) + 1
            for at in np.split(keep, cuts):
                s = int(sid[at[0]])
                if s not in inputs:
                    continue
                toks = inputs.pop(s)
                st, _ = tokens.parse_state(tokens.strs(toks.tolist()))
                a, bb = st.stack[-2], st.stack[-1]
                op = ev.opcode[s].split()[1][3:]
                t, p = tgt[at], pred[at]
                bad = np.flatnonzero(t != p)
                key = (op, abs(bb) if op in ("//", "%", "//=", "%=") else len(str(abs(bb))))
                n_by[key][0] += 1
                if not len(bad):
                    continue
                n_by[key][1] += 1
                m = int(bad[0])
                names_at = int(np.flatnonzero(t == NAMES)[0])
                state_at = int(np.flatnonzero(t == STATE)[0])
                res_at = max(i for i in range(names_at) if int(t[i]) in SIGNS)
                if m < state_at:
                    place = f"work token {m}"
                elif m < res_at:
                    place = "stack copy"
                elif m == res_at:
                    place = "result sign"
                elif m < names_at:
                    place = f"result digit {m - res_at - 1}"
                    tv, pv = tokens.VOCAB[t[m]], tokens.VOCAB[p[m]]
                    if tv.isdigit() and pv.isdigit():
                        miss[op][(int(pv) - int(tv)) % 10] += 1
                    else:
                        miss[op][f"{tv}->{pv}"] += 1
                else:
                    place = "names"
                where[op][place] += 1
                if len(examples[op]) < 12:
                    q = {"//": a // bb, "%": a % bb, "*": a * bb, "+": a + bb, "-": a - bb}.get(op.rstrip("="), "?")
                    got = " ".join(tokens.VOCAB[x] for x in p[res_at:names_at + 1])
                    examples[op].append(f"{a} {op} {bb} = {q}: first wrong token #{m - res_at} of the result, argmax result tokens [{got}]")

    print(f"{name}: BINARY_OP first wrong place, by operator")
    for op, c in sorted(where.items()):
        print(f"  {op:>4}: {dict(c.most_common())}")
    print("\nfirst wrong result digit: (predicted - true) mod 10")
    for op, c in sorted(miss.items()):
        print(f"  {op:>4}: {dict(sorted(c.items(), key=str))}")
    for op in ("//", "%"):
        print(f"\n{op} error by |divisor| (n >= 50)")
        rows_ = sorted((k[1], v) for k, v in n_by.items() if k[0] == op and v[0] >= 50)
        print("  " + "  ".join(f"{d}:{w / n:.0%}" for d, (n, w) in rows_))
    for op, ex in sorted(examples.items()):
        print(f"\nexamples {op}")
        for e in ex:
            print("  " + e)


if __name__ == "__main__":
    main(*sys.argv[1:3])
