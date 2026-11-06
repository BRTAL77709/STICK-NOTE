# M10 technical and production validation

Eight independent scene exports, 82.3s in total; 2469 fully decoded frames. All are 1080×1920,30FPS,H.264/yuv420p,AAC, with faststart verified from actual MP4 atom ordering. CRF18 encoding has no bitrate or arbitrary file-size target. Every main video differs from its actual M09 baseline hash.

Lossless native-resolution PNG masters are retained for every frame under frames/M10_<SCENE>_FINAL/: 161625142 bytes, 2469 frames. No low-resolution preview was upscaled. Fingerprints prevent stale-source frame reuse. After the exit correction, 168 frames had exact equivalent evaluated meshes/authoring states and critical source hashes; 156 changed frames were rendered anew. Original passes remain preserved.

## Actual measured checks

Stairs: 721 native reopen/evaluations at120Hz. Maximum stance drift 0.263183mm; foot/tread distance 0.263203mm; length variation 0.000439mm; connected bone gap 0.000322mm. Original1mm stance/contact and0.1mm length/joint tolerances retained. Retimed original keys pass after the resampled-key draft was rejected.

Six other native caches pass declared30Hz contact checks, with60Hz dense native evaluation data supplied. Maximum wrist target error 0.083196mm. Native no-stretch IK and actual bound skin supply the final body geometry. Stair upper-body FK is retained; no universal bone-mode switch or force-based muscle simulation is claimed.

Key: actual seated insertion depth 90.000mm; lock-axis lateral error 0.000000mm; hand/grip frame error 0.080490mm. Blade 100 mm, intended exposed shoulder10mm. Door/jamb sampled body penetration is 0 mm after the inside-elbow repair. Hallway root travel and four measured foot landings are recorded in MOTION_MEASUREMENTS.json.

Curtain: actual wrist/grip frame error 0.081325mm; horizontal material arc-length error 0.269735mm. Header/edge anchors are retained; deformation is authored, not full force/self-collision cloth physics.

Vehicle integration120Hz, conservative minimum bumper clearance 0.738969m; wheel-distance/heading residuals and road margins are in VEHICLE_WORLD_VALIDATION.json. Route and House17 registration remain shared. Existing valid bicycle/spring dynamics were preserved, not relabelled as new friction physics. The chase reaction edit now coincides with the actual glance and precedes the closer pursuer reveal.

Native cockpit hierarchy/axis/frame files preserve actual evaluated skin with zero measured geometry difference. CAR_ROOT groups are car-local, and integrated world motion is applied once by the renderer. Camera animation exports identify each local/world coordinate frame explicitly.

All main videos were fully decoded with no errors or detected black intervals. Normal- and half-speed Chromium playback reached each ending without corrupted frames. Actual displayed-frame drops under load are retained in playback reports, not omitted or confused with file corruption. Exact repeated-frame intervals are reported; deliberate holds do not establish artistic approval.

## Sound and inspection

Eight original local PCM WAV masters are retained; AAC finishing copies the encoded video stream. Footsteps derive from saved contacts, cloth sound from edge velocity, engine sound from integrated speed, with timed original suspense accents. No paid API, copyrighted sample library or new external asset was used. Human audio/artistic approval remains outstanding.

Actual encoded M09/M10 contact sheets and normal-speed side-by-side movies are included. Shorter baseline endings are explicitly held for comparison coverage; main films are unchanged. No full 86-second film is assembled.

## Preservation, source and limits

All 775 pre-edit M09 files remain byte-identical. V10 was not edited. Publication verifies every previous remote tree entry. SOURCE_TO_RENDER.json identifies actual models/caches/controllers; CAMERA_ANIMATION.json, native models, scripts and WAVs are supplied. Editable Blender files contain real rigs and mirrors, while the final look also uses Python/C++ world/prop/depth and vector-face composition. Native prop-only GUI edits need matching scripted definitions.

USER ARTISTIC REVIEW REQUIRED. Simplified/angular geometry, restrained acting, authored cloth and incomplete whole-house/force/continuous-collision certification remain. See KNOWN_LIMITATIONS.md. No 10/10 claim or automatic artistic approval.
