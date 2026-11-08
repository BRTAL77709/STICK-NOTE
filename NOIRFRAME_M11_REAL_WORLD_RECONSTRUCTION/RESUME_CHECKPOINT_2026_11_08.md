# M11 resume checkpoint — 8 November 2026

This is a new reconstruction from M10 commit `651b19f30ac23278445a0b74da71fff5337e895e`; the missing original M11 runtime was not recovered. Dedicated branch: `noirframe/m11-safe-rebuild`. Persistent directory: `/workspace/STICK-NOTE/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION`. No full-film assembly.

## Completed downloads

At the last successful filesystem inspection, these six standalone finals had passed full-byte remote-download checks, complete FFmpeg decoding, and normal/half-speed Chromium playback. On 8 November the connected GitHub API confirmed that all six canonical Git objects remain committed. Artistic approval is pending.

- [M11_CAR_CHASE_FINAL.mp4](https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/renders/M11_CAR_CHASE_FINAL.mp4) — 4876486 bytes; Git blob 8a97ac28146463526fd883d4d81878a4a1b9125e.
- [M11_CAR_EXIT_RUNNING_FINAL.mp4](https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/renders/M11_CAR_EXIT_RUNNING_FINAL.mp4) — 4002294 bytes; Git blob 946f87ca63902cfa77213f12bb4473c2effe345d.
- [M11_DRIVING_COCKPIT_FINAL.mp4](https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/renders/M11_DRIVING_COCKPIT_FINAL.mp4) — 3148807 bytes; Git blob 24db9f6277d6feabf241d2ef4176af95c52ab632.
- [M11_KEY_LOCK_FINAL.mp4](https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/renders/M11_KEY_LOCK_FINAL.mp4) — 1846317 bytes; Git blob c8b65c8c7dbfcc5bf18974e9fb18fa7d0316dbe2.
- [M11_ROAD_BUILDINGS_FINAL.mp4](https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/renders/M11_ROAD_BUILDINGS_FINAL.mp4) — 3527670 bytes; Git blob 855f1e1a68dcb94d99d62af09affe782b0a878f4.
- [M11_STAIRS_FINAL.mp4](https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/renders/M11_STAIRS_FINAL.mp4) — 5154983 bytes; Git blob 8f1b5c37b06f8edab28e893a4ac3979fded5dd91.

## Exact interruption

The environment initially resumed successfully, then became unavailable. Exec failed with: `Failed to create unified exec process: exec-server transport disconnected; failed to resume exec-server session: recovery timed out after 45s`.

The attempted local cache-restore-index/source-package-readme command is NOT confirmed executed. No source ZIP or completed remaining exports is claimed.

Eight unfinished scenes: DOOR_ENTRY, WINDOW_CURTAIN, PHONE_CALL, UNKNOWN_CALLER, DISCOVERY, PANIC, ARRIVAL, FINAL_POLL.

Last inspected local PNG counts: DOOR_ENTRY 434/600; WINDOW_CURTAIN 300/465. The resumed renderer reused the saved PNGs rather than restarting their geometric rendering. Remote committed batches cover door frames 0–419 and curtain frames 0–299. The latest batch manifests and Git part identities were rechecked through the connector. A current full binary restore through that connector is unavailable: binary fetch returned a UnicodeDecodeError. Do not call this a new full restore pass.

## Checkpoint references

Last normal source-file milestone before interruption: `3e316d98da4b4365f4f048359b989117359fd22e`. Earlier successful source/native and first-frame cold-restore drills remain in the reports.

Newest source-archive object commit: `0ff6803377c2e5be768d211464f0b53d2ce96c07`. SHA-256 `3fd9951e69c3fd53502ebad610f93294d069ac722e48c7899abb98eadb0d9647`, 72,390,404 bytes. Its parts are committed, but the interrupted milestone's final download/restore verification and source-tree commit are NOT confirmed complete. Verify before claiming that milestone passed.

Source archive manifest:
https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/checkpoint_objects/3fd9951e69c3fd53502ebad610f93294d069ac722e48c7899abb98eadb0d9647/0acc788b724c79c84ca2/manifest.json

Latest partial batch manifests:
- M11_WINDOW_CURTAIN_M11R03_FINAL-00240-00299: https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/checkpoint_objects/0aac762dfb658f9d8c292a30d226ef631f5c3000145d148fa2487014ceca6a5e/98d8a83166b2922caf52/manifest.json
- M11_DOOR_ENTRY_M11R03_FINAL-00360-00419: https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/0ff6803377c2e5be768d211464f0b53d2ce96c07/NOIRFRAME_M11_REAL_WORLD_RECONSTRUCTION/checkpoint_objects/8fde93a3822a22e41ce58690531f98fb968d298f76e691f43a03547aa0ac133d/3785de314f4919099779/manifest.json

## Resume without repeating completed work

1. Restore execution access and inspect process status before launching duplicates. Recheck actual files and remote branch head.
2. Preserve all six complete canonical/versioned exports. Reuse PNGs only when PRODUCER.json fingerprints match selected native projects and pixel-producing source.
3. Staircase selection: R03 native motion with separate R04 camera renderer. Skip the obsolete R03 final framing; preserve its preview, diagnostic and native source.
4. Resume only the eight unfinished scenes. The batch_m11.job helper supports saved frames; use FINAL=True and filter completed shots. Check actual MP4s and receipts as well: DELIVERY_MANIFEST.json on Git can lag completed MP4 commits.
5. Resume source/validate_exports_m11.py --watch, source/publish_scenes_m11.py and source/review_final_scenes_m11.py only after checking for existing workers.
6. Finish the interrupted source checkpoint and verify remote restore. Keep the 60-frame verified-backup gate. Ordinary Git chunks are active because Release upload returned HTTP 401. Never keep sole production copies in /tmp.
7. Finish source-package/restore-index preparation, reports and review index. No artistic self-approval or full 86-second assembly.

Previous protection recheck: 11,871 original files and 68 original symlink targets unchanged. Remaining limitations and the 126.84 mm exit-to-key conform gap are documented in reports/RECONSTRUCTION_TECHNICAL_REPORT.md.
