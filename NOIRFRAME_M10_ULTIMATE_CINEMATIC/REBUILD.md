# Free local M10 editing and rebuild

Existing dependencies: Blender4.3.2; Python3.12/NumPy/SciPy/Pillow/CairoSVG; FFmpeg; g++17. Chromium/Playwright is optional playback QA. No paid API, external sample library or generated-asset download is required.

1. Run `python source/prepare_m10.py` after extracting the editable package.
2. Run `python source/fetch_native_caches.py --revision <delivery-commit>` to obtain the exact separately published baseline/output caches. SHA256 checks protect every download; existing files are never overwritten. Omit the revision to use work. This retrieves this project's existing data, not new production assets.
3. Compile `g++ -O3 -shared -fPIC -std=c++17 source/fast_raster.cpp -o source/fast_raster.so`.
4. Use `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1` for production commands. `render_batch_m10.py --width 360` makes10FPS previews from native states; `--width 1080 --final` makes native1080p/30FPS exports. Rendering refuses existing completed outputs.

Selected source tags are in reports/SHOT_REVISIONS.json. actions_M10I.py supplies exit acting/handle timing, actions_M10G.py the hallway continuation, actions_M10B.py the seated key/cloth pass, and actions_M10.py the first driving pass. These consume exact selected M09 states from BASELINE_REVISIONS.json, preserving working contacts. interaction_system.py defines shared phases. The native builder evaluates real no-stretch two-bone IK and bound skin; render_clips.py consumes those exact cached states and native vertices.

stairs_m10d.py directly retimes the actual STAIRS_M09.blend contact/root/ankle/pole keys and adds FK effort. It exports STAIRS_M10D.blend. check_stairs_m10d.py reopens the native file and measures721 evaluations at120Hz.

For native actor edits, save under a new name and use evaluate_saved.py with a matching controller/new tag. Edit corresponding prop/target definitions together to preserve contact. For target-authoring edits, use bake_native.py with a NEW tag. Blender may exit0 after a Python error: require the expected complete native/cache files as well as checking logs.

## Masters and resumability

Final frames are rendered directly at1080×1920 and retained losslessly under frames/M10_<SCENE>_FINAL/. PNGs are masters, not upscaled preview images. PRODUCER.json fingerprints critical source/cache inputs. `render_clips.py ... --final --resume` preserves an interrupted MP4 in scratch and reuses validated saved frames; completed exports cannot be overwritten. Source changes reject stale frame caches. Preserve old frames in a history directory when making a new source revision.

MP4 encoding is CRF18 H.264/yuv420p,30FPS,faststart. No output bitrate or file-size target is imposed. File size follows content compressibility. Sound finishing retains original24kHz PCM WAVs under sound/ and muxes AAC with video stream copying. Do not reduce animation to satisfy upload limits; source caches may be delivered separately for transport.

CAMERA_ANIMATION.json supplies actual camera samples and explicit local/world spaces. SOURCE_TO_RENDER.json maps all eight outputs to native models, caches and controllers. The complete final look also uses scripted world/lighting/face/depth composition; native Blender mirrors are not a one-click replacement for that pipeline.

Preserve M09/V10 and previous versions. These are eight separate scenes; no full86-second film is assembled.
