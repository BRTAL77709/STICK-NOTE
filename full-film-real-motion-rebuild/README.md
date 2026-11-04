[Review videos and evidence](DELIVERABLES.md) · [Technical validation](TECHNICAL_VALIDATION.md)

# THE PRICE OF SILENCE — real-motion rebuild

Current production: five independently rendered physical motion proofs followed by an integrated 86-second review candidate. Original master, rejected V10-quality rebuild and approved V10 are preserved. No paid API, model download or new runtime installation.

Start with [ANIMATION_FAILURE_AUDIT.md](ANIMATION_FAILURE_AUDIT.md). It identifies actual source behavior without pretending the rejected engine had no IK or world motion. The significant corrections are exposed contact acquisition, readable interaction timing, metric 3D stair steps, entry depth masking, distance-driven running contacts and more visible subject movement.

## Five motion proofs

- [A — accelerator, 3 s](proofs/A/README.md)
- [B — actual vehicle travel, 4 s](proofs/B/README.md)
- [C — door and keys, extended to 9 s](proofs/C/README.md)
- [D — three stairs, 4 s](proofs/D/README.md)
- [E — curtain/window, 4 s](proofs/E/README.md)

Each folder includes the current HD MP4 path in `final.json`, source references, a contact sheet, normal/half-speed playback evidence, `MOTION_TRAJECTORY.csv`, `JOINTS_TRAJECTORIES.json`, `JOINT_TRANSFORMS.json` and `CONTACT_EVENTS.json`. Old failed draft filenames are not the current selection. Clips are intentionally silent to expose movement.

## Integrated film

Read ACTION_BREAKDOWN.md, SCENE_REPAIR_REGISTER.md and ANIMATION_SYSTEM.md. Current scene paths are in `scenes/scene_XX/*-cache.json`. V10 clips are byte-identical copies; other clips are independently reviewed replacements. Runtime state is exposed by `engine/api.py`. Source is under `engine/animation/`; composition uses `engine/composition/`; sound uses `engine/audio/mix_rebuild.py`; overlays use local HyperFrames.

The film remains 86 seconds. Door/keys receive more time, stairs show three complete upper risers, and the curtain/phone get separate beats. A cut elides the lower stair flight; no full visible ascent is claimed. Vehicle dashboards are removed. Existing voice performances remain listening-unverified; only timing/mix/foley are rebuilt. Artistic approval is pending user review.

## Local reproduction

Existing free dependencies: Python, NumPy/Pillow, librsvg/Cairo, FFmpeg/ffprobe, Chromium/Playwright, HyperFrames 0.8.226 and local GSAP. No hosted rendering or speech API is needed. Voice clips, fonts and their notices are supplied; installed binary runtimes/model weights are not bundled.

```sh
python scripts/render_proofs.py --stage preview
python scripts/review_proofs.py --stage preview --play
python scripts/render_proofs.py --stage final
python scripts/review_proofs.py --stage final --play
python scripts/gate_proofs.py
python scripts/render_scenes.py --stage previews --scenes 12:13
python scripts/review_scene.py 12 --stage previews
python scripts/render_scenes.py --stage final --scenes 12:13
python scripts/review_scene.py 12 --stage final
python scripts/review_scene.py 12 --stage final --rate .5
```

Choose a new audio directory and output video name for revisions. Export gates require current proof, scene, contact, source, audio and composition validation before a new full render. See PROGRESS.md for actual delivery status. Never overwrite previous versions or describe a technical gate as artistic approval.
