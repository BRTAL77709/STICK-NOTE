# M08 source audit and repair boundaries

Actual M07 native sources, renderers, action controllers and final MP4 frame sheets were inspected. M07 is preserved. No V10 edits and no full-film assembly.

- `actions.py:state`: M07 driver had constant root/weak torso acting and angular elbows. M08 adds timed mirror attention, brake anticipation and shoulder/chest response before native IK, with invariant wheel/pedal targets. Native Blender geometry is rebaked.
- `legacy/curtain_test.py:fabric`: M07 used regular phase-aligned sine folds close to the wall, some displaced behind its plane. M08 uses irregular rounded folds varying down the fabric, sagging hem, material arc-length solve and curtain plane farther inside. Its state recalculates the gripping hand/digits from that new actual edge.
- `sets.py:bedroom`: harsh three-band shading and column ink stripes amplified the blind-like appearance. M08 uses six controlled cel tones and connected fold surfaces, retaining support rings.
- `approved_head_view.py`: M07 hid facial features on rear views but left a pale face silhouette. M08 adds the dark rear cap/skull contour, retaining the original facial proportions for front/profile views.
- `sets.py:city`: the road/city ended close to the far camera range. M08 extends the fixed route geometry while retaining the existing streetlight/reflection treatment. Route/state/House17 geography stays unchanged.
- `sets.py:door_live`: duplicate17 glyph on moving door removed while the static facade number is retained. Door, handle and key transforms remain the verified shared hinge/attachment system.
- `cameras.py`: six abrupt cockpit angles replaced with five narrative angles timed for seated acting, mirror discovery, steering, brake pedal and reaction. No random shake.
- `polish_stairs_m08.py`: opens actual M05 source and edits torso/arm counter-swing controls; root, world ankles, foot schedule, knee poles and rest bones retained. New evaluated native export is used by cinematic output, not the old M05 render/cache.

M08 does not falsely add a force simulator. Vehicle bicycle integration and no-stretch native IK are reused; fabric is a controlled material-width rig, not full cloth dynamics. Render/decode success does not establish artistic success.

## Confirmed shared camera-space defect

M07 `render_clips.scene` built cockpit/exit exteriors with a placeholder `Camera((1,1,-2),(0,1,0))`. `World.face` clips geometry at construction time, so clipping happened against that unrelated world camera before car-local transformation. M08 constructs the actual world camera from the car-local eye/target/up and car pose first. Driver projection invariance is measured independently; six culling/reference images were compared, including the vehicle turn. The initially undersized facade-group bound missed lamp-reflection pixels and was expanded before the affected final exports.

## Measured rendering bottleneck and safe optimizations

`RENDER_PROFILE.txt` identified90 library-resolution subprocess calls per frame for30 SVG glyphs: `source/legacy/svg.py:Raster.__init__` repeatedly called `ctypes.util.find_library` for the same three libraries. `_library` now caches the resolved CDLL handles while each Cairo drawing surface/context remains fresh. `FastDepth` caches pure color parsing and per-camera vertex projection, clearing projection caches every render. SVG glyphs now rasterize only the visible viewport region. Four sampled before/after glyph/ROI images were pixel-identical. These are rendering optimizations, not new animation/physics claims.

## Final curtain readability corrections

The curtain's gripping edge now stays on its intended plane instead of being dragged behind the witness by an endpoint sine phase. Header pins align with the rail tabs, and the rail has wall brackets. The final camera is on the gripping-hand side; native M08F was baked for that camera so its evaluated illustrated head card matches the view. The recoil look turns into the room so the frightened face is readable. Earlier internal variants are preserved, not presented as final exports.

## Running subsystem repair

`legacy/contact_rig.channel` uses a quintic easing segment whose velocity reaches zero at every waypoint. In the inherited run, native measured forward speed nearly stopped at each key and peak running root acceleration was44.906m/s². `run_repair.RunPlan` now uses a clamped continuous-velocity root curve, separate world landing targets, short stance/long swing timing, anchored toe-off, terrain-aware shoe clearance, counter-swing and a bounded smooth vertical solve. Native M08J running peak root acceleration is3.184m/s² at60Hz; foot contact tolerances still pass. The first smoothing-only trial regressed vertical acceleration and was rejected, rather than selected for delivery.

The city also clipped House17's local geometry with the outer world camera. `sets.city` now transforms eye/target/up into House17's frame before construction, then transforms its geometry back. Driver/exit exterior conversions retain correctly transformed world glyphs, making the17address readable at arrival.
