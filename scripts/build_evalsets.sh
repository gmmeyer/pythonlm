#!/usr/bin/env bash
# Build the held-out eval sets for the given phases (default A B C).
set -euo pipefail
cd "$(dirname "$0")/.."
for phase in "${@:-A B C}"; do
  for phase1 in $phase; do
    uv run bcvm evalset --phase "$phase1" --name test --scripts 10000
    uv run bcvm evalset --phase "$phase1" --name natural --scripts 3000
    uv run bcvm evalset --phase "$phase1" --name bignum --scripts 3000
    if [ "$phase1" != "A" ]; then   # phase A scripts have no loops, so nothing runs 1,000+ steps
      uv run bcvm evalset --phase "$phase1" --name long --scripts 1000
    fi
  done
done
