"""Build native spatial/IK editing scenes from the same metre world used for proofs.
Run: blender -b --factory-startup -t 2 --python source/export_blender.py
This is an editable rig/architecture companion; the MP4 renderer is depth_render.py.
"""
import bpy,sys,json,math,os
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
from scenes import SCENES,DURATIONS
from actions import STATES
from rig import V
C=lambda p:(float(p[0]),float(p[2]),float(p[1]))
materials={}
def mat(col):
 if col not in materials:
  m=bpy.data.materials.new(col);h=col.lstrip('#');m.diffuse_color=tuple(int(h[i:i+2],16)/255 for i in (0,2,4))+(1,);materials[col]=m
 return materials[col]
def empty(name,p):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.empty_display_type='SPHERE';o.empty_display_size=.04;o.location=C(p);return o
for k in ['STAIRS','HOUSE','BEDROOM','DRIVING']:
 scene=bpy.data.scenes.new(k+'_V12_WORLD');bpy.context.window.scene=scene;scene.render.fps=30;scene.frame_end=round(DURATIONS[k]*30);scene.render.resolution_x=1080;scene.render.resolution_y=1920;scene.world=bpy.data.worlds.new(k+'_night');scene.world.color=(.025,.045,.07)
 s,d,w=SCENES[k](0)
 verts=[];faces=[];colors=[]
 for op in w.ops:
  if op[0]!='face':continue
  st=len(verts);verts.extend(C(p) for p in op[1]);faces.append(list(range(st,len(verts))));colors.append(op[2])
 mesh=bpy.data.meshes.new(k+'_architectural_surfaces');mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new(k+'_metre_environment',mesh);scene.collection.objects.link(obj)
 for color in sorted(set(colors)):mesh.materials.append(mat(color))
 indices={m.name:i for i,m in enumerate(mesh.materials)}
 for face,color in zip(mesh.polygons,colors):face.material_index=indices[color]
 camdata=bpy.data.cameras.new(k+'_perspective');cam=bpy.data.objects.new(k+'_camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.lens=36
 # Native IK edit rig, targets come from explicit contact choreography.
 if 'pose' in d:
  p=d['pose'];arm=bpy.data.armatures.new(k+'_contact_skeleton');rig=bpy.data.objects.new(k+'_articulated_witness',arm);scene.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bones={}
  root=arm.edit_bones.new('root');root.head=C(p['root']);root.tail=C(p['root']+V(0,.1,0));bones['root']=root
  for typ,joints,lens in [('arm',p['arms'],['shoulder','elbow','wrist']),('leg',p['legs'],['hip','knee','ankle'])]:
   for j,q in enumerate(joints):
    a=arm.edit_bones.new(f'{typ}_{j}_upper');a.head=C(q[lens[0]]);a.tail=C(q[lens[1]]);a.parent=root;b=arm.edit_bones.new(f'{typ}_{j}_lower');b.head=C(q[lens[1]]);b.tail=C(q[lens[2]]);b.parent=a;b.use_connect=True
  bpy.ops.object.mode_set(mode='OBJECT');targets={}
  for typ in ['arm','leg']:
   for j in range(2):
    q=p['arms' if typ=='arm' else 'legs'][j];end='wrist' if typ=='arm' else 'ankle';mid='elbow' if typ=='arm' else 'knee';target=empty(f'{k}_{typ}_{j}_CONTACT_TARGET',q[end]);pole=empty(f'{k}_{typ}_{j}_POLE',q[mid]);con=rig.pose.bones[f'{typ}_{j}_lower'].constraints.new('IK');con.target=target;con.pole_target=pole;con.chain_count=2;targets[(typ,j)]=(target,pole)
  rig.select_set(False)
 for f in range(scene.frame_end):
  t=f/30;_,state,ww=SCENES[k](t);cc=ww.cam;cam.location=C(cc.eye);direction=Vector(C(cc.target))-cam.location;cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=f+1);cam.keyframe_insert('rotation_euler',frame=f+1)
  if 'pose' not in state or k=='DRIVING':continue
  pp=state['pose'];rig.pose.bones['root'].location=Vector(C(pp['root']))-Vector(C(p['root']));rig.pose.bones['root'].keyframe_insert('location',frame=f+1)
  for (typ,j),(target,pole) in targets.items():
   q=pp['arms' if typ=='arm' else 'legs'][j];target.location=C(q['wrist' if typ=='arm' else 'ankle']);pole.location=C(q['elbow' if typ=='arm' else 'knee']);target.keyframe_insert('location',frame=f+1);pole.keyframe_insert('location',frame=f+1)
 scene.frame_set(1);print('NATIVE_SCENE_READY',k,flush=True)
tag=os.environ.get('NOIRFRAME_BLEND_TAG','');out=R/'assets'/('NOIRFRAME_V12_SPATIAL_CONTACT_EDIT'+('_'+tag if tag else '')+'.blend');assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out));print('BLENDER_EDIT_SOURCE_SAVED',out,flush=True)
