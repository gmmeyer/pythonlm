#!/usr/bin/env bash
# Copy generated shards to the training machine over the LAN.
#
#   scripts/sync_to_trainer.sh user@trainer:/data/pythonlm-data [phaseA phaseB ...]
#
# Re-runs only transfer what changed. Finished shards are immutable, and a
# shard's .json is written last, so a half-written shard is never mistaken for
# a complete one (the trainer only reads stems that have a .json).
set -euo pipefail
SRC="${BCVM_DATA:-$HOME/work/pythonlm-data}"
DEST="${1:?usage: $0 user@host:/path [phaseA ...]}"
shift
if [ "$#" -eq 0 ]; then
  set -- $(cd "$SRC" && ls -d phase* 2>/dev/null)
fi
for phase in "$@"; do
  echo "== $phase"
  rsync -a --partial --progress \
    --exclude '._*' --exclude '.DS_Store' --exclude '*.tmp' \
    "$SRC/$phase" "$DEST/"
done
