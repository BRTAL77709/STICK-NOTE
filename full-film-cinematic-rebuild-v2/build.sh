#!/bin/sh
set -eu
TASK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUTPUT_NAME=${1:-THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V2_15s.mp4}
case "$OUTPUT_NAME" in */*) echo 'Use a NEW filename without separators.' >&2; exit 2;; esac
mkdir -p "$TASK_DIR/previews" "$TASK_DIR/reports"
test -f "$TASK_DIR/audio/MIX_MASTER.wav"
python3 "$TASK_DIR/src/render.py" --scale 1 --fps 30 --out "$OUTPUT_NAME"
ffmpeg -v error -i "$TASK_DIR/$OUTPUT_NAME" -f null -
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration,size -of json "$TASK_DIR/$OUTPUT_NAME"
