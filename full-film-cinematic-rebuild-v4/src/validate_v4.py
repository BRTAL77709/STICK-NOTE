"""Inspect all poses/data, hand-wheel contacts, arm lengths and physical continuity."""
from pathlib import Path
import json,math,hashlib
import numpy as np
from motion_state import *
from driver_rig import pose
from render_base import ext_camera
R=Path(__file__).resolve().parents[1]
a=json.loads((R/'hyperframes/assets/vehicle-state.js').read_text().split('=',1)[1].rstrip(';'))
errors=[];contacts=[];arms=[];kin=[];data=[];steer=[]
for f in range(451):
 t=f/30;p=pose(t);s=vehicleState(t)
 for k,v in s.items():
  if isinstance(v,(int,float)):data.append(abs(v-a[f][k]))
 cx,cy,rx,ry,ang=p['wheel']
 for j,(sh,el,ha) in enumerate(zip(p['shoulders'],p['elbows'],p['hands'])):
  th=[math.pi*.80,math.pi*.20][j]+ang;target=(cx+rx*math.cos(th),cy-ry*math.sin(th));contacts.append(math.dist(ha,target));arms.extend([abs(math.dist(sh,el)-178),abs(math.dist(el,ha)-178)])
 for black in [False,True]:
  st=state(t,black);assert abs(st['wheel_rad']*.32-st['distance_m'])<1e-9
  if .001<t<14.999:
   dt=.0001;b=state(t-dt,black);c=state(t+dt,black);v=math.hypot(c['x']-b['x'],c['z']-b['z'])/(2*dt);kin.append(abs(v-st['speed_mps']))
 steer.append(s['steering_wheel_rad'])
assert max(data)<1e-8;assert max(contacts)<1e-8;assert max(arms)<1e-7;assert max(kin)<.01
prior=json.loads((R/'reports/previous-version-hashes.json').read_text())
missing_prior=[]
for e in prior:
 p=R.parent/e['path']
 if not p.exists(): missing_prior.append(e['path']);continue
 assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'],p
snap=[]
for t in [0,.8,2,2.2,2.65,3.35,4.45,6.3,9,11.7,12.3,13.25,15]:
 s=vehicleState(t);p=pose(t);snap.append({'t':t,'x':s['x'],'z':s['z'],'speed_kmh':s['speed_kmh'],'rpm':s['rpm'],'distance_m':s['distance_m'],'pursuit_distance_m':s['pursuit_distance_m'],'head_yaw':p['yaw'],'hands':p['hands'],'steering_wheel_rad':s['steering_wheel_rad']})
report={'ok':True,'poses_checked':451,'data_max_error':max(data),'hand_wheel_max_error_px':max(contacts),'arm_length_max_error_px':max(arms),'velocity_position_max_error_mps':max(kin),'steering_wheel_range_degrees':[min(steer)*180/math.pi,max(steer)*180/math.pi],'prior_files_hash_matched':len(prior)-len(missing_prior),'prior_files_not_present_in_this_checkout':len(missing_prior),'samples':snap,'caption_timing':'Measured whole-sentence boundaries; no verified word alignment','audio_listening':'Unsupported; creative review pending'}
(R/'reports/source-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='samples'},indent=2))
