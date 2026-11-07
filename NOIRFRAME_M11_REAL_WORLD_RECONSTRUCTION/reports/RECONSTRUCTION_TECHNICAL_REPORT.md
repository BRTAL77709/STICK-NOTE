# M11 reconstruction — source and validation report

This is a new reconstruction from M10. The lost runtime's original M11 files were not recovered. No full-film assembly has been made. No artistic approval is implied by the engineering checks.

## Verified baseline and protection

Repository: BRTAL77709/STICK-NOTE. Immutable baseline commit: `651b19f30ac23278445a0b74da71fff5337e895e`.

Baseline: `NOIRFRAME_M10_ULTIMATE_CINEMATIC/M10_EDITABLE_SOURCE.zip`, 17,786,445 bytes, SHA-256 `35f3d894f3f8bcce0a9c6ae51ace08f5a9936c761e9ff14a958f3bd73dee68e6`. All 281 ZIP entries were independently verified. Immutable extracted reference: `baseline/m10/`. The selected native M10 projects are identified in `configuration/M10_SELECTED_NATIVE.json`; selected reconstruction projects are in `configuration/selected_native.json`.

Working directory: `/workspace/STICK-NOTE/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION`, a real directory rather than a pointer into `/tmp`. Dedicated remote working branch: `noirframe/m11-safe-rebuild`. Remote commits use GitHub's Git Data API; the original local checkout and earlier source directories remain unchanged. Every source milestone verifies the old remote tree entries outside this directory. Local pre-rebuild hashes and recheck results are in `PROTECTED_PREVIOUS_VERSIONS.json` and `PREVIOUS_VERSION_RECHECK.json`. The approved V10 trunk sequence is preserved; it has not been regenerated or edited.

## Verified backup method

Release creation was possible, but binary Release upload returned HTTP 401 Bad credentials. The active fallback uses ordinary Git, not paid LFS: exact-byte 8 MiB transport chunks, manifests with SHA-256, fast-forward-only commits on the dedicated branch, then pinned-commit downloads and whole-file verification. Small videos also have direct MP4 paths whose complete remote bytes are checked. Receipts are under `checkpoints/receipts/`; milestone commit receipts are under `checkpoints/commits/`.

`source/production_guard.py` requires a successful remote source/native restore drill and a current backed-up source checkpoint before production. Each 60-frame final batch is saved as persistent PNGs, packed, uploaded and downloaded for verification before rendering continues. `PRODUCER.json` prevents mixing frames from changed pixel-producing source. The first frame batch was also cold-restored and its PNG dimensions verified. See `BACKUP_RESTORE_DRILL.json` and `FRAME_BACKUP_RESTORE_DRILL.json`.

Identical-byte preview outputs exposed a manifest-label collision. The correction gives each immutable object a content digest plus a label/name namespace; earlier objects are preserved. Source packing now snapshots each member's bytes once so concurrent report completion cannot invalidate its hash. Redundant *transport archives only* may be evicted after matching a verified remote receipt; `REDUNDANT_ARCHIVE_EVICTION.json` records this. Original native projects, source, caches, outputs and resumable frames are retained.

Restore with `python source/restore_checkpoint.py --manifest-url <receipt.url> --destination <new-directory>`. The restore helper refuses unsafe archive paths and conflicting existing files.

## What controls the new images and motion

- `actions.py`: individual stance/swing schedules, foot targets, pelvis motion, hand targets, authored acting, stair-to-landing progression and room entry. Planted targets stay in world space; swing translates the foot only after lift.
- `bake_native.py`: retained M04 Blender armature, native two-bone leg IK, stable pole controls, fixed limb lengths, native hand/finger IK, per-frame evaluated body mesh. `blender/*_M11*.blend` are editable native rigs; `scenes/*.json.gz` preserve the corresponding evaluated geometry and source/blend hashes.
- `native_world_m11.py`: prop and environment hierarchy, wheel-parented hand targets, rigid phone and authored folded fabric, native scene camera/property keys.
- `vehicle_system.py`: one 120 Hz vehicle trajectory/bicycle model, wheel rotation from travelled distance, shared parked transforms and pursuit distance. This is kinematic vehicle motion, not a tire/friction dynamics simulation.
- `spatial_world.py` and `sets.py`: connected House 17, real door/window apertures, enclosing bedroom, stairs and landing, cabin geometry, registered street and sedan. R03 corrects the previously solid wall behind the bedroom window and aligns interior/exterior wall depth.
- `mirror_feed.py`: an actual rear-facing view of the shared world, clipped to the mirror aperture. It is a planar camera-feed approximation, not ray-traced glass.
- `cameras.py`: world-consistent shot cameras. `cameras_stairs_m11r04.py` and `render_stairs_m11r04.py` preserve the same verified R03 body geometry and correct the landing camera crowding in a separately versioned export. R03 images remain available as evidence, not silently replaced.
- `render_m11.py`: projects actual Blender-evaluated character meshes into the illustrated depth renderer; final raster samples at 1620×2880 and downsamples to 1080×1920. H.264/yuv420p, 30 fps, AAC and fast-start. Faces use the approved illustrated view-conditioned head treatment bound to the evaluated head, rather than a volumetric facial rig.
- `sound_m11.py`, `dialogue_m11.py`, `overlays_m11.py`: local WAV/voice assets, footsteps/contact-derived events, vehicle and cloth sound, phone speech timing, subtitles/HUD and A/B presentation. No paid generation services.

The native projects contain the body/prop/world work, but the final cel look, illustrated head, captions and compositing require the accompanying Python/C++ renderer. This is not advertised as a one-click Blender-only final-look project.

## Numerical evidence and scope

`NATIVE_CONTACT_QA.json`: eleven selected native character shots evaluated at 30 Hz, with 60 Hz dense joint caches. Actual native wrists, fingertips, shoes, limb lengths and connections are measured against authored targets. Tolerances: wrist/leg IK 1.5 mm, finger target 2 mm, stance/contact 1.5 mm, limb length/connection 0.1 mm. All selected native shots pass these scoped checks.

`STAIRS_NATIVE_120HZ.json`: 2,040 samples of the actual selected R03 native rig. Maximum stance drift 0.002983 mm; tread error/penetration 0.002488 mm; limb length variation 0.000786 mm; connected-bone gap 0.001974 mm. Root rises 2.60000008 m. These are target/contact measurements, not a claim of force-based balance or universal collision freedom.

`CAMERA_QA.json` and `GEOGRAPHY_QA.json` check camera origins against explicit bounds and a head envelope, registered vehicle coordinates, native scene endpoints and the real facade window ray. They do not prove good composition or unobstructed image rays. Visual review found the staircase landing framing problem despite those checks; the R04 camera correction is separately identified.

`SHOT_BOUNDARY_LIMITATIONS.json` records a 126.84 mm exit-to-key root gap that still needs editorial/motion conform before a continuous film. Key-to-door root difference is 0.0157 mm, door-to-stairs 0, stairs-to-bedroom approximately 0.0000843 mm. Standalone clips are expanded and overlap in story coverage; summing them does not produce an 86-second edit.

`FINAL_EXPORT_QA.json` is populated only after completed files pass complete decoding, exact dimensions/frame count/rate, H.264/AAC, duration and atom-order checks. Browser playback reports record normal and half-speed playback, SHA-256, corrupted frames and actual presentation samples. Dropped presentation frames under concurrent CPU load are reported rather than mislabeled as corruption-free artistic approval.

## Remaining artistic and technical limitations

The overall look remains a stylized prototype: blocky interior/exterior furnishings, restrained emotional acting, limited facial deformation, and flat lighting in some angles. The rear-seat cockpit view naturally occludes portions of the driver and wheel; geometric contact accuracy alone does not make those actions sufficiently readable. Cloth folds are deliberately rigged, not a physical cloth solve. Contact validation uses named shoes, bones, fingertip proxies and selected prop surfaces; it is not exhaustive swept collision testing of every polygon. Sound levels and dialogue delivery still need a human listening/artistic review. Some inherited cue timing remains authored rather than triggered by evaluated collisions.

The M10 storyline conflicts and other audit/conform issues are itemized in the story audit rather than hidden by a premature full-film render. No 10/10 quality claim is made. User review is required before production approval or full-film assembly.
