# Implementation plan

Companion to [docs/DESIGN.md](docs/DESIGN.md) (the design doc, verbatim). This
file records what is built, the decisions made while building it, the data
volume estimate, and what comes next.

## Status

| Piece | State |
| --- | --- |
| Reference interpreter, phases A–C | Done. Checked against CPython on every generated script, instruction by instruction |
| Support check (refusals) | Done. Opcodes, names, constants, plus abstract interpretation of the stack (callee and arity for every call, value kinds per name) |
| Tokenizer, state parser, output grammar (constrained-decoding mask) | Done |
| Validator + runner loop with resampling | Done, exercised end to end with an oracle stepper (the reference VM behind the token interface) |
| Script sources: grammar, templates, natural | Done for A–C. 1,020 natural scripts written by Claude subagents (`natural/`) |
| Data pipeline (multiprocess, sharded, resumable) | Done |
| Phase A data (format 2) | 6.14B tokens, 102M steps, 6.39M scripts, 14 GB (light records) |
| Phase B data (format 2) | 3.01B tokens, 46.7M steps, 2.93M scripts, 6.8 GB |
| Phase C data (format 2) | 3.01B tokens, 31.2M steps, 1.95M scripts, 6.5 GB |
| Eval sets (test / natural / long / bignum) | Built for A–C, see below |
| Hand-written eval set | **Yours to write**, see `eval/handwritten/README.md` |
| Trainer (packed, FlexAttention) | Done: `bcvm train`, `bcvm evalsteps`. Measured 632K tok/s at 26M params |
| Model stepper, KV-cached batched runner | Done: `bcvm gate`, `bcvm run --ckpt` |
| Phases D–F | Designed below; vocabulary already reserves their tokens |

`uv run pytest` runs 106 tests (≈4 s).

## Decisions made while building

**Python 3.14.** The design says to pin the version you use day to day. That's
3.15 here, but torch 2.14.1 ships no cp315 wheels, and the runner needs
`compile()` and torch in the same interpreter. 3.14.8 is installed on this Mac;
install 3.14 on the 5090 machine too (`uv python install 3.14`). Changing it
later means regenerating data, which takes minutes.

**What "one step" looks like in tokens.** Everything the model sees, for
`x = 3; for i in range(2): print(x + i)`, at the `BINARY_OP` step:

```
<bos> <code> @0 @0 @0 RESUME @0 @0 @1 LOAD_SMALL_INT i+ 3 @0 @0 @2 STORE_NAME N0 @0 @0 @3 LOAD_NAME range
  @0 @0 @4 PUSH_NULL @0 @0 @5 LOAD_SMALL_INT i+ 2 @0 @0 @6 CALL 1 @0 @0 @7 GET_ITER @0 @0 @8 FOR_ITER @0 @1 @9
  @0 @0 @9 STORE_NAME N1 @0 @1 @0 LOAD_NAME print ... @0 @1 @4 BINARY_OP op:+ ... </code>
<state> ip @0 @1 @4 stack RANGE_IT i+ 1 i+ 2 i+ 1 print NULL i+ 3 i+ 0 names N0 i+ 3 N1 i+ 0 </state> =>
<state> ip @0 @1 @5 stack RANGE_IT i+ 1 i+ 2 i+ 1 print NULL i+ 3 names N0 i+ 3 N1 i+ 0 </state> <eos>
```

- Instruction indices are three *address digits* `@0`–`@9`, most significant
  first. They're never computed, only matched and copied (the next ip is the
  next listing entry or a jump target in the listing), so a separate digit set
  keeps them from being confused with values and removes the need for
  separators. Max 999 instructions per code object.
- Ints: sign token then digits least significant first (`120` → `i+ 0 2 1`),
  canonical (no leading zeros, no `-0`). Bools are `True`/`False`, distinct
  from ints.
- Strings: `"` + one `c:<char>` token per character + `"`. 95 printable ASCII
  plus `\n` and `\t`. Max 48 characters in the state.
- `FOR_ITER`'s listing argument is where execution lands on exhaustion (the
  instruction after `END_FOR`), because 3.14 skips `END_FOR`. Range iterators
  are `RANGE_IT next stop step`.
- `EXTENDED_ARG` prefixes are folded into the instruction they extend, like
  inline caches. They only widen the next argument, which `dis` already
  merges, and as real steps they were ~0.001% of the data, too rare to learn.
  The differential check drops CPython's events for them.
- `<out> ... </out>` appears only on steps that print. Loss starts after `=>`.
- **Work section (format 2).** A `BINARY_OP` step with `//` or `%` on ints
  starts its output with scratch the harness ignores: the quotient most
  significant digit first, and for `%` also the product divisor × quotient
  (least significant first), so the remainder is a plain subtraction.
  `754 // 13` → `=> <work> i+ 5 8 </work> <state> … i+ 8 5 names …`;
  `754 % 13` → `=> <work> i+ 5 8 op:* i+ 4 5 7 </work> <state> … i+ 0 names …`.
  Least-significant-first output suits `+ - *` but makes the quotient's
  units digit, the last thing long division determines, the first token;
  see the runs below. The output grammar requires the section on exactly
  these steps (`tokens.work_kind`).
- The run ends when ip reaches the module's `RETURN_VALUE`; the harness stops
  there, so the model never predicts it.
- User names become `N0..N31` in order of first appearance. A builtin name
  the script assigns (`sum = 0`) is a user name; one it never assigns stays
  a builtin token. A name that is read but never assigned is refused.
- Vocabulary: 354 tokens. Larger than the design's 150–250 because of 48
  single-token names (`N0..N31`, `L0..L15`) and tokens reserved for phases D–F
  (opcodes, `&0..&31` heap refs, `LIST`, `DICT`, …), so it never changes and
  checkpoints carry over between phases. Hash `308cf26ca50588a7` (format 2;
  format 1 was `a25d7f2a919c12f3`, before `<r0>`/`<r1>` became
  `<work>`/`</work>`) is in every shard's metadata and checked on load.

**A stronger check than the design asked for.** Instead of names at line
events, CPython runs with opcode tracing (`f_trace_opcodes`) and we compare,
at *every* instruction, the executed byte offset and every user name's
value, plus stdout and the exception type. The stack isn't visible from
Python but determines all of those, so stack bugs surface within a few steps.
A mismatch aborts generation and writes the script to `MISMATCH/`. So far:
zero mismatches. The final A–C datasets alone checked 7.2M scripts.

**Validator.** `dis.stack_effect()` turned out wrong for 3.14's `FOR_ITER` on
exhaustion (it assumes `END_FOR` runs). The validator uses its own effect
table and, beyond depth, checks only things that follow from the listing:
the next ip is a legal successor; the stack below the instruction's operands
is copied unchanged; every name except a `STORE_NAME` target is unchanged and
the stored value is the popped one; `COPY`/`SWAP` really copy/swap; only a
`print()` call produces output. It never recomputes values. The output
grammar (`decoding.py`) also bounds ip to the listing, keeps names in order and
ints canonical.

**Shards are groups, not single examples.** A group is one listing followed
by K=16 sampled steps of the same run. Train it either way:

- *expanded*: listing + one step per example, plain causal attention;
- *packed* (recommended): one forward pass per group with a block mask (each
  step attends to the listing and itself; positions restart after the
  listing). This is exactly inference with the listing's KV cache, and costs
  about a fifth of the compute (59 vs 320 tokens per step in phase A).

Format details are in `src/bcvm/shards.py`'s docstring; `Shard.example(i)`
and `Shard.groups()` are reference readers.

**Step sampling.** Weighted sample of 16 steps per script without
replacement: loop exits ×6, printing steps ×4, taken jumps ×2, no-ops
(`RESUME`, `NOT_TAKEN`, `NOP`, `EXTENDED_ARG`) ×0.3. Eval sets keep *all*
steps, unweighted, so per-step accuracy is measured on the real distribution.

**Splits.** Per script, by hash of its token listing: 0.5% test, 0.5% val,
the rest train; held-out hashes are skipped during training generation.
Natural scripts split by *base* script: 10% of the hand-curated bases (and
all their perturbed variants) never reach training, so the natural eval set
is structurally unseen.

**Natural scripts** were written by Claude subagents to `natural/SPEC.md`, then
filtered by the same support check and differential check as everything
else. The pipeline uses them as-is (15%) and with perturbed int/string
literals (85%). The design's hand-written set must come from you, not from
these.

## Data volume estimate

### What we measured on this Mac Studio (M3 Ultra, 32 cores)

| | Phase A | Phase B | Phase C |
| --- | --- | --- | --- |
| Throughput, 1 core (incl. CPython check) | ~1.0M tok/s | ~0.65M tok/s | ~0.8M tok/s |
| 1B tokens on 32 cores | 47 s | ~1.5 min | ~1.3 min |
| Scripts kept / generated | 92% | 82% | 82% |
| Listing, mean tokens | 278 | 288 | 365 |
| Step (state in + out), mean tokens | 42 | 44 | 68 |
| Tokens per step, packed | 59 | 62 | 91 |
| Tokens per step, expanded | 320 | 332 | 433 |
| Executed steps per script, mean | 53 | ~120 | ~145 |

Generation is effectively free. The budget is training compute on the 5090,
so size the data by what training can consume, then generate more on demand.

### How much training data

The bar is ~1e-5 error per step. A step mostly copies state, but the errors
that matter are rare situations: a 3-digit carry inside `BINARY_OP`, a loop
exit at depth 4, `//` with negative operands, the 30th variable. If such a
case is 1 in 1,000 steps, it needs thousands of examples before an exact
skill is reliable, which puts each phase in the tens of millions of steps.
The design's "a few billion tokens per phase" agrees.

| Phase | New data (packed tokens) | Steps | Replay in the mix | Model | 5090 time per pass* |
| --- | --- | --- | --- | --- | --- |
| A | 1B (generated) | 17.2M | none | ~25M | 27 min (measured) |
| B | 3B (generated) | 47.3M | 25% from A | 25–50M | ~1.3–2.5 h |
| C | 3B (generated) | 31.4M | 25% from A+B | ~50M | ~2.5 h |
| D lists | ~4B | ~40M | 25% | 50–100M | ~3.5–7 h |
| E functions | ~6B | ~50M | 25% | ~100M | ~10 h |
| F dicts | ~3B | ~25M | 25% | ~100M | ~5 h |
| **Total** | **~20B tokens** | **~210M steps** | | | |

\*Measured on the 5090 (WSL2, torch 2.14.1, bf16, compiled FlexAttention):
the 26.1M model trains at 632K packed tokens/s, ~97 TFLOPS counting 6N only
(attention excluded), with 12.5 GB peak memory at 64K tokens per micro-batch.
Other rows scale that rate by model size; bigger models should use the GPU
somewhat better. Expanded mode would cost ~5× more.

Replay re-reads earlier phases' shards, so it needs no extra generation.
Prefer fresh data to repeated epochs: if the held-out per-step error is
still falling at the end of a pass, generate another 1–3B tokens (minutes).
To resolve 1e-5 you need about 300K held-out steps with zero errors (rule of
three); the `test` sets have 0.47M (A), 2.5M (B) and 2.1M (C).

### Eval sets (built)

All scripts come from held-out splits; every step is kept, unweighted.
Records hold source and CPython's stdout for end-to-end runs.

| Set | What | A | B | C |
| --- | --- | --- | --- | --- |
| `eval_test` | generated, standard mix | 10K scripts / 0.47M steps | 10K / 2.5M | 10K / 2.1M |
| `eval_natural` | variants of held-out natural bases | 3K / 0.13M | 3K / 0.90M | 3K / 0.68M |
| `eval_long` | 1,000–10,000 executed steps | — (A has no loops) | 1K / 1.7M | 1K / 1.8M |
| `eval_bignum` | ints up to 99,999 | 3K / 0.14M | 3K / 0.76M | 3K / 0.63M |

Phase A's natural set comes from only ~14 held-out base scripts, so read it
as a smoke test; your hand-written set is the real check.

### Disk

| | Per 1B tokens | A–C now (7B) | All phases (~20B) |
| --- | --- | --- | --- |
| Token shards (`.bin`, uint16) | 2.0 GB | 14 GB | 40 GB |
| Step index (`.idx.npy`) | 0.2–0.35 GB | 2 GB | 5 GB |
| Records (source + full state traces, zstd) | 0.5–0.9 GB | 4 GB | 15 GB |
| **Total** | | **20.1 GB (measured)** | **~60 GB** |

## Storage and transfer

- **Code** → git: private repo `github.com/gmmeyer/pythonlm`
  (`git clone git@github.com:gmmeyer/pythonlm.git`). Remote Login is also on
  here, so `git clone greg@192.168.1.47:work/pythonlm` works on the LAN.
- **Data** → `~/work/pythonlm-data` on this Mac's SSD (override with
  `BCVM_DATA`). Copy it over the LAN, either pulled from the 5090 machine:
  `rsync -a --partial --exclude '._*' greg@192.168.1.47:work/pythonlm-data/ /data/pythonlm-data/`,
  or pushed from here: `scripts/sync_to_trainer.sh user@trainer:/data/pythonlm-data`.
  Re-runs only send new shards. Train from the 5090's local NVMe, not a
  network mount: memmap random reads over SMB/NFS are slow and flaky.
- **Not git or Git LFS** for data: 21–60 GB of binary shards, regenerable
  from seeds in minutes.
- **The USB drive** (exFAT, readable on Linux and Windows) is fine as a backup
  or if the trainer has no SSH, but it writes at only ~36 MB/s. An identical
  copy of phase A is in `/Volumes/New Volume/pythonlm-data`.

Layout:

```
pythonlm-data/
  phaseA/train/   A_0000.{bin,idx.npy,json,records.jsonl.zst} ... manifest.json
  phaseA/eval_test/  eval_natural/  eval_long/  eval_bignum/
  phaseB/...
```

## The 5090 box

- WSL2 Ubuntu 24.04 (native Windows lacks a first-class Triton for
  `torch.compile` and FlexAttention). Python 3.14.8, torch 2.14.1+cu130,
  `sm_120`. The venv lives on WSL's ext4 (`UV_PROJECT_ENVIRONMENT=~/.venvs/pythonlm`)
  while the source can stay on the Windows side; `~/.local/bin/pylm <cmd>`
  sets that up plus `BCVM_DATA` and runs `uv run --extra train <cmd>`.
- Data at `E:\work\pythonlm-data` = `/mnt/e/work/pythonlm-data`. WSL reads
  whole shards through 9P at ~200 MB/s but random memmap reads cost ~0.2 ms
  each, so the loader reads whole shards into RAM. No need to copy to ext4.
- Runs go to `$BCVM_DATA/runs/<name>/` (`log.jsonl`, `stdout.txt`,
  `latest.pt`, `final.pt`, eval and gate JSON). A checkpoint with optimizer
  state is ~310 MB at 26M params.
- Generation works here too: 2B phase A tokens in 159 s on 24 workers.

## Training runs

| Run | Model | Data | Step err, teacher-forced (`eval_test`) | Gate: stdout match (`eval_test`, 10,016 scripts) |
| --- | --- | --- | --- | --- |
| a1 | 26.1M: 8 layers × 512, 8 heads | A, 1.0B tokens, one pass, lr 1e-3 cosine, 27 min | 4.8e-3 (natural 5.4e-3, bignum 1.2e-2) | 85.1%; free-running step err 4.4e-3; 0 refusals; validator fired 6× |
| a2-16L | 51.8M: 16 layers × 512 | same recipe, 1.0B tokens, 52 min (317K tok/s) | 4.4e-3: only 9% better, same `//` and `%` errors | not run |
| a3 | as a1 | format 2 (work section, `//`/`%` weighted 4×), A, 3.0B tokens, 80 min | **2.9e-4** (natural 2.6e-4, bignum 8.1e-3); `//` 0.8%, `%` 0.5% wrong, all else ~5 errors | **98.97%** (9,913); free-running 2.8e-4; 0 refusals; validator never fired |
| a4 | a3 continued | A 70% + `train_arith` 30%, 3.0B tokens, lr 5e-4, 80 min | **7.1e-5** (natural 6.4e-5, bignum 8.0e-3); 33 wrong steps in 466K, 30 of them `//`/`%` | **99.81% (9,997): phase A gate passed** on generated scripts; free-running 6.9e-5; 0 refusals; validator never fired |
| b1 | a4 continued | B 60% + B arith 15% + A 15% + A arith 10%, 3.0B tokens, lr 8e-4, 80 min | B: **1.4e-4** (natural 1.3e-4, long 1.2e-4, bignum 1.3e-2); 341 wrong in 2.5M: `CALL`/print 147, `%` 128, `//` 38, `LOAD_CONST` 20. Phase A after B: 1.3e-4 (a4: 7.1e-5) | B, first 4,000 scripts: **97.5%**; free-running 8.0e-5 (`%` 39, `LOAD_CONST` 23, `//` 14); 0 refusals; validator stopped 3 runs, rescued 1. Scripts of 1,000–10,000 steps: 156/156 |
| b2 | b1 continued | same mix, 3.0B tokens, lr 5e-4, 80 min | B: **1.1e-4** (natural 1.2e-4, long 9.6e-5); 278 wrong: `LOAD_CONST` 141 (the `100101` script), `%` 100, `//` 25, rest ~12. Phase A after B: 6.4e-5 | B, first 4,000: **97.7%**; free-running 1.1e-4; 64 of 91 failures are the `100101` script family, without it ~99.3% |
| b3 | b2 continued | B 45% (6.0B available) + B arith 30% + A 15% + A arith 10%, 3.0B tokens, lr 3e-4, 80 min | B: **2.2e-5**; 56 wrong in 2.5M: `%` 35, `//` 16, `STORE_NAME` 4; the `100101` copy errors are gone (0 `LOAD_CONST`) without the copy drill | full gate running |

a1 and a2 used format 1 data, now in `$BCVM_DATA/v1/`. b1's `LOAD_CONST` and
`CALL` errors (167 of 341) all come from one held-out natural script that prints
the constant `"read bottom to top: 100101"` in a loop: copying the string, the
model writes `1 0 0 1` and closes the quote, losing its place in the repeated
digit pattern (`scripts/step_errors.py`). It is held-out natural base
`b5_018`, and 76 of the first 5,008 `eval_test` scripts are its variants
(the perturbation changes `n`, not the string), so one hard base is ~1.5% of
the gate. A copying weakness, not arithmetic, and it will matter more in
phase C: the `copy` source (below) targets it. a3's remaining errors
are in the work section's quotient digits, concentrated on divisors 11 and
13 (13–26% wrong; every divisor ≤ 10 is ~0%), which the `arith` source covers.

What a1 says:

- Everything except `BINARY_OP` is nearly there: 5 wrong steps in ~400K.
- `BINARY_OP` is 3.5% wrong, almost all `//` and `%`, and those errors sit
  in 3-digit dividends with 1–2-digit divisors (17–26% wrong); 2×2-digit
  `*` is 8%; `+`/`-` ≤0.4%. Negative operands are worse but rare. This is
  long division inside one step, with the quotient emitted least
  significant digit first, so it has to be finished before the first
  output token. `scripts/binop_detail.py` shows 760 of 761 `//` errors are
  at the result's first (units) digit, with the tens digit right given it;
  error by divisor goes from ~0% (1, 2, 4, 5, 10, 25, 100) to 45–55% (6–9)
  and 75–80% (11, 13). Doubling depth (a2-16L) at equal data barely helped.
  `scripts/binop_errors.py` gives the breakdown by operand size.
- `scripts/arith_probe.py` trains the same model on `a op b` alone, in the
  real int encoding, to compare output formats (error = result not exactly
  right; a1 saw ~0.3–0.5M examples per operator):

  | Format (output side) | `//` at 3M examples/op | `%` at 3M | `%` at 10M |
  | --- | --- | --- | --- |
  | `lsb`: result LSB-first (format 1) | 5.8e-3 | 2.2e-2 | 2.1e-3 |
  | `msb`: result MSB-first | 2.0e-3 | 1.3e-1 | |
  | `work`: quotient MSB-first, then result | 5.8e-4 | 3.2e-3 | |
  | `work2`: as work, `%` also writes b × q (format 2) | 6.4e-4 | 1.3e-3 | |

  Data helps every format; the work section gives ~10× at equal data, and
  writing b × q another 2.5× on `%`. `*` and `+` reach ~0 with a few
  million examples in any format.
- Free-running error matches teacher-forced error, so errors don't compound
  beyond the per-step rate. The validator almost never fires because these
  are wrong values in a well-formed state, which it is designed not to check.
- `eval_bignum` (ints to 99,999) also degrades copying and printing, the
  expected length-generalization gap.
- Gate throughput: ~1,000 steps/s at 256 slots, GPU ~55% busy
  (Python-bound); the whole phase A test set takes 8 minutes.
- Format 2 data, regenerated on the 5090 box (`--records light` for train):
  phase A 6.14B tokens (192 shards, 102M steps; division 9.1% of sampled
  steps vs 4.0% before), B and C 3.0B each, all eval sets with the same
  scripts as before. Plus `phaseA/train_arith`: 3.07B tokens from the
  `arith` source (the grammar with `*`, `//`, `%` dominant and divisors
  spread over 1–99; division 17% of sampled steps), to mix in with
  `--data A=0.7,A/train_arith=0.3`; likewise `phaseB/train_arith` and
  `phaseC/train_arith`, 2.02B tokens each. Phase B train now has 6.02B
  tokens (shards 64–127 added). `phaseB/train_copy`: 1.03B tokens from the
  `copy` source, the grammar with most string literals repetitive patterns
  over small alphabets (`100101`, `abaab`, `ACGT…`), for b4.

## Next steps

1. **Phase A: your hand-written set.** a4 passes the generated-script gate
   (99.81%); the design also requires 99% on ~200 scripts you write
   (`eval/handwritten/phaseA/`), run with `bcvm run --ckpt`/a gate over them.
2. **Phase B** (b1, from a4 with 25% A replay), then C. Phase B scripts
   average ~250 steps vs 47 in A, so 99% stdout match needs ~4e-5 per step.
3. **Baseline** (once, phase B): same-size model from source straight to
   stdout.
4. **Phases D–F**, below.

## Phases D–F design

The vocabulary already has their tokens; each needs interpreter, support
check, grammar and generator work, following the A–C pattern.

- **D: lists and tuples.** Tuples are inline values `( v v )`. Lists live in
  a heap section after `names`: `heap &0 LIST [ v v ] &1 LIST [ ... ]`, with
  stack and names holding `&k`, so aliasing works. Refs are numbered by
  allocation and unreachable lists are dropped. New: `BUILD_LIST/TUPLE`,
  `LIST_EXTEND`, `LOAD_ATTR` (method `append`), `STORE_SUBSCR`,
  `UNPACK_SEQUENCE`, subscript on lists and tuples, `LIST_IT &k idx`, builtins
  `sum min max len`. The differential check compares list contents and identity.
- **E: functions.** State gains `frames`: caller frames are `(code ip stack
  locals)`, and the current frame's locals are `L0..L15`. The harness switches
  the listing (and its KV cache) when the predicted frame changes code
  object. New: `MAKE_FUNCTION`, `SET_FUNCTION_ATTRIBUTE` (defaults),
  `LOAD_FAST*`/`STORE_FAST*` (incl. superinstructions), `LOAD_GLOBAL`,
  `RETURN_VALUE` in functions. Recursion depth capped (~16) to bound the state.
- **F: dicts.** `&k DICT [ k v k v ]` in insertion order, `BUILD_MAP`,
  `STORE_SUBSCR`, `CONTAINS_OP`, `DICT_IT`, methods `get items keys values`.

## Open decisions (from the design), with a recommendation

- **Python version:** 3.14, for the torch reason above. Revisit when torch
  ships 3.15 wheels.
- **Builtins:** keep learning them. Dispatching `sorted()` and friends to real
  Python is easy to add later as an explicit, logged escape hatch, but
  it should not be the default.
- **Uncaught exceptions:** for now, generation discards scripts that raise,
  and the runner has no exception state. Recommend learning to emit the
  final traceback line (`ZeroDivisionError: integer division or modulo by
  zero`) before phase D, since `IndexError` is common there. The
  interpreter already detects and classifies these, and the check already
  compares exception types.

## Commands

```bash
uv sync                                            # Python 3.14 env
uv run pytest                                      # tests
uv run bcvm check my_script.py -v 20               # support + reference run + CPython diff
uv run bcvm run my_script.py                       # full harness with the oracle stepper
uv run bcvm show my_script.py --steps 5            # listing and steps as tokens
uv run bcvm gen --phase B --tokens 3e9 --shard-tokens 4.7e7   # resumable
uv run bcvm evalset --phase B --name test --scripts 10000
uv run bcvm inspect ~/work/pythonlm-data/phaseB/train/B_0000 -n 3
uv run bcvm bench --phase C                        # single-core throughput
uv run --extra train bcvm train --name a1 --data A=1 --tokens 1e9            # packed training
uv run --extra train bcvm train --name b1 --data B=0.75,A=0.25 --tokens 3e9 --init $BCVM_DATA/runs/a1/final.pt
uv run --extra train bcvm evalsteps $BCVM_DATA/runs/a1/final.pt phaseA/eval_test   # teacher-forced, by opcode
uv run --extra train bcvm gate $BCVM_DATA/runs/a1/final.pt phaseA/eval_test        # end-to-end stdout match
uv run --extra train bcvm run my_script.py --ckpt $BCVM_DATA/runs/a1/final.pt
scripts/sync_to_trainer.sh user@trainer:/data/pythonlm-data phaseA phaseB
```
