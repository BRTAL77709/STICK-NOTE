# M04 source-level proof — exact rejected M03 exports

All five M03 clean previews are rejected for final production. This is an implementation audit, not an artistic approval. `reports/M03_SOURCE_PROVENANCE.json` confirms each exact MP4 matches its recorded export hash and compares its source snapshot with the delivered C02/C03 source archive. The C03 archive's later `qa.py` differs from the version captured when rendering; movement-source hashes match. The C02 movement sources match their archive. No Blender rig generated these five MP4s.

## Shared rendering/rig reality

Actual path: `render.py:55–74` → `shots.py` dispatch → controller `state(t)` → analytic `contact_rig.pose` and `rig.ik` → `actor.actor` geometry → `depth_render.DepthRaster` → RGB pipe → FFmpeg. `rig.ik:14–21` really is a fixed-length analytic two-bone IK calculation. It checks reach and a broad bend-angle range. It is not a physics engine or a general anatomical constraint solver. The `hierarchy` dictionary at `contact_rig.py:22` describes coordinate relationships; it is not a native armature, skin modifier or collision system.

`actor.py:9,24–31` reconstructs tubes/sleeve quadrilaterals and a shallow box-like hoodie from joint coordinates each frame. It has no common skinned garment mesh. `actor.py:35–38` draws a camera-facing head glyph at a single depth, and `head_view.py:4–6` changes its drawn appearance. This explains possible sleeve/face occlusion errors. Smooth root acceleration does not resolve those silhouette/posing limitations.

## 1. STAIRS_M03_C03

**Truly constrained:** `contact_rig.pose:19` calls `rig.ik` for each leg with fixed .37m segments. `stair_test.PLANS/INIT` keep stance sole coordinates constant. `foot_geometry:45–50` derives ankle/toe-pivot geometry. `stabilize.prepare` preserves those endpoints while rebuilding knees after its root adjustment.

**Authored rather than simulated:** `stair_test.py` supplies exact touchdown coordinates, swing windows, PRESSURE and HEIGHT arrays, torso pitch/roll/twist keys and wrist offsets. `contact_rig.step:29–36` supplies a prescribed rising arc. `stabilize.prepare` filters root X/Z and fits root Y within reach bounds. It optimizes a kinematic path; it does not solve body forces, balance recovery, joint torque or contact impulses. The LIPM-inspired horizontal preview is not a full-body dynamics simulation.

**Confirmed prototype causes:** the initial root is low relative to the .74m total leg length (the measured initial knee flexion is in `M03_INITIAL_STAIR_POSE.json`). Fixed early vertical lift and clearance can lift a swing foot higher than needed. Wrists are eased relative to the root, with elbows solved toward them, rather than naturally swinging shoulder/elbow joints. There is no independently constrained gaze/head bone. Root smoothing preserved the basic authored posing and timing; it could not make them natural by itself.

**QA limitation:** `qa.py:17–27` compares constructed toe points and shoe profile samples against a stair-height formula. It does not measure an independently evaluated skinned shoe against the actual staircase mesh. Its tiny drift values are useful coordinate checks, not evidence of convincing load transfer.

## 2. KEY_DOOR_M03_C03

**Truly constrained:** `key_test.state:17,25,29–39` derives key/lock/handle locations from a shared door hinge matrix; wrists and two simplified fingertips target prop surfaces. Arms use the same analytic two-bone IK. The blade is a full .16m mesh and the cylinder slot is an opening in `shots.door_geometry:24–46`.

**Authored:** `door_angle`, `heading`, `root_path`, SCHEDULE, insertion/turn/depth and grip-switch times are prescribed curves (`key_test.py:6–40`, `locomotion.ground_feet:3–14`). `stabilize` smooths the root and applies timed attachment weights; the door does not respond to hand force. Unlocking is a time flag, not a latch/lock mechanism simulation.

**Visually approximated:** palms are ellipses and the fingers are two short chains. Blade occlusion is depth rendering, not metal/key contact mechanics. Body/door collision is sampled spheres; complete palm, arm, garment and head collisions are absent. The cut label switches at 8.55s while the actual camera changes at 8.30s (`shots.py:59–62`), a confirmed metadata inconsistency. The underlying manually routed entry is not a general locomotion controller.

**Limit:** improving curve smoothness alone does not fix grip silhouette, coordinated reach/regrip, collision-free anatomical posing or natural walking around the leaf.

## 3. STEERING_M03_C02

**Genuine integration:** `vehicle_dynamics.advance:7–8` integrates rear-axle position, heading and speed from commanded steering and acceleration at 120Hz. `simulate:10–18` derives individual wheel travel and damped body pitch/roll. These are real kinematic/spring calculations, not merely a rotating wheel over an independently scrolling image.

**Genuine geometric attachment:** `vehicle_test.state:10–15` uses the same wheel matrix for the rim and hand targets; arms/fingers use analytic IK. `foot_on_pedal:6–7` geometrically places the toe on the pedal plane while anchoring the heel.

**Authored/approximated:** throttle, brake, steering, head/torso reactions and foot transfer times are scripted (`vehicle_dynamics:5–6`, `vehicle_test:17–25`). Pedal animation follows the control value; it does not mechanically generate engine torque. No tyre friction, steering effort, suspension geometry, driver muscle dynamics or body collision solver exists. `shots.cabin` reconstructs boxes/tubes; the mirror is a small projective rendering, not a physical mirror.

**Limit:** coherent matrices do not by themselves make seating, wheel grasp, pedal reach or acting convincing. The old character representation remains the same shared procedural body.

## 4. CURTAIN_M03_C02

**Genuine geometric constraint:** `curtain_test.fabric:5–16` binary-searches a sine-fold amplitude to preserve each row's horizontal polyline arc length. `state:18–20` takes a mesh-edge vertex as the hand target and solves the arm/fingers toward it.

**Authored/visually approximated:** curtain width, pull timing, row delay and decaying oscillation are explicit formulas. The mesh edge drives the hand target. There is no two-way hand/fabric tension, gravity/cloth integration, vertical strain solve or self-collision. Fear, recoil and head turn are eased pose parameters. This is a controlled procedural fold rig, not a cloth simulation.

**Limit:** preserving horizontal material length cannot establish fabric weight, local grip deformation or a natural release. The head remains a drawn glyph; a convincing reaction needs posing as well as parameter changes.

## 5. CHASE_M03_C02

**Genuine integration:** the witness uses the bicycle model above. The pursuer has its own integrated rear-axle state and a lookahead steering controller (`vehicle_dynamics:24–31`); the gap is not just an animated number. The world camera in `shots.chase:131–132` follows the actual pair midpoint.

**Authored/approximated:** speed-controller gains and desired separation are scripted. The road is sampled once from the witness's planned simulation (`vehicle_dynamics:21–23`); this is a fixed scene during playback, but not an independently authored street with arbitrary off-route driving. Car bodies are rigid meshes transformed by the state. Pitch/roll are approximate spring responses, not full chassis/tyre dynamics. `shots.vehicle_pair:111` uses the witness's brake flag for both cars' lamps, despite separate longitudinal controllers. Headlight footprints are flat polygons.

**Limit:** no collision, tyre slip, true load transfer, independent pursuer brake-light channel or full editorial route/arrival solution. A moving chase camera can establish travel without making the driver/vehicle acting cinematic.

## M04 replacement boundary

Only the staircase is rebuilt. Replace M03's per-frame procedural character pose generator with an actual Blender armature, native two-bone leg IK, connected bones, fixed world-space foot controls, rigid shoe binding and skinned hoodie/limb meshes. Use authored support-relative key poses and FK arm counter-swing, with a real head-orientation constraint. Measure evaluated bones and shoe vertices after Blender constraints, not copied target values. Retain the approved illustrated head/palette and the free illustrated output renderer. No full-body dynamics or muscle simulation will be claimed. Other four shots remain untouched until the staircase passes user visual review.
