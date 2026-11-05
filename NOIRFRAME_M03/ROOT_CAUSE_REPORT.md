# M03 forensic investigation

M01 is rejected. M02 was not found in the local project or the recursive remote `work` tree. Local branch is `work`; remote head at inspection: `8f195d04b7dd62302dbd46ffdcf44170ba271b0e`. Earlier local production directories are untracked relative to the old checkout; no reset, checkout, clone or cleanup is performed.

## Actual pipeline

M01 `source/render_tests.py` → `shots.SHOTS` → per-shot `state(time)` → `contact_rig.pose`/two-bone `rig.ik` → `actor.actor` + world geometry → `World.ops` → `DepthRaster.render` → streamed RGB frames → FFmpeg/libx264 → MP4. Procedural 3D coordinates with illustrated flat polygon surfaces, camera-space projected tubes and SVG head/palm glyphs. Not Blender, Remotion, sprite footage or a static SVG image slideshow. Units metres, Y up, +Z character forward before yaw. Cameras explicitly project world coordinates. Approved head is drawn in camera-facing SVG with yaw supplied independently.

The background cache stores a static color/depth prefix inside a raster instance, keyed by shot string. Each render starts a fresh process/raster. No MP4 input is used to generate corrected character frames. M03 will disable background caching until source-sensitivity checks pass. Old MP4s are used only in labeled comparisons.

| ID / symptom | Inspected implementation and confirmed cause | Proposed correction / validation | Status at investigation |
|---|---|---|---|
| A1 / insufficient climb proof | M01 `stair_test.PLANS`: one last-riser step followed by landing/hall targets. Three seconds cannot prove three consecutive risers. | New tread-indexed schedule over four risers, side view, all-joint/contact markers and tread measurements. | Confirmed scope defect; replace controller |
| A2 / body weight can look stiff despite IK | M01 `stair_test.state` solves COM X/Z but Y comes from an independent HEIGHT list; torso/arm motion largely individually eased. Numerical COM tracking alone does not establish visual effort. | Contact-phase pose keys, explicit anticipation/load transfer, inspect normal speed and support changes. | Confirmed architecture; artistic cause remains to review |
| A3 / planted check omits some solids | M01 `validate.check` tests shoe profile against a stair height formula, not swept knees/body/rail/ceiling volumes. | Explicit stair solids and joint/capsule clearance checks; report coverage limits. | Confirmed QA gap |
| R1 / joint limits/pole stability | M01 `rig.ik` checks reach but has no angular limits; default knee pole is world +X even when heading changes unless caller overrides. | Heading-relative poles, near-singularity rejection, fixed bone lengths and temporal joint checks. | Confirmed missing safeguard; no assertion that every old shot flips |
| R2 / billboard head can contradict camera | `actor.actor` projects a head center then draws an SVG; yaw/tilt are supplied separately from body/camera. | Derive view-relative yaw, keep approved drawing geometry, test side/front views. | Confirmed independence; fix view interpretation |
| B1 / incomplete key choreography | M01 `key_test.state`: no withdrawal channel; key is retained throughout; door maximum is 9°. | Explicit align/insert/rotate/return/withdraw/regrip/lever/open phases, continuous close-up. | Confirmed missing actions |
| B2 / blade disappears at the plate | M01 `shots.key` clips visible blade length at `FACE`; no cylinder interior/slot occlusion mesh. Clipping can conceal penetration rather than prove insertion. | Model a true dark slot with a matching blade and contact axes; keep key length invariant and track insertion depth. | Confirmed rendering shortcut |
| B3 / tiny grip/readability | Finger surface markers are constrained, but camera-facing palm glyph and fine fingers can visually merge into the prop. `actor.palm` is a flat ellipse. | Readable mitten/thumb grip silhouette attached to wrist and prop; render close contact detail. | Confirmed representation limit; inspect result |
| C1 / steering not causal | M01 `vehicle_test.RUN`: road curvature(s) gives steering via atan(WB*k); position/yaw are interpolated from ROAD. The route drives the wheel, rather than steering driving the trajectory. | Integrate rear-axle bicycle state from steering/throttle/brake at fixed dt; compare speed, heading and wheel phase. | Confirmed reverse causality |
| C2 / driver split-view proof is not clean shot | `shots.driving` stacks a local cockpit and overhead world camera, while transformation of glyph callbacks differs from transformed world op vertices. It is diagnostic framing, not a finished cinematic shot. | One authoritative local-to-world transform and separate clean/diagnostic renders; verify camera projections. | Confirmed representation risk; glyph mismatch requires projection test |
| D1 / world-space city already exists | M01 `geometry.city` uses fixed buildings and road vertices, then bends X by road_x(Z). It is not one scrolling illustration. | Preserve fixed-world geometry; build road from the new integrated reference route, documented map, no time-dependent scenery origins. | Confirmed capability; not a scrolling-background bug |
| E1 / curtain not repaired in M01 | No curtain controller or curtain render exists in M01. V12 bedroom remains rejected. | New pinned-top inextensible fold strip, edge/hand anchor, delayed settle and reaction. | Confirmed missing subsystem |
| QA1 / numerical checks called passes | Old `bounded_checks_pass` intentionally covers only sampled point geometry. It cannot prove cloth, volumetric grip, acting or full entry. | Separate numeric PASS, visible FAIL and NEEDS REVIEW; no artistic autoapproval. | Confirmed coverage limitation |

## Architecture decision

Keep the free Python/NumPy depth renderer and approved head asset: they support hierarchical coordinates, two-bone articulation, object parenting and depth-tested contacts. Replace per-shot controllers and add a shared explicit rig contract. For a controlled curtain pull use an arc-length-preserving fabric fold rig, not a rigid blind or rigid translate. Blender 4.3.2 is installed, but importing another renderer alone would not repair contact choreography. General cloth/body collision and full skin deformation remain outside this renderer; if the controlled fabric/hand geometry fails review, migrate that subsystem to Blender armature/cloth constraints rather than disguise it with camera motion.

## Asset/dependency verification

`reports/ENVIRONMENT.json` records actual installed executables and libraries. Approved head, ink renderer and sedan source are copied locally into M03. No external image downloads or APIs are required. Source hashes, frame-state hashes and render freshness checks will accompany every corrected export. All earlier M01/V12/V10 files have a protection manifest. No old render will be presented as M03.

## Observations confirmed during M03 implementation

- Initial M03 trial put the trailing foot too far back, producing a .95m first swing. Corrected initial stance reduces it to .59m. This was a controller error, not a rendering defect.
- A diagonal direct path behind an 80° open door crossed its solid leaf; sampled head/body overlap reached .26m. Routing around the free edge reduced the sampled residual to approximately .8mm. Opening/closing timing was extended to fifteen seconds instead of concealing this route with cuts.
- The exterior vehicle camera's initial lateral offset entered a building during a turn. Revised camera offsets remain in the road corridor in inspected frames.
- The first reconstructed rear-head implementation had a hard front/back branch. Consecutive frames exposed a view switch. `head_25d.py` replaces it with continuous cap contour/brim parameters and face-feature visibility. The approved asset file remains unchanged; drawn-head volumetric limitations remain.
- `SOURCE_EDIT_RENDER_PROOF.json` confirms source sensitivity with separate source copies and processes. No evidence of unintentionally reused old MP4 frames was found in the new render path.

Fix status is conditional on final exported-state checks and visual review. See the final acceptance report; none of these observations grants user approval.

## Confirmed body-trajectory defect and correction

Final-state differentiation exposed peak pelvis acceleration of 42.02 m/s² in stairs and 33.26 m/s² in the door controller. Inspection traced this to frame-local `min(requested_height, reach_cap)` and separately compensated horizontal body movement. This is a confirmed controller/root-motion defect despite stationary foot markers. `stabilize.py` now solves a predictive bounded trajectory and reconstructs IK without moving contacts. Preflight differentiation measured 2.11 and 3.55 m/s² after this correction, respectively. Final C03-state measurements and the trajectory plot are supplied. No force/biomechanical certification is implied.

## Current status by defect ID

| ID | Current status / evidence |
|---|---|
| A1 | Implemented: four risers and landing, side view and every-frame contact sheets. |
| A2 | Predictive body trajectory replaces the sharp clamp; acceleration measured before/after. Natural acting still NEEDS REVIEW. |
| A3 | Sampled sole/leg/door/body checks expanded; general swept-mesh collision remains unimplemented. |
| R1 | Heading-relative bend planes and fixed-length/angle checks implemented. Full anatomical limits remain simplified. |
| R2 | Continuous view-relative cap construction implemented; glyph depth and sleeve/head overlap remain limitations. |
| B1 | Full insertion/return/withdrawal/regrip/open/entry/close implemented over 15 seconds. |
| B2 | Full key mesh and actual slot/cylinder opening implemented; no blade scaling/clipping shortcut. |
| B3 | Modeled finger contacts checked; complete palm/skin volumes remain NEEDS REVIEW. |
| C1 | Causal bicycle integration replaces path-interpolated motion; independent left/right/straight checks provided. |
| C2 | Separate clean/diagnostic exports; exterior diagnostic grip projections corrected to the displayed coordinate frame. |
| D1 | Fixed-world street retained with documented route/local house frames; complete film route not rendered. |
| E1 | Controlled material-length-preserving fold rig implemented; no general cloth simulation/collision guarantee. |
| QA1 | Numeric evidence, playback drops and artistic review are separated; no user approval claimed. |
