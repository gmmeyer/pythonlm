"""Average the weights of checkpoints from the same model (a "model soup").
The shipped model, c56avg, is c5 and c6 averaged: c6 continued c5 and
overshot, and the average beat both on every eval set (PLAN.md).

  uv run --extra train python scripts/average_checkpoints.py \
      $BCVM_DATA/runs/c56avg/final.pt $BCVM_DATA/runs/c5/final.pt $BCVM_DATA/runs/c6/final.pt
"""
import argparse
import os

import torch


def main():
    p = argparse.ArgumentParser()
    p.add_argument("out")
    p.add_argument("ckpts", nargs="+")
    a = p.parse_args()
    cks = [torch.load(c, map_location="cpu", weights_only=False) for c in a.ckpts]
    first = cks[0]
    for ck in cks[1:]:
        assert ck["cfg"] == first["cfg"] and ck["vocab_hash"] == first["vocab_hash"], "different models"
    model = {k: (sum(ck["model"][k].float() for ck in cks) / len(cks)).to(v.dtype)
             for k, v in first["model"].items()}
    # Everything else comes from the last checkpoint. There's no optimizer
    # state for an average, so it can be evaluated or exported, not resumed.
    out = {k: v for k, v in cks[-1].items() if k != "opt"}
    out.update(model=model, opt=None)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    torch.save(out, a.out)
    print(f"averaged {len(model)} tensors from {len(cks)} checkpoints -> {a.out}")


if __name__ == "__main__":
    main()
