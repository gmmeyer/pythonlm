"""Packed training and teacher-forced step eval for the step model.

  bcvm train --name a1 --data A=1 --tokens 1e9
  bcvm evalsteps $BCVM_DATA/runs/a1/final.pt phaseA/eval_test
"""
import json
import math
import os
import time
from dataclasses import asdict

import numpy as np
import torch
import torch.nn.functional as F

from .. import config, tokens
from ..shards import list_shards
from .data import EvalSet, TrainStream, batches, pack, phase_dir
from .model import ModelConfig, StepModel, packed_block_mask


def to_device(batch, dev):
    return {k: v.to(dev, non_blocking=True) for k, v in batch.items()}


def forward(model, b):
    with torch.autocast("cuda", torch.bfloat16):
        return model(b["ids"], b["pos"], packed_block_mask(b["doc"], b["seg"]))


def load_model(path, dev="cuda"):
    ck = torch.load(path, map_location="cpu", weights_only=False)
    if ck["vocab_hash"] != tokens.VOCAB_HASH:
        raise ValueError(f"{path}: vocab hash {ck['vocab_hash']} != {tokens.VOCAB_HASH}")
    model = StepModel(ModelConfig(**ck["cfg"]))
    model.load_state_dict(ck["model"])
    return model.to(dev), ck


@torch.no_grad()
def evaluate(model, directory, seq_len, rows, max_steps=None):
    """Teacher-forced exact match: a step is right if argmax gets every output token right."""
    ev = EvalSet(directory, max_steps)
    dev = next(model.parameters()).device
    wrong = torch.zeros(ev.max_steps, dtype=torch.int64, device=dev)
    tok_n = torch.zeros((), dtype=torch.int64, device=dev)
    tok_bad = torch.zeros_like(tok_n)
    loss = torch.zeros((), device=dev)
    for b in batches(pack(ev.groups(), seq_len), rows, seq_len):
        b = to_device(b, dev)
        logits = forward(model, b).float()
        t = b["tgt"]
        loss += F.cross_entropy(logits.flatten(0, 1), t.flatten(), ignore_index=-1, reduction="sum")
        bad = (logits.argmax(-1) != t) & (t >= 0)
        wrong.index_add_(0, b["sid"].clamp(min=0).flatten(), bad.flatten().long())
        tok_n += (t >= 0).sum()
        tok_bad += bad.sum()
    n = len(ev.opcode)
    wrong = wrong[:n].cpu().numpy() > 0
    opcode, prints = np.array(ev.opcode), np.array(ev.prints)
    by_op = {tokens.VOCAB[op]: [int((opcode == op).sum()), int(wrong[opcode == op].sum())]
             for op in np.unique(opcode)}
    return dict(set=directory, steps=n, step_errors=int(wrong.sum()), step_err=float(wrong.mean()),
                tok_err=tok_bad.item() / max(1, tok_n.item()), loss=loss.item() / max(1, tok_n.item()),
                print_steps=[int(prints.sum()), int(wrong[prints].sum())], by_opcode=by_op)


def format_eval(r, top=8):
    n, e = r["steps"], r["step_errors"]
    bound = f"{e / n:.2e}" if e else f"0 (<{3 / n:.1e} at 95%)"
    lines = [f"eval {os.path.relpath(r['set'], config.DATA_DIR)}: {n} steps, step err {bound}, "
             f"tok err {r['tok_err']:.2e}, loss {r['loss']:.5f}, print steps {r['print_steps'][1]}/{r['print_steps'][0]} wrong"]
    worst = sorted(r["by_opcode"].items(), key=lambda kv: -kv[1][1])[:top]
    lines.append("  " + "  ".join(f"{op} {w}/{c}" for op, (c, w) in worst if w))
    return "\n".join(lines)


def lr_at(step, total, a):
    if step < a.warmup:
        return a.lr * (step + 1) / a.warmup
    t = min(1.0, (step - a.warmup) / max(1, total - a.warmup))
    return a.lr * (a.min_lr + (1 - a.min_lr) * 0.5 * (1 + math.cos(math.pi * t)))


def parse_mix(spec):
    sources = []
    for part in spec.split(","):
        phase, _, w = part.partition("=")
        stems = list_shards(phase_dir(config.DATA_DIR, phase.strip(), "train"))
        if not stems:
            raise SystemExit(f"no shards for phase {phase}")
        sources.append((float(w or 1), stems))
    return sources


def run_args(a):
    return {k: v for k, v in vars(a).items() if k != "fn"}


def save(path, model, opt, step, seen, a):
    tmp = path + ".tmp"
    torch.save(dict(model=model.state_dict(), opt=opt.state_dict(), step=step, tokens=seen,
                    cfg=asdict(model.cfg), args=run_args(a), vocab_hash=tokens.VOCAB_HASH), tmp)
    os.replace(tmp, path)


def train(a):
    dev = "cuda"
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    out = a.out or os.path.join(config.DATA_DIR, "runs", a.name)
    os.makedirs(out, exist_ok=True)
    log = open(os.path.join(out, "log.jsonl"), "a")

    def emit(line, **rec):
        print(line, flush=True)
        log.write(json.dumps(dict(rec, time=time.time())) + "\n")
        log.flush()

    ck = None
    if a.resume and os.path.exists(os.path.join(out, "latest.pt")):
        ck = torch.load(os.path.join(out, "latest.pt"), map_location="cpu", weights_only=False)
        cfg = ModelConfig(**ck["cfg"])
    elif a.init:
        init = torch.load(a.init, map_location="cpu", weights_only=False)
        cfg = ModelConfig(**init["cfg"])
    else:
        cfg = ModelConfig(d_model=a.d_model, n_layers=a.layers, n_heads=a.heads, d_ff=a.d_ff)
    torch.manual_seed(a.seed)
    model = StepModel(cfg).to(dev)
    if ck is None and a.init:
        model.load_state_dict(init["model"])

    decay = [p for n, p in model.named_parameters() if p.dim() == 2 and not n.startswith("emb")]
    other = [p for n, p in model.named_parameters() if not (p.dim() == 2 and not n.startswith("emb"))]
    opt = torch.optim.AdamW([dict(params=decay, weight_decay=a.wd), dict(params=other, weight_decay=0.0)],
                            lr=a.lr, betas=(0.9, 0.95), fused=True)
    step, seen = 0, 0
    if ck is not None:
        model.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        step, seen = ck["step"], ck["tokens"]

    per_step = a.seq_len * a.rows * a.accum
    total = math.ceil(float(a.tokens) / per_step)
    n_params = model.n_params()
    flops_per_tok = 6 * model.n_params(embeddings=False)
    eval_dir = os.path.join(config.DATA_DIR, a.eval_set or f"phase{a.data.split('=')[0].strip()}/eval_test")
    emit(f"run {a.name}: {n_params / 1e6:.1f}M params, {per_step} tokens/step, {total} steps "
         f"({float(a.tokens) / 1e9:.2f}B tokens), data {a.data}, out {out}",
         kind="start", params=n_params, cfg=asdict(cfg), args=run_args(a), total_steps=total)

    cmodel = torch.compile(model) if a.compile else model
    loader = torch.utils.data.DataLoader(
        TrainStream(parse_mix(a.data), a.seq_len, a.rows, seed=a.seed + step), batch_size=None,
        num_workers=a.workers, pin_memory=True, prefetch_factor=4, persistent_workers=True)
    it = iter(loader)

    t0 = time.perf_counter()
    tok_window, loss_tok_window = 0, 0
    while step < total:
        lr = lr_at(step, total, a)
        for g in opt.param_groups:
            g["lr"] = lr
        micro = [next(it) for _ in range(a.accum)]
        n_loss = sum(int((m["tgt"] >= 0).sum()) for m in micro)
        loss_sum = 0.0
        for m in micro:
            m = to_device(m, dev)
            logits = forward(cmodel, m)
            loss = F.cross_entropy(logits.float().flatten(0, 1), m["tgt"].flatten(), ignore_index=-1,
                                   reduction="sum") / n_loss
            loss.backward()
            loss_sum += loss.detach()
        gnorm = torch.nn.utils.clip_grad_norm_(model.parameters(), a.clip)
        opt.step()
        opt.zero_grad(set_to_none=True)
        step += 1
        seen += per_step
        tok_window += per_step
        loss_tok_window += n_loss

        if step % a.log_every == 0 or step == total:
            loss_v = float(loss_sum)
            dt = time.perf_counter() - t0
            tps = tok_window / dt
            eta = (total - step) * per_step / tps
            emit(f"step {step}/{total} | loss {loss_v:.5f} | lr {lr:.2e} | gnorm {float(gnorm):.3f} | "
                 f"{tps / 1e3:.0f}K tok/s ({loss_tok_window / dt / 1e3:.0f}K loss tok/s) | "
                 f"{tps * flops_per_tok / 1e12:.1f} TFLOPS (6N) | {seen / 1e9:.3f}B tok | ETA {eta / 60:.0f}m",
                 kind="train", step=step, loss=loss_v, lr=lr, gnorm=float(gnorm), tok_s=tps,
                 loss_tok_s=loss_tok_window / dt, tokens=seen, mem_gb=torch.cuda.max_memory_allocated() / 1e9)
            t0, tok_window, loss_tok_window = time.perf_counter(), 0, 0

        if step % a.ckpt_every == 0 or step == total:
            save(os.path.join(out, "latest.pt"), model, opt, step, seen, a)
        if step % a.eval_every == 0 or step == total:
            r = evaluate(cmodel, eval_dir, a.seq_len, a.rows, None if step == total else a.eval_steps)
            emit(format_eval(r), kind="eval", step=step, **r)
            t0 = time.perf_counter()
    save(os.path.join(out, "final.pt"), model, opt, step, seen, a)
    emit(f"done: {step} steps, {seen / 1e9:.2f}B tokens -> {out}/final.pt", kind="done", step=step)


def evalsteps(a):
    model, ck = load_model(a.ckpt)
    model.eval()
    cmodel = torch.compile(model) if a.compile else model
    results = []
    for s in a.sets:
        r = evaluate(cmodel, os.path.join(config.DATA_DIR, s), a.seq_len, a.rows, a.max_steps)
        print(format_eval(r, top=30), flush=True)
        results.append(r)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(dict(ckpt=a.ckpt, step=ck["step"], results=results), f, indent=1)
