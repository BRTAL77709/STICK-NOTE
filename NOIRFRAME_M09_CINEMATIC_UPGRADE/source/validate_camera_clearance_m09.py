"""Camera-to-vehicle solid-box clearance. Excludes intended cockpit cameras."""
import json,numpy as np
from bootstrap import ROOT as R
import actions,vehicle_system as VS
from cameras import camera
from contact_rig import RY
out={}
for shot,duration in [('CAR_CHASE',11),('ROAD_BUILDINGS',7)]:
 minimum=1e9;worst=None
 for i in range(round(duration*30)):
  t=i/30
  if shot=='CAR_CHASE' and 4.4<=t<6.3:continue
  d=actions.state(shot,t);cam=camera(shot,t,d)
  for pref in ['', 'pursuer_']:
   q=RY(-d[pref+'yaw'])@(cam.eye-d[pref+'position']);lo=np.array([-.9,0,-2.15]);hi=np.array([.9,1.5,2.15]);dist=float(np.linalg.norm(q-np.clip(q,lo,hi)))
   if dist<minimum:minimum=dist;worst={'time_s':t,'vehicle':pref or 'witness'}
 out[shot]={'minimum_camera_to_vehicle_bound_m':minimum,'worst':worst,'tolerance_m':.10,'pass':minimum>.10,'scope':'Camera origin versus conservative oriented vehicle boxes, 30Hz. Does not certify all camera rays or environment collision.'}
# Explicit street-side constraint for the repaired exit camera.
import gzip
D=json.load(gzip.open(R/'scenes/CAR_EXIT_RUNNING_M09K.json.gz','rt'));margin=min(camera('CAR_EXIT_RUNNING',i/30,{k:(np.array(v) if isinstance(v,list) and k=='unused' else v) for k,v in s.items()}).eye[0]+6 for i,s in enumerate(D['state']))
out['CAR_EXIT_RUNNING']={'minimum_camera_street_side_distance_to_House17_facade_m':float(margin),'facade_car_local_x_m':-6,'pass':bool(margin>0),'scope':'Actual final camera origin remains on street side; separate visual frame inspection checks readable witness silhouette.'}
(R/'reports/CAMERA_CLEARANCE.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
