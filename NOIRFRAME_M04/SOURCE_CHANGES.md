# Source changes

All work is new under NOIRFRAME_M04. No V10, V12 or M03 production source was modified.

- `plan_stairs.py`: support/contact schedule, pelvis/torso/FK acting curves and full shoe-profile clearance.
- `build_rig.py`: native Blender bones, IK, limits, constraints, vertex groups, Armature modifiers and evaluated-geometry export.
- `export_edited.py`: export an edited native scene to a new tag without rebuilding its animation.
- `render.py`: illustrated raster output from Blender-evaluated geometry, diagnostic bone/target overlay, FFmpeg stream.
- `validate.py`: evaluated foot, bone, tread, root and penetration measurements.
- `verify_native.py`: reopen the saved rig and compare actual evaluated geometry to the cache.
- `make_head.py`: preserve approved head art as packed native image.
- `approved_head.py`, `svg.py`, `world.py`, `depth_render.py`: retained illustrated rendering support. Approved head artwork preserved.
- `review_playback.py`, `finish_review.py`: real browser playback, decoding, comparison and all-frame inspection sheets.
- `rig.py`: small vector/math utilities only; the previous pose solver is not imported.

Exact hashes and constraint/binding manifests are in reports/RIG_MANIFEST_R06.json and DELIVERY_MANIFEST.json. M03 source paths/functions are enumerated in SOURCE_LEVEL_PROOF.md. The native scene contains genuine editable curves and constraints; the mesh cache is output, not the only editable source.
