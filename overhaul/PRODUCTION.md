# THE PRICE OF SILENCE — overhaul / approval stage

This is a separate project copy. Baseline source, original narration mix, and
SHA-256 preservation records are in `preserved/`. The existing film is unchanged.

## Diagnosis and implemented architecture

The old implementation advanced a global sinusoidal gait independently of the
root trajectory. A planted foot therefore moved with the character. The old
IK solver clamped reach for its cosine calculation but drew the hand at the
unclamped target; elbow-side selection could change abruptly. Lean rotated the
whole character and its shadow, moving the feet off their ground anchors.
Prop targets were generally body-local while handles/phones were scene-local.
Door opening used an arbitrary scale rather than a shared hinge projection.
Wheel rotation was driven by time independently of distance.

The new implementation uses world-space footsteps with stance/heel/toe contact,
swing arcs, separate torso motion, two-bone limb solvers with fixed poles, and a
smooth body-height reach constraint. Hands and carried props share the exact
same world-space attachment. The door and its handle use one projected hinge
transform. Vehicle wheels derive their angle from distance/radius, front-wheel
steering derives from path curvature, and both cars use the same arc-length path.
All cameras transform entire scenes after solving contacts.

The existing Head artwork, cap, face, hoodie paths, colors and body dimensions
are reused. Environment redesign is authorized by the later expanded briefs.
No human/3D character or generated image replaces the original stickman.

## Screenplay logic

The requested caller says “You saw something tonight,” but the supplied revised
drive did not establish a witnessed event. Add a short, grounded observation:
the protagonist brakes for a man near a closed service garage, then sees two
others force that man into a black sedan. He cannot tell whether it is an arrest
or an assault. He drives away rather than confronting three strangers.

The sedan follows. He tests the suspicion with ordinary turns, speeds up only
within the residential road's geometry, and loses sight of it before going home.
He does not knowingly lead an active pursuer to his house. Once inside, he
reaches for his phone to call for help; an incoming call interrupts him. The
million-dollar offer is an unverified coercive promise, not presented as a
credible guaranteed bank transfer. The threat becomes concrete when the car's
headlights respond to the caller's instruction.

## Production screenplay (full film NOT rendered / subject to preview approval)

### 1. Night drive, 02:17 AM

**NARRATOR, quiet:** “At two seventeen, I slowed for a man in the road. Two others
pushed him into a black car. I kept driving.”

A tired driver grips the wheel. Wet asphalt reflects practical streetlights.
In the mirror, the black sedan joins his lane. He turns once, then again.

**NARRATOR:** “At first, I thought it was a coincidence. Then I turned again.
So did they.”

### 2. Confirmed pursuit

He glances up, tightens his hands, and presses the accelerator. The sedan closes
the gap. Three deliberate turns follow the same neighborhood map; cars slow
through corners rather than drifting. A bend and a row of parked vehicles
temporarily obscure the pursuer. He checks the empty mirror before turning home.

**NARRATOR:** “I took three turns I didn't need. The car stayed behind me.
Then I couldn't see it anymore. I thought I'd lost it.”

### 3. Entrance

He parks, scans the apparently empty road, exits and runs to number 17. He slows,
finds the key, unlocks, grips and turns the handle, opens the door, steps inside,
turns back, closes it and turns the deadbolt. He waits and catches his breath.

**NARRATOR:** “I ran inside and locked the door. I stood there, listening.”

### 4. Bedroom window

An idling engine interrupts the quiet. He enters the bedroom, stops, reaches for
the curtain, draws it aside and leans toward the glass. Across the street is the
same sedan, headlights off. A seated silhouette is visible; no supernatural reveal.
He recoils, holds still for a beat, then takes two backward steps clear of furniture.

**NARRATOR:** “Then I heard the engine. Across the street. The same car.”

### 5. Call

He reaches for his phone to call for help. It vibrates first: UNKNOWN NUMBER.
He picks it up, checks the window once more, hesitates, answers and raises it.

**CALLER, low and controlled:** “You saw something tonight.”

**PROTAGONIST:** “Who is this?”

**CALLER:** “That doesn't matter.”

**PROTAGONIST:** “What do you want?”

**CALLER:** “We need you to forget what you saw. One million dollars.
All you have to do is stay silent.”

**PROTAGONIST:** “And if I call the police?”

Pause. No musical impact.

**CALLER:** “Look outside.”

He returns to the window. The headlights turn on, illuminating the wet road,
curb and opposite wall in one coherent lighting change.

**CALLER:** “We already know where you live.”

The call disconnects. He remains holding the phone, breathing shallowly.

### 6. Deadline / vote

A message arrives: “$1,000,000 FOR YOUR SILENCE. YOU HAVE UNTIL SUNRISE.”
He looks from the phone to the window. Cut to black, let the room tone fall away.

WHAT WOULD YOU DO? A — TAKE THE $1,000,000 / B — CALL THE POLICE.
Hold readable options for at least five seconds. One restrained final sound,
then a short silence. No invented voting totals.

## Shot and geography plan

| Shot group | Planned interval | Action / camera / synchronization |
|---|---:|---|
| Garage observation / drive | 0–12s | Windshield POV, driver medium, 02:17 display; brake sound only at deceleration |
| Mirror / two matched turns | 12–27s | Head glance, mirror push-in, shared-path exterior; steering and wheels tied to travel |
| Escape / lose sight / park | 27–39s | Acceleration, third corner, occlusion, mirror check, coast and brake into number 17 |
| Exit / run / entrance | 39–55s | Step out, grounded sprint, deceleration, key/handle/hinge, reverse angle inside, deadbolt |
| Interior pause / bedroom | 55–66s | Breathing, engine cue, cautious walk; hall to bedroom has a continuous route |
| Curtain / opposite car | 66–76s | Hand-pinned fabric, lean and recoil, two planted backward steps |
| Unknown call | 76–104s | Same physical phone on table and in hand, restrained dialogue, glances and tension |
| Headlights / disconnect | 104–113s | Caller “look outside,” headlight reveal with road/wall response, end-call cue |
| Message / vote | 113–126s | Message legibility, black beat, safe-area choice held 5+ seconds |

Timings are a production plan, not a claim of rendered scenes. Adjust only after
voice performance review while preserving action and synchronization.

The garage is before the first corner; number 17 is on the third residential
block. The driveway, front porch and entry share a door axis. The bedroom faces
the opposite curb where the sedan parks; the practical lamp is beside the table,
and the floor route avoids the bed and nightstand. Trees/poles occlude at actual
depth boundaries. Stillness is intentional during listening and the parked-car reveal.

## Preview scope and approval gate

The 20-second preview is a selected-action reel, not the complete revised film:
0–3 driving/mirror; 3–6 shared-path turn; 6–9 grounded escape; 9–15 approach and
handle-driven opening; 15–20 phone pickup, hesitation and answer. A short caller
line teases the offer. Revised narration is generated for this preview only.

Full close/lock, curtain/recoil, message deadline and complete conversation remain
planned integration after approval. Do not describe them as finished by this preview.
No complete-film render is authorized until the user approves the preview.
