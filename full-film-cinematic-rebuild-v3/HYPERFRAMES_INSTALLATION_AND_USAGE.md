# HyperFrames — verified installation and actual use

Installed package and CLI: **hyperframes 0.8.226**, verified from package.json and CLI --version. Official repository: https://github.com/heygen-com/hyperframes, packages/cli. Existing package path: /workspace/stick-note-dev/tools/node_modules/hyperframes. License: Apache 2.0. Local GSAP is version 3.15.0; its copyright header is preserved (https://gsap.com/standard-license/). No installation, clone retry or model download was necessary. The usage query returned unknown/no_subscription_login; rendering succeeded locally without a cloud subscription.

The bundled HyperFrames and HyperFrames CLI skills and their format, runtime, check and render references were read. The local telemetry/progress registry was inspected. Delivered counters use physical data rather than random character ticks.

## Engine responsibilities

| Layer | Engine |
|---|---|
| Illustrated world, rigs and vehicles | Existing Python SVG/librsvg renderer, with new V3 timing, POV and two-car corner; no baked HUD/captions |
| HUD counters, bars, clock, dial and pursuit | Actual HyperFrames HTML/GSAP driven by shared vehicle data |
| Captions and graphic entrances/exits | HyperFrames sub-composition with a registered paused GSAP timeline |
| Final picture/audio composition and encode | Official local HyperFrames CLI |
| Speech and sound | New local Kokoro candidates and original Python/FFmpeg mix, supplied as an audio track |

The Python renderer generates scene assets. It is not presented as HyperFrames. No fallback for HyperFrames was needed.

## Source and component proof

hyperframes/index.html declares the 15-second, 1080×1920, 30 FPS root, muted scene video, mixed audio and HUD/caption scene hosts. compositions/hud.html and captions.html use template roots, timed clips and matching composition/timeline IDs. Each registers a paused timeline through window.__timelines. hf-seek supplies deterministic time without timers or network clocks.

assets/components.js defines CinematicHUDPanel, AnimatedCounter, AnimatedProgressBar, DigitalClock, SpeedometerOverlay, PursuitDistanceHUD, IncomingCallInterface, MillionDollarOffer and InteractiveChoiceCards. Only time/speed/pursuit components appear in this chase. Future call/offer/choice helpers are source prototypes, not approved finished scenes.

vehicle-state.js contains 451 samples exported from the state that moves the cars. Initial/target fields derive from that data. Displayed values interpolate adjacent samples without independent arbitrary easing. GSAP easing controls UI entrances, while physical motion follows the shared model. The dial spans 0–140 km/h; the clock starts at 02:17:00; pursuit distance is Euclidean meters.

## Commands used

Set HYPERFRAMES_CLI to the installed hyperframes/bin/hyperframes.mjs. The actual local commands were:

```sh
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium node "$HYPERFRAMES_CLI" check hyperframes --json
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium node "$HYPERFRAMES_CLI" snapshot hyperframes --at 0.8,4.8,8.5,10.8,13.5 --json
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium node "$HYPERFRAMES_CLI" render hyperframes --fps 30 --quality looks --crf 20 --workers 1 --no-browser-gpu -o THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V3_15s.mp4
```

The same CLI rendered hyperframes-demo to HYPERFRAMES_HUD_DEMO_V3_FINAL.mp4: six seconds and 180 frames. It compresses the 15-second physical trajectory for component review. The final movie uses the real-time trajectory. The demo is not a substitute for integration: the final movie itself is official HyperFrames output.

Version, check, snapshot and render evidence appears in reports/. Official logs identify screenshot capture and software GPU rendering; no hardware GPU claim is made. All seven final check sections passed with zero errors/warnings. The motion-intent sidecar is included. Initial missing-mix/multiple-root issues were fixed by supplying the mix and separating the demo project. Clock overflow, small labels and a visually detected pursuit-label wrap were corrected before final rendering. Earlier files remain preserved locally.

The editable preview returned HTTP 200 at execution-environment-local http://localhost:4087/#project/hyperframes. This is not a public download URL. Reopen with the local CLI or the [HyperFrames desktop app](https://hyperframes.studio/studio/download?os=linux&src=cli). Source and MP4 delivery do not depend on that temporary server.
