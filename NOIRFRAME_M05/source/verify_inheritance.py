"""Verify M05 inherits M04 native skeleton, skin and all contact controllers exactly."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def h(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));rig=bpy.data.objects['M04_WITNESS_RIG'];bones={}
 for n,b in rig.data.bones.items():
  pb=rig.pose.bones[n];bones[n]={'head':list(b.head_local),'tail':list(b.tail_local),'matrix':[list(row) for row in b.matrix_local],'parent':b.parent.name if b.parent else None,'connected':b.use_connect,'length':b.length,'ik_limits':[pb.use_ik_limit_z,pb.ik_min_z,pb.ik_max_z,pb.lock_ik_x,pb.lock_ik_y,pb.ik_stretch]}
 meshes={}
 for o in bpy.context.scene.objects:
  if o.type=='MESH' and o.modifiers:
   meshes[o.name]={'verts':[list(v.co) for v in o.data.vertices],'faces':[list(f.vertices) for f in o.data.polygons],'weights':[[(o.vertex_groups[g.group].name,g.weight) for g in v.groups] for v in o.data.vertices],'modifiers':[(m.type,m.object.name if m.type=='ARMATURE' else '') for m in o.modifiers]}
 controls={}
 for name in ['CTRL_ANKLE_L','CTRL_ANKLE_R','CTRL_KNEE_POLE_L','CTRL_KNEE_POLE_R','CTRL_foot.L','CTRL_foot.R']:
  o=bpy.data.objects[name];controls[name]=[{'path':f.data_path,'index':f.array_index,'keys':[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation) for k in f.keyframe_points]} for f in o.animation_data.action.fcurves]
 return {'bones':h(bones),'character_meshes_and_skin':h(meshes),'contact_controllers':h(controls)}
a=snapshot(R.parent/'NOIRFRAME_M04/assets/STAIRCASE_M04_R06.blend');b=snapshot(R/'assets/STAIRCASE_M05_F01.blend');assert a==b,(a,b);report={'baseline':'NOIRFRAME_M04/assets/STAIRCASE_M04_R06.blend','M05':'assets/STAIRCASE_M05_F01.blend','M04_hashes':a,'M05_hashes':b,'all_identical':True,'meaning':'No bones, rest geometry, skinning, foot-target, foot-orientation or knee-pole curves reconstructed.'};(R/'reports/NATIVE_INHERITANCE.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
