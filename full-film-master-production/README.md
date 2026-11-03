# THE PRICE OF SILENCE — NOIRFRAME master production

This is a complete 86-second **review candidate** and reusable production project. It is not an assertion that professional artistic quality has been achieved. Read ARTISTIC_QUALITY_REPORT.md and QUALITY_GATES.md alongside the film. Previous versions, especially V10, are preserved.

## Film and review package

The actual MP4 is in renders/final/. Review the 18-scene contact sheet, full contact sheet, interaction strips, English narration script/SRT, narrator/caller audio, score/effects mix, technical report and artistic report. All 18 scene sources are under scenes/. The editable HyperFrames project includes the exact video inputs, lossless mix, fonts and local JS. The approved V10 crime functions are reused without changes; their time mapping preserves trunk closure/latch before the head turn.

## Reusable source

engine/api.py exposes characterState, vehicleState, cameraState, environmentState, propState, lightingState, graphicsState and audioEvents. Actual implementation is in engine/animation/, engine/composition/, engine/audio/ and engine/graphics/. assets/ contains editable SVG model assets, metric rig metadata, route/house plans, individual voice phrases, lossless audio and licenses. NOIRFRAME_TEMPLATE.json points to the reusable film configuration. PRODUCTION_BIBLE.md and ANIMATION_SYSTEM.md explain the staging and limits.

## Rebuild and edit

Existing free tools: Python 3, NumPy/Pillow, librsvg/Cairo, FFmpeg/FFprobe, Chromium, Node, HyperFrames 0.8.226 and GSAP 3.15.0. Binary runtimes and model weights are not redistributed. Set HYPERFRAMES_CLI if your install differs. `sh build.sh NEW_NAME.mp4` checks and renders the supplied composition with the official local CLI and refuses existing output names. It does not regenerate your edited HTML.

For picture edits, modify the scene/rig source, then run `python3 scripts/render_scenes.py --stage final`. Every scene's evaluated SVG content is hashed; unchanged pictures reuse validated caches even after unrelated source changes. Interrupted drafts remain preserved. `python3 scripts/build_hyperframes.py --stage final` mounts the actual current scene assets; preserve hand-edited HTML before running this explicit generator. After changing vehicle motion, run `python3 scripts/export_state.py`, rebuild the sound with engine/audio/mix.py into new output names, encode the lossless mix to FLAC and rebuild the composition. scripts/assemble_base.py can concatenate scene picture caches with FFmpeg.

Provided phrase audio is sufficient to rebuild the mix without a voice model. Only new speech generation needs existing Kokoro weights/runtime; KOKORO_MODEL and KOKORO_VOICES override the recorded workspace paths. Do not silently time-stretch a phrase that exceeds its scene budget. The script reports that mismatch for revision.

The editable preview returned HTTP 200 at execution-environment-local http://localhost:4090/#project/hyperframes. This is not a public download URL. Source can also be opened in the [HyperFrames desktop app](https://hyperframes.studio/studio/download?os=linux&src=cli).

## Honest limits

The reference MP4 was accessible and inspected. No reference frames or audio were copied into the movie. The scene remains stylized projected vector animation with simplified vehicle shells and staged house/alley lenses. New stock voices replace the rejected audio, but naturalness and emotional performance are unverified by listening. The attempted free Whisper model download was blocked by the proxy (403); no retry was made. Captions use measured phrases, not invented word timestamps. Technical success does not confer artistic approval. No paid API/service or new subscription was used.
