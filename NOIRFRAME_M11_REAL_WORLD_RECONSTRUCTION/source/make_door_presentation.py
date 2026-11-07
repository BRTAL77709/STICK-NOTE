"""Camera-only native presentation of already verified R08 motion; no rig/pose reconstruction."""
import bpy,sys,gzip,json,math,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from bootstrap import ROOT
from cameras import camera
B=Matrix(((0,0,1),(1,0,0),(0,1,0)));cache=json.load(gzip.open(R/'scenes/DOOR_ENTRY_R08.json.gz','rt'));bpy.ops.wm.open_mainfile(filepath=str(R/'blender/DOOR_ENTRY_R08.blend'));scene=bpy.context.scene;cam=scene.camera
for i in range(324,390):
 d=cache['state'][i];c=camera('DOOR_ENTRY',i/30,d);cam.location=B@Vector(c.eye);cam.rotation_euler=(-(B@Vector(c.forward))).to_track_quat('Z','Y').to_euler();cam.data.lens=c.focal*36/1080;cam.keyframe_insert('location',frame=i);cam.keyframe_insert('rotation_euler',frame=i);cam.data.keyframe_insert('lens',frame=i)
for o in scene.objects:
 if o.type=='MESH' and o.modifiers:
  keep=o.name!='APPROVED_HEAD_CARD'
  if not keep:
   o.hide_render=False;o.keyframe_insert('hide_render',frame=323);o.hide_render=True;o.keyframe_insert('hide_render',frame=324)
scene.frame_set(0);out=R/'blender/DOOR_ENTRY_PRESENTATION_R15.blend';assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);error=0;count=0
for i in [0,90,200,324,348,389]:
 scene.frame_set(i);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
 for name in ['SLEEVE_LOWER_L','MITTEN_L','M07_digit0b.L','M07_digit1b.L']:
  o=bpy.data.objects[name];ev=o.evaluated_get(dep);m=ev.to_mesh()
  for v,q in zip(m.vertices,cache['frames'][i]['meshes'][name]):error=max(error,(ev.matrix_world@v.co-Vector(q)).length);count+=1
  ev.to_mesh_clear()
assert error<.0002
(R/'reports/DOOR_POV_PRESENTATION.json').write_text(json.dumps({'native_presentation_file':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'motion_geometry_source':'blender/DOOR_ENTRY_R08.blend','arm_vertices_checked':count,'max_native_presentation_vs_R08_arm_error_m':error,'POV_cut_s':10.8,'door_closed_before_POV_s':9.85,'change':'Only native camera and body render visibility changed after entry. Gripping forearm, mitten and digits remain native evaluated meshes. Visible thumbturn uses same scripted transform as native prop.','approval':'ARTISTIC REVIEW REQUIRED'},indent=2));print('DOOR_POV_NATIVE_SAVED',error)
