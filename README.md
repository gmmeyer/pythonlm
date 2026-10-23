# pythonlm: a learned bytecode interpreter

Hand it a Python script; a small transformer executes CPython 3.14 bytecode one
instruction at a time and prints exactly what CPython would. Scripts outside
the supported subset are refused up front.

- `docs/DESIGN.md`: the design
- `PLAN.md`: what's built, decisions, data estimate, next steps

This repo is the harness and the data pipeline (data generated on the Mac
Studio), plus the trainer and model stepper (`bcvm.train`, run on the 5090
box under WSL2, `uv sync --extra train`).

```bash
uv sync && uv run pytest
uv run bcvm run natural/phaseB/b1_000.py          # runner with the oracle stepper
uv run bcvm gen --phase A --tokens 1e9            # -> ~/work/pythonlm-data/phaseA/train
uv run bcvm train --name a1 --data A=1 --tokens 1e9            # -> $BCVM_DATA/runs/a1
uv run bcvm gate $BCVM_DATA/runs/a1/final.pt phaseA/eval_test  # end-to-end stdout match
```

## Layout

```
src/bcvm/
  config.py      pinned Python version, limits, data dir
  phases.py      what each phase accepts
  program.py     compile + listing (instruction indices, anonymized names)
  support.py     the support check (refusals), incl. abstract interpretation
  refvm.py       reference interpreter: step(), run()
  check.py       differential check against CPython, every instruction
  tokens.py      vocabulary, encoders, state parser
  decoding.py    output grammar -> token masks for constrained decoding
  harness.py     validator + runner loop + oracle stepper
  gen/           script sources: grammar, templates, natural (+ perturbation)
  pipeline.py    generate -> check -> sample -> tokenize -> shards
  shards.py      shard writer and reference readers
  evalsets.py    held-out eval sets
  train/         model, packed loader, trainer, model stepper + gate (torch)
natural/         LLM-written natural scripts per phase (+ SPEC.md)
eval/handwritten/  hand-written eval scripts, 200 per phase (never in training)
scripts/sync_to_trainer.sh
```

## License

MIT, see [LICENSE](LICENSE). The model weights on Hugging Face
([gmmeyer/pythonlm](https://huggingface.co/gmmeyer/pythonlm)) are under the same license.
