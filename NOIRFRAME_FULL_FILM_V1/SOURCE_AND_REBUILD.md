# Source and reproducibility

All picture/audio inputs needed for this edit are copied into inputs/ and listed with origin/SHA256 in reports/SOURCE_INPUTS.json. Copies are byte-identical to their preserved sources. The baseline master and native clips are editing inputs, not claims that their animation was newly drawn for this version. No old project is overwritten.

Requirements: Python3 with NumPy, SoundFile and Pillow; FFmpeg/FFprobe with libx264/libass; Playwright+Chromium for the optional actual-playback check. Blender4.3.2 opens the delivered native scenes. No network access, paid API or model download is needed to reproduce the edit from these supplied media/stems.

Recommended: `python source/rebuild.py --out /absolute/path/to/a/new/directory`. It copies the complete source/inputs into a new directory, builds and validates there, and preserves the delivered outputs. Standalone validation skips only the old-workspace preservation scan, not media or V10 checks.

The individual stages, for a prepared empty output project, are:

1. `python source/build_film.py` generates the audio remix, caption ASS/SRT, preserved prefix/tail and newly encoded middle. The intermediate candidate is retained separately.
2. `python source/finish_film.py` creates the canonical COMPLETE MP4 with short start/end audio fades, copying the encoded picture.
3. `python source/validate_film.py` checks dimensions/frame count/full decoding, all480 V10 frame hashes, audio levels and prior-project preservation where the original workspace is available.
4. `python source/review_film.py` plays the actual complete MP4 and replacement interval in Chromium; it needs local browser launch permission in this managed workspace.

The assembly uses integer video frames:0–1410 preserved prefix,1035-frame middle,135-frame final choice. inputs/concat.txt is a generated runtime cache with absolute workspace paths; build_film.py recreates it for the current location. The canonical file is86s/2580frames. Audio is48kHz with sample-level edit boundaries; only effects beds receive25ms edge blends. The two-pass loudness measurement uses actual input values for the technical report.

Native source: source/rigs.py,world.py,actions.py,build_native.py and render_saved.py build actual armatures, weighted geometry, IK and metric props/cameras. blender/SHOT_B_NATIVE.blend and SHOT_C_NATIVE.blend are baked editable scenes that play/render without running source scripts. Workbench was selected for their flat proof renders. Changing the native art requires new clip renders and new edit inputs; merely rebuilding the assembly does not improve animation automatically.

The local narration stock voice is Kokoro bm_daniel, already rendered into the delivered voice stems. Kokoro model/wrapper notices are included; model weights are not required to remix these WAVs. The score/effects are original local synthesis. This version's edit/composition is Python/FFmpeg; it retains existing HyperFrames picture graphics and adds measured ASS sentence captions. No unnecessary tool installation or remote generation was performed.
