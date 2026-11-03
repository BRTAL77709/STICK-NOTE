# THE PRICE OF SILENCE — V3 production sample

The new 15-second sample is THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V3_15s.mp4. HyperFrames 0.8.226 rendered its HUD, captions, graphic entrances, final composition and encoding. Python generated the illustrated scene footage. Previous versions are preserved. The full 86-second film has not been rendered.

## Review files

- HYPERFRAMES_HUD_DEMO_V3_FINAL.mp4: six-second component demonstration.
- CONTACT_SHEET.jpg and V2_V3_COMPARISON.jpg: actual encoded frames.
- audio/: two new narrator auditions, narration-only WAV and mixed master WAV.
- caption-timing.json and NARRATION_EN.srt: measured sentence boundaries.
- TECHNICAL_VALIDATION.md, AUDIO_QUALITY_REPORT.md and HYPERFRAMES_INSTALLATION_AND_USAGE.md: evidence and limitations.
- hyperframes/ and hyperframes-demo/: editable compositions and required assets.
- src/: scene, vehicle, audio, state export and review code.

## Edit and rebuild

Free local tools used: Python 3, NumPy/Pillow, librsvg/Cairo/GObject, FFmpeg/FFprobe, Node 24, Chromium, HyperFrames 0.8.226 and GSAP 3.15.0. Existing Kokoro ONNX weights generated the new voice candidates. No paid API or cloud renderer was used. Runtime binaries and voice weights are not bundled.

Set HYPERFRAMES_CLI to your installed hyperframes/bin/hyperframes.mjs if different from the recorded workspace path. Run `sh build.sh MY_NEW_V3.mp4` to check and render the supplied HTML project. The script refuses existing output names and preserves edited HTML. To render a new scene asset, use `python3 src/render_base.py --out hyperframes/assets/MY_NEW_SCENE.mp4 --scale 1 --fps 30`, then update the video source in index.html. After changing motion_state.py, run src/export_state.py to update the shared state. src/build_hyperframes.py regenerates HTML; preserve your edits before invoking it.

`node "$HYPERFRAMES_CLI" preview hyperframes --background` opens the local editable preview. The project can also be opened in the HyperFrames desktop app. A localhost preview is not a public download link.

## Remaining review gates

Voice quality remains provisional: auditory input is unavailable to this assistant, so naturalness and professional performance have not been certified by listening. Both candidate WAVs are supplied for review. The exact CASH/SUSPICION HUD reference image was unavailable; the written navy/white/orange direction was followed without claiming an exact match. Future call, offer and choice helpers are included as source prototypes, not finished film scenes. Stop here for user review.
