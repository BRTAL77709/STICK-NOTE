# NOIRFRAME M07 — eight separate repair previews

Status: **ARTISTIC REVIEW REQUIRED** for every clip. No full-film render or user approval is implied. The strongest V10 trunk footage and earlier versions are preserved.

All clean previews are 1080×1920, 30fps, H.264 with locally synthesized AAC Foley. Open `CURRENT_SHOTS.json` for exact clean, diagnostic and comparison paths. Durations are natural interaction tests, not drop-in replacements for the existing 86-second edit.

| Clip | Seconds | Scope |
|---|---:|---|
| DRIVING_COCKPIT | 12 | Native seated actor, wheel grips, pedals, mirror, matched road/interior/exterior coverage |
| ROAD_BUILDINGS | 7 | Fixed road, intersections, varied facades, House17, stable projected landmarks |
| CAR_CHASE | 11 | Integrated two-car motion, changing gap, steering/wheel travel, interior reaction, arrival |
| CAR_EXIT_RUNNING | 10.8 | Stop, release, handle, hinge, legs out, weight transfer, run, entrance |
| KEY_LOCK | 7 | Pocket, grip, uninterrupted readable insertion/turn/withdrawal close-up |
| DOOR_ENTRY | 13 | Handle, hinge opening, threshold crossing, closing, interior thumbturn |
| STAIRS | 5 | Actual inherited M05 native mesh/IK performance and finished set; no new gait claim |
| WINDOW_CURTAIN | 10.5 | Bedroom threshold, approach, grip, fold pull, registered sedan reveal, recoil |

`ROOT_CAUSE_AUDIT.md` traces actual source failures. `REBUILD.md` explains the editable hybrid pipeline. `QA_REPORT.md`, `REMAINING_DEFECTS.md` and machine-readable `reports/` distinguish measured checks from unsolved artistic/physical limitations. `comparisons/` contains same-rate comparisons with prior footage. `contact_sheets/` includes ordered encoded diagnostic frames and playback-presented sheets.

The editable source ZIP includes the native armatures and final native scenes, Python controllers, C++ rasterizer source, shared world/vehicle assets and the retained staircase cache. Character surfaces in the cinematic output come from actual evaluated Blender geometry. The environment, prop and illustrated face renderer remains script-driven; see the explicit editing boundaries in REBUILD.

Only the user may grant USER APPROVED. These clips are review candidates, not final-production approval.
