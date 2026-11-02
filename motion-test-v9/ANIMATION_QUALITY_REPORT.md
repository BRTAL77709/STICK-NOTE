# V9 animation quality report — review pending

## Implementation relative to V8

The existing rigs, illustrated hoodie/cap/knit-cap characters, injured victim, alley and local SVG/librsvg renderer are reused. V8 is bundled byte-for-byte in src/v8_engine.py. The active V9 easing changes to quintic smoothstep and its monotonic PCHIP action clock makes the lift/load timing continuous. The head projection geometry is retained; a separate time adapter schedules rotation8–9.2s and narrowing9.2–9.7s.

The entire sedan uses one constant75% scale and translation, bringing the raised lid within the existing177-unit arm reach. This restages the approved black sedan without stretching limbs or changing its geometry during the shot. The victim descends into the transformed opening along a continuous170-unit loading arc. Inside/outside parts share one pose and near-sill holdout; no victim opacity fade is used.

Removed V8's small discontinuous stance-centroid hip correction. Extended the lower-leg fold interval after the first retiming made it too quick. Both criminals now withdraw hands below the sill; C02 then reaches the lid, tracks one fixed material point through closure and withdraws after latching. A smooth surface-color change reveals the closed metal deck instead of leaving it visually indistinguishable from the dark cavity.

## Pose checks across300 frames

- Maximum world-space stance movement:0. Every criminal has at least one supporting foot at every checked frame.
- Maximum criminal shoulder-to-hand reach:172.057 units, below177. Strict two-bone IK raises on unreachable targets.
- Named support gap during the established lift/load contacts:0. Regrips are deliberate traversals before support engagement.
- Closing hand-to-lid gap:0 during6.95–7.5s.
- Maximum rounded SVG segment-length variation after removing depth scale:0.023653 units. Criminal leg/arm lengths and victim leg lengths remain fixed in model space.
- Sampled victim marker maximum frame displacement:16.811 units versus19.290 in the independently imported original V8. This is a continuity diagnostic, not an artistic quality score.
- Maximum marker difference across±10 microseconds of authored state/clock boundaries:0.014974 units. No finite pose discontinuity was found at those boundaries.
- Victim feet remain passive; there is no walking gait. At4.6s ankle/shoe anchors clear their original pavement heights by205.98/216.67 units.
- The open body remains visible at6.7s, then is fully occluded by the closed lid at7.5s. The head stays at72° yaw before8s; narrowing remains zero before9.2s.

## Rendering and review

Complete low-resolution previews were rendered and played at1×. The corrected preview presented300 frames with zero drops/corruptions. Inspected key poses, actual presented-frame sequences, 0.1s encoded loading/closing detail, stance-foot strips and head-turn diagnostics. The first full draft was retained locally after its closed panel proved too similar in shade to the open cavity; the review render uses a smoothly changing metal surface.

FFprobe, final full decode, black-frame detection and final/comparison browser playback results are in encoding-verification.json, encoded-visual-verification.json and playback-verification.json. No encoded blank interval is acceptable. The intended cut is frame240 (8s); other camera motion remains restrained.

## Remaining artistic limits

The crouch is still exaggerated, especially C02's initial one-person support. Limbs overlap tightly while the victim is rolled horizontal, and finger compression is economical. The interaction is authored deterministic IK with phase-lagged torso/head/legs, not a full mass/collision simulation. The 2.5D entry holdouts are visually inspected but cannot certify every anatomical overlap as collision-free. No claim of exceptional quality,10/10 or user approval is made.

V9 fixes the action order and adds an explicit, reachable complete closure. Whether the weight and choreography now read convincingly remains for user review.

## Final encoded results

FFprobe confirms10.000000 seconds,300 video frames,1080×1920,30/1 FPS,H.264 and AAC audio. Final size:4,046,841 bytes. Full FFmpeg decode completed with no errors and no detected black intervals. Final MP4 and comparison each played at1× with300 frames,zero drops and zero corruptions. Original rain/cues peak at−8.5 dB; the frame225 latch event is recorded in the delivered sound-events JSON. The largest noncut decoded frame change is2.453 mean RGB units versus13.748 for the intended frame240 cut; these statistics supplement visual inspection and do not prove absence of every local artifact.
