"""Evaluate an edited native .blend into a NEW tag for the illustrated renderer.
blender -b assets/STAIRCASE_M05_R05.blend --python source/export_edited.py -- --out-tag EDITED
Never overwrites the input scene, controls or existing evaluated data.
"""
import bpy,json,gzip,math,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--out-tag',required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);tag=args.out_tag;scene=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];camera=scene.camera;planpath=R/'assets'/scene['controls_filename'];plan=json.loads(planpath.read_text());source_path=bpy.data.filepath;outblend=R/'blender'/f'STAIRS_{tag}.blend';outdata=R/'scenes'/f'STAIRS_{tag}_NATIVE.json.gz';outcontrols=R/'assets'/f'CONTROLS_{tag}.json';assert not any(q.exists() for q in [outblend,outdata,outcontrols]);outcontrols.write_bytes(planpath.read_bytes());scene['controls_filename']=outcontrols.name
meshes=[o for o in scene.objects if o.type=='MESH' and 'base_color' in o and not o.get('illustration_hidden',False)];feet={s:bpy.data.objects['SHOE_'+s] for s in ['L','R']}
def V(q):return [float(x) for x in q]
def settime(t):f=t*30;i=math.floor(f+1e-9);scene.frame_set(i,subframe=f-i);bpy.context.view_layer.update()
def verts(o,deps):
 ev=o.evaluated_get(deps);m=ev.to_mesh();q=[V(ev.matrix_world@v.co) for v in m.vertices];ev.to_mesh_clear();return q
def sample(t,full=False):
 settime(t);deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);bones={n:{'head':V(er.matrix_world@b.head),'tail':V(er.matrix_world@b.tail),'matrix':[[float(x) for x in row] for row in er.matrix_world@b.matrix]} for n,b in er.pose.bones.items()};step=plan['frames'][min(len(plan['frames'])-1,round(t*plan['rate']))];f={s:{'vertices':verts(feet[s],deps),'sole_indices':[0,1,5,6],'toe_indices':[1,6],'target':step['feet'][j],'ankle_target':V(bpy.data.objects['CTRL_ANKLE_'+s].matrix_world.translation)} for j,s in enumerate(['L','R'])};row={'time':t,'bones':bones,'feet':f}
 if full:
  row['meshes']={o.name:verts(o,deps) for o in meshes if o.modifiers}
  cm=scene.camera.matrix_world;row['camera']={'eye':V(cm.translation),'right':V(cm.to_3x3()@Vector((1,0,0))),'up':V(cm.to_3x3()@Vector((0,1,0))),'forward':V(cm.to_3x3()@Vector((0,0,-1))),'ortho_scale':scene.camera.data.ortho_scale}
  row['face']=step.get('face',{'yaw':.94,'gaze':.94,'fear':.35,'blink':0})
 return row
settime(0);bpy.ops.wm.save_as_mainfile(filepath=str(outblend),compress=True);meta={'blender_version':bpy.app.version_string,'evaluation_origin':'M05 edited original M04 native scene; no reconstructed skeleton or skin','edited_source_file':source_path,'controller_sha256':hashlib.sha256(outcontrols.read_bytes()).hexdigest(),'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').glob('*.py')},'bones':{n:{'parent':b.parent.name if b.parent else None,'connected':b.use_connect,'rest_length_m':b.length,'constraints':[{'type':c.type,'target':c.target.name if hasattr(c,'target') and c.target else None,'chain_count':c.chain_count if c.type=='IK' else None,'use_stretch':c.use_stretch if c.type=='IK' else None} for c in rig.pose.bones[n].constraints]} for n,b in rig.data.bones.items()}}
cm=camera.matrix_world;cam={'eye':V(cm.translation),'right':V(cm.to_3x3()@Vector((1,0,0))),'up':V(cm.to_3x3()@Vector((0,1,0))),'forward':V(cm.to_3x3()@Vector((0,0,-1))),'ortho_scale':camera.data.ortho_scale};topology={o.name:{'faces':[[int(x) for x in p.vertices] for p in o.data.polygons],'color':o['base_color'],'bound_to_armature':bool(o.modifiers),'rest_vertices':[V(o.matrix_world@v.co) for v in o.data.vertices]} for o in meshes};frames=[sample(i/30,True) for i in range(150)];dense=[sample(i/120) for i in range(601)];jumps=[{'time':q['time'],'before':sample(q['time']-1e-5)['bones']['root']['head'],'after':sample(q['time']+1e-5)['bones']['root']['head'],'center':sample(q['time'])['bones']['root']['head']} for q in plan['root_keys'][1:-1]];baseline=sample(2,True);con=rig.pose.bones['shin.L'].constraints['LEG_TWO_BONE_IK_L'];original=con.influence;con.influence=0;mutated=sample(2,True);con.influence=original;settime(0)
with gzip.open(outdata,'wt',compresslevel=6) as fp:json.dump({'metadata':meta,'camera':cam,'meshes':topology,'frames':frames,'dense':dense,'root_key_probes':jumps,'ik_mutation':{'baseline':baseline,'disabled_left_IK':mutated},'blend_sha256':hashlib.sha256(outblend.read_bytes()).hexdigest()},fp,separators=(',',':'))
print('EDITED_NATIVE_SCENE_EXPORTED',outdata)
