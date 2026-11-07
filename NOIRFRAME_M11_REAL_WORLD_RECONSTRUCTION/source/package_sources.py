from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];versions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());models={'BASELINE_M04.blend','STAIRS_M05_INHERITED.blend','KEY_LOCK_PRESENTATION_R15.blend','DOOR_ENTRY_PRESENTATION_R23.blend','CAR_CHASE_WORLD_R09.blend','ROAD_BUILDINGS_WORLD_R09.blend'};models.update(f'{s}_{t}.blend' for s,t in versions.items() if s not in ['STAIRS','ROAD_BUILDINGS','CAR_CHASE']);files=[]
for p in R.rglob('*'):
 if not p.is_file() or p.is_symlink():continue
 rel=p.relative_to(R)
 if (rel.parts[0]=='source' and p.suffix in ['.py','.cpp'] and '__pycache__' not in rel.parts) or (rel.parts[0]=='blender' and p.name in models) or rel.parts[0]=='assets' or (len(rel.parts)==1 and (p.suffix=='.md' or p.name=='CURRENT_SHOTS.json')) or (rel.parts[0]=='reports' and (p.name in {'SHOT_REVISIONS.json','QA_SUMMARY.json','MEDIA_VALIDATION.json','NATIVE_REOPEN_VERIFICATION.json','NATIVE_PROP_PARITY.json','PRESERVATION_AFTER.json','VEHICLE_WORLD_VALIDATION.json','SCENE_REGISTRATION.json','DOOR_BODY_COLLISION_CHECK.json','EXIT_TERRAIN_REPAIR.json','PROP_INTERACTION_VALIDATION.json','STAIRS_M05_NATIVE_RECHECK.json','BASELINE_NATIVE_RECHECK.json'} or p.name.startswith('M07_FINAL_') and p.name.endswith('final-playback.json'))):files.append(p)
files.append(R/'scenes/STAIRS_INHERITED.json.gz')
out=R/'M07_EDITABLE_SOURCE.zip';assert not out.exists();manifest=[]
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):
  rel=str(p.relative_to(R));z.write(p,R.name+'/'+rel);manifest.append({'path':rel,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 z.writestr(R.name+'/SOURCE_PACKAGE_MANIFEST.json',json.dumps(manifest,indent=2))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
(R/'reports/SOURCE_PACKAGE.json').write_text(json.dumps({'path':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'members':len(manifest),'zip_test':'PASS','native_models':sorted(models)},indent=2));print('SOURCE_PACKAGE',out.stat().st_size,len(manifest))
