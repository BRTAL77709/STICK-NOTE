# M10 source and motion audit

M09's eight actual MP4s, selected native models, skinned geometry caches, authoring states, cameras and prior QA were found. INPUT_MEDIA_AUDIT.json records the actual MP4 hashes. M09_PRESERVATION_BASELINE.json protects the pre-edit files. No missing character redesign or paid service was needed.

| Scene | M09 source-level limitation | M10 correction |
|---|---|---|
| Driving cockpit | Interior pieces and driver were coordinated in scripts but lacked a unified editable native car hierarchy; limited mirror/shoulder performance | Explicit CAR_ROOT hierarchy, local steering axis/frame geometry and native skin parity proof; stronger anticipatory mirror glance, shoulder tension, acceleration/brake body response and small grip tightening while native fingertip targets stay on wheel |
| Road/buildings | Connected geography existed, but route recognition was weak | Preserve road/facade scale and House17 transform; add two fixed route landmarks and registered wet-light accents; lower purposeful track with genuine world parallax |
| Chase | Driver reaction section occurred after its authored mirror-glance timing | Move driver section to1.6–3.6s, then the closing pursuer reveal to3.6–5.3s; preserve integrated positions, wheel-distance relation and safe braking instead of inventing a new disconnected route |
| Car exit/running | No explicit visible handle pull; regular running arm rhythm | Native grip follows a22mm handle pull only after contact, with spring return after release; body rise/lean and nonuniform authored arm/pelvis key poses tied to foot landings; original continuous root and independent planted-foot targets retained |
| Key/lock | M09's100mm blade stopped at51mm insertion depth | Defined90mm seated stop with10mm shoulder outside; move key, wrist and finger targets together on the lock axis; tighter readable angle, no middle cut concealing insertion/turn/withdrawal |
| Door entry | M09 ended at the inside lock, without a hallway continuation | Extend13s to16s with release, turn and four actual foot landings; shorten steps, add continuous PCHIP root advance/weight shift toward the stair hall; collision-safe inside elbow bend |
| Stairs | Even timing restrained urgency | Retain actual M09/M04 native root/ankle/foot/pole keys and fixed lengths; directly transform their timestamps through a nonuniform clock; add FK anticipation/individual chest effort and landing recovery;6s shot reaches landing |
| Window/curtain | Listening and follow-through were restrained | Native chest/listening reaction, grip-constrained pull and frightened recoil; damped interior fabric deformation with header/edge anchors unchanged; registered sedan reveal retained |

## Actual rigs and coordinate spaces

bake_native.py uses the retained M04 armature and approved bound skin, native two-bone leg IK, native arm IK with wrist/elbow poles, and native digit IK. Stable bones are not scaled. Stair arms/chest retain native FK controls. Contact transitions blend authored targets; no universal IK/FK mode-switch interface or force-based body simulation is claimed.

Legacy actor authoring is metres/Y-up and maps to native BlenderZ-up byB(x,y,z)=(z,x,y). The retained M05 staircase exporter uses its established separate native convention. Camera animation exports state the space for every frame. Cockpit native groups are car-local; the renderer applies integrated world motion once. Identity parent frames and preserved world matrices avoid double transforms. Native hierarchy files were checked against the actual evaluated skin.

The city, cars, House17 facade and bedroom sedan share vehicle_system.py registration. Native world mirrors and scripted final world geometry have the same definitions, but editing a native prop alone does not automatically update the scripted prop renderer.

## Rejected internal passes and repairs

- Resampling the staircase controls onto new30Hz keys caused1.438mm stance/tread error. Rejected. Directly retiming original contact keys reduced measured maximum stance drift to0.263mm at120Hz.
- The first hallway turn put a sleeve through the closed leaf. Rejected. Interior-facing elbow bend planes removed sampled penetration. A later pose review shortened the hallway steps and advanced the pelvis over their contacts.
- The inherited lock-detail visibility mask hid the added hallway body. Its time range was bounded to the actual lock detail, and the full hallway performance was rerendered.
- Handle pull initially began before contact. Corrected onset follows grip; changed source states are rendered anew. Frames are reused only when exact native mesh/state equality and critical source hashes establish equivalent rendering inputs.

See SOURCE_TO_RENDER.json, the final render provenance, scoped numerical QA, actual before/after MP4 comparisons and contact sheets. Passing engineering checks does not grant artistic approval.
