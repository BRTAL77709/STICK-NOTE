# M09 source-level audit and repair record

All eight M08 MP4s and their native .blend/cache/controller sources are present. Input hashes and probe metadata are in reports/INPUT_MEDIA_AUDIT.json. Previous versions are protected by a pre-edit manifest.

| Scene | Observed M08 defect / source cause | M09 source repair |
|---|---|---|
| Driving cockpit | Mirror framing hides emotional response; restrained torso; foot leaves accelerator before actual brake onset | cameras.py changes action/reaction coverage; actions_M09 controls retain fixed wheel pads and articulate chest/shoulders/head; pedal transfer ends at the actual brake onset |
| Road/buildings | Sparse cold streetlights and repetitive road edges; vehicle appears open/hollow | sets.py adds fixed lamp fixtures, broken amber wet-road reflections, drains, selective street props; legacy/geometry.py restores omitted side glass and rear deck |
| Chase | Witness acceleration lacks a clear danger response; car shell incomplete | vehicle_system.py adds a continuous throttle increase before braking, closer independently controlled pursuer, unchanged shared road and bicycle model; same camera/world transforms, with repaired clear exterior pursuer reveal instead of the obstructed low camera |
| Car exit/running | Long static setup and weak urgency; shell has missing body surfaces | preserve M08J continuous root and individual terrain contacts; native M09D torso/arm acting with M09K street-side camera/head presentation, actual opening in driver-side glazing |
| Key/lock | Oversized key and fast small interaction; source key geometry .16 m, relatively oversized bow | M09B .10 m blade/.025 m bow radius; fingertip targets follow actual reduced bow; native hand follows key; monotone 9-second action clock slows insertion/rotation/withdrawal; tight readable view |
| Door entry | Restrained look-back and settling | native fixed wrist/foot targets retained; tucked elbow bend restored after detecting and rejecting a 65mm sleeve/door regression; authored backward attention and torso preparation, recovery after closure; shared House17 architecture |
| Stairs | Mechanically repeated torso/arm pulses | preserve M08 actual root/ankles/IK/poles; non-repeating anticipation, individual step effort and landing recovery keyed on actual M08 native controls |
| Window/curtain | Performance small; rear/room reaction coverage weak; sedan shell incomplete | strongest M08F fabric/contact controls retained; wide approach coverage replacing an early out-of-frame view, then closer grip-side view and readable recoil coverage; full sedan surfaces in same registered parked location |

## Actual rig implementation
bake_native.py retains BASELINE_M04 armature/skin, native shin IK constraints LEG_TWO_BONE_IK_L/R with chain_count=2 and use_stretch=False; native forearm IK constraints M07_NATIVE_ARM_IK_L/R, explicit wrist and elbow pole objects; native two-bone digit IK. Controller feet and contact targets are authored, not force simulated. Blender evaluates final bones and skinned vertices used by render_clips.py. No separately redrawn skeleton supplies final body geometry.

Staircase native edits are in polish_stairs_m09.py; other character controls are in actions_M09D.py (unified acting), actions_M09H.py (restored tucked door elbows), actions_M09K.py (frozen original exit contacts plus native reframing); selected revisions are recorded. Actual selected revisions are in reports/SHOT_REVISIONS.json. The scripted geometry renderer provides illustrated world/props and face treatment, with physical depth ordering.

## Internal fault fixed
CAR_EXIT_RUNNING initial bake failed because wildcard legacy imports shadowed the module alias E with an easing function. The module was renamed EXIT_BASE and the shot rebaked. Blender can exit zero after a Python exception, so the batch runner separately requires the actual expected output file.

## Do not infer artistic approval
Rig/contact checks and playable files do not establish cinematic quality. Some movements, surfaces and faces remain stylized/procedural. No full film assembled; V10 and M08 are untouched.


## Rendered failure corrections
- Door M09D: sampled upper-sleeve penetration64.98mm at2.6s. Rejected. M09H restores the original collision-safe elbow bend while retaining acting/contact targets; final sampled penetration0mm.
- Window M09D: early close camera briefly excluded the approaching witness. Rejected as final staging. M09G uses a wider approach and actual native head/camera rebake before the grip close-up.
- Exit M09D: tracking camera crossed behind the facade and hid arrival. Rejected as final staging. M09K keeps the camera street-side. Native comparison:180,144 non-head vertices, zero coordinate differences.
- Chase M09D: low reveal view was obstructed by a car panel. Replaced by M09L pursuer-targeted exterior camera. No vehicle trajectory alteration during this camera correction.
- A sparse running solve was tested and rejected for non-convergence; the original successful bounded solver remains in the selected native motion.
