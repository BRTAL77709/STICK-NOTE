# Delivery map

The project contains the complete 18-scene, 86-second review candidate, preserved original export, and a separate download encoding. Prior versions remain unchanged.

| Deliverable | Location |
|---|---|
| Movie | `renders/final/THE_PRICE_OF_SILENCE_MASTER_86s.mp4`; repository delivery copy `THE_PRICE_OF_SILENCE_MASTER_86s_DOWNLOAD.mp4` |
| Production bible and storyboard | `PRODUCTION_BIBLE.md`, `STORYBOARD.md`, `storyboard.json` |
| 18 scene sources | `scenes/scene_01/` through `scenes/scene_18/`; implementation `engine/composition/scene_builder.py` |
| Shared animation engine | `engine/`, `ANIMATION_SYSTEM.md` |
| Character assets and rigs | `assets/characters/`, `engine/animation/actor.py`, `driver_rig.py`, `v10_trunk.py` |
| Vehicles and motion | `assets/vehicles/`, `engine/animation/motion_state.py`, `vehicle.py` |
| Environments and city map | `assets/environments/`, `ENVIRONMENT_MAP.md`, `ROUTE_MAP.svg` |
| Prop interactions | `assets/props/`, `engine/animation/house17.py` |
| Camera/physics systems | `engine/camera/`, `engine/physics/`, `engine/api.py` |
| Editable HyperFrames project | `hyperframes/`, `build.sh`, `package.json` |
| English narration | `NARRATION_SCRIPT.md`, `narration-timing.json` |
| Narrator and caller audio | `assets/audio/NARRATOR.flac`, `CALLER.flac`, individual phrase WAV files |
| Mix, effects and music | `assets/audio/MIX_MASTER.flac`, `FX.flac`, `SCORE.flac`, `SOUND_CUE_SHEET.md` |
| Subtitles | `THE_PRICE_OF_SILENCE_EN.srt` |
| Motion graphics and style | `MOTION_GRAPHICS_SPEC.md`, `STYLE_SHEET.md`, `engine/graphics/` |
| Review images | `CONTACT_SHEET_18_SCENES.jpg`, `CONTACT_SHEET_FULL.jpg`, `ACTION_CONTACT_STRIPS.jpg` |
| Technical and artistic reports | `TECHNICAL_VALIDATION.md`, `ARTISTIC_QUALITY_REPORT.md`, `reports/` |
| Licenses | `ASSET_AND_LICENSE_REPORT.md`, `assets/licenses/`, local font/license notices |
| Reusable template | `NOIRFRAME_TEMPLATE.json` |

Binary runtimes and Kokoro model weights are not redistributed. The supplied phrase audio and composition media allow rebuilding without generating new speech. Local draft caches, private reference-study images and rejected intermediate audio are excluded from the repository delivery.
