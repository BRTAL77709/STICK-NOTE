"""Open the actual delivered M04 blend; retain its armature, constraints and skin bindings.
No bones or character meshes are rebuilt. Only acting controls, set and camera are edited.
"""
import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];src=R.parent/'NOIRFRAME_M04/assets/STAIRCASE_M04_R06.blend';bpy.ops.wm.open_mainfile(filepath=str(src));scene=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];plan=json.loads((R/'assets/CONTROLS_POLISH_A02.json').read_text());scene['controls_filename']='CONTROLS_POLISH_A02.json';scene.name='HOUSE17_M05_EXISTING_M04_RIG';scene['M04_source_sha256']=hashlib.sha256(src.read_bytes()).hexdigest();restq={n:b.matrix_local.to_quaternion() for n,b in rig.data.bones.items()}
def rig_snapshot():return {'bones':{n:{'head':list(b.head_local),'tail':list(b.tail_local),'parent':b.parent.name if b.parent else None,'connected':b.use_connect,'length':b.length} for n,b in rig.data.bones.items()},'constraints':{n:[{'type':c.type,'name':c.name,'target':c.target.name if hasattr(c,'target') and c.target else None,'pole':c.pole_target.name if c.type=='IK' else None,'pole_angle':c.pole_angle if c.type=='IK' else None,'chain':c.chain_count if c.type=='IK' else None,'stretch':c.use_stretch if c.type=='IK' else None} for c in pb.constraints] for n,pb in rig.pose.bones.items()},'bindings':{o.name:[(m.type,m.object.name if m.type=='ARMATURE' else '') for m in o.modifiers] for o in scene.objects if o.type=='MESH' and o.modifiers}}
before=rig_snapshot();root=bpy.data.objects['CTRL_ROOT'];root.animation_data_clear();root.animation_data_create();act=bpy.data.actions.new('M05_C2_ROOT_ANTICIPATION_STEP_SETTLES');root.animation_data.action=act
for axis in range(3):
 fc=act.fcurves.new(data_path='location',index=axis);keys=plan['root_keys'];fc.keyframe_points.add(len(keys))
 for i,(kp,k) in enumerate(zip(fc.keyframe_points,keys)):
  t=k['time'];v=k['value'][axis];d=k['derivative'][axis];left=t-keys[i-1]['time'] if i else keys[1]['time']-t;right=keys[i+1]['time']-t if i<len(keys)-1 else left;kp.co=(30*t,v);kp.handle_left_type=kp.handle_right_type='FREE';kp.handle_left=(30*t-left*10,v-d*left/3);kp.handle_right=(30*t+right*10,v+d*right/3);kp.interpolation='BEZIER'
 fc.update()
names=['pelvis','spine','chest','neck','head']+[b+'.'+s for s in ['L','R'] for b in ['upper_arm','forearm','hand']]
for n in names:bpy.data.objects['CTRL_'+n].animation_data_clear()
for f in plan['frames']:
 t=f['time'];pelvis=Matrix.Rotation(f['pelvis_twist'],4,'Z')@Matrix.Rotation(f['pelvis_roll'],4,'X');spine=Matrix.Rotation(f['spine_pitch'],4,'Y')@Matrix.Rotation(-f['pelvis_roll']*.4,4,'X');chest=Matrix.Rotation(f['chest_twist'],4,'Z')@Matrix.Rotation(f['chest_pitch'],4,'Y')@Matrix.Rotation(-f['pelvis_roll']*.65,4,'X');head=Matrix.Rotation(f['head_yaw'],4,'Z')@Matrix.Rotation(f['head_pitch'],4,'Y');rots={'pelvis':pelvis,'spine':spine,'chest':chest,'neck':head,'head':head}
 for j,s in enumerate(['L','R']):
  rots['upper_arm.'+s]=chest@Matrix.Rotation(f['arm_swing'][j],4,'Y');rots['forearm.'+s]=chest@Matrix.Rotation(f['arm_swing'][j]+f['elbow_extra'][j],4,'Y');rots['hand.'+s]=chest@Matrix.Rotation(f['arm_swing'][j]+f['elbow_extra'][j]*.65,4,'Y')
 for n,m in rots.items():o=bpy.data.objects['CTRL_'+n];o.rotation_quaternion=m.to_quaternion()@restq[n];o.keyframe_insert('rotation_quaternion',frame=t*30)
for n in names:
 for fc in bpy.data.objects['CTRL_'+n].animation_data.action.fcurves:
  for k in fc.keyframe_points:k.interpolation='LINEAR'
# Preserve feet, ankle controllers and knee poles verbatim. Native IK resolves the altered pelvis.
assert before==rig_snapshot()
(R/'reports/RIG_RETENTION.json').write_text(json.dumps({'opened_actual_baseline':str(src),'baseline_sha256':scene['M04_source_sha256'],'bones_constraints_bindings_identical':before==rig_snapshot(),'snapshot':before},indent=2))
# Keep the tread solids unchanged; replace the prototype set around them.
for o in list(scene.objects):
 if o.type=='MESH' and not o.modifiers and o.name not in {'LOWER_FLOOR','TREAD_1','TREAD_2','TREAD_3_LANDING'}:bpy.data.objects.remove(o,do_unlink=True)
materials={}
def mesh(name,v,f,col):
 data=bpy.data.meshes.new(name+'_MESH');data.from_pydata(v,[],f);data.update();bm=bmesh.new();bm.from_mesh(data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(data);bm.free();o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o['base_color']=col
 if col not in materials:
  mat=bpy.data.materials.new(col);h=col[1:];mat.diffuse_color=tuple(int(h[i:i+2],16)/255 for i in (0,2,4))+(1,);materials[col]=mat
 data.materials.append(materials[col]);return o
faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box(n,x,y,z,dx,dy,dz,c):return mesh(n,[(x+i*dx,y+j*dy,z+k*dz) for i,j,k in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]],faces,c)
def beam(n,a,b,width,c):
 a=Vector(a);b=Vector(b);axis=(b-a).normalized();v=Vector((0,1,0))*width/2;u=axis.cross(Vector((0,1,0)))*width/2;return mesh(n,[tuple(p+v*s+u*t) for p in [a,b] for s,t in [(-1,-1),(1,-1),(1,1),(-1,1)]],faces,c)
# Room shell, upper hallway behind a real open portal.
box('HOUSE17_BACK_WALL_LEFT',-1.6,.78,0,2.58,.10,3.05,'#344d55');box('HOUSE17_BACK_WALL_RIGHT',1.79,.78,0,.91,.10,3.05,'#344d55');box('HOUSE17_PORTAL_HEADER',0.98,.78,2.40,.81,.10,.65,'#344d55')
box('HOUSE17_CEILING',-1.6,-.8,3.05,4.3,1.68,.08,'#25383e');box('HOUSE17_LEFT_WALL',-1.6,-.8,0,.10,1.58,3.05,'#233d49');near=box('HOUSE17_NEAR_WALL_CUTAWAY',-1.6,-.90,0,4.3,.08,3.05,'#243c47');near.hide_render=True;near['illustration_hidden']=True
box('HALLWAY_FLOOR',1.1,.45,.48,1.5,2.8,.06,'#6b5d4c');box('HALLWAY_FAR_WALL',1.1,3.15,.54,1.5,.1,2.5,'#142f3d');box('HALLWAY_LEFT_WALL',1.15,.89,.54,.1,2.3,2.5,'#203e49');box('HALLWAY_RIGHT_WALL',2.50,.89,.54,.1,2.3,2.5,'#203b45');box('HALLWAY_CEILING',1.15,.89,3.0,1.45,2.3,.05,'#182b34')
for x in [.94,1.76]:box('PORTAL_JAMB_'+str(x),x,.68,.54,.07,.17,1.9,'#98764b')
box('PORTAL_TOP',.94,.68,2.40,.89,.17,.07,'#b28a56');box('HALL_DOOR',1.50,3.08,.55,.8,.035,1.84,'#35484c')
for z in [.70,1.12]:box('HALL_DOOR_PANEL_'+str(z),1.59,3.055,z,.61,.015,.65,'#253c46')
box('HALL_HANDLE',2.14,3.01,1.35,.07,.05,.035,'#c09553')
# Wainscot, base/crown trim and wooden panels, never placed across visible feet.
for z,height,col in [(0,.12,'#142b35'),(.84,.055,'#806b50'),(.92,.025,'#c1a477'),(2.94,.07,'#806b50')]:box('WALL_TRIM_'+str(z),-1.5,.64,z,2.70,.13,height,col)
for x in [-1.38,-.92,-.46,0,.46,.92]:
 box('WAINSCOT_STILE_'+str(x),x,.65,.15,.025,.09,.64,'#45606a')
box('WAINSCOT_RAIL',-1.5,.65,.15,2.70,.09,.035,'#4d6670')
# Stair wood caps stay coplanar with verified solid contacts: decorative side nosings only.
for i,(x,z) in enumerate([(0,.18),(.3,.36),(.6,.54)]):
 box('NOSING_FAR_'+str(i),x,.455,z-.027,.30,.025,.025,'#ba9562');box('RISER_INLAY_'+str(i),x-.001,-.44,z-.12,.001,.88,.025,'#8c7557')
 for y in [-.20,.10,.40]:box('TREAD_GRAIN_'+str(i)+'_'+str(y),x+.03,y,z+.0001,.24,.002,.0001,'#8b806a')
beam('OAK_STRINGER',(-.08,.49,.02),(.64,.49,.46),.10,'#4f4033')
for i in range(7):
 x=i*.12;z=min(.54,.18+.60*x);box('BALUSTER_'+str(i),x,.50,z,.022,.022,(1.0+.37/.65*(x+.02) if x<=.63 else 1.37)-z,'#59717a')
for i,(x,z) in enumerate([(-.02,.18),(.63,.54),(1.20,.54)]):
 box('NEWEL_'+str(i),x,.48,z,.055,.07,.83,'#65513c');box('NEWEL_CAP_'+str(i),x-.015,.465,z+.83,.085,.10,.035,'#b79461')
beam('OAK_ASCENT_HANDRAIL',(-.02,.515,1.00),(.63,.515,1.37),.065,'#c09d6c');beam('OAK_LANDING_HANDRAIL',(.63,.515,1.37),(1.25,.515,1.37),.065,'#c09d6c')
# Architectural shadow shapes on the far wall, in world space behind the actor.
mesh('CEILING_CAST_SHADOW',[(-1.5,.635,2.94),(1.18,.635,2.94),(1.18,.635,2.72),(-1.5,.635,2.54)],[(0,1,2,3)],'#253d47')
# Two amber lamps and restrained geometric art.
for idx,(x,z) in enumerate([(-.67,2.02),(.80,2.37)]):
 box('SCONCE_BACK_'+str(idx),x-.065,.58,z-.17,.13,.09,.34,'#192b34');box('SCONCE_GLOW_'+str(idx),x-.048,.53,z-.105,.096,.04,.21,'#ffd393');box('SCONCE_CAP_'+str(idx),x-.085,.51,z+.105,.17,.12,.035,'#a88753')
 ld=bpy.data.lights.new('HOUSE17_AMBER_'+str(idx),'AREA');lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.location=(x,.30,z);lo.rotation_euler=(Vector((x,-.3,z-.4))-lo.location).to_track_quat('-Z','Y').to_euler();ld.energy=65;ld.color=(1,.63,.29);ld.size=.5
box('PORTRAIT_FRAME',-.1,.59,1.48,.47,.06,.64,'#a2865a');box('PORTRAIT_MAT',-.06,.555,1.52,.39,.025,.56,'#adac99');box('PORTRAIT_ART',-.02,.53,1.57,.31,.015,.46,'#24434e');beam('PORTRAIT_ILLUSTRATION',(.0,.51,1.63),(.25,.51,1.92),.018,'#87918a')
# Native moving camera follows ascent gently. Orthographic scale stays fixed, no zoom/cuts/shake.
cam=scene.camera;cam.name='M05_CINEMATIC_CAMERA';cam.data.ortho_scale=3.72;cam.animation_data_clear()
def s5(x):x=max(0,min(1,x));return x*x*x*(10-15*x+6*x*x)
for i in range(151):
 t=i/30;u=s5(t/5);target=Vector((.36+.22*u,0,1.29+.18*u));cam.location=target+Vector((1.65,-6.8,.72));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=i);cam.keyframe_insert('rotation_euler',frame=i)
cd=bpy.data.cameras.new('M05_FIXED_DIAGNOSTIC_CAMERA');fixed=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(fixed);fixed.location=(.4,-8,1.15);fixed.rotation_euler=(Vector((.4,0,1.15))-fixed.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=3.3
scene['diagnostic_camera']=fixed.name;scene['polish_summary']='M04 original armature retained; anticipation, counter-rotation, landing settles; House17 interior; controlled camera track';scene.frame_set(0);bpy.context.view_layer.update();out=R/'assets/M05_ACTING_A02.blend';assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);print('POLISHED_ACTUAL_M04_SAVED',out)
