"""Shard format, shared by the Mac (writer) and the 5090 (reader).

A shard is three files with a common stem:

  <stem>.bin        uint16 token ids. A sequence of *groups*; a group is one
                    script's listing followed by K sampled steps:
                      <bos> <code> ... </code>  [step]  [step] ...
                    where each step is
                      <state> ... </state> => <state> ... </state> [<out> ... </out>] <eos>
  <stem>.idx.npy    uint32 [n_steps, 5]: group_start, listing_len, step_start,
                    step_len, loss_start (offsets into .bin; loss_start is the
                    first token after "=>").
  <stem>.json       metadata: phase, vocab hash, counts, source mix, opcode histogram.

Two ways to train on it:

- expanded: example = tokens[group_start : group_start+listing_len] + tokens[step_start : step_start+step_len],
  loss on the step's tokens after "=>". Plain causal attention.
- packed: feed a whole group; each step attends to the listing and to itself
  only (a block mask, e.g. FlexAttention) with positions restarting at
  listing_len for every step. Identical to inference with the listing's KV
  cache, at a fraction of the compute.
"""
import json
import os
from array import array

import numpy as np

from . import config, tokens

IDX_COLS = ("group_start", "listing_len", "step_start", "step_len", "loss_start")


class ShardWriter:
    def __init__(self, stem):
        self.stem = stem
        self.buf = array("H")
        self.rows = array("I")

    @property
    def n_tokens(self):
        return len(self.buf)

    def add_group(self, listing_ids, steps):
        """steps: list of (token ids, index of first loss token within the step)."""
        g = len(self.buf)
        self.buf.extend(listing_ids)
        for ids, loss_off in steps:
            pos = len(self.buf)
            self.buf.extend(ids)
            self.rows.extend((g, len(listing_ids), pos, len(ids), pos + loss_off))
        if len(self.buf) >= 2**32 - 1:
            raise OverflowError("shard too large for uint32 offsets")

    def close(self, meta):
        os.makedirs(os.path.dirname(self.stem) or ".", exist_ok=True)
        tmp = self.stem + ".bin.tmp"
        arr = np.frombuffer(self.buf, dtype=np.uint16)
        arr.tofile(tmp)
        idx = np.frombuffer(self.rows, dtype=np.uint32).reshape(-1, len(IDX_COLS))
        with open(self.stem + ".idx.npy.tmp", "wb") as f:
            np.save(f, idx)
        meta = dict(meta, n_tokens=int(arr.size), n_steps=int(idx.shape[0]),
                    vocab_hash=tokens.VOCAB_HASH, vocab_size=tokens.VOCAB_SIZE,
                    format_version=config.FORMAT_VERSION, idx_cols=list(IDX_COLS))
        with open(self.stem + ".json.tmp", "w") as f:
            json.dump(meta, f, indent=1)
        # rename last, so a shard with a .json is always complete
        os.replace(tmp, self.stem + ".bin")
        os.replace(self.stem + ".idx.npy.tmp", self.stem + ".idx.npy")
        os.replace(self.stem + ".json.tmp", self.stem + ".json")
        return meta


class Shard:
    """Read-only view for training. Memory-maps the tokens."""

    def __init__(self, stem):
        self.stem = stem
        with open(stem + ".json") as f:
            self.meta = json.load(f)
        if self.meta["vocab_hash"] != tokens.VOCAB_HASH:
            raise ValueError(f"{stem}: vocab hash {self.meta['vocab_hash']} != {tokens.VOCAB_HASH}")
        self.tokens = np.memmap(stem + ".bin", dtype=np.uint16, mode="r")
        self.index = np.load(stem + ".idx.npy", mmap_mode="r")

    def __len__(self):
        return self.index.shape[0]

    def example(self, i):
        """Expanded example i: (token ids, loss mask) as numpy arrays."""
        g, ll, s, sl, ls = (int(x) for x in self.index[i])
        ids = np.concatenate([self.tokens[g:g + ll], self.tokens[s:s + sl]])
        mask = np.zeros(ids.size, dtype=bool)
        mask[ll + (ls - s):] = True
        return ids, mask

    def groups(self):
        """Yield (group_start, listing_len, [rows]) for packed training."""
        rows = self.index
        i = 0
        while i < len(rows):
            j = i
            while j < len(rows) and rows[j, 0] == rows[i, 0]:
                j += 1
            yield int(rows[i, 0]), int(rows[i, 1]), rows[i:j]
            i = j


def list_shards(directory):
    return sorted(os.path.join(directory, f[:-5]) for f in os.listdir(directory)
                  if f.endswith(".json") and not f.startswith("._") and f != "manifest.json")
