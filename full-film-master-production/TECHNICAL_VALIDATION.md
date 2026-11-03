# Technical validation — 86-second master

The original HyperFrames export is `renders/final/THE_PRICE_OF_SILENCE_MASTER_86s.mp4`. It is preserved and published (13,399,267 bytes). A separately named, smaller H.264 download encoding is also supplied (9,673,740 bytes); it does not replace the original export. The authenticated CLI transferred the original after connector binary uploads stalled.

## Original encoded media

- 1080 × 1920, H.264, yuv420p, 30 FPS; 86.000 seconds; 2,580 decoded frames.
- AAC, 48 kHz, stereo. Full FFmpeg decode exited 0.
- All 2,580 reduced-resolution frame samples were nonblack; minimum mean luminance-channel value across RGB samples was 11.94/255. No adjacent samples were byte-identical. These checks do not prove good choreography.
- Encoded audio measured −16.03 LUFS integrated and −3.63 dBTP. These are the meter's **input** values, not its hypothetical normalized output.
- Actual Chromium playback reached the end at rate 1: 86 seconds media time, 86.52 seconds wall time, 2,580 total frames, 2 dropped display frames, 0 corrupted frames. Canvas sampling was enabled; this is not a zero-drop claim. See `reports/MASTER_playback.json`.

## Source and composition

The smaller download encoding independently passed full decoding and the same dimension, rate, duration, codec and audio checks. Its Chromium playback ended at rate 1 in 86.50 seconds, with 2,580 total frames, 1 dropped display frame and 0 corrupted frames. One adjacent reduced-resolution frame pair was identical; no black frames were detected. Audio is copied from the original export. See `reports/download-*.json` and `reports/DOWNLOAD_playback.json`.

Source validation evaluated 2,580 poses and 2,581 vehicle-state samples. Exported state matched the live model exactly. Position/velocity integration error was at most 7.63e−7 m/s. Pitch sign, trunk-close-before-turn, unlock-before-open and close-before-relock assertions passed. Thirty narration phrases have measured timing; word alignment is unavailable. See `reports/source-validation.json`.

All 1,759 previously recorded local files matched their preservation hashes; none changed or went missing. Common approved V10 functions match their original source. See `reports/v10-preservation.json` and `reports/previous-version-hashes.json`.

The official local HyperFrames 0.8.226 check passed before export, including browser checks, with no reported errors or warnings. The final render used software GPU screenshot capture, not a paid generation API. See `reports/hyperframes-export-check.json` and `reports/hyperframes-master-render.log`.

## Limits

Foot/hand choreography was reviewed visually in interaction strips; no blanket automated zero-slip/zero-contact-error certification is claimed. Voice quality and sound balance require human listening. The ASR-weight request was proxy-blocked (403), so captions use actual phrase timing rather than claimed word transcription. Public download verification is recorded separately only after a successful HTTP download and SHA-256 comparison. Artistic approval is separate: read `ARTISTIC_QUALITY_REPORT.md`.

## Published delivery verification

Commit `97b9b61ee4b4af4656180ecbaa511e5ca4621cb6` contains the original movie and source package. All 290 manifest objects matched GitHub blob hashes; all 612 prior repository entries remained unchanged. Thirteen public raw downloads, including both actual MP4s, contact sheets, reports, source and narrator/caller/mix audio, returned HTTP 200 and matched local byte counts and SHA-256 hashes. See `reports/download-verification.json`. This confirms delivery access, not artistic approval.
