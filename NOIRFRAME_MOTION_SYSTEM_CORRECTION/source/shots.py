from world import *
from actor import actor
from environments import staircase,entrance
from contact_rig import *
import stair_test,key_test,vehicle_test
from geometry import city,car

def stair(t):
 d=stair_test.state(t);cam=Camera((4.5,4.6,.3),(2.45,3.25,1.42),1500);w=World(cam,t);staircase(w);w.cache_prefix=len(w.ops);w.cache_key='fixed_stair_background';actor(w,d);d['camera']={'eye':cam.eye,'target':cam.target,'fixed':True};return [w],d

def key(t):
 d=key_test.state(t);cam=Camera((2.42,1.41,-1.08),(1.85,1.16,-.05),1400);w=World(cam,t);entrance(w);w.cache_prefix=len(w.ops);w.cache_key='fixed_key_background';R=d['door_R'];D=lambda p:key_test.HINGE+R@np.array(p)
 front=[D(V(-.9,0,-.065)),D(V(0,0,-.065)),D(V(0,2.1,-.065)),D(V(-.9,2.1,-.065))];back=[D(V(-.9,0,.065)),D(V(0,0,.065)),D(V(0,2.1,.065)),D(V(-.9,2.1,.065))];w.face(front,'#193744','#83938b',4,name='door front');w.face(back,'#193744','#83938b',4,name='door back')
 for j in range(4):w.face([front[j],front[(j+1)%4],back[(j+1)%4],back[j]],'#213d47',w=3,name='door edge')
 for lo,hi in [(.17,.84),(1.12,1.93)]:w.face([D(V(-.78,lo,-.068)),D(V(-.12,lo,-.068)),D(V(-.12,hi,-.068)),D(V(-.78,hi,-.068))],'#213f4b','#5a7580',2,name='door panel')
 for y in [1.05,1.25]:
  p=D(V(-.75,y,-.071));w.face([p+R@V(-.027,-.040,0),p+R@V(.027,-.040,0),p+R@V(.027,.040,0),p+R@V(-.027,.040,0)],'#cfaa6c',w=2,name='lock escutcheon')
 hole=D(V(-.75,1.25,-.072));w.tube([hole+R@V(0,-.015,0),hole+R@V(0,.015,0)],'#030c18',.009)
 w.tube([d['spindle'],d['handle_end']],'#e9c58a',.022)
 # Actual local blade geometry is clipped at the lock face, not a floating key image.
 bow=d['keybow'];K=d['key_R'];points=[bow+K@V(.044*math.cos(j*math.tau/32),.027*math.sin(j*math.tau/32),0) for j in range(33)];w.tube(points,'#e5bf79',.008)
 length=min(.16,max(0,key_test.FACE-d['key_depth_local']));w.face([bow+K@V(-.008,0,0),bow+K@V(.008,0,0),bow+K@V(.008,0,length),bow+K@V(-.008,0,length)],'#d8b06b',w=1,name='flat key blade');w.tube([bow,bow+K@V(0,0,length)],'#dcb470',.008)
 for dz in [.12,.142,.158]:
  if d['key_depth_local']+dz<key_test.FACE:
   w.tube([bow+K@V(0,0,dz),bow+K@V(.018,0,dz)],'#e4bc76',.008)
 # Retracting latch belongs to the same leaf frame.
 w.tube([D(V(-.90,1.05,0)),D(V(-.925+d['latch_retraction'],1.05,0))],'#b6c0b8',.024)
 actor(w,d);d['camera']={'eye':cam.eye,'target':cam.target,'fixed':True};return [w],d

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
 rw=.10*12/d['gap'];w.face([V(-rw,1.22,.265),V(rw,1.22,.265),V(rw*.8,1.28,.265),V(-rw*.8,1.28,.265)],'#284a60','#8eabb3',1,name='pursuer reflection')

def driving(t):
 d=vehicle_test.state(t);R=RY(d['yaw'])@RZ(d['roll'])@RX(d['pitch']);o=np.array(d['position']);pivot=V(0,.55,0)
 def C(p):return o+RY(d['yaw'])@(pivot+(RZ(d['roll'])@RX(d['pitch']))@(np.array(p)-pivot))
 lc=Camera((.65,1.17,-.25),(-.32,.88,.52),780,center=(540,440));cam=Camera(C(lc.eye),C(lc.target),780,center=(540,440),up=R@V(0,1,0));w=World(cam,t);city(w,12,35);cw=World(lc,t);cabin(cw,d)
 for op in cw.ops:w.ops.append((op[0],[C(p) for p in op[1]],*op[2:]))
 # Fixed world camera proves actual movement/curvature, synchronized with the upper view.
 ec=Camera((3.8,24,7),(2.5,0,7),600,center=(540,480));ext=World(ec,t);city(ext,12,35);ext.cache_prefix=len(ext.ops);ext.cache_key='fixed_city';car(ext,d['position'],d['yaw'],d['wheel_phase'],d['steer'],False,d['roll'],d['pitch']);car(ext,d['pursuer_position'],d['pursuer_yaw'],d['pursuer_wheel_phase'],d['pursuer_steer'],True,d['pursuer_roll'],d['pursuer_pitch'])
 d['camera']={'cockpit_parent':'vehicle full rigid body transform','exterior_fixed':True,'same_state_two_views':True};d['camera_projection_agreement_px']=float(np.linalg.norm(np.array(lc(d['wheel_center']))-cam(C(d['wheel_center']))));return [w,ext],d
SHOTS={'STAIR_CONTACT':(stair,3.),'KEY_HANDLE':(key,3.),'STEERING_TURN':(driving,4.)}
