# NOIRFRAME local video production toolchain

[Download the integration demo](renders/NOIRFRAME_TOOLCHAIN_INTEGRATION_DEMO.mp4?raw=true) · [Contact sheet](CONTACT_SHEET.jpg) · [Installation/versions](TOOL_INSTALLATION_REPORT.md) · [Validation](TECHNICAL_VALIDATION.md)

A separate seven-second evaluation: three seconds of articulated pedal contact, then four seconds of metric vehicle travel with a transparent HyperFrames HUD. The previous 86-second film and V1–V10 are preserved. This is a tool-compatibility demonstration, not artistic approval or a new film.

**Four tools have exercised their intended roles. Whisper is installed/import-tested, but transcription is blocked by missing model weights: both checked checkpoint routes returned proxy HTTP403. No Whisper-generated subtitle sample is claimed.** Actual speech is included, with explicitly named `script-reference.srt` captions timed from the supplied script and measured WAV duration. `reports/whisper-transcription.json` records that inference did not run. No reference media was downloaded.

## One clock, separate responsibilities

`shared/timeline.json` owns dimensions, FPS, scene frame ranges, voice offset and HUD offset. The approved Python evaluators in `animation/` solve joints/contacts, metric car odometry and camera projection. `scripts/export_shared.py` evaluates every frame into compressed SVG DOM plus joint/vehicle data. Remotion's React composition selects that exact frame geometry, rather than moving a held picture. HyperFrames reads the same state array and renders only a 920×300 transparent region for the four-second vehicle beat. FFmpeg places it at (80,140), starting on global frame90, adds speech/captions and encodes the final MP4. There is no competing full-film HyperFrames timeline. PREPARED_INPUTS.json seals the evaluated rig/clock/audio inputs; the rerender wrapper refuses stale state.

The car travels18 m, accelerates2→7 m/s and rotates tires by distance/0.32. The displayed km/h is the same speed×3.6. The pedal keeps its contact constraint. Installing either compositor does not replace the underlying physical rigs.

## Use the prepared demo

In this workspace the verified packages are reused through `remotion/node_modules`; Python tools are isolated in `.venv`, with an explicit `.pth` to the existing CPU runtime. These absolute runtime links are not portable deliverables. A fresh machine installs dependencies as described in [SETUP.md](SETUP.md).

```sh
# Re-render prepared inputs into a NEW output directory; existing jobs are refused.
./scripts/pipeline.sh my-new-review
# Inspect the editable HUD; local workspace access is required.
./scripts/hf.sh preview hyperframes --background --port 3217
# Actual ASR, only after a verified local Whisper checkpoint is available:
.venv/bin/python scripts/transcribe.py shared/narration.wav --offset 0.9333333333333333
# Verify the downloader without downloading anything:
.venv/bin/python scripts/reference_download.py --check
```

The HyperFrames desktop app can edit the HUD project locally: https://hyperframes.studio/studio/download?os=linux . Its optional model services are not used.

## Future stories

Read [FUTURE_STORIES.md](FUTURE_STORIES.md). Start a separate project, author actual actions and constraints, then prepare/render it. Preserve approved character assets. `animation/` includes reusable character, car, street, house, door/key, stairs, curtain/phone and trunk systems; the integration demo exercises only pedal/driving/HUD/speech timing. More scenes are not automatically animated because a new timeline is added. Existing full-film source, music and footage are never regenerated or downloaded by this setup.

## Files

- `remotion/`: pinned React composition, package.json/lockfile and compressed evaluated SVG geometry.
- `hyperframes/`: transparent seekable HUD, bundled GSAP/font, shared-state adapter.
- `animation/`: copied approved deterministic physical evaluators; original files unchanged.
- `shared/`: integer-frame timeline, joint/vehicle state and actual retained speech.
- `scripts/`: preparation, rendering, ASR, authorized reference import, assembly and QC.
- `reports/`: exact versions, successful renders, contact/clock/media checks and explicit model failures.
- `licenses/`: official terms/notices; Remotion's free use is eligibility-dependent.
