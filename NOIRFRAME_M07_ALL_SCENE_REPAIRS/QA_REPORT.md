# M07 technical and artistic QA

Eight separate clean previews, diagnostic counterparts and before/after comparisons. **ARTISTIC REVIEW REQUIRED** for all8. No full86-second render; no user approval granted.

## Measured native actor checks

Metres in JSON; table in millimetres. Body evaluated in saved Blender scenes, not just controller targets. Native two-bone legs/arms and four two-bone digit chains use no stretch.

|Shot/native version|Wrist IK mm|Leg IK mm|Digit target mm|Stance drift mm|Limb variation mm|Measured status|
|---|---:|---:|---:|---:|---:|---|
|DRIVING_COCKPIT R12|0.068081|0.057973|0.005126|N/A|0.002383|TECHNICAL PASS|
|KEY_LOCK R08|0.080124|0.000668|0.003205|0.000319|0.001953|TECHNICAL PASS|
|DOOR_ENTRY R22|0.082168|0.013472|0.005844|0.007924|0.001599|TECHNICAL PASS|
|WINDOW_CURTAIN R11|0.076139|0.002552|0.012362|0.001221|0.001395|TECHNICAL PASS|
|CAR_EXIT_RUNNING R09|0.082785|0.087886|0.003324|0.069718|0.001924|TECHNICAL PASS|
|DRIVER_CHASE R07|0.068081|0.057973|0.005126|N/A|0.002383|TECHNICAL PASS|

Tolerance: native IK/contact and stance1.5mm; digit target2mm; limb length/joint gap0.1mm. Seated driving stance is N/A: heel anchor and toe/pedal-plane are tested separately. Actual native wrist/limb geometry is checked at30Hz; dense60Hz data is supplied. No continuous-collision or ground-reaction-force guarantee.

Retained M05 staircase freshly reopened at120Hz/601poses: stance drift **0.360045mm**, foot-to-tread **0.359281mm**. M04 baseline was independently reopened too. Native reopen sample/character-cache maximum vertex difference: **0.000000mm**. This is inheritance verification, not newly approved stair acting.

Root positions are piecewise-linear native keyed locations, position-continuous by construction; per-frame travel is reported, not mislabelled teleportation. Accelerations/jerk may still feel mechanical. General anatomical joint-limit and whole-body dynamic balance certification are absent.

## Prop, terrain and vehicle checks

- Door/jamb sampled native body vertex penetration: KEY 0.000000mm; DOOR 0.000000mm, tolerance5mm. Excludes intentional contact mittens/digits and transparent head card. No edge/swept-volume certification.
- Exit shoe/ramp check corrected109.443mm penetration to0.05456mm with revised swing clearance; see EXIT_TERRAIN_REPAIR.json. It samples actual shoes and edge points, not merely ankle markers.
- Key axis error, insertion depth, native fingertip-to-prop marker distances, handle hinge, curtain wrist/fold width and driving heel/toe checks are in PROP_INTERACTION_VALIDATION.json. Finger marker model uses a rounded7mm contact proxy; full finger mesh friction/collision is not solved.
- Saved native prop parity sampled independently: key/handle/door, wheel and fabric shape-key grid. This verifies editable mirror transforms, not automatic native prop edit ingestion by the scripted renderer.
- Integrated120Hz vehicle state: gap14.000m to **6.406866m**, conservative bumper clearance2.106866m, maxspeed9.921330m/s; stationary at end. Minimum tyre-centre/curb margin3.019050m. No tyre-friction/force simulator.
- City/House17/window and parked sedan share coordinates; ROUTE_MAP.png and SCENE_REGISTRATION.json show registration. Full-house navigable architecture and all camera/world swept collisions are not certified. Interior cutaways are intentional.

## Final encoded media and actual playback

|Clip|Seconds|Frames|Normal dropped|Half-speed dropped|Decode|
|---|---:|---:|---:|---:|---|
|DRIVING_COCKPIT|12.0|360|20|0|PASS|
|ROAD_BUILDINGS|7.0|210|10|0|PASS|
|CAR_CHASE|11.0|330|7|4|PASS|
|CAR_EXIT_RUNNING|10.8|324|1|1|PASS|
|KEY_LOCK|7.0|210|3|0|PASS|
|DOOR_ENTRY|13.0|390|7|7|PASS|
|STAIRS|5.0|150|12|0|PASS|
|WINDOW_CURTAIN|10.5|315|6|2|PASS|

All clean outputs:1080×1920/30fps/H.264/yuv420p, AAC Foley. ffprobe frame counts, complete FFmpeg decoding, black/identical-frame scans and SHA256 are in MEDIA_VALIDATION.json. Diagnostic frame counts also checked, with every encoded diagnostic frame on ordered contact pages. Browser playback ended at both1×/0.5× without corrupted-frame reports. Dropped frames above are real observed browser/render-load limitations; complete offline decode is a separate check, not proof of zero playback drops.

Playback-presented frames and encoded hero/contact sheets were visually inspected. This records actual automated playback plus image inspection, not a claim of human auditory/subjective artistic approval. Diagnostics use fixed actor views except key establishing/detail and vehicle tracking coverage; they are not all a single fixed world camera.

Foley is locally synthesized from contact events and vehicle speed; waveform peak/RMS and timing recorded. No paid service, narration or human listening approval. Samples follow30Hz event timing (bound1frame).

## Artistic verdict and unresolved issues

No sequence is USER APPROVED. All8 are available for review; measured checks pass only their stated tolerances. The cockpit remains angular, face perspective uses a graphic/card approximation, fabric folds can resemble vertical strips, motion is authored/kinematic and may still feel mechanical, lighting/reflections are simplified, and complete cloth/hand collision/force balance is absent. See REMAINING_DEFECTS.md. These are review candidates, not a claim that every M07 acceptance criterion has been met.

Before/after comparisons play at1× with different choreography/cameras labelled; shorter older sources are explicitly held after their ends. Stairs retains M05 gait. Prior782protected local files hash unchanged; publication additionally checks every old Git tree entry is preserved.
