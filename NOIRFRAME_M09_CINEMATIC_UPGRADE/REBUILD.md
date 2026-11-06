# M09 editable pipeline

Free existing dependencies: Blender4.3.2; Python3.12 with NumPy, SciPy, Pillow, CairoSVG; FFmpeg; g++17. Chromium/Playwright are optional playback QA tools. No paid API.

Compile: `g++ -O3 -shared -fPIC -std=c++17 source/fast_raster.cpp -o source/fast_raster.so`.

`reports/SHOT_REVISIONS.json` identifies selected native caches/controllers. `actions_M09D.py` is the unified acting baseline; M09H restores collision-safe door elbow bends. M09G supplies the wider bedroom approach; M09K retains the original exit body/foot motion with street-side camera/head orientation; M09L supplies the unobstructed chase reveal. KEY_LOCK uses the same actor geometry under presentation tag M09E. `blender/KEY_LOCK_EDITABLE_FINAL_M09_R02.blend` includes the final POV camera/visibility; KEY_LOCK_M09D retains the baked contact baseline.

Native pipeline: authored contact targets → retained M04 armature and skin → no-stretch native leg, arm and digit IK → evaluated Blender bone/vertex caches → render_clips.py consumes the exact cached authoring state and evaluated geometry → depth-aware Python/C++ illustrated world/face composition → FFmpeg → sound_finish.py.

Stairs: polish_stairs_m09.py edits the actual STAIRS_M08.blend torso and arm controls while preserving pelvis/root/feet/poles/contact schedule, and exports STAIRS_M09.blend with export_stairs_m08.py. check_stairs_m09.py reopens that file and measures 601 samples at120Hz.

To change a native actor, save under a NEW tag and run evaluate_saved.py with the matching controller. To change contact authoring, edit actions.py in a new production copy and run bake_native.py with a new tag. Blender can exit0 after a script error: require the expected nonempty cache and native output, not only the process exit code.

Set `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1` for production commands. render_batch_m09.py supports `--width 360 --shots ...` for previews and `--width 1080 --final --shots ...` for final video. All rendered filenames refuse overwrites. Native head/camera producer hashes are verified against frozen source snapshots.

Final renders omit duplicate full-resolution diagnostic encoding; Low-resolution diagnostics remain available (10FPS for the final chase preview, 30FPS for the other selected previews). Before/after contact sheets use frames from actual encoded M08 and M09 MP4s. Camera cuts are declared by cameras.py.

Sound is synthesized locally; actual staircase landings, saved character contact transitions and curtain edge velocity drive relevant effects. Vehicle engine pitch follows the integrated speed clock. Sound finishing copies the silent file to scratch and muxes AAC without changing its video stream.

Native .blend files are editable rigs/props. The complete final look also depends on the supplied scripted geometry/lighting/face/depth renderer; native prop-only changes do not automatically change scripted prop rendering. Keep those shared definitions in sync. No self-contained Blender-only final render is claimed.

Preserve M08/V10 and all previous versions. Do not assemble the full film without a separate instruction.

## Source transport

GitHub's blob API rejected the original70MB source ZIP with HTTP422. The smaller editable package retains all15 native Blender files, all scripts and the staircase cache. The ten evaluated caches are available separately under scenes/ in this same repository delivery. After extracting the source package, run `python source/fetch_native_caches.py --revision <delivery-commit>` (or omit the revision to use work). CACHES_MANIFEST.json supplies exact SHA256 checks. Existing files are never overwritten. This retrieves cached output from this project, not a paid service or new asset dependency. Native Blender files remain editable without downloading those caches.
