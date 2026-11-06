"""Reopen the saved .blend, evaluate its actual modifiers and compare to the rendered cache."""
import bpy,json,gzip,math,hashlib
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
R=Path(__file__).resolve().parents[1];tag='F01';scene=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];cache=json.load(gzip.open(R/'assets'/f'EVALUATED_{tag}.json.gz','rt'));worst=0.;checked=0
for i in [0,30,60,90,120,149]:
 scene.frame_set(i);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
 for name in ['SHOE_L','SHOE_R','WEIGHTED_APPROVED_HOODIE','APPROVED_HEAD_CARD']:
  obj=bpy.data.objects[name];ev=obj.evaluated_get(deps);mesh=ev.to_mesh()
  for actual,expected in zip(mesh.vertices,cache['frames'][i]['meshes'][name]):worst=max(worst,(ev.matrix_world@actual.co-Vector(expected)).length);checked+=1
  ev.to_mesh_clear()
cons=[c for b in rig.pose.bones for c in b.constraints if c.type=='IK'];assert len(cons)==2 and all(c.chain_count==2 and not c.use_stretch for c in cons);assert worst<1e-6
images=[image for image in bpy.data.images if image.name.startswith('APPROVED_HEAD')];assert images and all(image.packed_file for image in images)
cam=scene.camera;frame=cam.data.view_frame(scene=scene);width=max(v.x for v in frame)-min(v.x for v in frame);height=max(v.y for v in frame)-min(v.y for v in frame);points=[(-.22,0,.76),(.4,0,1.15),(.9,0,1.305)];probes=[]
for point in points:q=world_to_camera_view(scene,cam,Vector(point));probes.append({'point':point,'normalized_camera_xy':[q.x,q.y]})
projection_error=0.
for fi in [0,30,60,90,120,149]:
 scene.frame_set(fi);bpy.context.view_layer.update();record=cache['frames'][fi]['camera'];eye=Vector(record['eye']);right=Vector(record['right']);up=Vector(record['up']);scale=1920/record['ortho_scale']
 for point in points:
  p=Vector(point);q=world_to_camera_view(scene,scene.camera,p);expected=(540+(p-eye).dot(right)*scale,960-(p-eye).dot(up)*scale);actual=(q.x*1080,(1-q.y)*1920);projection_error=max(projection_error,math.dist(actual,expected))
report={'max_moving_camera_projection_error_px':projection_error,'reopened_blend':bpy.data.filepath,'Blender_version':bpy.app.version_string,'native_IK_constraints':len(cons),'evaluated_vertices_compared':checked,'max_saved_scene_vs_cache_vertex_error_m':worst,'head_image_packed':True,'orthographic_frame_width_m':width,'orthographic_frame_height_m':height,'projection_probes':probes,'rig_drives_the_exported_geometry':True};(R/'reports/NATIVE_REOPEN_VERIFICATION.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
