# Technical validation — exact delivered integrated test

File: THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_INTEGRATED_TEST_15s_FINAL.mp4.
Size: 4414974bytes. H.264/yuv420p,1080×1920,30/1FPS,450decoded picture frames. Both video and48kHz stereo AAC start0.000s and run15.000s. Full FFmpeg decoding completed successfully. The corrected_v2 and delivery H.264 packet hashes are identical; delivery audio is freshly encoded from original PCM with−0.3dB headroom trim, not from an AAC intermediate.

The exact delivery file completed1x Chromium playback in15.190s, reached ended=true at15s, with450total frames,0dropped and0corrupted display frames. Complete presented-frame evidence is in reports/DELIVERY_playback.json and previews/DELIVERY_presented.jpg. Original and corrected30FPS previews and final_v2 also completed with zero display drops/corruption. Contact sheet comes from the exact delivered encoded video.

Final AAC measurement: -16.24LUFS integrated, -1.69dBTP, 7.50LU range. Original PCM mastering report is separate. These measures verify signal levels; synthetic prosody/engine realism/mix suitability still need human listening and creative review.

No black interval was detected in corrected_v2. Whole-frame freeze heuristic flagged5.1–6.0667s and9.9667–11.3s, both largely fixed dashboard housings with moving needles/numbers. All93 consecutive selected decoded cluster crops differ; see reports/needle-motion-check.json. These flags are not silently treated as missing footage or ignored without inspection. Needle movement is also visible in the consecutive-frame sheet.

All450source poses evaluated. Speed/instruments/RPM/engine use common deterministic state. Maximum speed-position derivative error<0.00047m/s, separate pursuer<0.00032m/s.0.32m wheel-roll distance is exact in the model. Hip/shoulder/elbow/hand actions are source-constructed, not a full physical simulation. These numerical results cannot certify every perceptual contact or artistic defect.

No86-second rerender occurred. Full-film-v1,V10 and all previous repository content are retained. A separate expected-head GitHub update publishes only the new directory; remote tree hashes/sizes and actual public download are checked separately.
