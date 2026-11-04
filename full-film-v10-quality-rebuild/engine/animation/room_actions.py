"""Continuous upper-room walk, fabric grip, device pickup and physical listening beats."""
import math
from motion_state import ease,clamp,state
from house_actions import DoorCamera
import house_site as site
import stairs_actions
import articulated as rig
from world import Camera,city,INK
from house17 import DownCamera
from vehicle import sedan
from render_base import rain
FLOOR=2.7;ENTER=stairs_actions.END
PHONE=(-.05,FLOOR+.75+31.28*site.UNIT,.65)

def mix(A,B,q):return tuple(a+(b-a)*q for a,b in zip(A,B))
def root(t):
 q=ease(t,ENTER,61.35);x=-1.05-.45*q+.80*ease(t,61.6,62.2);z=1.3375-.8875*q+.52*ease(t,77.0,77.6)
 return x,FLOOR,z
PLANS=[[(ENTER,61.11,(-1.40,FLOOR,.83)),(61.22,61.38,(-1.40,FLOOR,.45)),(61.6,61.85,(-.90,FLOOR,.45)),(77.0,77.3,(-.90,FLOOR,.96))],[(61.03,61.29,(-1.58,FLOOR,.47)),(61.82,62.12,(-.60,FLOOR,.45)),(77.25,77.6,(-.50,FLOOR,1.02))]]
START=[(-1.05,FLOOR,1.475),(-1.05,FLOOR,1.20)]
def feet(t):
 out=[]
 for j in [0,1]:
  p=START[j];on=True
  for a,b,B in PLANS[j]:
   if t<a:break
   if t<b:
    q=ease(t,a,b);p=mix(p,B,q);p=(p[0],p[1]+.10*math.sin(math.pi*q),p[2]);on=False;break
   p=B
  out.append((p,on))
 return out

def camera(t):
 targetx=-1.0;A=site.door_world((-.60,FLOOR+1.25,3.5));B=site.door_world((targetx,0,0));return DoorCamera(Camera(A[0],A[2],A[1],math.atan2(B[0]-A[0],B[2]-A[2]),1250,960))
def curtain_edge(t):return -1.85+.73*ease(t,61.6,62.2)
def device_rest(t):
 amp=.007*ease(t,63.1,63.18)*(1-ease(t,64.05,64.15));angle=-12+1.5*math.sin(t*66)*amp/.007 if amp else -12;bottom=abs(14*math.sin(math.radians(angle)))+29*math.cos(math.radians(angle));return (PHONE[0]+amp*math.sin(t*66),FLOOR+.75+bottom*site.UNIT,PHONE[2]),angle

def actor_state(t):
 c=camera(t);r=root(t);x,y=c.project(r);scale=c.f/c.depth(r)*site.UNIT
 walk=math.sin(math.pi*ease(t,ENTER,61.35));pull=math.sin(math.pi*ease(t,61.6,62.2));reach=ease(t,63.65,64.15)*(1-ease(t,64.2,65.1));offer=ease(t,67.7,68.4)*(1-ease(t,69.1,69.8));threat=ease(t,75.0,75.6)
 hip=-150+15*walk+15*pull+22*reach+12*offer+14*threat;hipx=-7*offer-8*threat
 breath=(1-.6*threat)*(1.6*math.sin(t*2.4));hip+=breath
 lean=18*walk-20*pull-18*reach-12*offer-18*threat+4*math.sin((t-75.6)*9)*math.exp(-max(0,t-75.6)*3)*threat
 shx=hipx+lean;shy=hip-math.sqrt(125**2-lean**2);nod=4*ease(t,63.25,64)*(1-ease(t,65.1,65.6))
 yaw=.25+.65*ease(t,61.80,62.15)-1.45*ease(t,63.20,63.6)+.20*ease(t,64.8,65.6)+.40*ease(t,67.8,68.4)+.65*ease(t,69.2,69.8)*(1-ease(t,70.0,70.6))+.65*ease(t,75.15,75.65)
 gaze=.30+.65*ease(t,61.65,62.0)-1.45*ease(t,63.1,63.45)+.25*ease(t,64.65,65.3)+.40*ease(t,67.65,68.1)+.65*ease(t,69.05,69.5)*(1-ease(t,70.0,70.5))+.70*ease(t,74.95,75.3)
 fear=.45+.40*ease(t,62.05,62.35)+.15*threat
 hands={0:(hipx-43,hip-10),1:(hipx+45,hip-10)}
 # Free hand balances the approach, then expresses shock, hesitation and fear.
 hands[0]=(hands[0][0]-20*walk,hands[0][1]-25*walk)
 chest=ease(t,67.7,68.35)*(1-ease(t,69.1,69.6))+ease(t,75.1,75.7);chest=clamp(chest)
 gesture=ease(t,70.2,71.0)*(1-ease(t,71.7,72.4));hands[1]=mix(hands[1],(shx+12,shy+85),chest);hands[1]=mix(hands[1],(shx+75,shy+110),gesture)
 cloth=(curtain_edge(t),FLOOR+1.30,-.03);cx,cy=c.project(cloth);clothhand=((cx-x)/scale,(cy-y)/scale)
 if t<61.6:hands[1]=mix(hands[1],clothhand,ease(t,61.35,61.6))
 elif t<62.35:hands[1]=clothhand
 elif t<62.65:hands[1]=mix(clothhand,(shx+10,shy+100),ease(t,62.35,62.65))
 elif t<63.35:hands[1]=mix((shx+10,shy+100),hands[1],ease(t,62.65,63.35))
 phone,angle=device_rest(t);px,py=c.project(phone);phone_local=((px-x)/scale,(py-y)/scale);ear=(shx-64,shy-48+nod)
 if 63.6<=t<64.2:hands[0]=mix(hands[0],phone_local,ease(t,63.6,64.15))
 elif 64.2<=t<64.95:hands[0]=mix(phone_local,(shx-80,shy+65),ease(t,64.2,64.95))
 elif 64.95<=t<65.8:hands[0]=mix((shx-80,shy+65),ear,ease(t,64.95,65.8))
 elif t>=65.8:hands[0]=ear
 targets=[]
 for p,on in feet(t):
  fx,fy=c.project(p);targets.append(((fx-x)/scale,(fy-y)/scale,on,c.depth(r)/c.depth(p)))
 p=rig.pose(t,(hipx,hip),lean,targets,hands,yaw,gaze,fear,blink=max(0,1-abs(t-62.26)/.065)+max(0,1-abs(t-68.16)/.065)+max(0,1-abs(t-75.33)/.065));p['head']=(p['head'][0],p['head'][1]+nod);p['wrist_angles']={1:25*gesture-10*chest}
 held=t>=64.2
 if held:
  phone_pixel=(x+scale*hands[0][0],y+scale*hands[0][1]);table_scale=c.f/c.depth(phone)*site.UNIT;q=ease(t,64.2,64.95);phone_scale=table_scale*(1-q)+scale*q;angle=-12*(1-q)
 else:phone_pixel=(px,py);phone_scale=c.f/c.depth(phone)*site.UNIT
 return {'root':r,'camera':c,'pose':p,'x':x,'y':y,'scale':scale,'feet':feet(t),'cloth':cloth,'cloth_contact':61.6<=t<62.35,'phone_pixel':phone_pixel,'phone_scale':phone_scale,'phone_angle':angle,'phone_held':held,'phone_grip':t>=64.15,'ear_contact':t>=65.8,'head_ear_local':(p['head'][0]-66,p['head'][1]+24),'ear_point_local':(p['head'][0]-52,p['head'][1]+13),'phone_owner':0}

def room_box(a,c,ps,color,stroke=INK,w=3):c.poly(a,ps,color,stroke,w)
def table(a,c):
 x,z=PHONE[0],PHONE[2];top=FLOOR+.75
 c.poly(a,[(x-.25,FLOOR,z+.2),(x+.25,FLOOR,z+.2),(x+.25,top,z+.2),(x-.25,top,z+.2)],'#193542','#526d78',4)
 c.poly(a,[(x-.25,FLOOR,z-.2),(x-.25,FLOOR,z+.2),(x-.25,top,z+.2),(x-.25,top,z-.2)],'#132b39','#526d78',3)
 c.poly(a,[(x-.25,top,z-.2),(x+.25,top,z-.2),(x+.25,top,z+.2),(x-.25,top,z+.2)],'#365361','#859893',4)
 c.line(a,[(x-.18,FLOOR+.52,z+.202),(x+.18,FLOOR+.52,z+.202)],'#6c838b',2)

def bed(a,c):
 c.poly(a,[(-2.9,FLOOR,1.7),(-1.7,FLOOR,1.7),(-1.7,FLOOR+.48,1.7),(-2.9,FLOOR+.48,1.7)],'#1c3544','#425e6b',5)
 c.poly(a,[(-2.9,FLOOR+.48,1.7),(-1.7,FLOOR+.48,1.7),(-1.7,FLOOR+.48,3.2),(-2.9,FLOOR+.48,3.2)],'#294756','#0a1721',5)
 for z in [1.9,2.2,2.5,2.8]:c.line(a,[(-2.85,FLOOR+.50,z),(-1.75,FLOOR+.50,z+.16)],'#3c5c6a',4)
def lamp(a,c):
 c.poly(a,[(.25,FLOOR,.85),(.75,FLOOR,.85),(.75,FLOOR+.85,.85),(.25,FLOOR+.85,.85)],'#1b3848','#536b74',4);c.line(a,[(.5,FLOOR+.85,.95),(.5,FLOOR+1.5,.95)],'#947649',8)
 c.poly(a,[(.27,FLOOR+1.5,.95),(.73,FLOOR+1.5,.95),(.65,FLOOR+1.92,.95),(.35,FLOOR+1.92,.95)],'#dbac70','#6c553b',4)
 x,y=c.project((.5,FLOOR+1.5,.95));a.ellipse(x,y,230,370,'url(#lamphalo)')
def curve(a,c,points,fill,stroke=INK,width=4):
 pp=[c.project(p) for p in points];a.path('M'+f'{pp[0][0]} {pp[0][1]}'+' C'+' '.join(f'{x} {y}' for x,y in pp[1:4])+' L'+f'{pp[4][0]} {pp[4][1]}'+' C'+' '.join(f'{x} {y}' for x,y in pp[5:8])+'Z',fill,stroke,width)
def curtains(a,c,t):
 top=-1.85+.73*ease(t-.08,61.6,62.2);middle=curtain_edge(t);bottom=-1.85+.73*ease(t-.13,61.6,62.2)
 curve(a,c,[(-1.03,5.40,-.03),(top,5.45,-.03),(middle,4.8,-.03),(middle,4.0,-.03),(bottom,3.55,-.03),(-1.05,3.50,-.03),(-1.02,4.5,-.03),(-1.03,5.4,-.03)],'#294c5a','#06121d',5)
 for j in range(1,6):
  q=j/6;c.line(a,[(-1.03+(top+1.03)*q,5.35,-.035),(-1.03+(middle+1.03)*q,4.0,-.035),(-1.03+(bottom+1.03)*q,3.60,-.035)],'#547582',2.2)
 c.poly(a,[(-2.22,5.4,-.025),(-2.10,5.4,-.025),(-2.08,3.55,-.025),(-2.22,3.6,-.025)],'#294c5a',INK,4)

def phone_draw(a,d):
 x,y=d['phone_pixel'];s=d['phone_scale'];angle=d['phone_angle'];a.add(f'<g transform="translate({x} {y}) scale({s}) rotate({angle})">');a.rect(-14,-44,28,73,'#07131d','#a2b0b0',3,5);a.rect(-9,-35,18,53,'#23414f');a.line([(-4,-38),(4,-38)],'#718f98',1.5)
 if d['phone_grip']:
  a.path('M14 9 Q22 -2 13 -11','none','#d8ded1',7)
  for j in range(3):a.path(f'M-14 {-12+j*7} q9 -4 13 1','none','#d8ded1',3)
 a.add('</g>')

def draw(a,t):
 d=actor_state(t);c=d['camera'];a.rect(0,0,1080,1920,'#122b39')
 a.add('<defs><clipPath id="room-window"><polygon points="'+ ' '.join(f'{x},{y}' for x,y in [c.project(p) for p in [(-2.2,3.7,0),(-1.05,3.7,0),(-1.05,5.3,0),(-2.2,5.3,0)]])+'"/></clipPath></defs>')
 corners=[c.project(p) for p in [(-2.2,3.7,0),(-1.05,3.7,0),(-1.05,5.3,0),(-2.2,5.3,0)]];left=min(p[0] for p in corners);right=max(p[0] for p in corners);top=min(p[1] for p in corners);bottom=max(p[1] for p in corners);scale=max((right-left)/1080,(bottom-top)/1920)
 eye=site.door_world((-1.625,FLOOR+1.52,0));b=state(62,True);outside=DownCamera(eye[0],eye[2],eye[1],math.atan2(b['x']-eye[0],b['z']-eye[2]),1700,1000,down=.48)
 a.add(f'<g clip-path="url(#room-window)"><g transform="translate({(left+right)/2} {(top+bottom)/2}) scale({scale}) translate(-540 -960)">');black=state(t,True);city(a,outside,t,traffic=[((black['x'],.8,black['z']),lambda:sedan(a,outside,t,True))]);rain(a,t);a.add('</g></g>')
 for x1,x2,y1,y2 in [(-5,-2.2,FLOOR,6),(-1.05,5,FLOOR,6),(-2.2,-1.05,FLOOR,3.7),(-2.2,-1.05,5.3,6)]:c.poly(a,[(x1,y1,.01),(x2,y1,.01),(x2,y2,.01),(x1,y2,.01)],'#122b39','none',0)
 c.poly(a,[(-5,FLOOR,0),(5,FLOOR,0),(5,FLOOR,4.0),(-5,FLOOR,4.0)],'#142d3a','#49626e',3)
 for x in [-2.2,-1.05]:c.line(a,[(x,3.7,-.015),(x,5.3,-.015)],'#83999c',10)
 for y in [3.7,4.5,5.3]:c.line(a,[(-2.2,y,-.015),(-1.05,y,-.015)],'#83999c',8)
 c.line(a,[(-1.625,3.7,-.015),(-1.625,5.3,-.015)],'#587783',5);c.line(a,[(-2.3,5.42,-.025),(-.95,5.42,-.025)],'#879a9a',10);curtains(a,c,t)
 def draw_actor():
  for p,on in d['feet']:
   if on:
    x,y=c.project(p);a.ellipse(x,y+2,22*d['scale'],4*d['scale'],'#030b13',extra='opacity=".55"')
  rig.draw(a,d['x'],d['y'],d['scale'],d['pose'])
 queue=[(c.depth((.5,FLOOR,1.0)),lambda:lamp(a,c)),(c.depth((-2.3,FLOOR,2.3)),lambda:bed(a,c)),(c.depth((PHONE[0],FLOOR,PHONE[2])),lambda:table(a,c)),(c.depth(d['root']),draw_actor)]
 for depth,fn in sorted(queue,key=lambda p:-p[0]):fn()
 phone_draw(a,d)
