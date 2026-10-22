"""ONNX export of the step model for the web demo, with the KV cache as explicit
inputs and outputs, in two parts:

    logits, k, v = f(ids [1, T], pos [1, T], prefix_k [P, L, H, D], prefix_v,
                     step_k [S, L, H, D], step_v)

prefix is the listing's cache (computed once per script, kept on the GPU);
step is the current step's tokens so far (small, kept by the caller). k and v
are this call's keys and values only ([T, L, H, D]). Caches are token-major,
so a caller keeps the step cache as one flat array: appending is a copy at
the end and dropping rejected draft tokens is a length. The T new tokens attend to all P + S
cached ones and causally to each other, so one graph does the listing
prefill (P = S = 0, keep k/v as the prefix), a step's state prefill,
single-token decoding and multi-token draft verification. It runs StepModel's
own forward with a cache object that concatenates, so the graph is the trained
code path.

  bcvm export $BCVM_DATA/runs/c2/final.pt out/pythonlm.onnx
"""
import json
import os

import numpy as np
import torch

from .. import tokens
from .train import load_model


class _Concat:
    """StepModel cache for one layer: attend to prefix + step + this call's
    keys/values, and keep this call's."""

    def __init__(self, pk, pv, sk, sv):
        self.pk, self.pv, self.sk, self.sv = pk, pv, sk, sv

    def update(self, k, v):
        self.k, self.v = k, v
        return torch.cat([self.pk, self.sk, k], dim=2), torch.cat([self.pv, self.sv, v], dim=2)


class CachedStep(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, ids, pos, prefix_k, prefix_v, step_k, step_v):
        T, C = ids.shape[1], prefix_k.shape[0] + step_k.shape[0]
        q = torch.arange(T, device=ids.device)[:, None]
        kv = torch.arange(C + T, device=ids.device)[None, :]
        mask = ((kv < C) | (kv - C <= q))[None, None]           # [1, 1, T, C + T]
        layer = lambda x, i: x[:, i].transpose(0, 1)[None]      # noqa: E731  [N, L, H, D] -> [1, H, N, D]
        cache = [_Concat(layer(prefix_k, i), layer(prefix_v, i), layer(step_k, i), layer(step_v, i))
                 for i in range(prefix_k.shape[1])]
        logits = self.model(ids, pos, mask, cache)
        new = lambda xs: torch.cat(xs).permute(2, 0, 1, 3)      # noqa: E731  L x [1, H, T, D] -> [T, L, H, D]
        return logits, new([c.k for c in cache]), new([c.v for c in cache])


def empty_cache(cfg, n=0, dtype=torch.float32):
    shape = (n, cfg.n_layers, cfg.n_heads, cfg.d_model // cfg.n_heads)
    return torch.zeros(shape, dtype=dtype), torch.zeros(shape, dtype=dtype)


def export(model, path):
    """Write the ONNX graph to `path` (fp32) and a JSON sidecar with what the
    browser needs: model shape, vocabulary and its hash."""
    wrapped = CachedStep(model.float().eval().cpu())
    cfg = model.cfg
    T = torch.export.Dim("T", min=1, max=cfg.max_pos)
    P = torch.export.Dim("P", min=0, max=cfg.max_pos)
    S = torch.export.Dim("S", min=0, max=cfg.max_pos)
    ids = torch.randint(0, cfg.vocab_size, (1, 3))
    pos = torch.arange(9, 12)[None]
    pk, pv = empty_cache(cfg, 5)
    sk, sv = empty_cache(cfg, 4)
    torch.onnx.export(
        wrapped, (ids, pos, pk, pv, sk, sv), path, dynamo=True, external_data=False,
        input_names=["ids", "pos", "prefix_k", "prefix_v", "step_k", "step_v"],
        output_names=["logits", "k", "v"],
        dynamic_shapes={"ids": {1: T}, "pos": {1: T}, "prefix_k": {0: P}, "prefix_v": {0: P},
                        "step_k": {0: S}, "step_v": {0: S}},
    )
    meta = dict(n_layers=cfg.n_layers, n_heads=cfg.n_heads, head_dim=cfg.d_model // cfg.n_heads,
                max_pos=cfg.max_pos, vocab_size=cfg.vocab_size, vocab=list(tokens.VOCAB),
                vocab_hash=tokens.VOCAB_HASH)
    with open(os.path.splitext(path)[0] + ".json", "w") as f:
        json.dump(meta, f)


def ort_session(path):
    import onnxruntime as ort
    return ort.InferenceSession(path, providers=["CPUExecutionProvider"])


def ort_forward(sess, ids, pos, prefix_k, prefix_v, step_k, step_v):
    feed = dict(prefix_k=prefix_k, prefix_v=prefix_v, step_k=step_k, step_v=step_v)
    feed = {k: np.asarray(x, np.float32) for k, x in feed.items()}
    return sess.run(None, dict(feed, ids=np.asarray(ids, np.int64), pos=np.asarray(pos, np.int64)))


def cmd_export(a):
    model, _ = load_model(a.ckpt, dev="cpu")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    export(model, a.out)
    print(f"wrote {a.out} ({os.path.getsize(a.out) / 1e6:.1f} MB) and its .json")


class OrtModel:
    """web.run's model interface over onnxruntime on the CPU: the demo's runner,
    tested natively. The browser's JS model implements the same calls."""

    def __init__(self, path, seed=0):
        self.sess = ort_session(path)
        with open(os.path.splitext(path)[0] + ".json") as f:
            meta = json.load(f)
        self.empty = np.zeros((0, meta["n_layers"], meta["n_heads"], meta["head_dim"]), np.float32)
        self.vocab = meta["vocab_size"]
        self.rng = np.random.default_rng(seed)

    async def prefill(self, ids):
        e = self.empty
        _, self.pk, self.pv = ort_forward(self.sess, [ids], np.arange(len(ids))[None], e, e, e, e)
        self.sk = self.sv = e

    def truncate(self, n):
        self.sk, self.sv = self.sk[:n], self.sv[:n]

    async def forward(self, ids, masks, temperature=0):
        start = self.pk.shape[0] + self.sk.shape[0]
        pos = np.arange(start, start + len(ids))[None]
        logits, k, v = ort_forward(self.sess, [ids], pos, self.pk, self.pv, self.sk, self.sv)
        self.sk, self.sv = np.concatenate([self.sk, k]), np.concatenate([self.sv, v])
        allow = np.frombuffer(bytes(masks), np.uint8).reshape(len(ids), self.vocab).astype(bool)
        lg = np.where(allow, logits[0], -np.inf)
        out = []
        for j in range(len(ids)):
            if not allow[j].any():
                out.append(-1)
            elif temperature > 0:
                p = np.exp((lg[j] - lg[j].max()) / temperature)
                out.append(int(self.rng.choice(self.vocab, p=p / p.sum())))
            else:
                out.append(int(lg[j].argmax()))
        return out
