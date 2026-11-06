# Edit and reproduce M05 using free local tools

Tools used: Blender 4.3.2; Python with NumPy, SciPy, Pillow and Cairo/librsvg; FFmpeg. Chromium/Playwright are optional for playback verification. No paid API, key or downloaded generation service is needed.

The editable ZIP extracts two sibling directories: NOIRFRAME_M05 (source, updated native scene and controls) and NOIRFRAME_M04 (only the exact baseline native model and control data needed for reproduction). Previous M04 files are never changed. Extract the ZIP into a new directory to avoid any collision with existing files. The updated `.blend` is independently editable and its reference image is packed.

## Edit an existing native scene

Open `assets/STAIRCASE_M05_F01.blend`, edit native controls and save as a new file. Do not replace the delivered model. From NOIRFRAME_M05:

```bash
blender -b assets/MY_EDIT.blend -t 2 --python source/export_edited.py -- --out-tag EDITED
python source/validate.py --tag EDITED
python source/render.py --tag EDITED --width 1080 --name EDITED
```

Use new output tags and names. Existing outputs are refused. If you alter foot timing, update the corresponding controls contact schedule too; metadata is not a collision or contact solver. Native materials use `base_color` properties for illustrated output. The vector head's acting parameters live in the controls JSON; the native packed image is a reference.

## Reproduce the artistic pass from M04 without rebuilding its rig

In a fresh extraction of this source ZIP, from NOIRFRAME_M05:

```bash
OPENBLAS_NUM_THREADS=1 python source/polish_plan.py
blender -b -t 2 --python source/polish_existing.py
blender -b assets/M05_ACTING_A02.blend -t 2 --python source/export_edited.py -- --out-tag A02
blender -b -t 2 --python source/finish_set.py
blender -b assets/M05_SET_FINISHED.blend -t 2 --python source/export_edited.py -- --out-tag REBUILD
python source/validate.py --tag REBUILD
python source/render.py --tag REBUILD --width 1080 --name REBUILD
```

The last export creates the native cache required by the renderer; it is regenerable and omitted from the compact ZIP. The full evaluated F01 cache is separately published. No factory-reset build_rig invocation is used in this route. `verify_native.py` and `verify_inheritance.py` target the delivered F01 tag by default; change their selected tag if verifying an edited version.
