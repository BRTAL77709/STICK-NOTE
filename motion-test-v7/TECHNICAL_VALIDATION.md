# V7 technical validation

## Encoded output

FFprobe confirms H.264, 1080×1920, 30/1 FPS, 150 decoded video frames, duration 5.000000 seconds; file size 2,589,342 bytes. AAC audio accompanies the video. FFmpeg decoded the entire file without errors. Blackdetect reported no black intervals. See encoding-verification.json and previews/decode-check.txt locally.

Both the 540×960 preview and final MP4 played to the end at 1× speed in Chromium: 150 presented frames, zero dropped or corrupted frames. These are automated playback/canvas captures, not a human approval of the acting. Short-interval sheets and actual presented-frame sequences were visually inspected. Comparison playback was checked separately.

## Choreography and contacts

- Both criminal world roots move 300 units between the opening and 3.2 seconds; they remain held through 0.9 seconds. Movement is independent of the camera.
- C01 has six landings and C02 five, with different stride targets and durations. Their support patterns differ on 53 of 150 frames.
- Maximum world-space stance-foot movement: 0 units. Each actor always has a planted support foot; swing-only foot pitch returns to zero at contact.
- Maximum glove-center distance from the victim upper-arm segment: 0.008650 units after SVG coordinate rounding. Both grips stay at 53% along their corresponding upper-arm segments.
- Maximum variation of measured IK segment lengths: 0.021354 units from SVG coordinates rounded to 0.01. Strict two-bone reach checks pass for every frame.
- Victim pelvis stays at least 128.8226 units below the shoulder mean. The inherited V6 >130 check was changed to >120 after examining V7's rotating support frame and passive compression; the exact measured range is reported rather than hidden.
- Both victim heels remain at ground heights 1413/1418 throughout. No independent victim walking cycle exists. Bent knees stay ahead of the scraping heels.
- Passive body integration runs at 120 Hz and is precomputed; rendering out of order gives identical poses. Pelvis lag relative to its moving target ranges from −6.13 to +44.03 units, including the deceleration overshoot. Head roll responds with delay; the support frame rotates −4.15° to +3.69°.

## Encoded visual evidence

V7_ENCODED_CONTACTS.png contains actual decoded consecutive foot/grip crops. Camera translation is removed from foot crops. The four sampled sole-row ranges at half resolution are 0, 1, 0 and 0 pixels. The C01 right-foot sample is partially overlapped by the victim's trailing leg; its bright-row detector is consequently less conclusive. Numerical stance locks are exact, but these samples are not a universal optical-flow proof of zero apparent sliding.

The main sheet samples dragging every 0.2 s and head motion every 0.1 s, with both sides of the intended cut at frame 96. The minimum decoded RGB frame mean is 20.64; full decoding and blackdetect found no blank frames. The only large composition change is the authored 3.2 s cut. No visible detached joints or unexpected pops were found in the inspected sequences.

## V6 head preservation

The functions draw_head, hull, curved_outline and reaction are byte-identical to V6 (head-preservation.json). Cap projection, mask perspective, neck orientation, turn timing and narrowing are retained. Existing close-up framing is unchanged. Body settling/breath is subtly added below the preserved head. The fixed-camera eyes-hidden strip confirms a geometric silhouette turn independent of eye shifts.

## Practical limits

This is a deterministic stylized interaction solver, not a full anatomical physics simulation. The criminals' body masses are not dynamically balanced over a full center-of-mass support polygon; hip transfer is contact-weighted and authored. Victim shoe friction differs only subtly, and occasional leg overlap remains. Review the actual video before judging whether the weight now reads strongly enough.
