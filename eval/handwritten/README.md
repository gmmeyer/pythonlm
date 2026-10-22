# Hand-written eval set

About 200 scripts per phase, written by a person (not by the generator and not
by the LLM that wrote `natural/`). One script per file in `phaseA/`, `phaseB/`, ...

They must pass the phase's support check, which you can verify with:

    uv run bcvm check eval/handwritten/phaseB/*.py --phase B

The runner's stdout on these is compared against CPython; a phase is done
when 99% match (see docs/DESIGN.md). Keep them out of every training input.
