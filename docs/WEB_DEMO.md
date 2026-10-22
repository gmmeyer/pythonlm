# Web demo: the model running in the browser

A page at `gmmeyer.com/pythonlm/` (static, GitHub Pages, repo `gmmeyer/gmmeyer`)
where you type a script and watch the model run it, step by step, next to what
real CPython prints. Everything runs on the visitor's machine; the weights come
from Hugging Face. The blog post draft is in the site repo on branch
`pythonlm-post` (`posts/teaching-a-model-to-run-python.html`).

## Status

Built and working end to end in Chromium with c2: the page compiles the
script with CPython 3.14 (Pyodide), runs the model on ONNX Runtime Web, shows
the listing, stack, variables and both outputs. Left to do: the shipped
checkpoint (c3 or later), fp16 weights, curated examples, Hugging Face upload,
the site integration, the measured gate through the page.

| Piece | Where | Status |
| --- | --- | --- |
| CPython 3.14 in the browser | Pyodide 314.0.7 (CPython 3.14.2), jsDelivr | Verified: identical listings |
| Runner | `src/bcvm/web.py`: async `harness.run`, speculative decoding, views for the page | Tested (`tests/test_web.py`) |
| Export | `bcvm export` (`src/bcvm/train/export.py`): ONNX + `.json` (shape, vocab, self-test) | Parity exact |
| Model in JS | `web/model.js`: the runner's model interface on ONNX Runtime Web 1.30 | Matches PyTorch |
| Worker | `web/worker.js`: Pyodide + ORT, backend self-test and choice, run protocol | Works |
| Page | `web/index.html`, `web/app.js` | Works; needs a design pass |
| Build | `web/build.py` → `web/dist/` (page, 12-module runtime zip, examples) | Works |

Local try-out: `bcvm export <ckpt> out/pythonlm.onnx`, then
`python web/build.py --gate <run dir> --model out/` and
`python -m http.server -d web/dist`, open `http://localhost:8000/?model=./model/`.
`?backend=webgpu|wasm` forces a backend.

## Verified (Oct 22)

- **Bytecode identity.** Pyodide's CPython 3.14.2 and training's 3.14.8 give
  identical token listings for all 1,620 hand-written and natural scripts,
  refusals included (`web/test/listings.py`).
- **Harness under WebAssembly.** All 600 hand-written scripts through
  `harness.run` with the oracle stepper in Pyodide: 0 mismatches against
  `exec`, ~56 µs of Python per step (`web/test/harness_check.py`).
- **Export parity.** On 960 hand-written steps (30,447 output tokens) ONNX
  Runtime and PyTorch fp32 differ by at most 7e-5 in a logit and agree on
  every argmax (`scripts/onnx_parity.py`).
- **The runner equals the PyTorch gate.** On 60 hand-written scripts
  (`scripts/web_gate.py`, ONNX on the CPU, fp32, speculative decoding) every
  script passes or fails exactly as in c2's PyTorch (bf16) gate.
- **The whole browser stack in Node** (`web/test/node_run.mjs`: Pyodide +
  `bcvm.web` + `model.js` on onnxruntime-web WASM): same pass/fail as the
  PyTorch gate, 12.6 steps/s.
- **In Chromium 152** (T3's preview browser): the division example matches
  Python, 20 steps in 1.7 s on the CPU backend.

## Inference

Per script: prefill the listing once and keep its KV cache. Per step: feed the
state, then decode the output until `<eos>`; the step's cache is dropped
before the next step. The graph is
`logits, k, v = f(ids, pos, prefix_k, prefix_v, step_k, step_v)` with caches
token-major (`[tokens, layers, heads, 64]`): the listing's stays as the session
returned it, the step's is one flat Float32Array in JS, so appending is a
`set()` and dropping rejected draft tokens is a length.

**Speculative decoding** (`bcvm.web.decode_greedy`): every output state is
mostly a copy of the input state, so drafts come from prompt lookup over the
input state (with the ip moved to the next instruction), the current
instruction's listing entry and the values of the names it reads, then the
listing. A draft is verified in one forward pass under grammar masks and kept
only as far as the model's own masked argmax agrees, so the output is exactly
greedy decoding. 4.5–5.3 passes per step instead of 26–45 single-token passes.
Nothing in a draft comes from the reference interpreter.

**Backends.** The worker runs the self-test (PyTorch's argmax at every output
position of 9 fixed steps, in the model's `.json`) on WebGPU and on the CPU
and uses the faster of those that pass, timed on decode-sized passes. In
Chromium 152:

- ONNX Runtime Web's `ort.all` bundle computes this model wrongly on WebGPU
  (logits off by ~25, also with graph optimizations off; layer by layer the
  same ops are right in smaller graphs). The `ort.webgpu` (JS kernels) and
  `ort.jspi` bundles match the CPU to 1e-5. The worker uses `ort.webgpu`.
- WebGPU takes 68 ms per decode-sized pass, the CPU 7.2 ms: the model is too
  small for the GPU to pay for its per-kernel overhead and the listing cache
  uploaded every pass. Keeping the listing cache on the GPU
  (`preferredOutputLocation: "gpu-buffer"`) might change that.
- WASM runs single-threaded: threads need cross-origin isolation, which GitHub
  Pages can't set as headers (`coi-serviceworker` would).

## Before publishing

1. Pick the checkpoint (latest phase C; it runs A and B scripts too).
2. fp16 weights (~53 MB instead of 106): weight-only, computed in fp32;
   ships only if `scripts/web_gate.py` gives the same results.
3. Curate examples (`web/build.py` picks passing hand-written scripts by
   length; titles are their first lines).
4. Gate through the page itself in headless Chrome on the hand-written sets,
   and quote those numbers in the post (the Cicero lesson).
5. Upload `pythonlm.onnx` and `pythonlm.json` to Hugging Face
   (`gmmeyer/pythonlm`?) and copy `web/dist/` minus `model/` to the site's
   `pythonlm/`. Both are yours to approve.
