# Exact code changes

All changes are under `NOIRFRAME_M03/`. No earlier production source is edited. M01 is rejected and serves only as a labeled comparison source.

- `source/rig.py:ik`: fixed segment lengths, copied pole vector, explicit reach/angle limits; raises on impossible targets.
- `source/contact_rig.py:pose`: explicit hierarchy/chest/neck contract and heading-relative knee bend plane. `step`: revised early lift/continuous horizontal travel and toe-off pitch. Existing colour/design proportions retained.
- `source/stair_test.py`: entirely new four-riser schedule, lower-floor start, landing recovery, support-based horizontal plan, constrained pelvis height, differentiated torso/arm timing and explicit tread indices.
- `source/locomotion.py:ground_feet`: immutable floor touchdown points for the door route, alternating support and swing arcs. It does not translate planted soles with the root.
- `source/key_test.py`: new fifteen-second action state machine, approach/retrieval/alignment/insertion/return/withdrawal/stow/regrip/open/entry/inside regrip/closure. Routes around the open leaf instead of through it. One hand identity and one door state across angles.
- `source/vehicle_dynamics.py`: replaces road-interpolation motion with steering-input-driven bicycle integration, independent pursuer controller, per-wheel travel and acceleration-driven suspension.
- `source/vehicle_test.py`: reuses the established seated proportions and pedal geometry, connected to the new unified dynamics and controls. Accelerator release precedes foot transfer; brake pressure follows brake contact.
- `source/curtain_test.py`: new arc-length-preserving folded fabric rig, fixed rail/sliding rings, contact edge, grip/loosen timing, reveal freeze and delayed head/torso recoil.
- `source/head_25d.py` and `source/head_view.py`: continuous cap/brim rear-view construction derived from the approved drawing, camera-relative approved front/profile drawing plus reconstructed back-of-cap silhouette; no frontal eyes painted on a back view.
- `source/actor.py`: calls view-relative head renderer while retaining approved limb/hoodie/head dimensions and articulated finger geometry.
- `source/geometry.py:car`: per-wheel phase, Ackermann front tyre directions and brake-state lamps; preserves existing sedan design.
- `source/shots.py`: new explicit staircase solids, actual slotted door/cylinder/full key geometry, fixed city/route, coherent cabin/rearview feed, bedroom/window/fabric scene and clean camera phases.
- `source/render.py`: clean and diagnostic encoders from the same fresh frame; contact markers, joint chains, target/trajectory overlays, lock axes, vehicle telemetry, fabric grid; losslessly compressed exact-state exports and freshness hashes.
- `source/qa.py`: every-frame bone, planted toe, stair sole, sampled limb, door/body, independent prop-surface, insertion axis and fabric material-length checks. Numeric status is separate from artistic review.
- `source/prove_freshness.py`: isolated source-edit/render sensitivity test.
- `source/review_playback.py`: actual Chromium normal/half-speed playback evidence, copied into the new folder.
- `source/export_review.py`: native-media decode, unretimed before/after assembly, all-frame contact strips and inspection index.

Unchanged supporting copies: `source/approved_head.py`, `source/world.py`, `source/depth_render.py`, `source/svg.py`. Their hashes are compared to M01 in the preservation report. New camera/cloth geometry does not imply approval of the character motion.

- `source/repair_diagnostic_projection.py`: derives revised steering/chase diagnostic overlays from the new clean C02 frames and their exact rig states. Converts local grip markers into world space for the exterior view and removes unrelated cockpit markers from the chase view. This changes diagnostic overlays only; it is not presented as a new physical animation render. Both inputs and outputs have hashes. `source/finish.py` runs final QA, that overlay repair and review export sequentially.

- `source/stabilize.py`: new predictive, contact-feasible pelvis solver using installed SciPy bounded least squares. Removes frame-local height-clamp acceleration spikes, smooths X/Z, retains fixed foot/grip targets and rebuilds joints. `stair_test.state` and `key_test.state` wrap their original action generators with this solver. Other three tests retain their C02 animation.
- `source/make_report.py`: exported-frame provenance, measured root speed/acceleration, independent acceptance matrix and source archive.
- `source/plot_trajectory.py`: plots acceleration derived from the actual before/after rig states; no render animation is changed by the plot.
