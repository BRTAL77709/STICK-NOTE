"""Native Blender rigs: real armature IK, weighted meshes, world contact targets."""
import bpy,math
from mathutils import Vector,Matrix
M={}
def mat(name,color):
 if name in M:return M[name]
 rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)];rgb=[c/12.92 if c<.04045 else ((c+.055)/1.055)**2.4 for c in rgb];m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*rgb,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);M[name]=m;return m
INK=lambda:mat('Ink','#030c15')
NAVY=lambda:mat('Hoodie navy','#152b3a')
def mesh(name,verts,faces,material,parent=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 if parent:o.parent=parent
 return o
def cube(name,location,scale,material,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=location);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 if parent:o.parent=parent
 return o
def empty(name,location=(0,0,0),parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=location;o.empty_display_size=.10;o.empty_display_type='SPHERE';o.parent=parent;return o
def sphere(name,center,scale,material,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1,location=center);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material)
 if parent:o.parent=parent
 return o
def line(name,points,r,material,parent=None):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=1;c.bevel_depth=r;c.bevel_resolution=0;s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,v in zip(s.points,points):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(material);o.parent=parent;return o
def weighted(o,rig,bone):
 # Apply the rest geometry into armature coordinates and bind every vertex to a native bone.
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
 vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');mod=o.modifiers.new('Native armature skin','ARMATURE');mod.object=rig;o.parent=rig;return o
def segment(name,a,b,r,material,rig,bone):
 a,b=Vector(a),Vector(b);o=sphere(name,(a+b)/2,(r,r,(b-a).length/2+r*.5),material);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return weighted(o,rig,bone)
def key(o,frame,paths=('location','rotation_euler')):
 for path in paths:o.keyframe_insert(data_path=path,frame=frame)
def linearize():
 for a in bpy.data.actions:
  try:
   for c in a.fcurves:
    for p in c.keyframe_points:p.interpolation='LINEAR'
  except AttributeError:pass
class Character:
 def __init__(self,name='Witness',scale=1):
  self.scale=scale;arm=bpy.data.armatures.new(name+' articulated skeleton');self.root=bpy.data.objects.new(name+' RIG',arm);bpy.context.collection.objects.link(self.root);bpy.context.view_layer.objects.active=self.root;self.root.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
  specs={'pelvis':((0,0,.59),(0,0,.68),None),'torso':((0,0,.68),(0,0,1.20),'pelvis'),'neck':((0,0,1.20),(0,0,1.50),'torso')}
  for i,s in enumerate([-1,1]):
   specs[f'thigh{i}']=((s*.10,0,.68),(s*.10,-.08,.37),'pelvis');specs[f'shin{i}']=((s*.10,-.08,.37),(s*.10,0,.06),f'thigh{i}')
   specs[f'upperarm{i}']=((s*.17,0,1.16),(s*.28,-.06,.92),'torso');specs[f'forearm{i}']=((s*.28,-.06,.92),(s*.26,-.10,.68),f'upperarm{i}')
  for n,(a,b,p) in specs.items():
   bone=arm.edit_bones.new(n);bone.head=a;bone.tail=b
   if p:bone.parent=arm.edit_bones[p];bone.use_connect=False
  bpy.ops.object.mode_set(mode='OBJECT');self.root.select_set(False);self.root.scale=(scale,)*3;self.root.show_in_front=True
  self.feet=[];self.hands=[]
  for i,s in enumerate([-1,1]):
   ft=empty(name+f' foot {i} WORLD LOCK');hand=empty(name+f' hand {i} CONTACT');self.feet.append(ft);self.hands.append(hand)
   for n,target in [(f'shin{i}',ft),(f'forearm{i}',hand)]:
    c=self.root.pose.bones[n].constraints.new('IK');c.name='World contact two-bone IK';c.target=target;c.chain_count=2;c.use_stretch=False;c.iterations=256
   segment(name+f' trouser upper{i}',*specs[f'thigh{i}'][:2],.065,mat('Trouser cel','#1c3545'),self.root,f'thigh{i}');segment(name+f' trouser lower{i}',*specs[f'shin{i}'][:2],.057,NAVY(),self.root,f'shin{i}')
   segment(name+f' sleeve upper{i}',*specs[f'upperarm{i}'][:2],.062,NAVY(),self.root,f'upperarm{i}');segment(name+f' sleeve lower{i}',*specs[f'forearm{i}'][:2],.053,mat('Sleeve highlight','#274554'),self.root,f'forearm{i}')
   shoe=mesh(name+f' grounded shoe{i}',[(-.085,-.20,-.06),(.085,-.20,-.06),(.085,.08,-.06),(-.085,.08,-.06),(-.08,-.17,.035),(.08,-.17,.035),(.07,.06,.055),(-.07,.06,.055)],[(0,1,2,3),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0),(4,7,6,5)],mat('Shoe','#0b1d2b'),ft);shoe.scale=(scale,)*3
   palm=sphere(name+f' palm{i}',(0,0,0),(.047,.035,.064),mat('Skin','#c6cdd1'),hand);palm.scale=(scale,)*3
   for j in range(3):line(name+f' fingers{i}-{j}',[(-.02+j*.016,-.035,-.02),(-.02+j*.016,-.035,.025)],.0025,INK(),hand)
  # Extruded hoodie with drawn seams; mesh vertices are actually skinned to the torso bone.
  verts=[(x,y,z) for y in [-.115,.115] for x,z in [(-.20,.66),(.20,.66),(.18,1.18),(-.18,1.18)]]
  torso=mesh(name+' hoodie',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],NAVY());weighted(torso,self.root,'torso')
  for x in [-.05,.05]:
   o=cube(name+' drawstring',(x,-.124,1.06),(.008,.008,.15),mat('Thread','#536b75'));weighted(o,self.root,'torso')
  self.head=empty(name+' HEAD perspective');c=self.head.constraints.new('COPY_LOCATION');c.target=self.root;c.subtarget='neck';c.head_tail=1;self.head.scale=(scale,)*3
  sphere(name+' hood back',(0,.095,-.07),(.29,.19,.24),NAVY(),self.head)
  sphere(name+' approved round face',(0,0,0),(.285,.255,.285),mat('Face','#c3cbd0'),self.head)
  # Cap has a domed crown and actual projected brim, not a facial texture swap.
  sphere(name+' cap crown',(0,.015,.14),(.305,.27,.205),mat('Cap','#0c2231'),self.head);cube(name+' cap band',(0,-.205,.08),(.61,.10,.075),mat('Cap band','#122e40'),self.head)
  sphere(name+' cap brim',(0,-.285,.07),(.32,.14,.028),mat('Cap brim','#102b3c'),self.head)
  self.eyes=[]
  for i,x in enumerate([-.105,.105]):
   eye=sphere(name+f' eye{i}',(x,-.245,-.015),(.021,.014,.055),INK(),self.head);self.eyes.append(eye)
  self.mouth=sphere(name+' mouth',(.008,-.248,-.14),(.037,.012,.013),INK(),self.head)
  line(name+' amber rim',[(-.29,.005,.10),(-.26,.01,.25),(-.12,.01,.34)],.007,mat('Amber rim','#e5a34e'),self.head)
 def pose(self,frame,root,yaw,feet,hands,lean=0,head_yaw=None,fear=.3):
  self.root.location=root;self.root.rotation_euler=(0,0,yaw);key(self.root,frame);self.root.pose.bones['torso'].rotation_mode='XYZ';self.root.pose.bones['torso'].rotation_euler=(lean,0,0);self.root.pose.bones['torso'].keyframe_insert('rotation_euler',frame=frame)
  for o,p in zip(self.feet,feet):o.location=p;o.rotation_euler=(0,0,yaw);key(o,frame)
  for o,p in zip(self.hands,hands):o.location=p;key(o,frame)
  self.head.rotation_euler=(0,0,yaw if head_yaw is None else head_yaw);key(self.head,frame,('rotation_euler',))
  for o in self.eyes:o.scale.z=1+.25*fear;o.keyframe_insert('scale',frame=frame)
  self.mouth.scale.z=1+1.8*fear;self.mouth.keyframe_insert('scale',frame=frame)
 def residuals(self):
  bpy.context.view_layer.update();r=[]
  for j in range(2):
   for bone,target in [(f'shin{j}',self.feet[j]),(f'forearm{j}',self.hands[j])]:r.append((self.root.matrix_world@self.root.pose.bones[bone].tail-target.location).length)
  return r

def cloth_material():
 m=mat('Curtain blue','#31566c');nodes=m.node_tree.nodes;nodes.clear();geo=nodes.new('ShaderNodeNewGeometry');dot=nodes.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(.2,-.95,.1);ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT';ramp.color_ramp.elements[0].position=.20;ramp.color_ramp.elements[0].color=mat('Cloth shadow','#203c50').diffuse_color;ramp.color_ramp.elements[1].position=.72;ramp.color_ramp.elements[1].color=mat('Cloth light','#4a6b80').diffuse_color;mid=ramp.color_ramp.elements.new(.45);mid.color=mat('Cloth mid','#31566c').diffuse_color;e=nodes.new('ShaderNodeEmission');out=nodes.new('ShaderNodeOutputMaterial');links=m.node_tree.links;links.new(geo.outputs['Normal'],dot.inputs[0]);links.new(dot.outputs['Value'],ramp.inputs[0]);links.new(ramp.outputs[0],e.inputs[0]);links.new(e.outputs[0],out.inputs[0]);return m
