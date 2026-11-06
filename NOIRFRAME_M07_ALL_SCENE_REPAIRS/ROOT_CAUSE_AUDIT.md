# M07 forensic source audit

Active local branch: `work`. New work lives only in `NOIRFRAME_M07_ALL_SCENE_REPAIRS`. No complete-film composition is being rendered.

## Actual pipeline and confirmed causes

| Area | Actual files/functions | Confirmed implementation and limitation | M07 correction boundary |
|---|---|---|---|
| M03 shared actor | `NOIRFRAME_M03/source/render.py:main` → `shots.py` → controller `state` → `actor.actor` → `DepthRaster` → FFmpeg RGB pipe | Real analytic `rig.ik` existed. The hierarchy dictionary was not a native skeleton; tubes, sleeve polygons and hoodie panels were recreated each frame. Camera-facing head glyph and shallow torso could occlude awkwardly. | Evaluate the inherited M04 native armature and bound geometry. Add actual native arm IK and object-relative contact targets; do not just rename analytic math as native IK. |
| M04/M05 native rig | `NOIRFRAME_M04/source/build_rig.py`, `NOIRFRAME_M05/source/polish_existing.py`, `export_edited.py`, `render.py` | Native two-bone leg IK, no stretch, world ankle controls, stable poles, bound shoes and weighted hoodie. M05 edits actual saved M04. Prop interactions are not supplied by the staircase rig. | Reopen/evaluate the saved model, independently measure it, reuse its proportions and add shot-specific controls. Retain staircase scene instead of rebuilding it. |
| Key/door | `key_test.state`, `root_path`, `door_angle`; `shots.door_geometry` | Shared hinge matrix and real key blade/slot exist. Timing/grip switches are authored. Root filtering in `stabilize.prepare` is kinematic fitting, not physics. Camera cut metadata switched at 8.55s although camera cut was 8.30s. Inside lock operation was absent. | Split readable key and full entry clips; native arm IK; explicit inside locking phase; cameras and cut metadata from one function; evaluate contact errors from solved native joints. |
| Steering | `vehicle_test.state`, `pedal`, `foot_on_pedal`; `shots.cabin` | Wheel drives targets, rear-axle bicycle integration is genuine. Foot/sole surface used a different representation from native rigid shoes. Driver and cockpit were simplified; five requested cockpit angles were absent. | Native seated driver, invariant native shoes, shared wheel grip frames and pedal geometry; multiple matched local/world camera angles, explicit seat/cabin detail. |
| Vehicle chase | `vehicle_dynamics.advance/simulate`, `shots.chase/vehicle_pair` | Pursuer integration is real, but coverage is one elevated view; both brake lamps use witness brake flag. Road is an immutable sample of the witness reference route, not an independently surveyed city. | Independent brake channels, more coverage, continuous fixed route, shared stop/House17 registration and gap data. Explicitly retain kinematic/spring limits. |
| Curtain | `curtain_test.fabric/state`; `shots.bedroom` | Horizontal polyline arc-length fold rig exists. Not cloth dynamics: scripted row lag and sine folds, fabric drives hand. No entrance; sedan location is a separate local constant. | Enter/approach/reach/pull/reveal/recoil/release choreography, native hand IK, controlled fabric fold rig with material-width checks; sedan registered to city stop. No cloth-physics claim. |
| Arrival/exit | Existing film/v12 sources and M03 five-test dispatch | No M03 clean native-rig exit-and-running action. Existing car has a solid side panel and no articulated driver-door opening. | Dedicated hinge, real side opening, seated-to-ground contact phases, weight transfer, explicit running contacts and final approach to House17. |
| Environments | `shots.city_set/house_set/bedroom`, `geometry.car/city` | World geometry exists; city facades are repetitive boxes. Bedroom view and House17 are not registered by one transform. Cockpit and exterior detail levels differ. | Shared landmark registration, varied facade architecture/curbs/intersections, same vehicle geometry and exterior view derived from parked sedan state. |

## Production assets and alternative pipelines

The repository also contains Remotion/Hyperframes and many full-film source trees (`full-film-*`, `NOIRFRAME_FULL_FILM_*`, `NOIRFRAME_V11_ANIMATION_REPAIR`, `NOIRFRAME_V12_CINEMATIC_REBUILD`). Their renders are not the source of the delivered M04/M05 native staircase footage. M07 does not edit those compositions or render an old full-film cache. Existing narration, score and effects live under `full-film-*/assets/audio`, `full-film-cinematic-rebuild-v2/assets/audio`, and original rain ambience under `motion-test-v10/assets/original_ambience.wav`. Isolated clips omit dialogue; locally synthesized interaction effects and rain are separately documented.

Tools available locally: Blender 4.3.2, FFmpeg/ffprobe, Python, NumPy, SciPy, Pillow, Cairo/librsvg, Chromium/Playwright. No paid service is required. No GitHub cloning is attempted.

## Failure guards

Every render uses a new versioned output path, checks its producer-data/source hashes, validates frame count/FPS/codec/duration and full decoding, and records actual playback. Partial files are not published. Native geometry cache exports record their .blend hashes. Contact and vehicle measurements are reported separately from artistic review. Fixed diagnostic coverage remains separate from cinematic cuts. Only user review can change status to USER APPROVED.

## Scope of physical claims

Native IK and geometric attachment are constraint solving, not force/muscle/full-body dynamics. Vehicle integration is a bicycle model with spring approximations, not a tyre-friction simulator. Curtain repair uses a lightweight fold rig, not a general cloth simulation. Approximate contacts/collisions and any failed numerical or artistic checks remain listed in QA rather than hidden by a TECHNICAL PASS label.

## Failures actually found during M07 rendered/evaluated review

| Evidence | Source-level cause | Implemented correction |
|---|---|---|
| Window approach planted-foot jump | `actions.curtain`: prefix/contact targets did not join the original approach state | Added explicit threshold crossing and matched approach foot endpoints; native bakes R11 retain these contacts |
| Key stow digits detached17.5mm | Authored grip release preceded the end of the stow transition | Keep fingertip targets attached through withdrawal/stow; native R08 tip error measured |
| Bedroom look showed front face from behind | Original M05 face-card renderer always drew frontal features irrespective of view direction | `view_head.py`/`approved_head_view.py`: continuous camera-relative front/profile/back treatment, rear strap and feature fade |
| Driving OTS headrest/face obscured wheel | `cameras.py` used a camera within/behind the seat/head silhouette | Reframe OTS R12, use camera-relative face visibility; retain other matched cockpit angles |
| Inside thumbturn and key close-ups hidden by head | Camera direction passed through the witness head card | True self-POV after the completed establishing/entry phases; only the head hidden, connected native arms/torso remain |
| House foundation concealed feet | `sets.house_exterior`: foundation top sat above the intended porch plane | Lower foundation to the floor underside; shoes remain visible |
| Exit shoe terrain penetration109.443mm | Final running contacts crossed curb without sufficient arc clearance | `actions.EXIT_STEPS` and native R09 raise the swing path over actual ramp; sampled penetration reduced to0.05456mm |
| Pursuer gap too small3.24m | Independent pursuing vehicle brake schedule closed beyond body length | `vehicle_system.py`: earlier independent deceleration; minimum centre distance6.4069m, conservative bumper gap2.1069m |
| Door sleeve/jamb and closing trouser collision | Native wrist targets were correct but elbow poles and pelvis path put actual mesh into solid leaf/frame | `actions.continuous_key`: tuck both elbows during entry, route free elbow away from leaf tip, move pelvis farther inside before closing. Final R22 sampled body vertices report zero penetration; no continuous collision guarantee |
| Closed entrance missing in city/exit | Detailed facade contained a door opening but no closed leaf in the noninteractive world render | `sets.city`: add the same closed-door geometry before House17 world transform |

No confirmed root cause is attributed to Remotion or Blender physics that was not actually inspected. Final reports capture producer hashes and native version tags; native caches are not accepted merely because they exist. The final isolated audio is newly synthesized locally, not a claim of retained approved ambience.
