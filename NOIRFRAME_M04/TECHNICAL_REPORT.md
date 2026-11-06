# M04 technical and artistic report

## Root causes and replacement

Read SOURCE_LEVEL_PROOF.md for the exact five-shot source audit. M03 did contain real analytic two-bone IK and geometric attachments: describing everything as simple translated sprites would be incorrect. Its low initial pelvis, prescribed root/clearance timings, root-relative wrist paths and rebuilt tube/box garment limited posing and silhouette. Smoothing those curves did not replace the underlying representation.

M04 uses an actual Blender 4.3.2 armature with connected leg chains, native two-bone IK on each shin, fixed-length bones, stable knee poles, hinge limits, world ankle targets and world shoe-orientation controls. Shoes and articulated links are armature-bound; the hoodie has blended pelvis/spine/chest vertex weights. Shoulder and elbow counter-swing are authored FK. Pelvis/torso weight transfer is authored relative to support targets. Neck/head orientation constraints stabilize the approved illustrated head. No full-body force, muscle, cloth or general collision simulation is claimed.

`source/build_rig.py` creates those native constraints and bindings, evaluates Blender's dependency graph and exports its actual mesh vertices. `source/plan_stairs.py` authors the contact schedule and curves. `source/render.py` draws evaluated mesh vertices; it does not run the old analytic pose generator. The approved original vector head is mapped onto the evaluated, bone-bound head quad; its packed PNG also appears in the native scene. Head and limbs retain their approved stylized identity, not realistic anatomy.

Native causal test: disabling the left leg IK at 2s changes the bound shoe by **67.8034mm**. Reopening the delivered .blend and comparing 576 evaluated vertices at six times gives **0m difference** against the export cache. Blender camera and illustrated projection differ by at most **0.000094 pixels**. See NATIVE_REOPEN_VERIFICATION.json and RIG_MANIFEST_R06.json.

## Choreography and actual changes

A continuous five-second shot shows three consecutive 180mm rises, alternating legs and a fourth swing into landing recovery. Foot motion has a stationary stance, anchored toe-off rocker, clearance-calculated swing and landing. The pelvis rises with support transfer, shifts laterally and settles; the arms counter-swing from shoulder joints and the head remains within about 1 degree of vertical. Initial knee flexion is about 32 degrees, compared with M03's measured 79–80 degrees, using the same 370mm thigh and shin lengths. The final camera is static: no cut, shake or blur conceals contact.

M03 climbs four risers; M04 climbs three then recovers on the landing. Timing/framing and posture were deliberately changed along with the solver, so the side-by-side is not a solver-only ablation. Both play five seconds at their actual speed.

## Numerical validation

Units: metres in source/Blender, millimetres below. The character's thigh and shin are each 370mm; treads rise 180mm. At the final 3.3m vertical orthographic scale, 1mm is approximately 0.582 pixels. Tolerances are engineering thresholds for this proof, not industry certification or artistic approval.

| Measurement | Maximum | Allowed |
|---|---:|---:|
| Stance contact drift | 0.359807mm | 1mm |
| Foot-to-tread contact distance | 0.359386mm | 1mm |
| Limb length variation | 0.000435mm | 0.1mm |
| Connected bone gap | 0.000300mm | 0.1mm |
| Root key-limit discontinuity residual | 0.000200mm | 0.01mm |
| Sampled shoe/stair penetration | 0.001967mm | 1mm |

The 18.972mm maximum root displacement per rendered frame is normal continuous movement, not a teleportation measurement. The root discontinuity check compares positions just before/after each key (±0.00001s), subtracting expected continuous displacement from evaluated velocity. Peak speed is 0.570m/s and acceleration 1.939m/s². These checks cannot certify all possible subframe behaviour.

Contact/bone data are independently sampled after Blender constraints at 120Hz (601 samples). FLAT contact uses the actual four sole vertices; TOE uses the two front sole vertices anchored to that stance. Intended heel lift during toe-off is not classified as sliding. The near-flat threshold permits the reported 0.36mm movement; no zero-drift claim is made. Treads come from the exported staircase mesh surfaces, not a duplicate stair-height formula. All rendered frames additionally check mesh vertices and shoe-profile/riser-edge intersections. The edge check found a 4.72mm toe clip in an internal attempt; the final clearance curve corrects it and reports zero edge/riser penetration, with the 0.001967mm vertex residue still reported separately.

See VALIDATION_R06.json, CONTACTS_R06.csv and POSE_CHECKS_R06.json. Maximum native IK target error is 0.006979mm; knee flexion is 18.86–96.34 degrees. No backward knee direction was measured. Numeric tolerances pass, visual approval is pending.

## Playback and visual review

A low-resolution preview was played at normal and half speed before final export. Full-resolution clean and diagnostic exports fully decode with FFmpeg: 150 frames each, 1080×1920, 30fps, H.264. Final Chromium playback reaches the end at 1× and 0.5×, with no corrupt frames. The normal-speed browser run reports two dropped presentation frames; half-speed reports zero. These are local browser presentation statistics, not missing encoded frames. All 150 encoded frames exist. Captured playback sheets and five diagnostic contact sheets expose the full action. The clean strip and consecutive contact frames were inspected after the clearance correction.

## Remaining artistic and system limitations

This is still stylized authored kinematics: pelvis mass transfer is posed, not a solved centre-of-mass force balance. The proof has restrained arm swing and expression; nuanced acting, handrail interaction and hallway continuation are not established. The garment is a simple weighted mesh; no cloth simulation or full-body collision solver exists. The approved face remains illustrated vector artwork on a head-bound plane, not a volumetric facial rig. Mesh checks are sampled and cannot prove every continuous collision case. The simple lit staircase setting prioritizes readable contact over finished film cinematography. All clips are silent; sound synchronization is not validated here.

Only staircase is repaired. The other four rejected shots need shot-specific grip, prop and motion work after visual approval. No full film was started. Previous production files are checked by hash and preserved. Do not interpret this report as automatic artistic approval.
