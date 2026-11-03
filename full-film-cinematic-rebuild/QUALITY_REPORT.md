# Integrated test — technical and artistic review

Scope: new15-second systems test only. All18full-film scenes were audited; they have NOT all been rebuilt/rendered. No86s rerender was started. User creative approval is pending.

## Review evidence and corrections

The original and corrected360×640/30FPS previews both played to15s with450frames, zero dropped or corrupted display frames. A final revised8FPS preview played to15s with120frames, zero drops/corruption. Whole-duration encoded sheets and consecutive quarter-second strips were inspected. Later targeted motion strip checked the driving-acceleration beat, pursuit, instrument and OTS steering patch. The final-resolution file is independently probed, decoded, played and reviewed; measured results are recorded below after verification.

Corrections made during these loops: camera distance that initially clipped the pursuing car; caption collision with small dashboard/foot; wiper crossing face; wheel radius mismatch; road centerline arc-length distance; separate pursuer catch-up odometer/speed; rounded vehicle ink contours/wheel arches; a driver shot during acceleration rather than only before it; road-linked16:1 steering-rim rotation and articulated OTS grip.

## What the test actually demonstrates

|Requirement|Implementation/evidence|
|---|---|
|Moving illustrated city|World-fixed curbs, lanes, cross streets, windows/doors/gutters, drains, poles/wires/signs/trees, depth sorting and tracking; background changes with actual road position.|
|Vehicle motion|Integrated metric travel;0.32m tire spin; steering from curvature; pitch from acceleration; roll from lateral load; suspension bob and wet tire spray.|
|Acceleration/instruments|20→100km/h over8.6s; needle/digits/road/wheels/RPM/engine share state. Pedal begins4.2s; explicit driver weight response at6.5–7.4s.|
|Chase coverage|Exterior track, driver reaction, pedal, physical cluster, driver acceleration, road-level pursuit, second cluster, OTS, culmination cluster and mirror reaction.|
|Contact/acting|Driver elbow IK anchors to rim; boot toe tracks pedal; heel stays planted; shoulders/neck/eyes/blinks/breath/tension move. All450source poses evaluate.|
|Audio/captions|Four actual local English phrases and measured durations; RPM-integrated engine, wet-road/rain, original score, ducking and stereo mix; phrase-aligned SRT/burned captions.|
|House/props|Shared hinge/lock/key geometry prototype and source/order check. Full house/curtain/phone remain planned, not claimed complete.|

Source numerical checks in reports/source-validation.json: maximum world-speed discrepancy under0.00047m/s from arc-length interpolation; separate pursuer discrepancy under0.00032m/s; maximum witness acceleration3.876m/s²; exact tire odometer/radius relation. These do not replace visual/artistic review. The engine is a deterministic synthesized approximation, not a recorded real car.

The PCM master measures−16.14LUFS,−1.50dBTP and6.70LU loudness range (reports/audio-master.json). Final AAC is checked separately. Signal measurements and browser playback are NOT a claim that a person has judged narration, engine realism or mix on speakers.

## Remaining artistic limitations / next-stage work

- Flite narration is intelligible synthetic speech with mechanical prosody. A distinct anonymous caller is planned for the later film; it is absent from this driving excerpt.
- The sedan is an outlined geometric illustration with simplified surfaces, rather than a detailed hand-painted model. Surface finish and final silhouette fidelity need user review. Tire spokes may show temporal aliasing at high speed despite correct metric rotation.
- The city has persistent spatial depth and architectural detail, but it remains procedural and lacks the reference film's hand-painted texture density. This test shows a shallow continuous bend/intersections, not a complete90-degree chase-turn set piece.
- Driver reactions use constrained illustrated rigs and simplified face states, not phoneme-accurate speech or full physical simulation. Some rear-body limbs are intentionally occluded by the seat/car framing.
- The mirror establishes following headlights using gap-derived scale; it is a graphic mirror treatment, not a full physically reflected render of the black sedan.
- Full House17 exterior/interior/curtain/phone integration, richer victim/criminal acting and the final choice screen remain future work after the test gate. The door/key prototype requires a more oblique close-up to make shaft insertion more legible.

No10/10 score or blanket professional-quality certification is asserted. Review the MP4 for driving urgency, visual identity, body weight, readable acceleration, engine/narration quality and whether this direction meets the rebuild bar.

A first1080p export exposed a near-plane road-edge pop. World polygons now clip at the near plane instead of disappearing as whole faces; the low camera was moved from the curb into the roadway. The initial export and all preview drafts remain local; the delivered_v2 export incorporates the fix.

## Exact delivered-file verification

15.000s/450frames,1080×1920/30FPS,H.264/AAC. Full decode succeeded;1x playback ended with0drops/0corrupt frames. Final AAC: -16.24LUFS/-1.69dBTP. The freeze detector flags near-static dashboard housings;93/93consecutive cluster crops are unique. Detailed evidence: TECHNICAL_VALIDATION.md and reports/. Artistic approval remains pending.
