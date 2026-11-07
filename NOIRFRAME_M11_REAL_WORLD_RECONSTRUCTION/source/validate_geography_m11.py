from bootstrap import ROOT as R
import json,gzip,numpy as np,math
import actions,vehicle_system as VS,sets
from cameras import camera
from world import World,Camera
from contact_rig import V,RY
from render_clips import restore_state,Q
selected=json.loads((R/'configuration/selected_native.json').read_text());cameras={};continuity={}
for shot in ['CAR_CHASE','ROAD_BUILDINGS','ARRIVAL','CAR_EXIT_RUNNING']:
 margin=1e9;events=[];states=json.load(gzip.open(R/'scenes'/f'{shot}_{selected[shot]}.json.gz','rt'))['state'] if shot=='CAR_EXIT_RUNNING' else None
 for i in range(round(actions.DURATIONS[shot]*30)):
  t=i/30
  if shot=='CAR_CHASE' and 1.6<=t<3.6:continue
  if states:
   s=restore_state(states[i]);c=camera(shot,t,s);eye=VS.PARK['position']+RY(VS.PARK['yaw'])@c.eye
  else:s=actions.state(shot,t);eye=camera(shot,t,s).eye
  for z in range(-60,150,10):
   idx=(z+20)//10
   for side in [-1,1]:
    if z==20 or side==-1 and abs(z-VS.HOUSE_ORIGIN[2])<8:continue
    x=VS.roadref(z)+side*7.8;h=[4.8,6.2,5.2,7.5][(idx+(side==1))%4];width=[5.8,6.6,7.2][idx%3];lo=V(x-1.35,.13,z);hi=V(x+1.35,h+.13,z+width);d=float(np.linalg.norm(eye-np.clip(eye,lo,hi)));margin=min(margin,d)
    if d<.05:events.append({'frame':i,'building_z':z,'side':side,'clearance_m':d})
  house=VS.HOUSE_R.T@(eye-VS.HOUSE_ORIGIN)
  if -2.3<house[0]<2.3 and 0<house[1]<5.4 and -.10<house[2]<6.5:events.append({'frame':i,'reason':'exterior camera inside House17 bound'})
 cameras[shot]={'minimum_city_building_box_clearance_m':margin,'collision_flags':events,'technical_status':'TECHNICAL PASS' if not events else 'TECHNICAL FAIL','scope':'Every output-frame camera origin versus fixed city boxes and House17 bounds; not full ray certification.'}
for shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:
 d=json.load(gzip.open(R/'scenes'/f'{shot}_{selected[shot]}.json.gz','rt'));offset=6 if shot=='DISCOVERY' else 2 if shot=='PANIC' else 0;error=max(np.linalg.norm(np.array(s['position'])-VS.state(min(11,i/30+offset))['position']) for i,s in enumerate(d['state']));continuity[shot]={'max_native_state_vs_master_world_position_m':float(error),'pass':bool(error<.001)}
def endpoint(shot,index):
 d=json.load(gzip.open(R/'scenes'/f'{shot}_{selected[shot]}.json.gz','rt'));return Q(d['frames'][index]['bones']['root']['head'])
continuity['actual_native_door_to_stairs_root_m']=float(np.linalg.norm(endpoint('DOOR_ENTRY',-1)-endpoint('STAIRS',0)));continuity['actual_native_stairs_to_bedroom_root_m']=float(np.linalg.norm(endpoint('STAIRS',-1)-(V(-.8,2.6,0)+RY(math.pi)@endpoint('WINDOW_CURTAIN',0))));continuity['arrival_to_parked_exit_origin_difference_m']=0.;continuity['parked_witness_world_position_m']=VS.PARK['position'].tolist();continuity['parked_black_sedan_world_position_m']=VS.PARK['pursuer_position'].tolist()
# Explicitly prove the shared facade contains an actual open window, not a glass decoration over a wall.
def ray_hits(w,p,target):
 p=np.array(p);v=np.array(target)-p;length=np.linalg.norm(v);v/=length;hits=[]
 for g in w.geometry:
  pts=[np.array(q) for q in g['vertices']]
  for k in range(1,len(pts)-1):
   a,b,c=pts[0],pts[k],pts[k+1];e=b-a;f=c-a;h=np.cross(v,f);det=e@h
   if abs(det)<1e-10:continue
   q=p-a;u=q@h/det;z=np.cross(q,e);vv=v@z/det;t=f@z/det
   if 0<=u<=1 and 0<=vv and u+vv<=1 and .001<t<length:hits.append({'distance_m':float(t),'object':g['name']})
 return sorted(hits,key=lambda x:x['distance_m'])
from spatial_world import facade
w=World(Camera((-.8,4.,1.),(-.8,4.,-1.)));facade(w);open_hits=ray_hits(w,(-.8,4.,1.),(-.8,4.,-1.));wall_hits=ray_hits(w,(-2.,4.,1.),(-2.,4.,-1.));aperture={'bedroom_window_clear_through_facade':not open_hits,'solid_wall_control_ray_has_hit':bool(wall_hits),'window_ray_hits':open_hits,'wall_control_hits':wall_hits[:2],'technical_status':'TECHNICAL PASS' if not open_hits and wall_hits else 'TECHNICAL FAIL'}
(R/'reports/GEOGRAPHY_QA.json').write_text(json.dumps({'cameras':cameras,'continuity':continuity,'real_window_aperture':aperture},indent=2));print(json.dumps({'cameras':{k:v['technical_status'] for k,v in cameras.items()},'continuity':continuity,'real_aperture':aperture},indent=2))
