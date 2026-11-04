# Setup and exact runtime reuse

Verified here: Node24.19.0/npm11.9.0; Python3.12.14; FFmpeg/FFprobe7.1.5; Chromium154; Remotion4.0.419; React18.3.1; HyperFrames0.8.226; openai-whisper20250625; yt-dlp2026.10.26; CPU Torch2.15.0+cpu. Full command output and package paths: reports/installed-versions.json.

The existing Remotion npm tree and HyperFrames CLI were reused, not claimed as newly installed. A new Python venv installs the missing Whisper/yt-dlp packages and their direct helpers. Its `existing-cpu-runtime.pth` reuses the installed CPU Torch/NumPy. Initial dependency resolution selected unnecessary CUDA packages; it was interrupted, and the verified final environment uses CPU Torch. Existing dependency installations were not overwritten.

On a fresh machine, use Node22+, FFmpeg/FFprobe with libx264/libass/ProRes support, Chromium, and Python3.12:

```sh
cd remotion
npm ci --ignore-scripts
cd ..
# Install the pinned local CLI into a separate runtime folder:
npm install --prefix runtime --save-exact hyperframes@0.8.226
export HYPERFRAMES_CLI="$PWD/runtime/node_modules/hyperframes/bin/hyperframes.mjs"
python -m venv .venv
# Obtain CPU Torch from its official CPU wheel index, avoiding default CUDA downloads:
.venv/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r requirements-direct.txt numpy Pillow playwright
# Set HYPERFRAMES_BROWSER_PATH and the browserExecutable in render-remotion.cjs to local Chromium.
```

The above fresh-install recipe is documented, not claimed to have been re-executed on a second machine. The observed runtime versions are separately pinned in requirements-runtime-observed.txt. No model weights or binary runtimes are redistributed. `scripts/bootstrap.py` is a one-time workspace migration helper; do not rerun it over customized rigs. Fonts/GSAP and source are already supplied.

## Whisper status

Official checkpoint route was attempted once:
https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt

Result: URLError, `Tunnel connection failed: 403 Forbidden`. The Hugging Face openai/whisper-tiny.en PyTorch route also returned CONNECT403. Repeated identical downloads were not attempted. Package import, model-list access and CLI help work; inference does not. `scripts/transcribe.py` exits3 with an explicit report until a real checkpoint is present. `fetch_whisper_model.py` is an explicit, single-attempt download with official SHA256 validation; it is not run by the normal render pipeline. Do not bypass destination policy.

When network policy permits the official model host, run the fetch helper once, then transcribe the actual WAV. `--model PATH` accepts a local OpenAI-format checkpoint; retain its provenance/hash. `--words` asks Whisper for estimated word timings, which still need inspection. A forced-aligner such as WhisperX would be a separate dependency/model workflow; none is installed or claimed here.

## Authorized references

`reference_download.py --check` only reports the installed version. To fetch an explicitly authorized reference, supply `--url`, `--rights-note` and `--style-analysis-only`. It disables playlists/overwrites, stores a download archive and metadata, and uses local FFmpeg. Setup downloaded no video/music. Network access to a future media host must also be allowed; no access bypass is provided. No source footage or commercial music enters the demo.
