# V10 quality log — awaiting user review

Goal: fix V9's apparent bumper-standing and unstable loading, preserving the existing illustrated assets/renderer and closed-before-turn order.

## Implemented corrections

1. Introduced one orthographic world for pavement, soles, articulated joints, sedan, opening and hinged lid. Camera angle is three-quarter rear; both actors remain on pavement beside/behind the car.
2. Rebuilt the victim path as a limited90° supported roll, upward lift, horizontal advance with delayed legs, then descent into the opening. No opacity fade or rigid full-body translation is used.
3. Added deterministic three-dimensional two-bone IK with the prior rig's limb lengths. A preferred knee-plane instability was found during development and corrected before the review render.
4. Reach checks caught opening before C01's approach step, and C02's hands getting ahead of his loading steps. Corrected timing and support positions; no arm stretching was substituted.
5. Rendered low-resolution previews and inspected actual normal-speed playback. The first side-wall solution left a protrusion after closure; restaged the final body inside the opening and added the opening-derived visibility corridor.
6. Encoded review exposed the raised lid covering the victim too early during insertion. Corrected its depth order; it stays behind the body while raised and occludes the cavity during closure.
7. A rear-plane contact audit found straight withdrawal paths below the sill. Raised the loading shoulder poses, routed elbows above the opening and used up-and-out release/reach arcs. Added zero-below-sill-crossing verification. The first full-resolution world draft is preserved locally.
8. Kept planted feet fixed throughout the lift. Loading steps use separate explicit schedules; a short knee compression during C02's step maintains reach without foot sliding.
9. Produced world debug frames, encoded0.1s action detail, actual stance-foot strips, an eyes-hidden head test, metadata/decode reports and V9/V10 comparison artifacts.

## Remaining artistic weaknesses

- C02's one-person supporting crouch is still strongly stylized.
- Hands/fingers and cloth have limited deformation, and some regrip silhouettes overlap.
- Whole-body mass balance is authored rather than dynamically solved; the visibility solution is 2.5D.

No score of10/10 and no claim of artistic approval. Production cost:$0 additional. V1–V9 preserved. Stop after V10; the86-second full film has not started.
