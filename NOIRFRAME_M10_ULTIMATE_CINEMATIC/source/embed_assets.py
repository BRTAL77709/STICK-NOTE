"""Editable native prop/cloth/vehicle assets driven by the same authored states as output."""
import bpy,math
from mathutils import Matrix,Vector
import numpy as np
from contact_rig import V,RY
from world import World,Camera
import sets,vehicle_system as VS
B=Matrix(((0,0,1),(1,0,0),(0,1,0)));BT=B.transposed();FACES=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def native(q):return B@Vector(q)
def empty(scene,name):o=bpy.data.objects.new(name,None);scene.collection.objects.link(o);return o
def mesh(scene,name,vertices,faces,color,parent=None):
 m=bpy.data.meshes.new(name);m.from_pydata([native(v) for v in vertices],[],faces);m.update();o=bpy.data.objects.new(name,m);scene.collection.objects.link(o);o.parent=parent;mat=bpy.data.materials.get(color)
 if not mat:
  mat=bpy.data.materials.new(color);mat.diffuse_color=tuple(int(color[i:i+2],16)/255 for i in [1,3,5])+(1,)
 m.materials.append(mat);return o
def box(scene,name,p,size,col,parent=None):
 x,y,z=p;dx,dy,dz=size;vv=[(x+i*dx,y+j*dy,z+k*dz) for i,j,k in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]];return mesh(scene,name,vv,FACES,col,parent)
def key(scene,o,i,pos,R):
 o.location=native(pos);o.rotation_mode='QUATERNION';o.rotation_quaternion=(B@Matrix(np.asarray(R).tolist())@BT).to_quaternion();o.keyframe_insert('location',frame=i);o.keyframe_insert('rotation_quaternion',frame=i)
def vehicle(scene,name,black=False,exit_opening=False):
 root=empty(scene,name);temp=World(Camera((3,3,5),(0,.6,0)),0);sets.basecar(temp,V(0,0,0),0,0,0,black)
 for i,g in enumerate(temp.geometry):
  if g['name']=='wheel' or (exit_opening and g['name']=='car side' and all(abs(p[0]+.85)<1e-5 for p in g['vertices'])):continue
  mesh(scene,f'{name}_{g["name"]}_{i}',g['vertices'],[tuple(range(len(g['vertices'])))],g['color'],root)
 wheels=[]
 for xx in [-.9,.9]:
  for zz in [-1.32,1.28]:
   o=empty(scene,f'{name}_WHEEL_{xx}_{zz}');o.parent=root;o.location=native((xx,.30,zz));vv=[(0,.30*math.sin(a),.30*math.cos(a)) for a in np.linspace(0,math.tau,24,endpoint=False)];mesh(scene,o.name+'_TIRE',vv,[tuple(range(24))],'#07121c',o)
   for k in range(5):
    a=k*math.tau/5;mesh(scene,o.name+'_SPOKE_'+str(k),[(0,0,0),(0,.23*math.sin(a),.23*math.cos(a)),(.005,.23*math.sin(a+.035),.23*math.cos(a+.035)),(.005,0,0)],[(0,1,2,3)],'#82979e',o)
   wheels.append(o)
 if exit_opening:
  for k,(z0,z1) in enumerate([(-2.15,-.66),(.71,2.05)]):mesh(scene,name+'_FIXED_SIDE_'+str(k),[(-.85,.38,z0),(-.85,.38,z1),(-.85,.93,z1),(-.85,.93,z0)],[(0,1,2,3)],'#26485b',root)
 return root,wheels

def build(scene,shot,states):
 # Camera-readable native architecture snapshot; script remains authoritative for complete set regeneration.
 if shot in ['KEY_LOCK','DOOR_ENTRY']:
  w=World(Camera((-1,1.5,-3),(0,1,0)),0);sets.house_exterior(w)
 elif shot=='WINDOW_CURTAIN':
  w=World(Camera((-2.3,1.85,-2.25),(0,1.15,.2)),0);sets.bedroom(w,states[0])
 elif shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:
  w=World(Camera((.7,1.3,-.15),(-.38,.9,.35)),0);sets.cockpit(w,states[0])
 else:w=None
 if w:
  for i,g in enumerate(w.geometry):
   if g['name'] in ['rigged curtain fold','same-state projective mirror feed']:continue
   mesh(scene,f'SET_{g["name"]}_{i}',g['vertices'],[tuple(range(len(g['vertices'])))],g['color'])
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:
  wheel=empty(scene,'STEERING_COLUMN_AXIS');ring=[]
  for radius in [.230,.260]:ring.extend([(radius*math.cos(a),radius*math.sin(a),0) for a in np.linspace(0,math.tau,48,endpoint=False)])
  mesh(scene,'STEERING_RIM',ring,[(j,(j+1)%48,(j+1)%48+48,j+48) for j in range(48)],'#91a0a2',wheel)
  for j,a in enumerate([math.pi/6,5*math.pi/6,1.5*math.pi]):mesh(scene,'STEERING_SPOKE_'+str(j),[(0,0,0),(.245*math.cos(a),.245*math.sin(a),0),(.245*math.cos(a+.05),.245*math.sin(a+.05),0),(0,.012,0)],[(0,1,2,3)],'#395361',wheel)
  pedals=[empty(scene,'ACCELERATOR_HINGE'),empty(scene,'BRAKE_HINGE')]
  for j,o in enumerate(pedals):mesh(scene,o.name+'_PAD',[(-.054,0,0),(.054,0,0),(.054,0,.16),(-.054,0,.16)],[(0,1,2,3)],'#9fada9',o)
  for i,d in enumerate(states):
   key(scene,wheel,i,d['wheel_center'],d['wheel_R'])
   for j,o in enumerate(pedals):key(scene,o,i,d['pedals'][j]['hinge'],sets.RX(-d['pedals'][j]['angle']))
 if shot in ['KEY_LOCK','DOOR_ENTRY']:
  hinge=empty(scene,'PROP_DOOR_HINGE');
  for j,(x0,x1,y0,y1) in enumerate([(-.9,-.785,0,2.1),(-.715,0,0,2.1),(-.785,-.715,0,1.125),(-.785,-.715,1.195,2.1)]):box(scene,'DOOR_LEAF_'+str(j),(x0,y0,-.065),(x1-x0,y1-y0,.13),'#1d3c49',hinge)
  keyobj=empty(scene,'PROP_KEY_BOW');mesh(scene,'KEY_BLADE_160mm',[(-.008,-.002,0),(.008,-.002,0),(.008,-.002,.16),(-.008,-.002,.16)],[(0,1,2,3)],'#dcb875',keyobj)
  ring=[(.044*math.cos(a),.027*math.sin(a),0) for a in np.linspace(0,math.tau,32,endpoint=False)];mesh(scene,'KEY_BOW',ring,[tuple(range(32))],'#dcb875',keyobj)
  handle=empty(scene,'PROP_HANDLE_SPINDLE');box(scene,'HANDLE_LEVER',(0,-.011,-.011),(.105,.022,.022),'#dbbb7d',handle);thumb=empty(scene,'PROP_INSIDE_THUMBTURN');box(scene,'THUMBTURN_TAB',(-.024,-.006,-.006),(.048,.012,.012),'#c7aa70',thumb)
  for i,d in enumerate(states):
   key(scene,hinge,i,sets.old.key_test.HINGE,d['door_R']);key(scene,keyobj,i,d['keybow'],d['key_R']);key(scene,handle,i,d['spindle'],d['handle_R']);key(scene,thumb,i,sets.old.key_test.HINGE+np.array(d['door_R'])@V(-.75,1.16,.105),np.array(d['door_R'])@sets.RZ(d['keyturn']));keyobj.hide_render=not d['key_visible'];keyobj.keyframe_insert('hide_render',frame=i)
 if shot=='WINDOW_CURTAIN':
  grid=np.array(states[0]['fabric']);nr,nc=grid.shape[:2];faces=[(r*nc+c,r*nc+c+1,(r+1)*nc+c+1,(r+1)*nc+c) for r in range(nr-1) for c in range(nc-1)];o=mesh(scene,'RIGGED_FABRIC_MATERIAL_WIDTH_1_60m',grid.reshape(-1,3),faces,'#3c5b6a');o.shape_key_add(name='Basis')
  for i,d in enumerate(states):
   k=o.shape_key_add(name='FOLD_POSE_'+str(i))
   for v,q in zip(k.data,np.array(d['fabric']).reshape(-1,3)):v.co=native(q)
   k.value=0;k.keyframe_insert('value',frame=i-1);k.value=1;k.keyframe_insert('value',frame=i);k.value=0;k.keyframe_insert('value',frame=i+1)
 if shot in ['CAR_CHASE','ROAD_BUILDINGS','CAR_EXIT_RUNNING']:
  cars=[vehicle(scene,'WITNESS_CAR',False,shot=='CAR_EXIT_RUNNING')]
  if shot!='CAR_EXIT_RUNNING':cars.append(vehicle(scene,'BLACK_SEDAN',True))
  for i,d in enumerate(states):
   for j,(root,wheels) in enumerate(cars):
    prefix='' if j==0 else 'pursuer_';v=VS.state(min(11,9+d['time'])) if shot=='CAR_EXIT_RUNNING' else d;pos=V(0,0,0) if shot=='CAR_EXIT_RUNNING' else v[prefix+'position'];yaw=0 if shot=='CAR_EXIT_RUNNING' else v[prefix+'yaw'];key(scene,root,i,pos,RY(yaw));phase=v[prefix+'wheel_phase'];steer=v[prefix+'steer']
    for k,wh in enumerate(wheels):wh.rotation_mode='QUATERNION';wh.rotation_quaternion=(Matrix.Rotation(steer if k%2 else 0,3,'Z')@Matrix.Rotation(float(phase[k]),3,'Y')).to_quaternion();wh.keyframe_insert('rotation_quaternion',frame=i)
  if shot=='CAR_EXIT_RUNNING':
   door=empty(scene,'DRIVER_DOOR_REAL_HINGE');box(scene,'DRIVER_DOOR_LEAF',(0,-.28,-1.35),(.035,.56,1.35),'#294b5e',door)
   for i,d in enumerate(states):key(scene,door,i,V(-.85,.65,.70),RY(d['door_angle']))
 scene['native_asset_scope']='Native character, cameras, editable prop/cloth/vehicle assets. Procedural scripts supply complete illustrative architecture and projective mirrors.'


def cockpit_hierarchy(scene):
 names=['CAR_ROOT','BODY','INTERIOR','DRIVER_SEAT','DASHBOARD','STEERING_COLUMN','STEERING_WHEEL','WINDSHIELD','REARVIEW_MIRROR','SIDE_MIRRORS','DRIVER_RIG']
 old=list(scene.objects);groups={n:empty(scene,n) for n in names};root=groups['CAR_ROOT'];root['space']='car local; source vehicle_system supplies the registered world transform during rendering'
 for n,o in groups.items():
  if n=='CAR_ROOT':continue
  o.parent=groups['STEERING_COLUMN'] if n=='STEERING_WHEEL' else root
 for o in old:
  if o.parent:continue
  n=o.name.lower()
  if o.type=='ARMATURE' or n.startswith(('ctrl_','m07_wrist','m07_elbow','m07_fingertip')) or (o.type=='MESH' and o.modifiers):cat='DRIVER_RIG'
  elif 'steering_column_axis' in n:cat='STEERING_WHEEL'
  elif any(k in n for k in ['dashboard','dash top','air vent']):cat='DASHBOARD'
  elif any(k in n for k in ['seat ','headrest']):cat='DRIVER_SEAT'
  elif 'side mirror' in n:cat='SIDE_MIRRORS'
  elif 'mirror' in n:cat='REARVIEW_MIRROR'
  elif o.type=='CAMERA':continue
  else:cat='INTERIOR'
  m=o.matrix_world.copy();o.parent=groups[cat];o.matrix_world=m
 scene['M10_hierarchy']='Native identity parent frames preserve car-local transforms; wheel children keep their keyed local axis; all controls and bound skin share DRIVER_RIG.'
 return groups
