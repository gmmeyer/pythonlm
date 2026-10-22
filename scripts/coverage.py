"""Coverage: how often each kind of step (SWAP 3, BINARY_OP op://, ...) runs, and
how many names and listing tokens scripts have, in directories of eval .py
files versus training shards. A kind the eval scripts use that training
rarely shows is a gap for the generators to fill.

  uv run --extra train python scripts/coverage.py --scripts eval/handwritten/phaseA \
      --train phaseA/train phaseA/train_arith phaseA/train_edge --groups 20000
"""
import argparse
import os
from collections import Counter

import numpy as np

from bcvm import config, pipeline, tokens
from bcvm.shards import list_shards
from bcvm.train.data import LoadedShard, step_ip

V = tokens.VOCAB
# operands worth telling apart: the operator, or a small count
WITH_OPERAND = {"BINARY_OP", "COMPARE_OP", "SWAP", "COPY", "UNPACK_SEQUENCE", "BUILD_TUPLE", "BUILD_LIST",
                "BUILD_STRING", "CALL"}


def kinds_of(listing):
    """The kind of each instruction in a listing (token ids)."""
    listing = [int(t) for t in listing]
    out = []
    for p, t in enumerate(listing):
        name = V[t]
        if p == 0 or name.startswith("@") or not V[listing[p - 1]].startswith("@"):
            continue   # an opcode is the first token after an address
        if name in WITH_OPERAND:
            q = p + 1
            while q < len(listing) and not V[listing[q]].startswith("@") and V[listing[q]] != "</code>":
                q += 1
            name += " " + "".join(V[x] for x in listing[p + 1:q])
        out.append(name)
    return out


def n_names(listing):
    return 1 + max((int(V[t][1:]) for t in listing if V[t][:1] == "N" and V[t][1:].isdigit()), default=-1)


class Tally:
    def __init__(self):
        self.steps, self.scripts = Counter(), Counter()
        self.n_steps = self.n_scripts = 0
        self.names, self.lengths = [], []

    def add(self, listing, ips):
        kinds = kinds_of(listing)
        self.n_scripts += 1
        self.n_steps += len(ips)
        used = Counter(kinds[ip] for ip in ips)
        self.steps.update(used)
        self.scripts.update(used.keys())
        self.names.append(n_names(listing))
        self.lengths.append(len(listing))


def from_scripts(directories):
    t = Tally()
    for d in directories:
        phase = d.rstrip("/")[-1]
        for name in sorted(f for f in os.listdir(d) if f.endswith(".py")):
            with open(os.path.join(d, name)) as f:
                prog, trace = pipeline.prepare(f.read(), phase, max_steps=10_000)
            listing = tokens.ids(["<bos>"] + tokens.enc_listing(prog))
            t.add(listing, [s.ip for s in trace.states[:-1]])
    return t


def from_shards(directories, n_groups):
    t = Tally()
    for d in directories:
        seen = 0
        for stem in list_shards(os.path.join(config.DATA_DIR, d)):
            sh = LoadedShard(stem)
            for i in range(len(sh)):
                listing, steps = sh.group(i)
                t.add(listing, [step_ip(toks) for toks, _ in steps])
                seen += 1
                if seen >= n_groups:
                    break
            if seen >= n_groups:
                break
    return t


def pct(xs, q):
    return int(np.percentile(xs, q)) if xs else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scripts", nargs="+", required=True, help="directories of .py files")
    p.add_argument("--train", nargs="+", required=True, help="shard dirs under $BCVM_DATA")
    p.add_argument("--groups", type=int, default=20_000, help="groups read per training dir")
    p.add_argument("--min-ratio", type=float, default=0.0, help="only show kinds with eval/train share above this")
    a = p.parse_args()
    ev, tr = from_scripts(a.scripts), from_shards(a.train, a.groups)
    for label, t in (("eval", ev), ("train", tr)):
        print(f"{label}: {t.n_scripts} scripts, {t.n_steps} steps; names p50/p90/max "
              f"{pct(t.names, 50)}/{pct(t.names, 90)}/{max(t.names)}; listing tokens p50/p90/max "
              f"{pct(t.lengths, 50)}/{pct(t.lengths, 90)}/{max(t.lengths)}")
    for n in (8, 12, 16, 20):
        print(f"  scripts with >= {n} names: eval {np.mean(np.array(ev.names) >= n):.1%}  "
              f"train {np.mean(np.array(tr.names) >= n):.2%}")
    print(f"\n{'kind':28} {'eval steps':>11} {'eval scripts':>13} {'train steps':>12} {'train scripts':>14} {'ratio':>7}")
    rows = []
    for k in set(ev.steps) | set(tr.steps):
        e, r = ev.steps[k] / ev.n_steps, tr.steps[k] / tr.n_steps
        rows.append((e / r if r else float("inf"), k, e, ev.scripts[k] / ev.n_scripts, r, tr.scripts[k] / tr.n_scripts))
    for ratio, k, e, es, r, rs in sorted(rows, reverse=True):
        if ratio >= a.min_ratio:
            print(f"{k:28} {e:11.2e} {es:13.1%} {r:12.2e} {rs:14.2%} {ratio:7.1f}")


if __name__ == "__main__":
    main()
