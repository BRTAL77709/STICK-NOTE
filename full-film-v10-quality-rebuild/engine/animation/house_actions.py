"""Whole-owner key/door choreography, in the same metric site as the car exit."""
import math
from motion_state import ease,clamp
from world import Camera,INK
from approved_components import text

import house_site as site
import articulated as rig
from render_base import rain
UNIT=site.UNIT

def doorState(u):
 fail=ease(u,.22,.34)*(1-ease(u,.62,.80));success=ease(u,2.74,2.84)*(1-ease(u,4.35,4.95));check=ease(u,5.85,5.98)*(1-ease(u,6.03,6.18))
 return {'angle':math.radians(72)*ease(u,2.85,3.65)*(1-ease(u,4.35,4.95)),'handle':-.28*(fail+success)-.20*check,'locked':u<1.99 or u>=5.55}
def doorPoint(x,y,z,u):
 q=doorState(u)['angle'];return x*math.cos(q)-z*math.sin(q),y,x*math.sin(q)+z*math.cos(q)
def hardware(u,inside=False):
 z=.055 if inside else -.055;q=doorState(u)['handle'];return doorPoint(.84,.95,z,u),doorPoint(.84+.15*math.cos(q),.95+.15*math.sin(q),z,u),doorPoint(.84,1.12,z,u)

def mix(A,B,q):return tuple(a*(1-q)+b*q for a,b in zip(A,B))
class DoorCamera(Camera):
 def __init__(self,c):self.camera=c;self.f=c.f;self.h=c.h
 def depth(self,p):return self.camera.depth(site.door_world(p))
 def project(self,p):return self.camera.project(site.door_world(p))
def camera(u):
 if u<4.3:c=site.local_camera(site.HOUSE_X+4.1,-2.0,1.3,site.HOUSE_X,.25,1850,1000)
 else:c=site.local_camera(site.HOUSE_X-4.1,.0,1.3,site.HOUSE_X,.15,1500,990)
 return DoorCamera(c)
def root(u):return 1.2-.65*ease(u,3.25,3.72)-.40*ease(u,6.05,6.4),0,-.45+ease(u,3.55,4.3)+.10*ease(u,6.05,6.4)
PLANS=[[(0,.16,(1.03,0,-.48)),(3.25,3.52,(.55,0,-.42)),(3.72,3.98,(.44,0,.25)),(4.15,4.36,(.43,0,.65)),(6.05,6.28,(.15,0,.76))],[(.16,.32,(1.34,0,-.44)),(3.45,3.72,(.68,0,-.20)),(3.93,4.20,(.66,0,.65)),(6.21,6.4,(.15,0,.54))]]
START_FEET=[(p[2]+.5,p[1]-.15,site.HOUSE_X-p[0]) for p in [site.path(5.20),site.path(site.RUN_LENGTH)]]
def feet(u):
 out=[]
 for j in [0,1]:
  A=START_FEET[j];on=True
  for start,end,B in PLANS[j]:
   if u<start:break
   if u<end:
    q=ease(u,start,end);A=mix(A,B,q);A=(A[0],A[1]+(.04 if start<1 else .13)*math.sin(math.pi*q),A[2]);on=False;break
   A=B
  out.append((A,on))
 return out

def contact(u,inside=False):
 if inside:return hardware(u,True)[1]
 q=ease(u,3.05,3.55);h=doorState(u)['handle'];x=(.84+.15*math.cos(h))*(1-q)+.42*q;y=(.95+.15*math.sin(h))*(1-q)+1.01*q
 return doorPoint(x,y,-.055,u)
def thumb_points(u):
 q=math.pi/2*ease(u,5.1,5.55)
 return [doorPoint(.84+s*.065*math.cos(q),1.12+s*.065*math.sin(q),.055,u) for s in [-1,1]]

def key_state(u,pocket):
 pre=(.84,1.12,-.27)
 if u<1.12:B=pocket
 elif u<1.3:B=mix(pocket,(pocket[0]-.04,pocket[1]+.16,pocket[2]-.025),ease(u,1.12,1.3))
 elif u<1.5:B=mix((pocket[0]-.04,pocket[1]+.16,pocket[2]-.025),pre,ease(u,1.3,1.5))
 elif u<2.30:B=(.84,1.12,-.27+.10*ease(u,1.5,1.72)-.20*ease(u,2.12,2.30))
 else:B=mix((.84,1.12,-.37),pocket,ease(u,2.30,2.55))
 align=ease(u,1.3,1.5)*(1-ease(u,2.3,2.55));theta=align*math.pi/2;turn=math.pi/2*ease(u,1.76,1.98)*(1-ease(u,2.0,2.12))
 return {'bow':B,'tip':(B[0],B[1]-.13*math.cos(theta),B[2]+.13*math.sin(theta)),'turn':turn,'ring_axis':(0,math.sin(theta),math.cos(theta)),'held':1.0<=u<=2.55,'pocket':pocket}


def actor_state(u,c=None):
 c=c or camera(u);r=root(u);px,py=c.project(r);scale=c.f/c.depth(r)*UNIT
 panic=ease(u,.55,.72)*(1-ease(u,.9,1.17));hip=-150+19*panic+15*ease(u,3.18,3.5)*(1-ease(u,4.16,4.4));lean=23*ease(u,.40,.62)*(1-ease(u,.7,.9))-26*ease(u,2.75,3.20)*(1-ease(u,3.55,3.83))
 hip+=42*ease(u,6.05,6.4);lean+=24*ease(u,6.05,6.4)
 lean-=9*math.sin(math.pi*ease(u,1.76,2.06));lean+=6*math.sin(math.pi*ease(u,5.1,5.55));hip+=2*math.sin(u*3)*ease(u,4.4,4.6)
 rootx,_,rootz=r;pocket=(rootx-.19,-hip*UNIT+.044,rootz);key=key_state(u,pocket);handle=hardware(u,False)[1];target=None
 if u<.22:
  q=ease(u,0,.22);A=c.project(pocket);B=c.project(handle);target=mix(A,B,q)
 elif u<.65:target=c.project(handle)
 elif u<1.0:target=mix(c.project(handle),c.project(pocket),ease(u,.65,1.0))
 elif u<2.55:target=c.project(key['bow'])
 elif u<2.73:target=mix(c.project(pocket),c.project(handle),ease(u,2.55,2.73))
 elif u<3.55:target=c.project(contact(u))
 elif u<3.83:
  B=(px+scale*(-43),py+scale*(hip-10));target=mix(c.project(contact(u)),B,ease(u,3.55,3.83))
 elif u<4.17:target=(px+scale*(-43),py+scale*(hip-10))
 elif u<4.35:
  A=(px+scale*(-43),py+scale*(hip-10));target=mix(A,c.project(contact(u,True)),ease(u,4.17,4.35))
 elif u<4.95:target=c.project(contact(u,True))
 elif u<5.1:target=mix(c.project(contact(u,True)),c.project(hardware(u,True)[2]),ease(u,4.95,5.1))
 elif u<5.65:target=c.project(hardware(u,True)[2])
 elif u<6.05:target=mix(c.project(hardware(u,True)[2]),c.project(hardware(u,True)[1]),ease(u,5.65,5.85))
 else:target=mix(c.project(hardware(u,True)[1]),(px-43*scale,py+(hip-10)*scale),ease(u,6.05,6.22))
 hand=((target[0]-px)/scale,(target[1]-py)/scale);targets=[]
 for p,on in feet(u):
  x,y=c.project(p);targets.append(((x-px)/scale,(y-py)/scale,on,c.depth(r)/c.depth(p)))
 # The near hand changes with the camera side, while its world contact stays fixed.
 owner=0
 hands={owner:hand}
 if 1.35<=u<2.3:
  bx,by=c.project((1.08,1.25,-.03));q=ease(u,1.35,1.55)*(1-ease(u,2.1,2.3));hands[1]=mix((45,hip-10),((bx-px)/scale,(by-py)/scale),q)
 p=rig.pose(51+u,(0,hip),lean,targets,hands,head_yaw=-.75+1.15*panic,gaze=-.8+1.2*ease(u,.56,.69)*(1-ease(u,.91,1.09)),fear=.9,blink=max(0,1-abs(u-.74)/.07))
 p['wrist_angles']={0:math.degrees(key['turn']) if key['held'] else (90*ease(u,5.1,5.55)*(1-ease(u,5.65,5.85)) if u>=4.3 else 0)}
 return {'root':r,'x':px,'y':py,'scale':scale,'pose':p,'key':key,'hand_target':target,'hand_owner':owner,'feet_world':feet(u),'inside':u>=4.3,'hinge':doorState(u)['angle']}

def leaf(a,c,u):
 def pp(x,y,z=0):return doorPoint(x,y,z,u)
 c.poly(a,[pp(0,0),pp(1,0),pp(1,2.1),pp(0,2.1)],'#1c3644','#70868b',5)
 for yy,hh in [(.2,.62),(1.25,.60)]:c.poly(a,[pp(.12,yy,-.015),pp(.88,yy,-.015),pp(.88,yy+hh,-.015),pp(.12,yy+hh,-.015)],'#17303f','#536b77',3)
 for y in [.25,1.8]:c.line(a,[pp(.015,y,-.03),pp(.015,y+.13,-.03)],'#b2b6a8',7)
 H,E,L=hardware(u,u>=4.3);c.line(a,[H,E],'#d0ac72',11);x,y=c.project(L);a.ellipse(x,y,16,21,'#b2915b',INK,4)
 if u>=4.3:
  c.line(a,thumb_points(u),'#d5b67d',9)
 else:a.path(f'M{x} {y-5} v11','none',INK,4)

def draw_key(a,c,d,u):
 if not d['key']['held']:return
 k=d['key'];B=c.project(k['bow']);T=c.project(k['tip']);P=c.project(k['pocket']);rad=40*d['scale'];a.add(f'<defs><mask id="key-pocket"><rect width="1080" height="1920" fill="white"/><circle cx="{P[0]}" cy="{P[1]}" r="{rad}" fill="black"/></mask></defs><g mask="url(#key-pocket)">')
 a.line([B,T],'#d2d2b9',6);ang=k['turn'];p=k['bow'];q1=c.project((p[0]+.025*math.cos(ang),p[1]+.025*math.sin(ang)*k['ring_axis'][1],p[2]+.025*math.sin(ang)*k['ring_axis'][2]));q2=c.project((p[0]-.025*math.cos(ang),p[1]-.025*math.sin(ang)*k['ring_axis'][1],p[2]-.025*math.sin(ang)*k['ring_axis'][2]));a.line([q1,q2],'#e5bd79',10);a.ellipse(*B,10,8,'none','#d9af70',4);a.add('</g>')

def door(a,u):
 c=camera(u);d=actor_state(u,c);a.rect(0,0,1080,1920,'#152d3b')
 c.poly(a,[(-6,0,.08),(6,0,.08),(6,6,.08),(-6,6,.08)],'#152d3b','none',0)
 near,far=(0,7) if u>=4.3 else (-7,0)
 c.poly(a,[(-7,0,near),(7,0,near),(7,0,far),(-7,0,far)],'#0c1d29','#38525e',3)
 for j in range(1,24):c.line(a,[(-6,j*.26,.08),(6,j*.26,.08)],'#29414c',2)
 c.poly(a,[(-.1,0,.05),(1.1,0,.05),(1.1,2.22,.05),(-.1,2.22,.05)],'#4b6470','#899993',5);c.poly(a,[(0,0,.02),(1,0,.02),(1,2.1,.02),(0,2.1,.02)],'#030b13','none',0)
 leaf(a,c,u)
 if u<4.3:
  x,y=c.project((.5,2.4,0));text(a,x,y,'17',58,'#f0b969')
 for foot,on in d['feet_world']:
  if on:
   fx,fy=c.project(foot);a.ellipse(fx,fy+2,25*d['scale'],4*d['scale'],'#030b13',extra='opacity=".6"')
 rig.draw(a,d['x'],d['y'],d['scale'],d['pose'],back=u>=4.3)
 draw_key(a,c,d,u)
 if 5.1<=u<5.65:
  c.line(a,thumb_points(u),'#d5b67d',9);px,py=c.project(hardware(u,True)[2]);a.path(f'M{px-8} {py-5} q12 6 8 13','none','#d8ded1',8)
 a.ellipse(100,750,210,460,'url(#lamphalo)')
 if u<4.3:rain(a,51+u)
