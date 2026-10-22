// The whole browser stack in Node: Pyodide runs bcvm.web (compile, support
// check, grammar, validator, speculative decoding) and calls web/model.js on
// onnxruntime-web (WASM backend), on the first N hand-written scripts per
// phase. Compares each script's pass/fail with the PyTorch gate's JSON.
//
//   npm install pyodide@314.0.7 onnxruntime-web@1.30.0     (in a scratch directory)
//   node web/test/node_run.mjs <scratch>/node_modules <model.onnx> <gate dir with gate_handwritten_X.json> [N]
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { StepModel } from "../model.js";

const [nm, onnxPath, gateDir, perPhase = "5"] = process.argv.slice(2);
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const ort = await import(pathToFileURL(path.join(nm, "onnxruntime-web", "dist", "ort.node.min.mjs")).href);
const meta = JSON.parse(readFileSync(onnxPath.replace(/\.onnx$/, ".json"), "utf8"));
const model = await StepModel.load(ort, readFileSync(onnxPath), meta, { executionProviders: ["wasm"] });

const pyDir = path.join(nm, "pyodide");
const { loadPyodide } = await import(pathToFileURL(path.join(pyDir, "pyodide.mjs")).href);
const py = await loadPyodide({ indexURL: pyDir + path.sep });
py.FS.mkdirTree("/repo");
py.FS.mount(py.FS.filesystems.NODEFS, { root: repo.replaceAll("\\", "/") }, "/repo");
py.globals.set("js_model", model);
py.globals.set("PER_PHASE", Number(perPhase));

const t0 = Date.now();
const rows = (await py.runPythonAsync(`
import os, sys
sys.path.insert(0, "/repo/src")
from bcvm import refvm, support, web
from bcvm.program import Program

m = web.JsModel(js_model)
rows = []
for ph in "ABC":
    d = f"/repo/eval/handwritten/phase{ph}"
    for name in sorted(f for f in os.listdir(d) if f.endswith(".py"))[:PER_PHASE]:
        src = open(os.path.join(d, name)).read()
        prog = Program(src)
        support.check(prog, ph)
        truth = refvm.run(prog, 10_000)
        stats = web.Stats()
        res = await web.run(src, ph, m, max_steps=2 * truth.steps + 100, stats=stats)
        rows.append([ph, name, res.stdout == truth.stdout and not res.error, stats.steps, stats.forwards])
rows
`)).toJs();
const secs = (Date.now() - t0) / 1000;

let steps = 0, forwards = 0, differ = [];
for (const ph of "ABC") {
  const gate = path.join(gateDir, `gate_handwritten_${ph}.json`);
  const failing = existsSync(gate) ? new Set(JSON.parse(readFileSync(gate, "utf8")).failures.map((f) => f.file)) : null;
  const mine = rows.filter((r) => r[0] === ph);
  for (const [, name, ok, s, f] of mine) {
    steps += s;
    forwards += f;
    if (failing && ok === failing.has(name)) differ.push(`${name} ${ok ? "passes" : "fails"}`);
  }
  console.log(`phase ${ph}: ${mine.filter((r) => r[2]).length}/${mine.length} match`);
}
console.log(`${steps} steps in ${secs.toFixed(0)}s (${(steps / secs).toFixed(1)} steps/s, ${(forwards / steps).toFixed(2)} forwards per step); ` +
  `differs from the torch gate on ${differ.length ? differ.join(", ") : "none"}`);
