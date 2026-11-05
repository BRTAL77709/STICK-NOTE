# Rebuild

Free dependencies used: Python 3, NumPy, Pillow, CairoSVG, Cairo/librsvg through the supplied raster helper, FFmpeg/libx264. Chromium and Python Playwright are needed only for playback verification. No paid calls.

Extract the source ZIP into a new directory; create `previews`, `reviews`, `reports`, `comparisons`. Run each command once (the renderer refuses to overwrite):

```sh
python source/render_tests.py --test STAIR_CONTACT --width 1080 --tag REBUILD
python source/render_tests.py --test KEY_HANDLE --width 1080 --tag REBUILD
python source/render_tests.py --test STEERING_TURN --width 1080 --tag REBUILD
python source/validate.py --tag REBUILD --width 1080
```

The three corrected tests need only the included source. The comparison exporter additionally expects the read-only V12 originals beside this folder and CURRENT_SHOTS pointing at final exports. Output is silent 30 fps H.264, 1080 × 1920. Every render stores exact per-frame state and producer hashes. Do not copy results over previous versions.
