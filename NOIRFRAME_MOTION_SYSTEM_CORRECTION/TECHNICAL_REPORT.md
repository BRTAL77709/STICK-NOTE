# Technical and artistic review

These three candidates test the replacement contact logic, not the complete four scenes. They remain unapproved. The fixed stair and key cameras and synchronized two-view vehicle view intentionally expose interactions.

## Stair contact

The three-second sample covers the last two risers, landing and two hallway steps. Each foot has its own world-space touchdown and support interval. The pelvis is solved toward a segmented center-of-mass plan; pressure transfers before toe-off. Vertical movement uses a continuous spline with anticipation, not repeated identical root bobs. Heel lift pivots about the planted toe. The rail hand releases as the actor enters the hallway.

The frozen preflight measured approximately 1.003 m pelvis travel, 0.411 m center-of-mass rise, both feet on the upper floor at the end, no measured planted-toe drift beyond floating-point roundoff and no sampled sole/riser penetration. The final rendered-state JSON is authoritative for final values. This is an approximate linearized preview balance model, not a validated biomechanical simulation.

## Key, lock and handle

The key advances into a fixed cylinder, rotates 90 degrees and stays inserted. Finger pads follow the bow surface, rather than placing only a wrist marker near it. The other hand grips/depresses the lever before a nine-degree door hinge opening; key, lock and both hands follow the door frame. Depth clipping occurs at the metal face so the blade enters the cylinder instead of passing visibly through the panel.

A sampled finger/lever overlap of about 0.079 mm remains within the declared 1 mm geometry tolerance. Full skin-volume collision is not solved. This three-second stress test does not include key withdrawal, entry or closing.

## Steering and turning

Cockpit, wheel, hands, column, pedals and body share one vehicle transform. Both views use the same simulation time. The foot heel remains on the floor; the toe releases the accelerator, pivots and engages the brake. Throttle/brake channels drive longitudinal acceleration. Each car advances independently along the fixed city route, with its own steering, wheel phase and suspension response. The measured center-to-center pursuit gap decreases from 12.0 m to approximately 7.80 m. The route follows a feed-forward bicycle relationship; this is not a full tire/friction simulator.

## Review evidence

Low-resolution P07 videos were actually played in Chromium at normal and half speed; all three ended with zero dropped/corrupted frames in those runs. Final native-HD metadata, complete FFmpeg decode, rendered-state checks and playback logs are supplied separately. Frame sheets include every frame, not just selected poses. These numerical checks cannot approve artistic weight, acting or the viewer's perception of grip.

Original comparisons use V12 at its original speed: stairs 6.4–9.4 s, House 5.05–8.05 s, driving 2.5–6.5 s. Composition differs because these are deliberately focused diagnostic interactions. No time stretching, freeze frames or camera zoom disguise is used.

## Corrections during internal review

Internal trials revealed toe/riser clipping during heel roll, a rail release blended twice, fingertips placed inside the key bow rather than on its surface, and sleeve cuffs intruding into props. Targets were set back, the toe pivot made explicit, rail blending corrected, actual fingertip surfaces constrained and cuffs tapered. Only the final M01 candidates are offered as corrected review clips; internal preview exports are not deliverables.

Final HD playback completed at both speeds, with zero corrupted frames. In the first runs Chromium reported 3 dropped stair frames and 1 driving frame at normal speed, and 3 key frames at half speed. These are playback-environment drops; the files separately decode all 90/90/120 frames. The logs retain these observations.
