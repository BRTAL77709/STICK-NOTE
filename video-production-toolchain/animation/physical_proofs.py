"""Five exposed physical performances. Picture, contacts and evidence share this evaluator.
No camera motion in A/C/D/E. Vehicle B has independent SI odometry and tracking.
"""
import math
import numpy as np
from illustration_engine import Art
from approved_components import begin,limb,ik
from driver_rig import head
from motion_state import ease,clamp
import motion_state as motion
from world import Camera,city,INK
from vehicle import sedan
from render_base import rain
import articulated as rig
import house_actions as door
import room_actions as room
from scene_declarations import DEFS

def mix(A,B,q):return tuple(a+(b-a)*q for a,b in zip(A,B))
def remap(t,knots):
 if t<=knots[0][0]:return knots[0][1]
 for (a,x),(b,y) in zip(knots,knots[1:]):
  if t<=b:return x+(y-x)*(t-a)/(b-a)
 return knots[-1][1]
DURATIONS={'A':3.,'B':4.,'C':9.,'D':4.,'E':4.}
DOOR_KNOTS=[(0,0),(.6,.22),(.88,.34),(1.03,.4),(1.35,.62),(1.65,.8),(1.95,1),(2.15,1.12),(2.65,1.3),(3.15,1.5),(3.65,1.72),(3.85,1.76),(4.35,1.98),(4.5,2),(4.7,2.12),(5.1,2.3),(5.45,2.55),(5.8,2.73),(6.05,2.84),(6.1,2.85),(6.4,3.05),(6.65,3.25),(7.2,3.55),(7.45,3.65),(7.65,3.83),(8.1,4.17),(8.35,4.3),(8.5,4.36),(9.15,4.95),(9.7,5.55),(10.2,6.18),(10.4,6.4)]
CLOTH_KNOTS=[(0,60.85),(.6,61.35),(1.15,61.6),(2.7,62.2),(2.95,62.35),(3.65,62.65),(4,63.05)]

def accelerator(t):
 press=ease(t,.9,1.9)-.15*ease(t,2.3,2.7);angle=math.radians(24)*press
 hinge=(835.,1540.);planted=(540.,1530.);L=400.;direction=(math.sin(angle),-math.cos(angle));delta=(hinge[0]-planted[0],hinge[1]-planted[1]);dot=sum(x*y for x,y in zip(delta,direction));r=-dot+math.sqrt(dot*dot-(sum(x*x for x in delta)-L*L));touch=(hinge[0]+r*direction[0],hinge[1]+r*direction[1]);theta=math.atan2(touch[1]-planted[1],touch[0]-planted[0]);q=ease(t,.25,.75);heel=mix((470.,1545.),planted,q);theta+=.09*(1-q)
 def local(x,y):return heel[0]+x*math.cos(theta)-y*math.sin(theta),heel[1]+x*math.sin(theta)+y*math.cos(theta)
 toe=local(L,0);ankle=local(65,-85);load=press*22+5*math.sin(max(0,t-1.9)*13)*math.exp(-max(0,t-1.9)*5)*ease(t,1.9,2.0);hip=(300+press*14,855-load*.45);knee=ik(hip,ankle,370,360,-1);shoulder=(270-load*.55,570+load*.25);headpos=(258-load*.7,365+load*.15)
 hands=[(560.,560.),(560.,740.)];shoulders=[(shoulder[0]-50,shoulder[1]),(shoulder[0]+80,shoulder[1]+10)];elbows=[ik(s,h,190,180,1 if j==0 else -1) for j,(s,h) in enumerate(zip(shoulders,hands))]
 return {'time':t,'phase':'anticipation' if t<.25 else 'approach' if t<.75 else 'contact' if t<.9 else 'pressure' if t<1.9 else 'completion' if t<2.3 else 'follow-through','heel':heel,'toe':toe,'ankle':ankle,'hip':hip,'knee':knee,'shoulder':shoulder,'head':headpos,'hands':hands,'shoulders':shoulders,'elbows':elbows,'hinge':hinge,'pedal_contact':touch,'pedal_angle':angle,'shoe_angle':theta,'heel_planted':t>=.75,'contact':t>=.75,'pressure':press,'bone_lengths':[370,360]}
def draw_accelerator(a,t):
 p=accelerator(t);a.rect(0,0,1080,1920,'#0c2130');a.path('M40 900 L960 870 L1080 1740 H0Z','#203d49','#546d78',6)
 for j in range(10):a.line([(100+j*90,1020),(20+j*110,1740)],'#132b39',6)
 a.path('M70 380 Q125 300 225 360 L420 865 L160 940Z','#132b3a','#587381',10);a.rect(135,830,320,95,'#192e3a','#546d78',9,20)
 a.add(f'<g transform="rotate({math.degrees(p["pedal_angle"])} 835 1540)">');a.line([(835,1540),(835,1210)],'#839499',25);a.rect(775,1140,120,300,'#0b1925','#9ba49c',7,18)
 for j in range(6):a.line([(790,1170+j*44),(880,1170+j*44)],'#526d78',6)
 a.add('</g>');a.ellipse(835,1540,26,20,'#8f9e9d',INK,5)
 # Far leg stays supported on the floor while the working ankle rolls the near shoe.
 farhip=(p['hip'][0]-40,p['hip'][1]);farank=(390,1400);farknee=ik(farhip,farank,360,350,-1);limb(a,[farhip,farknee,farank],'#152c3b',90)
 a.path('M326 1450 Q345 1390 410 1405 L550 1467 Q590 1490 552 1515 H345Z','#0d2130',INK,10)
 sx,sy=p['shoulder'];hx,hy=p['hip'];a.path(f'M{sx-80} {sy-20} Q{sx+100} {sy-65} {sx+110} {sy+30} L{hx+90} {hy+25} Q{hx} {hy+70} {hx-80} {hy+10}Z','url(#cloth)',INK,10)
 a.path(f'M{sx-60} {sy-12} L{hx+65} {hy+18}','none','#6b7f85',13)
 for j in [0,1]:limb(a,[p['shoulders'][j],p['elbows'][j],p['hands'][j]],'#243e4e',38)
 a.ellipse(630,650,100,130,'none','#030b13',22);a.line([(630,650),(560,560)],'#779099',9);a.line([(630,650),(560,740)],'#779099',9)
 for h in p['hands']:a.ellipse(*h,19,23,'#d8ded1',INK,5)
 a.add(f'<g transform="translate({p["head"][0]} {p["head"][1]}) scale(1.1)">');head(a,0,0,t,.8,.8,.8,blink_override=max(0,1-abs(t-1.32)/.07));a.add('</g>')
 limb(a,[p['hip'],p['knee'],p['ankle']],'#294454',105)
 a.ellipse(*p['heel'],78,12,'#020c14',extra='opacity=".55"');a.add(f'<g transform="translate({p["heel"][0]} {p["heel"][1]}) rotate({math.degrees(p["shoe_angle"])})">');a.path('M0 0 Q-20 -60 30 -105 L100 -116 Q154 -70 250 -66 L380 -51 Q415 -40 411 -8 L400 0 H12Z','#152b3a',INK,11);a.line([(12,0),(400,0)],'#7d9096',6)
 for x in [130,170,210,250]:a.line([(x,-69),(x+20,-28)],'#82949a',4)
 a.add('</g>')

def vehicle_state(t):
 dist=2*t+5*motion.integral(t,.4,3.6);v=2+5*ease(t,.4,3.6);acc=5*motion.derivative(t,.4,3.6);table,keys=motion._LANES[1.55];_,x,z,yaw,cur=motion.sample_table(table,keys,motion.CORNER_S+6+dist);cur=cur/(1-1.55*cur)
 return {'t':t,'x':x,'z':z,'yaw':yaw,'heading':yaw,'speed_mps':v,'speed_kmh':v*3.6,'acceleration_mps2':acc,'distance_m':dist,'wheel_rad':dist/.32,'steer_rad':math.atan(2.7*cur),'pitch':.018*(.7*acc+.3*5*motion.derivative(max(0,t-.12),.4,3.6)),'roll':cur*v*v*.02,'suspension_m':.008*math.sin(dist*2.2),'rpm':950+v*3.6*65,'throttle':.8}
def vehicle_camera(t):
 s=vehicle_state(t);start=vehicle_state(0);ang=start['yaw'];sx=start['x']-6*math.cos(ang)-6*math.sin(ang);sz=start['z']+6*math.sin(ang)-6*math.cos(ang);cx=sx+.65*s['distance_m']*math.sin(ang);cz=sz+.65*s['distance_m']*math.cos(ang);initial=math.atan2(start['x']-sx,start['z']-sz);bearing=math.atan2(s['x']-cx,s['z']-cz);yaw=initial+.8*(bearing-initial)
 return Camera(cx,cz,1.35,yaw,1500,900)
def draw_vehicle(a,t):
 s=vehicle_state(t);c=vehicle_camera(t);city(a,c,t,traffic=[((s['x'],.8,s['z']),lambda:sedan(a,c,t,vehicle_state=s))]);rain(a,t)

def door_state(t):
 u=remap(t,DOOR_KNOTS);c=door.camera(0) if t<=8.5 else door.camera(u);d=door.actor_state(u,c);p=d['pose'];rock=math.sin(math.pi*ease(t,.88,1.65));hip=(p['hip'][0]+11*rock,p['hip'][1]+8*rock);hands={j:q['hand'] for j,q in enumerate(p['arms'])};new=rig.pose(51+t,hip,p['shoulder_center'][0]-p['hip'][0]+10*rock,[(q['sole'][0],q['sole'][1],q['planted'],q['shoe_scale']) for q in p['legs']],hands,p['head_yaw'],p['gaze'],p['fear'],p['blink']);new['wrist_angles']=p['wrist_angles'];d.update(pose=new,camera=c,reference_time=u,proof_time=t);return d

def draw_door(a,t,environment_time=None):
 d=door_state(t);u=d['reference_time'];c=d['camera'];inside=t>8.5;a.rect(0,0,1080,1920,'#122b39');c.poly(a,[(-7,0,-7),(7,0,-7),(7,0,7),(-7,0,7)],'#102532','#3c5663',3)
 # A real opening is cut from the fixed wall. Once inside, the owner is behind it.
 def actor():
  for foot,on in d['feet_world']:
   if on:
    x,y=c.project(foot);a.ellipse(x,y+2,24*d['scale'],4*d['scale'],'#030b13')
  rig.draw(a,d['x'],d['y'],d['scale'],d['pose'],back=inside);door.draw_key(a,c,d,u)
 behind=not inside and d['root'][2]>.03
 if behind:actor()
 for x1,x2,y1,y2 in [(-7,0,0,6),(1,7,0,6),(0,1,2.1,6)]:c.poly(a,[(x1,y1,.02),(x2,y1,.02),(x2,y2,.02),(x1,y2,.02)],'#183340','none',0)
 for yy in [j*.25 for j in range(1,24)]:
  for x1,x2 in [(-7,0),(1,7)]:c.line(a,[(x1,yy,0),(x2,yy,0)],'#2d4956',2)
 c.line(a,[(0,0,-.015),(0,2.1,-.015),(1,2.1,-.015),(1,0,-.015)],'#8c9e9c',15);door.leaf(a,c,u)
 if not behind:actor()
 if not inside:
  from approved_components import text
  x,y=c.project((.5,2.4,0));text(a,x,y,'17',58,'#efb367');rain(a,t if environment_time is None else environment_time)

def ik3(A,B,l1,l2,bend):
 A=np.asarray(A,float);B=np.asarray(B,float);d=float(np.linalg.norm(B-A));assert abs(l1-l2)<d<l1+l2,('3D reach',d,l1+l2);axis=(B-A)/d;v=np.asarray(bend,float);v-=axis*np.dot(v,axis);v/=np.linalg.norm(v);along=(l1*l1-l2*l2+d*d)/(2*d);return A+along*axis+math.sqrt(max(0,l1*l1-along*along))*v
STEP_PLANS=[[(.60,1.18,(.23,.18,-.10)),(2.35,2.93,(.99,.54,-.10))],[(1.47,2.05,(.61,.36,.10)),(3.20,3.72,(.90,.54,.10))]]
def stair_feet(t):
 out=[]
 for j in [0,1]:
  p=[(-.34,0,-.10),(-.18,0,.10)][j];on=True
  for a,b,B in STEP_PLANS[j]:
   if t<a:break
   if t<b:
    u=clamp((t-a)/(b-a));qx=ease(u,.25,.90);qy=ease(u,0,.55);p=(p[0]+(B[0]-p[0])*qx,p[1]+(B[1]-p[1])*qy+.12*math.sin(math.pi*u),p[2]+(B[2]-p[2])*qx);on=False;break
   p=B
  out.append((p,on))
 return out

def stair_state(t,base=0):
 # Support transfer follows each foot's landing. Lift and extension are distinct phases.
 fs=stair_feet(t);x=-.18-.03*ease(t,.1,.5)+.42*ease(t,1.18,1.47)+.36*ease(t,2.05,2.35)+.34*ease(t,2.93,3.2)+.01*ease(t,3.72,4)
 level=.18*(ease(t,1.18,1.47)+ease(t,2.05,2.35)+ease(t,2.93,3.2));crouch=.07*ease(t,.18,.6)*(1-ease(t,3.72,4));hip=np.array((x,base+level+.62-crouch,0.));lean=.08*ease(t,.25,.6)*(1-ease(t,3.5,4));shoulder=hip+np.array((lean,math.sqrt(.55**2-lean**2),0));headp=shoulder+np.array((.02,.32,0));legs=[]
 fs=[((p[0],p[1]+base,p[2]),on) for p,on in fs]
 for j,(p,on) in enumerate(fs):
  pitch=0.
  for start,end,target in STEP_PLANS[j]:
   if start-.13<=t<start:pitch=math.radians(14)*ease(t,start-.13,start)
   elif start<=t<end:pitch=math.radians(14)*(1-ease(t,start,start+.18))
  H=hip+np.array((0,0,(-.10,.10)[j]));ank=np.asarray(p)+np.array((.141*(1-math.cos(pitch))+.045*math.sin(pitch),.141*math.sin(pitch)+.045*math.cos(pitch),0));knee=ik3(H,ank,.40,.40,(1,0,0));legs.append({'hip':H,'knee':knee,'ankle':ank,'sole':p,'planted':on,'pitch':pitch,'toe_contact':(p[0]+.141,p[1],p[2])})
 arms=[]
 for j in [0,1]:
  sh=shoulder+np.array((0,0,(-.15,.15)[j]));hand=hip+np.array((.10+.10*math.sin(t*4+j*math.pi),.28+.07*math.sin(t*4+j*math.pi),(-.18,.24)[j]));el=ik3(sh,hand,.39,.38,(-1,0,1 if j else -1));arms.append({'shoulder':sh,'elbow':el,'hand':hand})
 def project(p):return 320+500*p[0]-150*p[2],1690-500*(p[1]-base)+65*p[2]
 # Drawing uses projected joints; the bone solve above remains in metric world space.
 origin=project((0,base,0));sc=500*.00442
 def local(p):p=project(p);return ((p[0]-origin[0])/sc,(p[1]-origin[1])/sc)
 pp={'t':t,'hip':local(hip),'shoulder_center':local(shoulder),'head':local(headp),'head_yaw':.72,'gaze':.9,'fear':.85,'blink':max(0,1-abs(t-2.2)/.07),'legs':[dict(hip=local(l['hip']),knee=local(l['knee']),ankle=local(l['ankle']),sole=local(l['sole']),planted=l['planted'],shoe_scale=1,shoe_angle=math.degrees(l['pitch'])) for l in legs],'arms':[{k:local(v) for k,v in q.items()} for q in arms]}
 return {'time':t,'root':hip,'feet':fs,'legs_world':legs,'arms_world':arms,'hip_world':hip,'shoulder_world':shoulder,'head_world':headp,'pose':pp,'x':origin[0],'y':origin[1],'scale':sc,'base':base,'project':project,'phase':'anticipation' if t<.6 else 'climb' if t<3.2 else 'follow-through'}
def draw_stairs(a,t,base=0):
 d=stair_state(t,base);P=d['project'];a.rect(0,0,1080,1920,'#142e3c')
 def poly(ps,col,stroke='#72908f',w=3):a.poly([P(p) for p in ps],col,stroke,w)
 poly([(-.6,base,.45),(1.5,base,.45),(1.5,base+3.3,.45),(-.6,base+3.3,.45)],'#1b3744','#3e5d68')
 for j in range(1,12):a.line([P((-.6,base+j*.25,.448)),P((1.5,base+j*.25,.448))],'#294958',2)
 poly([(-.6,base,-.5),(0,base,-.5),(0,base,.45),(-.6,base,.45)],'#284552')
 for n in range(1,4):
  x0=(n-1)*.38;x1=n*.38;y=base+n*.18
  poly([(x0,y,-.45),(x1,y,-.45),(x1,y,.45),(x0,y,.45)],'#3b5862')
  poly([(x0,y-.18,-.45),(x0,y,-.45),(x0,y,.45),(x0,y-.18,.45)],'#203e4d')
  poly([(x0,base,-.45),(x1,base,-.45),(x1,y,-.45),(x0,y,-.45)],'#244451','#546d79',3)
 for j in range(4):
  x=j*.38;a.line([P((x,base+max(.18,x*.473),.46)),P((x,base+1.05+x*.473,.46))],'#74928d',7)
 a.line([P((0,base+1.05,.46)),P((1.14,base+1.59,.46))],'#99aaa0',9)
 for p,on in d['feet']:
  if on:
   x,y=P(p);a.ellipse(x,y+2,55,9,'#030b13',extra='opacity=".55"')
 rig.draw(a,d['x'],d['y'],d['scale'],d['pose'])

def curtain_state(t,initial_feet=None):
 old=remap(t,CLOTH_KNOTS);d=room.actor_state(old,initial_feet=initial_feet);p=d['pose'];pull=math.sin(math.pi*ease(t,1.15,2.7));hands={j:q['hand'] for j,q in enumerate(p['arms'])};hands[0]=(p['hip'][0]-43-28*pull,p['hip'][1]-10-42*pull)
 hip=(p['hip'][0]-8*pull,p['hip'][1]+5*pull);lean=p['shoulder_center'][0]-p['hip'][0]-6*pull
 new=rig.pose(old,hip,lean,[(q['sole'][0],q['sole'][1],q['planted'],q['shoe_scale']) for q in p['legs']],hands,.20+.8*ease(t,1.65,2.9),.2+.8*ease(t,1.45,2.45),.45+.5*ease(t,2.4,3.2),p['blink']);d.update(pose=new,reference_time=old,proof_time=t);return d

def draw_curtain(a,t,initial_feet=None):
 old=remap(t,CLOTH_KNOTS)
 # draw() accepts a solved owner so no monkey-patched or independent prop animation exists.
 room.draw(a,old,actor_override=curtain_state(t,initial_feet=initial_feet))

def svg(kind,t):
 a=Art();begin(a);a.add(DEFS)
 {'A':draw_accelerator,'B':draw_vehicle,'C':lambda a,t:draw_door(a,min(t,8.5),environment_time=t),'D':draw_stairs,'E':draw_curtain}[kind](a,t);a.add('</svg>');return ''.join(a.s)
