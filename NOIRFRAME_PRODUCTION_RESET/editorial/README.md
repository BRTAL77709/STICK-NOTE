# Remotion review edit

This composition uses the new native Blender MP4s, not pre-evaluated SVG strings or the rejected film. The three source shots remain individually downloadable at1080×1920. The optional continuous review reel is rendered at540×960 to avoid needless duplication of HD encodes; the composition itself is1080×1920/30FPS,624frames.

Captions use the source narration and measured generated-WAV timing. They are sentence captions, not ASR or word-alignment results. Whisper inference did not run because its checkpoint download was proxy-blocked. No forced tools or fake transcription.

`node render.cjs` uses the existing local Remotion4.0.419 install. Install matching @remotion/bundler, @remotion/renderer, remotion4.0.419 and React18 if moving the source to another machine. Place the three delivered MP4s as public/shot-A.mp4, shot-B.mp4 and shot-C.mp4. Local public symlinks and copied render-assets are runtime-only and excluded from publication. The bundler skipped symlinked files in the first attempt; the successful renderer uses regular copied media in render-assets.
