# THE PRICE OF SILENCE — V7 motion test

Review file: **THE_PRICE_OF_SILENCE_MOTION_TEST_V7_5s.mp4**. Exactly 5 seconds / 150 frames / 1080×1920 / 30 FPS / H.264, with locally synthesized rain, scrape and footstep audio.

V7 reuses V6 assets, body rigs, SVG/librsvg engine and successful head-turn code. The interaction now uses distinct authored step plans, contact-weighted hip transfer, two-bone IK, a shared rigid upper-arm support frame, and a fixed-step passive pelvis/heels/head model. No paid API or additional installation was used.

Review the contact sheet, V6/V7 side-by-side video, encoded contact crops and eyes-hidden head test. See TECHNICAL_VALIDATION.md and QUALITY_LOG.md for measured results and limitations. Full ledgers remain local; summary JSON reports are included.

## Reproduce

Use the existing free environment: Python 3, numpy, Pillow, system librsvg/Cairo and FFmpeg. Run `./build.sh NEW_FILENAME.mp4`. The renderer refuses to replace an existing MP4. The sources require no external assets; illustrated assets and procedural audio are generated locally. For a preview: `python3 src/render_test_v7.py --scale .5 --fps 30 --stills --out previews/NEW_PREVIEW.mp4`.

The diagnostic browser helper additionally uses the existing Playwright and Chromium. No network is required to render.

V7 is for user review. Earlier versions are preserved. Production stops here; the full film has not started.
