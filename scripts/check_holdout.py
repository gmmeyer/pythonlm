"""Check that eval scripts never appear in training data: compares each
script's listing (the same digest the pipeline dedups and splits on) against
every group in the given training shard directories.

  uv run python scripts/check_holdout.py --scripts eval/handwritten/phase{A,B,C}       --train phase{A,B,C}/train phase{A,B,C}/train_arith phase{B,C}/train_copy
"""
import os

import numpy as np

from bcvm import config, pipeline, support, tokens
from bcvm.shards import list_shards
from bcvm.train.data import LoadedShard


def digest(ids):
    """pipeline's listing digest (blake2b of the uint16 token bytes)."""
    return pipeline._digest(np.asarray(ids, dtype=np.uint16).tobytes())


def main(script_dirs, train_dirs):
    want = {}
    for script_dir in script_dirs:
        for name in sorted(f for f in os.listdir(script_dir) if f.endswith(".py")):
            with open(os.path.join(script_dir, name)) as f:
                prog = support.check_source(f.read(), "C")
            want.setdefault(digest(tokens.ids(["<bos>"] + tokens.enc_listing(prog))), []).append(
                os.path.join(os.path.basename(script_dir), name))
    dups = sum(len(v) - 1 for v in want.values())
    print(f"{sum(len(v) for v in want.values())} scripts, {len(want)} distinct listings"
          + (f", duplicates among themselves: {[v for v in want.values() if len(v) > 1]}" if dups else ""))
    hits, groups = {}, 0
    for d in train_dirs:
        for stem in list_shards(os.path.join(config.DATA_DIR, d)):
            sh = LoadedShard(stem)
            for i in range(len(sh)):
                g, ll = int(sh.index[sh.bounds[i], 0]), int(sh.index[sh.bounds[i], 1])
                key = digest(sh.tokens[g:g + ll])
                if key in want:
                    hits.setdefault(key, set()).add(os.path.relpath(stem, config.DATA_DIR))
            groups += len(sh)
        print(f"  scanned {d}: {groups} groups so far, {len(hits)} scripts found in training", flush=True)
    for key, where in hits.items():
        print(f"  IN TRAINING: {want[key]} <- {sorted(where)[:3]}")
    print("clean" if not hits else f"{len(hits)} listings appear in training data")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--scripts", nargs="+", required=True)
    p.add_argument("--train", nargs="+", required=True, help="dirs under $BCVM_DATA")
    a = p.parse_args()
    main(a.scripts, a.train)
