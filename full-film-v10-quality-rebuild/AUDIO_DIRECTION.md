# Audio direction and limits

`engine/audio/mix_rebuild.py` retains 30 existing Kokoro phrase performances (narrator bm_daniel; caller am_echo). It does not generate a replacement actor performance. No paid API, new voice download, or reference soundtrack is used.

`narration-timing.json` records actual phrase durations; captions are phrase-aligned, not word-aligned. The black-car line is moved to its actual upstairs reveal. `CONTACT_SOUND_CUES.json` contains 96 source-derived cues. Foot strikes are quantized to the first visible 30 FPS contact frame. Wet pavement and indoor wood have distinct synthesized foley. Keys, lever, hinge, latch, lock, curtain, vibration and pickup follow the action controllers.

Engine synthesis uses actual vehicle speed/RPM. Rain changes between exterior, cabin and interior, and attenuates as the door closes. The procedural score ducks during speech and leaves two suspense gaps. Current lossless stems and mix are under the directory named by `AUDIO_OUTPUT.json`; older mixes are preserved locally as drafts.

The target mix is −16 LUFS with −2 dBTP headroom; the validation report measures the encoded film rather than assuming encoder settings guarantee its loudness. Signal validation and browser playback do not certify natural speech, convincing acting, or professional sound. Listening remains unverified. An unavailable transcription model was not repeatedly downloaded.
