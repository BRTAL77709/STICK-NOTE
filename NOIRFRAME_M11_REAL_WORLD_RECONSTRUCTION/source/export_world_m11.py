"""Native editable world/vehicles from the same registered procedural geometry as final output."""
import bpy,sys,json,math,hashlib,argparse,numpy as np
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));import actions,sets,vehicle_system as VS
from world import World,Camera
from cameras import camera
from embed_assets import build,mesh,native,empty,vehicle
from contact_rig import RY
p=argparse.ArgumentParser();p.add_argument('--shot',default='MASTER_LAYOUT');p.add_argument('--tag',default='M11R03');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);shot=a.shot;out=R/'blender'/f'{shot}_WORLD_{a.tag}.blend';assert not out.exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);sc=bpy.context.scene;sc.name='M11_'+shot;sc.render.fps=30;sc.render.resolution_x=1080;sc.render.resolution_y=1920;root=empty(sc,'WORLD_ROOT');groups={n:empty(sc,n) for n in ['CITY','ROAD_NETWORK','HOUSE_17','CHARACTER_RIGS','PROPS','CAMERA_RIGS','LIGHTS','AUDIO']}
for o in groups.values():o.parent=root
if shot!='MASTER_LAYOUT':
 dur=actions.DURATIONS[shot];states=[actions.state(shot,i/30) for i in range(round(dur*30))];build(sc,'CAR_CHASE' if shot=='ARRIVAL' else shot,states);sc.frame_end=len(states)-1
else:
 dur=1.;sc.frame_end=29
 for n,black in [('WITNESS_CAR',False),('BLACK_SEDAN',True)]:
  o,wheels=vehicle(sc,n,black);o.parent=root;pref='pursuer_' if black else '';o.location=native(VS.PARK[pref+'position']);B=Matrix(((0,0,1),(1,0,0),(0,1,0)));o.rotation_euler=(B@Matrix(RY(VS.PARK[pref+'yaw']).tolist())@B.transposed()).to_euler()
geometry=[]
for eye in [(100,20,50),(-100,20,50),(0,20,-100),(0,20,200),(0,150,50),(0,-50,50)]:
 w=World(Camera(eye,(0,1,50)));w.full_detail=True;sets.city(w);geometry.extend(w.geometry)
seen=set()
for i,g in enumerate(geometry):
 sig=(g['name'],tuple(sorted(tuple(round(x,5) for x in q) for q in g['vertices'])))
 if sig in seen:continue
 seen.add(sig);parent=groups['HOUSE_17'] if any(k in g['name'].lower() for k in ['stair','bedroom','house17','landing']) else groups['ROAD_NETWORK'] if any(k in g['name'].lower() for k in ['road','curb','sidewalk','crosswalk']) else groups['CITY'];mesh(sc,f'{g["name"]}_{i}',g['vertices'],[tuple(range(len(g['vertices'])))],g['color'],parent)
for o in list(sc.objects):
 if o!=root and o.parent is None:o.parent=root
cd=bpy.data.cameras.new('M11_CINEMATIC');cam=bpy.data.objects.new(cd.name,cd);sc.collection.objects.link(cam);cam.parent=groups['CAMERA_RIGS'];sc.camera=cam;cd.sensor_fit='HORIZONTAL';cd.sensor_width=36
for i in range(round(dur*30)):
 d=states[i] if shot!='MASTER_LAYOUT' else {};c=camera(shot,i/30,d) if d else Camera((12,16,48),VS.HOUSE_ORIGIN,850);cam.location=native(c.eye);cam.rotation_euler=(-native(c.forward)).to_track_quat('Z','Y').to_euler();cd.lens=c.focal/1080*36;cam.keyframe_insert('location',frame=i);cam.keyframe_insert('rotation_euler',frame=i);cd.keyframe_insert('lens',frame=i)
sc['units']='metres; Blender XYZ = renderer ZXY';sc['House17_origin']=VS.HOUSE_ORIGIN.tolist();sc['scope']='Complete editable spatial layout and native vehicle/camera keys. Character scene files supply evaluated skin; final cel face/mirror composition remains procedural.';sc.frame_set(0);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);(R/'reports'/f'{shot}_WORLD_SOURCE.json').write_text(json.dumps({'blend':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'surfaces':len(seen),'House17_origin':VS.HOUSE_ORIGIN.tolist(),'House17_rotation':VS.HOUSE_R.tolist()},indent=2));print('WORLD_EXPORTED',shot,len(seen))
