# Audio assets and licenses

All narration/caller text is original for this film. Speech was synthesized locally with the existing FFmpeg Flite filter: RMS narrator, AWB caller with telephone-band filtering. No voice API, key, model download, impersonated actor or external recording was used. These are synthetic voices and sound mechanical; no claim of human performance is made.

The supplied Flite copyright/license file reproduces the notices installed in this environment. Core/toolkit terms permit use/distribution under the documented conditions. No Flite binary or voice database is bundled. DejaVu/FFmpeg and other runtime binaries are also not bundled.

Rain, wind, tonal suspense score, engines, tire noise, footsteps, keys, locks, trunk and phone accents are original deterministic procedural synthesis from src/production_audio.py. No stock sample or copyrighted music is used.

Delivered: lossless individual voice phrases in voices/*.flac; original narration_stem.flac; mastered mix in master_mix.m4a; compact original music/FX stem in sound_design_stem.m4a. The full local WAV masters and lossless FX stem remain in the workspace and can be regenerated from source. The public delivery omits duplicate raw WAVs and the larger FX FLAC to keep the package practical. voice-assets.json maps each delivered phrase to its original timing/source filename.

The film's mastered mix targets−16 LUFS /−1.5 dBTP; measured results are in audio-master-verification.json. The original stems are pre-master and intentionally retain their editable dynamics. Captions use actual generated phrase boundaries. Scene18 suppresses burned captions so the decision screen stays clear; the SRT still transcribes the final spoken question.
