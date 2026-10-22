"""Assemble the demo's static files in web/dist/ (copy them to the site's
pythonlm/ directory):

    index.html app.js worker.js model.js   the page
    pythonlm-runtime.zip                   the bcvm modules bcvm.web imports, for Pyodide
    examples.json                          hand-written scripts the model gets right
    model/                                 with --model: a local export, for ?model=./model/

  python web/build.py --gate $BCVM_DATA/runs/c2 --model out/   # out/ has pythonlm.onnx + .json
  python -m http.server -d web/dist      # then open http://localhost:8000/?model=./model/
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile

WEB = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(WEB)
SRC = os.path.join(ROOT, "src")
PAGE = ["index.html", "app.js", "worker.js", "model.js"]

KIND = {"A": "Numbers", "B": "Loops", "C": "Strings"}
# The post's division example first, then hand-written scripts.
FIRST = ("Long division", "n = 487\nq = n // 13\nprint(q)\nprint(n % 13)\n")


def runtime_modules():
    """The bcvm modules that importing bcvm.web loads (no numpy, no torch)."""
    code = ("import sys; sys.path.insert(0, sys.argv[1]); import bcvm.web; "
            "print('\\n'.join(sorted(m for m in sys.modules if m == 'bcvm' or m.startswith('bcvm.'))))")
    mods = subprocess.run([sys.executable, "-c", code, SRC], check=True, capture_output=True, text=True).stdout.split()
    assert not any(m.startswith(("bcvm.train", "bcvm.shards", "bcvm.pipeline")) for m in mods), mods
    return mods


def write_runtime(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for mod in runtime_modules():
            rel = mod.replace(".", "/")
            rel += "/__init__.py" if os.path.isdir(os.path.join(SRC, rel)) else ".py"
            z.write(os.path.join(SRC, rel), rel)


def examples(gate_dir, per_phase, max_steps):
    sys.path.insert(0, SRC)
    from bcvm import refvm, support
    from bcvm.program import Program
    out = [dict(title=FIRST[0], src=FIRST[1])]
    for ph in "ABC":
        with open(os.path.join(gate_dir, f"gate_handwritten_{ph}.json")) as f:
            failing = {r["file"] for r in json.load(f)["failures"]}
        d = os.path.join(ROOT, "eval", "handwritten", f"phase{ph}")
        picks = []
        for name in sorted(os.listdir(d)):
            if not name.endswith(".py") or name in failing:
                continue
            with open(os.path.join(d, name)) as f:
                src = f.read()
            prog = Program(src)
            support.check(prog, ph)
            steps = refvm.run(prog, 10_000).steps
            if steps <= max_steps:
                lines = [ln.strip() for ln in src.splitlines() if ln.strip()]
                title = lines[0].lstrip("# ") if lines[0].startswith("#") else lines[0]
                title = title if len(title) <= 56 else title[:55] + "…"
                picks.append((steps, dict(title=f"{KIND[ph]}: {title}", src=src)))
        # a spread of lengths rather than only the shortest
        picks.sort(key=lambda p: p[0])
        step = max(1, len(picks) // per_phase)
        out += [p[1] for p in picks[::step][:per_phase]]
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gate", required=True, help="run dir with gate_handwritten_{A,B,C}.json for the shipped model")
    p.add_argument("--model", help="dir with pythonlm.onnx and pythonlm.json to copy into dist/model/")
    p.add_argument("--per-phase", type=int, default=6)
    p.add_argument("--max-steps", type=int, default=250)
    a = p.parse_args()
    dist = os.path.join(WEB, "dist")
    os.makedirs(dist, exist_ok=True)
    for name in PAGE:
        shutil.copy(os.path.join(WEB, name), dist)
    write_runtime(os.path.join(dist, "pythonlm-runtime.zip"))
    with open(os.path.join(dist, "examples.json"), "w") as f:
        json.dump(examples(a.gate, a.per_phase, a.max_steps), f, indent=1)
    if a.model:
        os.makedirs(os.path.join(dist, "model"), exist_ok=True)
        for name in ("pythonlm.onnx", "pythonlm.json"):
            shutil.copy(os.path.join(a.model, name), os.path.join(dist, "model", name))
    print(f"built {dist}: {sorted(os.listdir(dist))}")


if __name__ == "__main__":
    main()
