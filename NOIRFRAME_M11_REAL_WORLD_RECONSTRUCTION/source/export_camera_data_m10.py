"""Actual shot camera tracks with explicit spaces and matching cached actor state."""
import json,gzip,math,numpy as np
from bootstrap import ROOT as R
from cameras import camera
from interaction_system import restore
import vehicle_system as VS
from contact_rig import RY,V
versions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());shots=json.loads((R/'CURRENT_SHOTS.json').read_text());out={}
for shot,row in shots.items():
 data=None
 if shot=='STAIRS':
  data=json.load(gzip.open(R/'scenes/STAIRS_M10D_NATIVE.json.gz','rt'));out[shot]={'space':'native staircase coordinates, Blender Z-up','frames':[f['camera'] for f in data['frames']]};continue
 if shot not in ['ROAD_BUILDINGS','CAR_CHASE']:data=json.load(gzip.open(R/'scenes'/f'{shot}_{versions[shot]}.json.gz','rt'))
 driver=json.load(gzip.open(R/'scenes'/f'DRIVER_CHASE_{versions[shot]}.json.gz','rt')) if shot=='CAR_CHASE' else None;frames=[]
 for i in range(round(row['duration']*30)):
  t=i/30;subject='DRIVER_CHASE' if driver and 1.6<=t<3.6 else shot;d=restore(driver['state'][i]) if subject=='DRIVER_CHASE' else restore(data['state'][i]) if data else VS.state(t if shot=='CAR_CHASE' else t*1.1);c=camera(subject,t,d);space='car local' if subject in ['DRIVING_COCKPIT','DRIVER_CHASE','CAR_EXIT_RUNNING'] else 'House17 local' if shot=='DOOR_ENTRY' else 'bedroom/window local' if shot=='WINDOW_CURTAIN' else 'registered city world';frames.append({'time_s':t,'space':space,'eye':c.eye.tolist(),'target':c.target.tolist(),'up':c.up.tolist(),'focal_px':c.focal})
 out[shot]={'fps':30,'units':'metres; Y-up unless native staircase','frames':frames}
(R/'CAMERA_ANIMATION.json').write_text(json.dumps(out,separators=(',',':')))
