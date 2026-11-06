from pathlib import Path
import json,zipfile,hashlib
from bootstrap import ROOT as R
v=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());models={'BASELINE_M04.blend','STAIRS_M05_BASE.blend','STAIRS_M08.blend','KEY_LOCK_EDITABLE_FINAL.blend','DOOR_ENTRY_EDITABLE_FINAL.blend','CAR_CHASE_WORLD_M08_RELEASE.blend','ROAD_BUILDINGS_WORLD_M08_RELEASE.blend'};models.update(f'{s}_{t}.blend' for s,t in v.items() if s not in ['ROAD_BUILDINGS','CAR_CHASE','STAIRS']);files=[]
for p in (R/'source').rglob('*'):
 if p.is_file() and p.suffix in ['.py','.cpp'] and '__pycache__' not in p.parts:files.append(p)
files.extend(p for p in (R/'blender').iterdir() if p.name in models and p.is_file() and not p.is_symlink());files.extend(p for p in (R/'assets').iterdir() if p.is_file());files.extend(p for p in R.iterdir() if p.is_file() and (p.suffix=='.md' or p.name=='CURRENT_SHOTS.json'));files.append(R/'scenes/STAIRS_M08_NATIVE.json.gz')
for p in (R/'reports').iterdir():
 if p.name in ['SHOT_REVISIONS.json','QA_SUMMARY.json','MEDIA_VALIDATION.json','NATIVE_REOPEN_VERIFICATION.json','NATIVE_PROP_PARITY.json','NATIVE_POV_PRESENTATION.json','PROP_INTERACTION_VALIDATION.json','DOOR_BODY_COLLISION_CHECK.json','STAIRS_M08_NATIVE_RECHECK.json','CURTAIN_SUPPORT.json','CAMERA_SPACE_VALIDATION.json','GLYPH_ROI_VALIDATION.json','VEHICLE_WORLD_VALIDATION.json','PRESERVATION_AFTER.json','M07_M08_NATIVE_CHANGES.json','RUN_MOMENTUM_COMPARISON.json'] or p.name.startswith('M08_DELIVERY_') and p.name.endswith('final-playback.json'):files.append(p)
out=Path('/tmp/NOIRFRAME_M08_DATA/M08_EDITABLE_SOURCE.zip');assert not out.exists();rows=[]
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(set(files)):
  rel=str(p.relative_to(R));z.write(p,R.name+'/'+rel);rows.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
 z.writestr(R.name+'/SOURCE_PACKAGE_MANIFEST.json',json.dumps(rows,indent=2))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
link=R/out.name;assert not link.exists();link.symlink_to(out)
(R/'reports/SOURCE_PACKAGE.json').write_text(json.dumps({'path':link.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'files':len(rows),'zip_integrity':'PASS'},indent=2));print('SOURCE_PACKAGE_READY',out.stat().st_size,len(rows))
