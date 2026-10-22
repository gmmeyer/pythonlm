# Run every hand-written script through the bcvm harness with the oracle
# stepper (reference VM behind the token interface: listing, grammar parse,
# validator) and compare with CPython's own exec of the script.
import contextlib
import io
import os
import sys
import time

ROOT = sys.argv[1]
sys.path.insert(0, os.path.join(ROOT, "src"))
from bcvm import harness  # noqa: E402

t0, n, bad, steps = time.time(), 0, [], 0
for ph in "ABC":
    d = os.path.join(ROOT, "eval/handwritten", f"phase{ph}")
    for name in sorted(os.listdir(d)):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(d, name)) as f:
            src = f.read()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(src, "<script>", "exec"), {})
        res = harness.run(src, ph, harness.OracleStepper())
        n += 1
        steps += res.steps
        if res.stdout != buf.getvalue() or res.error or res.refused:
            bad.append((name, res.error or res.refused))
print(sys.version.split()[0], f"{n} scripts, {steps} steps, {len(bad)} mismatches, {time.time() - t0:.1f}s", bad[:5])
