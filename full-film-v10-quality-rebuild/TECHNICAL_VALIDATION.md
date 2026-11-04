# Technical validation

This report describes a review candidate, not artistic approval. Current scene assets are selected by `scenes/scene_XX/final-cache.json`; no draft filename guessing is used.

- 18 independently rendered HD scene inputs; 2580 frames total on the unchanged 86-second timeline.
- Preview and HD normal-speed Chromium playback reports and presented-frame evidence are linked by `SCENE_REPAIR_REGISTER.json`. Frames were also compared against the rejected master. Dropped presentation frames under concurrent load are recorded, not concealed; encoded clips receive full FFmpeg decode checks.
- `reports/driving-contact-validation.json`: 1441 driver samples; arm/rim constraints, eyes/head lead and actual scene-01 travel.
- `reports/pedal-contact-validation.json`: rigid shoe, heel pivot, pad contact and connected leg.
- `reports/chase-camera-validation.json` and `building-road-clearance.json`: readable vehicle bounds, road-aligned buildings and exterior cameras.
- `reports/house-motion-validation.json`: 3837 samples at 120 Hz, fixed limb lengths, planted world feet, own-depth shoe scale, projected sole contact, door/key/rail/curtain/phone contacts, phone ear anchor and table support. No audited foot points enter the cabinet. This is not exhaustive mesh collision simulation.
- `reports/v10-picture-preservation.json`: all 480 V10 SVG frames match baseline; original HD inputs match bytes. `reports/baseline-preservation.json` protects all 292 baseline files.
- `reports/choice-background-preservation.json`: all 180 low-res choice backgrounds pixel-match the baseline.
- `reports/source-validation.json`: current-source render hashes, HD codecs/dimensions/frame counts, baseline hashes, shared state/HUD data and measured audio/caption timing. `scripts/assert_final_gate.py` prevents export if validated inputs or active sources change.
- `reports/hyperframes-check-final.json`: actual local HyperFrames lint/runtime/layout/motion/contrast checks. Composite snapshots are in `reviews/graphics-check/`.

Final encoded-media, full-playback and download verification reports are added after those checks actually run. Do not infer final-file success from scene validation alone. Voice naturalness, emotional delivery and professional sound remain listening-unverified.

## Encoded review film

`renders/final/THE_PRICE_OF_SILENCE_V10_QUALITY_REBUILD_86s.mp4` exists: 14,154,055 bytes; SHA256 `2478d039720b69a28063317d8af8c772763c67c27110a45c5dda594e3b1134c2`.

`reports/REBUILD-encoding.json` verifies 1080×1920 H.264, 30 FPS, 2580 frames, 86.000000 seconds, stereo 48 kHz AAC. Full FFmpeg decode exits 0 (`REBUILD-decode.txt`). All 2580 decoded frames are nonblack and there are no identical adjacent frames; that pixel test alone is not a motion-quality assessment. `REBUILD-audio-meter.json` measures actual encoded input loudness −16.04 LUFS, true peak −3.63 dBTP and loudness range 7.60 LU. The meter's output fields describe its hypothetical normalization, not the delivered file.

Encoded contact sheets and 0.25-second action strips were inspected. Full normal-speed playback evidence is recorded separately in `reports/REBUILD_playback.json`; do not infer listening approval from this playback.

Full actual MP4 playback completed at rate 1 and media time 86 s: 2580 total frames, one dropped presentation frame, zero corrupted frames; wall time 86.895 s. See `reports/REBUILD_playback.json` and `renders/previews/REBUILD_PRESENTED.jpg`. The presentation drop is recorded rather than described as zero; the encoded full decode has no errors.
