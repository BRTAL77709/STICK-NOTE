# THE PRICE OF SILENCE — integrated cinematic rebuild V2

Watch THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V2_15s.mp4 and CONTACT_SHEET.jpg. This is a complete new15-second chase test for review; every earlier version/render is preserved. No86-second film has been rendered.

Deliverables: actualMP4, encoded contact sheet, before/after sheet/report, audio/NARRATION_ONLY.wav, audio/MIX_MASTER.wav andM4A, two male voice auditions, updated plan/timeline.json, captions/SRT, motion/vehicle/HUD/audio/character/camera source, technical validation and honest weaknesses. AUDIT_AND_REBUILD.md audits the rejected actual video/source/timeline; baseline playback evidence is retained in reports/.

## Reusable source

motion_state.py: SI-unit vehicle/path state and seven beats plus steering/corner subcut. world.py: fixed-world street/crossings/facades/curbs/trees/poles/reflections, bidirectional camera projection and near clipping. vehicle.py: continuous illustrated sedan, wheels/steering/roll/suspension and view-facing lights. driving.py: approved-identity perspective head, articulatedIK driver, real pedal/dash. graphics.py: compact transparent HUD/actual counters/bars and phrase captions measured usingDejaVu font metrics. render.py: deterministic assembly, actual projected mirrored pursuit, range/full renderer. audio.py: original state-driven soundscape and neural phrase assembly. voice.py: offlineKokoro audition/phrase generation using already present local model. review.py: actual1x browser playback/presented frames and encoded sheets. validate.py: all450poses/kinematics/projected displacement/contacts/timing checks.

## Free local rebuild

Existing runtime: Python3, NumPy/Pillow, librsvg/Cairo/GObject, FFmpeg7.1.5/libx264/AAC and installedDejaVuSans. Playwright/Chromium for playback verification. Localvoice generation uses the existing separate/workspace/stick-note-dev/.venv andKokoroONNX/model; it does not require a paidAPI or download. Model/license/path details are in VOICE_AND_LICENSE_NOTES.md.

`sh build.sh MY_NEW_TEST.mp4` uses the supplied mixedWAV and renders450frames at1080×1920/30FPS. ExistingMP4s refuse overwrite; choose a new filename. Preview: `python3 src/render.py --scale .333333333 --fps 30 --out previews/MY_NEW_PREVIEW.mp4`. Range: add `--from 13.2666666667 --to 15 --fps 15` with a new output. `python3 src/validate.py` checks source/model state; `python3 src/review.py MY_NEW_TEST.mp4 new_label --play` runs full1x playback and saves presented-frame evidence. Labels/output names must be new to preserve prior reviews.

To regenerate speech in a clean version folder, setKOKORO_MODEL/KOKORO_VOICES to your existing licensed files and invoke src/voice.py with aPython environment containingkokoro-onnx/onnxruntime/numpy. Then run src/audio.py in the render environment. Audition/phrase synthesis refuses overwrite; preserve previous media. The supplied WAV mix means a clone rebuild requires no speech-model download. Runtime binaries/weights/fonts are not bundled.

HUD image reference is unavailable in current accessible assets; written style direction was followed without inventingCASH/SUSPICION data. Artistic suitability, final voice choice and any remaining weaknesses require user review. Stop here: full86s production requires approval of this test.
