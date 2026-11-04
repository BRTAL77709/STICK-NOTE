# Door and keys, 9 seconds

**[Play/download MP4](MOTION_PROOF_C_DOOR_KEYS_final_ea39f8ecaf.mp4?raw=true)** · [Contact sheet](final_CONTACT_SHEET.jpg) · [Trajectory CSV](MOTION_TRAJECTORY.csv)

Extended from five seconds for readability; the final half second holds the completed entry. Reach, lever grip/turn, failed pull and torso recoil precede pocket retrieval, key alignment/insertion/rotation/withdrawal, handle regrip, hinge opening and supported entry. Targets constrain the hand to actual hardware. The exterior camera stays fixed; wall/leaf depth masks the entering owner.

Source: [physical_proofs.py](../../engine/animation/physical_proofs.py#L66), function `door_state`; shared approved rig in [articulated.py](../../engine/animation/articulated.py). Preview and HD paths are recorded in `preview.json` and `final.json`.

Evidence: `JOINTS_TRAJECTORIES.json`, `JOINT_TRANSFORMS.json`, `CONTACT_EVENTS.json`, `final_CONTACT_SHEET.jpg`, `final_PLAYBACK.json` and normal/half-speed presented-frame sheets. Videos are intentionally silent to expose motion.

See [numerical validation](../../reports/physical-proof-validation.json) and [integration gate](../../reports/proof-integration-gate.json). Technical validation is separate from user artistic approval.
