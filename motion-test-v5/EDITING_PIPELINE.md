# Reusable local editing/rendering pipeline

Tested in this Linux Codex workspace. No ZIP import, paid API, account key or network dependency is needed for the animation.

## Generate a new version

`bash build.sh review_v5_02.mp4`

This runs the self-contained procedural SVG source, local librsvg/Cairo rasterization, FFmpeg H.264/AAC encoding, full decode and ffprobe. Existing output MP4 names are refused. Keep NumPy, Pillow, FFmpeg, librsvg/Cairo and DejaVu Sans installed. The same source can render an internal preview:

`python3 src/render_test_v5.py --scale .5 --fps 30 --stills --out previews/review_v5_02.mp4`

The source refuses an existing MP4. Audio and scene snapshots generated inside this new V5 project are intermediate assets and may be regenerated. Earlier-version project folders are never edited. Native Windows execution has not been verified; use the current workspace rather than assuming its Cairo/librsvg libraries are on the user's Windows computer.

## Check choreography

`python3 src/audit_v5.py`

Parses all 150 SVG poses. Checks plant locks, upper-arm support, constant heel-ground heights, backward support, trailing-leg geometry, bone lengths, asynchronous phases, frame-96 cut and head-plane parameters. This complements visual inspection; it is not an artistic quality score.

## Review the actual encode

`python3 src/check_playback.py /absolute/path/to/new.mp4 review02`

Uses installed system Chromium through Playwright; this workspace requires the supported process escalation for browser launch. Plays the actual MP4 at 1× from an in-memory Blob, records completion/drop counts and saves presented-frame strips. No website or file-page policy changes. Listen to the soundtrack separately when reviewing; automated audio/decoder tests are not subjective listening.

`python3 src/make_review_artifacts.py`

Creates the named V5 contact sheet from the final encode at approximately 0.2 s intervals during dragging and 0.1 s during head rotation, including adjacent frames 95/96. Refuses an existing sheet. Update the target filename deliberately when producing a subsequent review set.

## Editing rules

Maintain one timing source in render_test_v5.py. Derive sound cues from the same contact phases as the characters. Use FFmpeg for cuts, comparisons, mixing and encoding. Do not run voice-transcription tools without actual speech. Do not use a different compositor as a substitute for rigging or choreography.

For the full film, approval is still required. The framework report describes an optional HyperFrames composition path; no full-film timeline or composition has been built.
