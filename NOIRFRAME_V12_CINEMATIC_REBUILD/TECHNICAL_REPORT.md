# V12 technical validation and limits

Authoritative pipeline: independently constructed perspective world → fixed-length articulated/contact state → per-pixel reciprocal-depth cel raster → streamed native1080×1920 RGB frames → FFmpeg H.264/30FPS + diagnostic AAC. No source pose images, slideshow or old footage drive the new motion. Old videos are used only as before/after inputs.

The world coordinate convention is metres, XYZ/Y-up. Blender companion files map to XYZ/Z-up as(x,z,y). A stable house entrance,12×0.20m risers/2.40m upper floor and actual window aperture support coherent architecture. The city uses deterministic world addresses along one fixed road centreline. Camera changes are deliberate storyboard cuts and a continuous stair/porch track, not hidden world teleports.

Valid V11 IK/contact mathematics are reused explicitly. The staircase F01 preserves the earlier ink-depth policy, documented in source/versions/STAIRS_F01; later line-bias fixes target ring/prop overdraw in the other shots. Shared active-source hashes written at render end are provenance observations, not a claim of immutable import-time code. No byte-identical source rebuild claim is made.

See reports/RENDERED_STATE_VALIDATION.json for the final-file pose checks (including seated-driver/wheel contacts), and reports/RIG_CHECKS.json for pre-render action checks. These cover every-frame fixed-length bone, planted-sole displacement, sampled lever/cloth contact and integrated vehicle travel checks. These are bounded numerical tests, not full garment/hand-volume collision tests or artistic certification. The native Blender file is a supplementary spatial/IK editing scene; the Python renderer is the source of truth for the reviewed pictures. Its reference IK controls and static architectural state do not replace the authored Python driver/cloth motion.

Actual preview playback is recorded under reports/*preview-playback.json. The first House preview failed visual inspection because its inside camera was behind a wall. That camera and the obstructed key insert were fixed in P02. The first driving attempt stopped on an unreachable arm target and was preserved as partial; the wheel was moved closer and all360 driving poses evaluated. A later preview's footwell camera was inside a seat; P03 fixes it. Busy-preview browser drop counts are reported rather than suppressed. Final-file playback/decode results are recorded separately in FINAL_PLAYBACK.json and MEDIA_VALIDATION.json.

The diagnostic track contains authored synthetic contacts/engine tone and low-level noise. No professional listening approval, final Foley material realism, narration alignment or full-film mix is claimed. Remotion editorial verification and Blender execution are recorded by their actual tool logs. HyperFrames is not claimed as used in these proofs.

The18-scene film remains outside this review delivery. No full V12 was rendered, no paid services were used, and artistic approval remains pending.

The current renderer also culls invisible box backs, uses float32 image buffers and caches a fixed road centreline to reduce software-raster cost. These are image-performance changes; joint/contact calculations remain float64. Earlier F01 exports began before these optimizations. Editing sources reproduce the staged action; exact encoded-byte identity is not claimed.

Bed F01 was visually readable as a cheek/phone gesture despite exact cloth endpoint constraints. The selected Bed F02 mirrors the approved head to face the pull and offsets it from the grip; cloth and foot contacts are unchanged. Its revised preview and final playback are recorded separately. F01 remains preserved and is not the submitted bedroom proof.

## Selected media

| Shot | Duration | Frames | Format |
|---|---:|---:|---|
| STAIRS | 9.400000s | 282 |1080×1920 H.26430FPS|
| HOUSE | 13.000000s | 390 |1080×1920 H.26430FPS|
| BEDROOM | 8.400000s | 252 |1080×1920 H.26430FPS|
| DRIVING | 12.000000s | 360 |1080×1920 H.26430FPS|

All four were fully decoded with FFmpeg. The12,257 protected prior files had zero changes/missing files. Bounded render-state checks include300 seated-driver poses,600 wheel contacts,88 cloth grip samples and no door arm-centreline crossings. No full collision-volume or whole-film continuity approval is claimed.

Driving F01 was superseded after a physical-scale check found its seated cap exceeded the exterior1.48m roof. Driving F02 lowers the pelvis/seat without changing limb lengths, adjusts the wheel, and matches inner windshield pillar coordinates to the same exterior windshield. The interior roof is1.46m. A sampled conservative cap bound is included in rendered-state validation. The exterior car and world trajectory remain unchanged. The native R02 companion is regenerated from this source; it remains a reference/editing scene rather than the final illustrative renderer.

The selected Driving F03 retains the corrected F02 cockpit/seat and replaces only exterior frames165–224 with new native-HD frames. Tyres are unsprung, centre0.30m/radius0.30m, while the body retains its roll. Existing shot boundaries and synchronized audio are preserved; no new cuts conceal the action. The unchanged cabin frames are reused explicitly.
