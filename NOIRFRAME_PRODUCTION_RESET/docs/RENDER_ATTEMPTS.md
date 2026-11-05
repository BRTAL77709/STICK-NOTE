# Render attempts and exact limitations

Native Cycles with emission materials and Freestyle was tested and used for the low-resolution animated previews. Eight-sample1080 rendering with three concurrent CPU jobs proved expensive (roughly15–17s per frame per job). Those earlier jobs were terminated before completion. Their partial MP4s remain local and are excluded from delivery. An initial SIGINT cancelled only an individual Blender render; the loop continued, so the renderer was repaired to require the FINISHED return state and final decoded frame-count/duration checks. The old partial files are not valid deliverables.

The selected native proof renderer is Blender Workbench, flat material colors, FXAA, object outlines,1080×1920. A measured three-frame probe took2.32s for initial setup then0.61/0.60s per frame in isolation. Concurrent full-shot jobs are slower. Workbench successfully uses software OpenGL despite EGL setup warnings; these warnings were not treated as a successful render without file/decode checks.

Workbench preserves the native geometry, IK, prop transforms and camera projection. It does not reproduce the custom Cycles cloth shader, cinematic illumination or Freestyle line treatment. This is a performance/style tradeoff, not evidence that the approved illustrated look has been reproduced. Render availability does not pass the artistic gate.
