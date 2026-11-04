# Physical animation system

`physical_proofs.py` provides the five isolated, deterministic performances. `film_performance.py` integrates them into 18 scenes. `scene_builder.py` wraps vectors, and `render_scenes.py` renders independent clips with content hashes. HyperFrames only composites reviewed clips, captions and story graphics; it is not the character rig.

The approved V10 engineering approach supplies independent contact anchors, deliberate phases and 3D IK as a reference. The new stair solver uses metric 3D bones and a fixed projection, including foot pitch and swept shoe clearance. Other actors use articulated 2D IK on projected world targets. This hybrid is declared explicitly; it is not a full dynamics simulation or a claim that all limbs are solved in 3D.

Vehicle travel is SI world motion with distance-driven tires, curvature-driven steering and body load. Main-film acceleration starts only after the exposed pedal acquisition; its integrated trajectory rejoins the existing route at 38 s. Running contacts follow distance rather than a separate time clock, allowing upright body height. Props use actual hand/hinge targets. Entry is depth masked; a phone remains owned by its gripping hand. The stair landing seeds the curtain approach stance.

Source/trajectory/contact tests support actual normal/slow playback review. Do not infer animation quality merely from non-identical pixels, contact residuals or a valid MP4. All artistic approval remains with the user.
