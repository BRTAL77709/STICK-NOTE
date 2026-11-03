# Production plan by reusable system

GateA (this delivery): audit18scenes, route/house plan, revised storyboard, implement metric road projection + vehicle state + dashboard + driving rig + camera + rain/light + subtitle/audio scheduler, render15s integrated test, inspect/fix, verify and deliver. GateB: user review. No86s render before approval.

1. World: immutable scene objects in meter coordinates, deterministic projection and depth sort, road spline/tangents, intersections, procedural architectural variants with nonrepeating facade layouts. Preserve navy/teal/amber.
2. Vehicle: same sedan dimensions across shots; wheelbase2.7m, tire radius0.32m; integrated speed for travel/spokes, yaw from route tangent, pitch from acceleration, roll from curvature×speed², road contact and headlights/reflections.
3. Instruments: continuous km/h from same state as road displacement; analog0–160 scale with20km/h labels, RPM and clock in physical dashboard. Pedal angle and driver compression follow throttle; no arbitrary decorative number animation.
4. Character/props: approved cap/head/hoodie dimensions retained, two-linkIK driver elbows to steering rim, coordinated shoulder/head/reaction, gaze/blinks, seatbelt and contact. V10 crime rig retained for future scene adaptation. House/phone constraints in separate prototypes.
5. Cameras: tracking, interior reaction, pedal macro, dashboard insert, low chase/corner, OTS, final cluster/mirror. All driving coverage refers to the same time/position state; shots cannot reset car/world positions.
6. Audio: local English Flite voice with actual phrase durations; deterministic motor synthesis follows RPM/speed/gear data; rain/road-water stereo with passing-pole transients tied to world positions; duck score under voice. Footstep/latch/key/curtain/phone future cues must come from event states.
7. Graphics: DejaVu Sans bold; warm emphasis only for story words; phrase captions centered x540,baseline1500 (pedal450) with margin96px; two lines max, stable placement and brief eased entrance. No captions over eyes, wheel, needle or pedal. Timeline/rpm/speed shares one data module.
8. Review: preview at360×640/30FPS; consecutive frame strips for acceleration/steer; actual playback at1x; fix; final1080×1920/30FPS/H.264/AAC. Validate450frames/15s and world/instrument/audio state. Report subjective limitations and approval status honestly.
