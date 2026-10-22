# Natural-script spec (for LLM-written training scripts)

These scripts are training data for a model that learns to execute CPython 3.14
bytecode. They must look like code a person would actually write, while staying
strictly inside one phase's subset. Every script is filtered by the support
check and the reference interpreter, so out-of-subset scripts are wasted, not
harmful.

## Files

- One script per file: `natural/phase<X>/<prefix>_<NNN>.py` (e.g. `natural/phaseB/b1_017.py`).
- Plain top-level code. No `if __name__ == "__main__":`, no functions, no imports,
  no comments-only files. Short comments are fine and encouraged where natural.
- 3–30 lines each; vary the length.
- Each script must run with `python3.14 <file>` without error and print something.

## Hard constraints (all phases)

- Every int value at every moment (literals, intermediates, loop counters,
  results) must stay within -999..999. Keep products small.
- No division or modulo by zero.
- Executes fewer than ~1,500 bytecode instructions: keep loops short
  (a few dozen iterations total, not hundreds).
- Deterministic: no `input()`, files, randomness, time.
- ASCII only in strings (printable characters, `\n` and `\t` are ok).
- Do not shadow builtins (`print`, `range`, `len`, `str`, `sum`, `min`, `max`).
  Names like `total`, `count`, `result` are fine.

## Phase A: arithmetic and print

Allowed: int literals, variables, `+ - * // %`, unary minus, parentheses,
augmented assignment (`+=` etc.), chained assignment `a = b = 0`, swaps like
`a, b = b, a`, and `print()` with zero or one argument, where the argument is an
int expression or a string literal.

Not allowed: `print` with 2+ arguments, f-strings, string variables or string
operations, comparisons, `if`, loops, `/`, `**`, bools, floats, any other
builtin.

Typical shapes: unit conversions with integer math, splitting minutes into
hours/minutes, change-making with `//` and `%`, simple accounting, running
totals, digit extraction, area/perimeter, a label line `print("Total:")` then
the value on the next line.

## Phase B: control flow (adds to A)

Adds: comparisons (`< <= == != > >=`, chained like `0 < x < 10`), `and`, `or`,
`not`, `True`/`False`, `if/elif/else`, `while`, `for i in range(...)` with 1–3
arguments (including negative steps), `break`, `continue`, `pass`, and printing
a comparison or bool result. `print()` still takes zero or one argument.

Not allowed: anything from Phase C onward (multi-arg print, f-strings, string
variables, `len`, `str`), lists, functions.

Typical shapes: gcd, primes by trial division, Collatz, digit sums, counting
divisors, FizzBuzz (printing string literals), triangle/square numbers, simple
simulations (bank balance, population, countdown), searching for the first
number with a property, nested loops printing products, min/max tracking with
variables, state machines with a counter.

## Phase C: strings (adds to B)

Adds: string variables, concatenation `+`, repetition `s * n`, f-strings with
plain `{expr}` placeholders (no format specs like `:3` or `!r`), `str(x)`,
`len(s)`, indexing `s[i]` and `s[-1]` (no slicing), comparing strings with
`==`/`!=`, and `print()` with several arguments plus `sep=` / `end=` keywords.

Not allowed: slicing, string methods (`.upper()`, `.join()`, ...), `for ch in s`,
`in` on strings, lists, `int()`, functions.

Typical shapes: building a line of `*` characters in a loop, labelled output
`print("total:", total)`, f-string reports, simple text banners, reversing a
string by indexing in a while loop, counting a character by indexing,
receipts, progress bars, multiplication tables with `end=" "`.
