from world import *
from actor import actor
from contact_rig import *
import stair_test

def stairs_world(w):
 floor(w,-1.3,0,-.5,.8)
 for i in range(4):w.box(i*.30,0,-.36,.30,(i+1)*.18,.72,'#56616a','tread '+str(i+1))
 floor(w,1.2,2.5,-.5,.8,.72)
 wall(w,(-1.3,0,.85),(2.5,0,.85),3.45)
 # Far railing only: the diagnostic never hides the feet behind a near balustrade.
 for i in range(5):
  x=i*.30;y=(i+1)*.18 if i<4 else .72;w.tube([V(x,y,.42),V(x,y+.70,.42)],'#6b7f83',.028)
 w.tube([V(0,.88,.42),V(1.2,1.60,.42),V(2.0,1.60,.42)],'#b4a47f',.045)
 w.line([V(-1.3,3.4,.85),V(2.5,3.4,.85)],'#3f5965',5)
 sconce(w,V(1.6,2.55,.80))

def stair(t):
 d=stair_test.state(t);cam=Camera((.45,1.33,-7.5),(.45,1.33,0),3300);w=World(cam,t);stairs_world(w);actor(w,d);d['camera']={'eye':cam.eye,'target':cam.target,'fixed':True};return [w],d
SHOTS={'STAIRS':(stair,5.)}

import key_test

def door_geometry(w,d):
 R=d['door_R'];D=lambda q:key_test.HINGE+R@np.array(q)
 # Door with real openings through the leaf at the cylinder; no clipping the key mesh.
 for z in [-.065,.065]:
  for x0,x1,y0,y1 in [(-.9,-.785,0,2.1),(-.715,0,0,2.1),(-.785,-.715,0,1.125),(-.785,-.715,1.195,2.1)]:
   w.face([D(V(x0,y0,z)),D(V(x1,y0,z)),D(V(x1,y1,z)),D(V(x0,y1,z))],'#1d3c49','#4f6973',2,name='solid door leaf')
 for x in [-.9,0]:w.face([D(V(x,0,-.065)),D(V(x,0,.065)),D(V(x,2.1,.065)),D(V(x,2.1,-.065))],'#38505b',w=3,name='door edge')
 for z in [-.071,.071]:
  ctr=D(V(-.75,1.16,z));K=R@RZ(d['keyturn']);normal=R@V(0,0,1)
  # Brass cylinder annulus, rotated slot. The opening is a real hole in the mesh.
  def inside(a):
   c=math.cos(a);s=math.sin(a);rad=min(.012/max(1e-8,abs(c)),.006/max(1e-8,abs(s)));return V(rad*c,rad*s,0)
  for j in range(32):
   a=j*math.tau/32;b=(j+1)*math.tau/32;w.face([ctr+K@V(.034*math.cos(a),.034*math.sin(a),0),ctr+K@V(.034*math.cos(b),.034*math.sin(b),0),ctr+K@inside(b),ctr+K@inside(a)],'#d5b476',w=1,name='cylinder face / open key slot')
  w.face([D(V(-.764,1.152,.055)),D(V(-.736,1.152,.055)),D(V(-.736,1.168,.055)),D(V(-.764,1.168,.055))],'#020b14',stroke='none',name='cylinder dark interior')
  spindle=D(V(-.75,.96,z));end=spindle+d['handle_R']@V(.105,0,0);w.tube([spindle,end],'#dbbb7d',.022)
 # Model fixed hinge pins, one shared world pivot.
 for y in [.24,1.75]:w.tube([key_test.HINGE+V(0,y-.06,0),key_test.HINGE+V(0,y+.06,0)],'#b1b2a0',.040)
 if d['key_visible']:
  bow=d['keybow'];K=d['key_R'];w.tube([bow+K@V(.025*math.cos(j*math.tau/32),.018*math.sin(j*math.tau/32),0) for j in range(33)],'#e5bf79',.006)
  # Invariant full-length blade, physically depth-occluded by the solid cylinder/leaf.
  w.face([bow+K@V(-.006,-.002,0),bow+K@V(.006,-.002,0),bow+K@V(.006,-.002,.10),bow+K@V(-.006,-.002,.10)],'#dcb875',w=1,name='full key blade .10m')
  for dz in [.065,.080,.095]:w.tube([bow+K@V(0,0,dz),bow+K@V(.010,0,dz)],'#e5bf79',.005)
 w.text(D(V(-.43,1.75,-.072)),'17',.17)

def house_set(w):
 floor(w,-1.8,1.8,-1.8,2.0)
 # Doorway sides and lintel. Cutaway wall leaves interactions readable from both sides.
 for x in [-.54,.45]:w.box(x,0,-.10,.09,2.18,.20,'#8b846c','fixed door jamb')
 w.box(-.54,2.10,-.10,1.08,.10,.20,'#8b846c','lintel')
 for x0,x1 in [(-1.7,-.54),(.54,1.7)]:w.face([V(x0,0,.10),V(x1,0,.10),V(x1,2.5,.10),V(x0,2.5,.10)],'#203d4b',w=2,name='house wall')
 sconce(w,V(-.85,1.8,-.11))

def key(t):
 d=key_test.state(t)
 if t<4.43:cam=Camera((-.85,1.40,-1.6),(-.25,1.0,-.10),1600)
 elif t<8.30:cam=Camera((-.9,1.5,-2.8),(-.10,1.02,.20),1900)
 else:cam=Camera((1.6,1.45,2.65),(.12,1.0,.28),1800)
 w=World(cam,t);house_set(w);door_geometry(w,d);actor(w,d);d['camera']={'eye':cam.eye,'target':cam.target,'cut':0 if t<4.43 else 1 if t<8.55 else 2};return [w],d
SHOTS['KEY_DOOR']=(key,15.)

import vehicle_test,vehicle_dynamics
from geometry import car
def cabin(w,d):
 w.box(-.85,0,-.60,1.7,.04,2.0,'#142a37','footwell floor');w.box(-.81,.30,.78,1.62,.68,.27,'#203e4e','dashboard');w.box(-.83,.84,.90,1.66,.12,.27,'#365563','dash top')
 for side in [-1,1]:
  w.box(side*.83-.025,.25,-.60,.05,.69,1.70,'#1b3544','door card');w.tube([V(side*.70,1.02,.84),V(side*.62,1.46,.10)],'#587481',.06);w.tube([V(side*.62,1.46,.10),V(side*.62,1.46,-.65)],'#304e5f',.06)
 for x in [-.38,.40]:
  w.box(x-.24,.08,-.36,.48,.18,.55,'#294654','seat cushion');w.box(x-.24,.25,-.46,.48,.72,.12,'#1c3543','seat back');w.box(x-.15,.95,-.43,.30,.22,.10,'#31505c','headrest')
 center=d['wheel_center'];M=d['wheel_R'];W=lambda a:center+M@V(.245*math.cos(a),.245*math.sin(a),0)
 w.tube([V(-.38,.70,.90),center],'#182c38',.065);w.tube([W(j*math.tau/48) for j in range(49)],'#91a0a2',.030)
 for a in [math.pi/6,5*math.pi/6,1.5*math.pi]:w.tube([center,W(a)],'#395361',.026)
 for p in d['pedals']:
  q=p['hinge'];F=V(0,math.sin(p['angle']),math.cos(p['angle']));w.tube([q-V(.045,0,0),q+V(.045,0,0)],'#778d96',.025);w.face([q-V(.054,0,0),q+V(.054,0,0),q+V(.054,0,0)+F*.16,q-V(.054,0,0)+F*.16],'#9fada9',w=2,name='hinged pedal')
 actor(w,d,True)
 w.tube([d['pose']['shoulder']+V(-.14,0,-.018),d['pose']['root']+V(.15,.02,-.018)],'#6c7c80',.027)
 w.box(-.22,1.20,.28,.44,.13,.035,'#071823','mirror');w.tube([V(0,1.33,.28),V(0,1.46,.10)],'#59717b',.018)
 # Project the actual pursuer geometry into the mirror instead of an unrelated icon.
 rel=RY(-d['yaw'])@(d['pursuer_position']-d['position']);rear=World(Camera((0,1.25,.28),(0,1.25,-20),1300,center=(0,0)),d['time']);car(rear,rel,d['pursuer_yaw']-d['yaw'],d['pursuer_wheel_phase'],d['pursuer_steer'],True)
 for op in rear.ops:
  if op[0] not in ['face','line']:continue
  points=[]
  for q in op[1]:
   x,y=rear.cam(q);points.append(V(clamp(x*.001,-.215,.215),clamp(1.26-y*.001,1.205,1.325),.259))
  if op[0]=='face':w.face(points,op[2],op[3],.7,name='same-state projective mirror feed')
  else:w.line(points,op[2],.6)

def city_set(w):
 # Build fixed vertices on a route sampled ONCE, not a time-varying road scroll.
 road=vehicle_dynamics
 for z in np.arange(-24,82,4):
  def P(x,zz,y=0):return V(road.road_x(zz)+x,y,zz)
  w.face([P(-4.5,z),P(4.5,z),P(4.5,z+4),P(-4.5,z+4)],'#122c3b',w=1,name='fixed road')
  if int(z)%8==0:w.face([P(-.035,z+1,.012),P(.035,z+1,.012),P(.035,z+3,.012),P(-.035,z+3,.012)],'#849695',stroke='none',name='lane marking')
  for side in [-1,1]:
   w.face([P(side*4.5,z,.02),P(side*4.7,z,.13),P(side*4.7,z+4,.13),P(side*4.5,z+4,.02)],'#556571',w=1,name='curb');w.face([P(side*4.7,z,.13),P(side*6.5,z,.13),P(side*6.5,z+4,.13),P(side*4.7,z+4,.13)],'#2b414e',w=1,name='sidewalk')
   if int(z)%12==0:
    x=road.road_x(z)+side*7.5;h=4.8+(int(z)//12%3)*1.1;w.box(x-1.2,.13,z,2.4,h,7.,'#203d4d','fixed building')
    wx=x-side*1.21
    for y in [1.4,2.8,4.2]:
     for zz in [z+1.3,z+3.6,z+5.8]:w.face([V(wx,y-.36,zz-.40),V(wx,y+.36,zz-.4),V(wx,y+.36,zz+.4),V(wx,y-.36,zz+.4)],'#b6905b' if int(zz+y)%3==0 else '#2a5061',w=1,name='window')
    pole=P(side*4.9,z+8,.13);w.tube([pole,pole+V(0,4.4,0)],'#657b80',.04);w.face([P(side*4.4,z+7.8,.014),P(side*2.4,z+8,.014),P(side*2.8,z+11,.014),P(side*4.2,z+11,.014)],'#3d5661',stroke='none',name='fixed wet reflection')
    w.box(*(P(side*7.,z+2,.13)),.65,1.7,.12,'#142d3c','entrance')
 # House 17 on the same mapped street; no relocation between chase and bedroom.
 z=50.;x=road.road_x(z)+6.8;w.box(x,0,z,3.,4.7,6.,'#314c58','House 17');w.text(V(x-.02,1.5,z+1.2),'17',.3)

def vehicle_pair(w,d):
 car(w,d['position'],d['yaw'],d['wheel_phase'],d['steer'],False,d['roll'],d['pitch'],d['brake']);car(w,d['pursuer_position'],d['pursuer_yaw'],d['pursuer_wheel_phase'],d['pursuer_steer'],True,d['pursuer_roll'],d['pursuer_pitch'],d['brake'])
 for pos,yaw in [(d['position'],d['yaw']),(d['pursuer_position'],d['pursuer_yaw'])]:
  R=RY(yaw);w.face([pos+R@V(-.65,.018,2.1),pos+R@V(.65,.018,2.1),pos+R@V(1.8,.018,8.),pos+R@V(-1.8,.018,8.)],'#35525c',stroke='none',name='vehicle-parented headlight footprint')

def driving(t):
 d=vehicle_test.state(t);o=np.array(d['position']);R=RY(d['yaw'])@RZ(d['roll'])@RX(d['pitch']);pivot=V(0,.55,0)
 def C(p):return o+RY(d['yaw'])@pivot+R@(np.array(p)-pivot)
 def INV(p):return pivot+R.T@(np.array(p)-o-RY(d['yaw'])@pivot)
 if t<3.15:
  lc=Camera((.65,1.25,-.12),(-.38,.9,.35),780);w=World(lc,t);external=World(Camera((1,1,-2),(0,1,0)),t);city_set(external)
  for op in external.ops:
   if op[0] in ['face','line']:w.ops.append((op[0],[INV(p) for p in op[1]],*op[2:]))
  cabin(w,d);d['diagnostic_coordinate_space']='driver local';d['world_to_local_R']=R.T;d['world_origin']=o
 else:
  eye=o+RY(d['yaw'])@V(3.2,2.2,4.5);cam=Camera(eye,o+V(0,.7,0),1350);w=World(cam,t);city_set(w);vehicle_pair(w,d);d['diagnostic_coordinate_space']='world';d['pose_world']={}
  # Transform rig points into the same world coordinates for diagnostic overlay.
  for name in ['root','shoulder','head']:d['pose_world'][name]=C(d['pose'][name])
  d['pose_world']['legs']=[{**l,**{q:C(l[q]) for q in ['hip','knee','ankle','sole']}} for l in d['pose']['legs']];d['pose_world']['arms']=[{q:C(a[q]) for q in ['shoulder','elbow','wrist']} for a in d['pose']['arms']]
 d['phase']='steer input / cockpit' if t<3.15 else 'front tyres / world trajectory';return [w],d

def chase(t):
 d=vehicle_test.state(t);mid=(d['position']+d['pursuer_position'])/2;cam=Camera(mid+V(3.5,10.,13.),mid+V(0,.3,0),1050);w=World(cam,t);city_set(w);vehicle_pair(w,d);d['phase']='two independent cars / connected road';d['hide_rig_debug']=True;return [w],d
SHOTS.update(STEERING=(driving,6.),CHASE=(chase,6.))

import curtain_test

def bedroom(t):
 d=curtain_test.state(t);cam=Camera((1.6,1.8,-1.4),(0,1.15,.15),1100);w=World(cam,t)
 floor(w,-1.8,1.8,-2.,.10)
 for x0,x1,y0,y1 in [(-1.8,-.77,0,2.6),(.77,1.8,0,2.6),(-.77,.77,0,.60),(-.77,.77,2.2,2.6)]:w.face([V(x0,y0,.10),V(x1,y0,.10),V(x1,y1,.10),V(x0,y1,.10)],'#233e4b',w=2,name='bedroom wall')
 w.box(-1.7,0,-1.8,.75,.32,1.55,'#172e3d','bed');w.box(-1.72,.32,-1.8,.79,.13,1.55,'#496171','mattress');w.box(-1.65,.45,-1.7,.60,.10,.33,'#9eaa9f','pillow')
 # Local exterior maps to the same street beside House 17; floor is 2.6m above pavement.
 w.face([V(-10,-2.60,2.5),V(6,-2.60,2.5),V(6,-2.60,10),V(-10,-2.60,10)],'#183443',w=1,name='street outside');car(w,d['sedan_position'],math.pi/2,0,0,True)
 for x in [-.76,.73]:w.box(x,.60,.03,.03,1.60,.09,'#83958e','window jamb')
 for y in [.60,2.17]:w.box(-.76,y,.03,1.52,.035,.09,'#83958e','window lintel')
 w.tube([V(-.86,2.23,-.035),V(.86,2.23,-.035)],'#bea977',.025)
 mesh=d['fabric']
 for row in range(curtain_test.NR):
  for col in range(curtain_test.NC):
   a,b,c,e=mesh[row,col],mesh[row,col+1],mesh[row+1,col+1],mesh[row+1,col];normal=np.cross(b-a,e-a);normal/=np.linalg.norm(normal);shade=float(normal@V(.9,.05,-.4));colr='#7a8d94' if shade>.40 else '#163442' if shade<-.10 else '#3c5b6a';w.face([a,b,c,e],colr,stroke='none',name='fabric fold')
 for col in range(0,curtain_test.NC+1,6):
  top=mesh[0,col];w.tube([top,top+V(0,.08,0)],'#c5b68f',.009);w.line([mesh[r,col] for r in range(curtain_test.NR+1)],'#193344',1)
 w.line(list(mesh[-1]),'#748892',2);w.line(list(mesh[:,-1]),'#8194a0',2)
 actor(w,d);return [w],d
SHOTS['CURTAIN']=(bedroom,5.)
