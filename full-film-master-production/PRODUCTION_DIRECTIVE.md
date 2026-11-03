# THE PRICE OF SILENCE
# ULTIMATE MASTER PRODUCTION DIRECTIVE
## Complete Cinematic Animation Studio — STICK-NOTE / NOIRFRAME
### Read this entire document before writing code, editing, generating audio, or rendering.

---

# 0. THE MOST IMPORTANT INSTRUCTION

This is not another request for minor improvements.

The user has repeatedly rejected previous full-film and 15-second outputs because they do not resemble a professionally directed animated film.

The recurring failures are:

- Static illustrated scenes instead of genuine animation
- Sliding sprites instead of convincing world-space movement
- Repeated backgrounds instead of connected environments
- Mechanical character poses instead of physical acting
- Cars that appear stationary while dashboard numbers change
- Unconvincing acceleration and pursuit
- Incorrect interactions with doors, keys, windows, curtains, cars and phones
- Poor narration and generic synthetic voices
- Weak sound design and missing synchronization
- Basic captions instead of professionally animated typography
- Generic HUD panels instead of premium cinematic motion graphics
- Repeated low-quality renders with only superficial changes
- Claims of completion based on valid MP4 metadata rather than artistic quality

**Do not repeat these failures.**

Your job is to create a reusable, professional animation-production system and use it to produce the complete 86-second film THE PRICE OF SILENCE.

You must address all known requirements without repeatedly asking the user to restate them.

Do not pretend that a longer prompt guarantees a better film. Demonstrate improvements through actual rendered motion, measured checks and honest review.

---

# 1. PROJECT IDENTITY

Repository:

`BRTAL77709/STICK-NOTE`

Publishing brand:

`NOIRFRAME`

Film:

`THE PRICE OF SILENCE`

Format:

- Vertical 9:16
- 1080 × 1920
- 30 FPS
- 86 seconds
- 2,580 frames
- H.264 MP4
- English narration and dialogue
- English animated captions
- Cinematic 2D / 2.5D illustrated stickman animation
- Crime / mystery / suspense
- Additional tool and service budget: $0

The movie is intended for TikTok, Instagram Reels and YouTube Shorts.

The film must be original.

Use appropriately licensed assets, music, effects, fonts and software.

No paid API, subscription or service may be added without explicit authorization.

---

# 2. NON-NEGOTIABLE CREATIVE DIRECTION

The user wants the visual quality of a professionally directed illustrated thriller.

Preserve the approved aesthetic:

- Dark navy and teal
- Amber streetlights
- Rainy nighttime environments
- Wet asphalt reflections
- Bold illustrated outlines
- Expressive white eyes
- Stylized stickman characters
- Layered backgrounds
- Cinematic composition
- Suspenseful lighting
- Controlled motion graphics

The characters must remain illustrated stickmen.

Do not replace them with photorealistic humans.

Do not turn the film into realistic 3D character animation.

Do not redesign the approved characters without a clear reason.

The best existing V10 crime sequence is the main visual and character reference.

Preserve V10 and all earlier versions.

Previous V1–V4 integrated production tests are references for identifying failures, not proof of acceptable quality.

---

# 3. FULL PRODUCTION ARCHITECTURE

Create a new project area:

`full-film-master-production/`

Recommended structure:

```text
full-film-master-production/
├── README.md
├── PRODUCTION_BIBLE.md
├── STORYBOARD.md
├── STYLE_SHEET.md
├── AUDIO_DIRECTION.md
├── MOTION_GRAPHICS_SPEC.md
├── ANIMATION_SYSTEM.md
├── ENVIRONMENT_MAP.md
├── QUALITY_GATES.md
├── CHANGELOG.md
├── assets/
│   ├── characters/
│   ├── vehicles/
│   ├── environments/
│   ├── props/
│   ├── fonts/
│   └── audio/
├── engine/
│   ├── animation/
│   ├── camera/
│   ├── characters/
│   ├── vehicles/
│   ├── environments/
│   ├── lighting/
│   ├── particles/
│   ├── physics/
│   ├── graphics/
│   ├── audio/
│   └── composition/
├── scenes/
│   ├── scene_01/
│   ├── scene_02/
│   ├── scene_03/
│   ├── scene_04/
│   ├── scene_05/
│   ├── scene_06/
│   ├── scene_07/
│   ├── scene_08/
│   ├── scene_09/
│   ├── scene_10/
│   ├── scene_11/
│   ├── scene_12/
│   ├── scene_13/
│   ├── scene_14/
│   ├── scene_15/
│   ├── scene_16/
│   ├── scene_17/
│   └── scene_18/
├── renders/
│   ├── previews/
│   ├── approved/
│   └── final/
├── reports/
└── scripts/
```

Use existing project conventions when appropriate.

Do not reorganize or delete working source code unnecessarily.

---

# 4. REQUIRED TOOLCHAIN

Evaluate and use tools according to their actual capabilities.

## HyperFrames

https://github.com/heygen-com/hyperframes

Primary candidate for:

- Animated typography
- Cinematic HUDs
- Numerical counters
- Progress bars
- Animated timestamps
- Speedometer overlays
- Phone interfaces
- Offer graphics
- Final decision cards
- Graphic transitions

Inspect actual documentation and APIs.

Do not fabricate successful integration.

If HyperFrames is unavailable due to blocked downloads, record the failure and use a clearly identified alternative.

## Lemo-Opuscar

https://github.com/lemomo-ai/lemo-opuscar

Evaluate compatible code-driven filmmaking techniques for:

- Deterministic rendering
- Camera choreography
- 2.5D scene construction
- Hierarchical transforms
- Layered depth
- Character rigs
- Cinematic composition

Do not assume that a framework alone guarantees quality.

## FFmpeg

https://ffmpeg.org/

Use for:

- Rendering and encoding
- Video assembly
- Audio mixing
- Transitions
- Technical validation
- Contact sheets
- Scene-level caching

## Whisper

https://github.com/openai/whisper

Use for transcription and subtitle timing when actual speech audio requires recognition.

## Kokoro TTS

Evaluate for free/local English narration.

Use only if available and compatible with the environment.

## ElevenLabs

https://elevenlabs.io/

Evaluate only if authorized and accessible within the user's budget.

Do not request or fabricate API keys.

## Additional tools

You may use Blender, SVG animation, Canvas, WebGL, GSAP, Remotion, Python or other compatible free tools where technically justified.

Choose tools based on actual rendered results, not popularity.

Do not install redundant dependencies.

Do not repeatedly retry blocked network access.

---

# 5. ANIMATION ENGINE — THE CORE PROBLEM

The previous films failed because objects were positioned but not convincingly animated.

Build a deterministic animation system where scene state is evaluated at time t.

Example conceptual interfaces:

```text
characterState(characterId, t)
vehicleState(vehicleId, t)
cameraState(t)
environmentState(t)
propState(propId, t)
lightingState(t)
graphicsState(t)
audioEvents(t)
```

The system must maintain:

- World-space coordinates
- Parent-child transforms
- Local joint transforms
- Character scale
- Contact constraints
- Temporal continuity
- Velocity
- Acceleration
- Orientation
- Camera projection
- Depth ordering
- Occlusion

Do not move an entire character as one rigid sprite when the action requires articulation.

Do not use camera zooms to disguise missing motion.

Do not teleport characters between poses.

Do not independently animate components that must physically interact.

---

# 6. CHARACTER RIGGING AND ACTING

Build reusable hierarchical stickman rigs.

Required body controls:

- Head
- Neck
- Torso
- Pelvis
- Upper arms
- Forearms
- Hands
- Thighs
- Shins
- Feet
- Eyes
- Eyebrows where appropriate
- Clothing elements

Use inverse kinematics or appropriate constrained animation for hand and foot contacts.

### Walking

Each walking cycle must contain:

- Contact
- Weight acceptance
- Passing pose
- Push-off
- Swing
- Foot planting
- Pelvis translation
- Torso compensation
- Arm counter-swing

Feet must not slide during planted phases.

### Running

Use stronger forward lean, longer stride, faster weight transfer and appropriate airborne phases.

### Fear

Show:

- Eyes widening
- Shoulder tension
- Faster breathing
- Hesitation
- Sudden reactions
- Head and torso coordination

### Looking

A head turn must include real orientation change, not merely pupils moving sideways.

The cap brim, face silhouette and eye perspective must respond to head rotation.

### Hand interactions

Hands must remain attached to held objects.

Objects must follow physically plausible paths.

Use clear grip and release events.

---

# 7. CRIME SEQUENCE — PRESERVE V10

The V10 sequence is the strongest existing animation reference.

Do not rebuild it unnecessarily.

The scene contains:

- Two masked criminals
- An injured victim
- A black sedan
- A rear trunk
- A rainy alley
- A criminal turning toward the witness

Preserve approved visual designs and successful motion.

Where feasible, correct obvious continuity problems without destroying the original baseline.

Required action order:

1. Criminals drag the victim.
2. They reach the sedan.
3. The trunk opens.
4. They reposition their grips.
5. They lift the victim.
6. The victim enters the trunk.
7. They release him.
8. The trunk closes completely.
9. The latch engages.
10. Only then does Criminal 01 turn toward the witness.

Do not reverse the action order.

Keep the action non-graphic.

---

# 8. COMPLETE CITY AND ENVIRONMENT DESIGN

The city must be a connected illustrated world.

Create a coherent geographic layout containing:

- Main road
- Side streets
- Alley
- Intersections
- Residential neighborhood
- House 17
- Pursuit route
- Escape route

Maintain consistent screen direction and spatial geography.

### Roads

Include:

- Road geometry
- Perspective
- Lane markings
- Curbs
- Sidewalks
- Drains
- Puddles
- Reflections
- Intersections
- Turns
- Road elevation where appropriate

Road markings must move correctly relative to the vehicle and camera.

### Buildings

Include:

- Different building silhouettes
- Doors
- Windows
- Frames
- Rooflines
- Architectural depth
- Lit and unlit windows
- Distinct street-facing surfaces

Do not duplicate the same house or building arrangement throughout the entire city.

### Atmosphere

Include:

- Rain
- Fog
- Wet pavement
- Streetlight illumination
- Moving reflections
- Wind
- Distant city ambience
- Foreground and background depth

Atmosphere must support visibility, not obscure all action.

---

# 9. HOUSE 17 — COMPLETE ARCHITECTURE

House 17 must have consistent exterior and interior geometry.

Required exterior:

- Front steps
- Door
- House number 17
- Door frame
- Handle
- Lock
- Windows
- Roof
- Exterior light
- Sidewalk
- Street connection

Required interior:

- Entrance
- Hallway
- Stairs
- Upstairs room
- Window
- Curtains
- Curtain rod
- Bed or furniture
- Interior lamp
- Doorways
- Consistent spatial relationship to exterior

### Door interaction

Animate:

1. Character reaches handle.
2. Handle turns.
3. Door fails to open.
4. Character reacts.
5. Character takes out key.
6. Key aligns with keyhole.
7. Key enters lock.
8. Key rotates.
9. Lock releases.
10. Door opens on hinges.
11. Character enters.
12. Door closes.
13. Character locks door.

Use believable timing and hand contact.

### Window interaction

Animate:

1. Character approaches window.
2. Reaches curtain.
3. Grips fabric.
4. Pulls curtain aside.
5. Fabric folds move.
6. Character looks outside.
7. Black sedan is revealed.
8. Character reacts.

Do not show a car pasted inside a window rectangle.

---

# 10. VEHICLE SYSTEM — ACTUAL DRIVING

Create reusable vehicle rigs.

Each vehicle should include:

- Body
- Wheels
- Wheel rotation
- Steering
- Suspension
- Headlights
- Taillights
- Windows
- Mirrors
- Interior dashboard
- Steering wheel
- Accelerator pedal
- Speedometer

Define coherent motion using position, velocity, acceleration and heading.

The car must actually travel through world space.

The environment must react to camera and vehicle motion.

### Acceleration

Communicate acceleration through:

- Increasing road-flow speed
- Passing buildings
- Faster streetlight motion
- Wheel rotation
- Engine pitch
- Vehicle pitch
- Driver body response
- Camera tracking
- Dashboard instruments

The speedometer must not be the only indication of acceleration.

### Speedometer

Use a consistent unit such as km/h.

Numbers and needle must match modeled vehicle speed.

No arbitrary speed jumps.

No disconnected speed HUD.

### Rearview mirror

The mirror must show the pursuing car in the correct relative position.

Its apparent size and placement should change coherently with distance.

### Cornering

Show:

- Steering input
- Heading change
- Road curvature
- Body roll
- Wheel orientation
- Camera tracking
- Environmental perspective

Do not rotate the car over an unchanged background.

---

# 11. CINEMATOGRAPHY

Direct every shot with a specific narrative purpose.

Use:

- Establishing shots
- Tracking shots
- Low-angle road shots
- Interior driver shots
- Over-the-shoulder shots
- Rearview mirror shots
- Close-ups
- Reaction shots
- POV shots
- Object inserts
- Suspenseful reveals

Maintain:

- Clear geography
- Character eyelines
- Screen direction
- Camera continuity
- Motivated movement
- Readable action

Do not create a movie from one static image per scene.

A scene may contain multiple shots and meaningful action beats.

Do not overuse zooms, camera shake or fast cuts to conceal animation problems.

---

# 12. PREMIUM MOTION GRAPHICS

The user supplied a reference featuring:

- CASH — $20,000,000
- SUSPICION — 43%
- Orange progress bar
- Dark translucent panels
- Bold numerical typography
- Thin orange outlines

This reference defines the visual design language.

It does not define the story's actual numerical values.

### Required design system

- Deep navy translucent backgrounds
- Amber/orange accents
- Crisp white values
- Compact uppercase labels
- Clean spacing
- Smooth easing
- Precise timing
- Mobile readability
- Subtle entrance and exit animation

### Required components

- Animated clock
- Numerical counter
- Progress bar
- Speedometer
- Pursuit distance tracker
- Incoming call interface
- Million-dollar offer counter
- A/B decision cards
- Animated captions

### Required behaviors

Numbers must interpolate over time.

Bars must fill or empty smoothly.

Panels must enter and exit intentionally.

Every graphic must be synchronized with the story.

Do not use random decorative badges.

Do not clutter the frame.

Use HyperFrames where actually available and appropriate.

---

# 13. CINEMATIC ENGLISH NARRATION

The current narration quality is rejected.

Target:

- Natural male English narrator
- Warm, deep voice
- Intimate storytelling
- Suspenseful delivery
- Emotional variation
- Strategic pauses
- Clear pronunciation
- No robotic cadence
- No exaggerated announcer tone

The anonymous caller must sound distinct.

The caller should be calm, unsettling and controlled.

Use appropriate telephone filtering.

Evaluate available high-quality voice engines.

Do not assume a tool is available without checking.

Do not claim the voice is acceptable merely because a WAV or AAC file exists.

Use a natural narration script and synchronize it to the film.

---

# 14. SOUND DESIGN

Create a full sound cue sheet.

Required sounds:

- Rain
- Wind
- Distant traffic
- Engine idle
- Engine acceleration
- Wet tires
- Wheel movement
- Footsteps
- Clothing movement
- Trunk opening
- Trunk closure
- Trunk latch
- Keys
- Door handle
- Lock
- Door closing
- Curtain movement
- Phone vibration
- Phone ringing
- Telephone ambience
- Suspense music
- Cinematic impacts

Synchronize sounds to visible events.

Engine pitch must respond to vehicle speed.

Trunk latch sound must occur at actual closure.

Keys must sound when handled.

Phone vibration must occur when the phone vibrates.

Keep narration intelligible.

Avoid clipping and abrupt changes in loudness.

Use only original or appropriately licensed audio.

---

# 15. CAPTIONS AND TYPOGRAPHY

Create a consistent English caption system.

Use:

- Large mobile-readable typography
- High contrast
- Selective amber emphasis
- Word-level or phrase-level animation
- Actual narration timestamps
- Consistent placement
- Platform-safe margins

Do not cover faces, important actions, phone interfaces or final decision cards.

Use Whisper when transcription is needed.

For generated narration, synchronize captions to the actual audio.

---

# 16. COMPLETE STORY — 18 SCENES

The film must contain the following story structure.

| Scene | Time | Action |
|---|---|---|
| 01 | 00:00–00:04 | 2:17 AM, rainy neighborhood |
| 02 | 00:04–00:08 | Protagonist driving |
| 03 | 00:08–00:12 | Suspicious movement |
| 04 | 00:12–00:18 | Criminals drag victim |
| 05 | 00:18–00:24 | Victim loaded into trunk |
| 06 | 00:24–00:28 | Trunk closes, criminal notices witness |
| 07 | 00:28–00:32 | Protagonist panics |
| 08 | 00:32–00:37 | Black sedan follows |
| 09 | 00:37–00:42 | High-speed escape |
| 10 | 00:42–00:47 | Pursuer appears gone |
| 11 | 00:47–00:51 | Arrival at House 17 |
| 12 | 00:51–00:55 | Locked door and keys |
| 13 | 00:55–00:59 | Protagonist enters |
| 14 | 00:59–01:03 | Curtain and window reveal |
| 15 | 01:03–01:07 | Unknown caller |
| 16 | 01:07–01:14 | $1,000,000 offer |
| 17 | 01:14–01:20 | Threat and warning |
| 18 | 01:20–01:26 | Audience decision |

The total duration must remain 86 seconds.

---

# 17. DETAILED SCENE EXECUTION

## Scene 01 — Opening

Start with wet pavement and reflected headlights.

Camera reveals a rainy neighborhood.

The protagonist's car travels through the environment.

Display 2:17 AM with a restrained animated timestamp.

Create immediate curiosity.

## Scene 02 — Driver

Animate hands, steering wheel, shoulders, eyes and head.

Show rain on windshield and passing lights.

The car must visibly travel.

## Scene 03 — Discovery

The protagonist notices movement.

He slows down.

Eyes and head turn.

Camera reveals the suspicious alley.

## Scene 04 — Dragging

Use approved V10-style staging.

Criminals physically drag the victim.

Show contact, weight and movement.

## Scene 05 — Trunk

Trunk opens.

Criminals lift victim.

Victim enters.

Hands release.

No teleportation or unnatural flipping.

## Scene 06 — Witness spotted

Trunk closes.

Latch clicks.

Criminal turns head toward protagonist.

Build threatening eye contact.

## Scene 07 — Panic

Protagonist reacts.

Foot presses accelerator.

Hands grip wheel.

Car begins accelerating.

## Scene 08 — Pursuit

Black sedan enters the road.

Headlights approach.

The distance between vehicles changes.

## Scene 09 — Escape

Use moving streets, dashboard, rearview mirror and exterior shots.

Speedometer climbs in synchronization with actual vehicle speed.

Show sharp cornering.

## Scene 10 — False safety

The protagonist reaches his neighborhood.

Pursuing headlights disappear.

The car slows.

A brief moment of relief.

## Scene 11 — House 17

The protagonist exits the car.

Runs to the house.

House number 17 is readable.

## Scene 12 — Locked door

Show actual hand, key, lock and door interaction.

Create tension through the failed first attempt.

## Scene 13 — Inside

He enters.

Closes door.

Locks it.

Moves toward the stairs.

## Scene 14 — Window

He reaches upstairs.

Parts the curtain.

Sees black sedan outside.

Reacts with fear.

## Scene 15 — Phone

Phone vibrates.

UNKNOWN CALLER appears.

He hesitates and answers.

## Scene 16 — Offer

Caller offers $1,000,000 for silence.

Use a premium animated money counter.

Show the protagonist reacting.

## Scene 17 — Warning

Caller threatens him if he contacts police.

The protagonist looks toward the window.

Maintain suspense.

## Scene 18 — Choice

Display:

WHAT WOULD YOU DO?

A — TAKE $1,000,000

B — CALL THE POLICE

COMMENT A OR B FOR PART 2

Make the final decision screen readable and cinematic.

---

# 18. EDITING AND PACING

The film must feel deliberately edited.

Avoid long static holds.

Avoid repetitive framing.

Use shot changes motivated by:

- Character reactions
- New information
- Physical action
- Sound cues
- Suspense
- Narrative reveals

The opening must hook viewers quickly.

The chase must feel urgent.

The house sequence must feel tense.

The phone call must feel threatening.

The ending must encourage audience participation without becoming visually cluttered.

---

# 19. PRODUCTION QUALITY GATES

Do not blindly rerender the full film.

Use the following internal quality gates.

### Gate A — Motion engine

Prove that vehicles and characters can move convincingly in a continuous shot.

### Gate B — Environment

Prove that streets, buildings, perspective and parallax remain coherent.

### Gate C — Interaction

Prove that hands, props, doors and windows physically interact.

### Gate D — Motion graphics

Prove that counters, bars, typography and HUDs animate smoothly.

### Gate E — Voice

Prove that the narration is intelligible and appropriately expressive.

### Gate F — Sound

Prove that effects are synchronized to actual action.

### Gate G — Integrated sequence

Produce a coherent short sequence containing all relevant systems.

### Gate H — Complete film

Only after the systems are sufficiently reliable should the full 86-second film be assembled.

Do not treat a passed technical test as artistic approval.

Save previews and progress at each stage.

Avoid asking the user to repeat established requirements.

If a major artistic decision requires approval, present a concrete sample rather than a vague question.

---

# 20. AUTOMATED QUALITY CONTROL

Create checks for:

- Resolution
- Frame rate
- Frame count
- Duration
- Audio presence
- Audio clipping
- Missing assets
- Broken scene transitions
- Black frames
- Subtitle timing
- Text safe areas
- Render errors
- Missing audio cues
- Missing scene outputs

Create motion-specific checks where feasible:

- Vehicle position changes over time
- Wheel rotation corresponds to travel
- Speedometer corresponds to velocity
- Camera follows correct world position
- Character contacts remain stable
- Prop positions follow held hands
- Scene transitions maintain continuity

These checks support quality control but cannot replace viewing the film.

Do not mark subjective quality as perfect automatically.

---

# 21. RENDERING STRATEGY

Use scene-level rendering and caching.

Render low-resolution previews before expensive final exports.

Reuse approved assets.

Avoid rerendering unchanged scenes.

Maintain deterministic frame timing.

Export each scene independently where practical.

Assemble with FFmpeg.

Validate the final 86-second output.

Preserve source files for future revisions.

If execution limits are reached, save durable checkpoints and continuation instructions.

Do not claim that work continues after the environment stops unless a supported execution system actually does so.

---

# 22. REQUIRED FINAL DELIVERABLES

Deliver:

1. Complete 86-second film MP4
2. Full project source
3. All 18 scene source files
4. Reusable character rigs
5. Reusable vehicle rigs
6. City environment components
7. House 17 environment
8. Animated door and lock system
9. Animated curtain and window system
10. HyperFrames motion-graphics components where successfully integrated
11. Speedometer and pursuit HUD
12. English narration script
13. Narration audio
14. Anonymous caller dialogue
15. Sound effects and music mix
16. SRT subtitle file
17. Motion-graphics style sheet
18. Contact sheets
19. Technical validation report
20. Artistic quality report
21. Asset and license report
22. Reusable NOIRFRAME production template

Do not claim any unavailable deliverable exists.

---

# 23. EXECUTION PRIORITIES

Prioritize in this order:

1. Real animation and movement
2. Character and prop interaction
3. Coherent environments
4. Vehicle acceleration and pursuit
5. Cinematic camera choreography
6. Natural narration
7. Synchronized sound design
8. Premium motion graphics
9. Captions
10. Final editing polish

Do not sacrifice actual motion to add more decorative overlays.

Do not use visual effects to conceal broken animation.

Do not prioritize quantity over quality.

---

# 24. FINAL INSTRUCTIONS

Read all existing project documentation and inspect the actual source code.

Preserve all previously approved assets.

Use the established user requirements as the single production brief.

Do not repeatedly ask the user to explain the same details.

Do not repeatedly generate near-identical low-quality versions.

When a method demonstrably fails, change the underlying implementation rather than merely changing prompt wording.

Build reusable production systems.

Test them honestly.

Fix structural defects.

Use real animation.

Use real camera movement.

Use coherent city geography.

Use properly animated doors, keys, windows and curtains.

Make the cars move convincingly.

Make the speedometer reflect actual acceleration.

Make the characters act and react.

Use high-quality narration.

Synchronize sound and captions.

Create premium cinematic HUD motion graphics.

Preserve the visual style of the approved V10 sequence.

Build the complete story with all 18 scenes.

Export and validate the 86-second movie.

If the production cannot reach the requested quality with the available environment, identify the actual technical limitation and provide the best viable alternative rather than claiming success.

**DO NOT CONFUSE A SUCCESSFUL RENDER WITH A SUCCESSFUL FILM.**

BEGIN THE COMPLETE PRODUCTION SYSTEM REBUILD.