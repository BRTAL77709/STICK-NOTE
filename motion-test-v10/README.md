# THE PRICE OF SILENCE — V10 grounded loading test

Review **THE_PRICE_OF_SILENCE_MOTION_TEST_V10_10s.mp4**: 1080×1920, 30 FPS, H.264/yuv420p, 10 seconds / 300 frames. The complete action remains in one wide three-quarter rear view until the 8-second head-turn cut.

V10 replaces V9's screen-space staging with a shared orthographic world: X across the sedan, Y along it, Z height; pavement is Z=0. The same local SVG/librsvg renderer, illustrated character/hoodie/cap/knit-cap palette and successful head projection remain. This is cel-illustrated 2.5D, not a photorealistic renderer.

## Review package

- THE_PRICE_OF_SILENCE_V10_CONTACT_SHEET.jpg — frames decoded from the final MP4.
- V10_GROUND_PLANE_DIAGNOSTICS.jpg and diagnostics/ — clearly labeled review-only ground grid, car footprint, opening, foot contacts, hand anchors and pelvis trajectory.
- V10_LIFTING_LOADING_DETAIL.jpg — actual encoded action frames every 0.1 seconds.
- V10_ENCODED_PLANTED_FEET.jpg — consecutive stance-foot crops from the final MP4.
- V10_HEAD_TURN_EYES_HIDDEN.jpg — fixed-camera geometry proof with/without eyes.
- V9_V10_COMPARISON_REPORT.md and the side-by-side MP4.
- TECHNICAL_VALIDATION.md, QUALITY_LOG.md and machine-readable validation JSON.

## Reproduce locally

`./build.sh NEW_FILENAME.mp4` renders a new full-resolution file and refuses an existing MP4. Preview: `python3 src/render_test_v10.py --scale .5 --fps 30 --stills --out previews/NEW_PREVIEW.mp4`.

Only existing Python, numpy, Pillow, system librsvg/Cairo and FFmpeg are needed. Source assets and procedural audio are included as code. The optional playback helper uses existing Playwright and Chromium. No API, network, new installation or paid service is needed to render. Generated WAV/SVG snapshots and internal drafts remain local.

Diagnostics are separate artifacts. The delivered film contains no debug overlays. V1–V9 remain intact. Stop after V10 for user review; the 86-second film has not started.

Diagnostic legend: teal grid=pavement Z=0; red outline=car footprint; cyan outline=trunk opening; green dots=stance feet; amber dots=swing feet; pale yellow=hand anchors; magenta=pelvis path. All eleven full-size ground-overlay PNGs are included.
