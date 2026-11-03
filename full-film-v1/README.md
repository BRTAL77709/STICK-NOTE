# THE PRICE OF SILENCE — complete film v1

Delivered film: [THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4](delivery/THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4?raw=true), 86.000 seconds, 1080×1920, 30 FPS, H.264/AAC. All 18 storyboard scenes are present. This is the first full-film version for creative review; prior motion-test versions are preserved.

Start with the MP4 and the complete encoded-frame contact sheet. FINAL_STORYBOARD.md and storyboard.json specify every scene. NARRATION_SCRIPT.md, narration-timing.json and THE_PRICE_OF_SILENCE_EN.srt provide the original dialogue and actual local voice timings. TECHNICAL_VALIDATION.md and QUALITY_CONTROL_REPORT.md distinguish measurements from visual review and remaining limitations.

## Rebuild with free local tools

Runtime used: Python3, NumPy, Pillow, librsvg2/GObject/Cairo shared libraries, FFmpeg/FFprobe with libx264, AAC and Flite, and installed DejaVu Sans. Chromium plus Python Playwright are only needed for playback verification. No paid API, key, external generation service or downloaded voice model is required. Runtime binaries and fonts are not bundled.

From this directory run `sh build.sh MY_NEW_FULL_FILM.mp4`. Choose a NEW filename; existing MP4 outputs refuse overwrite. This reconstructs a local WAV master from the delivered AAC audio, renders 18 scene caches, assembles the film, fully decodes it and probes metadata. Rebuilding from AAC entails one audio generation loss. For original lossless synthesis instead run `python3 src/production_audio.py` then `python3 src/master_audio.py` before build.sh. Those commands regenerate original audio assets and timing; preserve any edited audio beforehand. The lossless individual voice phrases and narration stem are also supplied for editing.

For a low-resolution animatic run `python3 src/render_film.py --stage preview`. Scene-cache fingerprints invalidate image changes; interrupted .rendering.mp4 drafts are not treated as completed caches. The public delivery excludes redundant raw WAVs, earlier preview drafts and rendered scene caches; they remain in the original workspace. Internal cache-migration scripts are not needed to rebuild.

`python3 src/validate_source.py` evaluates all2580 source poses and timing/order constraints. `python3 src/check_full_playback.py YOUR.mp4 review_label` plays the whole film at1x and records presented frames. Review labels should be new to preserve evidence. Source functions and reusable rigs are documented in REUSABLE_COMPONENTS.md.

The voices have synthetic prosody; character movement, car perspective and lip shapes remain deliberately simplified. These are documented limitations, not an assertion of final broadcast quality. User creative approval is pending.

## Download encoding

The GitHub connector rejects request bodies over16MiB. The original16,004,921-byte render remains unchanged in the workspace. The published delivery/THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4 is a smaller11,427,199-byte H.264 CRF24 copy of those exact frames with the original AAC stream copied unchanged. Resolution, frame rate, scene timing and runtime are identical. It is separately decoded, probed and played. The public delivery omits the larger duplicate original; root encoding/contact reports refer to that original, while delivery/ records refer to the downloadable copy.
