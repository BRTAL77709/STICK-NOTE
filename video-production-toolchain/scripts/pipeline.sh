#!/bin/sh
# Render prepared scene state into a NEW job directory. Never overwrite outputs.
set -eu
cd "$(dirname "$0")/.."
name="${1:?Usage: ./scripts/pipeline.sh NEW_JOB_NAME}"
case "$name" in *[!A-Za-z0-9_-]*|'') echo 'Use letters, digits, _ or - in job name' >&2; exit 2;; esac
export NOIRFRAME_RUN_DIR="$(pwd)/renders/$name"
if [ -e "$NOIRFRAME_RUN_DIR" ]; then echo 'Job already exists; choose a new name' >&2; exit 2; fi
python scripts/check_prepared.py
mkdir -p "$NOIRFRAME_RUN_DIR"
.venv/bin/python scripts/reference_download.py --check > "$NOIRFRAME_RUN_DIR/yt-dlp-version.txt"
offset=$(python -c 'import json; t=json.load(open("shared/timeline.json")); print(t["speechStartFrame"]/t["fps"])')
if .venv/bin/python scripts/transcribe.py shared/narration.wav --offset "$offset" > "$NOIRFRAME_RUN_DIR/whisper-status.txt" 2>&1; then
  echo 'Using actual Whisper transcript.'
else
  code=$?
  if [ "$code" -ne 3 ]; then cat "$NOIRFRAME_RUN_DIR/whisper-status.txt" >&2; exit "$code"; fi
  echo 'Whisper checkpoint unavailable: using measured source-script captions, NOT ASR.' >&2
fi
node scripts/render-remotion.cjs
./scripts/hf.sh check hyperframes --json > "$NOIRFRAME_RUN_DIR/hyperframes-check.log"
./scripts/hf.sh render hyperframes --format mov --prores-profile 4444 --fps 30 --quality looks --workers 1 --no-browser-gpu -o "$NOIRFRAME_RUN_DIR/hyperframes-hud.mov"
python scripts/assemble.py
python scripts/validate_demo.py
python scripts/review_demo.py
