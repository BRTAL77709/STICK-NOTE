#!/bin/sh
set -eu
cd "$(dirname "$0")"
HYPERFRAMES_CLI="${HYPERFRAMES_CLI:-/workspace/stick-note-dev/tools/node_modules/hyperframes/bin/hyperframes.mjs}"
export HYPERFRAMES_TELEMETRY_DISABLED=1
export HYPERFRAMES_BROWSER_PATH="${HYPERFRAMES_BROWSER_PATH:-/usr/bin/chromium}"
out="${1:-THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4}"
if [ -e "$out" ]; then echo "Output exists; choose a new filename: $out" >&2; exit 1; fi
node "$HYPERFRAMES_CLI" check hyperframes --json
node "$HYPERFRAMES_CLI" render hyperframes --fps 30 --quality looks --crf 20 --workers 1 --no-browser-gpu -o "$out"
