# Web demo: the model running in the browser

Goal: a page at `gmmeyer.com/pythonlm/` (static, GitHub Pages, repo
`gmmeyer/gmmeyer`) where you type a script and watch the model run it, step by
step, next to what real CPython prints. Everything runs on the visitor's
machine; the weights come from Hugging Face. The blog post draft is in the site
repo on branch `pythonlm-post` (`posts/teaching-a-model-to-run-python.html`).

## Pieces

| Piece | Choice | Status |
| --- | --- | --- |
| CPython 3.14 in the browser | Pyodide 314.x (CPython 3.14.2 in WebAssembly), from the jsDelivr CDN | **Verified** (below) |
| Compile, support check, encode, grammar, validator | `bcvm` itself, unchanged, shipped as a zip of the pure-Python runtime modules | **Verified** (below) |
| Reference output | `exec` of the same script in Pyodide, shown next to the model's | Verified as part of the harness check |
| Model runtime | ONNX Runtime Web: WebGPU, falling back to WASM | To build |
| Weights | ONNX export, fp16 if it measures the same as fp32 (~52 MB), on Hugging Face (`gmmeyer/pythonlm`?) | To build |
| Loop | Async variant of `harness.run` (`bcvm/web.py`); model calls go to JS | To build |
| Page | Editor, examples, listing with the current instruction, stack, variables, both outputs | To build |

WebGL: ONNX Runtime's WebGL backend is deprecated and lacks ops this model
needs; WebGPU is in every current major browser, and the WASM backend is a
safe fallback (26M parameters is ~50 MFLOP per token). Cicero's WebGPU backend
produced garbage logits for that model, so the page runs a self-test at load
(below) and falls back to WASM if WebGPU disagrees.

## Verified so far (Oct 22, Node + Pyodide 314.0.7)

- **Bytecode identity.** Pyodide runs CPython 3.14.2; training used 3.14.8.
  All 1,620 hand-written and natural scripts (A–C) give token listings
  identical to native 3.14.8, refusals included. The model only knows the
  exact 3.14.8 bytecode, so this was the biggest risk.
- **Harness under WebAssembly.** All 600 hand-written scripts run through
  `harness.run` with the oracle stepper (listing, grammar parse, validator)
  in Pyodide, 0 mismatches against Pyodide's own `exec`. 159,584 steps in
  8.9 s: ~56 µs of Python per step, so the model is the whole cost.

Reproduce with `web/test/pyodide_run.mjs` (usage in its header):
`listings.py` writes the listings under either interpreter for comparison,
`harness_check.py` runs the oracle harness.

## Inference

Per script: run the listing once (≤1,408 tokens) and keep its KV cache. Per
step: append the state tokens (prefill), then decode the output until `<eos>`,
then drop the step's cache entries back to the listing. This is exactly how
the model was trained (each step attends to the listing and itself).

The ONNX graph: `logits, present_k, present_v = f(ids, pos, past_k, past_v)`,
with past/present `[layers, 1, heads, T, 64]`, RoPE on explicit positions,
and the cache concatenated inside the graph. With WebGPU, keep the cache on
the GPU between calls (`preferredOutputLocation: "gpu-buffer"`); with WASM the
cache is copied per call (16 MB at a 500-token context), which is acceptable.

**Speed.** A typical hand-written script is ~270 steps of ~60 output tokens:
~16K decode calls, ~50 s at ~3 ms each. Too slow for a demo, but most of every
output state is a copy of the input state. Prompt-lookup speculative decoding
(draft the continuation by matching the last few generated tokens against the
input state, verify the draft in one forward pass, keep the longest prefix the
model agrees with) should bring a step to a few forward passes. It's exact:
the output is identical to greedy decoding. The draft never comes from the
reference VM, so nothing about it is "the answer".

Grammar masks come from Python (`decoding.OutputGrammar`) per position: for a
draft of k tokens, Python walks the grammar along the draft and sends k masks
(354 bools each) with the verify call. JS applies them before the argmax.

## Ship what you measure

1. `scripts/export_onnx.py`: export, then run teacher-forced step error with
   onnxruntime (CPU) on `eval_test` subsets and require it to match PyTorch;
   then the hand-written gates with an ONNX-backed stepper. fp16 ships only if
   its gate numbers match fp32.
2. In the browser, a self-test at load: a few hundred fixed (input, expected
   argmax) pairs from the PyTorch model; WebGPU is used only if all match.
3. Before publishing: the hand-written sets through the actual page in
   headless Chrome (Playwright, WebGPU and WASM), compared with the PyTorch
   gate numbers. The blog quotes these.

## Hosting

- Static files (`index.html`, worker, `bcvm` zip, examples) in the site repo
  under `pythonlm/`. Pyodide and onnxruntime-web from jsDelivr; the model from
  `huggingface.co/<repo>/resolve/main/model.onnx` (both send CORS headers).
- WASM multithreading needs cross-origin isolation, which GitHub Pages can't
  set as headers; `coi-serviceworker` works, or the WASM fallback runs single
  threaded. WebGPU doesn't need it.
- Everything runs in a Web Worker so the page stays responsive; the worker
  posts each accepted step (listing index, stack, names, printed text).

## Order of work

1. ONNX export + parity + ONNX gate (Python, CPU; can run while training).
2. `bcvm/web.py`: async session API over `harness` (start, step, refusal,
   stdout), plus the speculative decode loop driver.
3. Worker + minimal page; Node/Playwright test harness; self-test vectors.
4. UI: listing with highlighted ip, stack and names, two outputs, speed
   control, examples that pass, clear refusals ("lists come in phase D").
5. Measure in headless Chrome, upload weights, open the site PR.

## Decisions for you

- Which checkpoint ships: the latest phase C model (it also runs A and B
  scripts), once its hand-written numbers are where you want them.
- Hugging Face repo name (Cicero is `gmmeyer/cicero`), and the URL path.
- Uploading to Hugging Face and pushing the site are yours to approve.
