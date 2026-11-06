# Scene-specific M07 → M08 repairs

|Scene|Actual change|Retained system / review limit|
|---|---|---|
|Driving12s|Rebaked timed shoulder/chest response to mirror attention and braking, revised elbow paths, five purposeful camera angles. Correct driver-local/world exterior clipping camera.|Same wheel/pedal attachments and vehicle integration; no force-driven body balance.|
|Road/buildings7s|Extended fixed road/city ends; existing facade assignments/geography preserved, frustum culling for off-screen geometry.|No new city geography or redesigned approved assets; facades remain stylized and procedural.|
|Chase11s|Shared rear head treatment and revised rebaked driver acting. Correct inside/outside camera transform, same fixed route and extended city with motivated coverage.|Existing120Hz two-car integration, closing gap and bicycle steering retained, not a new tyre-physics simulator.|
|Exit/running10.8s|Anticipatory look to House17, dark rear head silhouette, corrected world/car-local exterior camera clipping. Replanned running with continuous root momentum, individual terrain-aware foot targets, short stance, toe-off, pelvis/arm counter-motion and a bounded vertical trajectory.|Seated-to-standing phases retained; running replaced by source/run_repair.py and rebaked as native M08J.|
|Key/lock7s|Rebaked source with coherent rear-head treatment and same complete pocket/raise/insert/turn/withdraw mechanism; no gratuitous change to validated key mechanics.|Underlying key choreography is inherited. Head/scene clarity changes are not called a new hand-physics solution.|
|Door/entry13s|Timed look back outside, fear/readiness change, corrected rear head, removed duplicate moving17 glyph. Retains handle/hinge/threshold/closing/inside lock.|Native body/hand constraints retained; full hand and swept-volume collisions remain unproven.|
|Stairs5s|Actual saved M05 native armature edited for torso urgency and arm counter-swing, then freshly evaluated. New body geometry is rendered, not an old MP4.|Original root/ankle targets/poles/foot schedule retained. Depicts the last short flight and landing, not a newly animated entire two-storey climb.|
|Window/curtain10.5s|Irregular curved connected fabric folds, shaped hem and material-width solve; recalculated hand/digit targets; closer action framing; correct rear cap/skull treatment and existing sedan registration.|Rigged fabric, not full cloth forces. Native bakes were revised after16mm width regression was measured and fixed.|

All scenes have synchronized local procedural Foley and new outputs. Internal working previews are360px/10fps to inspect timing cheaply; final scenes are1080px/30fps. Final playback and encoded-frame checks are separate from those working previews.
