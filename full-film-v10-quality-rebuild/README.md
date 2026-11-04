# THE PRICE OF SILENCE — V10 quality rebuild

An 86-second, 18-scene **review candidate**, repaired scene by scene from the existing illustrated animation project. 1080×1920, 30 FPS, H.264/AAC. No paid service or new model download.

The previous master and all earlier versions are preserved. Scenes 04–06 retain all 480 approved V10 picture frames and byte-identical HD inputs. Other scenes receive articulated driving, accelerator, car-exit/run, key/door, stair, curtain, phone and acting repairs. See `ACTION_BREAKDOWN.md` and `SCENE_REPAIR_REGISTER.md` for the actual choreography, limitations and evidence.

## Review files

- `renders/final/THE_PRICE_OF_SILENCE_V10_QUALITY_REBUILD_86s.mp4` — assembled review film (verify delivery status in `DELIVERABLES.md`).
- `CONTACT_SHEET_18_SCENES.jpg`, `CONTACT_SHEET_FULL.jpg`, `ACTION_CONTACT_STRIPS.jpg` — extracted from the encoded deliverable.
- `SCENE_REPAIR_REGISTER.json` — current preview/HD render paths and playback evidence.
- `REPLACEMENT_TIMELINE.json`, `storyboard.json` — unchanged 86-second timing.
- `TECHNICAL_VALIDATION.md`, `ARTISTIC_QUALITY_REPORT.md`, `REVIEW_INDEX.md` — findings and limits.
- `AUDIO_OUTPUT.json`, `AUDIO_CUE_SHEET.md`, `narration-timing.json`, `THE_PRICE_OF_SILENCE_EN.srt` — current mix/cue/phrase timing sources.

## Continue or reproduce locally

Use Python 3 with NumPy/Pillow and the existing librsvg/Cairo raster runtime, FFmpeg/ffprobe with libx264, Chromium and Playwright. HyperFrames is pinned to 0.8.226 in `package.json`; the local GSAP file and fonts are supplied. No hosted render or speech service is needed. The delivered phrase WAVs allow rebuilding the audio without model weights. Installed dependency binaries are not bundled.

Render an individual preview, review it, then render only that scene in HD:

```sh
python scripts/render_scenes.py --stage previews --scenes 11:11
python scripts/review_scene.py 11 --stage previews
python scripts/render_scenes.py --stage final --scenes 11:11
python scripts/review_scene.py 11 --stage final
```

Current caches are content-addressed; prior outputs are preserved. Source changes require renewed motion/contact review. Update the register using `scripts/checkpoint_scene.py` only after actual visual inspection. Contact checks are in `validate_driving_contacts.py`, `validate_pedal.py`, `validate_chase_cameras.py` and `validate_house_motion.py`.

```sh
python scripts/build_hyperframes.py --stage final
python scripts/check_candidate_content.py
python scripts/validate_source.py
# Run local HyperFrames check and review its results, then update FINAL_GATE.json.
HYPERFRAMES_CLI=/path/to/hyperframes/bin/hyperframes.mjs sh build.sh renders/final/NEW_REVIEW_NAME.mp4
python scripts/validate_media.py renders/final/NEW_REVIEW_NAME.mp4 NEW_REVIEW
python scripts/review.py renders/final/NEW_REVIEW_NAME.mp4
python scripts/review.py renders/final/NEW_REVIEW_NAME.mp4 --play --label NEW_REVIEW
```

To rebuild the audio, choose a new directory: `python engine/audio/mix_rebuild.py --out assets/audio-rebuild-v3`. Rebuild HyperFrames and renew timing/source gates afterward.

The export gate rejects changed active sources or HD inputs. Use a new filename; never overwrite previous renders. `engine/api.py` exposes active state; `ANIMATION_SYSTEM.md` identifies actual controllers. The preserved `../full-film-master-production/` documents describe the earlier version; the current repair register takes precedence.

## Remaining approval

Technical playback/contact validation is not artistic approval. Existing stock narrator/caller performances are retained; naturalness, emotional delivery and professional sound remain listening-unverified. Further production stops for user review of this candidate.
