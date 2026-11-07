from pathlib import Path
import json,zipfile,hashlib
from bootstrap import ROOT as R
assert (R/'TECHNICAL_REPORT.md').exists()
models={'BASELINE_M04.blend','STAIRS_M08.blend','STAIRS_M09.blend','DRIVING_COCKPIT_M09D.blend','DRIVER_CHASE_M09D.blend','DRIVER_CHASE_M09L.blend','KEY_LOCK_M09D.blend','KEY_LOCK_M09E.blend','KEY_LOCK_EDITABLE_FINAL_M09_R02.blend','DOOR_ENTRY_M09H.blend','WINDOW_CURTAIN_M09G.blend','CAR_EXIT_RUNNING_M09D.blend','CAR_EXIT_RUNNING_M09K.blend','ROAD_BUILDINGS_WORLD_M09_RELEASE.blend','CAR_CHASE_WORLD_M09_RELEASE.blend'}
scenes={'STAIRS_M09_NATIVE.json.gz','DRIVING_COCKPIT_M09D.json.gz','DRIVER_CHASE_M09D.json.gz','DRIVER_CHASE_M09L.json.gz','KEY_LOCK_M09D.json.gz','KEY_LOCK_M09E.json.gz','DOOR_ENTRY_M09H.json.gz','WINDOW_CURTAIN_M09G.json.gz','CAR_EXIT_RUNNING_M09D.json.gz','CAR_EXIT_RUNNING_M09K.json.gz'}
files=[p for p in (R/'source').rglob('*') if p.is_file() and p.suffix in ['.py','.cpp'] and '__pycache__' not in p.parts]
files += [R/'blender'/n for n in sorted(models)]+[R/'scenes'/'STAIRS_M09_NATIVE.json.gz']+list((R/'assets').glob('*.json'))
files += list(R.glob('*.md'))+[R/'CURRENT_SHOTS.json',R/'CACHES_MANIFEST.json']
files += [p for p in (R/'reports').glob('*.json') if not p.name.startswith(('github-','DOWNLOAD','SOURCE_PACKAGE','PUBLICATION_REJECTED')) and not p.name.endswith('_RENDER.json')]
assert all(p.exists() for p in files)
manifest=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(files))]
out=R/'M09_EDITABLE_SOURCE.zip';assert not out.exists()
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for row in manifest:z.write(R/row['path'],row['path'])
 z.writestr('SOURCE_FILE_MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for row in manifest:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
assert out.stat().st_size<95*1024*1024
report={'archive':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'native_blend_files':len(models),'evaluated_native_caches_available_separately':len(scenes),'evaluated_native_caches_bundled':1,'files':len(manifest)+1,'all_members_match_current_source_SHA256':True,'zip_integrity_pass':True,'manifest':manifest}
(R/'reports/SOURCE_PACKAGE.json').write_text(json.dumps(report,indent=2));print('SOURCE_PACKAGE',report['bytes'],report['files'],flush=True)
