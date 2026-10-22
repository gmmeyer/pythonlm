# Compile eval and natural scripts and write their token listings as JSON.
# Run under native CPython and under Pyodide to check the bytecode matches.
import json
import os
import sys

ROOT, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(ROOT, "src"))
from bcvm import support, tokens  # noqa: E402

out = {}
for top in ("eval/handwritten", "natural"):
    for ph in "ABC":
        d = os.path.join(ROOT, top, f"phase{ph}")
        for name in sorted(os.listdir(d)):
            if not name.endswith(".py"):
                continue
            with open(os.path.join(d, name)) as f:
                src = f.read()
            key = f"{top}/phase{ph}/{name}"
            try:
                out[key] = " ".join(tokens.enc_listing(support.check_source(src, ph)))
            except Exception as e:
                out[key] = f"ERR {type(e).__name__}: {str(e)[:80]}"
with open(OUT, "w") as f:
    json.dump({"version": sys.version, "listings": out}, f)
print(sys.version, len(out), "scripts")
