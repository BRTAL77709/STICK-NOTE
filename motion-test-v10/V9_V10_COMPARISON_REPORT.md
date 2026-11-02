# V9 versus V10 — actual rendered-test comparison

| Area | V9 | V10 |
|---|---|---|
| Feet and bumper | Exact screen-space foot anchors still looked attached to the car silhouette | Shared pavement Z=0, three-quarter rear view, full legs shown below/beside bumper, zero projected shoe/bumper overlaps |
| Ground validation | Foot-lock calculations without a shared vehicle/foot ground plane | World-space soles, car footprint, projected bumper polygons and review overlays |
| Lift | Regular pose retiming with crowded rolled body | Two-person preparatory crouch, planted feet, fixed 3D bone lengths, offset hip/shoulder loading and a limited90° roll |
| Loading | Screen-space depth scaling and a head-first holdout | Body advances over the actual world opening, legs follow, then the horizontal body lowers into the cavity |
| Vehicle contact | Arm withdrawal could be difficult to distinguish from the panel | Raised shoulder/elbow routing and up-and-out hand withdrawal; no below-sill rear-plane centerline crossing |
| Depth | Primarily a front/rear painting split | Raised lid behind insertion, opening-derived side-wall corridor, near face in front, closing lid over the cavity |
| Head turn | Successful side-to-front projection after closure | Same projection module and timing order, plus grounded shoulder follow-through |

The side-by-side video uses the actual original-speed ten-second files. Both have equal duration; no hold or time stretch is applied. V10 audio accompanies the comparison.

V10 changes the camera and staging, so this is not a pixel-matched quality score. V9's screen-space trajectory numbers and V10's 3D world distances are not directly comparable. The strongest verified improvement is readable pavement placement and explicit separation from the bumper. The actual encoded review also shows a clearer torso-first placement path and uninterrupted closure before the head-turn cut.

Remaining weaknesses: economical finger compression, stylized center-of-mass control and some arm overlap during regripping. The sedan's hidden surfaces are reconstructed for this rear-three-quarter view using the same black body, navy/teal cel palette, window/taillight language and outlines. No exact match to unseen source geometry is claimed.
