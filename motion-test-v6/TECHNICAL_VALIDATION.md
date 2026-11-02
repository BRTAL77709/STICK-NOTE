# V6 technical validation — artistic approval pending

## Actual final MP4

1080 × 1920, 9:16, H.264/yuv420p, 30 FPS, exactly 150 decoded frames, 5.000000 seconds, AAC stereo 48 kHz. File size: 2,563,997 bytes. Full FFmpeg decode passed.

Isolated, fully buffered Chromium playback at 1× ended normally in approximately 5.08 seconds: 150 total frames, zero dropped, zero corrupted. A prior unbuffered preview presentation dropped three startup frames; encoded frames were not missing. The buffered preview and final checks passed. No artistic score is inferred from this.

## Head-turn strategy and validation

Criminal 01 now uses a local 2.5D geometric head/cap/mask/neck module. Ellipsoidal head and cap surfaces, curved eye/mask patches and a rigid visor are yawed together from 72° to frontal and projected into flat SVG. Surface occlusion changes near/far eye visibility. This replaces V5's feature morph strategy without replacing the body renderer or approved cap/mask/hoodie design.

The visible visor's rightward projection changes from about 111.15 to 75 world units; mask-chin projection changes from 20.37 to 0; head silhouette radius changes from 54.71 to 61. The cap seams, mask surfaces and neck use the same rotation. The face is frontal by 4.0 s; eye narrowing follows through 4.5 s, then a breathing hold.

V6_HEAD_TURN_EYES_HIDDEN.png shows the same head at a **fixed diagnostic camera**, every 0.1 s from 3.2–4.0, with/without eye geometry. It tests the turn without eye movement or camera reframing. This is generated from the actual head module, not retouched film frames. The actual encoded contact sheet separately checks the delivered shot.

## Contacts and planted feet

- Both criminal roots advance 300 world units by 3.2 s; roots hold through 0.9 s.
- Every generated pose was checked: maximum stance-foot world displacement 0; both criminals always have a support foot. Their support patterns differ across 32 frames.
- Criminal 01's full rig occupies the slightly farther pavement-depth row y=1384; Criminal 02 remains at y=1404. Corresponding shadows, splashes and close-up framing were moved together. This separates a previously occluded boot without changing proportions or bone lengths.
- Maximum glove-center distance from victim upper-arm segment: approximately 1.14×10^-13 world units. The target remains 53% along shoulder-to-elbow length.
- All IK targets are reachable; maximum measured bone-length variation is 0.020342 units, due to 0.01-unit SVG coordinate formatting. Joint polylines share endpoint coordinates.
- V6_ENCODED_CONTACTS.png uses **actual consecutive decoded frames**, not SVG snapshots. Inverse camera translation registers pavement and planted feet together. Four four-frame stance windows cover both legs of both criminals. The locally measured sole-peak row is constant in each displayed window after correction (0-pixel row range at half resolution). Guides mark expected world anchors. This sampled pixel check does not claim universal optical-flow tracking.
- Two additional four-frame grip rows show the actual encoded support contacts during the first pull. Guides/crops are diagnostic only; no guides appear in the final video.

## Supported victim and timing

The pelvis stays at least 134.97 world units below shoulder height. There is no victim walk cycle. Both heels remain at pavement heights 1413/1418; knees stay at least 70.15 units ahead of the dragging ankle. Short passive catches vary heel spacing approximately 29.99–38.35 units without lifting the shoes.

Upper-body pull impulses are tied to actual lead-foot distances 50, 150 and 250 units (about 1.325, 1.975 and 2.625 s). Pelvis, heel and head responses lag; this is deterministic load-response animation, not a dynamics simulation.

The cinematic cut remains exactly frame 96 / 3.2 s. The encoded cut pixel change is 9.15 times the median non-cut change. Encoded contact sheet: 0.2 s dragging, 0.1 s reaction, exact cut-adjacent and final frames. Consecutive playback frames and comparison encode were inspected. No unintended geometry pop was found in these checked views; the cut is intentional.

## Image, sound and limits

No full-black frame was detected by the configured full-file pass; minimum decoded-frame mean was 20.67/255. No decoder errors. Original local procedural audio only; sample peak -5.9 dBFS, mean -25.0 dBFS, no digital clipping. Subjective listening QA was not performed.

QUALITY_LOG.md identifies the three most visible remaining flaws and bounded next-revision hypotheses. Technical contact, projection and playback checks do not establish exceptional acting or user approval. V6 is delivered for review. No V7 or full 1:26 film has begun. Additional cost $0.
