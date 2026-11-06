import bpy,sys,math,hashlib,json,argparse
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from bootstrap import ROOT
import actions,vehicle_system as VS,sets
from world import World,Camera
from cameras import camera
from embed_assets import build,mesh,native
p=argparse.ArgumentParser();p.add_argument('--shot',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);shot=a.shot;dur=actions.DURATIONS[shot];out=R/'blender'/f'{shot}_WORLD_M09_RELEASE.blend';assert not out.exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);scene=bpy.context.scene;scene.name='M09_'+shot;scene.render.fps=30;scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.frame_start=0;scene.frame_end=round(dur*30)-1;states=[actions.state(shot,i/30) for i in range(round(dur*30))];build(scene,shot,states)
# Build the registered city from actual fixed geometry, not a scrolling plane.
w=World(Camera((10,12,-20),(0,1,25)),0);sets.city(w)
for i,g in enumerate(w.geometry):mesh(scene,f'WORLD_{g["name"]}_{i}',g['vertices'],[tuple(range(len(g['vertices'])))],g['color'])
cd=bpy.data.cameras.new('M07_CINEMATIC');cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);scene.camera=cam;cd.sensor_fit='HORIZONTAL';cd.sensor_width=36
for i,d in enumerate(states):
 c=camera(shot,i/30,d);cam.location=native(c.eye);cam.rotation_euler=(-native(c.forward)).to_track_quat('Z','Y').to_euler();cd.lens=c.focal/1080*36;cam.keyframe_insert('location',frame=i);cam.keyframe_insert('rotation_euler',frame=i);cd.keyframe_insert('lens',frame=i)
scene.frame_set(0);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);(R/'reports'/f'{shot}_WORLD_SOURCE.json').write_text(json.dumps({'blend':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'vehicle_state_source':'source/vehicle_system.py','shared_House17_origin':VS.HOUSE_ORIGIN.tolist(),'shared_House17_rotation':VS.HOUSE_R.tolist(),'native_scene_scope':'Editable vehicle roots, rotating wheels, fixed architecture and animated cinematic camera; procedural renderer uses same world definitions.'},indent=2));print('WORLD_EXPORTED',shot)
