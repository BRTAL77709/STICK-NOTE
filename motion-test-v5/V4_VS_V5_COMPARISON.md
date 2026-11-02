# Actual V4 versus V5 comparison

Compared the existing V4 MP4 with the newly encoded V5 MP4 at matching times, using a side-by-side comparison encode, extracted frames and the V5 normal-speed playback/pose checks. No quality score is assigned.

| Item | V4 | V5 |
|---|---|---|
| Victim legs | The bend and nearly upright shins can read as stepping | Both knees now stay ahead of the trailing ankles; both heels share one grounded passive trajectory, with no alternating leg phase or lift |
| Weight/anticipation | Pull begins at 0.2 s; limited preparation | 0–0.45 s establish, 0.45–0.90 s bracing/compression, then pull and 2.70–3.20 s deceleration; pelvis shifts with support transfer |
| Locomotion | Criminal feet use synchronized phases | Criminal 02 has a 0.12-cycle offset; support patterns differ across 32 of the 150 poses |
| Travel | 320 world units | 300 world units, still more than a full posed-character width; reduced slightly to accommodate the longer anticipation and larger stride |
| Grips | Geometrically attached but visually weak dark ellipses | Same stable upper-arm constraints, with sleeve-wrapping finger/cuff details and local highlights |
| Foot/hand readability | Dark planes merge | Brighter local limb rims, soles, glove edges and heel-contact shadows; global exposure/palette unchanged |
| Head turn | Cap seam, eye position and modest silhouette change | Coupled head width, projected cap bill/crown, face-plane alignment, mask chin and neck change from three-quarter to front |
| Frontal stare | Narrowed-eye hold | Preserved frontal hold after 4.5 s, with the same cap/mask/hoodie identity and restrained breathing |
| Camera | Frame-96 cut to close-up | Preserved exact cut, two-shot structure, lateral track and restrained close-up push |

## Verified details

V5: 300-unit root travel; fixed planted feet; heels stay at ground heights 1413/1418, with constant 30-unit spacing; knees remain at least 68.93 units ahead of the dragging ankle. Maximum upper-arm contact error is floating-point noise. All measured bone-length variation is below 0.02 SVG units, attributable to 0.01-unit coordinate formatting.

The actual final V5 MP4 played at 1× to completion with 150 frames, zero dropped/corrupted frames. The contact sheet samples dragging at about 0.2 s and rotation at about 0.1 s, including adjacent frames 95/96. The comparison MP4 uses V5 audio and has decoded without errors.

## Remaining weaknesses

The acting is still stylized and constraint-driven. Shoulder loading and cloth movement are simplified; some forearm poses remain diagrammatic. The head turn is a designed 2D/2.5D orientation rig, not a full volumetric head model. Dark staging and overlapping limbs may still benefit from user review on a phone. There is no claim of professional/reference-level equivalence or of subjective audio listening QA. The user's review remains the approval gate.
