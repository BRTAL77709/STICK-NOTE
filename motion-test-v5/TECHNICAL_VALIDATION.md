# V5 technical validation

## Final file

`THE_PRICE_OF_SILENCE_MOTION_TEST_V5_5s.mp4`: 1080 × 1920, vertical 9:16, H.264/yuv420p, 30 FPS, exactly 150 frames and 5.000000 seconds, AAC stereo 48 kHz. Size: 2,486,686 bytes. Full FFmpeg decoding passed.

Normal-speed Chromium playback completed at 1× in approximately 5.18 seconds: 150 total frames, zero dropped, zero corrupted, ended at 5.0 seconds. Consecutive frames presented by playback were inspected; the complete encoded contact sheet and V4/V5 comparison were also inspected.

## Choreography and geometry

- Root motion is held through 0.9 s, then both criminals advance 300 world units by 3.2 s. A camera-independent pose ledger records this.
- Both retain at least one support foot in each of 150 poses. Maximum planted-foot world slide: 0 units.
- Individual support states differ on 32 frames; footstep sounds derive from the corresponding actor/leg contact events.
- Victim pelvis remains at least 136.995 units below shoulder height. Both heels remain grounded, with constant spacing and no independent victim gait/lift. Folded leg geometry puts each knee at least 68.93 units ahead of its dragging ankle.
- Both glove centers remain on the victim upper arms at 53% of shoulder-to-elbow length. Maximum numerical gap: approximately 1.14 × 10^-13 units.
- All IK targets were reachable across 150 poses. Maximum measured bone-length variation: 0.019633 units, from rounding SVG coordinates to 0.01 units. Polylines share their joint coordinates; no disconnected limb geometry was found in the checked sequence.
- Shot A is frame 0–95, Shot B begins at frame 96 / 3.200 s. The encoded cut has about 12.99 times the typical adjacent-frame pixel change.
- The head orientation control changes horizontal radius 52→61, cap projection 99→76 and mask-chin shift 18→0 world units. Neck/face-plane alignment changes with the same orientation parameter; frontal by 4.0 s, eye narrowing completed by 4.5 s.

## Image and audio checks

Contact sheet: 0.2 s dragging / 0.1 s reaction intervals, plus exact cut-adjacent and final frames. No blank frame detected by the full decode/black-detection pass; minimum sampled-frame RGB mean is 19.90/255. No unintended geometry popping was found in the inspected strips; the frame-96 discontinuity is the deliberate cut.

Original procedural rain/footsteps/friction/accent only. Final decoded sample peak: -5.9 dBFS; mean volume: -25.0 dBFS. No digital clipping. No narration or captions; no Whisper or yt-dlp install. Subjective listening QA was not performed.

The checks establish encoded-file and rig behavior, not artistic realism. Remaining perceptual weaknesses are listed in V4_VS_V5_COMPARISON.md. No fabricated quality score.

## Preservation and delivery

Earlier V1/V3/V4 videos and source folders are preserved. No separate named V2 final project was found; V1's second preview remains intact. Approved story/timeline was not edited. Five-second test only; no full film started. Local production tools, no paid API or model downloads, additional cost $0. The framework report distinguishes inspected documentation from runtime integration.
