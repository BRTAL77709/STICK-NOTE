# THE PRICE OF SILENCE — 15-second movement test

This isolated movement test does not alter the locked storyboard or generate the full film.

- 00:00–00:06: constrained steering-wheel grips, wheel rotation, articulated elbows, mirror head/eye glance, approaching vehicle in mirror, acceleration response.
- 00:06–00:09: criminal anticipates, turns head toward camera, eyes shift, shoulders settle; lowered gun remains attached to wrist.
- 00:09–00:15: human running motion retargeted to the existing capped/hooded character; world-space foot pins and articulated hips, knees, elbows and wrists.

## Motion source and method

Recorded CMU motion 02_03 (run), BVH conversion credited to Bruce Hahne/CGSpeed. Original capture is approximately 120 Hz. Source: https://github.com/una-dinosauria/cmu-mocap/blob/master/data/002/02_03.bvh . Dataset notice is retained in reference/READMEFIRST.txt. No Mixamo download, reference-footage viewing, or Blender render is claimed.

The parser evaluates BVH hierarchy rotations in channel order. Source hand arcs and stride/contact timing drive the running rig. The stride is shortened to respect the stickman's fixed leg lengths. The small cycle seam is corrected in hip-relative coordinates. Stances pin feet in world coordinates; swings connect those pins smoothly. Two-bone IK keeps limbs connected. Neck yaw, eye direction and pitch are separate controls. Driving hands use shared rotating wheel-rim coordinates.

The test reuses the workspace's existing painted character parts and environment assets; no new image generation was used. Those assets were produced during an earlier approximation and are **not certified as an exact reconstruction of the locked reference**. The head turn is a constrained 2D yaw deformation, not a complete model with unseen head views. This is a technical movement test requiring human visual approval, not a claim of photorealistic human motion or exact final art fidelity.

Render: Remotion 4.0.419, React, SVG articulated rig, Chromium; compositing only. Blender 4.3.2 is available but was not needed for this test. A full production should replace any rejected art with approved layered character turnarounds without changing the recorded-motion/IK controls.

## Reproduction

Run source/parse_mocap.py using Python/numpy, bundle source/run.ts with esbuild, then node source/qc.cjs. Run source/audio.py with numpy/soundfile. Render source/Test.tsx, composition MovementTest, using the provided public assets at 1080x1920, 30 FPS, 450 frames. Mux test_mix.wav to AAC without changing duration.

No full-film render is authorized until the user approves movement. Original video files and main repository branch are preserved.
