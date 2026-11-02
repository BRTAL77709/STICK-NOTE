# V8 technical validation

## File and playback

FFprobe: H.264, 1080×1920, 30/1 FPS, **240 frames**, **8.000000 seconds**, 3414037 bytes. Full FFmpeg decoding completed without errors. Blackdetect reported no black intervals. AAC audio is present (48 kHz stereo); measured maximum −6.2 dB and mean −27.0 dB. This is quiet cinematic ambience, not a mastered narration mix.

The corrected 540×960 preview played to completion at 1×: 240 frames, zero dropped/corrupted frames. The first final-resolution browser check recorded four presentation drops, while all encoded frames decoded correctly. A longer-buffered isolated repeat completed at 1× with 240 frames, zero drops and zero corruptions, as did comparison playback. Both final attempts are recorded in playback-verification.json. These are automated Chromium playback/canvas checks, followed by visual inspection of the presented-frame sequences; they do not constitute artistic approval.

## Six-beat timing

| Time | Implemented action |
|---|---|
| 0–1.5 s | Separate step schedules move both criminals 110 world units toward the sedan's rear. Victim hips hang 138 units below the shoulders and shoes scrape the pavement. |
| 1.5–2.5 s | C02 receives a waist support before C01 releases his upper-arm grip. C01 unlatches/pushes the lid, releases at 1.94 s within arm reach, and the struts complete opening by 2.42 s. |
| 2.5–4.5 s | Deliberate regrips, deep knee/hip lowering, then extension and coordinated lift. C01 supports upper arm/upper back; C02 supports waist/pelvis and knee. Both victim feet are more than one unit clear by 3.5667 s. |
| 4.5–5.8 s | Passive lower legs fold over the sill, torso rolls further and the knees articulate during insertion. Head-first entry runs 4.92–5.72 s; body remains visible in the dark open cavity. Support hands release sequentially only after placement. |
| 5.8–6.4 s | Support releases finish, criminals step away with separate footfalls, C01 raises/changes posture and attention. |
| 6.4–8 s | One authored cut to C01's preserved side-to-front head turn, then eye narrowing and held stare. |

## Contact, rig and car checks

All 240 scenes evaluate with strict two-bone reach checks; no unreachable targets are silently clamped in the criminal rigs. The victim's passive shoe lag is constrained by fixed leg reach before solving its knees. This prevents stretching during lift-off.

- Maximum world-space stance movement: **0**. Every criminal always has at least one stance foot. Swing paths and subsequent anchor positions are distinct.
- Maximum gap at the explicitly active named support targets: **0** in the deterministic pose model. Grips are handed off with overlap; free hands deliberately traverse to new targets before contact begins. No claim is made that every hand remains on the same location throughout regripping.
- Criminal torso joint distance: 125 units throughout. IK leg segments remain 85/85 and support-arm segments 90/87. Victim legs remain 77/80, with projection scale removed for measurement.
- Maximum rounded-SVG segment variation after projection normalization: **0.022400 units**.
- At 4.5 s the two victim ankle/shoe anchors are at y≈1273.32/1270.97, versus pavement y=1480/1488. Neither shoe penetrates the pavement during the initial lift.
- During 4.5–5.72 s the torso angle changes ≈−82° to −96° and the sampled right-knee angle ranges ≈93.3°–170.9°. Loading therefore includes articulation rather than a single frozen body moved as one object.
- Sedan body, wheels, rim and rear fascia use invariant coordinates. Lid vertices keep invariant x coordinates and rotate through one trigonometric hinge transform at y=1005; no car morph is used. Fully open angle: 102°.

## Depth and pixel review

The sedan is restaged from V7's three-quarter view to a rear view. Its closed/open geometry is one consistent V8 model, not a claim of exact match to hidden surfaces in the composite sheet.

The victim is projected progressively into depth with a uniform 1→0.88 scale. The identical pose is drawn on either side of a head-first entry plane: inside parts are clipped to the cavity, then the fixed near sill is painted over them; outside parts stay in front. There is no alpha fade or abrupt whole-body disappearance. The victim remains visible lying inside the open trunk after release. This is an authored 2.5D holdout solution, not a collision-certified 3D simulation.

The contact sheet samples all beats and both sides of the frame-192 cut. Loading detail samples 2.5–5.8 s every 0.1 s and shows the final placed pose. Actual decoded foot crops show fixed shoe positions with knee extension above them. Dense arm/head overlap during the middle of loading remains an artistic readability limit. No unexpected large frame pop or blank interval was found in the inspected sequences; the intended cut is the largest frame change (15.41 versus 3.76 maximum elsewhere).

## Head preservation

`draw_head`, `draw_head_legacy`, `hull`, `curved_outline` and `reaction` are byte-identical to V7. The V8 input clock maps `3.2 + (t−6.4)×1.125`, fitting the earlier turn into 1.6 seconds. Cap, mask silhouette, neck projection and eyes turn coherently before narrowing. Only staging/body posture and the time adapter changed.

## Limits

This test uses authored support poses, deterministic IK and explicit phase lags, not full mass/contact dynamics. C02's supporting crouch is exaggerated. Gloves have limited finger deformation, and overlapping arms briefly obscure part of the victim. Technical contact checks cannot certify that the acting feels heavy enough; judge that from the video.
