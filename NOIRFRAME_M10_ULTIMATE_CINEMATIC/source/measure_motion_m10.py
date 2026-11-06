"""Scoped actual evaluated geometry measurements; no force-simulation claims."""
import gzip,json,numpy as np,math
from bootstrap import ROOT as R
versions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());report={}
for s in ['DRIVING_COCKPIT','DRIVER_CHASE','CAR_EXIT_RUNNING','KEY_LOCK','DOOR_ENTRY','WINDOW_CURTAIN']:
 data=json.load(gzip.open(R/'scenes'/f'{s}_{versions[s]}.json.gz','rt'));maxangle=0.;prev={}
 for f in data['frames']:
  for side in ['L','R']:
   hip=np.asarray(f['bones']['thigh.'+side]['head']);knee=np.asarray(f['bones']['thigh.'+side]['tail']);ankle=np.asarray(f['bones']['shin.'+side]['tail']);normal=np.cross(knee-hip,ankle-knee);length=np.linalg.norm(normal)
   if length<1e-5:prev.pop(side,None);continue
   normal/=length
   if side in prev:maxangle=max(maxangle,math.degrees(math.acos(float(np.clip(normal@prev[side],-1,1)))))
   prev[side]=normal
 report[s]={'maximum_adjacent_knee_plane_change_deg_at_30Hz':maxangle,'interpretation':'A change in the measured bend plane, including intended turning; not a standalone natural-motion pass.'}
 if s=='DOOR_ENTRY':
  first=data['state'][390]['pose']['root'];last=data['state'][-1]['pose']['root'];landings={}
  for j in range(2):
   prev=True;land=[]
   for d in data['state'][390:]:
    planted=d['pose']['legs'][j]['planted']
    if planted and not prev:land.append(d['time'])
    prev=planted
   landings[str(j)]=land
  report[s].update(hallway_root_displacement_m=float(np.linalg.norm(np.asarray(last)-first)),hallway_foot_landings_s=landings,final_root=last)
(R/'reports/MOTION_MEASUREMENTS.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
