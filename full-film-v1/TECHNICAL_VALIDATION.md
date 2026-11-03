# Technical validation — full film v1

Measured final file: THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4, 16,004,921 bytes. encoding-verification.json is the direct FFprobe record.

| Property | Measured result |
|---|---|
| Picture | H.264,1080×1920,30/1 FPS |
| Decoded video frames |2580 |
| Duration |86.000000 seconds |
| Video/audio start |0.000000 seconds |
| Audio |AAC,48kHz,stereo,86.000000 seconds |
| Scenes |18, exact requested intervals |

A complete FFmpeg decode finished successfully. All2580 frames were independently read to generate encoded-visual-verification.json and the contact sheet. No black interval was detected. Freeze detection flagged61.4–62.8s (held window observation, minor rain below the threshold) and80.566667s onward (intentional held decision card). These are documented holds, not missing scene clips. Encoded audio volume detection measured mean−19.6dB and maximum−2.5dB. Two-pass master loudness measured−15.96LUFS and−2.47dBTP before final AAC; see audio-master-verification.json. No claim of human listening or professional loudness certification is made from these signal checks.

The final file played from0 to86s at1x in local Chromium, taking86.218s. It reached ended=true with2580 total video frames,2 dropped display frames and0 corrupted frames. These two browser display drops are0.078% of the stream, not missing encoded frames. Actual requestVideoFrameCallback snapshots were retained and inspected across all18 scenes. The corrected full animatic also played to the end with zero dropped/corrupted frames. Detailed evidence is in playback-verification.json.

All2580 SVG source poses evaluated without NaN/unreachable-IK errors. Source checks verify all18 boundaries,33 phrase captions with zero overlap, six seconds for the final decision card, and required A/B text. Trunk fully closed first at frame750/25.000s; latch scheduled25.000s; first head rotation frame768/25.600s. Every sampled reaction pose requires closed lid. Those source constraints complement visual review; they do not prove absence of every possible local contact artifact.

The final contact sheet contains actual encoded frames including immediate before/after closure and head-turn frames. No debug ground overlay or promotional logo is substituted for story action. Caption18 is suppressed in-picture to protect the decision card, while SRT includes the final spoken question.

Download publication is verified separately against GitHub blob hashes and sizes. delivery-manifest.json identifies the local delivered contents. Previous repository entries are preserved by building on the prior tree and updating the branch with an expected-head lease.

## Downloadable copy

The connector's16MiB request-body ceiling prevented uploading the original MP4. delivery/THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4 is an11,427,199-byte CRF24 re-encode with unchanged copied AAC. delivery/encoding-verification.json independently confirms86.000s,2580 frames,1080×1920,30FPS,H.264/AAC. It completed a separate full decode with no errors. The original render remains untouched locally. Separate playback evidence is included in playback-verification.json. Compression can soften very fine rain/outline detail.

The downloadable copy completed86.646s of1x Chromium playback, ended=true at86.000s,2580 total frames,5 dropped display frames(0.194%),0 corrupted frames. Its presented-frame sheet was inspected. Those browser display drops do not remove encoded frames.
