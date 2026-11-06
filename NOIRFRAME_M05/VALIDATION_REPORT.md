# M05 numerical validation and M04 regression report

The unchanged M04 validation script measures Blender-evaluated bones and shoe vertices, not just desired target coordinates. Native data use metres/seconds; the table converts lengths to millimetres. One millimetre is about 0.516 pixels in the final 3.72m vertical orthographic frame. Tolerances are engineering thresholds for the proof, not artistic certification.

| Measurement | M04 maximum mm | M05 maximum mm | Change mm | Allowed mm |
|---|---:|---:|---:|---:|
| Stance contact drift | 0.359807298 | 0.360045435 | +0.000238138 | 1 |
| Foot-to-tread contact distance | 0.359386206 | 0.359266996 | -0.000119209 | 1 |
| Limb length variation | 0.000434623 | 0.000433200 | -0.000001424 | 0.1 |
| Connected bone gap | 0.000299510 | 0.000337915 | +0.000038405 | 0.1 |
| Sampled mesh/stair penetration | 0.001966953 | 0.002264977 | +0.000298023 | 1 |
| Edge/riser penetration | 0.000000000 | 0.000000000 | +0.000000000 | 1 |
| Root key-limit discontinuity residual | 0.000200054 | 0.000176224 | -0.000023830 | 0.01 |

All stated M04 tolerances still pass. The small increases in stance drift, connected bone gap and sampled penetration are explicitly reported, not rounded away as zero. The edge/riser check remains zero. There is no material contact regression at this scale, but numerical pass does not establish artistic quality.

Sampling: 601 evaluated poses at 120Hz for contacts, bones and root; all 150 rendered frames at 30Hz for body mesh/stair vertex and edge tests. Stance FLAT uses four actual sole vertices; TOE uses the two actual front sole vertices. Heel rise during toe-off is intentional pivoting. The same 0.002rad near-flat classification threshold accounts for the approximately 0.36mm contact drift. Tread bounds come from the actual unchanged native stair meshes.

Root discontinuity residual uses actual positions just before/after every root key (±0.00001s), minus expected continuous movement estimated from evaluated velocity. Maximum normal frame displacement is 18.835mm, below the unchanged 35mm sanity bound; that ordinary displacement is not called teleportation. Maximum native IK target error is approximately 0.0068mm. Peak root speed is 0.5656m/s. Added anticipation and landing settles raise peak authored root acceleration from 1.9394 to 3.6994m/s²; balance forces and joint torques are not simulated.

Native retention: NATIVE_INHERITANCE.json hashes actual native rest bones/limits, all character mesh/skin data and ankle/foot-orientation/knee-pole curves. M04 and M05 hashes match. RIG_RETENTION.json separately records unchanged constraint definitions and targets. FOOT_PLAN_PRESERVATION.json confirms every foot target and contact schedule entry is identical. The original validate.py itself is byte-identical to M04.

Reopening the delivered native .blend gives zero vertex difference against the exported cache for 576 checked shoe/hoodie/head vertices at six times. Both native leg IK constraints remain two-bone with no stretch. The head image is packed. Moving camera projection agrees with Blender to within 0.000172px. All evaluated shoe vertices stay inside both cinematic and diagnostic frames; FOOT_FRAMING.json checks bounds, not visibility through the shoe's own geometry.

The collision tests are sampled stair checks, not a universal continuous full-body collision solver. Measurements are not a claim that every hidden body part or environmental interaction is physically simulated. See VALIDATION_F01.json, CONTACTS_F01.csv, M04_M05_REGRESSION.json and NATIVE_REOPEN_VERIFICATION.json for unrounded results.
