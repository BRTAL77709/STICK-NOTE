#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 scripts/assert_final_gate.py
HYPERFRAMES_CLI="${HYPERFRAMES_CLI:-/workspace/stick-note-dev/tools/node_modules/hyperframes/bin/hyperframes.mjs}"
export HYPERFRAMES_TELEMETRY_DISABLED=1
export HYPERFRAMES_BROWSER_PATH="${HYPERFRAMES_BROWSER_PATH:-/usr/bin/chromium}"
out="${1:-renders/final/THE_PRICE_OF_SILENCE_V10_QUALITY_REBUILD_86s.mp4}"
if [ -e "$out" ]; then echo "Output exists; choose a NEW filename: $out" >&2; exit 1; fi
node "$HYPERFRAMES_CLI" check hyperframes --json
node "$HYPERFRAMES_CLI" render hyperframes --fps 30 --quality looks --crf 26 --workers 1 --no-browser-gpu -o "$out"
