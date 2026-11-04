# Technical validation — review candidate

Technical checks support evidence; they do not confer user artistic approval. The previous rejected production is protected by a 1039-file hash manifest. Approved V10 source and clip bytes remain unchanged.

## Five physical proofs

Current MP4s are selected by `proofs/A–E/final.json`, not by guessed draft filenames. `reports/proof-integration-gate.json` compares each current source SVG stream to the reviewed preview and HD clip metadata, requires full/half-speed playback and records source-file SHA256. `physical-proof-validation.json` checks actual contact/trajectory/bone states at 120 Hz.

A includes foot approach and acquisition, a fixed heel, 24° pedal rotation and articulated hip/knee/ankle plus body response. B travels 18 m, accelerates smoothly from 2 to 7 m/s, turns about 15°, rotates tires by distance/radius, and settles into cruise without HUDs. C is extended to nine seconds for readable key/door/entry action and a completion hold; wall/leaf depth masks entry. D completes three metric 3D stairs with landing-before-pelvis transfer, ankle/toe-off motion and swept shoe clearance (2 mm tolerance). E starts with a closed curtain and maintains hand/edge ownership during the pull, then releases into fold/head/body response. Each proof includes source references, CSV/JSON trajectory and joint transforms, contact events, contact sheets and actual normal/half-speed presentation evidence.

## Master integration

`master-motion-validation.json` checks 10321 samples at 120 Hz: wheel odometry, velocity/position consistency, driver bones, run feasibility, registered curtain approach and phone rigs. Pedal contact is at global28.75 s; pressure/acceleration start together at28.9. The route from38 s onward is unchanged. Three upper stairs are visible; the lower flight is explicitly elided by a cut. This is not a claim that all fifteen risers are shown.

`city-occlusion-regression.json` and `reviews/CITY_DEPTH_BEFORE_AFTER.jpg` document a real painter-order bug: road-centre depth4.95 m incorrectly put a far facade over the car at6.5 m; actual facade centre depth is16.2 m. Buildings, lamps, utility poles and signs now join traffic using their actual side-aware world positions. Whole-object ordering remains a 2.5D approximation, not a full polygon depth buffer.

The repair register links current independent preview/HD normal and slow playback evidence. Dropped presentation frames are retained in reports. All encoded inputs receive complete decode checks. `source-validation.json` verifies all2580 current SVG frames, 18 HD inputs, current review paths, preserved V10480 frames/bytes, protected baseline hashes, voice/cue timing and stamped composition inputs.

## Compositing and audio

HyperFrames only assembles independently animated clips, captions, clock/call/offer/choice. Vehicle dashboards are removed. A broad `data-layout-ignore` on subject videos was replaced with narrow overlap/caption allowances, so their pixels/time are included in motion inspection. No fake `data-hold` or decorative movement is used to silence liveness warnings. `checker-annotation-diagnosis.json` records the implementation evidence. Actual encoded subject crops are additionally compared to exact raw frame indices by `verify_composited_subjects.py` after export.

The current mix is selected by AUDIO_OUTPUT.json. Eighty-two source-derived cues track foot plants, key/handle/lock/hinge, folds and phone acquisition. Device vibration modulation uses the exact retimed reference clock. Thirty existing stock voice performances are retained; phrase lengths stay unchanged and captions use measured boundaries. Audio metadata and playback do not certify natural speech or professional sound; listening remains unverified.

Final encoded-film validation and verified download records are appended only after those checks run.

## Encoded review-film checks

The new MP4 passes complete FFmpeg decode, 1080×1920 H.264 at30 FPS,2580 frames/86.000 seconds, AAC stereo48 kHz. The measured encoded mix is−16.03 LUFS integrated and−3.64 dBTP. Two identical adjacent-frame pairs occur; pixel liveness is not used as proof of acting.

All57 selected exact-frame subject crops match the current raw clips. Maximum mean absolute error is2.454/255. The frozen-control criterion was corrected after one low-motion door sample failed: neighboring frames confirmed the exact expected source frame75 matched best. The revised criterion accounts for additive re-encoding noise and requires the correct frame to beat the frozen control by more than half the actual source change. The video did not change. See fidelity-checker-correction.json and encoded-subject-fidelity.json for the measurements.

Full normal-speed browser playback reached86 s/ended=true with zero corrupted frames. The presentation reported5 dropped frames out of2580 while validation work ran concurrently; the independent full FFmpeg decode has no error. Full half-speed review is recorded separately. This is presentation evidence and frame inspection, not a claim of human listening or artistic approval.

Full half-speed playback also ended normally at86 s, rate0.5, wall time172.142 s, with0 dropped presentation frames and0 corrupted frames. Both complete presentation sheets were inspected. Artistic approval and voice listening remain pending.
