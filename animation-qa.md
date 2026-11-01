# THE PRICE OF SILENCE — Part One

## Mandatory test gate
The ten-second test was rendered and actual frames inspected before full-film
rendering. The first version had a cropped mirror close-up and an undersized
reaction shot. Both were corrected and the second version was inspected.
Within the SAME fixed mirror shot, the pursuing car's headlight span grows from
39 to 159 pixels: 4.08×. This is
car-scale motion inside the reflection, not camera zoom. Driver head/eyes,
steering grips, and foot/pedal regions independently change in decoded frames.
Detailed measurements: driving_test_motion_qc.json. Test is 300 frames, 30 fps;
the review copy is 540×960. Full film is 1080×1920.

## Action coverage / inspected continuity corrections
- 0–8s: driver grips a rotating wheel; eyes and head turn toward roadside.
- 8–14s: two masked men turn, walk to the black car, and descend behind its
  body as its hinged doors open and close. Clothing remains distinct.
- 14–24s: upward mirror glance, approaching black car, enlarged frightened
  eyes/raised eyebrows, faster breathing, return forward, shoe presses pedal.
- 24–38s: independently translating vehicles and rotating side-view wheels;
  sharper interior steering; both vehicles follow the SAME curved trajectory
  with a delay. Turn shot uses overhead cars and tangent-aligned orientation,
  not rotated side-view cars. Perspective is deliberately illustrated 2D.
- 38–50s: car slows and parks, arm reaches door, hinged door opens, driver steps
  out, door closes, full run cycle toward house. Exit and run shots share their
  end/start positions. Knees and elbows articulate; limbs retain fixed lengths.
- 50–61s: visible key turn, opening door, entry, closing door, deadbolt turn,
  departure toward stairs, articulated diagonal stair run. No run-in-place hold.
- 61–71s: bedroom door opens, character walks behind the foreground bed, hand
  grips and draws curtain, POV of black car directly across road, lights off.
- 71–85s: backward steps, phone vibrates on table, actual phone-screen insert
  reads UNKNOWN NUMBER, visible reach, pickup, pause, phone lifted to ear.
- 85–94s: distinct telephone-filtered caller offers one million dollars to stay
  silent. Character continues nervous breathing and blinking during the call.
- 94–102s: TAKE THE MONEY / CALL THE POLICE audience vote and Part Two prompt.

## Technical / synchronization checks
Full decoding passed with FFmpeg -xerror. H.264/AAC fast-start MP4;
3060 video frames / 102s, portrait 1080×1920 at 30 fps. English mov_text subtitle
track plus burned-in phrase captions during narrative shots, and external SRT.
40 nonoverlapping phrase cues validated against generated line placement.
Loudness: -16.63 LUFS integrated; true peak -4.23 dBTP.
No clipping detected. 118 authored sound events/intervals, including
engine speed rise, two tire squeals, parked-door actions, keys/deadbolt,
curtain, breathing, heartbeat, vibration, answer tap and original suspense score.
Footstep event times derive from the SAME gait frequency/phase as the animated
legs (12 rad/s run, 7 rad/s walk), rather than an unrelated constant interval.

## Scope and honest limits
Original deterministic SVG/React puppet animation and procedural environments.
No generated still-image montage, stock characters, or substituted Ken Burns
shots. Sustained parked-car POV and voting graphics are intentional held views.
This is stylized 2D vector animation, not photorealistic vehicle simulation.
The drawing, rigid props and joint rotations are computed frame by frame.
Kokoro ONNX am_michael narrator / am_adam caller generated locally. This session
cannot listen to audio: expressive delivery and subjective mix quality need
human listening review. Phrase splits are proportional, not forced word alignment.
Visual contact review does not constitute human real-time screening approval.
Model and renderer licenses remain applicable. Music and Foley are synthesized
originals, with no external sound samples.

## Preservation
The previous 12,815,592-byte film remains unchanged, with SHA-256
a1b30aa651b1e2db749ea3bf1616a685e3414718340d9a1b13ffad980a30f9b4.
The new delivery is exported on a separate chase-animation branch. The main
branch and the previous video-export branch are preserved.
