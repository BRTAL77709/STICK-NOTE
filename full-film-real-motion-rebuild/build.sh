#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 scripts/assert_final_gate.py
out="${1:-renders/final/THE_PRICE_OF_SILENCE_REAL_MOTION_REBUILD_86s.mp4}"
if [ -e "$out" ]; then echo "Output already exists; choose a NEW filename: $out" >&2; exit 1; fi
HYPERFRAMES_CLI="${HYPERFRAMES_CLI:-/workspace/stick-note-dev/tools/node_modules/hyperframes/bin/hyperframes.mjs}"
export HYPERFRAMES_TELEMETRY_DISABLED=1
export HYPERFRAMES_BROWSER_PATH="${HYPERFRAMES_BROWSER_PATH:-/usr/bin/chromium}"
node "$HYPERFRAMES_CLI" render hyperframes --fps 30 --quality looks --crf 26 --workers 1 --no-browser-gpu -o "$out"
