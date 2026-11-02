# V9 action-order validation

The absolute-time deterministic state function and head-time guard are defined in src/render_test_v9.py. src/audit_v9.py checks all 300 poses. The observed state sequence matches the required sequence with zero head-before-closure violations.

| Start | State / verification |
|---|---|
| 0.00 | DRAGGING — passive victim shoes, asynchronous criminal foot plans |
| 1.40 | TRUNK_OPENING — support handoff precedes C01 opening reach |
| 2.30 | REPOSITIONING — hands move to upper arm/back, waist and knee supports |
| 3.00 | LIFTING — feet planted, knees/hips extend; victim follows continuous articulated arc |
| 4.60 | LOADING — feet are 206/217 units above their original pavement anchors; fold then descend into cavity |
| 6.20 | RELEASING — complete depth entry reached before hands start withdrawal |
| 6.70 | TRUNK_CLOSING — all four withdrawn hand centers at y=1338; glove tops at1321, below the sill at1312.5 |
| 6.95 | C02's closing hand contacts the actual lid material point; downward rotation starts |
| 7.50 | TRUNK_CLOSED — angle exactly0°, frame225; distinct original latch click begins at7.50s; hand releases lid and retreats |
| 7.75 | WITNESS_NOTICED — C01 shoulder/posture reaction begins after closure |
| 8.00 | HEAD_TURNING — cut to close-up only now; guard requires lid angle0° |
| 9.20 | THREATENING_STARE — front-facing turn complete; eyelids narrow, then hold |

The lid decelerates to zero angular speed at7.5s. The body/cavity geometry does not toggle visibility; a rotating solid panel covers the cavity. Raster ablation at7.5 and7.8s shows **zero changed pixels** if only the victim drawing is removed. At6.7s, removing him changes4884 half-resolution pixels. This confirms that the body remains in the scene and is naturally hidden by closure.

During6.95–7.5s maximum modeled closing hand-to-lid separation is0. The same rigid trapezoid, hinge and uniform sedan transform are used for opening and closing. The hand is drawn on the exterior panel surface at closure, then withdraws by7.75s. The other hands remain below the mouth.

HEAD_TURNING cannot begin at any absolute time before8s, and its geometry guard additionally requires TRUNK_CLOSED (angle0°). Rendering frames in a different order does not change these states. See action-order-validation.json, occlusion-verification.json, assets/sound-events.json locally and the delivered decoded contact sheet.
