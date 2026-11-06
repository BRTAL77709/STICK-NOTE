# Rebuild and edit

Free local dependencies used: Blender4.3.2, Python3.12 with NumPy/SciPy/Pillow/CairoSVG, FFmpeg/ffprobe, g++17. Chromium/Playwright is optional for playback QA. No keys or paid services.

## Actual production graph

`actions_<TAG>.py` + shared `vehicle_system.py` → `bake_native.py` → inherited M04 native armature with real leg/arm/digit IK → saved `.blend` + evaluated character mesh cache → `render_clips.py` with `sets.py`, `cameras.py`, `view_head.py`, `fast_depth.py` → FFmpeg H.264 → `sound_finish.py` AAC mux.

`reports/SHOT_REVISIONS.json` selects the delivered actor versions. Each cache records native file SHA and original producer/controller SHA. Historical producer snapshots are retained to validate earlier native bakes. Caches for all actors are omitted from the ZIP because they can be exported from supplied models; the inherited staircase evaluated cache is included. Do not use scratch/internal native history as production sources.

Compile the free raster helper:

```sh
g++ -O3 -shared -fPIC -std=c++17 source/fast_raster.cpp -o source/fast_raster.so
```

To export an already edited actor without reconstructing its rig, save the edit as a NEW model and run, substituting the controller tag listed in SHOT_REVISIONS:

```sh
blender -b blender/MY_KEY_EDIT.blend --python source/evaluate_saved.py -- --shot KEY_LOCK --tag MY_EDIT --controller source/actions_R08.py
python source/render_clips.py --shot KEY_LOCK --tag MY_EDIT --width 1080
```

This produces fresh `KEY_LOCK_MY_EDIT` native/cache data and a uniquely named cinematic/debug pair. Do not add `--final` for an experimental version: it deliberately routes to the official version map. Native user keyframes/mesh changes are evaluated, not replaced by the analytic pose dictionary. Scripted props and graphic head acting still come from the matching controller.

To regenerate a native scene from controllers rather than edit it, copy the chosen snapshot into a separate working package as `actions.py`, then `blender -b --python source/bake_native.py -- --shot KEY_LOCK --tag NEW_TAG`. The builder refuses to overwrite an existing native/cache output. It retains M04 bound geometry and replaces arm controls with native two-bone IK; it adds four two-bone digit chains. Units are metres, Blender is Z-up, illustrative controller space is Y-up; mapping is B(x,y,z)=(z,x,y), a proper rotation.

For identical delivered renders, export supplied actor models to NEW tags with the matching snapshots, then render those tags. The native presentation files add POV head visibility; the source motion files are geometry-cache authorities. DOOR_ENTRY and KEY_LOCK use POV only after the completed establishing/action phases. Both retain connected evaluated arms/torso while hiding the head from its own camera.

The source ZIP contains `scenes/STAIRS_INHERITED.json.gz`. `STAIRS` intentionally renders this exact M05 evaluated mesh/pose source, its original cinematic/fixed cameras and retained controls. To change that performance use the M05 native export workflow in the preserved repository; M07 does not claim an independent newly authored staircase rig.

## Editing boundaries

- Actual skinned actor geometry, native IK and poses: edit `.blend`, then `evaluate_saved.py`.
- Key, handle, door, fabric, vehicles, world, timing/contact schedule: edit the matching controller/`sets.py`/`vehicle_system.py`, rebake fresh native mirrors, export and rerender. Native prop-only GUI edits are not consumed by the scripted prop renderer.
- Cameras: `cameras.py` overrides and `cameras_base_R07.py`; native camera snapshots mirror the intended framing but final face-card/view treatment is separate vector rendering.
- Face/cap/mask: `approved_head_view.py` and `view_head.py`; original illustrated design retained, front/profile/rear features camera-dependent.
- Sound: `sound_finish.py`, contact events + integrated vehicle speed, no narration. The supplied utility targets official names; for experimental audio copy the package or adapt output stems to fresh names.

## Checks

`validate_interactions.py` checks solved native bones/shoes; `validate_props.py` tests rounded tip contact markers against props; `validate_exit_terrain.py` checks actual shoes against road/curb ramp; `check_door_body.py` tests sampled visible body vertices against door/jamb; `validate_world.py` checks integrated trajectories; `native_reopen_check.py` independently reopens saved models. `review_playback.py` uses actual Chromium playback at1× and0.5×. Reports state sampling/tolerances and exclusions. Validation is not full collision, cloth or force simulation.

Full-film assembly is deliberately absent. Preserve prior M03/M04/M05/V10 files and use new tags/directories for edits.
