#!/bin/sh
set -eu
export HYPERFRAMES_TELEMETRY_DISABLED=1
export HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium
exec node "${HYPERFRAMES_CLI:-/workspace/stick-note-dev/tools/node_modules/hyperframes/bin/hyperframes.mjs}" "$@"
