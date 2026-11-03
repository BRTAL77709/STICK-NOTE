#!/bin/sh
set -eu
TASK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUTPUT_NAME=${1:-THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_INTEGRATED_TEST_15s_FINAL.mp4}
case "$OUTPUT_NAME" in */*) echo 'Use a new filename without separators.' >&2; exit 2;; esac
mkdir -p "$TASK_DIR/assets/audio" "$TASK_DIR/previews" "$TASK_DIR/reports"
if [ ! -f "$TASK_DIR/assets/audio/master.wav" ]; then
 if [ -f "$TASK_DIR/audio/master.m4a" ]; then
  ffmpeg -v error -n -i "$TASK_DIR/audio/master.m4a" -c:a pcm_s16le -ar 48000 -ac 2 "$TASK_DIR/assets/audio/master.wav"
 else
  python3 "$TASK_DIR/src/audio.py"
 fi
fi
python3 "$TASK_DIR/src/render.py" --scale 1 --fps 30 --out "$OUTPUT_NAME"
ffmpeg -v error -i "$TASK_DIR/$OUTPUT_NAME" -f null -
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration,size -of json "$TASK_DIR/$OUTPUT_NAME"
