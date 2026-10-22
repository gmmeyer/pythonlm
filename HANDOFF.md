# Handoff

> Generated: 2026-10-21 21:05 EDT  
> Project: pythonlm (github.com/gmmeyer/pythonlm, private)  
> Session summary: On the Mac Studio we built the harness and data pipeline for a learned CPython bytecode interpreter and generated phases A–C training data plus eval sets. Next is training on the Windows RTX 5090 box.

## Goal

The goal is a learned Python runtime. Given a script, CPython 3.14 compiles it, and
a small decoder-only transformer executes the bytecode one instruction at a time
(state t → state t+1). A harness validates every step and streams stdout. The
output must match CPython exactly. Scripts outside the supported subset are
refused up front. The subset grows by phase: A arithmetic/print, B control
flow, C strings, D lists, E functions, F dicts. A phase is done at 99% exact
stdout match on held-out scripts of up to 1,000 instructions, and on a
hand-written set. That needs about 99.999% per-step accuracy. **Read
`docs/DESIGN.md` (the user's design doc) and `PLAN.md` (decisions, data
estimate, next steps) before doing anything.**

## Current State

**Working (all on the Mac, committed and pushed to `main`):**
- Reference interpreter for phases A–C (`src/bcvm/refvm.py`). Every generated
  script is checked against real CPython at every instruction: executed byte
  offset, all user names, stdout and exception type. That covers 7.2M
  scripts with 0 mismatches.
- Support check / refusals (`support.py`), tokenizer and state parser
  (`tokens.py`), output grammar for constrained decoding (`decoding.py`),
  validator and runner loop (`harness.py`). The runner is proven end to end
  with `OracleStepper` (the reference VM behind the token interface).
- `uv run pytest`: 106 passed (~4 s).
- Data on the Mac at `~/work/pythonlm-data` (22 GB). The vocab hash in every
  shard is `a25d7f2a919c12f3` (354 tokens).
  - `phaseA/train`: 1.02B tokens, 17.2M steps, 32 shards
  - `phaseB/train`: 3.01B tokens, 47.3M steps, 64 shards
  - `phaseC/train`: 3.01B tokens, 31.4M steps, 64 shards
  - `phase{A,B,C}/eval_{test,natural,bignum}` and `phase{B,C}/eval_long`.
    These keep all steps, unweighted, plus records with source and CPython
    stdout.

**Not built yet (this is your job):**
- Windows/5090 environment setup, the trainer, the model stepper (KV-cached),
  and the phase A gate run.
- `eval/handwritten/phase*/` is empty. **The user writes these. Never generate them.**
- Phases D–F: designed in `PLAN.md`; their vocab tokens are already reserved.

Nothing is currently broken.

## Files in Play

| File | Why It Matters |
|------|---------------|
| `docs/DESIGN.md` | The user's design doc, verbatim. Source of truth for goals and targets |
| `PLAN.md` | Every decision made, token format, data estimate, D–F design, commands |
| `src/bcvm/shards.py` | Shard format + reference readers (`Shard.example`, `Shard.groups`). The trainer reads this |
| `src/bcvm/tokens.py` | Vocab (354), encoders, `parse_state`, `parse_step_output`. Don't reorder `VOCAB` |
| `src/bcvm/decoding.py` | `OutputGrammar(n_instrs, n_names)`: `.allowed()` → set of token ids, `.feed(tok)`, `.done` |
| `src/bcvm/harness.py` | `run(src, phase, stepper, max_steps, candidates, stream)` and `validate()`. The model stepper plugs in here |
| `src/bcvm/refvm.py` | Reference interpreter; `step(prog, state)` → `(state, printed)` |
| `src/bcvm/program.py` | `Program(src)`: `.instrs` (listing), `.names`; EXTENDED_ARG folding |
| `src/bcvm/support.py` | `check(prog, phase)` raises `Refusal` |
| `src/bcvm/pipeline.py` | Generation, step sampling weights, splits, records |
| `src/bcvm/evalsets.py` | Eval-set definitions |
| `src/bcvm/config.py` | Python pin 3.14, limits (context 2048, listing ≤1408 tokens, int bound 999), `BCVM_DATA` |
| `scripts/sync_to_trainer.sh`, `scripts/build_evalsets.sh` | Data transfer / eval build |
| `natural/` | 1,020 LLM-written training scripts + `SPEC.md`. Training data, not eval |
| `tests/` | 106 tests; run them on the new box first |

## What Has Been Tried (and Why It Failed)

### Pinning Python 3.15 (the user's day-to-day version)
- **What:** The design says to pin the daily driver, which is 3.15 on the Mac.
- **Why it failed:** torch 2.14.1 has no cp315 wheels, and the runner needs
  `compile()` and torch in one interpreter. **Pinned 3.14.** The data is only
  valid for 3.14 bytecode.

### Writing shards to the USB drive
- **What:** Generated to `/Volumes/New Volume` (exFAT, USB).
- **Why it failed:** It writes at ~36 MB/s, and the 32 workers stalled in I/O.
  Data now lives on the local SSD. The USB drive still holds a stale but
  identical copy of phase A only.

### Trusting `dis.stack_effect()` in the validator
- **Why it failed:** In 3.14, `FOR_ITER` on exhaustion jumps past `END_FOR`
  (it never runs), but `stack_effect` assumes it does. `harness.operand_effect`
  is our own table instead, and the listing's FOR_ITER argument is the
  landing index (END_FOR + 1).

### EXTENDED_ARG as a real model step
- **Why it failed:** It was 46 of 47M sampled steps, too rare to learn, and
  carries no semantics. It's now folded into the instruction it extends;
  `check.py` drops CPython's events for prefixes. The `EXTENDED_ARG` vocab token
  is kept unused, so the vocab hash is unchanged.

### Line-event-only differential check (as the design specified)
- Replaced by opcode tracing (`frame.f_trace_opcodes`), which is stricter.
  Gotcha: the opcode trace never reports the `RESUME` at offset 0, so
  `check.run_cpython` inserts it.

### Fixed bugs worth knowing about
- `LOAD_CONST None` was encoded with no argument token. Fixed before the
  final data, and a test covers it.
- The support check missed `for ch in s` and unknown names like `abs`. It now
  tracks per-name value kinds to a fixpoint and refuses names that are read
  but never assigned.

## Current Best Theory

**Use WSL2 (Ubuntu) on the Windows box, not native Windows.**
`torch.compile`, Triton and FlexAttention are Linux-first; native Windows only
has a community Triton port. rsync, memmap and uv all behave normally in WSL2,
and CUDA passes through with the standard Windows NVIDIA driver. Keep the data
on WSL's ext4 filesystem (`~/...`), never `/mnt/c` (9P is slow).

Train in **packed** mode. A group is one listing plus 16 steps from the same
run. Feed a whole group with a block mask: a step's tokens attend to the
group's listing plus earlier tokens of the same step, and listing tokens are
causal among themselves. Positions restart at `listing_len` for every step.
This is exactly inference with the listing's KV cache, and costs about 5×
less than expanded mode: phase A is 59 tokens per step packed vs 320 expanded.
Expanded mode (`Shard.example(i)`, plain causal SDPA) is the simple fallback
and a good first sanity run.

## Next Steps

1. **Set up WSL2 + env** (PowerShell: `wsl --install -d Ubuntu-24.04`, then inside WSL):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   git clone git@github.com:gmmeyer/pythonlm.git ~/work/pythonlm   # needs GitHub SSH key or `gh auth login`
   cd ~/work/pythonlm && uv python install 3.14 && uv sync --extra train
   uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_capability(), torch.cuda.get_arch_list())"
   ```
   Expect capability `(12, 0)` and `sm_120` in the arch list. If missing,
   install torch from `https://download.pytorch.org/whl/cu128` (or newer).
   Then run `uv run pytest`; expect 106 passed.
2. **Pull the data** from the Mac (192.168.1.47, user `greg`; Remote Login is on).
   Landing it at `~/work/pythonlm-data` matches the `BCVM_DATA` default:
   ```bash
   rsync -a --partial --exclude '._*' greg@192.168.1.47:work/pythonlm-data/ ~/work/pythonlm-data/
   uv run bcvm inspect ~/work/pythonlm-data/phaseA/train/A_0000 -n 2
   ```
3. **Write `src/bcvm/train/model.py`:** decoder-only, RoPE, vocab 354,
   context 2048. Phase A start: d_model 512, 8 layers, 8 heads (~25M).
   Accept explicit `position_ids` and a FlexAttention `BlockMask`.
4. **Write `src/bcvm/train/data.py`:** a packed loader over `Shard.groups()`.
   - Concatenate whole groups into fixed-length sequences (e.g. 16K tokens).
     If a group doesn't fit, split its steps across sequences and repeat the
     listing in each.
   - Per token, emit `group_id`, `seg` (0 for listing, k for step k),
     `position_id` and `loss_mask` (tokens at or after `loss_start`; columns
     are in `shards.IDX_COLS`).
   - `mask_mod`: `same group and kv <= q and (seg[kv] == 0 or seg[kv] == seg[q])`.
   - Shard weights per phase give the replay mix (phase B = 75% B + 25% A, …).
5. **Write `src/bcvm/train/train.py`:**
   - bf16 autocast, `torch.compile`, AdamW (β 0.9/0.95, wd 0.1, lr ~1e-3,
     cosine), grad clip 1.0, ~256K tokens/batch, checkpoints.
   - Log measured tokens/s and achieved TFLOPS, and replace the estimates in
     `PLAN.md`'s data table.
   - Eval periodically: teacher-forced step exact match on
     `phaseA/eval_test`, using argmax and requiring every output token right.
     Break it down by opcode: parse the input state's ip
     (`tokens.parse_state`), then read the opcode token after that address in
     the listing.
6. **Write the model stepper** (e.g. `src/bcvm/model_stepper.py`) implementing
   `propose(prog, listing_tokens, state_tokens, n)`.
   - Inputs: `listing_tokens` starts with `<bos> <code>`; `state_tokens` ends
     with `=>`. It must return `n` token-string lists, each ending `<eos>`.
   - Prefill the listing KV cache once per program. For each step, feed the
     state at positions starting from the listing length and decode under
     `decoding.OutputGrammar(len(prog.instrs), len(prog.names))` masks.
   - Candidate 1 is greedy; the rest are sampled. `harness.run` validates
     each candidate and counts rejections and rescues.
7. **Phase A gate:** run `harness.run` on every script in
   `phaseA/eval_test/*.records.jsonl.zst` (one JSON per line with `src`,
   `stdout`, `steps`; decompress with `compression.zstd`). Compare stdout,
   report the match rate, per-step error, safeguard rate, and refusal
   correctness. The bar is 99%. Then ask the user for their hand-written phase A set.
8. Then phase B (continue from the A checkpoint, 25% A replay), then C. Phases
   D–F need interpreter and generator work. Data generation is CPU-heavy and
   was designed for the Mac's 32 cores (`bcvm gen`, ~1 min per 1B tokens
   there), though it runs anywhere with Python 3.14.

## Key Constraints

- The user said **do not train on the Mac**; training happens on the 5090 box.
- **Never write the hand-written eval set.** It must come from the user, not
  an LLM (`natural/` was LLM-written and is training data).
- Python **3.14** only. Don't change `tokens.VOCAB` or its order; checkpoints
  carry across phases, and shards are checked against `VOCAB_HASH`. Any
  token-format change means regenerating all data.
- The token format is documented in `PLAN.md` and the `tokens.py` docstring:
  - ip is 3 address digits `@0`–`@9`, most significant first.
  - Ints are `i+`/`i-` then digits, least significant first.
  - Strings are `"`, then `c:<char>` tokens, then `"`.
  - `<out>…</out>` appears only on steps that print. Loss starts after `=>`.
  - The run halts when ip reaches the module's `RETURN_VALUE`, which the
    harness handles, so the model never predicts it.
- The validator must check only structure, never recompute values. It is a
  safeguard, not an executor.
- The user prefers concise responses. Commit and push to `gmmeyer/pythonlm`
  as work lands; that's how the Mac and the 5090 box share code.
- Data (22 GB) is never committed. It moves by rsync, and can be regenerated
  deterministically from seeds.
- Open decisions, with recommendations in `PLAN.md`: learn the final
  traceback line before phase D; keep builtins learned, not dispatched to
  real Python.

## Memory Pointers

claude-mem lives on the Mac. On the Windows box these IDs resolve only if
memory is synced; otherwise `PLAN.md` holds the same facts.

- Observations: #25875 (EXTENDED_ARG folding: why and how), #25793 (EXTENDED_ARG discovery), #25808 (eval-set builder), #25879 (measured data stats in PLAN.md), #25809 (test-suite scope)
- Searches worth re-running: `search("pythonlm EXTENDED_ARG folding")`, `search("pythonlm data pipeline throughput shards")`
