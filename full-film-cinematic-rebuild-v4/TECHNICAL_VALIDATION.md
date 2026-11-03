# V4 technical validation

Final: THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4, 7,689,479 bytes. H.264/yuv420p, 1080×1920, 30/1 FPS, 450 decoded frames, exactly 15.000000 seconds. AAC audio: 48000 Hz stereo, 15 seconds; both streams start at zero. Full FFmpeg decoding passed. All 450 downsampled RGB frames are nonblack and no adjacent pair is pixel-identical; this does not establish subjective motion quality.

Actual normal-rate Chromium playback with presented-frame JPEG capture completed the movie with three display drops, zero corrupt frames and 450 total frames. That report and presented sheet are preserved. A separate isolated repeat without JPEG capture completed at rate 1, currentTime 15, wall time 15.2325s, 450 total frames, 0 drops and 0 corrupt frames. The unmodified six-second HyperFrames demo completed 180 frames with 0 drops/corruption.

The final encoded AAC measured -16.04 LUFS integrated and -1.89 dBTP. Mastering and cue reports are included. Audio was measured, not heard; naturalness and subjective synchronization/performance remain pending listening approval.

All 451 source poses evaluate. Maximum exported-state error is 0.0; hand-wheel target error is 0.0 px; arm-length error is 2.56e-13 px. Position/velocity consistency error is at most 2.73e-05 m/s. Wheel rotation uses each vehicle's 0.32 m tire odometer. The steering wheel spans about 37.17°. The shared trajectory reaches 96 km/h and exits at 64 km/h, with a route heading change of about 47°. Actual relative positions supply pursuit distance. The pitch sign was corrected so acceleration raises the front and braking lowers it.

HyperFrames 0.8.226 rendered the complete final composition and the HUD demo through its official local CLI. The logs show screenshot capture/software GPU, not a hardware GPU or paid cloud render. HTML templates, paused registered GSAP timelines, hf-seek updates, 451 exported data samples and the real media inputs are supplied. Checks, snapshots and rendering logs are in reports/. Source-level motion assertions cover the clock and instrument/pursuit panels.

Quarter-second encoded contact frames, the driver/contact strip, role-matched V3/V4 frames, HD HyperFrames snapshots and the 360-pixel review sheet were inspected. Corrections include gauge typography/clipping, pivot bounds, pursuit-label wrapping, caption fit, hand orientation, hood detail and body pitch. The silent demo is intentional.

Hashes of all 1,619 prior local files match; no prior version, including V10, was altered. Remote preservation and actual public download hashes are verified separately. No full 86-second production occurred.

Limitations: exact HUD reference image unavailable; no verified word alignment, so production captions use measured phrase windows; voice and subjective motion quality require user review. The illustrated vehicle/world model remains simplified.
