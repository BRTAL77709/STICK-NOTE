# THE PRICE OF SILENCE — V8 cinematic action test

**THE_PRICE_OF_SILENCE_MOTION_TEST_V8_8s.mp4** — 1080×1920, 30 FPS, H.264/yuv420p, exactly 8 seconds and 240 frames. Original locally synthesized rain, footsteps, scrape and trunk accents accompany the action.

V8 corrects the storyboard: the criminals approach the rear of the black sedan, open the trunk, crouch and lift the victim, fold his passive legs over the sill, place him inside, then react to the witness. The wide shot is continuous until 6.4 seconds, so the loading action is not hidden by a cut.

## Review files

- THE_PRICE_OF_SILENCE_V8_CONTACT_SHEET.jpg: encoded frames throughout all six beats.
- V8_LOADING_DETAIL.jpg: actual encoded action crops every 0.1 seconds, plus the loaded pose.
- V8_PLANTED_FEET.jpg: four consecutive encoded stance frames per foot during the lift.
- THE_PRICE_OF_SILENCE_V7_V8_COMPARISON.mp4: original-speed V7 and V8, with V7's final frame explicitly held for three seconds to match V8's duration. Audio is V8.
- TECHNICAL_VALIDATION.md, QUALITY_LOG.md and JSON reports: checks and limits.

## Reproduce with existing free tools

`./build.sh NEW_FILENAME.mp4` renders a new full-resolution output. It refuses to replace an existing MP4. For a preview: `python3 src/render_test_v8.py --scale .5 --fps 30 --stills --out previews/NEW_PREVIEW.mp4`.

The renderer is self-contained and uses existing Python, numpy, Pillow, system librsvg/Cairo and FFmpeg. No network, paid API or new installation is required. The optional playback helper uses the existing Playwright and Chromium. `src/audit_v8.py` additionally compares head functions against the preserved sibling V7 source. The source includes the illustrated assets and deterministic articulated choreography; generated WAV/SVG snapshots and intermediate previews remain local.

Previous versions are preserved. V8 awaits user review. No full film or V9 has begun.
