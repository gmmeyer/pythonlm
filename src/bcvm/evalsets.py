"""Held-out eval sets. Every script comes from the test split (by listing hash,
or by natural base script), so none of them can appear in training shards.

Each set is a directory of shards whose records hold the source, CPython's
stdout and the step count (for end-to-end stdout match), and whose steps are
*all* the script's steps, unweighted (for teacher-forced per-step accuracy
on the real step distribution).

  test     generated scripts, standard mix and limits
  natural  variants of the natural scripts held out from training
  long     1,000-10,000 executed instructions, for the length curve
  bignum   ints up to 99,999, beyond the training bound
"""
import json
import multiprocessing as mp
import os

from . import config, pipeline
from .shards import list_shards

SETS = {
    "test": dict(),
    "natural": dict(mix={"natural": 1.0}),
    "long": dict(max_steps=10_000, min_steps=1_000),
    "bignum": dict(bound=99_999, literal_max=99_999),
}


def build(phase, out_dir, name, n_scripts, workers=None, seed=1, max_steps=None, bound=None):
    spec = dict(SETS[name])
    if max_steps:
        spec["max_steps"] = max_steps
    if bound:
        spec["bound"] = bound
    mix = spec.pop("mix", pipeline.DEFAULT_MIX[phase])
    workers = workers or os.cpu_count()
    per = -(-n_scripts // workers)
    jobs = [dict(phase=phase, shard_id=i, seed=f"eval-{name}-{seed}", out_dir=out_dir, target_tokens=0,
                 target_scripts=per, mix=mix, steps_per_script=spec.get("max_steps", config.MAX_STEPS),
                 records="full", split="test", **spec) for i in range(workers)]
    os.makedirs(out_dir, exist_ok=True)
    with mp.get_context("spawn").Pool(workers) as pool:
        for meta in pool.imap_unordered(pipeline.build_shard, jobs):
            print(f"[eval {phase}/{name}] shard {meta['shard_id']}: {meta['stats'].get('kept', 0)} scripts, "
                  f"{meta['n_steps']} steps, {meta['seconds']}s", flush=True)
    manifest = pipeline.write_manifest(out_dir)
    manifest["eval_set"] = dict(name=name, phase=phase, **spec)
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    return list_shards(out_dir)
