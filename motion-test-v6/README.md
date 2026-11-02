# THE PRICE OF SILENCE — V6 review package

- THE_PRICE_OF_SILENCE_MOTION_TEST_V6_5s.mp4 — actual five-second 1080×1920/30 FPS test.
- THE_PRICE_OF_SILENCE_V6_CONTACT_SHEET.png — decoded-frame review, 0.2 s dragging / 0.1 s head-turn samples.
- V6_HEAD_TURN_EYES_HIDDEN.png — same head at a fixed diagnostic camera, with/without eye geometry, at 0.1 s intervals. This is a diagnostic SVG render, not a retouched final frame.
- V6_ENCODED_CONTACTS.png — consecutive crops decoded from the final MP4. Foot rows are registered to world/pavement coordinates; grip rows follow each support anchor. Guides appear only in this evidence image, not in the film.
- THE_PRICE_OF_SILENCE_V5_V6_COMPARISON.mp4 — actual V5/V6 encodes at matching times, V6 audio.
- QUALITY_LOG.md — changes, corrections, visible improvements and three remaining flaws.
- TECHNICAL_VALIDATION.md, VERSION_HISTORY.md and JSON evidence — measured checks and limits.
- src/ — complete animation, original audio, audits, playback and diagnostic code.

Re-render in the existing Linux workspace with a NEW filename:

`bash build.sh review_v6_02.mp4`

Preview: `python3 src/render_test_v6.py --scale .5 --fps 30 --stills --out previews/review02.mp4`

The renderer refuses an existing MP4. Existing NumPy, Pillow, librsvg/Cairo, FFmpeg and DejaVu Sans are required; no new installation, paid API or model. Browser playback QA uses installed Playwright/system Chromium and the supported local process escalation. An eyes-hidden render can be made with --hide-eyes for diagnostics only.

The approved designs/story are preserved. No full 1:26 film is started. V6 awaits user review; no artistic score is claimed.
