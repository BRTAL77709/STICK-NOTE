#!/bin/sh
set -eu
TASK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUTPUT_NAME=${1:-THE_PRICE_OF_SILENCE_MOTION_TEST_V5_5s.mp4}
case "$OUTPUT_NAME" in */*) echo 'Use a new filename inside motion-test-v5, without directory separators.' >&2; exit 2;; esac
python3 "$TASK_DIR/src/render_test_v5.py" --scale 1 --fps 30 --stills --out "$OUTPUT_NAME"
ffmpeg -v error -i "$TASK_DIR/$OUTPUT_NAME" -f null -
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration -of json "$TASK_DIR/$OUTPUT_NAME"
