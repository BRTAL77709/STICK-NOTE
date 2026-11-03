# THE PRICE OF SILENCE — V4 MOTION & MOTION GRAPHICS REBUILD

You are the animation director, motion-graphics engineer, cinematographer and editing supervisor for THE PRICE OF SILENCE.

The V3 15-second test is not approved yet.

The priority for V4 is **real movement, professional cinematic motion graphics, and visual synchronization**.

Repository: BRTAL77709/STICK-NOTE

Input: `THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V3_15s.mp4`

Output directory: `full-film-cinematic-rebuild-v4/`

Preserve all previous versions, especially the approved V10 crime sequence.

Target: 15 seconds, 1080×1920, 30 FPS, 450 frames.

## 1. USE HYPERFRAMES FOR REAL MOTION GRAPHICS

Official repository:
https://github.com/heygen-com/hyperframes

Inspect the existing workspace and determine whether HyperFrames is actually installed.

Read its documentation and use its real, documented rendering API.

Do not claim HyperFrames integration merely because a custom HTML overlay looks similar.

Create reusable components for:

- Animated numerical counters
- Speedometer and tachometer
- Cinematic HUD panels
- Progress bars
- Digital clock
- Pursuit distance tracker
- Word-by-word captions
- Animated transitions

If HyperFrames is unavailable, report the exact blocker and produce a separately labeled fallback rather than falsely claiming HyperFrames was used.

## 2. EXACT HUD STYLE

Match the user's CASH / SUSPICION visual reference.

Design system:

- Dark translucent navy backgrounds
- White bold numerical values
- Amber/orange highlights
- Thin amber borders
- Uppercase compact labels
- Rounded rectangular panels
- Animated progress bars
- Smooth numerical counters
- Professional typography and spacing

Use purposeful overlays only.

The interface must feel like a premium cinematic motion-graphics production, not a generic dashboard.

## 3. SHARED VEHICLE MOTION ENGINE

Build one deterministic vehicle state:

`vehicleState(t)`

It must provide:

- World position
- Speed
- Acceleration
- Heading
- Steering
- Wheel rotation
- Suspension response
- Engine RPM estimate
- Pursuer distance

Use this state for every dependent element.

The car, environment, dashboard, HUD and camera must remain synchronized.

No arbitrary counter values.

## 4. REAL DRIVING ANIMATION

The protagonist must visibly drive.

Animate:

- Hands gripping and rotating the steering wheel
- Shoulder and elbow movement
- Head turning toward rearview mirror
- Eye tracking
- Torso leaning under acceleration and cornering
- Foot pressing the accelerator
- Natural reaction timing

Use articulated character rigs.

Avoid isolated pose swaps.

## 5. REAL VEHICLE ACCELERATION

Show acceleration through:

- Increasing wheel rotation
- Road markings moving faster
- Buildings passing faster
- Streetlights sweeping across the car
- Stronger environmental parallax
- Vehicle pitch
- Suspension movement
- Engine pitch
- Camera tracking

The viewer must feel the speed even when the speedometer is hidden.

## 6. CINEMATIC CAMERA MOTION

Use purposeful:

- Tracking shots
- Interior close-ups
- Dashboard inserts
- Rearview mirror shots
- Road-level views
- Cornering shots
- Controlled camera shake
- Perspective-correct parallax

Avoid repeated static compositions.

Do not substitute digital zooms for actual character and vehicle animation.

## 7. ANIMATED HUD CHOREOGRAPHY

Create these timeline-driven animations:

### Clock

The LOCAL TIME panel appears with a short fade-and-slide.

Its digits update only when the story timeline requires it.

### Speedometer

The speed value counts smoothly and the needle follows the same value.

Add a restrained orange progress indicator.

The HUD responds to acceleration and then exits cleanly.

### Pursuer Distance

Use actual relative vehicle positions.

Animate the displayed distance and its progress indicator.

Do not invent unsupported values.

### Captions

Animate words or short phrases with subtle scaling, opacity and emphasis.

Keep text synchronized to the actual narration.

No random word bouncing.

## 8. EDITING AND PACING

Rebuild the 15-second chase sequence around clear visual beats.

Suggested structure:

0–2s: Exterior moving car, clock HUD.

2–4s: Driver reaction and steering.

4–6s: Accelerator and speedometer.

6–9s: Fast exterior acceleration.

9–12s: Rearview mirror, pursuing sedan.

12–15s: Sharp turn and escape.

Allow timing adjustments for action and narration.

Every shot must add new information.

## 9. AUDIO SYNCHRONIZATION

Keep audio and visuals synchronized.

Engine acceleration must follow vehicle speed.

Sound effects must land on visible actions.

Preserve usable narration while identifying remaining voice-quality limitations honestly.

Do not claim that HyperFrames improves text-to-speech quality; it is being used for motion graphics.

## 10. RENDERING AND VALIDATION

Render the actual V4 MP4.

Inspect frames at 0.25-second intervals around:

- Acceleration
- Speedometer animation
- Steering
- Mirror reveal
- Cornering
- HUD entrance and exit

Check that values and motion evolve continuously rather than changing only between static shots.

Use FFprobe to verify:

- 1080×1920
- 30 FPS
- 15 seconds
- 450 frames
- H.264 MP4

Watch the result at normal playback speed.

Do not claim subjective quality is perfect without user review.

## 11. DELIVERABLES

Provide:

1. `THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4`
2. Actual HyperFrames project/source files, if successfully integrated
3. Animated HUD demo
4. Vehicle animation source
5. Caption animation source
6. Contact sheet
7. V3/V4 comparison
8. Technical validation report
9. Honest motion-quality report

Do not render the full 86-second movie yet.

Do not overwrite previous versions.

## FINAL DIRECTIVE

The V4 objective is not more decorative effects.

It is to make every movement physically readable and every motion graphic feel professionally designed.

The car must genuinely accelerate.

The driver must genuinely react.

The camera must genuinely track the action.

The environment must genuinely move.

The numbers must genuinely animate.

The captions must genuinely follow the narration.

Use HyperFrames where available and verifiably integrated.

Implement, render, inspect, correct and deliver V4.

BEGIN PRODUCTION.