#!/bin/bash
# Verifier entrypoint. pytest + pytest-json-ctrf are baked into the environment
# image (environment/Dockerfile), so nothing is installed here.
set -uo pipefail

LOGDIR=/logs/verifier
mkdir -p "$LOGDIR"

pytest /tests/test_outputs.py -rA --ctrf "$LOGDIR/ctrf.json"
status=$?

if [ "$status" -eq 0 ]; then
  echo 1 > "$LOGDIR/reward.txt"
else
  echo 0 > "$LOGDIR/reward.txt"
fi

# The reward file is the signal; always exit cleanly so the harness reads it.
exit 0
