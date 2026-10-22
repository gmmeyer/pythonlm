# Hand-written eval set

200 scripts per phase in `phaseA/`, `phaseB/`, `phaseC/`, one per file,
written to look like code people write rather than like the generators'
output. They come from Claude subagents (at the project owner's request; the
design originally asked for a person): four writers per phase, each told a
different style (everyday quick scripts, terse algorithms, semantics corner
cases, long simulations), none of which saw `natural/` or the generators.
Each script was checked with

    uv run bcvm check eval/handwritten/phaseB/*.py --phase B

`scripts/check_holdout.py` confirms none of their listings occur in any
training shard. The runner's stdout on these is compared against CPython; a
phase is done when 99% match (see `docs/DESIGN.md`). Keep them out of every
training input.
