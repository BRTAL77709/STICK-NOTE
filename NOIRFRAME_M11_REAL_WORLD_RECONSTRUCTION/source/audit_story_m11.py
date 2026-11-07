from bootstrap import ROOT as R
from pathlib import Path
import json,hashlib,shutil,subprocess,importlib
old=R.parent/'NOIRFRAME_FULL_FILM_V1/STORYBOARD_18_SCENES.json';shutil.copy2(old,R/'configuration/STORYBOARD_18_SCENES_REFERENCE.json');rows=json.loads(old.read_text());mapping={1:'ROAD_BUILDINGS',2:'DRIVING_COCKPIT',3:'DISCOVERY',7:'PANIC',8:'CAR_CHASE',9:'CAR_CHASE',10:'ARRIVAL',11:'CAR_EXIT_RUNNING',12:'KEY_LOCK',13:'DOOR_ENTRY',14:'STAIRS',15:'WINDOW_CURTAIN',16:'PHONE_CALL',17:'UNKNOWN_CALLER',18:'FINAL_POLL'};out=[]
for row in rows:
 n=row['scene'];conflicts=[b for b in row['action_beats'] if b['start']<row['start'] or b['end']>row['end']];m=mapping.get(n);src=R.parent/'full-film-real-motion-rebuild'/row['physical_source'];out.append({'scene':n,'title':row['title'],'narrative_start':row['start'],'narrative_end':row['end'],'existing_source':str(src) if src.exists() else None,'M11_sequence':m,'protected_V10':n in [4,5,6],'timing_conflicts':conflicts,'status':'USER APPROVED — existing V10 protected per instruction' if m is None else 'ARTISTIC REVIEW REQUIRED','audit_scope':'Movement/contact/camera/geometry/sound reports supplied per standalone sequence; exact 86s edit/conform is deferred. New durations intentionally expand actions and some coverage overlaps world-clock ranges. No full-film assembly.'})
(R/'reports/STORYBOARD_AUDIT_18_SCENES.json').write_text(json.dumps(out,indent=2));deps={}
for n in ['blender','ffmpeg','ffprobe','gh','g++','chromium']:deps[n]={'path':shutil.which(n),'available':bool(shutil.which(n))}
for n in ['numpy','scipy','PIL','playwright','cv2']:
 try:m=importlib.import_module(n);deps[n]={'available':True,'version':getattr(m,'__version__',None)}
 except ImportError:deps[n]={'available':False}
(R/'reports/DEPENDENCIES.json').write_text(json.dumps(deps,indent=2));print('18 shots audited;',sum(bool(x['timing_conflicts']) for x in out),'timing conflicts; V10 unchanged')
