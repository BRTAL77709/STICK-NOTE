# NOIRFRAME production reset — native animation proofs

**Status: technical proofs delivered; artistic gate not passed; full86-second rebuild incomplete.**

The new workflow uses actual Blender4.3.2 scenes, native armatures/weighted meshes/IK, metric environments, object contacts and cameras. It does not feed the rejected film or SVG pose images into Blender. All previous versions and the approved V10 sequence are preserved.

## Review the actual MP4s

- `renders/NOIRFRAME_SHOT_A_DRIVING_PROOF_R1.mp4` —5.0s,150frames.
- `renders/NOIRFRAME_SHOT_B_HOUSE17_PROOF_R1.mp4` —7.8s,234frames.
- `renders/NOIRFRAME_SHOT_C_STAIRS_WINDOW_PROOF_R1.mp4` —8.0s,240frames.

Each is native1080×1920,30FPS,H.264/yuv420p with AAC sound. They are test footage, not approved professional shots. Their exact hashes/decoding checks are in `reports/proof-media-validation.json`. The optional Remotion three-shot review edit is540×960 and adds source-script sentence captions; it is not the full film.

## Editable source and evidence

- `blender/SHOT_A_PROOF_R1_HD.blend`, `SHOT_B_PROOF_R1_HD.blend`, `SHOT_C_PROOF_R1_HD.blend`: native baked animation, rigs, environments, geometry and cameras.
- `source/`: authoring, native validation, rendering, audio synthesis, playback review and comparisons.
- `editorial/`: Remotion review composition and caption timing.
- `graphics/`: HyperFrames/GSAP clock, speed, pursuit, phone, offer and choice drafts; actual state binding only for speed.
- `audio/tests-v2/`: local licensed voice/original Foley mixes; cue and narration JSONs.
- `reviews/`: actual playback samples and old/new comparisons.
- `ANIMATION_ENGINE_AUDIT.md`, `TECHNICAL_VALIDATION.md`, `ARTISTIC_QUALITY_REPORT.md`, `BEFORE_AFTER.md`, `UPDATED_PIPELINE.md` and `docs/`: findings, limitations and exact continuation.

The car travels24.05m; wheel distance matches; fixed ground stance controls do not slide or spin; door hardware and curtain grip track actual transformed objects. These checks pass, but simplified silhouettes, flat lighting, stiff acting and insufficient fabric response fail the artistic gate. No new86-second master is rendered from a failed proof.

No paid services were used. Whisper inference remains unavailable because checkpoint downloads returned proxy403; captions are explicitly not ASR. No critical listening approval is claimed. A separately named CASH/SUSPICION reference could not be positively identified; the accessible supplied diamonds reference was not reused as footage.

Prior production preservation:4695 protected files checked,0 changed,0 missing. The local working folder retains earlier drafts and incomplete render attempts; only completed selected proofs are included in this delivery. See the delivery manifest for exact published file hashes.
