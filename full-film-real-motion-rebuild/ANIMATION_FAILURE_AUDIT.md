# Animation failure audit — actual rejected source

Baseline: `../full-film-v10-quality-rebuild/`, film `renders/final/THE_PRICE_OF_SILENCE_V10_QUALITY_REBUILD_86s.mp4`. No baseline file is edited. Source references below refer to that baseline, not newly authored files. The existing MP4 contact sheet/presentation evidence and actual rendering dispatch were inspected. User rejection is the artistic finding; numerical contact residuals do not rebut it.

## Engine findings

The renderer evaluates SVG each frame (`scripts/render_scenes.py:9–17, 44–52`), so this is not literally an image slideshow. `articulated.py:33–44` solves screen-plane fixed-length limbs to targets, then draws a root-scaled illustration (`:47–70`). A fixed shoulder/hip outline and default hands near the waist recur across many actions. The contact math is useful, but it does not by itself establish convincing body mechanics or readily visible motion. Perspective is applied to world roots/targets and a whole projected owner scale; most non-V10 knees are solved afterward in 2D rather than as a metric spatial skeleton.

`scene_builder.py:51–92` determines what reaches the screen. Several well-engineered contacts receive only fractions of a second. Passing numeric audits while the action is tiny, brief, weakly staged or repeatedly returning to the same waist-hand silhouette was the central validation failure. Head outlines do vary (`driver_rig.py:38–60`); it would be false to report a static frontal head throughout. Those changes are modest and many attention beats share the same easing pattern.

## Scene-by-scene evidence

| Scene / film time | Actual world/joint/prop motion | Failure or remaining weakness in the rejected staging |
|---|---|---|
| 01 / 0–4 | `motion_state.py:12–38,70–77`: SI car displacement/heading/odometry; `vehicle.py:6–40`: body/wheels; `scene_builder.py:25–30`: 35%-travel camera | Genuine vehicle motion, not a static car. Needs an exposed acceleration/heading proof with independently reported camera/car trajectories, not confidence inferred from background motion. |
| 02 / 4–8 | `driver_rig.py:13–36`: eye/head/torso mirror beat and wheel-constrained elbows | Mostly a held driving pose punctuated by one mirror glance; restrained shoulder change and nearly unchanged silhouette. No regrip/force-release performance. |
| 03 / 8–12 | Same module: braking load and left gaze | Continuous articulated gaze exists, but uses a similar interpolated head/torso beat and small displacement. Camera/environment movement can dominate perception. |
| 04 / 12–18 | `v10_trunk.py:33–66,98+`: world foot plans, 3D knees, hand constraints | Preserve approved choreography. Independent foot anchors and contact staging are the engineering reference. |
| 05 / 18–24 | `v10_trunk.py:68–93`: delayed victim core/limbs, support/grips, lift/loading | Preserve. Multiple coordinated joints, distinct action phases and prop occlusion make the action legible. |
| 06 / 24–28 | `v10_trunk.py:24–30`: closure precedes spatial head turn | Preserve. Do not replace it with the witness head rig. |
| 07 / 28–32 | `driving.py:10–21`: rigid shoe/heel solve, knee/ankle, rotating pedal | Dispatch `scene_builder.py:62–65` exposes the foot only from local .55 to 1.55 s. Toe starts in contact; no approach or contact acquisition. Hip is constant `(205,420)` and torso is cropped. This fails the requested complete action, despite valid shoe-to-pedal math. |
| 08 / 32–37 | `motion_state.py:45–68` black-car merge; `scene_builder.py:67–71` exterior then mirror | Real travel/merge exists; cut to mirror replaces exterior evidence before the whole chase beat is evaluated. HUD cannot serve as its proof. |
| 09 / 37–42 | `driver_rig.py:30–35` wheel IK; `scene_builder.py:73–75` POV, driver, exterior | Real steering and heading, but distributed across three views. Need an uninterrupted exposed vehicle proof; no claim that static background imagery alone is travel. |
| 10 / 42–47 | Vehicle deceleration; driver scan/release (`driver_rig.py:18–25`) | Restrained release looks much like the earlier parked silhouette; world motion is genuine but does not replace acting. |
| 11 / 47–51 | `house_site.py:21–27,69+`: rotating car door, explicit exit/run feet, world root | Actual exit, handoff and run exist. Car leaf partly occludes the owner and the four-second compound beat gives little time to read contacts. Keep real movement, expose the running owner more clearly. |
| 12 / 51–55 | `house_actions.py:12–23,57–109`: handle/key/hinge; screen IK owner follows targets | About 15 interactions compressed into 4 s. Initial reach .22 s, key alignment .2 s, wrist turn .22 s. Root waits through most of it; body force is modest. Key tip insertion is shallow. Extend; show continuous whole-owner action and completion, rather than asserting every tiny interpolation is readable. |
| 13 / 55–59 | Same door controller closes/locks/checks; `stairs_actions.py:8,26–51` first flight | Door camera flips at local 4.3 s; old draw orders entire owner over the leaf/wall (`house_actions.py:139+`) rather than explicitly masking entry depth. Eight steps take 1.45 s, about 5.5 risers/s. The body can look like a rapidly translated illustration despite planted target math. |
| 14 / 59–63 | `stairs_actions.py:39–68` upper flight; `room_actions.py:17–29,54–58,92–97` approach/curtain | Upper seven steps take 1.3 s. Curtain reach .25 s and pull .6 s; entire room owner uses similar waist-hand defaults. Curtain initially covers only part of the window. The complete physical beats are too compressed. |
| 15 / 63–67 | `room_actions.py:36–37,59–72,99–103`: vibration, grip and lift | A continuous hand-owned phone exists. It must be judged in an exposed shot, not through the incoming-call panel or a contact residual. Retain the constraint but give approach/grip/chest-to-ear motion readable timing. |
| 16 / 67–74 | `room_actions.py:41–53`: knee/chest/head/hand reaction while holding phone | One primary reaction with a long recurring waist-hand/listening pose. Counter animation is not acting. Re-time reactions to speech, change the body silhouette and attention deliberately. |
| 17 / 74–80 | `room_actions.py:17–29,41–53`: two backward plants, recoil | Real feet/root changes exist, but the performance remains restricted to a small head/chest/hand pose family. Retain contacts; strengthen reaction and completion without camera zoom. |
| 18 / 80–86 | Intentional graphic choice screen, rain, text animation | No physical character action intended. Preserve graphic design; shorten only if necessary for readable preceding actions. Do not count rain/pixel differences as acting. |

## Replacement strategy

No wholesale claim that the engine lacked motion, and no change to approved designs. Reuse the successful V10 principle: explicit contact intervals, independent planted targets, articulated bodies, visible force transfer and purposeful holds. Test A adds acquisition and a connected seated body. B exposes independent SI travel with no HUD. C extends the action and adds entry depth masking. D solves metric 3D legs and arms and separates lift/land/transfer/extension for three readable steps. E starts closed and extends grip/pull/reaction/fold lag.

Proof videos, per-frame joint/trajectory data, events, full-speed and slow-play evidence must pass before master integration. No subjective quality approval is inferred from a rendered file or the audit.

## Running follow-up: measured cause

The old run already includes swing and flight intervals; it is not a walking-duty-cycle loop. It fixes the hip near −102 rig units for most of the run while a separate time-based foot schedule follows eased root travel. In the steady-stride interval (root progress 0.8–4.8 m), root-to-planted-foot horizontal offset reaches 0.469 m. The new distance-based contacts keep that interval within 0.193 m and allow a median pelvis height of 0.651 m versus 0.451 m. The initial exit/launch still reaches 0.490 m horizontal offset; no reduction of the whole-run maximum is claimed. Pelvis feasibility and actual playback were checked. See reports/running-cause-comparison.json.

## Side-view world occlusion failure discovered during composite review

Rejected `world.py:144–164` assigns facade/lamp queue depth using `(road_x(z),0,z)` instead of their actual lateral position. At a curbside perpendicular view this places a far-side building near the road-centre depth, so it can paint over the sedan. Utility poles/signs are also drawn after traffic regardless of depth. Actual composite captures exposed facades/poles crossing the vehicle silhouette.

The new `world.city_queue` uses tangent-transformed facade centres and actual side positions for all street objects, together with vehicle depth. Poles, signs and wires enter the same queue. Affected vehicle/window/environment clips are rerendered; approved V10 is independent and unchanged. This is a painter-order correction, not a redesign or camera disguise. Whole-object sorting remains a 2.5D approximation, not an exhaustive polygon depth-buffer simulation.
