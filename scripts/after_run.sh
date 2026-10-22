#!/usr/bin/env bash
# Standard evaluation of a finished run: teacher-forced step accuracy on the
# phase's eval sets, the BINARY_OP breakdown, and the end-to-end gate.
# Results land in $BCVM_DATA/runs/<run>/. Run inside the train env (pylm).
#   scripts/after_run.sh a3 A
set -euo pipefail
run=$1
phase=${2:-A}
dir=$BCVM_DATA/runs/$run
ckpt=$dir/final.pt
sets="phase$phase/eval_test phase$phase/eval_natural phase$phase/eval_bignum"
[ "$phase" != A ] && sets="$sets phase$phase/eval_long"
bcvm evalsteps "$ckpt" $sets --json "$dir/evalsteps.json" > "$dir/evalsteps.txt" 2>&1
python scripts/binop_detail.py "$ckpt" "phase$phase/eval_test" > "$dir/binop_detail.txt" 2>&1
bcvm gate "$ckpt" "phase$phase/eval_test" --json "$dir/gate_eval_test.json" > "$dir/gate.txt" 2>&1
grep -E "^eval" "$dir/evalsteps.txt"
cat "$dir/gate.txt"
