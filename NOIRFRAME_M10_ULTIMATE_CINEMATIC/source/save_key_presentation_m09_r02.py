"""Save final POV camera/visibility in editable native scene; verify contact mesh parity."""
import bpy,sys,json,gzip,hashlib,math
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from cameras import camera
B=Matrix(((0,0,1),(1,0,0),(0,1,0)));d=json.load(gzip.open(R/'scenes/KEY_LOCK_M09D.json.gz','rt'));bpy.ops.wm.open_mainfile(filepath=str(R/'blender/KEY_LOCK_M09D.blend'));sc=bpy.context.scene
for i,s in enumerate(d['state']):
 c=camera('KEY_LOCK',i/30,s);sc.camera.location=B@Vector(c.eye);sc.camera.rotation_euler=(-(B@Vector(c.forward))).to_track_quat('Z','Y').to_euler();sc.camera.data.lens=c.focal*36/1080;sc.camera.keyframe_insert('location',frame=i);sc.camera.keyframe_insert('rotation_euler',frame=i);sc.camera.data.keyframe_insert('lens',frame=i)
 for o in [q for q in sc.objects if q.type=='MESH' and q.modifiers]:
  keep=o.name in ['SLEEVE_UPPER_L','SLEEVE_LOWER_L','MITTEN_L'] or o.name.startswith('M07_digit') and o.name.endswith('.L');o.hide_render=i>=56 and not keep;o.keyframe_insert('hide_render',frame=i)
for o in sc.objects:
 if o.animation_data and o.animation_data.action:
  for fc in o.animation_data.action.fcurves:
   if fc.data_path=='hide_render':
    for k in fc.keyframe_points:k.interpolation='CONSTANT'
error=0;count=0
for i in [0,60,120,180,240,269]:
 sc.frame_set(i);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
 for name in ['SLEEVE_LOWER_L','MITTEN_L','M07_digit0b.L','M07_digit1b.L']:
  o=bpy.data.objects[name];ev=o.evaluated_get(dep);mesh=ev.to_mesh()
  for v,q in zip(mesh.vertices,d['frames'][i]['meshes'][name]):error=max(error,(ev.matrix_world@v.co-Vector(q)).length);count+=1
  ev.to_mesh_clear()
assert error<1e-6
sc.frame_set(0);p=R/'blender/KEY_LOCK_EDITABLE_FINAL_M09_R02.blend';assert not p.exists();bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
(R/'reports/KEY_NATIVE_PRESENTATION_PARITY_R02.json').write_text(json.dumps({'native_mesh_vertices_checked':count,'maximum_geometry_difference_m':error,'change':'Camera and POV visibility only; interacting arm/hand/digits remain original evaluated native geometry','file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
