from pathlib import Path
import sys,math,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'));from scene_builder import corner_camera,pursuit_camera;from motion_state import state,road_x
out={}
for name,fn,start,duration in [('pursuit',pursuit_camera,32,3),('corner',corner_camera,40,2)]:
 xs=[];depths=[];offsets=[]
 for k in range(int(duration*30)):
  t=start+k/30;c=fn(t);offsets.append(abs(c.x-road_x(c.z)))
  for black in [False,True]:
   s=state(t,black);hd=s['yaw']
   for x,y,z in [(x,y,z) for x in [-1.25,1.25] for y in [0,1.65] for z in [-2.45,2.45]]:
    p=(s['x']+x*math.cos(hd)+z*math.sin(hd),y,s['z']+z*math.cos(hd)-x*math.sin(hd));xs.append(c.project(p)[0]);depths.append(c.depth(p))
 out[name]={'max_camera_road_x_offset_m':max(offsets),'min_vehicle_depth_m':min(depths),'vehicle_horizontal_bounds_px':[min(xs),max(xs)]}
 assert max(offsets)<7.8 and min(depths)>1 and min(xs)>0 and max(xs)<1080,out[name]
(R/'reports/chase-camera-validation.json').write_text(json.dumps(out,indent=2));print(out)
