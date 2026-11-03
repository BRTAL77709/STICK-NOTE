# Actual HyperFrames use

Installed package and CLI: hyperframes 0.8.226, official repository https://github.com/heygen-com/hyperframes, Apache 2.0. Existing path: /workspace/stick-note-dev/tools/node_modules/hyperframes. Version metadata and actual CLI/check/render logs appear in reports/. No cloning or installation was needed. Usage is unknown because there is no subscription login; only local rendering was used.

The bundled HyperFrames/CLI skills and rendering, format, character, captions and review documentation were read. The caption-style registry was queried. Python generates the underlying illustrated animation only. HyperFrames/GSAP renders the clock, speed counter/needle/bar, tachometer, distance counter/bar, panel entrances/exits, transition rules and caption typography. The official HyperFrames CLI composes the scene video and WAV mix and encodes the final MP4. The final is not a custom renderer labeled HyperFrames.

The root mounts HUD and caption HTML templates and a muted scene video plus separate audio. Paused registered GSAP timelines and hf-seek drive deterministic playback. Exported vehicle-state.js contains 451 samples from vehicleState(t); every displayed value comes from those samples. UI entrances have independent easing; physical values do not have arbitrary count-up targets. The six-second demo compresses the same 15-second trajectory by 2.5× for component review.

components.js supplies panels, counters, progress bars, clock, speedometer and pursuit tracker. components-v4.js adds TachometerOverlay, AnimatedTransition and WordByWordCaptions. The word method accepts real timing records; production uses its phrase method because word alignment is unavailable. No fake exact word timings are supplied. Future offer/call/choice code inherited from V3 is not shown in the chase.

Clock, speed/RPM and pursuit panels enter in 0.24 seconds and exit in 0.16 seconds. The amber rule animates over 0.28 seconds. Gauge values, needles, engine and motion share the same state. Minor gauge labels were enlarged and moved inside the SVG, and the needle bounds were centered on the real hub to resolve audit findings. Motion assertions are included. Exact reference-image matching remains unverified because that image is inaccessible.

Actual command: `HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium node "$HYPERFRAMES_CLI" render hyperframes --fps 30 --quality looks --crf 20 --workers 1 --no-browser-gpu -o THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4`.

This is local screenshot capture/software GPU rendering. No hardware GPU or paid cloud claim is made. GSAP 3.15.0 is local and retains its copyright header; see https://gsap.com/standard-license/ . DejaVu font and Kokoro notices are supplied. See build.sh and README.md for editing instructions.
