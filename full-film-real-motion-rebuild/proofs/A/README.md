# Accelerator, 3 seconds

**[Play/download MP4](MOTION_PROOF_A_ACCELERATOR_final_9a1134d481.mp4?raw=true)** · [Contact sheet](final_CONTACT_SHEET.jpg) · [Trajectory CSV](MOTION_TRAJECTORY.csv)

A seated hip/knee/ankle chain approaches the pedal. A rigid shoe reaches contact at .75 s, then rolls about a planted heel while the pedal rotates 24 degrees. The linked torso/shoulders/head load and settle; both hands remain on the wheel. Fixed camera, no cuts.

Source: [physical_proofs.py](../../engine/animation/physical_proofs.py#L29), function `accelerator`; shared approved rig in [articulated.py](../../engine/animation/articulated.py). Preview and HD paths are recorded in `preview.json` and `final.json`.

Evidence: `JOINTS_TRAJECTORIES.json`, `JOINT_TRANSFORMS.json`, `CONTACT_EVENTS.json`, `final_CONTACT_SHEET.jpg`, `final_PLAYBACK.json` and normal/half-speed presented-frame sheets. Videos are intentionally silent to expose motion.

See [numerical validation](../../reports/physical-proof-validation.json) and [integration gate](../../reports/proof-integration-gate.json). Technical validation is separate from user artistic approval.
