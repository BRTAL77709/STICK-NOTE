# THE PRICE OF SILENCE — V4 motion rebuild

A new 15-second illustrated chase sample. Previous versions, including V10, are preserved. Do not render the full 86-second movie without user approval.

## Review artifacts

- THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4: final 1080×1920, 30 FPS movie.
- HYPERFRAMES_HUD_DEMO_V4.mp4: actual HyperFrames speed/RPM/pursuit demonstration.
- CONTACT_SHEET.jpg: encoded frames at quarter-second intervals.
- V3_V4_COMPARISON.jpg and V3_V4_COMPARISON.md: role-matched differences.
- TECHNICAL_VALIDATION.md, MOTION_QUALITY_REPORT.md, REVIEW.md: checks and remaining limitations.
- audio/NARRATION_ONLY.wav and MIX_MASTER.wav: speech stem and new synchronized mix.
- caption-timing.json and NARRATION_EN.srt: measured phrase boundaries.

## Editable source

hyperframes/ contains the actual HTML/GSAP root, HUD/caption sub-compositions, component classes, shared vehicle data, local fonts and media. hyperframes-demo/ is a separate six-second composition. src/motion_state.py exposes vehicleState(t). src/driver_rig.py controls continuous face/cap/neck/torso/shoulders and contact-constrained arms/hands. src/driving.py supplies the hinged pedal. src/vehicle.py and world.py project layered illustrated assets from fixed world coordinates. src/audio.py uses the same RPM/motion state. src/build_hyperframes.py is the explicit HTML generator.

Use `sh build.sh NEW_OUTPUT.mp4` to check and render the supplied editable composition with the official local HyperFrames CLI. The script refuses existing output names. Set HYPERFRAMES_CLI if the local installation differs. The media, fonts and JS are included; binary runtimes and voice weights are not. Rebuilding the illustrated scene requires Python, NumPy, Pillow, librsvg/GObject/Cairo and FFmpeg. Use `python3 src/render_base.py --scale 1 --out hyperframes/assets/NEW_SCENE.mp4` and change index.html to that asset. Regenerate vehicle-state.js with src/export_state.py after changing the motion engine; then regenerate the audio mix. Preserve hand edits before rerunning the HTML generator.

The editable preview was opened and verified at execution-environment-local http://localhost:4088/#project/hyperframes. It is not a public download link. You can also open the source in the [HyperFrames desktop app](https://hyperframes.studio/studio/download?os=linux&src=cli).

## Honest limits

The exact CASH/SUSPICION reference image remains inaccessible. The supplied written navy/white/amber design direction was followed; no exact-match claim is made. Preserved V3 Michael narration is provisional, not approved. Auditory input is unavailable to this assistant: audio is measured, not certified by listening. A reusable word-caption method is included, but no local word aligner/model is installed; V4 uses measured phrase windows instead of invented word timestamps. The scene uses stylized projected vector geometry, not a photorealistic environment or a 3D asset renderer. No paid API, paid service or new download was used.
