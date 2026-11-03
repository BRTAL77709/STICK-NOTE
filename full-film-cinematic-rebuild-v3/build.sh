#!/bin/sh
set -eu
TASK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUTPUT_NAME=${1:-THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V3_15s.mp4}
case "$OUTPUT_NAME" in */*) echo 'Use a NEW filename without separators.' >&2;exit 2;; esac
test ! -e "$TASK_DIR/$OUTPUT_NAME" || { echo 'Output exists; choose a new name.' >&2;exit 2; }
HF_BIN=${HYPERFRAMES_CLI:-/workspace/stick-note-dev/tools/node_modules/hyperframes/bin/hyperframes.mjs}
export HYPERFRAMES_BROWSER_PATH=${HYPERFRAMES_BROWSER_PATH:-/usr/bin/chromium}
export HYPERFRAMES_TELEMETRY_DISABLED=1
node "$HF_BIN" check "$TASK_DIR/hyperframes" --json
node "$HF_BIN" render "$TASK_DIR/hyperframes" --fps 30 --quality looks --crf 20 --workers 1 --no-browser-gpu -o "$TASK_DIR/$OUTPUT_NAME"
ffmpeg -v error -i "$TASK_DIR/$OUTPUT_NAME" -f null -
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration,size -of json "$TASK_DIR/$OUTPUT_NAME"
