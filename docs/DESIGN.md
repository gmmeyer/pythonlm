# Learned Bytecode Interpreter

Oct 21, 2026 · @Greg Meyer

## Goal

Build a learned Python runtime: you hand it a script and it prints exactly what CPython would. CPython's own compiler turns the source into bytecode, which is exact and needs no learning. The model then executes that bytecode one instruction at a time, and a thin harness streams whatever the program prints.

Scripts that use anything outside the supported subset are refused before they run, so the runner never guesses at code it wasn't trained on. Arbitrary Python won't be reliable; the supported subset grows phase by phase.

Targets for calling a phase done:

- Stdout identical to CPython on 99% or more of held-out programs in the subset, up to 1,000 executed instructions
- The same bar on a hand-written eval set, not only generated programs
- Every script with unsupported features refused up front
- Per-step accuracy to match: 99% end to end at 1,000 steps needs about 99.999% per step, before runtime safeguards

[embedded content: how a run works · compile once, then a validated step loop]

Only steps that pass the validator change the state or reach stdout; a step that fails every resample stops the run with an error.

## Core design decisions

The model learns only execution: CPython does the compiling, and every predicted step is checked before it's applied. The step-model design keeps context fixed however long a script runs.

| Decision | Choice | Why |
| --- | --- | --- |
| Interface | Python source in; CPython's `compile()` produces the bytecode | Compiling is exact and solved; only execution needs learning |
| Step model vs. full trace | Step model: (current code object, state t) in, state t+1 out | Context never grows with run length |
| Printed output | Each step emits only the text it printed; the harness appends it to real stdout | Keeps stdout out of the state |
| Unsupported code | Refused before running, by scanning opcodes and names against the supported set | A clear refusal beats wrong output |
| Runtime safeguards | Grammar-constrained decoding, plus a stack-depth check against `dis.stack_effect()`; resample on failure | Catches malformed or impossible steps before they propagate |
| Python version | Pin one minor version, e.g. 3.12 | The opcode set changes between minor versions |
| Trace source | Own reference interpreter for the subset, differentially tested against CPython | CPython doesn't expose the value stack to Python code |
| Instruction pointer | Instruction index, not byte offset | Inline cache entries make byte offsets uneven |
| Names | User names become indices (L0, N0, …); builtins like `print` keep their names | Execution doesn't depend on user identifiers |
| Integers | Sign plus digit tokens, least significant first | Carries run in generation order; printing learns the reversal |
| Strings | One token per character | Stdout is judged character for character |
| Vocabulary | Custom, roughly 150–250 tokens (opcodes, digits, printable ASCII, structure), trained from scratch | Small vocab suits a small model |

Illustrative and simplified, the step that runs `print(x + 1)` with x = 3 (exact opcodes depend on the pinned version):

```
<code> … | 5 LOAD_CONST 1 | 6 BINARY_OP + | 7 CALL 1 | 8 POP_TOP | … </code>
<state> ip 7 | stack [ NULL print +4 ] | names N0=+3 </state>
=>
<state> ip 8 | stack [ None ] | names N0=+3 </state>
<out> 4\n </out>
```

## Language subset

Scripts are ordinary top-level Python, and each phase widens what the runner accepts. Every phase adds one new kind of state; a script that steps outside the current phase is refused.

| Phase | Adds | New state |
| --- | --- | --- |
| A: arithmetic and print | Int literals, variables, `+ - * // %`, unary minus, `print()` of ints and string literals | Value stack, module names, per-step output |
| B: control flow | Comparisons, `and`/`or`/`not`, if/elif/else, while, `for` over `range()`, break, continue | Range iterator objects |
| C: strings | Concatenation, f-strings with ints, `str()`, `len()`, indexing, `print()` with several arguments | String values |
| D: lists and tuples | Literals, indexing, `append`, `len`, `for` over a list, `sum`, `min`, `max` | Heap section; objects by reference id, so aliasing works |
| E: functions | `def`, calls, return, recursion | Frame stack; the model sees only the current code object's listing |
| F: dicts (stretch) | Literals, get and set, `in`, iteration | Dicts, iterated in insertion order |

Ints start small (e.g. under 1,000 in magnitude) and the bound widens while accuracy holds. The only builtins are the ones named above, learned as primitives.

Out of scope: floats (shortest round-trip printing is hard to learn exactly), sets (string hash order varies per process), classes, exceptions, imports, closures, generators, `input()` and files.

## Trace generation

Traces come from a small reference interpreter that is checked against real CPython on every script. Labels are free and unlimited, so the generator's correctness and the realism of its scripts are what to protect.

1. **Generate** from three sources, all filtered the same way:
   - Grammar-based random scripts over the current phase's subset
   - Templated classics: gcd, Fibonacci, FizzBuzz, Collatz, digit sums, trial-division primes, bubble sort from phase D
   - Natural scripts written by an LLM in the style people actually write, constrained to the subset
   - CPython constant-folds expressions like `3 + 4` at compile time, so random arithmetic must go through variables to produce `BINARY_OP`.
   - Enforce an instruction budget (e.g. 2,000) and the int bound at run time; discard scripts that exceed either. Deduplicate by a hash of the bytecode.
2. **Compile** with `compile(src, "<script>", "exec")` and list it with `dis.get_instructions()`. The same support check the runner uses rejects anything outside the phase.
3. **Execute** in the reference interpreter, which implements only the subset's opcodes and snapshots the full state plus any printed text after every instruction. An unsupported opcode raises.
4. **Check** by running each script in CPython with stdout captured. Stdout must match exactly, and names must match at every line event via `sys.settrace`. A mismatch is an interpreter bug, so it fails the run rather than being dropped.
5. **Write** one record per script: source, instruction listings, state sequence, output. Splits are assigned per script, never per step.

## Data pipeline on the Mac Studio

The Mac Studio generates and tokenizes; the 5090 only trains. Generation is CPU-bound Python, so it scales across the Mac's cores.

- **Workers:** a `multiprocessing` pool, one worker per core, each running generate → compile → execute → check → write. Measure scripts per second in week one before sizing datasets.
- **Examples:** one example is the current code object's listing plus state t, mapped to state t+1 plus any printed text. Loss applies only to the output side.
- **Step sampling:** long loops produce thousands of near-identical steps. Sample steps per script and upweight rare transitions: loop exits, `break`, steps that print, function returns.
- **Storage:** uint16 token arrays in roughly 100M-token `.bin` shards (nanoGPT-style memmap), plus an index of example offsets and where the loss starts.
- **Volume:** at about 250 tokens per example, 1B tokens is about 4M examples. Plan a few billion tokens per phase, replaying earlier phases in each new mix so they aren't forgotten.
- **Transfer:** rsync shards to the 5090 machine. Generation for the next phase runs while the current one trains.

## Model, training and the runner on the 5090

A decoder-only transformer trained from scratch, starting near 25M parameters for phase A and growing to 50–100M as phases add state. Each phase continues from the previous checkpoint.

- **Architecture:** decoder-only with RoPE, 2,048-token context, enough for a listing of a few hundred instructions plus the state.
- **Training:** PyTorch in bf16 with `torch.compile` and SDPA attention, AdamW with cosine decay, loss masked to output tokens.
- **Throughput:** back of the envelope (6 × parameters FLOPs per token, about 70 TFLOPS achieved), a 50M model trains at roughly 1–2 hours per billion tokens. Replace this with a measured number in week one.
- **Runner, `run script.py`:** compile, support check, then greedy decoding step by step, streaming printed text as it appears.
- **Prefix caching:** a code object's listing is identical on every step of a run, so its KV cache is computed once and each step only processes the state.
- **Safeguards:** a token mask from a small state grammar keeps every output well formed, and the predicted stack depth is checked against `dis.stack_effect()`. On a failed check, resample a few candidates; if all fail, stop with an error instead of printing anything wrong.
- **Speed:** expect orders of magnitude slower than CPython, since each instruction costs dozens of decoded tokens. The delta-output experiment is the main lever.

## Evaluation

The metric that matters is exact stdout match against CPython on scripts the model never saw. Everything else explains why a run failed.

| Eval | What it measures | Set |
| --- | --- | --- |
| Stdout match | Full runner output vs. CPython, character for character | Held-out generated scripts, per phase |
| Hand-written set | Same, on code a person wrote | About 200 scripts per phase written by you, not by the generator or the training LLM |
| Length curve | Stdout match by instructions executed (100, 1k, 10k), against per-step accuracy raised to the step count | Held-out scripts, bucketed |
| Number size | Stdout match on ints larger than the training bound | Held-out scripts with widened constants |
| Per-step and per-opcode | Teacher-forced exact match on single steps, broken down by opcode | Held-out steps |
| Refusals | Unsupported scripts refused; supported ones never refused | Mixed set, labeled by the support check |
| Safeguard rate | How often the validator fires, and how often resampling rescues the run | Every eval run |
| Baseline, run once | A same-size model mapping source straight to stdout | Phase B held-out set |

## Milestones

The harness comes first and has its own gate; after that, each phase widens the runner only once its scripts pass.

[embedded content: roadmap · harness plus six phases, a gate after each]

Each phase reuses the harness and the previous checkpoint, so later phases mostly cost data generation and training time.

## Risks and open decisions

The biggest risk is the per-step bar: 99.999% exact is demanding, and every phase lives or dies on it.

- **Per-step ceiling:** if accuracy plateaus short of the bar, cap supported script length, lean on resampling, and grow the model before widening the subset.
- **Multi-digit arithmetic:** a whole multiplication happens inside one `BINARY_OP` step, the classic transformer failure. Keep int bounds tight and widen slowly.
- **Generated vs. real code:** random scripts don't look like what people write. The LLM-written training scripts and the hand-written eval set exist to catch this.
- **Interpreter drift:** a reference interpreter that disagrees with CPython poisons every label. Differential checks on every script guard it.
- **Listing size:** a code object too long for the context window can't run. Refuse it for now; windowing the listing is a later option.
- **Version churn:** moving to a new Python version means regenerating data and retraining.

To decide:

- [ ] Which Python version to pin: whichever you'd run scripts with day to day
- [ ] Builtins: learn each one (current plan) or dispatch some to real Python, which would make `sorted()` and friends work immediately but means the model isn't executing everything
- [ ] Uncaught exceptions: refuse, or learn to print the traceback. Worth settling before phase D, where index errors appear
