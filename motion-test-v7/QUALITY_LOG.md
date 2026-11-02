# V7 quality log — awaiting user review

Baseline: V6. Preserve its accepted directional improvements without claiming approval of the whole test. No numerical artistic score is assigned.

## Changes tied to V6 weaknesses

1. Replaced shared periodic locomotion with separate explicit step schedules: six C01 and five C02 landings. Hip transfer follows support contacts; knees compress and torsos settle after actual landings.
2. Pullers request grip anchors from their current shoulder poses. A shared distance constraint preserves victim upper-arm proportions, then two-bone IK drives both criminal arms. The victim's upper body is derived from those same anchors.
3. Replaced delayed curve offsets with a 120 Hz spring/damping model for passive pelvis, heels and head. Gravity lowers the pelvis; acceleration produces lag and deceleration produces a small overshoot. Heels scrape continuously without deliberate steps.
4. Shirt spine/crease deformation follows the pelvis relative to supported shoulders. Wrist orientation follows arm geometry around the unchanged grip center. Palette and designs remain V6.
5. Preserved V6's head-turn implementation exactly, along with cap/mask perspective and expression timing.

## Review and corrections

Rendered a 540×960 preview first. It played at 1× with all 150 frames and no drops. Inspected the actual presented-frame sequence and short-interval contact sheet. Checked every pose for reach, grip, grounded heels, support and constant bone lengths before full rendering.

The inherited fixed sag assertion failed at 128.82 units because V7 rotates/compresses the upper torso. Visually examined the low pelvis and replaced the obsolete >130 bound with >120; reported both the change and exact result. No footage was changed simply to satisfy an arbitrary inherited threshold.

Final rendering passed full decoding and exact metadata checks. Inspected encoded consecutive foot/grip crops and normal-speed final playback. V6/V7 comparison uses actual rendered videos with V7 audio. All prior versions remain intact.

## Actual V6 versus V7 findings

| Area | Finding |
|---|---|
| Weight transfer | V7's hip shift follows the supporting foot and separate landing impulses, rather than V6's more regular cadence. More asymmetric loading is visible, but the broad lean is still stylized. |
| Foot sliding | Both versions have zero modeled stance movement; no improvement is claimed in that metric. V7 sampled encoded rows vary by at most one half-resolution pixel; V6's selected samples had zero. Leg overlap remains a readability limitation. |
| Grip stability | Both versions maintain upper-arm contact. V7 derives the shared torso from puller support poses and adds wrist orientation; no claim that V6 grips were detached. |
| Victim inertia | V7 shows shoulder-led pulling, pelvis delay/overshoot and passive head lag. Shirt now deforms slightly. Friction differences between the shoes remain very subtle. |
| Gait realism | Step count, timing, swing height and targets differ between criminals. The action is less synchronized; center-of-mass balance is still authored rather than fully simulated. |
| Head turn | V6 geometry/timing code is preserved; the comparison retains the same recognizable side-to-front turn and final narrowed stare. |

## Three remaining weaknesses

- Victim shoe catches are too subtle to make the two scrape patterns strongly distinct.
- C01's planted shoe is partly obscured by the victim's trailing leg during part of deceleration.
- Shoulder loading and wrist compression still look economical and graphic; finger deformation and full mass balance are not simulated.

V7 is delivered for user review, not declared exceptional or approved. Additional production cost: $0. Stop after V7; no V8 or full film has begun.
