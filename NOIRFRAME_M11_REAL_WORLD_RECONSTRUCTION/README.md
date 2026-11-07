# NOIRFRAME M11 — persistent reconstruction

New reconstruction from verified M10 commit `651b19f30ac23278445a0b74da71fff5337e895e`. Lost original M11 files have **not** been recovered. This directory is a real persistent workspace directory, not a `/tmp` symlink.

Working branch: `noirframe/m11-safe-rebuild`.

## Checkpoint guarantees

- The real remote backup/restore drill passed before production was enabled.
- Source, configuration, native Blender files, validation reports, and receipts are committed at milestones.
- Each native .blend/cache pair is archived, committed as immutable chunks, downloaded, and SHA-256 checked before moving to the next native shot.
- Every 60 final lossless PNG frames form a resumable batch. Rendering waits for the verified remote backup before proceeding.
- Completed MP4s are backed up and downloaded for SHA-256 verification. Feasible-size videos also receive an ordinary direct `.mp4` GitHub file URL.
- No output is called verified or downloadable based only on an upload response.
- GitHub Release upload returned HTTP 401 Bad credentials. Release assets are **not** the active storage backend. The verified fallback is normal Git with content-addressed chunks; it does not re-encode or reduce file quality and requires no paid LFS service.
- Existing V10/M10 and earlier project entries remain unchanged in every checkpoint commit; local originals have a SHA-256 protection manifest.

## Cold restore

Obtain the desired receipt under `checkpoints/receipts/` from a pinned milestone commit. Run:

```bash
python source/restore_checkpoint.py --manifest-url '<receipt url>' --destination '/workspace/STICK-NOTE/M11_RESTORED_CHECKPOINT'
```

The restore helper downloads and verifies every chunk, checks the combined file SHA-256, verifies every archived file, and refuses to overwrite different existing files. To restore a video binary only, add `--no-extract`. For frame batches, restore only batches matching the same `PRODUCER.json` fingerprint and native revision.

The M10 dependency caches are independently recoverable from the pinned baseline using `source/fetch_native_caches.py --revision 651b19f30ac23278445a0b74da71fff5337e895e` and the checked manifest.

## Production status

Individual scenes only. No full-film assembly and no M12. Native geometry and contact/camera metrics require explicit scoped QA. Artistic approval remains with the user; an encoded MP4 alone is not a quality pass.
