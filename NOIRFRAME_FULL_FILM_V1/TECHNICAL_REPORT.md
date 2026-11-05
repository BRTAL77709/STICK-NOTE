# Complete-film technical report

Delivered file: renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4.

- 86.000s;2580 decoded video frames;1080×1920;30/1FPS;H.264 High/yuv420p;AAC48kHz stereo.
- 16,677,566bytes;SHA256 `05838df3a154373bd54507b5fbc3d3030de2f6b0b5da6e351532bc132335136e`.
- Full FFmpeg audio/video decode passed without errors. All2580 reduced RGB samples were nonblack, with0 adjacent identical frames. This is a media check, not evidence that all acting is convincing.
- All480 decoded V10 frames at12–28s have identical MD5 hashes to the baseline. Original encoded video through47s and from81.5s is copied. Only the47–81.5s picture section is encoded again, incorporating the new actions and original closing/phone sections.
- Actual full-speed Chromium playback reached86s in86.112s wall time:2580 total frames,0 display drops,0 corrupted frames. The replacement interval49.2–69.4s played at0.5× in40.709s, also0 drops/corruption. Presented-frame evidence is retained; contact sheets were not the only review.
- Actual encoded audio measured−16.03LUFS integrated,−3.20dBTP,7.40LU loudness range. These are the meter's INPUT values for the actual file, not hypothetical output normalization values. Critical listening remains unverified.
- All7150 protected earlier production files were hash-checked:0 changed,0 missing. Previous master/proof versions and V10 are preserved.

## What changed

The latest full real-motion master supplies the18-scene/86s story. Its driving/chase is kept because the new driving test's art is weaker. NativeB occupies49.2–57s, preserving the original exit before it. NativeC occupies61.4–69.4s. Original door-closing/locking action connects the two. The call, million-dollar offer, threat and A/B ending remain. The inserted native scenes retain their exact animation timing; they are not speed-compressed into shorter slots.

The soundtrack is rebuilt from existing licensed narration/caller stems, original effects and continuous score. New native foot/key/door/fabric cues replace the relevant original effects. The home phrase finishes intact after the picture cut. A checked-again phrase that crossed the stairs boundary is removed completely; the redundant proof "Inside" line is omitted in favor of the original "Inside. I locked it." sentence. New source-script captions follow measured WAV timings. Effects beds have25ms edge blends, and final audio has short beginning/end fades.

## Sources and limits

EDIT_DECISION_LIST.json and STORYBOARD_18_SCENES.json describe every interval. The complete edit inputs are copied and hashed in reports/SOURCE_INPUTS.json. Python/FFmpeg assembly scripts, caption ASS/SRT, contact/narration timing, native Blender files and rig/environment source are provided. No paid service or new model download was used. Whisper inference and word-level alignment are not claimed.

This is a complete best-achievable hybrid film, not a professional-quality certification. Visible model/lighting differences, stiff performances, simplified cloth and imperfect spatial continuity remain. See ARTISTIC_LIMITATIONS.md. The user explicitly authorized this complete export despite those limitations; the earlier proof quality gate is not used to block delivery.

## Reproducibility

A fresh source-only rebuild using the supplied inputs completed in a new directory and produced a byte-identical complete MP4 with the same SHA256. Its frame/decode/V10 checks also passed. The initial missing progress-log initialization was fixed before the successful fresh rebuild. See reports/SOURCE_REBUILD_VERIFICATION.json.
