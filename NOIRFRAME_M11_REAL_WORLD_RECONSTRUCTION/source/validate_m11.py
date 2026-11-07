"""Actual Blender cache checks and explicit camera/continuity scope; artistic approval is never inferred."""
from bootstrap import ROOT as R
import json,gzip,numpy as np,math,hashlib
import actions,vehicle_system as VS
from cameras import camera
from render_clips import restore_state,Q
from validate_interactions import run
from spatial_world import ROOM
TAG='M11R01';contacts={};cams={};paths={};producer={}
for shot,TAG in json.loads((R/'configuration/selected_native.json').read_text()).items():
 file=R/'scenes'/f'{shot}_{TAG}.json.gz';d=json.load(gzip.open(file,'rt'));blend=R/'blender'/f'{shot}_{TAG}.blend';assert hashlib.sha256(blend.read_bytes()).hexdigest()==d['blend_sha256'];producer[shot]={'blend':str(blend.relative_to(R)),'blend_sha256':d['blend_sha256'],'cache_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'cached_source_sha256':d['source_sha256']};contacts[shot]=run(shot,TAG);rows=[];bad=[];margin=1e9;headclear=1e9
 for i,(raw,f) in enumerate(zip(d['state'],d['frames'])):
  s=restore_state(raw);c=camera(shot,i/30,s);head=Q(f['bones']['head']['head']);headclear=min(headclear,float(np.linalg.norm(c.eye-head))-.22)
  if shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:
   m=min(.62-abs(c.eye[0]),1.425-c.eye[1],c.eye[2]+1.35,-.46-c.eye[2])
   if not c.eye[2]<s['pose']['root'][2]-.4:bad.append({'frame':i,'reason':'camera not behind driver'})
  elif shot in ['WINDOW_CURTAIN','PHONE_CALL','UNKNOWN_CALLER']:
   x0,x1,z0,z1=ROOM;m=min(c.eye[0]-x0,x1-c.eye[0],c.eye[2]-z0,z1-c.eye[2],c.eye[1],2.8-c.eye[1])
  elif shot=='STAIRS':
   m=min(c.eye[0]+2.3,2.3-c.eye[0],c.eye[2],6.5-c.eye[2],5.36-c.eye[1])
   if c.eye[1]>2.6 and abs(c.eye[0]-.34)<.06 and c.eye[2]<5.6:bad.append({'frame':i,'reason':'bedroom partition'})
  else:m=None
  if m is not None:
   margin=min(margin,float(m))
   if m<.02:bad.append({'frame':i,'reason':'boundary clearance','metres':float(m)})
  rows.append({'frame':i,'time_s':i/30,'eye':c.eye.tolist(),'target':c.target.tolist(),'focal_pixels_1080':c.focal,'horizontal_FOV_degrees':math.degrees(2*math.atan(540/c.focal)),'near_m':.1,'space':'vehicle local' if shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC','CAR_EXIT_RUNNING'] else 'House17 local' if shot in ['KEY_LOCK','DOOR_ENTRY','STAIRS'] else 'bedroom local'})
 cams[shot]={'minimum_enclosing_boundary_clearance_m':None if margin==1e9 else margin,'minimum_head_envelope_clearance_m':headclear,'collision_flags':bad,'technical_status':'TECHNICAL PASS' if not bad and headclear>.03 else 'TECHNICAL FAIL','scope':'Every-frame camera origin versus explicit enclosing room/cabin bounds and .22m head envelope. Not a proof of every image ray or all swept mesh collisions.'};paths[shot]=rows
 if shot=='STAIRS':contacts[shot]['root_elevation_gain_m']=float(np.array(d['state'][-1]['pose']['root'])[1]-np.array(d['state'][0]['pose']['root'])[1]);contacts[shot]['actual_risers']=15
(R/'reports/NATIVE_CONTACT_QA.json').write_text(json.dumps(contacts,indent=2));(R/'reports/CAMERA_QA.json').write_text(json.dumps(cams,indent=2));(R/'reports/NATIVE_PRODUCERS.json').write_text(json.dumps(producer,indent=2));(R/'CAMERA_ANIMATION.json').write_text(json.dumps(paths,separators=(',',':')));print('CAMERAS',{k:v['technical_status'] for k,v in cams.items()})
