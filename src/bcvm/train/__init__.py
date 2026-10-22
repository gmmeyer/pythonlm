"""Trainer for the step model (runs on the 5090 box; needs `uv sync --extra train`).

This module only defines command-line options, so `bcvm` starts without
importing torch; the work is in train.py.
"""


def add_model_args(p):
    p.add_argument("--d-model", type=int, default=512)
    p.add_argument("--layers", type=int, default=8)
    p.add_argument("--heads", type=int, default=8)
    p.add_argument("--d-ff", type=int, default=1408)


def add_batch_args(p):
    p.add_argument("--seq-len", type=int, default=16384, help="tokens per packed row")
    p.add_argument("--rows", type=int, default=4, help="rows per micro-batch")
    p.add_argument("--no-compile", dest="compile", action="store_false")


def add_train_args(p):
    p.add_argument("--name", required=True, help="run name; output goes to $BCVM_DATA/runs/<name>")
    p.add_argument("--data", default="A=1", help="phase mix by group, e.g. B=0.75,A=0.25")
    p.add_argument("--tokens", default="1e9", help="packed tokens to train on (incl. listings and padding)")
    p.add_argument("--init", help="checkpoint to start from (weights only, e.g. the previous phase)")
    p.add_argument("--resume", action="store_true", help="continue from the run's latest.pt")
    p.add_argument("--out")
    add_model_args(p)
    add_batch_args(p)
    p.add_argument("--accum", type=int, default=4, help="micro-batches per optimizer step")
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--min-lr", type=float, default=0.1, help="final lr as a fraction of --lr")
    p.add_argument("--warmup", type=int, default=200)
    p.add_argument("--wd", type=float, default=0.1)
    p.add_argument("--clip", type=float, default=1.0)
    p.add_argument("--workers", type=int, default=3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--log-every", type=int, default=20)
    p.add_argument("--eval-every", type=int, default=500)
    p.add_argument("--eval-set", help="eval dir under $BCVM_DATA, default phase<first phase>/eval_test")
    p.add_argument("--eval-steps", type=int, default=50_000, help="steps per periodic eval")
    p.add_argument("--ckpt-every", type=int, default=500)


def add_evalsteps_args(p):
    p.add_argument("ckpt")
    p.add_argument("sets", nargs="+", help="eval dirs, relative to $BCVM_DATA, e.g. phaseA/eval_test")
    p.add_argument("--max-steps", type=int)
    p.add_argument("--json", help="write results here")
    add_batch_args(p)
