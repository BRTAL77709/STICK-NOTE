# Overhaul preview — implementation and review status

**Approval pending. No complete revised-film render has been made.**

## Implemented and exercised in this 20-second preview

- 0–3s: same original stickman Head artwork, upward mirror glance, fear/tension,
  breathing, articulated driving arms, hands constrained to rotating wheel rim.
- 3–6s: both cars follow one arc-length street path with a 6m rear-axle gap.
  Corner speed decreases near the apex and increases on exit; front steering
  follows curvature with inner/outer Ackermann angles. Wheel rotation follows
  per-wheel travel/radius, including different inside/outside travel.
  Suspension moves the body while tire bottoms remain on the road plane.
- 6–9s: acceleration, grounded alternating run, counter-swinging arms,
  forward lean, braking/settling and a follow camera toward number 17.
- 9–15s: upright walking with planted support feet and heel/toe roll, reach,
  grip, handle turn and hinge-projected door opening. The hand follows the
  SAME transformed point used to draw the handle. This preview ends with the
  door open; complete entry/closing/locking is not represented as finished.
- 15–20s: new room/furniture depth, phone vibration, continuous pickup of one
  constant-size phone prop, screen-reading pause, tremor and near-ear movement.
  The carried phone and hand share a single world-space attachment.
- Architectural houses with roofs, side walls, windows, porch details, curbs,
  wet-road reflections, streetlight pools, haze, subtle trees/curtains and
  purposeful camera tracking/push-ins. Original minimalist character identity
  and source body dimensions are retained; environments may change under the
  expanded request.

## Actual checks

Full FFmpeg decoding with -xerror passed. MP4 H.264/AAC, fast-start,
1080×1920, 30fps, 600 video frames, 20 seconds; English burned-in captions and
selectable mov_text subtitle track. 7 caption cues validated for range
and overlap. Audio: -15.74 LUFS integrated, -1.47 dBTP.
Stereo Foley/ambience, centered dialogue, music ducking. 34 sound
events/intervals quantized to rendered frames; footstep impacts follow the
actual foot landing schedule. Headlight span in the rendered fixed mirror shot
grows from 24 to 48 pixels at the same downsample scale.

At 120Hz kinematic sampling, every exercised limb stays within reach and has
its original fixed segment lengths. Planted support contact and hand-to-prop
errors are within floating-point rounding; floor penetration is zero. The
checks also bound inter-sample joint jumps, catching the elbow-branch pops
found in an earlier draft. See kinematics-qc.json for measured values.

An early draft had crouched default stances and branch-switching elbows. The
current version uses reach-aware upright body height and explicit stable bend
sides; it was rendered again after these corrections. Representative frames
were inspected and a contact sheet was extracted from the actual muxed MP4.
These are mathematical/technical checks and visual frame review, not a claim
that every aesthetic aspect is professionally approved.

## Still pending / limitations

- Your review of the actual movement, environment quality, pacing and voices.
- This session cannot listen to audio. The narrator/caller are locally generated
  Kokoro voices (am_michael/am_adam), not human-recorded performances. Naturalness
  and subjective mix balance require your listening review.
- The screenplay/shot plan is rewritten, but the full revised conversation,
  curtain/recoil, complete entry/locking, headlights-on threat, sunrise message
  and final vote have not been rendered. The preview is a selected-action reel.
- This is deliberately illustrated 2D / projected vehicle geometry, not a
  photorealistic vehicle or ray-traced lighting simulation.
- Subtitles use phrase timing tied to generated speech, not forced word alignment.

## Preservation

Original source, prior films and original audio hashes were checked unchanged.
The original Head artwork is byte-identical. Work is in a separate project.
Read PRODUCTION.md for the causal rewrite, complete screenplay and shot plan.
Wait for user approval before full-film integration/rendering.
