# Three stairs, 4 seconds

**[Play/download MP4](MOTION_PROOF_D_STAIRS_final_0d2ffd2dc7.mp4?raw=true)** · [Contact sheet](final_CONTACT_SHEET.jpg) · [Trajectory CSV](MOTION_TRAJECTORY.csv)

Metric 3D hip/knee/ankle chains solve against explicit treads, not a diagonally translated sprite. Foot lift occurs before forward swing; landing precedes pelvis transfer/extension. Toe-off rotates the shoe and attached ankle around a fixed forefoot. Three risers and a trailing-foot follow are completed. Fixed camera.

Source: [physical_proofs.py](../../engine/animation/physical_proofs.py#L103), function `stair_state`; shared approved rig in [articulated.py](../../engine/animation/articulated.py). Preview and HD paths are recorded in `preview.json` and `final.json`.

Evidence: `JOINTS_TRAJECTORIES.json`, `JOINT_TRANSFORMS.json`, `CONTACT_EVENTS.json`, `final_CONTACT_SHEET.jpg`, `final_PLAYBACK.json` and normal/half-speed presented-frame sheets. Videos are intentionally silent to expose motion.

See [numerical validation](../../reports/physical-proof-validation.json) and [integration gate](../../reports/proof-integration-gate.json). Technical validation is separate from user artistic approval.
