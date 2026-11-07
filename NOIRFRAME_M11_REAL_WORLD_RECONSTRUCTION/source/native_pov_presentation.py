"""POV visibility only, preserve native geometry/motion; save separate editable files."""
import bpy,json,gzip,sys,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];versions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());report={}
for shot,cut in [('KEY_LOCK',2.),('DOOR_ENTRY',10.8)]:
 tag=versions[shot];cache=json.load(gzip.open(R/'scenes'/f'{shot}_{tag}.json.gz','rt'));bpy.ops.wm.open_mainfile(filepath=str(R/'blender'/f'{shot}_{tag}.blend'));sc=bpy.context.scene;head=bpy.data.objects['APPROVED_HEAD_CARD'];head.hide_render=False;head.keyframe_insert('hide_render',frame=round(cut*30)-1);head.hide_render=True;head.keyframe_insert('hide_render',frame=round(cut*30));sc.frame_set(0);out=R/'blender'/f'{shot}_EDITABLE_FINAL.blend';assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);err=0.;n=0
 for i in [0,len(cache['frames'])//2,len(cache['frames'])-1]:
  sc.frame_set(i);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
  for name in ['SLEEVE_LOWER_L','MITTEN_L','SHOE_L']:
   o=bpy.data.objects[name];ev=o.evaluated_get(dep);m=ev.to_mesh()
   for v,q in zip(m.vertices,cache['frames'][i]['meshes'][name]):err=max(err,(ev.matrix_world@v.co-Vector(q)).length);n+=1
   ev.to_mesh_clear()
 report[shot]={'path':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'native_motion_source':f'{shot}_{tag}.blend','checked_vertices':n,'max_body_vertex_change_m':err,'cut_s':cut,'technical_status':'TECHNICAL PASS' if err<.0002 else 'TECHNICAL FAIL','scope':'Only self-POV head visibility changes; body remains native evaluated and unchanged.'}
(R/'reports/NATIVE_POV_PRESENTATION.json').write_text(json.dumps(report,indent=2))
