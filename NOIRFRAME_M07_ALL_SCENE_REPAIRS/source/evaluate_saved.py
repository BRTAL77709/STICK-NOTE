"""Export an edited saved native character scene without recreating its rig.
blender -b blender/MY_EDIT.blend --python source/evaluate_saved.py -- --shot KEY_LOCK --tag EDIT --controller source/actions_R08.py
Prop/camera timing remains in the controller scripts; this utility exports character geometry.
"""
import bpy,sys,json,gzip,math,hashlib,argparse,importlib.util,shutil
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from bootstrap import ROOT
p=argparse.ArgumentParser();p.add_argument('--shot',required=True);p.add_argument('--tag',required=True);p.add_argument('--controller',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);controller=Path(a.controller).resolve();spec=importlib.util.spec_from_file_location('edited_controller',controller);actions=importlib.util.module_from_spec(spec);spec.loader.exec_module(actions);dur=actions.DURATIONS[a.shot];n=round(dur*30);scene=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];outblend=R/'blender'/f'{a.shot}_{a.tag}.blend';outdata=R/'scenes'/f'{a.shot}_{a.tag}.json.gz';ctrlcopy=R/'source'/f'actions_{a.tag}.py';assert not any(q.exists() for q in [outblend,outdata,ctrlcopy]);shutil.copy2(controller,ctrlcopy);scene.frame_set(0);bpy.ops.wm.save_as_mainfile(filepath=str(outblend),compress=True);objects=[o for o in scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]
def L(q):return list(map(float,q))
def sample(t,full):
 fr=t*30;i=math.floor(fr);scene.frame_set(i,subframe=fr-i);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);row={'time':t,'bones':{n:{'head':L(er.matrix_world@b.head),'tail':L(er.matrix_world@b.tail)} for n,b in er.pose.bones.items()},'targets':{s:L(bpy.data.objects['M07_WRIST_'+s].matrix_world.translation) for s in ['L','R']},'finger_targets':{s:[L(bpy.data.objects[f'M07_FINGERTIP_{j}_{s}'].matrix_world.translation) for j in range(2)] for s in ['L','R']}};geometry={}
 for o in objects if full else [bpy.data.objects['SHOE_'+s] for s in ['L','R']]:
  ev=o.evaluated_get(deps);m=ev.to_mesh();geometry[o.name]=[L(ev.matrix_world@v.co) for v in m.vertices];ev.to_mesh_clear()
 row['meshes' if full else 'shoes']=geometry;return row
frames=[sample(i/30,True) for i in range(n)];dense=[sample(i/60,False) for i in range(round(dur*60))]
def conv(q):
 if isinstance(q,np.ndarray):return q.tolist()
 if isinstance(q,np.generic):return q.item()
 if isinstance(q,dict):return {k:conv(v) for k,v in q.items()}
 if isinstance(q,(list,tuple)):return [conv(v) for v in q]
 return q
hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').rglob('*.py')};hashes['source/actions.py']=hashlib.sha256(controller.read_bytes()).hexdigest();data={'shot':a.shot,'duration':dur,'fps':30,'evaluation_origin':'Edited native scene; no reconstructed animation','topology':{o.name:{'faces':[list(p.vertices) for p in o.data.polygons],'color':o.get('base_color','#294653')} for o in objects},'frames':frames,'dense':dense,'state':[conv(actions.state(a.shot,i/30)) for i in range(n)],'blend_sha256':hashlib.sha256(outblend.read_bytes()).hexdigest(),'source_sha256':hashes}
with gzip.open(outdata,'wt',compresslevel=6) as f:json.dump(data,f,separators=(',',':'))
print('EDITED_NATIVE_GEOMETRY_EXPORTED',outdata)
