"""Check native shoes against actual world road/curb/sidewalk surfaces, not planned markers."""
import gzip,json,math,numpy as np
from bootstrap import ROOT as R
import vehicle_system as VS
from contact_rig import RY

def terrain(p):
 z0=-24+5*math.floor((p[2]+24)/5);u=(p[2]-z0)/5;c=VS.roadref(z0)*(1-u)+VS.roadref(z0+5)*u;x=abs(p[0]-c)
 return 0. if x<=4.5 else .13*min(1,(x-4.5)/.20)
def measure(tag):
 d=json.load(gzip.open((R.parent/'NOIRFRAME_M07_ALL_SCENE_REPAIRS'/'scenes'/f'CAR_EXIT_RUNNING_{tag}.json.gz') if tag=='R09' else (R/'scenes'/f'CAR_EXIT_RUNNING_{tag}.json.gz'),'rt'));worst=0;info=None
 for f in d['frames']:
  t=f['time'];v=VS.state(min(11,9+t));M=RY(v['yaw']);pos=v['position']
  for s in ['L','R']:
   vv=np.array([[q[1],q[2],q[0]] for q in f['meshes']['SHOE_'+s]]);edges=set()
   for face in d['topology']['SHOE_'+s]['faces']:
    for a,b in zip(face,face[1:]+face[:1]):edges.add(tuple(sorted([a,b])))
   pts=list(vv)
   for a,b in edges:
    for u in [.2,.4,.6,.8]:pts.append(vv[a]*(1-u)+vv[b]*u)
   for p in pts:
    world=pos+M@p;penetration=terrain(world)-world[1]
    if penetration>worst:worst=penetration;info={'time_s':t,'side':s,'world_point':world.tolist(),'surface_height_m':terrain(world)}
 return {'max_sampled_shoe_terrain_penetration_m':worst,'worst':info}
a=measure('R09');b=measure(json.loads((R/'reports/SHOT_REVISIONS.json').read_text())['CAR_EXIT_RUNNING']);report={'M07_baseline':a,'M08':b,'method':'Native evaluated shoe vertices and four interior edge samples, every rendered frame30Hz; terrain interpolates exact5m road mesh endpoints and actual0..130mm curb ramp. Not continuous collision certification.','tolerance_m':.0015,'technical_status':'TECHNICAL PASS' if b['max_sampled_shoe_terrain_penetration_m']<.0015 else 'TECHNICAL FAIL'};(R/'reports/EXIT_TERRAIN_REPAIR.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
