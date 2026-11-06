# M05 artistic and technical report

## Preserved animation system

This scene starts by opening the actual delivered `NOIRFRAME_M04/assets/STAIRCASE_M04_R06.blend`. No character mesh, armature, rest bone, limb length, native IK constraint, knee pole, skin weight or contact-controller curve was rebuilt. Native equality checks are in NATIVE_INHERITANCE.json. The M04 validation script is retained unchanged. Actual dependency-graph mesh vertices and native camera transforms drive the illustrated renderer.

## Deliberate artistic changes

- The original 0–0.35s pre-step window now has a 12mm anticipatory pelvis dip and 10mm rearward preparation, a brief glance and blink, followed by forward commitment. Contact times remain exact.
- Pelvis and chest counter-rotate in opposite directions. Pelvis/chest lateral roll accompanies support changes. Arm swing rises from about 0.29rad to 0.40rad (approximately 17° to 23°), with phased elbow articulation and a guarded initial pose.
- Forward torso lean builds before the first lift and remains during ascent. The independent head/neck controls stabilize the head while allowing a small look around the interior. The approved vector face uses a more frightened gaze and mouth parameter, preserving its original outline/cap/eyes/artwork implementation.
- Each original touchdown receives a 5mm body settling offset and a smaller recovery. The final support transfer eases onto the landing. There is no extra hallway walking cycle in this five-second proof.
- The exact M04 sole trajectories, toe-off timing, swing paths and stance schedule are unchanged. The coordinated body response improves their presentation; no newly invented foot mechanics are claimed.

## House 17 set and camera

The prototype wall and rail are replaced with an illustrated stairwell shell, ceiling, floorboards, wainscot, base/crown trim, detailed balusters/newels, wood trim, two amber sconces, framed art, a visible landing and an open hallway portal with corridor geometry. All these details are native world-space geometry. The near wall exists as a render-hidden cutaway so it does not block the filming position or feet. This is a stairwell set, not a completed model of the entire house.

Flat cel tones retain the dark navy/teal palette and amber highlights. Planar shoe shadows are derived from evaluated shoe positions and clipped to receiving tread rectangles. They are an illustrated contact-shadow approximation, not a ray-traced global shadow simulation. Floor seams outside the contact zone add depth without raising the physical contact treads. The original stair solids remain unchanged.

The cinematic native camera has a constant 3.72m orthographic scale and a smooth 0.22m lateral / 0.18m upward follow. No zoom, cuts, shake, motion blur or contact masking is used. A separate fixed side diagnostic camera retains the M04 3.3m scale. The illustrated renderer uses the actual native camera basis exported at every rendered frame. Orthographic depth interpolation was corrected to linear depth, matching its projection.

## Verification and comparisons

A 540px preview was played at 1× and 0.5× before final export, completing with zero corrupt/dropped presentation frames. Final clean/diagnostic files are decoded and their actual playback recorded separately; see the included MEDIA_VALIDATION and FINAL playback reports for the measured results rather than assuming browser presentation statistics. Consecutive diagnostic sheets expose all 150 frames. Full-resolution source frames are 1080×1920, 30fps H.264, five seconds.

The side-by-side uses the exact delivered M04 R06 film and M05, synchronized at their original times, without retiming. Both share the same stair-contact schedule and three rises plus landing recovery. The different environment and camera are labelled; this is not a camera-matched solver ablation.

## Remaining artistic limitations — not approved for film

The action remains authored kinematics, with native IK geometric constraints rather than solved balance forces, muscles or joint torque. Its frightened intention is stronger but subtle acting, urgency and cinematic quality still require user judgment. There is no handrail grip, cloth simulation or general body/environment collision solver. The head is the original illustrated art on a bound native quad; the packed native image is a static reference while timed facial parameters are reproduced by the supplied vector renderer and controls JSON. No volumetric facial deformation is claimed. Contact shadows and light bands are deliberately illustrated approximations.

The landing recovery does not yet continue through the hallway. The environment is a cutaway staircase set. Videos are silent; there is no new sound-synchronization claim. The camera/framing differs from M04 and some far-side anatomy naturally overlaps in the side view, which the diagnostic colours clarify.

Engineering checks pass with the small floating-point regressions itemized in VALIDATION_REPORT.md. Artistic status is pending user review, not automatic approval. Key/door, curtain, steering/driving, chase and the 86-second film were not started. Any later reuse needs their separate prop/vehicle constraints.

## Recorded final playback result

Final clean playback completes at normal and half speed with zero dropped/corrupt frames in Chromium. The fixed diagnostic playback completes at normal speed with one dropped presentation frame and zero corrupt frames. FFmpeg decodes all 150 encoded frames in each file without error; the browser presentation drop does not indicate a missing encoded frame. All 150 diagnostic frames were inspected on ordered sheets.
