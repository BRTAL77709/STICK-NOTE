# Vehicle, 4 seconds

**[Play/download MP4](MOTION_PROOF_B_VEHICLE_final_dd24ad03b3.mp4?raw=true)** · [Contact sheet](final_CONTACT_SHEET.jpg) · [Trajectory CSV](MOTION_TRAJECTORY.csv)

A metric arc-length path establishes a rolling start, smoothly accelerates from 2 to 7 m/s over 18 m, then releases load into a cruise hold and turns about 15 degrees. Wheels rotate by distance/radius, steering by curvature. Fixed-world houses, lamps and reflections share the projection. Camera follows only 65% of travel with partial pan: subject displacement remains visible. No HUD.

Source: [physical_proofs.py](../../engine/animation/physical_proofs.py#L57), function `vehicle_state`; shared approved rig in [articulated.py](../../engine/animation/articulated.py). Preview and HD paths are recorded in `preview.json` and `final.json`.

Evidence: `JOINTS_TRAJECTORIES.json`, `JOINT_TRANSFORMS.json`, `CONTACT_EVENTS.json`, `final_CONTACT_SHEET.jpg`, `final_PLAYBACK.json` and normal/half-speed presented-frame sheets. Videos are intentionally silent to expose motion.

See [numerical validation](../../reports/physical-proof-validation.json) and [integration gate](../../reports/proof-integration-gate.json). Technical validation is separate from user artistic approval.
