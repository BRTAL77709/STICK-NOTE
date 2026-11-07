"""Retain M04 native skin; extend real native arm/finger IK; bake evaluated geometry."""
import bpy,sys,json,gzip,math,argparse,hashlib,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from bootstrap import ROOT
import actions
from cameras import camera
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--shot',required=True);p.add_argument('--tag',default='R01');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);shot=a.shot;dur=actions.DURATIONS[shot];n=round(dur*30);out=R/'blender'/f'{shot}_{a.tag}.blend';cache=R/'scenes'/f'{shot}_{a.tag}.json.gz';assert not out.exists() and not cache.exists();bpy.ops.wm.open_mainfile(filepath=str(R/'blender/BASELINE_M04.blend'));scene=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];scene.name='M11_'+shot;scene.frame_end=n-1;scene.render.fps=30;scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100
# Proper rotation mapping legacy Y-up coordinates into Blender Z-up: (z,x,y).
B=Matrix(((0,0,1),(1,0,0),(0,1,0)));Bt=B.transposed()
def V(q):return B@Vector(q)
def L(q):return [float(x) for x in q]
def empty(name):
 o=bpy.data.objects.new(name,None);scene.collection.objects.link(o);o.empty_display_size=.035;return o
for o in list(scene.objects):
 if o.type=='MESH' and not o.modifiers:bpy.data.objects.remove(o,do_unlink=True)
# Existing arm COPY_ROTATION is replaced by native IK; native connected rest bones and skin stay intact.
restq={name:b.matrix_local.to_quaternion() for name,b in rig.data.bones.items()};targets={};poles={};handcons={}
for s in ['L','R']:
 for prefix in ['upper_arm.','forearm.']:
  for c in list(rig.pose.bones[prefix+s].constraints):rig.pose.bones[prefix+s].constraints.remove(c)
 t=empty('M07_WRIST_'+s);pole=empty('M07_ELBOW_POLE_'+s);pb=rig.pose.bones['forearm.'+s];c=pb.constraints.new('IK');c.name='M07_NATIVE_ARM_IK_'+s;c.target=t;c.pole_target=pole;c.chain_count=2;c.iterations=128;c.use_stretch=False;targets[s]=t;poles[s]=pole;handcons[s]=c
 for pref in ['upper_arm.','forearm.']:rig.pose.bones[pref+s].ik_stretch=0
# Native thumb/index bones with fixed .034m phalanges, bound visible digit meshes.
bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for s in ['L','R']:
 hand=rig.data.edit_bones['hand.'+s]
 for j in range(2):
  start=hand.head.copy();mid=start+Vector((.025,(-1,1)[j]*.023,0));end=mid+Vector((.025,(-1,1)[j]*.023,0));mid=start+(mid-start).normalized()*.034;end=mid+(end-mid).normalized()*.034
  b=rig.data.edit_bones.new(f'digit{j}a.{s}');b.head=start;b.tail=mid;b.parent=hand;b.align_roll(Vector((0,0,1)));c=rig.data.edit_bones.new(f'digit{j}b.{s}');c.head=mid;c.tail=end;c.parent=b;c.use_connect=True;c.align_roll(Vector((0,0,1)))
bpy.ops.object.mode_set(mode='OBJECT');digits={}
for s in ['L','R']:
 for j in range(2):
  t=empty(f'M07_FINGERTIP_{j}_{s}');c=rig.pose.bones[f'digit{j}b.{s}'].constraints.new('IK');c.name='M07_NATIVE_DIGIT_IK';c.target=t;c.chain_count=2;c.use_stretch=False;c.iterations=64;digits[s,j]=t
  for pref in ['a','b']:
   name=f'digit{j}{pref}.{s}';b=rig.data.bones[name];A=b.head_local;D=b.tail_local-A;side=Vector((0,0,1))*.007;other=D.normalized().cross(side);verts=[tuple(A+D*u+side*x+other*y) for u in [0,1] for x,y in [(-1,-1),(1,-1),(1,1),(-1,1)]];faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update();o=bpy.data.objects.new('M07_'+name,m);scene.collection.objects.link(o);o['base_color']='#d1d7d2';g=o.vertex_groups.new(name=name);g.add(list(range(8)),1,'REPLACE');mod=o.modifiers.new('NATIVE_DIGIT_SKIN','ARMATURE');mod.object=rig
# Base approved head card basis; orient this illustrated plane with the native camera, not a detached glyph.
card=bpy.data.objects['APPROVED_HEAD_CARD'];vv=[v.co for v in card.data.vertices];right=(vv[1]-vv[0]).normalized();up=(vv[3]-vv[0]).normalized();normal=right.cross(up).normalized();cardbasis=Matrix((right,up,normal)).transposed()
controls={n:bpy.data.objects['CTRL_'+n] for n in ['pelvis','spine','chest','neck','head','hand.L','hand.R','foot.L','foot.R']};root=bpy.data.objects['CTRL_ROOT']
for o in [root,*controls.values(),bpy.data.objects['CTRL_ANKLE_L'],bpy.data.objects['CTRL_ANKLE_R'],bpy.data.objects['CTRL_KNEE_POLE_L'],bpy.data.objects['CTRL_KNEE_POLE_R']]:o.animation_data_clear()
states=[]
for i in range(n+1):
 t=min(dur-1e-6,i/30);d=actions.state(shot,t);pose=d['pose'];states.append(d);r=V(pose['root']);root.location=r;root.keyframe_insert('location',frame=i);torso=B@Matrix(pose['torso_basis'].tolist())@Bt;pelvis=B@Matrix(pose['pelvis_basis'].tolist())@Bt;rots={'pelvis':pelvis,'spine':torso,'chest':torso,'neck':Matrix.Identity(3)};cam=camera(shot,t,d);cr=V(cam.right).normalized();cu=V(cam.up).normalized();cn=cr.cross(cu).normalized();headrot=Matrix((cr,cu,cn)).transposed()@cardbasis.transposed();rots['head']=headrot
 worst=None
 for side,jj in [('L',1),('R',0)]:
  shoulder=r+torso@Vector((0,(-.19,.19)[jj==0],.50));direction=V(pose['arms'][jj]['wrist'])-shoulder
  if worst is None or direction.length>worst.length:worst=direction
 if worst.length>.662:
  horizontal=Vector((worst.x,worst.y,0))
  if horizontal.length>.001:
   axis=Vector((0,0,1)).cross(horizontal).normalized();angle=min(.055,(worst.length-.662)/.38);lean=Matrix.Rotation(angle,3,axis);rots['spine']=lean@torso;rots['chest']=lean@torso
 for s,j in [('L',1),('R',0)]:
  arm=pose['arms'][j];leg=pose['legs'][j];wr=V(arm['wrist']);elbow=V(arm['elbow']);shoulder=V(arm['shoulder']);pole=elbow+(elbow-(shoulder+wr)/2)*3
  targets[s].location=wr;poles[s].location=pole;targets[s].keyframe_insert('location',frame=i);poles[s].keyframe_insert('location',frame=i)
  bpy.data.objects['CTRL_ANKLE_'+s].location=V(leg['ankle']);bpy.data.objects['CTRL_ANKLE_'+s].keyframe_insert('location',frame=i)
  kneepole=V(leg['knee'])+(V(leg['knee'])-(V(leg['hip'])+V(leg['ankle']))/2)*4;bpy.data.objects['CTRL_KNEE_POLE_'+s].location=kneepole;bpy.data.objects['CTRL_KNEE_POLE_'+s].keyframe_insert('location',frame=i)
  footR=B@Matrix(actions.RY(leg.get('heading',0)).tolist())@Bt@Matrix.Rotation(-leg.get('pitch',0),3,'Y');rots['foot.'+s]=footR
  H=d.get('hand_frames',[None,None])[j];rots['hand.'+s]=torso if H is None else B@Matrix(np.asarray(H).tolist())@Bt
  groups=d.get('fingers',[[],[]])[j]
  for digit in range(2):
   point=groups[digit].get('tip_center',groups[digit]['pad']) if len(groups)>digit else np.asarray(arm['wrist'])+np.asarray(pose['torso_basis'])@np.array([(-1,1)[digit]*.015,-.050,.025]);digits[s,digit].location=V(point);digits[s,digit].keyframe_insert('location',frame=i)
 for name,m in rots.items():o=controls[name];o.rotation_mode='QUATERNION';o.rotation_quaternion=m.to_quaternion()@restq[name];o.keyframe_insert('rotation_quaternion',frame=i)
# Native solvers with constant pole calibration, no per-frame joint substitution.
scene.frame_set(0);bpy.context.view_layer.update()
for s,j in [('L',1),('R',0)]:
 wanted=V(states[0]['pose']['arms'][j]['elbow']);best=(1e9,0)
 for angle in [0,math.pi/2,-math.pi/2,math.pi]:
  handcons[s].pole_angle=angle;bpy.context.view_layer.update();cost=(rig.pose.bones['upper_arm.'+s].tail-wanted).length
  if cost<best[0]:best=(cost,angle)
 handcons[s].pole_angle=best[1]
 # Preserve no-stretch native legs but adapt their poles to each action's world direction.
 wanted=V(states[0]['pose']['legs'][j]['knee']);con=rig.pose.bones['shin.'+s].constraints['LEG_TWO_BONE_IK_'+s];best=(1e9,0)
 for angle in [0,math.pi/2,-math.pi/2,math.pi]:
  con.pole_angle=angle;bpy.context.view_layer.update();cost=(rig.pose.bones['thigh.'+s].tail-wanted).length
  if cost<best[0]:best=(cost,angle)
 con.pole_angle=best[1]
for o in scene.objects:
 if o.animation_data and o.animation_data.action:
  for fc in o.animation_data.action.fcurves:
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
# Native cinematic camera tracks the same source function used by illustrated output.
cam=scene.camera;cam.data.type='PERSP';cam.data.sensor_fit='HORIZONTAL';cam.data.sensor_width=36;cam.animation_data_clear()
for i,d in enumerate(states):
 c=camera(shot,i/30,d);cam.location=V(c.eye);cam.rotation_euler=(-V(c.forward)).to_track_quat('Z','Y').to_euler();cam.data.lens=c.focal/1080*36;cam.keyframe_insert('location',frame=i);cam.keyframe_insert('rotation_euler',frame=i);cam.data.keyframe_insert('lens',frame=i)
from embed_assets import build as embed_assets
embed_assets(scene,'DRIVING_COCKPIT' if shot in ['DISCOVERY','PANIC'] else 'WINDOW_CURTAIN' if shot in ['PHONE_CALL','UNKNOWN_CALLER'] else shot,states)
if shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:
 from embed_assets import cockpit_hierarchy
 cockpit_hierarchy(scene)
if shot=='WINDOW_CURTAIN':
 for o in [q for q in scene.objects if q.type=='MESH' and q.modifiers]:
  for i,d in enumerate(states):o.hide_render=bool(d.get('hide_actor',False));o.keyframe_insert('hide_render',frame=i)
from native_world_m11 import complete
complete(scene,shot,states)
scene['M07_source']='Existing M04 native rig; added native arm/digit IK. Controllers author targets, Blender evaluates final meshes.';scene['shot']=shot;scene.frame_set(0);bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
meshes=[o for o in scene.objects if o.type=='MESH' and o.modifiers];topology={o.name:{'faces':[list(f.vertices) for f in o.data.polygons],'color':o.get('base_color','#294653')} for o in meshes}
def sample(t,full):
 fr=t*30;floor=math.floor(fr);scene.frame_set(floor,subframe=fr-floor);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(dep);bones={n:{'head':L(er.matrix_world@b.head),'tail':L(er.matrix_world@b.tail)} for n,b in er.pose.bones.items()};data={'time':t,'bones':bones,'targets':{s:L(targets[s].matrix_world.translation) for s in ['L','R']},'finger_targets':{s:[L(digits[s,j].matrix_world.translation) for j in range(2)] for s in ['L','R']}}
 if full:
  data['meshes']={}
  for o in meshes:
   ev=o.evaluated_get(dep);m=ev.to_mesh();data['meshes'][o.name]=[L(ev.matrix_world@v.co) for v in m.vertices];ev.to_mesh_clear()
 else:
  data['shoes']={}
  for s in ['L','R']:
   o=bpy.data.objects['SHOE_'+s];ev=o.evaluated_get(dep);m=ev.to_mesh();data['shoes'][s]=[L(ev.matrix_world@v.co) for v in m.vertices];ev.to_mesh_clear()
 return data
frames=[sample(i/30,True) for i in range(n)];dense=[sample(i/60,False) for i in range(round(dur*60))];scene.frame_set(0)
def conv(q):
 if isinstance(q,np.ndarray):return q.tolist()
 if isinstance(q,np.generic):return q.item()
 if isinstance(q,dict):return {k:conv(v) for k,v in q.items()}
 if isinstance(q,(list,tuple)):return [conv(v) for v in q]
 return q
with gzip.open(cache,'wt',compresslevel=6) as f:json.dump({'shot':shot,'duration':dur,'fps':30,'topology':topology,'frames':frames,'dense':dense,'state':[conv(s) for s in states[:-1]],'blend_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').rglob('*.py')}},f,separators=(',',':'))
print('NATIVE_BAKED',shot,n,flush=True)
