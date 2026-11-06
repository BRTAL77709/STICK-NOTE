# M08 technical validation and artistic report

Eight finished scene exports; all artistic approvals remain with the user. FINAL filenames identify deliverables, not acceptance. No86-second film was assembled.

## Objective native measurements

Millimetres below, metres in source JSON. Native body/limb evaluation at30Hz, with denser joint data available. Thresholds:IK/contact and stance1.5mm, digits2mm, limb lengths/joint connections0.1mm. Seated pedal contacts use heel/toe checks rather than flat floor stance. These are sampled geometric checks, not force/friction/full collision certification.

|Scene / native tag|Wrist IK mm|Leg IK mm|Digit target mm|Stance drift mm|Limb variation mm|Measured check|
|---|---:|---:|---:|---:|---:|---|
|DRIVING_COCKPIT M08|0.067917|0.057973|0.005083|N/A|0.002364|TECHNICAL PASS|
|KEY_LOCK M08|0.080124|0.000668|0.003205|0.000319|0.001953|TECHNICAL PASS|
|DOOR_ENTRY M08D|0.082168|0.013472|0.005844|0.007924|0.001599|TECHNICAL PASS|
|CAR_EXIT_RUNNING M08J|0.082860|0.087886|0.003324|0.069718|0.001924|TECHNICAL PASS|
|WINDOW_CURTAIN M08F|0.082121|0.002552|0.012283|0.001221|0.001409|TECHNICAL PASS|
|DRIVER_CHASE M08|0.067917|0.057973|0.005083|N/A|0.002364|TECHNICAL PASS|

Staircase:601fresh evaluations at120Hz. Stance drift **0.360045mm**, foot/tread distance **0.359281mm**. Original foot targets/IK retained; torso/arm acting changes actual bound geometry by57.511mm. Fresh sampled native actor reopen/cache vertex difference max **0.000000mm**.

Door/frame sampled native body vertex penetration **0.000000mm**, tested tolerance5mm, excluding intentionally contacting mittens/digits and transparent head card. Exit shoe/terrain penetration **0.013327mm**, tolerance1.5mm. No continuous swept-volume guarantee.

Curtain horizontal material arc-length error **0.000008765mm**. Header-pin/rail-tab authored alignment error0.000000000mm. Native cloth parity checked separately at saved samples. Controlled fold/attachment rig, not cloth forces/self-collision.

Vehicle:120Hz bicycle integration, centre gap14.000→6.406866m; conservative bumper gap2.106866m; speed0–9.921330m/s; parked speed0. No tyre-force simulator.

World/car-local camera projection residual **1.32580496366e-12px**. Six sampled culled/reference environment frames are pixel-identical after fixing the group bounds. This does not certify all camera/world collisions.

Finger tests use rounded contact markers, not the entire hand mesh. Native key/handle/wheel/fabric mirror transforms were independently sampled. Full prop-only native GUI edits do not automatically update the scripted renderer; editing boundaries are in REBUILD.md.

## Final encoded media and actual playback

|Clip|Seconds|Frames|Normal dropped|Half-speed dropped|Full decode|
|---|---:|---:|---:|---:|---|
|DRIVING_COCKPIT|12.0|360|1|0|PASS|
|ROAD_BUILDINGS|7.0|210|1|2|PASS|
|CAR_CHASE|11.0|330|9|1|PASS|
|CAR_EXIT_RUNNING|10.8|324|7|0|PASS|
|KEY_LOCK|7.0|210|21|0|PASS|
|DOOR_ENTRY|13.0|390|5|0|PASS|
|STAIRS|5.0|150|0|0|PASS|
|WINDOW_CURTAIN|10.5|315|8|6|PASS|

All clean clips1080×1920/30fps/H.264/yuv420p withAAC Foley. Complete FFmpeg decoding, frame counts, duration, black-frame and repeated-thumbnail scans, SHA256 and diagnostic frame pages are in MEDIA_VALIDATION.json. Actual Chromium playback completed at1×/0.5× without corrupted-frame reports. Browser drops above are real host-load observations; they are not hidden or equated with missing encoded frames. Playback reports are bound to exact MP4 hashes.

Final displayed-frame and encoded-frame sheets were inspected alongside the working renders. Waveform peaks/RMS and event timing are recorded; no human auditory approval is claimed. Foley is original local synthesis, no paid service and no dialogue. Debug titles were corrected in a separate documented finishing pass, preserving their original diagnostic videos and all clean films.

## Genuine change versus inheritance

M07_M08_NATIVE_CHANGES.json distinguishes actual body changes from reused choreography. Driving, running, curtain and staircase have new evaluated native body geometry. Key/door and early car-exit phases retain established trajectories. Running is replanned with continuous momentum, shorter stance, toe-off, terrain-aware targets and bounded pelvis height; native peak running root acceleration drops44.906→3.184m/s². Shared illustrated head/attention/camera/environment corrections remain separate. Do not interpret a new MP4 filename or fresh native bake as an entirely new movement system.

Remaining artistic limits: angular hands/cockpit/vehicle surfaces; authored kinematic weight and timing; graphic/card head perspective; controlled rather than simulated cloth; simplified light/reflection/mirror treatment; local interior cutaways and an uncertified whole-house route. All8 are ready for user review; no10/10, USER APPROVED or blanket artistic-success claim. See KNOWN_LIMITATIONS.md.

Preservation:all489hashed M07 files and782older protected files unchanged. GitHub publication additionally preserves every previous tree entry. Internal partial/cancelled exports are retained in scratch and excluded from delivery.
