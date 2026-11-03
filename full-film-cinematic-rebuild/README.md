# THE PRICE OF SILENCE — cinematic rebuild / integrated gate

This delivery replaces neither V10 nor the rejected full-film-v1. It contains a complete18-scene defect audit, revised86s storyboard, systems/route/house/audio/graphics plans, a new15-second integrated driving test, editable source and technical/artistic reports. The whole86s film has NOT been rerendered. User approval of this test is required first.

Watch THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_INTEGRATED_TEST_15s_FINAL.mp4. Review its encoded contact sheet and QUALITY_REPORT.md, then compare the substantive defects in SCENE_DEFECT_AUDIT.md. House17's door/key sheet is a labeled prototype, not finished film footage. Exterior/interior/window/curtain/phone continuity is specified in ENVIRONMENT_AND_HOUSE_PLAN.md for the next production stage.

## Implemented systems

- Persistent metric city: roads/curves, crossing geometry, sidewalks/curbs, drains, puddle glints, varied facades with frames/glass/doors/gutters, poles/wires/signs/trees and depth layers.
- Shared motion state:20→100km/h over8.6s after pedal onset4.2s; integrated arc-length travel; separate pursuer closing-speed/odometer;0.32m tires; steering/pitch/roll/suspension and wet-road light footprints.
- Physical in-dash speedometer/RPM/clock; visible needle climb across inserts, pedal/boot contact, approved witness head/cap/hoodie rig, IK rim grips, shoulder/head/eye/blink/breath/acceleration actions. Front and OTS steering use16:1 rack ratio.
- Ten motivated shot segments with tracking, reaction, pedal, cluster, driver weight response, low pursuit and OTS. Rain/glass/wiper/amber passing lights; phrase-aligned subtitles.
- Original local engine/road/rain/score and Flite English narration, with continuous engine phase following shared RPM. No paid API or downloaded model/sample.

These are intentionally illustrated geometric components, not photorealistic3D. The sedan rendering is simplified; natural acting and synthetic speech still need user judgment. Technical validity is not an artistic approval.

## Files

SCENE_DEFECT_AUDIT.md and plan/scene-audit.json: all18scenes, eight defect/fix categories each. REVISED_CINEMATIC_STORYBOARD.md: all18intervals. SYSTEM_PRODUCTION_PLAN.md: reusable production tasks/gates. ENVIRONMENT_AND_HOUSE_PLAN.md and plan/house_geometry.json: route and architecture. AUDIO_REBUILD_PLAN.md: sound audit/next-stage cue contract. MOTION_GRAPHICS_STYLE.md: palette/type/layout/timing. INTEGRATED_TEST_EN.srt and narration-timing.json: actual phrase timing. reports/: quantitative source/audio/encoding/playback evidence. src/: complete renderer/system source.

src/illustration_engine.py and approved_components.py preserve the original Art/librsvg raster engine and approved witness drawing functions; unused legacy functions remain available but are not the rebuilt driving world. New world.py, vehicle.py, driving.py, motion_state.py, render.py, audio.py and house_system.py are separate new components. Existing V10 crime rigs remain untouched in their original directories; not used as a substitute for driving footage.

## Rebuild locally

Existing free runtime: Python3.12, NumPy, Pillow, librsvg2/Cairo/GObject, FFmpeg7.1.5/libx264/AAC/Flite, installed DejaVu Sans. Chromium/Playwright are needed only for review. No package installation is required in the production workspace. No runtime binaries/fonts are bundled.

`sh build.sh MY_NEW_TEST.mp4` decodes the supplied audio master if needed, then renders15s at1080×1920/30FPS. The renderer refuses to overwrite an existing MP4. Use a new output name. For fresh original synthesis run `python3 src/audio.py` in a clean version folder; it generates local PCM/stems/phrase timings and masters audio. The delivered compressed master can introduce a second AAC generation on a clone rebuild; original local WAV masters are retained in the production workspace.

Preview: `python3 src/render.py --scale .333333333 --fps 30 --out previews/MY_PREVIEW.mp4`. Range preview: add `--from 6.5 --to 12.3 --fps 8 --scale .25` with a NEW output. `python3 src/validate.py` checks all450 source poses/kinematics/order. `python3 src/review.py MY_NEW_TEST.mp4 new_label --play` performs complete1x playback and retains presented-frame evidence. `--step .25` without --play generates an encoded frame sheet. Reuse labels only in a new folder; review outputs are preserved.

No full-film rendering command is provided: this branch stops at the integrated approval gate.

## Free runtime preflight

|Tool|Status|Version|Action|
|---|---|---|---|
|Python|Available|3.12.14|Used|
|FFmpeg/FFprobe|Available|7.1.5|Used for encode/mix/decode/metadata|
|NumPy / Pillow|Available|2.3.5 /12.3.0|Used|
|librsvg/Cairo/GObject|Available|System shared libraries|Existing raster engine used|
|Chromium/Playwright|Available|System Chromium / Playwright1.62.0|Actual local playback|
|Node|Available|24.19.0|Not required by this renderer|

External voice APIs, downloads,3D tools, stock/matting/transcription models are unnecessary for this test and skipped under the user's free-local-tools instruction. No API-key setup is needed.
