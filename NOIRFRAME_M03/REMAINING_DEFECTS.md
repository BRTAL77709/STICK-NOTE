# Remaining known defects and review limits

All five tests are unapproved. None is permission to integrate the 86-second film.

- The character remains deliberately stylized, with simplified two-finger hands, tube limbs and shallow hoodie surfaces. Fixed-length/contact math does not establish convincing acting. Stair swing speed and door-route knee bends need normal-speed artistic review.
- Stair balance uses a linearized COM/pressure preview and reach constraints, not force/muscle simulation. Rail/ceiling and sampled joint clearance are bounded checks, not a watertight swept-mesh collision proof.
- The fifteen-second door test extends the six-second minimum to include all requested actions. It uses a close-up for the uninterrupted key action and wider exterior/interior phases for opening, entry and closing. No claim of full-volume skin/key collision is made. A conservative sampled body/door sphere test permits a 2mm tolerance; any residual overlap is reported numerically. The predictive C03 solver reduces that dip and removes acceleration spikes, but the remaining bend still needs visual review.
- Vehicle motion is a kinematic bicycle model, with approximate spring suspension and no tyre friction/drift simulation. Mirror uses a small projective feed, not ray-traced reflection. Window/glass, contact shadows, headlight falloff and wet-road reflection remain simplified illustrated representations.
- The curtain is a controlled fold rig with horizontal material-length preservation, sliding top rings and delayed response. It lacks full fabric self-collision, vertical strain simulation, wind and general hand/cloth collision. The reveal/head-turn clarity must be judged in playback.
- City geometry is a fixed connected test street. It does not yet cover every turn, parking, or all required editorial angles of the full film. Test lighting and environmental detail are limited; they are not used to conceal contact failures.
- These are silent motion tests. Foley, narration, subtitles, HUD and the final A/B choice are not repaired or approved by this package. Motion approval must precede sound/full-film integration.

If controlled fabric or contact silhouettes still fail review, the justified free replacement is Blender armature IK/object constraints with pinned cloth for the fabric and cel/Grease Pencil rendering. It is installed, but no claim is made that a Blender conversion has already been completed. The present implementation replaces the action controllers while keeping the functioning free renderer, rather than renaming a framework as a repair.

- Oblique views can still show sleeve/face overlap because the approved drawn head uses a depth-tested camera-facing glyph rather than a watertight head mesh. Full arm/head volume collision is not certified.
- The witness lamps follow its brake input; the pursuer lamp channel currently mirrors the witness brake flag rather than its independent longitudinal controller. This lighting limitation is not a vehicle-trajectory validation.
