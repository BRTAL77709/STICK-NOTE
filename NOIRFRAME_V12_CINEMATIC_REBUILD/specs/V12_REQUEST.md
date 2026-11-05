# NOIRFRAME V12 — CINEMATIC WORLD & CHARACTER ANIMATION REBUILD

Repository: BRTAL77709/STICK-NOTE

You are the animation director, environment artist, character animator, vehicle animator, cinematographer and technical director.

The user has rejected the V11 previews:
- STAIRS_V11_R07_1080.mp4
- HOUSE_V11_R08_1080.mp4
- WINDOW_V11_R07_1080.mp4

These are NOT approved.

Your task is to correct the underlying animation and environment systems, not simply produce R09/R10 using the same approach.

## 1. ABSOLUTE VISUAL REQUIREMENTS

Preserve the approved illustrated stickman designs and V10 trunk choreography.

Build a consistent, cinematic 2D/2.5D world with:
- Real spatial depth
- Coherent perspective
- Detailed architectural environments
- Character acting with body weight
- Accurate physical interactions
- Camera blocking and continuity
- Cinematic lighting and shadows
- Rain and environmental atmosphere

Do not change the characters into realistic humans.

Do not replace real animation with static images, sprite sliding or camera-only movement.

## 2. REBUILD THE STAIRCASE

The existing stairs look like a simplified diagram.

Create an actual interior staircase environment with:
- Visible walls and ceiling
- Consistent step dimensions
- Landing and upper floor
- Proper railings and banisters
- Wall lights and shadows
- Connected hallway
- Correct character-to-stair proportions

Animate every step using grounded foot contacts.

Each foot must land on the actual stair surface.

The pelvis must rise with each step.

Animate knees, hips, torso, shoulders and arms with staggered timing.

Avoid repeating the same walk cycle without adapting to individual stairs.

The camera should follow the character with cinematic composition while preserving spatial clarity.

## 3. REBUILD HOUSE 17 AND THE KEY INTERACTION

Create a believable house entrance with consistent architecture.

Animate this exact action sequence:

1. Character runs toward House 17.
2. Slows down and plants feet.
3. Reaches for the door handle.
4. Attempts to open the locked door.
5. Reacts to the resistance.
6. Searches pocket.
7. Retrieves a correctly sized key.
8. Aligns the key with the keyhole.
9. Inserts it into the cylinder.
10. Rotates the key.
11. Unlocks the door.
12. Withdraws the key.
13. Grips the handle.
14. Opens the door on its actual hinge.
15. Enters through the doorway.
16. Closes and locks the door behind him.

Hands, fingers, key, handle and lock must stay physically connected at contact points.

Use close-up shots only when the action remains readable and spatially consistent.

## 4. REBUILD THE BEDROOM WINDOW

Create an actual bedroom:
- Bed
- Door
- Walls
- Window frame and sill
- Curtain rail
- Fabric curtains with visible folds
- Exterior street and parked black sedan
- Nighttime lighting and shadows

The character must approach the window, reach toward the curtain, grip the fabric edge and pull it sideways.

The curtain must follow the hand, bunch realistically and settle after release.

Show the black sedan outside through the same window.

Animate the character noticing it, freezing briefly, recoiling and looking frightened.

No instantaneous curtain disappearance.

## 5. REBUILD THE CAR INTERIOR

The cockpit must be a coherent environment, not disconnected drawings.

Include:
- Dashboard
- Steering wheel and column
- Driver seat
- Windshield
- Rearview mirror
- Side windows
- Pedals and footwell
- Road visible through the windshield

The driver must remain properly seated.

Hands must grip the steering wheel.

Steering wheel rotation must correspond to actual vehicle direction.

Foot pressure must correspond to acceleration and braking.

Show meaningful driver reactions through head, shoulders and torso.

Use convincing camera angles:
- Driver over-the-shoulder
- Dashboard POV
- Rearview mirror close-up
- Passenger-side medium shot
- Exterior tracking shot

## 6. REBUILD THE ROAD AND BUILDINGS

Create one consistent rainy nighttime city environment.

Build:
- Continuous connected roads
- Intersections and corners
- Sidewalks and curbs
- Buildings with believable scale
- Windows, entrances and streetlights
- Parked cars
- Road markings
- Reflections and puddles
- Street depth and perspective

Buildings must occupy stable world positions.

As the car drives, nearby buildings must pass faster than distant buildings.

Do not use a repeating flat scrolling background.

## 7. REBUILD THE CAR CHASE

Animate both cars in world space.

The black sedan must visibly follow the witness.

Show:
- Acceleration
- Wheel rotation
- Steering and turns
- Braking
- Vehicle body roll
- Road perspective
- Changing distance between vehicles
- Realistic camera tracking

Do not make the car appear to accelerate solely because a speedometer number changes.

The speedometer must derive from the animated vehicle state.

## 8. CINEMATIC ANIMATION PRINCIPLES

Study:
https://github.com/JohnHeibel/ClaudeAnimationBase

Use its animation principles where compatible:
- Strong key poses
- Anticipation
- Follow-through
- Overlapping action
- Weight transfer
- Arcs
- Character reactions
- Readable timing

Study:
https://github.com/feitangyuan/onetake

Use its conceptual lessons for shot continuity, rhythm and camera movement. Respect its noncommercial license; do not import restricted code without appropriate permission.

Do not make the entire film one continuous take. Use appropriate cinematic cuts.

VOX-COLLAGE-BROLL may inform optional editorial QA, but must not replace the established stickman visual style or introduce paid API dependencies.

## 9. TECHNICAL ARCHITECTURE

Use Blender for spatial environments, rigs, character-object constraints and vehicle animation when appropriate.

Use Remotion for editorial composition.

Use HyperFrames for HUD and motion graphics.

Use FFmpeg for encoding and audio processing.

Use a single consistent coordinate system and reusable assets across scenes.

Do not add dependencies that have no demonstrated benefit.

Do not claim a tool is installed or functioning without verifying it.

## 10. FIRST DELIVERY — FOUR NEW PROOF SHOTS

Before producing the complete film, deliver:

A. Staircase — fully connected interior, grounded climbing.

B. House 17 — detailed key, lock, door and entry choreography.

C. Bedroom — actual curtain pull, black sedan reveal and emotional reaction.

D. Driving — coherent cockpit, moving road, buildings and a visible black-sedan pursuit.

Each shot must include:
- 1080×1920 MP4
- 30 FPS
- Editable source
- Normal-speed playback
- Close-up frame strips for physical contacts
- Before/after comparison
- A list of remaining visible defects

Review all four shots for:
- Foot sliding
- Hand penetration
- Prop disconnection
- Character scale changes
- Camera jumps
- Broken perspective
- Mechanical timing
- Static scenery
- Missing reactions

Do not label these tests approved.

## 11. FINAL FILM

Only after the four new shots are reviewed and approved, integrate the validated improvements into the complete 86-second THE PRICE OF SILENCE film.

Preserve V10 and all previous versions.

Use only legitimately available free tools and assets.

## START IMMEDIATELY

Inspect the actual V11 source and identify why the previous animation approach produced simplified movement and environments.

Create the V12 source structure.

Begin with the staircase and house architecture, then implement the character rig and contact choreography.

Show real improvements in rendered video, not only in code or technical reports.