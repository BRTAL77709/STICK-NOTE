"""Metric House 17 site and visible driver-door exit. All contacts share the site frame."""
import math
from motion_state import state,ease,clamp
from world import Camera,terrain,INK
from vehicle import sedan
from approved_components import text
import articulated as rig
ORIGIN=state(48);UNIT=1.90/430.;HOUSE_X=-7.2
EXIT=[(48.14,48.52,(-.46,.18,.77),(-1.55,0,.43)),(48.34,48.73,(-.43,.18,.85),(-1.35,0,.06))]
RUN_START=49.15;RUN_END=50.88;RUN_LENGTH=5.33

def W(x,y,z):
 h=ORIGIN['yaw'];return ORIGIN['x']+x*math.cos(h)+z*math.sin(h),y,ORIGIN['z']+z*math.cos(h)-x*math.sin(h)
def door_world(p):return W(HOUSE_X-p[2],.15+p[1],-.5+p[0])
def ground(x):return .15*ease(-x,4.15,4.8)
def local_camera(x,z,y,target_x,target_z,focal=1150,horizon=940):
 a=W(x,y,z);b=W(target_x,0,target_z);return Camera(a[0],a[2],y,math.atan2(b[0]-a[0],b[2]-a[2]),focal,horizon)
def wide_camera(t):return local_camera(3.5,-10,1.7,-3.4,0,1350,1080)
def run_camera(t):
 root=path(run_progress(t));return local_camera(-4.0,root[2]-4.5,1.45,root[0],root[2]+.15,1350,1050)
def exit_camera(t):return local_camera(-4.2,-2.4,1.15,-.9,.25,1050,940)

def car_door_angle(t):return math.radians(66)*ease(t,48.05,48.36)*(1-ease(t,48.88,49.14))
def car_leaf_point(t,u,y):
 q=car_door_angle(t);return W(-1.01-1.60*u*math.sin(q),y,.72-1.60*u*math.cos(q))
def car_handle(t):return car_leaf_point(t,.72,.87)
def car_door(a,c,t):
 def pp(u,y):return car_leaf_point(t,u,y)
 c.poly(a,[pp(0,.43),pp(1,.43),pp(1,1.02),pp(0,1.02)],'#3a5d70',INK,4)
 c.poly(a,[pp(0,1.02),pp(.88,1.02),pp(.73,1.48),pp(0,1.50)],'#102b3b','#78929c',3)
 c.line(a,[pp(.63,.87),pp(.80,.87)],'#c2c3b3',5)
 c.line(a,[pp(0,.45),pp(0,1.50)],'#78909a',3)

def facade(a,c,t):
 def poly(ps,col,stroke=INK,w=4):c.poly(a,[W(*p) for p in ps],col,stroke,w)
 # Side walls and connected roof retain the illustrated house silhouette in oblique views.
 for side in [-1,1]:poly([(HOUSE_X,.15,side*4),(HOUSE_X-9,.15,side*4),(HOUSE_X-9,6.3,side*4),(HOUSE_X,6.3,side*4)],'#102a37' if side>0 else '#193644','#476471',4)
 for side in [-1,1]:poly([(HOUSE_X,6.3,side*4.3),(HOUSE_X-9,6.3,side*4.3),(HOUSE_X-9,7.6,0),(HOUSE_X,7.6,0)],'#18313e' if side>0 else '#284451','#536e79',4)
 for y in [1.0,3.85]:
  poly([(HOUSE_X-4,y,-4.025),(HOUSE_X-5.15,y,-4.025),(HOUSE_X-5.15,y+1.6,-4.025),(HOUSE_X-4,y+1.6,-4.025)],'#0c2230','#728993',3)
 poly([(HOUSE_X,.15,-4),(HOUSE_X,.15,4),(HOUSE_X,6.3,4),(HOUSE_X,6.3,-4)],'#142f40','#63808b',5)
 poly([(HOUSE_X,6.3,-4.3),(HOUSE_X,7.6,0),(HOUSE_X,6.3,4.3)],'#203c4c','#6d8790',5)
 for z in [-2.7,1.8]:
  for y in [1.0,3.85]:
   poly([(HOUSE_X+.025,y,z),(HOUSE_X+.025,y,z+1.15),(HOUSE_X+.025,y+1.6,z+1.15),(HOUSE_X+.025,y+1.6,z)],'#9d7e51' if z<0 and y>3 else '#0a2130','#82949a',3)
   c.line(a,[W(HOUSE_X+.045,y+.8,z),W(HOUSE_X+.045,y+.8,z+1.15)],'#5b7480',3)
   c.line(a,[W(HOUSE_X+.045,y,z+.575),W(HOUSE_X+.045,y+1.6,z+.575)],'#5b7480',3)
 for j in range(10):c.line(a,[W(HOUSE_X+.01,.15+j*.6,-4),W(HOUSE_X+.01,.15+j*.6,4)],'#294958',1.4)
 poly([(HOUSE_X+.03,.15,-.5),(HOUSE_X+.03,.15,.5),(HOUSE_X+.03,2.25,.5),(HOUSE_X+.03,2.25,-.5)],'#203a49','#8d9b99',5)
 for y,h in [(.35,.62),(1.40,.60)]:poly([(HOUSE_X+.05,y,-.38),(HOUSE_X+.05,y,.38),(HOUSE_X+.05,y+h,.38),(HOUSE_X+.05,y+h,-.38)],'#17303f','#536b77',2)
 p=c.project(door_world((.5,2.45,0)));text(a,p[0],p[1],'17',max(23,c.f/max(1,c.depth(door_world((.5,2.45,0))))*.31),'#f0b969')
 c.line(a,[door_world((.84,.95,-.04)),door_world((.98,.95,-.04))],'#d5b078',5)
 # Level entrance walk meets a 15 cm curb; no floating porch stair geometry.
 poly([(-4.5,.15,-1),(-7.2,.15,-1),(-7.2,.15,1),(-4.5,.15,1)],'#324b56','#70858b',2)
 for j in range(12):
  x=-4.15-.65*j/12;xx=-4.15-.65*(j+1)/12
  poly([(x,ground(x),-.5),(x,ground(x),1.2),(xx,ground(xx),1.2),(xx,ground(xx),-.5)],'#344c57','none',0)
 light=W(HOUSE_X+.08,1.85,.95);xx,yy=c.project(light);sc=c.f/max(1,c.depth(light));a.ellipse(xx,yy,sc*.7,sc*1.3,'url(#lamphalo)');a.rect(xx-8,yy-20,16,40,'#ecb86f','#6f6b58',3,3)

def exit_feet(t):
 out=[]
 for start,end,A,B in EXIT:
  q=ease(t,start,end);p=tuple(A[i]+(B[i]-A[i])*q for i in range(3));p=(p[0],p[1]+.19*math.sin(math.pi*q),p[2]);out.append((p,t<start or t>=end))
 return out

def run_progress(t):return RUN_LENGTH*ease(t,RUN_START,RUN_END)
def path(s):
 q=clamp(s/RUN_LENGTH);x=-1.45-5.3*q;z=.25+.45*q;return x,ground(x),z

def run_feet(t):
 # Explicit alternating contact schedule seeded from the actual exit stance.
 # The same held world anchors drive both drawing and footstep events.
 out=[]
 for j in [0,1]:
  pos=EXIT[j][3];planted=True
  for k,target in enumerate(([.72,2.18,3.80,5.20] if j==0 else [1.43,3.0,4.53,5.33])):
   center=[49.34,49.76,50.18,50.56][k]+(.19 if j else 0)
   start=center-.17;end=center+.11
   if t<start:break
   B=path(target)
   if t<end:
    q=ease(t,start,end);pos=tuple(pos[i]+(B[i]-pos[i])*q for i in range(3));pos=(pos[0],pos[1]+.23*math.sin(math.pi*q),pos[2]);planted=False;break
   pos=B
  out.append((pos,planted))
 return out

def actor_state(t,c):
 if t<RUN_START:
  feet=exit_feet(t);root=(-.55-0.90*ease(t,48.15,48.74),0,.35-.10*ease(t,48.3,48.74));hip=-66-84*ease(t,48.70,48.96)+48*ease(t,48.98,49.15);lean=-18*(1-ease(t,48.6,48.95))-25*ease(t,49.0,49.15);yaw=-.65-.1*ease(t,49.0,49.15);progress=0
 else:
  progress=run_progress(t);root=path(progress);feet=run_feet(t);hip=-102-48*ease(t,50.55,50.95);lean=-25*(1-ease(t,50.65,50.95));yaw=-.75
 world=W(*root);x,y=c.project(world);scale=c.f/c.depth(world)*UNIT
 targets=[]
 for point,on in feet:
  fx,fy=c.project(W(*point));targets.append(((fx-x)/scale,(fy-y)/scale,on,c.depth(world)/c.depth(W(*point))))
 sh_y=hip-math.sqrt(125**2-lean**2)
 defaults={j:(-43+88*j,hip-10) for j in [0,1]}
 if t>=49.0:
  q=ease(t,49.0,49.3);running={j:(-45+90*j+22*math.sin(progress/1.5*math.tau+j*math.pi),sh_y+62+30*math.cos(progress/1.5*math.tau+j*math.pi)) for j in [0,1]};defaults={j:tuple(defaults[j][k]*(1-q)+running[j][k]*q for k in [0,1]) for j in [0,1]}
 settle=ease(t,50.65,50.99);defaults={j:tuple(defaults[j][k]*(1-settle)+(-43+88*j,hip-10)[k]*settle for k in [0,1]) for j in [0,1]}
 hands=dict(defaults);hx,hy=c.project(car_handle(min(t,49.14)));handle=((hx-x)/scale,(hy-y)/scale)
 def blend(A,B,q):return tuple(A[i]*(1-q)+B[i]*q for i in [0,1])
 if t<48.94:hands[0]=handle
 elif t<49.12:hands[0]=blend(handle,defaults[0],ease(t,48.94,49.12))
 if 48.82<=t<48.94:hands[1]=blend(defaults[1],handle,ease(t,48.82,48.94))
 elif 48.94<=t<49.14:hands[1]=handle
 elif 49.14<=t<49.26:hands[1]=blend(handle,defaults[1],ease(t,49.14,49.26))
 p=rig.pose(t,(0,hip),lean,targets,hands,yaw,fear=.75)
 return {'root_site':root,'feet_world':feet,'x':x,'y':y,'scale':scale,'pose':p,'door_grip':t<49.14,'progress_m':progress}

def splashes(a,c,t):
 events=[(end,B) for start,end,A,B in EXIT]
 for j in [0,1]:
  for k,target in enumerate(([.72,2.18,3.80,5.20] if j==0 else [1.43,3.0,4.53,5.33])):
   events.append(([49.34,49.76,50.18,50.56][k]+(.19 if j else 0)+.11,path(target)))
 for when,p in events:
  dt=t-when
  if not 0<=dt<.18:continue
  radius=.025+.13*dt/.18;a.add(f'<g opacity="{.40*(1-dt/.18)}">')
  c.line(a,[W(p[0]+radius*math.cos(j*math.tau/18),p[1]+.005,p[2]+radius*math.sin(j*math.tau/18)) for j in range(19)],'#89adb8',2)
  for j in [-1,1]:
   P=W(p[0]+j*.06*dt/.18,p[1]+.14*math.sin(math.pi*dt/.18),p[2]);x,y=c.project(P);a.line([(x,y),(x-1,y+5)],'#9cbcc2',1.8)
  a.add('</g>')

def arrival(a,t):
 c=wide_camera(t) if t<48.02 else (run_camera(t) if t>=49.15 else exit_camera(t))
 terrain(a,c,t);facade(a,c,t)
 if t<48.02:sedan(a,c,t);return
 # Closed door is a retained design; its open aperture is painted in the side shell.
 sedan(a,c,t)
 if t<49.14:
  ps=[W(-1.016,.45,-.12),W(-1.016,.45,1.08),W(-1.016,1.46,.45),W(-1.016,1.50,-.12)];c.poly(a,ps,'#06131d','#4c6975',3)
 d=actor_state(t,c);rig.draw(a,d['x'],d['y'],d['scale'],d['pose'])
 if t<49.15:car_door(a,c,t)
 splashes(a,c,t)
