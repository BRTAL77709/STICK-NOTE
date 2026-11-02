# V10 technical validation

## Shared world and fixed camera basis

Coordinates: X is vehicle width; Y is forward along the sedan; Z is height. Pavement is exactly Z=0. A fixed orthographic yaw of 20° and elevation of 35° projects the sedan, articulated joints, soles, lid, contact points and debug ground grid. The restrained camera movement applies to the whole projected scene. Character motion does not use independent screen offsets to imitate ground movement.

The rear bumper occupies world Y=−16, X=350–850, Z=72–100. The opening is the fixed quadrilateral defined by OPENING in the source, at Z=235, with an interior floor at Z=85–90. The lid rotates about world Y=135, Z=235. All vertices keep their local material coordinates through opening and closure. Wheel contours are also projected world circles tangent to Z=0.

## All-frame checks

- **300 frames** checked; all feet, hands, torso and leg poses solve without unreachable targets.
- Maximum stance-foot Z error: **0**. Maximum displacement between consecutive stance frames: **0**.
- **All four feet are planted throughout 3.0–4.6s.** Subsequent loading moves use explicit, nonoverlapping per-character swing/stance schedules.
- Full projected shoe quadrilaterals versus the projected rear bumper: **0 overlaps** across all 300 frames. Shoe ground-footprint intrusions into the car: **0**. These go beyond the numerical foot locks used in V9.
- Maximum shoulder-to-hand reach: **173.631 units**, below the 90+87 arm-length limit.
- Maximum 3D bone-length variation: **1.99e-13 units** (floating-point precision). Projected limb lengths can change naturally with the three-quarter view; the underlying bones do not stretch.
- The victim's torso rotates continuously from **0° to 90°**. It does not invert. Head, pelvis and legs use delayed follow-through, and the body stays largely horizontal for final loading.
- Final skeletal anchors are inside the cavity bounds: X=380–840, Y=12–135, Z=85–235. The final shoulder is (505,65,155); pelvis is approximately (643.27,65,126.25).
- Arm centerline crossings of the rear plane below the sill: **0**. Lowest checked crossing: **235.841**, versus sill height235. Withdrawal and subsequent lid reach use raised arcs rather than straight paths through the panel.
- Maximum closing hand-to-lid gap: **0 units**. The same material point is followed through closure.

These are geometric checks, not a whole-body mass simulation or a guarantee about every painted sleeve edge. Contact, silhouette and apparent weight are additionally reviewed in the encoded frames.

## Action and occlusion

Drag0–1.4s; trunk opening/support handoff1.4–2.3s; regrip2.3–3s; grounded lift3–4.6s; loading4.6–6.2s; release/withdraw6.2–6.7s; lid reach/close6.7–7.5s; notice after7.75s; head turn8–9.2s; narrowing9.2–9.7s and final hold.

The first pair of support grips is on the upper arms; C02 receives a lower-body support before C01 opens the lid. C01 reestablishes upper-body support before lifting. As the victim becomes horizontal, C02 cradles the pelvis/knee, then guides the lower legs while C01 supports the chest/upper back. Regrips traverse deliberately while the other contacts remain active. Exact target positions are shared by the hand IK and victim rig.

The torso advances over the opening; the legs follow a delayed world path. The body then lowers into the cavity. A projected loading corridor is derived from the actual opening and the body's current height; it supplies side-wall occlusion without an opacity fade. The raised lid stays behind the victim during insertion. Once closing begins, the rotating lid passes in front of the cavity. The victim remains in the source scene after closure: pixel ablation verifies complete occlusion at7.5 and7.8s.

The head-time function guards against any turn while the lid is nonzero. Closure is7.5s/frame225; the original synthesized latch click begins at exactly7.5s. The notice and head turn follow closure. See action-order-validation.json, occlusion-verification.json and assets/sound-events.json.

## Encoded and visual checks

The low-resolution preview is checked in Chromium at normal1× playback. The final receives FFprobe metadata/frame counting, a complete FFmpeg decode, blackdetect and a separate final/comparison playback check. Results are recorded in encoding-verification.json, playback-verification.json and encoded-visual-verification.json.

The final contact sheet covers every beat and both sides of the8s cut. Actual lift/loading frames are decoded at0.1s intervals. The ground-plane images are explicitly labeled rerenders of the same poses with diagnostic overlays; they are not presented as unmodified final footage. The clean film is rendered with debug=False.

## Limits

Weight transfer and contact timing are authored; mass balance and cloth/finger deformation are simplified. Some arms still overlap during the support handoff. Trunk side-wall holdouts are a 2.5D visibility solution, not a complete solid-body simulator. Judge the improvement in acting from the video; no artistic score or user approval is asserted.

## Final export results

FFprobe confirms H.264,1080×1920,30/1 FPS,300 video frames and10.000000 seconds. File size:4034109 bytes. AAC audio accompanies the film. Full FFmpeg decoding completes without errors; blackdetect reports no black intervals. Minimum decoded RGB frame mean:19.283. The intended frame240 cut changes13.448 mean RGB units versus a maximum2.259 elsewhere. These statistics supplement visual inspection. Original ambience/cues measure−28.0 dB mean and−8.7 dB peak.

Normal-speed final playback presented all300 frames with zero drops/corruptions. The corrected preview also presented300 frames without drops/corruptions. These are automated browser playback captures, followed by inspection of the frame sequences and encoded detail sheets; they do not imply user approval.
