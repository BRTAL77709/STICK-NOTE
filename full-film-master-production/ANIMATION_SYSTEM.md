# Deterministic animation system

All picture is evaluated from absolute time at 30 FPS. No runtime clock, accumulated simulation or unseeded randomness is used. engine/animation contains the actual reusable modules; the domain folders expose their APIs. Each scenes/scene_XX/scene.py evaluates its own scene with local time. scripts/render_scenes.py renders independent caches, validates completed files, and preserves interrupted .rendering.mp4 candidates. Fingerprints use the scene branch and relevant dependencies, excluding unrelated audio changes.

motion_state.py supplies position, velocity, acceleration, heading, rack angle, steering wheel angle, per-car wheel odometers, suspension, pitch, roll, RPM and pursuit separation. The global route slows for discovery, stops during the crime, accelerates after 28.6s, corners at 38.5s and brakes for home. DownCamera projects the actual street and parked sedan through the upstairs aperture. The alley uses V10's shared ground plane, IK, foot plans, grips and trunk hinge.

actor.py has contact-aware running and stair gait. Stance anchors remain fixed while root/pelvis advance; stair floors use fixed tread levels. Two-bone arms constrain the wheel, phone and curtain contacts. Head rendering changes silhouette, cap/brim and eye perspective. driver_rig.py preserves approved witness identity and separates attention, torso load and shoulder timing.

house17.py owns doorState, doorPoint, hardware, curtain/window staging and phone grip paths. Key geometry, hand target and hardware use one hinge projection. Opening occurs after unlock; the door closes before interior locking. The curtain edge determines its grip, and folds compress with the pull. Phone hand and prop use the same anchor after pickup.

This is a coded illustrated system, not a claim of human-level acting or physical simulation. Camera cuts and simplified geometry still require visual review. Source constraints support quality control; they do not certify artistic success.
