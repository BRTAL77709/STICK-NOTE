# M03 technical and artistic assessment

The rejected M01 files were traced to their real Python controllers and depth renderer. No M02 exists in the inspected local/remote tree. `ROOT_CAUSE_REPORT.md` records confirmed implementation defects separately from suspected artistic causes. No full-film render or integration is authorized by these tests.

## Delivered scope

- A: five seconds, four .18m risers and an upper landing, fixed side view. Targets, actual joint chains, support states, tread indices and pelvis trajectory are shown in the separate diagnostic.
- B: fifteen seconds. The requested six seconds was extended to fit approach, pocket retrieval, uninterrupted alignment/insertion/rotation/return/withdrawal, stow/regrip, opening, walking around the open leaf, inside regrip and closing. The long route is deliberate: earlier direct motion intersected the open door. Key, cylinder, hand identity and hinge are the same objects across angles.
- C: six seconds, cockpit steering followed by exterior tyre/trajectory evidence using one authoritative simulation state.
- D: six seconds, two independently integrated cars on the same fixed street with changing separation.
- E: five seconds, contact before pull, material folds, sedan reveal, freeze/recoil and release/settle. The fold rig is controlled geometry, not full cloth simulation.

All clean and diagnostic exports are native 1080×1920 at 30fps, H.264, silent. Comparisons retain the rejected originals at their actual speed. Where M01 ends earlier, the comparison's left panel goes black with an explicit ORIGINAL ENDED label. No looping, retiming or freeze-frame extension is presented as original footage.

## Measured preflight evidence

The stair harness reaches treads 1–4, raised the estimated COM approximately .732m before the predictive repair; the revised stair trajectory raises it approximately .777m and has no sampled shoe or leg penetration at the declared points. Planted toe drift is at floating-point roundoff. These tests preserve .37m leg and .34m arm segments; they do not scale limbs to reach targets.

The sampled conservative body-sphere/door test retains approximately .799mm residual overlap, within the explicitly declared 2mm geometry tolerance. It is not zero volumetric collision. The door-route pelvis initially dropped to about .484m before the predictive trajectory repair, which may still look too crouched. This remains an artistic concern rather than being certified by the numeric label.

Pursuit centre separation decreases from 12.0m to about 7.1m over the six-second samples. Straight, right and left steering were separately integrated and compared to the bicycle heading equation in `VEHICLE_CAUSAL_TESTS.json`. Front tyre direction, per-wheel travel, hands, pedals and acceleration share the controller state.

Curtain material rows retain horizontal arc length to less than 1mm in the sampled fold rig. This does not verify full vertical strain, self-collision or all hand/palm volumes. Exact final numbers come from `CONTACT_QA_FINAL.json`, computed from the states actually exported for the delivered C03 stair/door and C02 vehicle/curtain clips, not from a later live controller.

## Source and render verification

A controlled source edit in an isolated copy changed actual pixels in a fresh renderer (`SOURCE_EDIT_RENDER_PROOF.json`). Corrected frames use no MP4 inputs or stale image caches. Each final export records producer hashes, every frame's exact rig state and source RGB hash, and final MP4 hashes. Compressed JSON is lossless; some own internal preview state files were archived to conserve disk without touching previous productions.

Full FFmpeg decode, exact frame counts and actual Chromium playback are recorded separately. Preview playback completed at normal and half speed; some frames were dropped by the playback environment under concurrent rendering, with zero corrupted-frame reports. The final playback logs retain the actual counts. Technical playback completion is not artistic approval.

## Corrections caught during inspection

An oversized initial stair stride, early toe/riser clipping, unreachable pelvis heights, direct traversal through the open door leaf, a camera crossing a building, indistinct curtain fold shading and an abrupt front/back head-view switch were detected and revised. Partial C01 renders are preserved locally and excluded from delivery. C02 uses continuous view-relative cap construction. Face-detail visibility still uses a drawn representation, not a full volumetric head mesh.

## Coverage limits

See `REMAINING_DEFECTS.md` and the criterion-by-criterion `ACCEPTANCE_REPORT.md`. Geometry PASS labels refer only to the documented sampled tests/tolerances. Composition, emotional acting, weight, grip readability and continuous head silhouette require user review. Sound and 86-second integration remain pending. No 10/10 rating or artistic approval is claimed.

## Predictive root-motion audit

C02 contact checks initially missed implausible pelvis acceleration. Actual exported-state differentiation measured 42.02 m/s² for stairs and 33.26 m/s² for the door. The contact-feasible predictive solver reduced these in preflight to 2.11 and 3.55 m/s², without shifting planted feet or attached grips. Only the stair and door animation are rerendered as C03; the other three keep their C02 animation. The C02 source archive is retained for provenance and the current editable archive includes the new solver. See PELVIS_TRAJECTORY_REPAIR.json and the acceleration plot.
