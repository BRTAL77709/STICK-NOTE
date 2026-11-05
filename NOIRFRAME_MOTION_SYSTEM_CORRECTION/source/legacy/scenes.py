import actions as act
from actions import *
from world import *
from character import actor,hand
from environments import *
from vehicles import *

def door(w,t,inside=False):
 q=lambda u,y,z=0:contact.doorpoint(t,u,y,z)
 w.face([q(.9,0),q(0,0),q(0,2.1),q(.9,2.1)],'#193744','#8a978f',4,name='hinged door')
 for lo,hi in [(.17,.84),(1.12,1.93)]:w.face([q(.78,lo,-.008),q(.12,lo,-.008),q(.12,hi,-.008),q(.78,hi,-.008)],'#213f4b','#5a7580',2,bias=-.01,name='door panel')
 z=.065 if inside else -.065
 for y in [.28,1.78]:w.tube([q(.015,y-.05),q(.015,y+.05)],'#a39e83',.025)
 spindle=q(.75,1.05,z);hole=q(.75,1.25,z)
 for p in [spindle,hole]:w.box(*(p+V(-.025,-.035,-.008)),.05,.07,.015,'#cfaa6c','lock plate')
 w.tube([spindle,contact.handle(t,inside)],'#e9c58a',.022);w.tube([hole+V(0,-.014,-.018),hole+V(0,.014,-.018)],'#030c18',.012)
 if inside:
  p=q(.75,1.30,z)+V(-.07*E(t,9.7,10),0,0);w.tube([q(.83,1.30,z),q(.67,1.30,z)],'#a6b4b2',.022);w.tube([p+V(0,-.035,0),p+V(0,.035,0)],'#e2be82',.025)

def key(w,d):
 if not d['keyvisible']:return
 b=d['keybow'];th=d['keyturn'];pts=[b+V(.047*math.cos(j*math.tau/24)*math.cos(th)-.027*math.sin(j*math.tau/24)*math.sin(th),.047*math.cos(j*math.tau/24)*math.sin(th)+.027*math.sin(j*math.tau/24)*math.cos(th),0) for j in range(25)];w.tube(pts,'#e4c080',.008);tip=d['keytip'].copy();tip[2]=min(-.065,tip[2]);w.tube([b,tip],'#ddbb75',.009)
 if d['keytip'][2]<-.065:w.tube([d['keytip']+V(0,0,-.025),d['keytip']+V(.025*math.cos(th),.025*math.sin(th),-.025)],'#ddbb75',.009)

def house_scene(t):
 d=house(t);u=d['contact_time'];inside=u>=7.8
 if 3.05<=u<4.94:cam=Camera((2.38,1.37,-.85),(1.85,1.17,-.01),1250);view='mechanism insert'
 elif 9.45<=u<10.25:cam=Camera((2.35,1.55,1.15),(1.85,1.28,.05),1250);view='inside bolt'
 elif inside:cam=Camera((.3,1.65,2.5),(1.85,1.10,.1),1400);view='interior'
 else:
  dx=.8*(1-E(t,.4,3.25));cam=Camera((4.1-dx,1.85,-4.6),(1.65-dx,1.16,.0),1850);view='porch'
 w=World(cam,t);entrance(w,inside);w.cache_prefix=len(w.ops);w.cache_key=('HOUSE',inside,view,tuple(cam.eye),tuple(cam.target));door(w,u,inside)
 target=d['keybow'] if d['contact']=='key' else None;actor(w,d,target);key(w,d)
 if target is not None:hand(w,d['pose']['arms'][0]['wrist'],target)
 d['camera_view']=view;d['camera']={'eye':cam.eye.tolist(),'target':cam.target.tolist(),'focal':cam.focal}
 return w.render((lambda a:rain_overlay(a,t,65)) if not inside and view=='porch' else None),d,w

def stair_scene(t):
 d=stairs(t);r=d['pose']['root'];track=E(t,.8,8.2);cam=Camera((-1.65+1.4*track,2.10+1.10*track,-4.4),(.55+1.1*track,1.62+1.05*track,1.45),1630);w=World(cam,t);staircase(w);actor(w,d);d['camera']={'eye':cam.eye.tolist(),'target':cam.target.tolist(),'focal':cam.focal};return w.render(),d,w

def bedroom_scene(t):
 d=act.bedroom(t);d['mirror_head']=True;d['pose']['head'][0]-=.10*(E(t,1.3,2.25)-E(t,5.3,6.1));u=d['contact_time'];cam=Camera((3.5,4.60,5.2),(2.9,3.50,.10),1550);cam=Camera((3.35,4.6,.8),(3.95,1.0,-10),1250) if 4.50<=t<5.25 else cam;w=World(cam,t)
 # Stable outside street below the upper-storey window, with a life-size parked car.
 city(w,-8,22);car(w,(3.9,0,-10),0,0,black=True);bedroom(w);w.cache_prefix=len(w.ops);w.cache_key=('BEDROOM',tuple(cam.eye),tuple(cam.target))
 for j in range(36):
  f=j/36;g=(j+1)/36;pts=[contact.cloth(u,f,k/16) for k in range(17)]+[contact.cloth(u,g,k/16) for k in reversed(range(17))];w.face(pts,['#294b5b','#42677a','#1e3c50','#365c70'][j%4],stroke='none',bias=-.01,name='curtain cloth')
 for f in np.linspace(0,1,10):w.line([contact.cloth(u,f,k/24) for k in range(25)],'#7693a0' if round(f*9)%2 else '#10283b',1.4)
 w.tube([V(2.98,4.56,.075),V(4.42,4.56,.075)],'#b6b5a1',.023)
 for j in range(9):
  q=contact.cloth(u,j/8,1);pts=[q+V(.014*math.cos(k*math.tau/16),.045+.03*math.sin(k*math.tau/16),0) for k in range(17)];w.tube(pts,'#d4c7a6',.004)
 target=d['grip'] if d['cloth_contact'] else None;actor(w,d,target);return w.render(),d,w

def driving_scene(t):
 d=driving(t);o=np.array(d['position']);yaw=d['yaw'];co,si=math.cos(yaw),math.sin(yaw)
 def C(p):
  x,y,z=np.array(p);return o+V(x*co+z*si,y,z*co-x*si)
 if 5.5<=t<7.5:
  eye=C(V(3.4,3.2,-22));target=C(V(-.1,.75,-5.5));cam=Camera(eye,target,1200);w=World(cam,t);city(w,o[2]-8,32);car(w,o,yaw,d['wheel_angle'],d['steer'],False,d['body_roll']);car(w,d['pursuer_position'],yaw,d['wheel_angle']*.98,black=True,roll=d['body_roll']*.8);d['view']='exterior pursuit'
 else:
  if t<3:eye=V(.72,1.32,.20);target=V(-.35,.88,.15);focal=650;view='passenger medium'
  elif t<5.5:eye=V(.16,1.38,-.60);target=V(-.10,1.10,3.5);focal=750;view='over shoulder windshield'
  elif t<9:eye=V(.10,.34,.24);target=V(-.30,.13,.39);focal=1000;view='pedal insert'
  else:eye=V(.72,1.32,.20);target=V(-.35,.88,.15);focal=700;view='driver reaction'
  cam=Camera(C(eye),C(target),focal);w=World(cam,t);city(w,o[2]+20,35)
  lc=Camera(eye,target,focal);cab=World(lc,t)
  # Connected cabin surfaces and continuous steering column/dashboard.
  cab.box(-.85,.0,-.60,1.7,.04,2.0,'#142a37','footwell floor');cab.box(-.81,.30,.78,1.62,.68,.27,'#203e4e','dashboard');cab.box(-.83,.84,.90,1.66,.12,.27,'#365563','dash top')
  for side in [-1,1]:
   cab.box(side*.83-.025,.25,-.60,.05,.69,1.70,'#1b3544','door card');cab.tube([V(side*.70,1.02,.84),V(side*.62,1.46,.10)],'#587481',.06);cab.tube([V(side*.62,1.46,.10),V(side*.62,1.46,-.65)],'#304e5f',.06)
  # Driver and passenger seats with upright backs, no floating pelvis.
  for x in [-.38,.40]:
   cab.box(x-.24,.08,-.36,.48,.18,.55,'#294654','seat cushion');cab.box(x-.24,.25,-.46,.48,.72,.12,'#1c3543','seat back');cab.box(x-.15,.95,-.43,.30,.22,.10,'#31505c','headrest')
  # Wheel and hands share one exact rigid transform, steering ratio12:1.
  angle=d['steer']*12;center=V(-.38,.79,.56)
  def ring(a):return center+V(.245*math.cos(a+angle),.245*math.sin(a+angle),-.07*math.sin(a+angle))
  cab.tube([V(-.38,.82,.91),center],'#182c38',.065);cab.tube([ring(j*math.tau/40) for j in range(41)],'#98a6a6',.030)
  for a in [math.pi/6,5*math.pi/6,1.5*math.pi]:cab.tube([center,ring(a)],'#395361',.026)
  # Two actual pivoting pedals. Contact ankle follows accelerator press.
  pedal=V(-.22,.10,.61);press=d['throttle'];brake=d['brake'];footR=V(-.22-.30*brake,.10-.025*press-.035*brake,.31+.04*press+.04*brake);footL=V(-.64,.10,.17)
  for x,push in [(-.22,press),(-.52,brake)]:
   cab.tube([V(x,.08,.44),V(x,.18-.05*push,.35+.03*push)],'#778d96',.035);cab.face([V(x-.06,.087-.035*push,.36+.04*push),V(x+.06,.087-.035*push,.36+.04*push),V(x+.06,.103-.035*push,.46+.04*push),V(x-.06,.103-.035*push,.46+.04*push)],'#9fada9',w=2,name='pedal')
  ff=[{'sole':footR,'planted':False,'pitch':-.10*press},{'sole':footL,'planted':False,'pitch':-.08*brake}];r=V(-.38,.30,-.02);hands=[ring(math.pi/6),ring(5*math.pi/6)];fear=.3+.5*E(t,1.9,2.6)+.15*E(t,9.5,10.2);p=skeleton(r,ff,hands,.025,.45-.35*(E(t,2.0,2.8)-E(t,3.2,3.5)),fear,head_tilt=5*(E(t,2.0,2.5)-E(t,2.8,3.1)),head_lead=-.025*E(t,9,9.6),breath=.006*math.sin(t*7));
  for leg in p['legs']:leg['knee']=ik(leg['hip'],leg['ankle'],.37,.37,V(0,.5,1))
  ad={'time':t,'pose':p,'seated':True};actor(cab,ad)
  # Belt is attached to seated torso, coherent shoulder support.
  cab.tube([r+V(-.15,.52,-.015),r+V(.16,.02,-.015)],'#6c7c80',.030)
  # Rearview mirror uses actual pursuer state gap. Illustrated optical inset.
  mirror=V(.0,1.30,.34);cab.box(-.22,1.21,.34,.44,.15,.035,'#071823','rearview mirror');cab.tube([V(0,1.37,.28),V(0,1.46,.10)],'#59717b',.018)
  # Reflected pursuer silhouette scales with measured world distance, no arbitrary growth.
  rw=.13*18/d['gap'];pts=[V(-rw,1.23,.325),V(rw,1.23,.325),V(rw*.8,1.29,.325),V(-rw*.8,1.29,.325)];cab.face(pts,'#284a60','#8eabb3',1,bias=-.02,name='mirror pursuer')
  for xx in [-rw*.65,rw*.65]:cab.tube([V(xx-.018,1.244,.318),V(xx+.018,1.244,.318)],'#e2e9d4',.007)
  cab.text(V(-.38,.97,.765),str(round(d['speed_kmh']))+' km/h',.050,'#a5d5d3')
  # Transform cabin geometry and IK into the vehicle world, same camera projection.
  for op in cab.ops:
   if op[0]=='face':w.ops.append((op[0],[C(p) for p in op[1]],*op[2:]))
   elif op[0]=='line':w.ops.append((op[0],[C(p) for p in op[1]],*op[2:]))
   else:w.ops.append((op[0],[C(p) for p in op[1]],*op[2:]))
  w.geometry.extend(cab.geometry);d['pose']=p;d['wheel_contacts']=[h.tolist() for h in hands];d['pedal_contact']=[footR.tolist(),footL.tolist()];d['view']=view
 d['camera']={'eye':cam.eye.tolist(),'target':cam.target.tolist(),'focal':cam.focal}
 return w.render(lambda a:rain_overlay(a,t,65) if d['view']!='pedal insert' else None),d,w
SCENES={'HOUSE':house_scene,'STAIRS':stair_scene,'BEDROOM':bedroom_scene,'DRIVING':driving_scene}
