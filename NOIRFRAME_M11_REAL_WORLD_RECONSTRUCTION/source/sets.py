"""World-space illustrated architecture and props; all shot transforms share one registration."""
from bootstrap import ROOT
from world import *
from contact_rig import *
import shots as old
from geometry import car as basecar,rain_overlay
import vehicle_system as VS
old.actor=lambda *a,**k:None

def in_view(w,c,radius):
 if not getattr(w,'render_frustum',False):return True
 q=np.asarray(c)-w.cam.eye;z=float(q@w.cam.forward);x=float(q@w.cam.right);y=float(q@w.cam.up)
 hx=540/w.cam.focal;hy=960/w.cam.focal
 return z+radius>.1 and abs(x)<=z*hx+radius*math.sqrt(1+hx*hx) and abs(y)<=z*hy+radius*math.sqrt(1+hy*hy)

def city(w):
 # Continuous fixed reference road, intersections and varied designed facades.
 def P(x,zz,y=0):return V(VS.roadref(zz)+x,y,zz)
 for z in range(-64,161,5):
  if not in_view(w,V(VS.roadref(z+2.5),.05,z+2.5),9.):continue
  w.face([P(-4.5,z),P(4.5,z),P(4.5,z+5),P(-4.5,z+5)],'#132d3c',w=1,name='fixed road')
  if z%10==1 and not 20<=z<=26:w.face([P(-.035,z+1,.009),P(.035,z+1,.009),P(.035,z+3.2,.009),P(-.035,z+3.2,.009)],'#a4ada0',stroke='none',name='lane dash')
  for side in [-1,1]:
   if 20<=z<=26:continue
   w.face([P(side*4.5,z,0),P(side*4.7,z,.13),P(side*4.7,z+5,.13),P(side*4.5,z+5,0)],'#52636a',w=1,name='curb');w.face([P(side*4.7,z,.13),P(side*6.3,z,.13),P(side*6.3,z+5,.13),P(side*4.7,z+5,.13)],'#30434e',w=1,name='sidewalk')
 for idx,z in enumerate(range(-60,150,10)):
  idx=(z+20)//10 # Preserve existing facade assignments; extension must not reseed the old city.
  for side in [-1,1]:
   if z==20 or (side==-1 and abs(z-VS.HOUSE_ORIGIN[2])<8):continue
   x=VS.roadref(z)+side*7.8;h=[4.8,6.2,5.2,7.5][(idx+(side==1))%4];width=[5.8,6.6,7.2][idx%3];wallx=x-side*1.36;col=['#29424d','#263c4a','#354b50'][idx%3]
   if not in_view(w,V(x,h*.5,z+width*.5),11.0):continue
   w.box(x-1.35,.13,z,2.7,h,width,col,'masonry building')
   # Cornices, pilasters, storefront and inset front door: no repeating blank boxes.
   for yy in [.25,2.7,h-.13]:w.box(wallx-.05,yy,z,.12,.09,width,'#647175','facade cornice')
   for zz in [z+.12,z+width-.20]:w.box(wallx-.04,.25,zz,.10,h-.40,.10,'#596974','facade pier')
   for yy in np.arange(1.45,h-.6,1.35):
    for j,zz in enumerate(np.arange(z+1,z+width-.3,1.65)):
     corners=[V(wallx,yy-.37,zz-.37),V(wallx,yy+.37,zz-.37),V(wallx,yy+.37,zz+.37),V(wallx,yy-.37,zz+.37)];w.face(corners,'#d2a16b' if (idx+j+int(yy))%4==0 else '#284e60','#0e2635',2,name='inset window');w.line([V(wallx-side*.004,yy-.37,zz),V(wallx-side*.004,yy+.37,zz)],'#61767e',1)
   w.face([V(wallx,.13,z+.3),V(wallx,2.1,z+.3),V(wallx,2.1,z+.95),V(wallx,.13,z+.95)],'#102a36','#87968b',2,name='street entrance')
   if idx%3==0:
    w.face([V(wallx,.15,z+1.2),V(wallx,1.9,z+1.2),V(wallx,1.9,z+3.6),V(wallx,.15,z+3.6)],'#173f50','#b09c78',2,name='shopfront');w.face([V(wallx,2.25,z+1.0),V(wallx-side*.50,2.0,z+1.0),V(wallx-side*.50,2.0,z+3.9),V(wallx,2.25,z+3.9)],'#597278',name='shop awning')
   pole=P(side*4.95,z+7,.13);w.tube([pole,pole+V(0,4.3,0),pole+V(-side*.55,4.3,0)],'#74858b',.04);w.glow(pole+V(-side*.55,4.25,0),.40);lamp=pole+V(-side*.55,4.25,0);w.box(lamp[0]-.16,lamp[1]-.04,lamp[2]-.15,.32,.065,.30,'#e8af69','amber streetlight housing');w.face([lamp+V(-.14,-.045,-.13),lamp+V(.14,-.045,-.13),lamp+V(.14,-.045,.13),lamp+V(-.14,-.045,.13)],'#ffcd80',stroke='none',name='lit streetlamp underside')
   w.face([P(side*3.7,z+5,.006),P(side*4.2,z+5,.006),P(side*3.8,z+8.5,.006),P(side*3.2,z+8.5,.006)],'#355365',stroke='none',name='lamp reflection')
 # Visible cross street and markings, same geometry in every view.
 z=25.;w.face([V(-16,.003,z-3),V(24,.003,z-3),V(24,.003,z+3),V(-16,.003,z+3)],'#142e3b',stroke='none',name='intersection')
 for x in np.arange(-4,4,.7):w.face([V(VS.roadref(z)+x,.013,z-3.4),V(VS.roadref(z)+x+.32,.013,z-3.4),V(VS.roadref(z)+x+.32,.013,z-2.4),V(VS.roadref(z)+x,.013,z-2.4)],'#8e9f9f',stroke='none',name='crosswalk')
 # House17 on registered left side of stopping location. It is the same facade as entry.
 Hcam=Camera(VS.HOUSE_R.T@(w.cam.eye-VS.HOUSE_ORIGIN),VS.HOUSE_R.T@(w.cam.target-VS.HOUSE_ORIGIN),w.cam.focal,up=VS.HOUSE_R.T@w.cam.up);local=World(Hcam,w.t);house_exterior(local);old.door_geometry(local,old.key_test._raw_state(0));append_transform(w,local,VS.HOUSE_R,VS.HOUSE_ORIGIN);w.text(VS.HOUSE_ORIGIN+VS.HOUSE_R@V(-.13,2.35,-.08),'17',.22)
 for z in [-6,17]:
  parked=World(w.cam,w.t);basecar(parked,V(VS.roadref(z)-3.4,0,z),0,0,0,True)
  for op in parked.ops:
   if op[0]=='face':
    col={'#102838':'#41474b','#c7e1dc':'#334850','#922e38':'#4c353a'}.get(op[2],op[2]);op=(op[0],op[1],col,*op[3:])
   w.ops.append(op)
 street_details(w)
 world_rain(w)

def world_rain(w):
 for j in range(170):
  z=-24+(j*13.571)%125;x=VS.roadref(z)-8.5+(j*7.391)%17;y=(j*.113-w.t*(4+j%4*.22))%6
  w.line([V(x,y,z),V(x-.025,y-.23,z+.035)],'#5c7e8f',1)

def append_transform(w,other,R,T):
 for op in other.ops:
  if op[0] in ['face','line']:w.ops.append((op[0],[np.array(T)+R@np.asarray(p) for p in op[1]],*op[2:]))
  elif op[0]=='glyph':
   # Text/glow drawing closures are camera-specific. Do not move a pre-projected glyph.
   pass

def house_exterior(w):
 for x0,x1 in [(-2.2,-.54),(.54,2.2)]:w.box(x0,0,.10,x1-x0,5.1,.20,'#2c4854','House17 facade')
 w.box(-.54,2.15,.10,1.08,2.95,.20,'#2c4854','House17 above door');w.box(-2.3,5.1,.10,4.6,.12,2.7,'#152f3d','house cornice');w.box(-2.2,-.14,.15,4.4,.14,3.,'#3a4d51','house foundation')
 for x in [-1.65,1.25]:
  w.box(x,1.0,-.02,.65,1.05,.08,'#142f3d','ground window');w.line([V(x+.32,1,-.04),V(x+.32,2.05,-.04)],'#788f98',3)
 w.box(-1.56,3.20,-.02,1.52,1.60,.08,'#294b5a','registered bedroom window');w.box(.70,3.20,-.02,.90,1.2,.08,'#294b5a','upper window')
 old.house_set(w);w.text(V(-.13,2.35,-.08),'17',.22);w.box(-.47,0,-.65,.94,.035,.53,'#4b5050','door mat')
 for x in [-2.0,1.90]:w.box(x,0,-.7,.30,.40,.40,'#53616a','porch planter');w.tube([V(x+.15,.35,-.5),V(x+.15,.95,-.5)],'#31544e',.15)

def pair(w,d):
 basecar(w,d['position'],d['yaw'],d['wheel_phase'],d['steer'],False,d['roll'],d['pitch'],d['brake']);basecar(w,d['pursuer_position'],d['pursuer_yaw'],d['pursuer_wheel_phase'],d['pursuer_steer'],True,d['pursuer_roll'],d['pursuer_pitch'],d['pursuer_brake'])
 for p,y in [(d['position'],d['yaw']),(d['pursuer_position'],d['pursuer_yaw'])]:
  R=RY(y);w.face([p+R@V(-.65,.008,2.12),p+R@V(.65,.008,2.12),p+R@V(1.6,.008,7.2),p+R@V(-1.6,.008,7.2)],'#304e5a',stroke='none',name='world headlight footprint')

def cockpit(w,d):
 old.cabin(w,d)
 # Cohesive dashboard components use the same cabin coordinates, never separate overlay illustrations.
 for x in [-.65,-.38,-.11]:
  ctr=V(x,.91,.756);w.tube([ctr+V(.075*math.cos(a),.055*math.sin(a),0) for a in np.linspace(0,math.tau,25)],'#7a9296',.007);needle=math.pi*.8-d['speed']/14*math.pi*1.5;w.line([ctr,ctr+V(.053*math.cos(needle),.041*math.sin(needle),-.004)],'#e9bd7e',2)
 w.text(V(.2,.74,.748),f"{round(d['speed']*3.6)}",.06)
 for x in [-.7,.6]:w.box(x,.72,.744,.16,.10,.018,'#102330','air vent')
 for side in [-1,1]:w.tube([V(side*.79,.61,-.20),V(side*.79,.61,.10)],'#728b91',.022);w.box(side*.82-.015,1.04,.55,.03,.17,.30,'#1a3543','side mirror')

def exit_car(w,d):
 temp=World(w.cam,w.t);temp.open_driver=True;v=VS.state(min(11,9+d['time']));basecar(temp,V(0,0,0),0,v['wheel_phase'],v['steer'],False,0,.01*(1-Q(d['time'],0,2)),v['brake'])
 for op in temp.ops:
  # Replace actual driver's side panel with a real opening and hinged leaf.
  if op[0]=='face' and len(op[1])==4 and all(abs(p[0]+.85)<1e-5 for p in op[1]) and max(p[1] for p in op[1])>.9:continue
  w.ops.append(op)
 # Solid fixed front/rear body panels, middle opening unobstructed.
 for z0,z1 in [(-2.15,-.66),(.71,2.05)]:w.face([V(-.85,.38,z0),V(-.85,.38,z1),V(-.85,.93,z1),V(-.85,.93,z0)],'#26485b','#54717f',3,name='body beside door opening')
 H=V(-.85,.65,.70);R=RY(d['door_angle']);T=lambda q:H+R@np.array(q)
 w.face([T(V(0,-.28,0)),T(V(0,-.28,-1.35)),T(V(0,.28,-1.35)),T(V(0,.28,0))],'#294b5e','#80939a',3,name='hinged driver door');w.face([T(V(0,.28,0)),T(V(0,.28,-1.35)),T(V(0,.72,-1.12)),T(V(0,.72,-.22))],'#294c5f','#80939a',3,name='driver door window');handle=np.asarray(d['car_handle']);w.tube([handle+R@V(0,0,.09),handle+R@V(0,0,-.09)],'#c3c6b7',.02)
 # Visible seat and footwell at the same coordinates as cockpit.
 w.box(-.62,.08,-.36,.48,.22,.55,'#294654','exit seat cushion');w.box(-.62,.30,-.46,.48,.72,.12,'#1c3543','exit seat back')

def bedroom(w,d):
 # Reuse detailed native-ready fabric geometry; replace its disconnected car registration.
 old.bedroom(d['time']) if False else None
 floor(w,-1.9,1.9,-2.3,.10)
 for x0,x1,y0,y1 in [(-1.9,-.77,0,2.8),(.77,1.9,0,2.8),(-.77,.77,0,.60),(-.77,.77,2.2,2.8)]:w.face([V(x0,y0,.10),V(x1,y0,.10),V(x1,y1,.10),V(x0,y1,.10)],'#233e4b',w=2,name='bedroom wall')
 w.box(1.0,0,-1.6,.82,.32,1.6,'#172e3d','bed');w.box(.98,.32,-1.6,.86,.14,1.6,'#496171','mattress');w.box(1.06,.46,-1.5,.65,.10,.35,'#9eaa9f','pillow');w.box(.56,.0,-1.4,.38,.55,.4,'#33484d','nightstand');sconce(w,V(.72,1.03,-1.55))
 # Real open doorway at z=-1.7; near back wall is a deliberate cutaway after entry coverage.
 if d['time']<1:
  for x0,x1 in [(-1.9,-.24),(.64,1.9)]:w.face([V(x0,0,-1.70),V(x1,0,-1.70),V(x1,2.8,-1.70),V(x0,2.8,-1.70)],'#233e4b',name='bedroom cutaway back wall')
 for x in [-.24,.60]:w.box(x,0,-1.74,.04,2.15,.08,'#9c8969','bedroom doorway jamb')
 w.box(-.24,2.10,-1.74,.88,.06,.08,'#9c8969','bedroom doorway lintel');H=V(-.20,0,-1.70);M=RY(math.radians(80));w.face([H+M@q for q in [V(0,0,0),V(.8,0,0),V(.8,2.1,0),V(0,2.1,0)]],'#1d3946','#7b8d8f',3,name='already open bedroom door')
 floor(w,-.50,.90,-2.80,-1.70);w.face([V(-.50,0,-2.8),V(-.50,0,-1.7),V(-.50,2.6,-1.7),V(-.50,2.6,-2.8)],'#1c3442',name='upper hallway side wall');w.box(-1.9,2.75,-2.3,3.8,.06,2.4,'#1b303b','ceiling')
 for j in range(65):
  x=-9+(j*3.17)%18;z=2+(j*2.37)%13;y=-2.73+(j*.23-w.t*4.1)%6
  w.line([V(x,y,z),V(x-.025,y-.24,z+.03)],'#607f90',1)
 # Street and sedan derived from the same parked world state, not unrelated local constants.
 w.face([V(-12,-2.73,2),V(12,-2.73,2),V(12,-2.73,15),V(-12,-2.73,15)],'#142f3f',w=1,name='registered street outside');basecar(w,d['sedan_position'],d['sedan_yaw'],VS.PARK['pursuer_wheel_phase'],0,True)
 for x in [-.76,.73]:w.box(x,.60,.03,.03,1.60,.09,'#83958e','window jamb')
 for y in [.60,2.17]:w.box(-.76,y,.03,1.52,.035,.09,'#83958e','window lintel')
 w.box(-.82,.56,-.08,1.64,.05,.20,'#9a9e8b','window sill');w.tube([V(-.86,2.23,-.21),V(.86,2.23,-.21)],'#bea977',.025)
 for xx in [-.86,.86]:w.tube([V(xx,2.23,.03),V(xx,2.23,-.21)],'#8c815f',.018)
 mesh=d['fabric'];nr,nc=np.array(mesh).shape[:2]
 for row in range(nr-1):
  for col in range(nc-1):
   a,b,c,e=mesh[row,col],mesh[row,col+1],mesh[row+1,col+1],mesh[row+1,col];normal=np.cross(b-a,e-a);normal/=max(1e-10,np.linalg.norm(normal));shade=float(normal@V(.65,.15,-.72));palette=['#243e4d','#304d5c','#3a5968','#486b78','#5b7b87','#708d96'];cc=palette[int(np.clip((shade+1)*2.5,0,5))];w.face([a,b,c,e],cc,stroke='none',name='rigged curtain fold')
 for col in range(0,nc,6):
  top=mesh[0,col];w.tube([top,top+V(0,.08,0)],'#c5b68f',.009);None # material curvature supplies fold shading; avoid blind-like ink bars
 w.line(list(mesh[-1]),'#748892',2);w.line(list(mesh[:,-1]),'#8194a0',2)


def door_live(w,d):
 start=len(w.ops);old.door_geometry(w,d)
 # Suppress only duplicate projected door-number glyphs; key/handle are actual geometry.
 w.ops[start:]=[op for op in w.ops[start:] if op[0]!='glyph']
 if d.get('inside'):
  R=np.array(d['door_R'])@RZ(d['keyturn']);c=old.key_test.HINGE+np.array(d['door_R'])@V(-.75,1.16,.105);w.tube([c+R@V(-.024,0,0),c+R@V(.024,0,0)],'#c7aa70',.012)


def street_details(w):
 # Unique fixed addresses, drain grates and pools of warm streetlight.
 for k,z in enumerate(range(-40,141,10)):
  if not in_view(w,V(VS.roadref(z),1,z),11):continue
  for side in [-1,1]:
   P=lambda x,y,zz:V(VS.roadref(zz)+x,y,zz)
   for j in range(4):
    w.line([P(side*4.42,.015,z+j*.055),P(side*4.1,.015,z+j*.055)],'#0b1b25',2)
   for j in range(3):
    w.face([P(side*(3.1+j*.16),.012,z+5+j*.45),P(side*(3.7+j*.16),.012,z+5+j*.45),P(side*(3.6+j*.16),.012,z+5.15+j*.45),P(side*(3.0+j*.16),.012,z+5.15+j*.45)],['#6b6653','#7e775b','#5e665e'][j],stroke='none',name='broken amber wet reflection')
   if k%3==0:
    w.box(VS.roadref(z)+side*5.4,.13,z+3,.30,.65,.30,'#294a4d','street waste bin')
   if k%4==1:
    for dz in [1.8,2.7]:w.tube([P(side*5.1,.13,z+dz),P(side*5.1,.75,z+dz)],'#7c8d8c',.028)
    w.tube([P(side*5.1,.75,z+1.8),P(side*5.1,.75,z+2.7)],'#7c8d8c',.028)


_CITY_M09=city
def city(w):
 _CITY_M09(w)
 # Two fixed route landmarks, consistent between exterior and windshield views.
 for z,label in [(12.,'NORTH'),(35.,'17')]:
  x=VS.roadref(z)+5.35
  if in_view(w,V(x,1.2,z),3):
   w.tube([V(x,.13,z),V(x,2.15,z)],'#7a8c91',.035);w.box(x-.28,1.75,z-.035,.56,.35,.07,'#274c52','fixed route marker');w.text(V(x,1.92,z-.08),label,.09,'#d2bea0')
   for dz in [.1,.4,.7]:w.face([V(VS.roadref(z)+3.5,.014,z+dz),V(VS.roadref(z)+4.1,.014,z+dz),V(VS.roadref(z)+4.0,.014,z+dz+.06),V(VS.roadref(z)+3.4,.014,z+dz+.06)],'#6b6b58',stroke='none',name='landmark wet light')
_HOUSE_M09=house_exterior
def house_exterior(w):
 _HOUSE_M09(w)
 # Interior hallway connects toward a right-hand stair flight, preserving door/lock geometry.
 floor(w,-.6,1.55,1.5,2.9)
 for i in range(3):w.box(.55+i*.30,0,1.9,.30,.18*(i+1),.85,'#435761','hall stair continuation')
 w.tube([V(.53,.95,2.72),V(1.45,1.49,2.72)],'#bea16b',.035)
 w.box(-.62,0,1.5,.06,2.5,1.4,'#243f4b','hallway wall');sconce(w,V(-.55,1.85,2.0))
