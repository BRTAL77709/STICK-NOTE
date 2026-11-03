# Resume this checkpoint

Read PROGRESS.md, PRODUCTION_BIBLE.md, QUALITY_GATES.md and the final reports first. Check running render processes before launching another. All work is inside full-film-master-production; do not overwrite previous version directories.

Current scene assets are identified by scenes/scene_XX/final-cache.json. scripts/render_scenes.py --stage final validates and reuses caches based on the evaluated picture content. It preserves interrupted files. Do not rerender unchanged scenes. scripts/build_hyperframes.py --stage final mounts the current assets; preserve hand-edited HTML before regenerating it.

The official local CLI is /workspace/stick-note-dev/tools/node_modules/hyperframes/bin/hyperframes.mjs. Use HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium and HYPERFRAMES_TELEMETRY_DISABLED=1. Check hyperframes, inspect snapshots, then render to a NEW output path with --fps 30 --quality looks --crf 26 --workers 1 --no-browser-gpu. A shell wrapper is build.sh.

After rendering, run scripts/validate_media.py, scripts/review.py for encoded contact sheets and --play for the whole movie at normal rate. Record exact failures and artistic limits. Do not claim voice naturalness from signal properties or a valid file. The free Whisper weight request already failed with 403; do not retry it blindly.

Publish only final files, required source/media, licenses and reports. Exclude old drafts, .hyperframes caches, raw reference frames and duplicated WAV stems. Verify public downloads against local hashes before sharing links. A valid render is a review candidate, not automatic artistic approval. Work does not continue after the execution environment stops unless a supported running job exists.
