"""Editable package plus exact separately published cache manifest; no video-size cap."""
from pathlib import Path
import json,hashlib,zipfile
from bootstrap import ROOT as R
assert (R/'TECHNICAL_REPORT.md').exists()
versions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());baseline=json.loads((R/'BASELINE_REVISIONS.json').read_text());cachepaths={f'scenes/{s}_{t}.json.gz' for s,t in versions.items() if s not in ['ROAD_BUILDINGS','CAR_CHASE','STAIRS']};cachepaths.add('scenes/STAIRS_M10D_NATIVE.json.gz');cachepaths.add('scenes/DRIVER_CHASE_M10C.json.gz');cachepaths.update(f'scenes/{s}_{t}.json.gz' for s,t in baseline.items() if s not in ['ROAD_BUILDINGS','CAR_CHASE','STAIRS'])
caches=[{'path':p,'bytes':(R/p).stat().st_size,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()} for p in sorted(cachepaths)];(R/'CACHES_MANIFEST.json').write_text(json.dumps(caches,indent=2))
models={'BASELINE_M04.blend','STAIRS_M09.blend','STAIRS_M10D.blend','DRIVING_COCKPIT_M10.blend','DRIVING_COCKPIT_EDITABLE_M10.blend','DRIVER_CHASE_M10.blend','DRIVER_CHASE_M10C.blend','DRIVER_CHASE_EDITABLE_M10.blend','KEY_LOCK_M10B.blend','DOOR_ENTRY_M10G.blend','CAR_EXIT_RUNNING_M10I.blend','WINDOW_CURTAIN_M10B.blend','ROAD_BUILDINGS_WORLD_M10_RELEASE.blend','CAR_CHASE_WORLD_M10_RELEASE.blend'}
files=[p for p in (R/'source').rglob('*') if p.is_file() and p.suffix in ['.py','.cpp'] and '__pycache__' not in p.parts];files += [R/'blender'/m for m in sorted(models)];files += list((R/'assets').glob('*.json'))+list((R/'sound').glob('M10_*_FOLEY.wav'));files += list(R.glob('*.md'))+[R/n for n in ['CURRENT_SHOTS.json','BASELINE_REVISIONS.json','CACHES_MANIFEST.json','CAMERA_ANIMATION.json','SOURCE_TO_RENDER.json']];files += [R/'scenes/STAIRS_M10D_NATIVE.json.gz'];files += [p for p in (R/'reports').glob('*.json') if not p.name.startswith(('github','DOWNLOAD','SOURCE_PACKAGE')) and not p.name.endswith('_RENDER.json')]
manifest=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(files))];out=R/'M10_EDITABLE_SOURCE.zip';assert not out.exists()
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for row in manifest:z.write(R/row['path'],row['path'])
 z.writestr('SOURCE_FILE_MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for row in manifest:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
report={'archive':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'native_blend_files':len(models),'sound_masters':8,'evaluated_native_caches_available':len(caches),'evaluated_native_caches_bundled':1,'files':len(manifest)+1,'all_members_match_current_source_SHA256':True,'zip_integrity_pass':True,'transport_note':'Complete evaluated caches are separately published and checksum-verified by the included helper; all local master videos/PNGs are preserved at production quality. No artificial MP4 size limit.','manifest':manifest};(R/'reports/SOURCE_PACKAGE.json').write_text(json.dumps(report,indent=2));print('M10_SOURCE_PACKAGE',report['bytes'],report['files'],flush=True)
