# THE PRICE OF SILENCE — V9 ten-second action test

Review **THE_PRICE_OF_SILENCE_MOTION_TEST_V9_10s.mp4**: 1080×1920, 30 FPS, H.264/yuv420p, exactly 10 seconds and 300 frames. Original procedural rain, footfalls, scrape, fabric, closing thump and latch audio.

V9 extends V8: drag → open → regrip → lift → load → release/withdraw → close completely → latch → notice → head turn → narrowed stare. The continuous wide shot remains through the complete closure; the close-up cut is at 8 seconds.

## Files

- THE_PRICE_OF_SILENCE_V9_CONTACT_SHEET.jpg: decoded frames across all phases and the cut.
- V9_LOADING_DETAIL.jpg: actual encoded frames every 0.1 seconds from regripping through closure.
- V9_PLANTED_FEET.jpg: consecutive decoded stance-foot crops during lifting.
- V9_HEAD_TURN_EYES_HIDDEN.jpg: fixed-camera head geometry diagnostic with/without eyes.
- THE_PRICE_OF_SILENCE_V8_V9_COMPARISON.mp4: original-speed V8 and V9; V8's last frame is explicitly held two seconds. V9 audio accompanies it.
- ANIMATION_QUALITY_REPORT.md, ACTION_ORDER_VALIDATION.md, QUALITY_LOG.md and JSON reports.

## Existing free pipeline

`./build.sh NEW_FILENAME.mp4` renders a new full-resolution file; existing MP4s are never replaced. Preview: `python3 src/render_test_v9.py --scale .5 --fps 30 --stills --out previews/NEW_PREVIEW.mp4`.

Source uses existing Python, numpy, Pillow, librsvg/Cairo and FFmpeg. `src/v8_engine.py` is a byte-identical snapshot of V8, bundled for reusable assets, rig math and rasterizer. `src/render_test_v9.py` supplies the retiming, action states, restaging, withdrawal and closure. The optional playback checker uses existing Playwright/Chromium. Audit comparison additionally reads the sibling preserved V8 source. No network, paid API, new package or third-party footage is needed to render. Generated WAV/SVG snapshots and intermediate drafts remain local.

V1–V8 are preserved. V9 awaits user review. No V10 or full 86-second film has begun.
