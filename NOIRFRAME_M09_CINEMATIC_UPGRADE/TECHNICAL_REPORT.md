# M09 technical validation report

Eight separate scenes, 78.3 seconds of scene exports in total, 2349 decoded video frames. This is not an assembled film. All final files are 1080×1920, 30 FPS,H.264/yuv420p with AAC Foley. All 8 were fully decoded with no errors or detected black intervals. Browser playback reached the end at normal and half speed without corrupted frames. Resource-related displayed-frame drops and wall-clock timing are retained honestly in the playback JSON; they are not omitted or presented as file corruption.

## Measured native/contact results

Units are metres unless stated otherwise. Stairs were reopened and evaluated601 times at 120 Hz. Maximum stance drift: 0.360045mm; foot-to-tread distance: 0.359281mm; limb length variation: 0.000427mm; connected bone gap: 0.000338mm. Tolerances:1mm stance/contact,0.1mm lengths/connections. The existing world ankle targets, poles and native no-stretch two-bone leg IK are retained. Stair arms use actual native FK controls.

Other six native caches were checked at 30 Hz, with native 60 Hz dense data supplied. Maximum wrist IK error across those caches: 0.083250mm; maximum limb-length variation: 0.002394mm. All 6 pass their declared tolerances. The separate reports include actual foot drift, floor distance, root displacement/acceleration and connected joint gaps. Native arm/digit IK is implemented in bake_native.py; no full-body force simulation is claimed.

Key lock-axis lateral error: 0.000000mm. The blade is 100 mm long; contact fingers and hand follow its resized bow, and the 9-second monotone clock exposes insertion/rotation/withdrawal. Door body/jamb penetration is 0 mm at sampled vertices after restoring the collision-safe elbow. Curtain wrist/grip frame error: 0.082123mm. Curtain arc-length error and native prop parity are in separate scoped reports.

Vehicles integrate at 120 Hz. Minimum conservative bumper clearance: 0.738969m. Maximum speed: 10.066250m/s. Heading/velocity and wheel-distance residuals, road margin and braking channels are measured in VEHICLE_WORLD_VALIDATION.json. House17 is locked to its original world transform; the new parked position differs from the approved original by less than 0.03 mm. This is a bicycle/spring model, not tyre-friction physics.

The repaired chase exterior camera stays at least 2.504496m outside the conservative vehicle bounds. The repaired exit camera remains at least 750 mm street-side of the facade. Exit native non-head geometry parity is exact across 180,144 vertices; only camera/head presentation changed in that correction.

## Rendered inspection and corrections

Actual previews played at normal and half speed. Inspected encoded-frame contact sheets and consecutive playback capture sheets are included. Rejected failures were repaired: a 64.98 mm sleeve/door intersection, early bedroom framing that excluded the approaching witness, an exit camera behind the facade, and an obstructed chase reveal. See SCENE_DEFECT_REPORT.md and the archived rejection reports. The failed sparse running solver was rejected; the successful existing bounded solve remains selected.

Sound is locally synthesized from integrated speed and saved contact/event clocks; staircase landings and curtain edge velocity drive the relevant cues. No paid APIs or externally licensed audio were used. Audio is sample-clock aligned; human artistic/audio approval remains outstanding.

## Editable source and preservation

The final body pixels use actual Blender-evaluated mesh geometry. Supplied .blend files retain native rigs and prop/world mirrors. Python/C++ supplies the complete illustrated world, depth rendering, camera staging and face artwork. Blender-only GUI rendering does not reproduce all final pixels; see REBUILD.md. The source package includes scripts, native files, selected evaluated caches and reports.

All 426 protected M08 files remain byte-identical. V10 was not edited; no full film was rendered or assembled. Existing remote Git entries are preserved and checked during publication.

## Artistic status

USER REVIEW REQUIRED. Engineering passes do not certify cinematic acting. Simplified/angular geometry, restrained acting, authored cloth and incomplete force/collision simulation remain. See KNOWN_LIMITATIONS.md and ARTISTIC_REPORT.md. No 10/10 or user approval is claimed.

## Download packaging

The70MB all-cache ZIP exceeded the GitHub blob API input limit (HTTP422). Delivery uses a smaller editable ZIP plus separately published native caches with a checksum-verified helper. All15 editable Blender files and scripts remain included. MP4 files were not regenerated or altered for this transport fix.
