# V11 technical review — three motion tests

All three canonical clips are1080×1920,30FPS,H.264/yuv420p with AAC contact-Foley tracks. No narration, captions or HUD is present in the new proofs. This is not a full-film export or artistic approval.

| Shot | Duration | Frames | File bytes | Full decode |
|---|---|---|---|---|
| HOUSE | 11s | 330 | 1,072,377 | clean |
| STAIRS | 8.5s | 255 | 1,453,490 | clean |
| WINDOW | 7.5s | 225 | 945,544 | clean |

## Actual playback

Each actual1080 MP4 played to its end at normal and half speed in Chromium, with presented-frame evidence. The busy House normal pass recorded8 display drops; its isolated repeat completed with0 drops and0 corruption. Stairs and Window normal passes and all three half-speed passes recorded0 drops/corruption. Encoded frame counts and full FFmpeg decodes are clean. The busy-pass record is retained, not replaced.

## Rig/contact checks

Every encoded frame has a matching evaluated world-joint sample. Bone lengths are0.37+0.37m per leg and0.34+0.34m per arm. Their numerical errors stay below1e-12m. Consecutive planted soles have0m displacement. Sampled shoe vertices clear the ground/treads within floating-point precision. The first stair draft had57.7mm penetration; its failed result is preserved, and the corrected source was rerendered and rechecked.

House: visible key rotation reaches90°;25 sampled frames have the shaft inside the lock plane. Fingertip/key-bow, lever and inside-bolt constraints agree within numerical precision. The primary arm centreline does not intersect the door panel in sampled frames, including the free-edge handoff. The single hinge/leaf/hardware model is used in both views.

Stairs: twelve0.20m risers reachY2.40m, with13 landings including the trailing-foot catch-up. The far wrist follows the same rail equation. Pelvis world travel and fixed-scale camera tracking are independent. Window:80 gripped frames connect the fingertips to the actual deforming cloth edge; rod/rings remain attached. The outside car is ground-level geometry viewed through an upper-storey opening.

These are joint, shoe-vertex and arm-centreline tests, not an exhaustive garment-volume collision simulation. Exact constraint numbers do not establish convincing acting.

## Review evidence and source

Before/after MP4s preserve each source at normal speed. Comparison end holds are explicitly labeled. Old action ranges are49.2–61.4s,61.4–65.4s and65.4–69.4s of the rejected master; the new stand-alone timings differ. First/mid/last decoded frames and contact strips sampled at0.0667–0.1s are supplied. The House wide diagnostic retains all poses while removing mechanism inserts.

The new renderer has no old-film or pose-image input. A fresh source-only rebuild produced all three canonical MP4s byte-identically. Source hashes are recorded in the world-state datasets. All11,533 protected prior production files matched their original SHA256 hashes, including V10 and previous full-film versions.

## Audio and approval boundary

The track is original synthetic Foley at event times from the authored actions. It is a quiet diagnostic track, not a mastered final soundtrack. Critical listening, perceived material realism and subjective sync approval remain pending. No rejected narration was reused and no Whisper/word-alignment claim is made. The voice auditions, full soundtrack, HUD and final choice remain planned in the18-scene register.

No full86-second V11 was rendered. The three motion tests require the user’s review and approval before full-film work proceeds. No paid APIs, paid services, Onetake restricted code or new toolkit installs were used.
