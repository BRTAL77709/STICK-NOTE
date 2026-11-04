"""Two metric stair flights and a visible U-turn landing; planted world feet drive the pelvis."""
import math
from house_actions import DoorCamera
import house_site as site
import articulated as rig
from world import Camera,INK
from motion_state import ease,clamp
T0=57.4;T1=58.85;T2=59.35;T3=60.65;END=60.85
RISE=.18;TREAD=.25

def lerp(A,B,q):return tuple(a+(b-a)*q for a,b in zip(A,B))
def swing(A,B,t,start,end):
 q=ease(t,start,end);p=lerp(A,B,q);return (p[0],p[1]+.11*math.sin(math.pi*q),p[2])
def flight_feet(t,start,end,count,x,z0,base,direction,initial):
 period=(end-start)/count;feet=[]
 for j in [0,1]:
  p=initial[j];on=True
  for n in range(j+1,count+1,2):
   a=start+(n-1)*period;b=a+.65*period;target=(x,base+n*RISE,z0+direction*(n-.5)*TREAD)
   if t<a:break
   if t<b:p=swing(p,target,t,a,b);on=False;break
   p=target
  feet.append((p,on))
 return feet

def feet(t):
 if t<T1:return flight_feet(t,T0,T1,8,.15,.9,0,1,[(.15,0,.76),(.15,0,.54)])
 first=[(.15,1.26,2.525),(.15,1.44,2.775)];plans=[[(58.85,59.08,(-.45,1.44,2.94)),(59.16,59.35,(-1.05,1.44,3.20))],[(59.03,59.28,(-1.05,1.44,2.98))]]
 if t<T2:
  out=[]
  for j in [0,1]:
   p=first[j];on=True
   for a,b,B in plans[j]:
    if t<a:break
    if t<b:p=swing(p,B,t,a,b);on=False;break
    p=B
   out.append((p,on))
  return out
 out=flight_feet(t,T2,T3,7,-1.05,3.1,1.44,-1,[(-1.05,1.44,3.20),(-1.05,1.44,2.98)])
 if t>=T3:
  A=(-1.05,2.52,1.725);B=(-1.05,2.70,1.20);out[1]=(swing(A,B,t,T3,END),t>=END)
 return out

def root(t):
 fs=feet(t);x=sum(p[0] for p,on in fs)/2;z=sum(p[2] for p,on in fs)/2
 if t<T1:
  n=8*clamp((t-T0)/(T1-T0));k=math.floor(n);u=n-k;y=RISE*(k+ease(u,.64,.98))
 elif t<T2:y=1.44
 else:
  n=7*clamp((t-T2)/(T3-T2));k=math.floor(n);u=n-k;y=1.44+RISE*(k+ease(u,.64,.98))
 return x,y,z

def camera(t):
 pos=site.door_world((2.9,2.35,2.15));target=site.door_world((-.45,0,1.70));return DoorCamera(Camera(pos[0],pos[2],pos[1],math.atan2(target[0]-pos[0],target[2]-pos[2]),900,950))

def actor_state(t):
 c=camera(t);r=root(t);x,y=c.project(r);scale=c.f/c.depth(r)*site.UNIT;targets=[]
 for p,on in feet(t):
  px,py=c.project(p);targets.append(((px-x)/scale,(py-y)/scale,on,c.depth(r)/c.depth(p)))
 turn=ease(t,58.85,59.35);direction=1-2*turn;hip=-108-42*ease(t,60.65,60.85);lean=24*direction*(1-ease(t,60.65,60.85));shy=hip-math.sqrt(125**2-lean**2);phase=(t-T0)*math.pi*5
 hands={0:(-48+20*math.sin(phase),shy+65+25*math.cos(phase)),1:(48-20*math.sin(phase),shy+65-25*math.cos(phase))}
 settle=ease(t,T3,END);hands={j:tuple(hands[j][k]*(1-settle)+(-43+88*j,hip-10)[k]*settle for k in [0,1]) for j in [0,1]}
 q0=ease(t,T0,T0+.16);hands={j:tuple((-43+88*j,hip-10)[k]*(1-q0)+hands[j][k]*q0 for k in [0,1]) for j in [0,1]}
 # Rail contact slides along the actual sloped rail, then releases onto landing.
 rz=r[2]+.13*direction;ry=1.05+(rz-.9)*.72 if t<T1 else 2.49+(3.1-rz)*.72;rail=(.69 if t<T1 else -1.59,ry,rz)
 if t<T1 or t>=T2:
  rx,ry=c.project(rail);q=ease(t,T0,T0+.16)*(1-ease(t,T1-.18,T1)) if t<T1 else ease(t,T2,T2+.16)*(1-ease(t,60.5,60.75));base=hands[1];hands[1]=(base[0]*(1-q)+(rx-x)/scale*q,base[1]*(1-q)+(ry-y)/scale*q)
 p=rig.pose(t,(0,hip),lean,targets,hands,.78*direction,gaze=.9*direction,fear=.85,blink=max(0,1-abs(t-59.16)/.065))
 return {'camera':c,'root':r,'feet':feet(t),'x':x,'y':y,'scale':scale,'pose':p,'rail':rail,'rail_contact':T0+.16<=t<T1-.18 or T2+.16<=t<60.5}

def draw(a,t):
 d=actor_state(t);c=d['camera'];a.rect(0,0,1080,1920,'#122d3c')
 # Side wall, skirting and upper-floor landing locate the staircase in the house.
 c.poly(a,[(-1.7,0,.3),(-1.7,0,3.6),(-1.7,5.3,3.6),(-1.7,5.3,.3)],'#1c3a48','#49616d',5)
 for base,count,x,z0,direction in [(1.44,7,-1.05,3.1,-1),(0,8,.15,.9,1)]:
  for n in range(1,count+1):
   zA=z0+direction*(n-1)*TREAD;zB=z0+direction*n*TREAD;y=base+n*RISE
   c.poly(a,[(x-.43,y,zA),(x+.43,y,zA),(x+.43,y,zB),(x-.43,y,zB)],'#39515b','#91a39c',3)
   c.poly(a,[(x-.43,y-RISE,zA),(x+.43,y-RISE,zA),(x+.43,y,zA),(x-.43,y,zA)],'#203d4d','#66818b',2)
 c.poly(a,[(-1.5,1.44,2.9),(.6,1.44,2.9),(.6,1.44,3.5),(-1.5,1.44,3.5)],'#36515c','#91a39c',3)
 rig.draw(a,d['x'],d['y'],d['scale'],d['pose'])
 # Rail is physically anchored at each third tread; both flights stay fixed.
 for x,z0,y0,z1,y1 in [(.69,.9,1.05,2.9,2.49),(-1.59,3.1,2.49,1.35,3.75)]:
  c.line(a,[(x,y0,z0),(x,y1,z1)],'#819894',9)
  for j in range(4):
   q=j/3;z=z0+(z1-z0)*q;y=y0+(y1-y0)*q;c.line(a,[(x,y-1.0,z),(x,y,z)],'#466573',5)
