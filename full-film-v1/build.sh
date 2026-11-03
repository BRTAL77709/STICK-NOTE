#!/bin/sh
set -eu
TASK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUTPUT_NAME=${1:-THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4}
case "$OUTPUT_NAME" in */*) echo 'Use a new filename without path separators.' >&2; exit 2;; esac
mkdir -p "$TASK_DIR/assets/audio" "$TASK_DIR/cache/preview" "$TASK_DIR/cache/final" "$TASK_DIR/previews"
if [ ! -f "$TASK_DIR/assets/audio/master_mix.wav" ]; then
 if [ -f "$TASK_DIR/audio/master_mix.m4a" ]; then
  ffmpeg -v error -n -i "$TASK_DIR/audio/master_mix.m4a" -ar 48000 -ac 2 -c:a pcm_s16le -t 86 "$TASK_DIR/assets/audio/master_mix.wav"
 else
  python3 "$TASK_DIR/src/production_audio.py"
  python3 "$TASK_DIR/src/master_audio.py"
 fi
fi
python3 "$TASK_DIR/src/render_film.py" --stage final --out "$OUTPUT_NAME"
ffmpeg -v error -i "$TASK_DIR/$OUTPUT_NAME" -f null -
ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames,sample_rate,channels:format=duration -of json "$TASK_DIR/$OUTPUT_NAME"
