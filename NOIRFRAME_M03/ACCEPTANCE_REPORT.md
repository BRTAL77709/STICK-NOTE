# M03 criterion assessment

Overall: **NEEDS REVIEW** for every test. No artistic approval is granted. PASS below means only a bounded measured check, never a production-quality rating.

| Test | Fixed bone lengths | Planted toe drift | Sampled penetration | Prop surface error | Artistic weight/readability |
|---|---|---|---|---|---|
| STAIRS | 2.78e-16 m | 1.11e-16 m | shoe 0 m / body 0 m | 0 m | NEEDS REVIEW |
| KEY_DOOR | 2.22e-16 m | 0 m | shoe 0 m / body 0.0007989 m | 3.03e-16 m | NEEDS REVIEW |
| STEERING | 1.53e-16 m | 0 m | shoe 0 m / body 0 m | 1.39e-16 m | NEEDS REVIEW |
| CHASE | 1.53e-16 m | 0 m | shoe 0 m / body 0 m | 1.39e-16 m | NEEDS REVIEW |
| CURTAIN | 5.07e-16 m | 0 m | shoe 0 m / body 0 m | 0 m | NEEDS REVIEW |

| Acceptance criterion | Assessment and evidence |
|---|---|
| Foot sliding while planted | PASS for measured toe/heel anchors; visual sole compression is not simulated. |
| Hands detached from props | PASS for modeled phalanges/prop surfaces; full palm/skin collision NEEDS REVIEW. |
| Key entering the lock | PASS for axial alignment and full-length key geometry entering the slotted cylinder; read the uninterrupted close-up. |
| Door hinge | PASS for fixed pivot/parent frames. Leaf begins opening after the modeled unlock. |
| Character through solid geometry | NEEDS REVIEW: conservative sampled body/door overlap about 0.8mm remains; no watertight full-body collision guarantee. |
| Vehicle steering causes trajectory | PASS for straight/right/left integration tests; tire friction is not modeled. |
| Road perspective and camera continuity | NEEDS REVIEW; fixed-world route and shared transforms are supplied, not an artistic certification. |
| Curtain moves before grip | PASS for timing: pull begins after contact; complete hand/cloth self-collision NEEDS REVIEW. |
| Floating / teleporting / joint flips | Fixed lengths and continuous positions are checked. Kinematic peak motion is reported in FRAME_FRESHNESS.json; visible weight, pace and head construction NEED REVIEW. |
| Camera hides interactions | NEEDS REVIEW in full-resolution clean/diagnostic playback; close-up and side-view proofs are supplied. |
| Static illustration / reused rejected render | PASS for fresh-source pipeline and source-edit sensitivity; no old MP4 enters corrected rendering. Old footage appears only in explicitly labeled comparisons. |
| General volumetric skin/cloth collision | FAIL — not implemented as a general-purpose solver. Controlled surface/arc checks do not replace it. |
| Audio synchronization | NOT TESTED; these motion proofs are silent. |

The deeper door-route knee bend, rapid stair foot swing, simplified fabric/hand silhouette and drawn head representation remain artistic limitations. See REMAINING_DEFECTS.md. Do not integrate all 18 scenes or render the full film on these numeric results.
