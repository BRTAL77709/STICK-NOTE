# NOIRFRAME / THE PRICE OF SILENCE — full 86-second film audit

**Source reviewed:** `THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4` (uploaded Nov 5, 2026). Analysis is based on the actual decoded video (86 one-second samples, additional 0.33–0.65-second motion strips around critical actions, and FFprobe/FFmpeg audio metrics), plus the connected `BRTAL77709/STICK-NOTE` GitHub repository's `work` branch. **Important limitation:** detailed subjective listening to narration and every sound cue was not completed; this report does **not** assert that vocal acting or individual SFX were audibly verified. No source code execution was performed in the user's Codex workspace.

## Technical facts (verified)
- 86.000 seconds; 2,580 frames; 1080×1920, portrait 9:16, 30 fps, H.264.
- AAC stereo at 48 kHz; file 16,677,566 bytes (~15.9 MiB), overall bitrate about 1.55 Mb/s.
- Measured integrated audio loudness approx **−16.0 LUFS**, true peak **−3.2 dBTP**. This shows overall level and absence of a full-scale peak, **not** voice naturalness, mix quality, audio-to-image sync or correct Foley.
- The connected production source (`work` branch, `NOIRFRAME_FULL_FILM_V1/TECHNICAL_REPORT.md`) confirms: frames **12–28 s are a pixel-identical copy of the existing V10 trunk action (480 frames)**; most original picture is preserved outside the 47–81.5 s replacement zone. The newly assembled file is not an entirely newly animated 86-second film.
- The source's `ARTISTIC_LIMITATIONS.md` admits differences between native Blender inserts and the baseline illustration, simplified silhouettes and hand work, mechanical performance, spatial discontinuity, stiff/flat curtain, and lack of critical listening verification.
- Motion differences are **not the same as good animation**. Rain particles, shifting text or zoom can make every adjacent frame technically different without convincing physical acting.

## Critical problems (ranked)

### P0 — structural / production failures
1. **Unequal animation craft**: trunk shot (12–28 s) was iterated through many versions; driving, door, stairs, window, phone and end card are much less convincing.
2. **Hybrid visual discontinuity**: original 2D illustrated shots and Blender-derived shots use different silhouette, hand, contour and lighting treatments (especially ~49–69 s).
3. **Action logic is not legible**: many shots display the character next to an object, but do not clearly show anticipation → contact → cause → object response → follow-through.
4. **Character performance repeatedly holds one silhouette/stance** instead of conveying distinct emotions and intent for danger, acceleration, fumbling for keys, panic, discovery and threat.
5. **Camera and picture do not consistently show the actual mechanism**: the foot/pedal shot (~28–31), door/lock (~51–55), stairs (~62–65), curtain/window (~65–69) fail to make contact and physical interaction easy to read.
6. **Overall continuity is preserved at an edit level but not necessarily at character/prop/environment level**; the same character looks differently rendered across shots and geography/door perspective changes.
7. **No demonstrated artistic approval gate**: technical verification was passed, yet the connected source explicitly acknowledges no full artistic approval; should not be promoted as production-ready.

### P1 — direction, motion and design
8. Repeated frontal driving composition across ~4–12 and ~37–40 s; insufficient visual variety and visible steering/driver response.
9. Very little visually readable body acceleration despite the story saying "I hit the gas" (~29–31 s).
10. Pedal/steering composition appears schematic and detached from a recognizable realistic/stylized vehicle cabin (~28–31 s); pedal is isolated rather than clearly mounted in a footwell.
11. Car pursuit lacks clear change in separation, convincing tire/road relationship and escalating danger (~32–45 s).
12. Street and house repetition weakens the sense of traveling across different blocks (~0–4, 32–45 and 47–49 s).
13. Road geometry and car perspective vary shot to shot; cuts do not provide a clear route map.
14. Rearview mirror reveal (~45–47 s) is visually understated, so "nothing in the mirror" is not a clear visual payoff.
15. Exterior character exiting the parked car around ~49 s has an overlap/scale problem; stepping and run-up lack a distinct, readable contact sequence.
16. Door/key shot (~51–55 s): a hand/handle is visible, but key insertion, key rotation and latch release cannot be clearly identified from the sampled frames.
17. Door interior (~57–60 s) has a sudden camera/geometry shift; exterior house number **17** remains visible high on the wall in the interior-looking shot, weakening geography.
18. Interior standing/half-crouched pose (~57–61 s) looks generic rather than a frightened character running in and securing a door.
19. Stair climb (~62–65 s): feet/hips appear to progress largely via translated poses; clear step-by-step loading, tread contact and pelvic rise are missing/weak.
20. Stairs environment and upper-floor route do not establish a physically connected second storey.
21. Window (~65–69 s): no clearly animated hand-to-fabric grip, moving curtain folds or curtain rod; view is revealed more like a visual state change.
22. Black sedan outside (~68–69 s) is not clearly established via full over-the-shoulder eyeline and spatial continuity from street to upper window.
23. Phone (~70–72 s): phone and call interface are too small relative to frame; incoming-call title is detached from the device.
24. Long phone exposition (~72–82 s) reuses nearly the same protagonist pose and background as counter, narration and warning change. The facial response, breathing, hand, eye and body acting do not develop meaningfully.
25. Money counter jumps through large values around ~72.6–74 s then sits at $1,000,000 through multiple seconds; not a cinematic reveal with cause, landing, reaction and timed exit.
26. Story text frequently carries information that should be shown by actions: "I hit the gas", "The lid shut", "Upstairs", etc.
27. The finale choice card lasts about **82–86 s (4 s)**, whereas the original 18-scene plan allocated **80–86 s (6 s)**. The final choice needs adequate reading time and visual emphasis.
28. End-card is comparatively static and could benefit from restrained sequenced entrances for question, A, B, and CTA (not constant motion).
29. Mobile caption/title sizes and the placement of top/bottom text require UI-safe-area verification against TikTok, Reels and Shorts; this was not independently tested on the platform.

### P2 — sound and motion graphics (verification boundaries)
30. The source reports Kokoro TTS voice **`bm_daniel`**, but *critical listening and subjective voice performance were not verified*. User dissatisfaction with the voice is credible feedback; raw file metadata cannot settle it.
31. Sound cue synchronization for wheel movement, foot/pedal, trunk contact, key/lock, stair foot plants, fabric, phone pickup and threat has not been established by audio-visual event-by-event listening in this review. Mark **needs audition**, not factually absent.
32. -16 LUFS and -3.2 dBTP are technically reasonable average/output measurements but say nothing about narration's emotional phrasing, caller voice distinctness, Foley realism or music ducking.
33. Source acknowledges that no Whisper-derived or precise word-level alignment was verified; captions appear primarily phrase/sentence based.
34. HUD treatment (clock, monetary offer, unknown caller) is inconsistent across scenes and does not yet match the supplied CASH/SUSPICION reference's refined hierarchy, progress bars and controlled easing.
35. More counters alone would worsen readability. HUD must be anchored to a story event and share actual timeline data (e.g. actual car speed, not arbitrary values).
36. Overall bitrate around 1.55 Mb/s may make fine rainy outlines and dark gradients vulnerable to compression; check higher-quality H.264 CRF export once the motion itself is fixed. Higher bitrate cannot fix acting.

## Timecoded scene-by-scene repair register

| Time | Observed problem | Concrete repair / proof |
|---|---|---|
| 00–04 | Opening city/road looks schematic; weak event-based visual hook; mostly environment/camera view. | One motivated road-level shot: passing tires, perspective-correct motion, wet reflection reaction, controlled 2:17 AM reveal. |
| 04–08 | Frontal driver in similar held pose. | Head/eyes/mirror action, hand steering constraints, moving streetlight illumination, driver body load. |
| 08–12 | Driver reacts but shot remains similar composition; alley action delayed. | Eyeline POV and car braking insert, then match cut to what he actually sees. |
| 12–18 | Stronger existing V10 choreography, but criminals/victim relatively small, hands/weight difficult to read. | Preserve existing V10; improve only with validated new source and separate comparison, no accidental regression. |
| 18–24 | Lift/loading poses are hard to read in rear-of-car perspective; victim-body support and contact merit close inspection. | Preserve V10 if preferred; inspect silhouette, ground anchors, gripping hands, victim arc, trunk opening and occlusion. |
| 24–28 | Closure/head turn is the clearest acting moment; limited bridging to driver's reaction. | Preserve turn, use eyeline match to driver and a reaction sound. |
| 28–32 | Schematic side view of pedal and steering; acceleration poorly felt; pedal not embedded in recognizable car interior. | Build a real footwell with ankle/pedal contact; link throttle to vehicle displacement, engine pitch, driver load and road flow. |
| 32–37 | Pursuit image does not clearly communicate gap change and escalation. | Two identifiable cars in shared world coordinates; distance changes evident in shot without HUD. |
| 37–40 | Repeated frontal driver view and limited performance variation. | Short mirror/head reaction, turn anticipation, steering torque, shoulder counter-movement. |
| 40–45 | Exterior road shots are stylized but speed, cornering, wheel contact and route need stronger spatial logic. | World-space car path, wheel rotation, tire tracks, camera track, parallax, grounded intersection geography. |
| 45–47 | "Nothing in the mirror" information is largely narration-driven. | Clear mirror insert, empty road, driver visibly checks and briefly relaxes. |
| 47–51 | House/car/character exit and run look spatially awkward. | Driver door opening, both feet on ground, shut door, run from parked sedan to door; one continuous coordinate map. |
| 51–55 | Lock action not physically legible at normal viewing size; key shaft/hand contact is missing or obscured. | Enlarged insert with failed handle turn, pocket, key grip, insertion, twist, latch feedback. |
| 55–62 | Exterior-to-interior handoff, door geometry, character stance and pace feel inconsistent. | Shared door rig and opening direction in both angles, actual threshold crossing, door closure/lock and transition to stairs. |
| 62–65 | Stair climb looks mostly like repeated walk poses translated over steps. | IK plus per-tread planted contacts, hip rise, weight transfer, one visible step at a time. |
| 65–69 | Window/curtain doesn't visually show physical fabric being pulled; black car revealed rather than genuinely seen. | Curtain mesh/shape and rod; hand grip; folds; accurate over-the-shoulder view and character recoil. |
| 70–72 | Call UI and device are under-scaled; pickup less convincing than large caption. | Phone close-up: vibration, reachable table, grip, answer UI, raise to ear. |
| 72–78 | Dollar figure animates quickly; protagonist's figure largely static as threat escalates. | Timed money HUD in the supplied reference style, narrator pause and visible physical shock/decision. |
| 78–82 | Threat phase reuses same framing/pose; little physical reaction to "we know where you live". | Change shot to window/car, close phone-grip, eye and shoulder recoil, room tension, sound perspective. |
| 82–86 | A/B end card fairly static, only ~4 s. | Controlled sequential reveal, CTA safe zone, sufficient hold; recover the original 6 s ending if retaining 86-s target. |

## What the three linked GitHub projects can actually contribute

### ClaudeAnimationBase — **most relevant to character acting**
`https://github.com/JohnHeibel/ClaudeAnimationBase`
- p5.js/p5.brush illustrated character kit with key views, emotions, event-driven shot design, pure functions of time, render/contact-strip/crop review and animation principles.
- Relevant insights: cause then reaction, anticipation, weight, arcs, asynchronous parts, strong key poses, reader timing, contact-sheet plus frame-strip QA.
- MIT-licensed. Do **not** copy its default Clawd character/design or its no-text-only rule into NOIRFRAME. Use the engine/rigging ideas while preserving the approved stickman assets and captions.
- It is not a drop-in replacement for the already rendered footage. A proper rig adaptation and performance animation are still required.

### Onetake — **relevant to continuity, rhythm and camera/motion-graphics language**, not main character rigging
`https://github.com/feitangyuan/onetake`
- Skill's central concept is *carry across a beat*: an object or camera movement survives into the next event, avoiding random title/scene replacement. Has reference-analysis, motion library, quality verification, shutter motion blur and event-based sound principles.
- Optimized for short motion/promo films, not an 86-s crime-acting pipeline. Do not demand a literal single take for this thriller: motivated cinematic cuts are legitimate.
- **CRITICAL LICENSE: PolyForm Noncommercial 1.0.0.** The free code is for noncommercial use only. Since NOIRFRAME may be used for public/promotional/monetized social content, **do not copy its library/source into a commercial production** without a suitable license. General cinematography concepts and independently authored approaches can be studied.

### VOX-COLLAGE-BROLL — **optional stylized cutaways only**
`https://github.com/MegaTroll222/VOX-COLLAGE-BROLL`
- MIT skill for 5-second paper-collage editorial explainer B-roll, first/end-frame staging, multi-gate review and frame QA.
- Requires MaxFusion MCP to generate media (or alternate Google AI Studio / ElevenLabs API integrations). This **does not establish a $0 production path**. No API keys or paid services are authorized here.
- The halftone photo-collage aesthetic conflicts with our approved dark illustrated stickman film if applied globally. Consider only as an optional brief conceptual cutaway after explicit stylistic approval; otherwise do not use.

## Real root cause, based on GitHub source
- On `work`, the project metadata confirms **12–28 s was copied identically from V10**; new 86-second output is largely an edit assembled from older picture plus limited Blender replacements.
- `ARTISTIC_LIMITATIONS.md` already documents simplified silhouettes/hands, inconsistent Blender vs illustration lighting, mechanical action, a physically incomplete House-17 upstairs plan and a sheet-like curtain.
- `SOURCE_AND_REBUILD.md` explicitly says simply rebuilding the assembly **cannot improve animation**; the Blender shots would have to be reanimated/rerendered as source clips.
- `TECHNICAL_REPORT.md` explicitly says subjective critical listening wasn't performed.
- The current public `main` branch holds essentially just README and ZIP, while the actual developed project is on **`work`**. Future Codex work must target and preserve `work` or a new branch from `work`, not assume `main` is up to date.

## Recommended repair approach

**Do not add five tools and rerun the same build script.** First build genuine artistic proofs with clear mechanical anchors using `ClaudeAnimationBase` principles and/or suitable existing rig code. Keep V10 unchanged. Fix the worst cinematic actions (door/keys, stairs/curtain, pedal/chase, phone), then integrate scene-level renders into the film. Use Remotion/HyperFrames only for correctly timed composition/graphics, FFmpeg for assembly and audio, and a separately quality-approved narration workflow. Every repaired scene needs a visible original-vs-new video comparison, source project, event/contact timeline and reviewer approval.

**Stop conditions:** If a scene remains visibly mechanical at normal-speed playback, do not describe it as fixed because FFprobe passes. Preserve work and report the specific unsolved issue.

## Evidence used
- User-uploaded 86-s MP4; 1-s contact boards at `film_00_21.jpg`, `film_22_43.jpg`, `film_44_65.jpg`, `film_66_85.jpg`, with detailed strips for trunk, gas pedal, door, stairs/window, and phone; FFprobe and EBU R128 audio analysis.
- GitHub: `https://github.com/BRTAL77709/STICK-NOTE/tree/work/NOIRFRAME_FULL_FILM_V1` with `ARTISTIC_LIMITATIONS.md`, `TECHNICAL_REPORT.md`, `SOURCE_AND_REBUILD.md`, `STORYBOARD_18_SCENES.json`.
- Original README, skill, animation guide and license in the three provided public GitHub repositories.
