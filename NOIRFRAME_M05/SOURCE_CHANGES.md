# M05 source changes

All new work is confined to NOIRFRAME_M05. Prior sources/models/videos are preserved by SHA-256 checks.

- `polish_plan.py`: offsets the saved M04 control data for anticipation, pelvis/chest acting, arms, gaze and settling. Foot targets and schedule are copied unchanged.
- `polish_existing.py`: opens the saved M04 .blend, keys existing native controls and builds the House17 set/camera. It does not recreate the character rig or skin.
- `finish_set.py`: extends the room floor of the edited scene; no character changes.
- `export_edited.py`: exports evaluated native meshes and per-frame camera transforms/facial parameters from the saved scene to a new tag.
- `render.py`: consumes that evaluated geometry; adds world-space cel lighting and planar contact shadows, follows the exported camera for clean output, fixes the diagnostic camera.
- `depth_render.py`: uses linear depth interpolation for orthographic geometry, retaining the depth buffer and silhouettes.
- `verify_inheritance.py`: hashes M04/M05 rest rig, meshes, skin and contact-controller curves.
- `verify_native.py`: reopens the delivered .blend, compares evaluated mesh vertices and moving-camera projection.
- `prepare_review.py`: validates complete decoding, creates synchronized comparison and every-frame contact sheets.
- `review_playback.py`: plays actual clips at normal/half speed; supports diagnostic playback.

`validate.py`, `plan_stairs.py`, `build_rig.py` and `approved_head.py` are inherited byte-identically from M04. The old build_rig.py is retained for provenance, not invoked for M05; use the native-scene edit route in REBUILD.md. It is not a claim that the M05 character was rebuilt. Core bake and final-render source hashes are recorded in the native export/render reports and delivery manifest.
