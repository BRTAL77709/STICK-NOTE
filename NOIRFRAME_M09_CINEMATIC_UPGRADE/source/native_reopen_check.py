"""Independently reopen saved native files and compare evaluated skinned vertices."""
import bpy,sys,json,gzip,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];versions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());results={}
for shot in ['DRIVING_COCKPIT','KEY_LOCK','DOOR_ENTRY','WINDOW_CURTAIN','CAR_EXIT_RUNNING','DRIVER_CHASE']:
 tag=versions[shot];path=R/'blender'/f'{shot}_{tag}.blend';d=json.load(gzip.open(R/'scenes'/f'{shot}_{tag}.json.gz','rt'));bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];worst=0.;count=0;n=len(d['frames'])
 for i in sorted({0,n//5,n//2,n*3//4,n-1}):
  scene.frame_set(i);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
  for name in ['SHOE_L','SHOE_R','HOODIE_TORSO','SLEEVE_LOWER_L','MITTEN_L']:
   if name not in d['frames'][i]['meshes']:continue
   o=bpy.data.objects[name];ev=o.evaluated_get(dep);m=ev.to_mesh()
   for v,q in zip(m.vertices,d['frames'][i]['meshes'][name]):worst=max(worst,(ev.matrix_world@v.co-Vector(q)).length);count+=1
   ev.to_mesh_clear()
 ik=[{'bone':b.name,'constraint':c.name,'chain_count':c.chain_count,'stretch':c.use_stretch} for b in rig.pose.bones for c in b.constraints if c.type=='IK']
 results[shot]={'file':str(path.relative_to(R)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checked_vertex_samples':count,'max_reopened_vs_exported_vertex_error_m':worst,'tolerance_m':.0002,'IK_constraints':ik,'technical_status':'TECHNICAL PASS' if worst<.0002 and len(ik)>=8 and all(not c['stretch'] for c in ik) else 'TECHNICAL FAIL','limits':'Five saved-pose samples, skinned meshes only. Prop controller/native mirror parity and full collision are separate checks.'};print('REOPENED',shot,worst,flush=True)
(R/'reports/NATIVE_REOPEN_VERIFICATION.json').write_text(json.dumps(results,indent=2))
