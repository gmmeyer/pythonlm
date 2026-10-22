"""Decoder-only transformer for the step model.

Pre-norm RMSNorm, RoPE on explicit position ids, QK-norm, SwiGLU, no biases.
Attention takes a FlexAttention BlockMask (packed training), a dense boolean
mask (tests), or a KV cache (the runner).
"""
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.attention.flex_attention import BlockMask, create_block_mask, flex_attention

from .. import config, tokens


@dataclass
class ModelConfig:
    vocab_size: int = tokens.VOCAB_SIZE
    d_model: int = 512
    n_layers: int = 8
    n_heads: int = 8
    d_ff: int = 1408            # SwiGLU hidden size, ~8/3 d_model
    max_pos: int = config.CONTEXT
    rope_base: float = 10_000.0


def apply_rope(x, cos, sin):
    x1, x2 = x.float().chunk(2, dim=-1)
    return torch.cat([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1).type_as(x)


class Attention(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.h, self.hd = cfg.n_heads, cfg.d_model // cfg.n_heads
        self.qkv = nn.Linear(cfg.d_model, 3 * cfg.d_model, bias=False)
        self.out = nn.Linear(cfg.d_model, cfg.d_model, bias=False)
        self.q_norm = nn.RMSNorm(self.hd)
        self.k_norm = nn.RMSNorm(self.hd)

    def forward(self, x, cos, sin, mask, cache=None):
        B, T, _ = x.shape
        q, k, v = self.qkv(x).view(B, T, 3, self.h, self.hd).permute(2, 0, 3, 1, 4)
        q = apply_rope(self.q_norm(q), cos, sin)
        k = apply_rope(self.k_norm(k), cos, sin)
        if cache is not None:
            k, v = cache.update(k, v)
        if isinstance(mask, BlockMask):
            y = flex_attention(q, k, v, block_mask=mask)
        else:
            y = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
        return self.out(y.transpose(1, 2).reshape(B, T, -1))


class Block(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.n1 = nn.RMSNorm(cfg.d_model)
        self.attn = Attention(cfg)
        self.n2 = nn.RMSNorm(cfg.d_model)
        self.up = nn.Linear(cfg.d_model, 2 * cfg.d_ff, bias=False)
        self.down = nn.Linear(cfg.d_ff, cfg.d_model, bias=False)

    def forward(self, x, cos, sin, mask, cache=None):
        x = x + self.attn(self.n1(x), cos, sin, mask, cache)
        a, b = self.up(self.n2(x)).chunk(2, dim=-1)
        return x + self.down(F.silu(a) * b)


class StepModel(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.blocks = nn.ModuleList(Block(cfg) for _ in range(cfg.n_layers))
        self.norm = nn.RMSNorm(cfg.d_model)
        self.head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        hd = cfg.d_model // cfg.n_heads
        inv = 1.0 / cfg.rope_base ** (torch.arange(0, hd, 2).float() / hd)
        ang = torch.outer(torch.arange(cfg.max_pos).float(), inv)
        self.register_buffer("cos", ang.cos(), persistent=False)
        self.register_buffer("sin", ang.sin(), persistent=False)
        self.apply(self._init)
        for blk in self.blocks:  # residual projections scaled by depth
            for w in (blk.attn.out.weight, blk.down.weight):
                nn.init.normal_(w, std=0.02 / (2 * cfg.n_layers) ** 0.5)

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)

    def n_params(self, embeddings=True):
        n = sum(p.numel() for p in self.parameters())
        return n if embeddings else n - self.emb.weight.numel() - self.head.weight.numel()

    def forward(self, ids, pos, mask, cache=None):
        """ids, pos: [B, T]. mask: BlockMask, bool [B, 1, T, S] (True = attend), or None.
        cache: per-layer objects with update(k, v) -> (k, v) over the full context."""
        x = self.emb(ids)
        cos, sin = self.cos[pos].unsqueeze(1), self.sin[pos].unsqueeze(1)
        for i, blk in enumerate(self.blocks):
            x = blk(x, cos, sin, mask, None if cache is None else cache[i])
        return self.head(self.norm(x))


def _packed_mask_mod(doc, seg):
    def mask_mod(b, h, q, kv):
        return (doc[b, q] == doc[b, kv]) & (kv <= q) & ((seg[b, kv] == 0) | (seg[b, kv] == seg[b, q]))
    return mask_mod


def packed_block_mask(doc, seg):
    """A step attends to its chunk's listing (seg 0) and its own earlier tokens."""
    B, T = doc.shape
    return create_block_mask(_packed_mask_mod(doc, seg), B, None, T, T, device=doc.device, _compile=True)


def packed_dense_mask(doc, seg):
    """Same as packed_block_mask, as a dense [B, 1, T, T] bool mask."""
    T = doc.shape[1]
    q = torch.arange(T, device=doc.device)
    causal = q[:, None] >= q[None, :]
    same = doc[:, :, None] == doc[:, None, :]
    segok = (seg[:, None, :] == 0) | (seg[:, None, :] == seg[:, :, None])
    return (same & causal & segok)[:, None]
