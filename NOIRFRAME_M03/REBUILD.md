# Rebuild without overwriting

Free tools: Python 3, NumPy, SciPy, Pillow, system librsvg/Cairo/GObject, FFmpeg/libx264. Playwright/Chromium are used only for playback verification. No remote generation, paid API or new dependency download is needed.

Extract `M03_EDITABLE_SOURCE_C03.zip` into a new directory, create `previews`, `diagnostics`, `comparisons`, `reports`, `reviews` and run:

```sh
python source/render.py --test STAIRS --width 1080 --tag C03
python source/render.py --test KEY_DOOR --width 1080 --tag C03
python source/render.py --test STEERING --width 1080 --tag C02
python source/render.py --test CHASE --width 1080 --tag C02
python source/render.py --test CURTAIN --width 1080 --tag C02
python source/qa.py --tag FINAL --width 1080
python source/repair_diagnostic_projection.py
```

Use these tags only in a NEW extracted directory; never run this over the production directory. The renderer refuses existing output MP4 paths. The projection-repair command produces the final steering/chase diagnostic overlays from these new clean frames and updates CURRENT_SHOTS. Every command creates separate clean and diagnostic H.264 videos, compressed exact-state JSON, hashes and contact strips. It streams raw frames directly into FFmpeg and does not reuse MP4 footage. Rendering native 1080 is CPU-intensive. Comparison assembly additionally requires the read-only rejected M01/V12 files beside this production directory. Corrected rendering needs only the included source.
