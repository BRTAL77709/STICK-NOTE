# Free local rebuild

Dependencies used: Blender 4.3.2, Python 3 with NumPy/SciPy/Pillow and Cairo/rsvg support, FFmpeg. Chromium/Playwright is optional for recorded playback. No paid API or service is used. Run from NOIRFRAME_M04; keep the source/ and assets/ directory relationship.

The source ZIP includes native .blend, controls and approved packed head image. The evaluated geometry cache is published separately because it is regenerable.

## Build a new version without overwriting the delivered proof

```bash
OPENBLAS_NUM_THREADS=1 python source/plan_stairs.py --tag REBUILD
blender -b --factory-startup -t 2 --python source/build_rig.py -- --tag REBUILD
python source/validate.py --tag REBUILD
python source/render.py --tag REBUILD --width 1080 --name REBUILD_5s
```

Use a fresh tag/name each time. Source and controller hashes guard against stale geometry. Rendering only the included R06 cache requires the unchanged corresponding source/model/controls files.

## Edit the native scene

Open assets/STAIRCASE_M04_R06.blend in Blender. Native ankle/foot/root/head controls and their animation curves are editable. Save to a new filename. To evaluate the edited scene without reconstructing its animation:

```bash
blender -b assets/MY_EDIT.blend --python source/export_edited.py -- --out-tag EDITED
python source/validate.py --tag EDITED
python source/render.py --tag EDITED --width 1080 --name EDITED_5s
```

The generic edit exporter is supplied as an editing utility; the delivered R06 bake was produced by build_rig.py and independently reopened/verified with verify_native.py. The contact schedule remains the authored controls JSON: update it when changing foot timing or tread assignments. Geometry base_color custom properties feed the illustrated renderer; approved_head.py controls the original vector facial artwork. No full Blender material/lighting parity is promised for arbitrary edits.
