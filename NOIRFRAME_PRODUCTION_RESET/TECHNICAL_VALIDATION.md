# Technical validation — completed native proofs

Technical checks pass for the delivered proof files. The artistic gate fails; see ARTISTIC_QUALITY_REPORT.md.

| Shot | Duration / frames | Native IK max | Actual prop max | Full decode | Browser playback |
|---|---|---|---|---|---|
| A | 5.0s / 150 | 0.1346mm | 0.00535mm | clean | 1× and0.5× ended |
| B | 7.8s / 234 | 0.1060mm | 0.00013mm | clean | 1× and0.5× ended |
| C | 8.0s / 240 | 0.0928mm | 0.00000mm | clean | 1× and0.5× ended |

All videos:1080×1920,30/1 FPS,H.264,yuv420p,AAC audio; every encoded video frame decoded with FFmpeg and counted with FFprobe. Native renderer completion records include source/HD .blend SHA256 and per-frame PNG hashes.

Normal playback host dropped-frame counts: A=6, B=0, C=2. All half-speed passes have zero dropped frames and all six passes report zero corrupted frames. The first normal pass overlapped other local review work. These are presentation drops, not missing encoded frames; frame counts and full decodes are clean. No zero-drop normal playback claim is made.

Ground stance controls: B/C0m consecutive planted displacement and0rad planted yaw change. A feet use the moving cabin support frame, so world travel is expected. Bone-length variation stays below0.003mm. A car24.05m,2→7.5m/s; wheel odometry error~0.0012mm. B hinge77°,12 sampled inserted-key frames. C3×0.2m risers and0.60m pelvis rise.

These samples validate actual evaluated bones/prop matrices, not just desired target coordinates. They do not prove mesh-surface collision freedom, convincing weight or model-sheet fidelity. No blanket collision-simulation pass is claimed. Curtain deformation uses authored shape keys, not a full cloth solver.

Audio: newly synthesized local Kokoro voice, original deterministic Foley, measured speech boundaries, contact-derived foot/hardware/fabric cues and speed-derived engine. Critical listening remains unverified. Sentence captions use script/WAV timing; Whisper inference did not run.

Preservation:4695 existing production files checked against SHA256 baseline,0 missing,0 changed. V10 and previous films are untouched.

Renderer: native Blender Workbench FXAA, flat material colors/object contours. Earlier Cycles/Freestyle previews are preserved. Workbench ignores the custom cloth shader and is not claimed to match V10 lighting/linework. Interrupted old Cycles outputs are excluded.

Full film: not generated because the artistic quality gate is not met. Native rigs, proof media, audit, source and explicit continuation are delivered instead.

Remotion review edit:624 video frames/20.8s at540×960. AAC packet padding extends the container duration to20.842667s; no extra video action is implied. The individual HD proofs retain their separately verified durations.
