"""bcvm command line. Run `bcvm <command> -h` for options."""
import argparse
import json
import os
import random
import sys
import time

from . import config


def _phase_for(src):
    """Smallest phase that accepts src, or None."""
    from . import support
    from .phases import PHASES
    from .program import Program
    prog = Program(src)
    for p in PHASES:
        try:
            support.check(prog, p)
            return p
        except support.Refusal:
            continue
    return None


def cmd_check(a):
    from . import check, pipeline, refvm, support, tokens
    from .program import Program
    bad = 0
    for path in a.files:
        src = open(path).read()
        try:
            prog = Program(src)
            phase = a.phase or _phase_for(src) or "C"
            support.check(prog, phase)
        except (support.Refusal, support.CompileError) as e:
            print(f"{path}: refused ({e})")
            bad += 1
            continue
        try:
            trace = refvm.run(prog, a.max_steps, a.bound)
            check.differential_check(prog, trace)
        except check.Mismatch as e:
            print(f"{path}: MISMATCH\n{e}")
            bad += 1
            continue
        except Exception as e:  # noqa: BLE001
            print(f"{path}: {type(e).__name__}: {e}")
            bad += 1
            continue
        status = f"raises {trace.error.exc_type}" if trace.error else "ok"
        print(f"{path}: phase {phase}, {trace.steps} steps, listing {len(tokens.enc_listing(prog))} tokens, "
              f"{len(prog.names)} names, {status}")
        if a.verbose:
            for line in pipeline.listing_text(prog):
                print("   ", line)
            for i, st in enumerate(trace.states[: a.verbose]):
                print(f"  {i:4d} {pipeline.state_text(prog, st)}  {trace.outs[i]!r}" if i < trace.steps else f"  {i:4d} {pipeline.state_text(prog, st)}")
    return 1 if bad else 0


def cmd_show(a):
    from . import refvm, support, tokens
    src = open(a.file).read()
    prog = support.check_source(src, a.phase or _phase_for(src) or "C")
    trace = refvm.run(prog)
    print(" ".join(["<bos>"] + tokens.enc_listing(prog)))
    for i in range(min(a.steps, trace.steps)):
        st = trace.states[i]
        print(" ".join(tokens.enc_step(st, trace.states[i + 1], trace.outs[i], tokens.enc_work(prog.instrs[st.ip], st))))
    return 0


def cmd_run(a):
    from . import harness
    src = open(a.file).read()
    phase = a.phase or _phase_for(src) or "C"
    if a.ckpt:
        from .train import stepper
        return stepper.run_script(a.file, a.ckpt, phase)
    return harness.main_run(a.file, phase, oracle=True)


def cmd_gen(a):
    from . import pipeline
    config.require_pinned_python()
    mix = json.loads(a.mix) if a.mix else None
    out = a.out or os.path.join(config.DATA_DIR, f"phase{a.phase}", "train")
    t0 = time.time()
    m = pipeline.generate(a.phase, out, float(a.tokens), shard_tokens=float(a.shard_tokens), workers=a.workers,
                          mix=mix, steps_per_script=a.k, seed=a.seed, records=a.records, first_shard=a.first_shard)
    tot = m["totals"]
    print(f"done in {time.time() - t0:.0f}s: {tot['tokens'] / 1e9:.2f}B tokens, {tot['steps'] / 1e6:.1f}M steps, "
          f"{tot.get('kept', 0)} scripts -> {out}")
    return 0


def cmd_evalset(a):
    from . import evalsets
    config.require_pinned_python()
    out = a.out or os.path.join(config.DATA_DIR, f"phase{a.phase}", f"eval_{a.name}")
    evalsets.build(a.phase, out, a.name, a.scripts, workers=a.workers, seed=a.seed,
                   max_steps=a.max_steps, bound=a.bound)
    return 0


def cmd_inspect(a):
    from . import tokens
    from .shards import Shard
    sh = Shard(a.stem)
    print(json.dumps({k: v for k, v in sh.meta.items() if k not in ("opcodes",)}, indent=1))
    rng = random.Random(a.seed)
    for i in rng.sample(range(len(sh)), min(a.n, len(sh))):
        ids, mask = sh.example(int(i))
        toks = tokens.strs(ids.tolist())
        first = int(mask.argmax())
        print(f"--- example {i}: {len(ids)} tokens, loss on last {int(mask.sum())}")
        print(" ".join(toks[:first]))
        print(">>> " + " ".join(toks[first:]))
    return 0


def cmd_bench(a):
    from . import pipeline
    job = dict(phase=a.phase, shard_id=9999, seed=a.seed, out_dir=a.out, target_tokens=int(float(a.tokens)),
               mix=pipeline.DEFAULT_MIX[a.phase], steps_per_script=a.k, records=a.records)
    stem = os.path.join(a.out, f"{a.phase}_9999")
    for ext in (".json", ".bin", ".idx.npy", ".records.jsonl.zst"):
        if os.path.exists(stem + ext):
            os.remove(stem + ext)
    t0 = time.time()
    m = pipeline.build_shard(job)
    dt = time.time() - t0
    st = m["stats"]
    print(json.dumps({"tokens_per_s_per_core": round(m["n_tokens"] / dt), "scripts_per_s_per_core": round(st["kept"] / dt, 1),
                      "tokens_per_step": round(m["n_tokens"] / m["n_steps"], 1),
                      "tokens_per_script": round(m["n_tokens"] / st["kept"]),
                      "steps_executed_per_script": round(st["steps_executed"] / st["kept"], 1),
                      "keep_rate": round(st["kept"] / st["generated"], 3), "stats": st}, indent=1))
    return 0


def cmd_train(a):
    from .train import train
    train.train(a)
    return 0


def cmd_evalsteps(a):
    from .train import train
    train.evalsteps(a)
    return 0


def cmd_gate(a):
    from .train import stepper
    stepper.gate(a)
    return 0


def cmd_export(a):
    from .train import export
    export.cmd_export(a)
    return 0


def main(argv=None):
    from . import train
    p = argparse.ArgumentParser(prog="bcvm", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("check", help="support check + reference run + CPython comparison")
    s.add_argument("files", nargs="+")
    s.add_argument("--phase")
    s.add_argument("--max-steps", type=int, default=100_000)
    s.add_argument("--bound", type=int, default=10**9)
    s.add_argument("-v", "--verbose", type=int, default=0, help="print the listing and the first N states")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("show", help="print a script's listing and first steps as tokens")
    s.add_argument("file")
    s.add_argument("--phase")
    s.add_argument("--steps", type=int, default=5)
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("run", help="run a script through the harness (oracle stepper, or the model with --ckpt)")
    s.add_argument("file")
    s.add_argument("--phase")
    s.add_argument("--ckpt", help="model checkpoint; default is the oracle stepper")
    s.set_defaults(fn=cmd_run)

    s = sub.add_parser("gen", help="generate training shards for a phase")
    s.add_argument("--phase", required=True)
    s.add_argument("--tokens", default="1e9")
    s.add_argument("--shard-tokens", default="5e7")
    s.add_argument("--out")
    s.add_argument("--workers", type=int)
    s.add_argument("--mix", help='JSON, e.g. {"grammar": 0.6, "template": 0.2, "natural": 0.2}')
    s.add_argument("-k", type=int, default=16, help="steps sampled per script")
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--first-shard", type=int, default=0)
    s.add_argument("--records", default="full", choices=["full", "light", ""])
    s.set_defaults(fn=cmd_gen)

    s = sub.add_parser("evalset", help="build a held-out eval set (scripts + per-step shard)")
    s.add_argument("--phase", required=True)
    s.add_argument("--name", default="test", help="test | long | bignum | natural")
    s.add_argument("--scripts", type=int, default=5000)
    s.add_argument("--out")
    s.add_argument("--workers", type=int)
    s.add_argument("--seed", type=int, default=1)
    s.add_argument("--max-steps", type=int)
    s.add_argument("--bound", type=int)
    s.set_defaults(fn=cmd_evalset)

    s = sub.add_parser("inspect", help="decode a few examples from a shard")
    s.add_argument("stem", help="shard path without extension")
    s.add_argument("-n", type=int, default=3)
    s.add_argument("--seed", type=int, default=0)
    s.set_defaults(fn=cmd_inspect)

    s = sub.add_parser("bench", help="measure single-core generation throughput")
    s.add_argument("--phase", default="B")
    s.add_argument("--tokens", default="2e6")
    s.add_argument("--out", default="/tmp/bcvm-bench")
    s.add_argument("-k", type=int, default=16)
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--records", default="full", choices=["full", "light", ""])
    s.set_defaults(fn=cmd_bench)

    s = sub.add_parser("train", help="train the step model on packed shards (5090 box)")
    train.add_train_args(s)
    s.set_defaults(fn=cmd_train)

    s = sub.add_parser("evalsteps", help="teacher-forced per-step exact match of a checkpoint, by opcode")
    train.add_evalsteps_args(s)
    s.set_defaults(fn=cmd_evalsteps)

    s = sub.add_parser("gate", help="end-to-end stdout match of a checkpoint on an eval set's scripts")
    train.add_gate_args(s)
    s.set_defaults(fn=cmd_gate)

    s = sub.add_parser("export", help="ONNX export with an explicit KV cache, for the web demo (needs --extra export)")
    s.add_argument("ckpt")
    s.add_argument("out", help="path of the .onnx file; a .json sidecar is written next to it")
    s.set_defaults(fn=cmd_export)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
