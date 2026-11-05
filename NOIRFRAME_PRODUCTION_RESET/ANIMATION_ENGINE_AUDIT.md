# Production reset audit — inspectable source, no invented static-car finding

The previous86-second film and7-second integration demonstration were rejected by the user. The rejection is the artistic finding. Numeric residuals and successful encodes do not rebut it.

The integration project in `../video-production-toolchain/remotion/src/index.tsx` decompresses pre-evaluated SVG strings and selects them by current frame. It did not implement a new physical rig. `scripts/export_shared.py` evaluates the same copied `animation/physical_proofs.py`; `hyperframes/index.html` displays its vehicle state. Adding Remotion/HyperFrames therefore tested compositing compatibility, not better body mechanics. The new reset does not feed SVG or previous-video frames into Blender.

The rejected source was not literally motionless: `../full-film-real-motion-rebuild/engine/animation/physical_proofs.py:accelerator`, `vehicle_state`, `door_state` and `stair_state` have real time-dependent joints/contacts and metric travel. `vehicle.py:sedan` rotates tires by distance/radius; there is no basis to call that car stationary just because its performance was rejected. Likewise, `world.py:city_queue` already uses depth sorting. Those facts do not establish convincing acting.

Key limits in that method were screen-plane IK for most witness joints, repeated default waist-hand silhouettes, limited torso deformation, root/pose interpolation without an authored shoulder/hip counter-rotation pass, and visual ownership implemented in an SVG draw order. The integration demo keeps hands on a wheel and exposes a pedal, but largely holds the upper body; its background motion and HUD cannot supply weight transfer. A changing face is not by itself a body/head performance. Initial brief anticipation holds are real source holds, not a claim that all210 frames were unique poses.

The existing audit in `../full-film-real-motion-rebuild/ANIMATION_FAILURE_AUDIT.md` supplies the detailed18-scene source references. All of that baseline is preserved, including its failed staging. Its house/key and stair timings were previously stretched to make contact beats readable; compressing them again can reintroduce the same failure and must be judged in playback.

## V10 engineering reference

`../full-film-real-motion-rebuild/engine/animation/v10_trunk.py:foot_world`, `actor_pose`, `victim_pose`, `contacts`, `lid_world`, `head_time` coordinate independent ground anchors, torso/hips, delayed victim weight, grip changes, hinge rotation and spatial head silhouette. Clear opening/lift/loading stages and preserved car geometry make the action legible. V10's picture/clip bytes are not regenerated. The reset borrows the principles of supported contact, distinct phases and spatial continuity, not its rendered frames as a shortcut for new action.

## Native Blender replacement

Blender4.3.2 is available and actually renders on CPU. `reports/blender-capability.json` and `blender/engine-probe.blend` provide actual evidence. Grease Pencil v3 is available; native skinned meshes with orthographic/perspective cameras and Freestyle are selected for this spike because a single3D coordinate system can own IK, hinge, stairs, driver/car, head silhouette and window occlusion. This is a2.5D emission/ink render, not photoreal shading. A Grease Pencil production is not claimed.

`source/rigs.py:Character` creates a native armature, weighted sleeve/trouser/hoodie meshes, two-bone IK constraints with stretch disabled, world foot/wrist empties, a bone-constrained head mount and a geometrical cap/face. `source/world.py:Car` separates stable body, steering pivots and distance-driven wheel rotation. Door hardware parents to a real hinge; wall apertures are actual geometry. `source/actions.py` owns independent stance anchors and body placement. `source/build.py` bakes controls into editable .blend files. Curtain motion is a keyframed draped mesh with changing folds and a constrained gripped edge, not a solved full cloth simulation; this limitation is explicit.

## Observed early defects and revisions

House17v1 had up to0.473 m native IK error because the running root overtook an anchored foot. The opening door also exceeded a supporting arm's reach. The v2 blocking replaces the mismatched quintic root plan with a controlled speed/deceleration and matching foot anchors, then steps the body into the door's arc. Camera height/brim depth are corrected for eye visibility. These are actual failed constraint samples and visible frames, not hypothetical risks. Further results and remaining defects must be recorded from the current proof, never inferred from Blender's name.
