# Exact source changes and root causes

All files below are under this NEW production folder. No V10 or V12 source is edited. `source/legacy/` contains read-only reference copies, not runtime imports.

The previous system already contained IK: adding another IK label would not fix it. Inspection found independently retimed pelvis/foot channels, repeated steps with little support transfer, grip checks based on wrist targets rather than rendered fingertips, and vehicle/camera transforms that could disagree. These tests replace the per-shot action generator instead of decorating those curves.

- `source/contact_rig.py`: hierarchical pelvis, torso, head and articulated limbs; individual world foot targets, fixed-length two-bone IK, toe-pivot lift, explicit two-phalange fingers, sole mesh and continuous pelvis spline.
- `source/rig.py`: removes old feet/skeleton cycle generators; makes IK pole copying explicit to prevent shared-vector mutation.
- `source/stair_test.py`: separately timed tread/landing targets, anticipatory support transfer, segmented mass estimate and preview balance solve; rail touch/release and hallway transition.
- `source/key_test.py`: door-local lock, inserted/rotated key, articulated grip, separate lever hand, then 9-degree hinge movement. Both grips follow their moving objects.
- `source/vehicle_test.py`: one cockpit/vehicle state; wheel and finger contacts share its matrix; heel-anchored pedal movement drives acceleration/braking; independently integrated chase distances on one fixed curved road; suspension response.
- `source/actor.py`: renders actual hierarchical geometry, contact-aware shoes, tapered sleeves, oriented palms and fingers. No generic replacement character.
- `source/geometry.py`: keeps the sedan/city design; body yaw/roll/pitch and unsprung wheels use consistent transforms.
- `source/world.py`: optional camera-up vector and numeric camera transforms.
- `source/depth_render.py`: native half-height rendering for simultaneous cockpit/road views; depth-buffer occlusion.
- `source/shots.py`: fixed diagnostic compositions, physical key/lever/door parent geometry, synchronized cockpit and fixed-road cameras. Camera movement does not create stair progress.
- `source/render_tests.py`: native-resolution streaming H.264 export and exact per-frame rig-state/source hashes.
- `source/validate.py`: bounded geometry, contact, support, grip, pedal and projection checks, every-frame CSV.
- `source/review_playback.py`: actual Chromium video playback and presented-frame samples.
- `source/export_review.py`: unretimed original/corrected comparisons, full decode, metadata checks and all-frame cropped inspection pages.
- `source/finish_render.py`: sequential validation/export entry point.

`source/approved_head.py`, `source/environments.py` and `source/svg.py` are unchanged V12 copies. Asset/source SHA records are included. All modifications are reviewable Python source; no paid APIs or generated image services were used.
