# NOIRFRAME V12 — cinematic world/character proof rebuild

Status: four stand-alone proof shots for user review; not approved. No complete86-second V12 film.

Read [the supplied directive](specs/V12_REQUEST.md), [root causes and changes](ROOT_CAUSES.md), [storyboard](STORYBOARD.md), [technical report](TECHNICAL_REPORT.md) and [remaining visible defects](ARTISTIC_REVIEW.md).

| Shot | MP4 | Before/after |
|---|---|---|
| Staircase9.4s | [1080×1920](previews/STAIRS_V12_F01_1080.mp4) | [V11/V12](reviews/STAIRS_V11_V12_BEFORE_AFTER.mp4) |
| House17 13s | [1080×1920](previews/HOUSE_V12_F01_1080.mp4) | [V11/V12](reviews/HOUSE_V11_V12_BEFORE_AFTER.mp4) |
| Bedroom8.4s | [1080×1920](previews/BEDROOM_V12_F02_1080.mp4) | [V11/V12](reviews/BEDROOM_F02_V11_V12_BEFORE_AFTER.mp4) |
| Driving12s | [1080×1920](previews/DRIVING_V12_F03_1080.mp4) | [previous master/V12](reviews/DRIVING_F03_V11_V12_BEFORE_AFTER.mp4) |

Each main MP4 is30FPS H.264 with a quiet diagnostic AAC track. See reviews/ for actual decoded contact strips and browser-presented playback sheets. Source-only rebuilding creates a new output directory:

```sh
python source/rebuild.py --output /workspace/NOIRFRAME_V12_FRESH_BUILD --width 1080
```

Python/Numpy/Pillow/Cairo/librsvg and FFmpeg are used by the authoritative renderer. Blender's native spatial/IK companion is supplementary: `blender -b --factory-startup -t 2 --python source/export_blender.py`. It is not a promise that Blender itself reproduces the illustrated MP4s. Native IK view/skin polish and full Blender vehicle scene integration remain separate work. The Python source includes all vehicle, cloth and character channels.

Remotion editorial source is under editorial/; point its public files at the delivered clips and use existing Remotion4.0.419 dependencies. It is a review composition, not the approved film. HyperFrames is deferred until HUD work has a demonstrated purpose. All tooling is local/free; no paid API calls or new toolkit downloads.

Old project versions and the approved V10 trunk sequence are not changed. The V11 files remain rejected. See REPAIR_CHECKLIST.json for the review gate.

[Editable source archive](NOIRFRAME_V12_EDITABLE_SOURCE_R02.zip) contains the Python rig/world/render code, native Blender companion, Remotion project and documentation. MP4s are downloaded separately. The authoring sets share metre/Y-up conventions; continuous full-house bridges and final city/house integration remain pending, as stated in the artistic report.
