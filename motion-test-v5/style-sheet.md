# THE PRICE OF SILENCE — reusable V5 style sheet

The V4 artwork is the style lock. Values below come from the actual V5 source unless marked as recommendations. This is a five-second test; it does not change the approved story.

## Palette and drawing

- Contours: `#030b12`, typically 5–7 world units; continuous round caps/joins.
- Sky: `#020a12` to `#153443`; ground `#142c34` to `#040d16`.
- Hoodie: gradient `#253540`, `#14222d`, `#0b151e`. Mask `#0b1721`; cap `#142532` and `#091923`.
- Leg planes: `#172833`, `#243945`; victim trousers `#213b47`.
- Victim shirt: `#b8bdbb` with `#74848b` shade. Eye opening: `#f1ede4` to `#9ca9af`.
- Amber contour: `#ecab54`; lamp `#f8b158`, reflection hues `#715337` and `#9c7040`.
- Local limb rim: `#64818c` at 2.5 units. Grip rim `#94afb3` at 2 units. Sole `#8d9c9e` at 2.5 units. Global exposure unchanged.

## Proportions and joints

- Criminal frontal head radii 61 × 65 world units; three-quarter Criminal 01 horizontal radius 52. Approximate full height 440 units (pose dependent).
- Criminal thigh/shin 85/85; support upper arm/forearm 90/87; free arm 65/63.
- Victim head 51 × 58; leg segments 77/80. The pelvis hangs about 137–139 units below shoulder height.
- Root governs pelvis and torso; shoulders derive from torso; neck/head from shoulder frame. Two-bone IK derives elbows/knees from their parent and constrained wrist/ankle targets. SVG groups retain joint annotations for inspection.
- Both grips lie at 53% along the corresponding victim upper arm. Grip graphics wrap the light sleeve; do not replace them with detached circles.

## Lighting and depth

Dark navy/teal illustrated alley, amber edge light, cel planes, no photorealistic textures. Separate distant buildings, walls, sedan, ground/contact details, characters and rain. Small local contact-light pool has maximum opacity 0.22; do not brighten the entire image. Heel and stance shadows touch the floor.

## Camera and edit

Shot A is medium-wide: scale 1.08, vertical translation -250 in the 1080 × 1920 layout. Tracking is `0.28 × world travel + 8 × smooth(t/0.8)`, with smaller distant-layer parallax.

Cut at frame 96 / 3.200 seconds. Shot B is a chest-up view of the same live vector rig: scale 6.0 to 6.22 over 1.8 seconds, aimed at Criminal 01's neck/head frame. No crossfade, random shake or still-image substitute.

## Timing and movement

- 0.00–0.45: hanging victim and clear grips.
- 0.45–0.90: knee/hip compression and backward bracing.
- 0.90–2.70: active pull, then deceleration to a planted stop at 3.20.
- Net travel: 300 world units. Stride: 100. Stance: 70%; swing: 30%, with a 31-unit maximum lift.
- Criminal 02 has a 0.12-cycle gait offset; foot anchors remain fixed through stance. At least one foot supports each criminal.
- Victim has no gait phase. Both heels follow one delayed drag trajectory, fixed ground heights 1413/1418 and 30-unit horizontal spacing. Both knees stay ahead of the dragging ankles. Pelvis follows with 0.09 s lag, heels 0.13 s; head follows the pull with delayed tilt.
- Cubic smoothstep controls pose changes; continuous acceleration/deceleration controls travel. Secondary motion follows the load, not an unrelated decorative oscillation.
- Head turn changes silhouette, cap seam/brim, eye alignment, mask chin and neck together; frontal by 4.00. Eye narrowing 4.00–4.50; hold through 5.00 with breathing.

## Rain, audio and future captions

Seeded rain layers have 300/220/85 streaks, speeds 520/760/1120 world units/s. Close-up uses 125 fine screen-space streaks so rain does not become oversized under camera magnification. Rain ripples and heel scrapes stay at ground height.

Audio is original procedural rain, wet foot plants, heel friction and a restrained cut accent. Footstep times derive from individual support phases. No voice or subtitles in this test; Whisper and yt-dlp are unnecessary.

Future caption recommendation, not implemented: short English phrases, white with a restrained amber emphasis, approved free font, roughly 52–64 output pixels; place after shot blocking, inside safe zones without covering eyes or grip contacts. The inherited alley labels now explicitly use installed DejaVu Sans; no font download.

## Export

1080 × 1920, 9:16, 30 FPS, exactly 150 frames/5 seconds; H.264/yuv420p, CRF 18, medium preset, AAC stereo 48 kHz/192 kbps, fast-start MP4. Preserve each prior output; new renders require new filenames.
