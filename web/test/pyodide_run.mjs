// Run a Python file under Pyodide (CPython 3.14 in WebAssembly) in Node, with
// the repo mounted at /repo and the current directory at /cwd.
//
//   npm install pyodide@314.0.7    (in a scratch directory)
//   node web/test/pyodide_run.mjs <scratch>/node_modules/pyodide web/test/listings.py /repo /cwd/pyodide.json
//   node web/test/pyodide_run.mjs <scratch>/node_modules/pyodide web/test/harness_check.py /repo
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const [pkgDir, file, ...args] = process.argv.slice(2);
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const { loadPyodide } = await import(pathToFileURL(path.join(pkgDir, "pyodide.mjs")).href);
const py = await loadPyodide({ indexURL: pkgDir + path.sep });
for (const [mnt, dir] of [["/repo", repo], ["/cwd", process.cwd()]]) {
  py.FS.mkdirTree(mnt);
  py.FS.mount(py.FS.filesystems.NODEFS, { root: dir }, mnt);
}
py.globals.set("ARGV", py.toPy([file, ...args]));
py.runPython("import sys; sys.argv = list(ARGV)\n" + readFileSync(file, "utf8"));
