# Technical validation

The delivered integration demonstration is a new7-second evaluation at1080×1920,30 FPS,H.264/AAC. It is not a regenerated86-second movie. Exact report: reports/demo-validation.json.

Actual successful checks:

- Remotion rendered210 per-frame SVG scenes from the existing articulated/metric evaluators.
- HyperFrames check passed; the local editable preview respondedHTTP200. The120-frame HUD is ProRes4444,920×300,30 FPS with yuva444p12le alpha; decoded alpha has transparent, partial and fully opaque pixels.
- FFmpeg placed the HUD at(80,140) from global frame90, using the same frame-state array as the car. It mixed actual retained speech at0.933333 s and encoded captions from measured source-script timing.
- Full final decode has zero errors. All210 frames are nonblank. There are no unexpected duplicate frames. The original evaluator intentionally holds brief contact/anticipation poses; source-derived hold indices are disclosed rather than mistaken for accidental liveness.
- Ten exact-frame subject regions match the raw Remotion scene within4/255 mean absolute difference, excluding HUD/caption regions. Real pedal/joint/prop/car movement survives composition.
- Encoded speech has0.99992 zero-lag waveform correlation with the prepared reference, supporting sample-clock synchronization. This is not subjective listening certification.
- All4544 pre-existing STICK-NOTE files match their preservation hashes, including previous films and V10. No previous86-second file was overwritten.

Normal/half-speed browser presentation and exact HUD state checks are saved in reports/playback-and-hud-sync.json after successful completion. These are technical checks, not artistic approval.

Whisper package installation is real; model inference is blocked by proxyHTTP403. The demo does not contain Whisper-produced subtitles. Its source-script fallback is explicitly named and recorded. Word alignment is not claimed. yt-dlp installation/version is verified; external media fetching is intentionally unexercised because no approved new URL was requested. Supplied reference footage/music was not reused.

No full-film production is authorized or started by this setup. Future story actions require separate scene authoring, contact/foot/prop review and listening QA.

Completed presentation review: normal playback7.376 s,210 frames,5 browser presentation drops and0 corrupt frames; half-speed14.427 s,0 drops/corrupt frames. Full encoded decode is independently clean. Seven actual DOM HUD samples match exact master frames90,91,105,120,150,180,209; an off-by-one caused by rounded fractional GSAP time was corrected using integer-frame selection. The two presented-frame sheets and final contact sheet were inspected. No subjective audio listening or artistic approval is claimed.
