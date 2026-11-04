# Tool installation and status

| Tool | Exact observed version | Status and actual verification |
|---|---|---|
| Node / npm |24.19.0 /11.9.0|CLI versions executed. Meets HyperFrames Node22+ requirement.|
| Python |3.12.14|New isolated venv; CLI/import checks executed.|
| Remotion / renderer / bundler |4.0.419|Existing local packages reused; React composition rendered210 genuine vector frames.|
| React |18.3.1|Pinned installed runtime used by Remotion.|
| HyperFrames |0.8.226|Existing local CLI reused; check passed; editable previewHTTP200; transparent ProRes HUD rendered120 frames.|
| FFmpeg / FFprobe |7.1.5-0+deb13u1|Installed GPL build with libx264/libass; alpha assembly, speech mix, captions, H.264/AAC export and full decode exercised.|
| OpenAI Whisper |20250625|New venv install/import/model-list/CLI verified. Inference blocked by missing checkpoint; official and HF route return proxyHTTP403. Not a completed ASR integration.|
| yt-dlp |2026.10.26|New venv install/import/version verified. Authorized-download workflow supplied; no unapproved download executed.|
| CPU PyTorch |2.15.0+cpu|Existing CPU runtime reused through explicit venv .pth; no GPU service.|
| Git |2.52.0|CLI version verified; no clone.|

Full exact paths/commands: reports/installed-versions.json. Python direct versions: requirements-direct.txt. npm reproducibility: remotion/package-lock.json. No global tool installation or previous project replacement. Existing Remotion/HyperFrames were reused, not reinstalled under a false success claim.

## Installation fixes and blockers

The initial Python resolver selected CUDA packages unnecessarily; it was stopped and replaced with direct missing-package installation using existing CPU Torch. Verified imports use CPU2.15.0+cpu. Remotion initially rejected an underscore composition ID; the corrected hyphen ID renders successfully. FFmpeg's font scan initially included the compressed geometry bundle; a dedicated font directory fixes that, and the earlier draft is preserved separately. These are resolved local setup errors, not simulated tool success.

Whisper official tiny.en checkpoint failed once with `URLError: <urlopen error Tunnel connection failed: 403 Forbidden>`. The HF openai/whisper-tiny.en PyTorch route also returned CONNECT403. No identical repeated download, fake model, hosted ASR or paid substitute was used. `reports/whisper-model.json`, whisper-weight-network-probe.txt and whisper-transcription.json preserve the exact status. The transcription script exits3 until verified local weights exist. Therefore no Whisper-generated subtitle sample is delivered; script-reference.srt is explicitly a source-script/measured-duration fallback.

## License review / $0 scope

- Remotion4.0.419 terms permit free evaluation, individual use, for-profit organizations with up to3 employees and non-profit use. Larger for-profit organizations require a company license. This local integration is an evaluation; NOIRFRAME's company size is not asserted. Confirm eligibility before future commercial production. Exact pinned official license: licenses/REMOTION.md.
- HyperFrames: Apache2.0. The local CLI/renderer is used; optional hosted/model features are not invoked.
- Whisper code/weights: MIT; yt-dlp source: Unlicense. Their official notices are supplied. Existing Python/Torch binary runtimes are not redistributed.
- Installed FFmpeg reports GPLv2-or-later terms; its build/license output is supplied. No FFmpeg binary is redistributed. The requested H.264/AAC output uses the existing build.
- GSAP3.15.0 retains its embedded standard-license notice; the font is the same approved DejaVu-derived font from the project. Existing notices are copied with the assets.
- All reference footage remains for analysis; none is reused in the demo. No cloud render, paid API, paid service or commercial music purchase occurred. Additional service spend: $0.

The review harness was corrected to use loopback HTTP after managed Chromium blocked file://, and to avoid returning GSAP's paused thenable timeline to Playwright. Exact HUD frame checks then exposed a fractional-time rounding edge case; the actual HUD adapter was corrected, rerendered and validated. Earlier draft videos/layers remain local; they are not the final deliverable.
