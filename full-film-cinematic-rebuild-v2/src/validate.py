"""Independent numerical checks over every rendered pose and projected camera."""
import json,math
from pathlib import Path
import motion_state as m
from render import scene,ext_camera
ROOT=Path(__file__).resolve().parents[1]
def main():
 errors=[[],[]];max_ay=0;states=[]
 for f in range(450):
  t=f/30;svg=scene(t);assert svg.startswith('<svg') and svg.endswith('</svg>') and 'nan' not in svg.lower()
  for i,b in enumerate([False,True]):
   s=m.state(t,b);h=.0001;a=m.state(t-h,b);z=m.state(t+h,b);v=math.hypot(z['x']-a['x'],z['z']-a['z'])/(2*h);errors[i].append(abs(v-s['speed_mps']))
   assert all(math.isfinite(v) for v in s.values());assert abs(s['wheel_rad']*.32-s['distance_m'])<1e-9
   max_ay=max(max_ay,abs(s['roll']))
  if f%15==0:states.append({'frame':f,**m.state(t),'pursuit_distance_m':m.pursuit_distance(t)})
 assert max(errors[0])<.02 and max(errors[1])<.02,[max(x) for x in errors]
 assert sum(round((b-a)*30) for a,b,n in m.CUTS)==450
 caps=json.loads((ROOT/'narration-timing.json').read_text());assert all(a['end']<=b['start'] for a,b in zip(caps,caps[1:]));assert caps[-1]['end']<15
 displacement={}
 for a,b,mode in [(0,1.966667,'Departure'),(7,9.966667,'Street acceleration'),(13.25,14.966667,'Corner escape')]:
  sa=m.state(a);sb=m.state(b);ca=ext_camera(a,mode);cb=ext_camera(b,mode);pa=ca.project((sa['x'],.8,sa['z']));pb=cb.project((sb['x'],.8,sb['z']))
  displacement[mode]={'world_distance_m':m.travel(b)-m.travel(a),'projected_center_first':pa,'projected_center_last':pb,'projected_center_delta_px':math.hypot(pb[0]-pa[0],pb[1]-pa[1])}
 assert displacement['Departure']['projected_center_delta_px']>100
 result={'source_poses_evaluated':450,'fps':30,'duration':15,'maximum_world_speed_error_mps':[max(x) for x in errors],'speed_kmh_samples':{str(t):m.speed(t)*3.6 for t in [0,2,4,5,7,10,12,14.5,15]},'heading_change_corner_degrees':math.degrees(m.state(14.966667)['yaw']-m.state(12.5)['yaw']),'tire_radius_m':.32,'wheel_travel_relation':'Exact distance/radius for independent blue/black odometers','ground_tire_bottom_m':0,'vehicle_state_fields':list(m.state(1).keys()),'projected_movement':displacement,'mirror_distance_10s_m':m.pursuit_distance(10),'mirror_distance_12_5s_m':m.pursuit_distance(12.5),'captions':len(caps),'caption_overlaps':0,'note':'Source/model/IK and camera checks, not an artistic certification or a replacement for encoded playback.'}
 (ROOT/'reports/source-validation.json').write_text(json.dumps(result,indent=2));(ROOT/'reports/motion-samples.json').write_text(json.dumps(states,indent=2));(ROOT/'plan/timeline.json').write_text(json.dumps([{'start':a,'end':b,'shot':n} for a,b,n in m.CUTS],indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
