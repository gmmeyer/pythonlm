"""generate -> compile -> support check -> execute -> check against CPython -> sample -> tokenize -> write.

One worker builds one shard end to end; shards are deterministic given
(phase, shard id, seed), and finished shards are skipped on re-run, so an
interrupted generation resumes where it stopped.
"""
import collections
import hashlib
import json
import multiprocessing as mp
import os
import random
import sys
import time
from array import array
from compression import zstd

from . import check, config, refvm, support, tokens
from .gen import common, make
from .program import CompileError
from .shards import ShardWriter
from .values import LimitExceeded, Unsupported

TRIVIAL = {"RESUME", "NOP", "NOT_TAKEN"}

DEFAULT_MIX = {
    "A": {"grammar": 0.75, "template": 0.15, "natural": 0.10},
    "B": {"grammar": 0.60, "template": 0.25, "natural": 0.15},
    "C": {"grammar": 0.60, "template": 0.20, "natural": 0.20},
}

HELD_OUT_PER_MILLE = {"val": 5, "test": 5}       # generated scripts, by listing hash
NATURAL_HELD_OUT_PER_MILLE = 100                 # natural base scripts held out entirely


class Skip(Exception):
    pass


def prepare(src, phase, bound=config.INT_BOUND, max_steps=config.MAX_STEPS):
    """Return (Program, Trace) for a script that is usable as data, else raise Skip.
    Raises check.Mismatch if the reference interpreter disagrees with CPython."""
    try:
        prog = support.check_source(src, phase)
    except (support.Refusal, CompileError) as e:
        raise Skip("refused") from e
    try:
        refvm.check_constants(prog, bound)
        trace = refvm.run(prog, max_steps, bound)
    except LimitExceeded as e:
        raise Skip("limit") from e
    except Unsupported as e:
        raise Skip("unsupported") from e
    check.differential_check(prog, trace)
    if trace.error is not None:
        raise Skip("pyerror")
    if trace.steps == 0:
        raise Skip("empty")
    return prog, trace


def _digest(data):
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "little")


def split_of(listing_ids, source, base_id):
    if source == "natural" and base_id is not None:
        h = _digest(f"natural:{base_id}".encode()) % 1000
        return "test" if h < NATURAL_HELD_OUT_PER_MILLE else "train"
    h = _digest(bytes(memoryview(_u16(listing_ids)))) % 1000
    if h < HELD_OUT_PER_MILLE["test"]:
        return "test"
    if h < HELD_OUT_PER_MILLE["test"] + HELD_OUT_PER_MILLE["val"]:
        return "val"
    return "train"


def _u16(ids):
    return array("H", ids)


def step_weight(prog, trace, i):
    s0, s1 = trace.states[i], trace.states[i + 1]
    op = prog.instrs[s0.ip].opname
    if op == "FOR_ITER" and s1.ip != s0.ip + 1:
        return 6.0        # loop exit
    if trace.outs[i]:
        return 4.0        # printed something
    if s1.ip != s0.ip + 1:
        return 2.0        # taken jump, break, continue
    if op in TRIVIAL:
        return 0.3
    if op == "LOAD_CONST" and type(prog.instrs[s0.ip].arg) is str and len(prog.instrs[s0.ip].arg) >= 4:
        return 3.0        # copying a label out of the listing, often one of several near-identical ones
    if op in ("BINARY_OP", "COMPARE_OP", "BUILD_STRING"):
        n = prog.instrs[s0.ip].arg if op == "BUILD_STRING" else 2
        if len(s0.stack) > n and type(s0.stack[-n - 1]) is str and any(type(v) is str for v in s0.stack[-n:]):
            return 4.0    # a string op above another string: c4 merged them into its result
    if op == "BINARY_OP":
        ins = prog.instrs[s0.ip]
        if tokens.work_kind(ins, s0):
            return 4.0    # // and %: the hardest arithmetic, see scripts/arith_probe.py
        if ins.arg in ("*", "*="):
            return 2.0
    return 1.0


def sample_steps(rng, prog, trace, k):
    """Weighted sample of k step indices without replacement (Efraimidis-Spirakis)."""
    n = trace.steps
    if n <= k:
        return list(range(n))
    keyed = [(rng.random() ** (1.0 / step_weight(prog, trace, i)), i) for i in range(n)]
    keyed.sort(reverse=True)
    return sorted(i for _, i in keyed[:k])


def encode_group(prog, trace, idxs):
    listing = tokens.ids(["<bos>"] + tokens.enc_listing(prog))
    steps = []
    for i in idxs:
        st = trace.states[i]
        s_in = tokens.enc_state(st)
        toks = tokens.enc_step(st, trace.states[i + 1], trace.outs[i], tokens.enc_work(prog.instrs[st.ip], st))
        if len(listing) + len(toks) > config.CONTEXT:
            raise Skip("too_long")
        steps.append((tokens.ids(toks), len(s_in) + 1))
    return listing, steps


def state_text(prog, st):
    """Compact human-readable state for records: 'ip|stack|names'."""
    stack = ",".join(_vtext(v) for v in st.stack)
    names = ",".join(f"{prog.names[k]}={_vtext(v)}" for k, v in sorted(st.names.items()))
    return f"{st.ip}|{stack}|{names}"


def _vtext(v):
    if type(v) in (int, bool, str) or v is None:
        return repr(v)
    return " ".join(tokens.enc_value(v))


def listing_text(prog):
    return [" ".join(tokens.enc_instr(ins)) for ins in prog.instrs]


def _record(prog, trace, src, source, base_id, split, idxs, full):
    rec = {"src": src, "source": source, "base": base_id, "split": split,
           "steps": trace.steps, "stdout": trace.stdout, "names": prog.names, "sampled": idxs}
    if full:
        rec["listing"] = listing_text(prog)
        rec["states"] = [state_text(prog, st) for st in trace.states]
        rec["outs"] = trace.outs
    return rec


def build_shard(job):
    """Worker entry point. job is a dict; returns the shard's metadata."""
    phase, shard_id, seed = job["phase"], job["shard_id"], job["seed"]
    stem = os.path.join(job["out_dir"], f"{phase}_{shard_id:04d}")
    os.makedirs(job["out_dir"], exist_ok=True)
    if os.path.exists(stem + ".json"):
        with open(stem + ".json") as f:
            return json.load(f)
    rng = random.Random(f"{phase}:{shard_id}:{seed}")
    mix = job["mix"]
    sources, weights = list(mix), list(mix.values())
    writer = ShardWriter(stem)
    want_split = job.get("split", "train")
    seen = set()
    stats = collections.Counter()
    ops = collections.Counter()
    by_source = collections.Counter()
    records = []
    t0 = time.time()
    target_scripts = job.get("target_scripts")
    min_steps = job.get("min_steps", 0)
    if job.get("literal_max"):
        common.LITERAL_MAX = job["literal_max"]
    while (stats["kept"] < target_scripts) if target_scripts else (writer.n_tokens < job["target_tokens"]):
        source = rng.choices(sources, weights)[0]
        src, base_id = make(rng, phase, source)
        stats["generated"] += 1
        try:
            prog, trace = prepare(src, phase, job.get("bound", config.INT_BOUND),
                                  job.get("max_steps", config.MAX_STEPS))
            listing = tokens.ids(["<bos>"] + tokens.enc_listing(prog))
            key = _digest(bytes(memoryview(_u16(listing))))
            if key in seen:
                raise Skip("duplicate")
            seen.add(key)
            split = split_of(listing, source, base_id)
            if split != want_split:
                raise Skip("held_out" if want_split == "train" else "not_" + want_split)
            if trace.steps < min_steps:
                raise Skip("short")
            idxs = sample_steps(rng, prog, trace, job["steps_per_script"])
            listing, steps = encode_group(prog, trace, idxs)
        except Skip as e:
            stats["skip:" + str(e)] += 1
            continue
        except check.Mismatch as e:
            _report_mismatch(job, src, e)
            raise
        writer.add_group(listing, steps)
        stats["kept"] += 1
        stats["steps_executed"] += trace.steps
        stats["steps_sampled"] += len(idxs)
        by_source[source] += 1
        for i in idxs:
            s0, s1 = trace.states[i], trace.states[i + 1]
            op = prog.instrs[s0.ip].opname
            ops[op] += 1
            if trace.outs[i]:
                ops["@print"] += 1
            if op == "FOR_ITER" and s1.ip != s0.ip + 1:
                ops["@loop_exit"] += 1
        if job.get("records"):
            records.append(_record(prog, trace, src, source, base_id, split, idxs, job["records"] == "full"))
    if records:
        blob = "\n".join(json.dumps(r, separators=(",", ":")) for r in records).encode()
        with open(stem + ".records.jsonl.zst.tmp", "wb") as f:
            f.write(zstd.compress(blob, level=6))
        os.replace(stem + ".records.jsonl.zst.tmp", stem + ".records.jsonl.zst")
    meta = {"phase": phase, "shard_id": shard_id, "seed": seed, "split": want_split,
            "mix": mix, "steps_per_script": job["steps_per_script"],
            "int_bound": job.get("bound", config.INT_BOUND), "max_steps": job.get("max_steps", config.MAX_STEPS),
            "python": sys.version.split()[0], "seconds": round(time.time() - t0, 1),
            "stats": dict(stats), "scripts_by_source": dict(by_source), "opcodes": dict(ops.most_common())}
    return writer.close(meta)


def _report_mismatch(job, src, err):
    path = os.path.join(job["out_dir"], "MISMATCH", f"{job['phase']}_{job['shard_id']:04d}.py")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(src)
        f.write("\n# " + str(err).replace("\n", "\n# ") + "\n")
    print(f"MISMATCH (reference interpreter bug) written to {path}:\n{err}", file=sys.stderr)


def generate(phase, out_dir, total_tokens, shard_tokens=50_000_000, workers=None, mix=None,
             steps_per_script=16, seed=0, records="full", split="train", first_shard=0, **extra):
    """Build ceil(total_tokens / shard_tokens) shards in parallel; returns the manifest."""
    mix = mix or DEFAULT_MIX[phase]
    n = max(1, -(-int(total_tokens) // int(shard_tokens)))
    jobs = [dict(phase=phase, shard_id=first_shard + i, seed=seed, out_dir=out_dir,
                 target_tokens=int(shard_tokens), mix=mix, steps_per_script=steps_per_script,
                 records=records, split=split, **extra) for i in range(n)]
    os.makedirs(out_dir, exist_ok=True)
    workers = workers or os.cpu_count()
    metas = []
    t0 = time.time()
    with mp.get_context("spawn").Pool(min(workers, n)) as pool:
        for meta in pool.imap_unordered(build_shard, jobs):
            metas.append(meta)
            done_tok = sum(m["n_tokens"] for m in metas)
            print(f"[{phase}] shard {meta['shard_id']:04d}: {meta['n_tokens'] / 1e6:.1f}M tokens, "
                  f"{meta['stats'].get('kept', 0)} scripts, {meta['seconds']}s "
                  f"({len(metas)}/{n}, {done_tok / 1e9:.2f}B total, {time.time() - t0:.0f}s)", flush=True)
    return write_manifest(out_dir)


def write_manifest(out_dir):
    from .shards import list_shards
    metas = []
    for stem in list_shards(out_dir):
        with open(stem + ".json") as f:
            metas.append(json.load(f))
    tot = collections.Counter()
    ops = collections.Counter()
    for m in metas:
        tot["tokens"] += m["n_tokens"]
        tot["steps"] += m["n_steps"]
        for k, v in m["stats"].items():
            tot[k] += v
        ops.update(m["opcodes"])
    manifest = {"shards": [os.path.basename(f"{m['phase']}_{m['shard_id']:04d}") for m in sorted(
                    metas, key=lambda m: m["shard_id"])],
                "totals": dict(tot), "opcodes": dict(ops.most_common()),
                "vocab_hash": tokens.VOCAB_HASH, "vocab_size": tokens.VOCAB_SIZE,
                "format_version": config.FORMAT_VERSION}
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    return manifest
