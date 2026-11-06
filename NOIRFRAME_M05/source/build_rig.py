"""Native Blender armature is the evaluated animation source, not an editing companion.
Run: blender -b --factory-startup -t 2 --python source/build_rig.py -- --tag R03 --quick
"""
import bpy,bmesh,sys,json,math,gzip,hashlib,argparse
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--tag',default='R03');parser.add_argument('--quick',action='store_true');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);planfile=R/'assets'/f'CONTROLS_{args.tag}.json';plan=json.loads(planfile.read_text());root0=Vector(plan['frames'][0]['root']);NAMES=['L','R'];MATERIALS={};meshes=[];shoe_objects={}
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.name='NOIRFRAME_M04_STAIRS';scene.render.fps=30;scene.frame_start=0;scene.frame_end=149;scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.render.resolution_percentage=100;scene.world.color=(.018,.035,.055);scene['animation_type']='Authored kinematic armature; Blender native IK and skinned meshes. No force simulation.'

def material(col):
 if col not in MATERIALS:
  m=bpy.data.materials.new(col);h=col.lstrip('#');m.diffuse_color=tuple(int(h[i:i+2],16)/255 for i in (0,2,4))+(1,);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=m.diffuse_color;bs.inputs['Roughness'].default_value=1;MATERIALS[col]=m
 return MATERIALS[col]
def empty(name,point=(0,0,0)):
 o=bpy.data.objects.new(name,None);scene.collection.objects.link(o);o.location=point;o.empty_display_type='SPHERE';o.empty_display_size=.035;return o

def mesh_object(name,verts,faces,col,weights=None):
 m=bpy.data.meshes.new(name+'_mesh');m.from_pydata(verts,[],faces);m.update();bm=bmesh.new();bm.from_mesh(m);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(m);bm.free();o=bpy.data.objects.new(name,m);scene.collection.objects.link(o);m.materials.append(material(col));o['ink_color']='#06121c';o['base_color']=col
 if weights:
  groups={n:o.vertex_groups.new(name=n) for n in sorted({n for w in weights for n in w})}
  for i,w in enumerate(weights):
   for n,value in w.items():groups[n].add([i],value,'REPLACE')
  mod=o.modifiers.new('ACTUAL_CHARACTER_SKIN','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
 meshes.append(o);return o

def rest_knee(hip,ank,l=.37):
 u=ank-hip;d=u.length;u.normalize();pole=Vector((0,-1,0)).cross(u).normalized();return hip+u*d/2+pole*math.sqrt(l*l-d*d/4)
# Genuine connected bone hierarchy. Metres, Blender Z up, +X ascent.
arm=bpy.data.armatures.new('M04_WITNESS_SKELETON');rig=bpy.data.objects.new('M04_WITNESS_RIG',arm);scene.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT');B={}
def bone(name,head,tail,parent=None,connected=False):
 b=arm.edit_bones.new(name);b.head=head;b.tail=tail
 if parent:b.parent=B[parent];b.use_connect=connected
 b.align_roll(Vector((0,1,0)));B[name]=b;return b
bone('root',root0,root0+Vector((0,0,.10)))
bone('pelvis',root0,root0+Vector((0,0,.12)),'root')
bone('spine',root0,root0+Vector((0,0,.28)),'pelvis')
bone('chest',root0+Vector((0,0,.28)),root0+Vector((0,0,.50)),'spine',True)
bone('neck',root0+Vector((0,0,.50)),root0+Vector((0,0,.79)),'chest',True)
bone('head',root0+Vector((0,0,.79)),root0+Vector((0,0,.89)),'neck',True)
rest_legs={}
for j,s in enumerate(NAMES):
 hip=root0+Vector((0,(-.07,.07)[j],0));ank=Vector(plan['frames'][0]['feet'][j]['ankle']);knee=rest_knee(hip,ank);rest_legs[s]=(hip,knee,ank)
 bone('thigh.'+s,hip,knee,'pelvis');bone('shin.'+s,knee,ank,'thigh.'+s,True);bone('foot.'+s,ank,ank+Vector((.080,0,0)),'shin.'+s,True);bone('toe.'+s,ank+Vector((.080,0,0)),ank+Vector((.145,0,0)),'foot.'+s,True)
 shoulder=root0+Vector((0,(-.19,.19)[j],.50));elbow=shoulder+Vector((0,(-.028,.028)[j],-math.sqrt(.34**2-.028**2)));wrist=elbow+Vector((.34*math.sin(math.radians(22)),0,-.34*math.cos(math.radians(22))))
 bone('upper_arm.'+s,shoulder,elbow,'chest');bone('forearm.'+s,elbow,wrist,'upper_arm.'+s,True);direction=(wrist-elbow).normalized();bone('hand.'+s,wrist,wrist+direction*.075,'forearm.'+s,True)
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True;arm.display_type='OCTAHEDRAL'
restq={n:b.matrix_local.to_quaternion() for n,b in arm.bones.items()};controls={};qcontrols={}
rootctrl=empty('CTRL_ROOT',root0);c=rig.pose.bones['root'].constraints.new('COPY_LOCATION');c.name='WORLD_ROOT_POSITION';c.target=rootctrl;c.owner_space='WORLD';c.target_space='WORLD'

def rot_control(name):
 o=empty('CTRL_'+name);o.rotation_mode='QUATERNION';qcontrols[name]=o;con=rig.pose.bones[name].constraints.new('COPY_ROTATION');con.name='WORLD_ORIENTATION_'+name;con.target=o;con.owner_space='WORLD';con.target_space='WORLD';return o
for name in ['pelvis','spine','chest','neck','head']+[p+'.'+s for s in NAMES for p in ['upper_arm','forearm','hand','foot']]:rot_control(name)
ikcons={}
for j,s in enumerate(NAMES):
 target=empty('CTRL_ANKLE_'+s,plan['frames'][0]['feet'][j]['ankle']);pole=empty('CTRL_KNEE_POLE_'+s,root0+Vector((.8,(-.09,.09)[j],-.20)));controls[s]=(target,pole);pb=rig.pose.bones['shin.'+s];con=pb.constraints.new('IK');con.name='LEG_TWO_BONE_IK_'+s;con.target=target;con.pole_target=pole;con.chain_count=2;con.iterations=128;con.use_stretch=False;con.use_tail=True;ikcons[s]=con
 for n in ['thigh.'+s,'shin.'+s]:rig.pose.bones[n].ik_stretch=0.
 pb.lock_ik_x=True;pb.lock_ik_y=True;pb.lock_ik_z=False
# Exact cubic-root curves: handles encode derivatives in seconds, preserving C2 authoring.
rootctrl.animation_data_create();action=bpy.data.actions.new('M04_ROOT_C2_SUPPORT_POSES');rootctrl.animation_data.action=action
for axis in range(3):
 fc=action.fcurves.new(data_path='location',index=axis);keys=plan['root_keys'];fc.keyframe_points.add(len(keys))
 for i,(kp,k) in enumerate(zip(fc.keyframe_points,keys)):
  t=k['time'];value=k['value'][axis];slope=k['derivative'][axis];left=(t-keys[i-1]['time']) if i else (keys[1]['time']-t);right=(keys[i+1]['time']-t) if i<len(keys)-1 else left;kp.co=(t*30,value);kp.handle_left_type='FREE';kp.handle_right_type='FREE';kp.handle_left=(t*30-left*10,value-slope*left/3);kp.handle_right=(t*30+right*10,value+slope*right/3);kp.interpolation='BEZIER'
 fc.update()

# Native controller keys for foot locks, joint rotations and pole motion; no per-frame analytic limb solver.
for f in plan['frames']:
 frame=f['time']*30;r=Vector(f['root']);pelvisR=Matrix.Rotation(f['pelvis_roll'],4,'X');spineR=Matrix.Rotation(f['spine_pitch'],4,'Y')@Matrix.Rotation(-f['pelvis_roll']*.4,4,'X');chestR=Matrix.Rotation(f['chest_twist'],4,'Z')@Matrix.Rotation(f['chest_pitch'],4,'Y')@Matrix.Rotation(-f['pelvis_roll']*.6,4,'X');headR=Matrix.Rotation(f['head_pitch'],4,'Y')
 rotations={'pelvis':pelvisR,'spine':spineR,'chest':chestR,'neck':headR,'head':headR}
 for j,s in enumerate(NAMES):
  rotations['upper_arm.'+s]=chestR@Matrix.Rotation(f['arm_swing'][j],4,'Y');rotations['forearm.'+s]=chestR@Matrix.Rotation(f['arm_swing'][j]+f['elbow_extra'][j],4,'Y');rotations['hand.'+s]=chestR@Matrix.Rotation(f['arm_swing'][j]+f['elbow_extra'][j]*.65,4,'Y');rotations['foot.'+s]=Matrix.Rotation(-f['feet'][j]['pitch'],4,'Y')
  target,pole=controls[s];target.location=f['feet'][j]['ankle'];pole.location=(r.x+.85,(-.09,.09)[j],r.z-.24);target.keyframe_insert('location',frame=frame);pole.keyframe_insert('location',frame=frame)
 for name,m in rotations.items():o=qcontrols[name];o.rotation_quaternion=m.to_quaternion()@restq[name];o.keyframe_insert('rotation_quaternion',frame=frame)
for o in list(qcontrols.values())+[o for pair in controls.values() for o in pair]:
 if o.animation_data and o.animation_data.action:
  for fc in o.animation_data.action.fcurves:
   for kp in fc.keyframe_points:kp.interpolation='LINEAR'
scene.frame_set(0);bpy.context.view_layer.update()
# Constant pole-angle calibration against the rest bend plane. This is not per-frame pose substitution.
calibration={}
for s in NAMES:
 best=None
 for angle in [0,math.pi/2,-math.pi/2,math.pi]:
  ikcons[s].pole_angle=angle;bpy.context.view_layer.update();knee=rig.pose.bones['thigh.'+s].tail;cost=(knee-rest_legs[s][1]).length
  if best is None or cost<best[0]:best=(cost,angle)
 ikcons[s].pole_angle=best[1];calibration[s]={'pole_angle_rad':best[1],'rest_knee_error_m':best[0]}
 # Limit the hinge relative to the authored rest bend: 5..135 degrees flexion.
 hip,knee,ank=rest_legs[s];restflex=math.pi-(hip-knee).angle(ank-knee);pb=rig.pose.bones['shin.'+s];pb.use_ik_limit_z=True;pb.ik_min_z=math.radians(5)-restflex;pb.ik_max_z=math.radians(135)-restflex
bpy.context.view_layer.update()

# Bound meshes, rather than reconstructing a tube/box from target arrays each frame.
def capsule(name,bone_name,radius,col,end_radius=None):
 b=arm.bones[bone_name];a=b.head_local;tail=b.tail_local;axis=(tail-a).normalized();side=Vector((0,1,0));side=(side-axis*side.dot(axis)).normalized();other=axis.cross(side).normalized();length=(tail-a).length;verts=[];N=8
 for along,rad in [(-radius*.6,radius*.35),(0,radius),(length*.82,(end_radius or radius)),(length,(end_radius or radius)),(length+radius*.5,radius*.3)]:
  for j in range(N):verts.append(tuple(a+axis*along+(side*math.cos(j*math.tau/N)+other*math.sin(j*math.tau/N))*rad))
 faces=[tuple(reversed(range(N)))]+[(i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j) for i in range(4) for j in range(N)]+[tuple(4*N+j for j in range(N))]
 return mesh_object(name,verts,faces,col,[{bone_name:1.} for v in verts])
for s in NAMES:
 capsule('TROUSER_THIGH_'+s,'thigh.'+s,.0525,'#263e4b');capsule('TROUSER_SHIN_'+s,'shin.'+s,.050,'#1b3343');capsule('SLEEVE_UPPER_'+s,'upper_arm.'+s,.051,'#294653');capsule('SLEEVE_LOWER_'+s,'forearm.'+s,.047,'#294653',.028);capsule('MITTEN_'+s,'hand.'+s,.030,'#d1d7d2',.024)
# Rounded, weighted hoodie rings; vertex weights interpolate pelvis/spine/chest.
verts=[];weights=[];rings=[(-.06,.100,.175),(0,.115,.180),(.16,.120,.180),(.32,.125,.190),(.46,.112,.195),(.51,.100,.130)];N=12
for z,rx,ry in rings:
 for j in range(N):
  a=j*math.tau/N;verts.append(tuple(root0+Vector((rx*math.cos(a),ry*math.sin(a),z))))
  if z<.12:u=max(0,z/.12);w={'pelvis':1-u,'spine':u}
  elif z<.32:u=(z-.12)/.20;w={'spine':1-u,'chest':u}
  else:w={'chest':1.}
  weights.append({k:v for k,v in w.items() if v>0})
faces=[tuple(reversed(range(N)))]+[(i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j) for i in range(len(rings)-1) for j in range(N)]+[tuple((len(rings)-1)*N+j for j in range(N))];mesh_object('WEIGHTED_APPROVED_HOODIE',verts,faces,'#233f4d',weights)
# Approved shoe profile, actual skin binding. Two lowest vertices per side are contact samples.
for j,s in enumerate(NAMES):
 sole=Vector(plan['initial'][j]);profile=plan['shoe_profile'];vv=[tuple(sole+Vector((x,side,z))) for side in [-.045,.045] for x,z in profile];ff=[tuple(reversed(range(5))),tuple(range(5,10))]+[(i,(i+1)%5,(i+1)%5+5,i+5) for i in range(5)];o=mesh_object('SHOE_'+s,vv,ff,'#142733',[{'foot.'+s:1.} for v in vv]);o['sole_contact_vertices']=[0,1,5,6];o['toe_contact_vertices']=[1,6];shoe_objects[s]=o

# Static stair solids and unobstructed far railing. Three .18m risers, .30m run.
def box(name,x,y,z,dx,dy,dz,col):
 vv=[(x+i*dx,y+j*dy,z+k*dz) for i,j,k in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]];ff=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];return mesh_object(name,vv,ff,col)
box('LOWER_FLOOR',-1.2,-.5,-.10,1.2,1.,.10,'#263b43')
box('TREAD_1',0,-.45,0,.30,.90,.18,'#56616a');box('TREAD_2',.30,-.45,0,.30,.90,.36,'#56616a');box('TREAD_3_LANDING',.60,-.45,0,1.,.90,.54,'#56616a');box('WALL',-1.2,.68,0,3.,.05,3.05,'#243e4b');box('CEILING',-1.2,-.45,3.05,3.,1.18,.04,'#182f3c')
for i,(x,z) in enumerate([(0,.18),(.3,.36),(.6,.54),(1.3,.54)]):box('FAR_RAIL_POST_'+str(i),x,.48,z,.025,.025,.73,'#667e86')
# Rail as a narrow mesh beam, not a near-side occluder.
def beam(name,a,b,width,col):
 a=Vector(a);b=Vector(b);axis=(b-a).normalized();s=Vector((0,1,0))*width/2;u=axis.cross(Vector((0,1,0)))*width/2;v=[tuple(p+s*ds+u*du) for p in [a,b] for ds,du in [(-1,-1),(1,-1),(1,1),(-1,1)]];return mesh_object(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],col)
beam('FAR_HANDRAIL',(0,.49,.90),(.60,.49,1.26),.045,'#b4a47f');beam('LANDING_HANDRAIL',(.60,.49,1.26),(1.45,.49,1.26),.045,'#b4a47f')
box('AMBER_WALL_LIGHT',1.45,.62,2.15,.10,.04,.22,'#d8ad70')
# Native camera is also exported; the illustrative renderer must match this projection.
cd=bpy.data.cameras.new('M04_FIXED_CAMERA');camera=bpy.data.objects.new('M04_FIXED_CAMERA',cd);scene.collection.objects.link(camera);camera.location=(2.5,-6.5,2.1);target=Vector((.40,0,1.15));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=3.30;scene.camera=camera
# Static camera is intentional: no cuts, shake or motion blur conceal contact.
scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.film_transparent=False
# One directional area light for a usable editable Blender scene (final style renderer uses flat cel tones).
ld=bpy.data.lights.new('AMBER_KEY','AREA');lo=bpy.data.objects.new('AMBER_KEY',ld);scene.collection.objects.link(lo);lo.location=(-1.5,-2,3);lo.rotation_euler=(root0-lo.location).to_track_quat('-Z','Y').to_euler();ld.energy=180;ld.color=(1.,.70,.38);ld.shape='DISK';ld.size=3.

# Approved drawn head is genuinely bound to the head bone in the editable scene.
bpy.context.view_layer.update();right=camera.matrix_world.to_3x3()@Vector((1,0,0));up=camera.matrix_world.to_3x3()@Vector((0,1,0));center=root0+Vector((0,0,.79));half=600*.26/(61*2.62)/2
card=mesh_object('APPROVED_HEAD_CARD',[tuple(center-right*half-up*half),tuple(center+right*half-up*half),tuple(center+right*half+up*half),tuple(center-right*half+up*half)],[(0,1,2,3)],'#d1d7d2',[{'head':1.}]*4)
uv=card.data.uv_layers.new(name='APPROVED_HEAD_UV')
for loop in card.data.loops:uv.data[loop.index].uv=[(0,0),(1,0),(1,1),(0,1)][loop.vertex_index]
image=bpy.data.images.load(str(R/'assets/APPROVED_HEAD.png'));image.pack();mat=bpy.data.materials.new('APPROVED_ILLUSTRATED_HEAD');mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear();tex=nodes.new('ShaderNodeTexImage');tex.image=image;em=nodes.new('ShaderNodeEmission');tr=nodes.new('ShaderNodeBsdfTransparent');mix=nodes.new('ShaderNodeMixShader');out=nodes.new('ShaderNodeOutputMaterial');links=mat.node_tree.links;links.new(tex.outputs['Color'],em.inputs['Color']);links.new(tex.outputs['Alpha'],mix.inputs[0]);links.new(tr.outputs[0],mix.inputs[1]);links.new(em.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],out.inputs['Surface']);card.data.materials.clear();card.data.materials.append(mat);scene['controls_filename']=planfile.name;scene['pole_calibration']=json.dumps(calibration)

# Export actual dependency-graph meshes and bones. Blender evaluation is authoritative.
def set_time(t):
 fr=t*30;scene.frame_set(math.floor(fr+1e-9),subframe=fr-math.floor(fr+1e-9));bpy.context.view_layer.update()
def V(v):return [float(x) for x in v]
def evaluated_mesh(o,deps):
 ev=o.evaluated_get(deps);m=ev.to_mesh();verts=[V(ev.matrix_world@v.co) for v in m.vertices];ev.to_mesh_clear();return verts

def sample(t,full=False):
 set_time(t);deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);bones={n:{'head':V(er.matrix_world@b.head),'tail':V(er.matrix_world@b.tail),'matrix':[[float(x) for x in row] for row in (er.matrix_world@b.matrix)]} for n,b in er.pose.bones.items()};findex=min(len(plan['frames'])-1,round(t*plan['rate']));f=plan['frames'][findex];feet={}
 for j,s in enumerate(NAMES):
  vv=evaluated_mesh(shoe_objects[s],deps);feet[s]={'vertices':vv,'sole_indices':[0,1,5,6],'toe_indices':[1,6],'target':f['feet'][j],'ankle_target':V(controls[s][0].matrix_world.translation)}
 d={'time':t,'bones':bones,'feet':feet}
 if full:d['meshes']={o.name:evaluated_mesh(o,deps) for o in meshes if o.modifiers}
 return d
# Probe both feet before expensive full export, and keep the .blend independently inspectable.
quick=[]
for t in [0,.8,1.2,1.8,2.23,2.8,3.26,3.9,4.5,149/30]:quick.append(sample(t,True))
source_sha={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').glob('*.py')};metadata={'blender_version':bpy.app.version_string,'calibration':calibration,'bones':{n:{'parent':b.parent.name if b.parent else None,'connected':b.use_connect,'rest_length_m':b.length,'constraints':[{'name':c.name,'type':c.type,'target':c.target.name if hasattr(c,'target') and c.target else None,'chain_count':c.chain_count if c.type=='IK' else None,'use_stretch':c.use_stretch if c.type=='IK' else None} for c in rig.pose.bones[n].constraints]} for n,b in arm.bones.items()},'skin_modifiers':{o.name:[{'type':m.type,'object':m.object.name if m.type=='ARMATURE' else None} for m in o.modifiers] for o in meshes if o.modifiers},'controller_sha256':hashlib.sha256(planfile.read_bytes()).hexdigest(),'source_sha256':source_sha}
(R/'reports'/f'RIG_MANIFEST_{args.tag}.json').write_text(json.dumps(metadata,indent=2))
# Mesh topology/materials stored once, meshes for animation frames are evaluated above.
mesh_meta={o.name:{'faces':[[int(i) for i in p.vertices] for p in o.data.polygons],'color':o['base_color'],'bound_to_armature':bool(o.modifiers),'rest_vertices':[V(o.matrix_world@v.co) for v in o.data.vertices]} for o in meshes};cm=camera.matrix_world;camera_data={'eye':V(cm.translation),'right':V(cm.to_3x3()@Vector((1,0,0))),'up':V(cm.to_3x3()@Vector((0,1,0))),'forward':V(cm.to_3x3()@Vector((0,0,-1))),'ortho_scale':cd.ortho_scale}
set_time(0);blend=R/'assets'/f'STAIRCASE_M04_{args.tag}.blend';assert not blend.exists();bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True)
if args.quick:
 with gzip.open(R/'reports'/f'QUICK_{args.tag}.json.gz','wt') as fp:json.dump({'metadata':metadata,'camera':camera_data,'meshes':mesh_meta,'frames':quick},fp,separators=(',',':'))
 print('QUICK_COMPLETE',blend,flush=True)
else:
 frames=[sample(i/30,True) for i in range(150)];dense=[sample(i/120,False) for i in range(601)];jumps=[]
 for key in plan['root_keys'][1:-1]:
  t=key['time'];jumps.append({'time':t,'before':sample(t-1e-5)['bones']['root']['head'],'after':sample(t+1e-5)['bones']['root']['head'],'center':sample(t)['bones']['root']['head']})
 # Causal mutation proof: disabling actual IK must change the bound shoe/limb evaluation.
 baseline=sample(2.,True);ikcons['L'].influence=0.;mutation=sample(2.,True);ikcons['L'].influence=1.;set_time(0)
 with gzip.open(R/'assets'/f'EVALUATED_{args.tag}.json.gz','wt',compresslevel=6) as fp:json.dump({'metadata':metadata,'camera':camera_data,'meshes':mesh_meta,'frames':frames,'dense':dense,'root_key_probes':jumps,'ik_mutation':{'baseline':baseline,'disabled_left_IK':mutation},'blend_sha256':hashlib.sha256(blend.read_bytes()).hexdigest()},fp,separators=(',',':'))
 print('FULL_EVALUATION_COMPLETE',blend,flush=True)
