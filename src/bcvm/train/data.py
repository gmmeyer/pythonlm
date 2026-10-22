"""Packed batches over shard groups, for training and teacher-forced eval.

A group is one listing plus the steps sampled from one run (shards.py).
Groups are packed into fixed-length rows. Each step attends to its group's
listing and to its own earlier tokens, with positions restarting at
listing_len, which is exactly what the runner sees with the listing's KV
cache. A group that doesn't fit in what's left of a row is split: the
listing is repeated, then as many steps as fit.

Per token a row holds
  ids  input token              tgt  next token, or -1 where there is no loss
  pos  RoPE position            doc  chunk id (a listing and its steps); each pad is its own
  seg  0 listing, k step k      sid  eval step id of the target token, else -1
"""
import itertools
import json
import os

import numpy as np
import torch

from .. import tokens
from ..shards import list_shards

PAD = tokens.TOKEN_ID["<pad>"]
OUT = tokens.TOKEN_ID["<out>"]
ADDR0 = tokens.TOKEN_ID["@0"]
OPCODE_IDS = np.array(sorted(tokens.TOKEN_ID[o] for o in tokens.OPCODES))
FIELDS = ("ids", "tgt", "pos", "doc", "seg", "sid")


class LoadedShard:
    """A shard read whole into RAM. Random memmap reads through WSL's 9P mount
    cost ~0.2 ms each, while a whole shard streams at ~200 MB/s."""

    def __init__(self, stem):
        with open(stem + ".json") as f:
            meta = json.load(f)
        if meta["vocab_hash"] != tokens.VOCAB_HASH:
            raise ValueError(f"{stem}: vocab hash {meta['vocab_hash']} != {tokens.VOCAB_HASH}")
        self.tokens = np.fromfile(stem + ".bin", dtype=np.uint16)
        self.index = np.load(stem + ".idx.npy")
        first = np.flatnonzero(np.r_[True, self.index[1:, 0] != self.index[:-1, 0]])
        self.bounds = np.r_[first, len(self.index)]

    def __len__(self):
        return len(self.bounds) - 1

    def group(self, i):
        """(listing ids, [(step ids, index of the first loss token in the step)])."""
        rows = self.index[self.bounds[i]:self.bounds[i + 1]]
        g, ll = int(rows[0, 0]), int(rows[0, 1])
        steps = [(self.tokens[s:s + sl], ls - s) for _, _, s, sl, ls in rows.tolist()]
        return self.tokens[g:g + ll], steps


class _Row:
    def __init__(self, n):
        self.ids = np.full(n, PAD, np.int32)
        self.tgt = np.full(n, -1, np.int64)
        self.pos = np.zeros(n, np.int32)
        self.doc = -1 - np.arange(n, dtype=np.int32)
        self.seg = np.full(n, -1, np.int32)
        self.sid = np.full(n, -1, np.int64)
        self.n = 0
        self.chunks = 0

    @property
    def free(self):
        return len(self.ids) - self.n

    def add_listing(self, listing):
        n, ll = self.n, len(listing)
        self.ids[n:n + ll] = listing
        self.pos[n:n + ll] = np.arange(ll)
        self.doc[n:n + ll] = self.chunks
        self.seg[n:n + ll] = 0
        self.n += ll

    def add_step(self, toks, loss_off, ll, k, sid):
        n, sl = self.n, len(toks)
        self.ids[n:n + sl] = toks
        self.pos[n:n + sl] = np.arange(ll, ll + sl)
        self.doc[n:n + sl] = self.chunks
        self.seg[n:n + sl] = k
        # the token before each loss token predicts it
        self.tgt[n + loss_off - 1:n + sl - 1] = toks[loss_off:]
        self.sid[n + loss_off - 1:n + sl - 1] = sid
        self.n += sl

    def arrays(self):
        return {k: getattr(self, k) for k in FIELDS}


def pack(groups, seq_len):
    """groups yields (listing, steps, first step id or None); yields rows as dicts of arrays."""
    row = _Row(seq_len)
    for listing, steps, sid0 in groups:
        ll, i = len(listing), 0
        while i < len(steps):
            if ll + len(steps[i][0]) > row.free:
                if row.n == 0:
                    raise ValueError(f"listing + step is {ll + len(steps[i][0])} tokens, longer than a row")
                yield row.arrays()
                row = _Row(seq_len)
            row.add_listing(listing)
            k = 0
            while i < len(steps) and len(steps[i][0]) <= row.free:
                k += 1
                row.add_step(*steps[i], ll, k, -1 if sid0 is None else sid0 + i)
                i += 1
            row.chunks += 1
    if row.n:
        yield row.arrays()


def batches(rows, n_rows, seq_len):
    """Stack rows into [n_rows, seq_len] tensors; the last batch is padded with empty rows."""
    rows = iter(rows)
    while chunk := list(itertools.islice(rows, n_rows)):
        chunk += [_Row(seq_len).arrays() for _ in range(n_rows - len(chunk))]
        yield {k: torch.from_numpy(np.stack([r[k] for r in chunk])) for k in FIELDS}


def _shuffled_groups(stems, rng):
    while True:
        for s in rng.permutation(len(stems)):
            sh = LoadedShard(stems[s])
            for i in rng.permutation(len(sh)):
                yield *sh.group(i), None


class TrainStream(torch.utils.data.IterableDataset):
    """Endless shuffled batches from a weighted mix of shard sets (replay).

    sources: [(weight, [shard stems])]. The weight picks the source per group.
    Each DataLoader worker reads its own slice of every source's shards."""

    def __init__(self, sources, seq_len, n_rows, seed):
        self.sources, self.seq_len, self.n_rows, self.seed = sources, seq_len, n_rows, seed

    def __iter__(self):
        info = torch.utils.data.get_worker_info()
        wid, nw = (info.id, info.num_workers) if info else (0, 1)
        rng = np.random.default_rng([self.seed, wid])
        streams = [_shuffled_groups(stems[wid::nw] or stems, rng) for _, stems in self.sources]
        w = np.array([w for w, _ in self.sources], float)
        w /= w.sum()

        def mixed():
            while True:
                for j in rng.choice(len(streams), size=4096, p=w):
                    yield next(streams[j])

        return batches(pack(mixed(), self.seq_len), self.n_rows, self.seq_len)


def step_ip(toks):
    """Instruction index in a step's input state: <state> ip @d @d @d ..."""
    return int(toks[2] - ADDR0) * 100 + int(toks[3] - ADDR0) * 10 + int(toks[4] - ADDR0)


_WITH_OPERATOR = {tokens.TOKEN_ID["BINARY_OP"], tokens.TOKEN_ID["COMPARE_OP"]}


def step_kind(listing, op_pos, ip):
    """The instruction at ip, e.g. 'STORE_NAME', or 'BINARY_OP op://' with its operator."""
    p = op_pos[ip]
    op = int(listing[p])
    if op in _WITH_OPERATOR:
        return f"{tokens.VOCAB[op]} {tokens.VOCAB[listing[p + 1]]}"
    return tokens.VOCAB[op]


class EvalSet:
    """Every step of an eval set's shards, in order. Iterating groups() also
    records each step's kind (the instruction at the input ip, see step_kind)
    and whether it prints."""

    def __init__(self, directory, max_steps=None):
        self.stems = list_shards(directory)
        if not self.stems:
            raise FileNotFoundError(f"no shards in {directory}")
        total = 0
        for stem in self.stems:
            with open(stem + ".json") as f:
                total += json.load(f)["n_steps"]
        self.max_steps = min(total, max_steps) if max_steps else total
        self.opcode, self.prints = [], []

    def groups(self):
        self.opcode, self.prints = [], []
        sid = 0
        for stem in self.stems:
            sh = LoadedShard(stem)
            for i in range(len(sh)):
                listing, steps = sh.group(i)
                steps = steps[:self.max_steps - sid]
                if not steps:
                    return
                op_pos = np.flatnonzero(np.isin(listing, OPCODE_IDS))
                for toks, _ in steps:
                    self.opcode.append(step_kind(listing, op_pos, step_ip(toks)))
                    self.prints.append(bool((toks == OUT).any()))
                yield listing, steps, sid
                sid += len(steps)


def phase_dir(data_dir, phase, split):
    return os.path.join(data_dir, f"phase{phase}", split)
