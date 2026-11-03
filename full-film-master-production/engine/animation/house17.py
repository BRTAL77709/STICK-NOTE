"""House 17: shared hinge/hardware/key state, hallway, stairs and window aperture."""
import math
from approved_components import text,limb,ik
from motion_state import ease,state
from world import Camera,city,INK
from actor import actor,gait
from choreography import ENTRY_LOCAL,STAIRS_LOCAL
from vehicle import sedan
HOUSE={'door_width':1.,'door_height':2.1,'floor_to_floor':3.,'window_sill':3.8,'window_x':1.4,'roof_height':6.5,'curb_to_facade':6.}
EVENTS=[(.18,'handle contact'),(.45,'locked handle rattle'),(.92,'key retrieval'),(1.65,'key insertion'),(1.95,'key rotation'),(2.12,'lock releases'),(2.45,'key withdrawn'),(2.75,'handle turns'),(2.85,'hinge opens'),(4.2,'threshold footfall'),(4.95,'door closes'),(4.95,'door latch'),(5.55,'interior lock'),(5.95,'handle check')]
def doorState(u):
 angle=math.radians(72)*ease(u,2.85,3.65)*(1-ease(u,4.35,4.95))
 fail=ease(u,.05,.22)*(1-ease(u,.48,.72));success=ease(u,2.64,2.82)*(1-ease(u,4.35,4.95))
 return {'angle':angle,'handle':-.28*(fail+success),'key_depth':.035*ease(u,1.40,1.70)*(1-ease(u,2.24,2.48)),'key_turn':math.pi/2*ease(u,1.76,2.06),'locked':u<2.12 or u>=5.55,'inside':u>=4.2,'latch_engaged':u>=4.95}
def doorPoint(x,y,z,u):
 ang=doorState(u)['angle'];return x*math.cos(ang)-z*math.sin(ang),y,x*math.sin(ang)+z*math.cos(ang)
def hardware(u,inside=False):
 st=doorState(u);z=.055 if inside else -.055
 handle=doorPoint(.84,.95,z,u);lock=doorPoint(.84,1.12,z,u)
 end=doorPoint(.84+.15*math.cos(st['handle']),.95+.15*math.sin(st['handle']),z,u)
 return handle,end,lock

def door(a,u):
 close=u<3.05;inside=u>=4.9
 c=Camera(.50,3.4 if inside else (-2.4 if close else -5.2),1.25,math.pi if inside else 0,1500 if close else 1300,1010 if close or inside else 890)
 a.rect(0,0,1080,1920,'#152d3b');a.path('M0 1500 H1080 V1920 H0Z','#0c1d29',INK,5)
 for yy in range(250,1600,100):a.line([(0,yy),(1080,yy)],'#29414c',2)
 # Fixed jamb, opening and top-mounted number.
 c.poly(a,[(-.1,0,.05),(1.1,0,.05),(1.1,2.22,.05),(-.1,2.22,.05)],'#4b6470','#899993',5)
 c.poly(a,[(0,0,.02),(1,0,.02),(1,2.1,.02),(0,2.1,.02)],'#030b13','none',0)
 def pp(x,y,z=0):return doorPoint(x,y,z,u)
 c.poly(a,[pp(0,0),pp(1,0),pp(1,2.1),pp(0,2.1)],'#1c3644','#70868b',5)
 for yy,hh in [(.2,.62),(1.25,.60)]:c.poly(a,[pp(.12,yy,-.015),pp(.88,yy,-.015),pp(.88,yy+hh,-.015),pp(.12,yy+hh,-.015)],'#17303f','#536b77',3)
 for yy in [.25,1.8]:c.line(a,[pp(.015,yy,-.03),pp(.015,yy+.13,-.03)],'#b2b6a8',7)
 handle,end,lock=hardware(u,inside);H=c.project(handle);E=c.project(end);L=c.project(lock);c.line(a,[handle,end],'#d0ac72',11);a.ellipse(*L,19,23,'#b2915b',INK,4);a.path(f'M{L[0]} {L[1]-6} v13','none',INK,4)
 num=c.project((.5,2.38,0))
 if not inside:text(a,*num,'17',63,'#f0b969')
 if close:
  # Hand transitions from handle to pocket/key, aligns, inserts, rotates and withdraws.
  if u<.65:hand=(E[0]+8,E[1]+8)
  elif u<1.0:
   q=ease(u,.65,1.0);hand=((E[0]+8)*(1-q)+930*q,(E[1]+8)*(1-q)+1390*q)
  elif u<1.35:
   q=ease(u,1.0,1.35);B=c.project(doorPoint(.84,1.12,-.38,1.35));hand=(930*(1-q)+(B[0]+23)*q,1390*(1-q)+(B[1]+8)*q)
  elif u<2.48:
   gap=.15*(1-ease(u,1.35,1.45))+.18*ease(u,2.30,2.55);st=doorState(u);tip=pp(.84,1.12,-.075-gap+st['key_depth']);bow=pp(.84,1.12,-.23-gap+st['key_depth']);T=c.project(tip);B=c.project(bow);hand=(B[0]+23,B[1]+8)
   a.line([B,T],'#c7cabc',8);ang=st['key_turn'];r1=c.project(pp(.84+.04*math.cos(ang),1.12+.04*math.sin(ang),-.23-gap+st['key_depth']));r2=c.project(pp(.84-.04*math.cos(ang),1.12-.04*math.sin(ang),-.23-gap+st['key_depth']));a.line([r1,r2],'#d1b785',12);a.ellipse(*B,18,12,'none','#d1b785',5)
  elif u<2.70:
   q=ease(u,2.48,2.70);B=c.project(doorPoint(.84,1.12,-.41,2.48));hand=((B[0]+23)*(1-q)+(E[0]+8)*q,(B[1]+8)*(1-q)+(E[1]+8)*q)
  else:hand=(E[0]+8,E[1]+8)
  sh=(1150,1390);el=ik(sh,hand,280,270,-1);limb(a,[sh,el,hand],'#264552',52);a.ellipse(*hand,28,35,'#e0e1d4',INK,5)
  for j in range(3):a.line([(hand[0]-16+j*8,hand[1]-10),(hand[0]-13+j*8,hand[1]+9)],'#82958f',2)
 elif u<4.9:
  q=ease(u,*ENTRY_LOCAL);z=-1.0+1.9*q;root=(.65,0,z);x,y=c.project(root);scale=c.f/c.depth(root)*1.8/350;progress=1.9*q*350/1.8;feet=[]
  for j in [0,1]:
   fx,fy,on=gait(progress,j);wp=(.65+(-.10 if j==0 else .10),-fy*1.8/350,-1+(progress+fx)*1.8/350);xx,yy=c.project(wp);feet.append(((xx-x)/scale,(yy-y)/scale,on))
  target=None
  if u<3.65:
   xx,yy=c.project(hardware(u)[1]);target=((xx-x)/scale,(yy-y)/scale)
  actor(a,x,y,u,progress,scale,True,yaw=.7,fear=.7,feet_override=feet,back=True,hand_target=target)
 else:
  # The hand grips the interior thumbturn only after the door is shut.
  target=(L[0]+10,L[1]+3) if u<5.8 else E
  sh=(-60,1310);el=ik(sh,target,280,280,1);limb(a,[sh,el,target],'#264552',52);a.ellipse(*target,28,35,'#e0e1d4',INK,5)
  turn=math.pi/2*ease(u,5.1,5.55);a.line([(L[0]-20*math.cos(turn),L[1]-20*math.sin(turn)),(L[0]+20*math.cos(turn),L[1]+20*math.sin(turn))],'#d5b67d',10)
 a.ellipse(100,700,210,460,'url(#lamphalo)')

def stairs(a,u,t):
 a.rect(0,0,1080,1920,'#122d3c');q=ease(u,*STAIRS_LOCAL);d=520*q;track=120*ease(u,1.45,2.15)
 a.add(f'<g transform="translate({-track} 0)">')
 a.poly([(100,1800),(1250,1800),(1250,700),(100,1550)],'#1c3a48','#49616d',7)
 for j in range(-1,12):
  x=270+j*65;y=1690-j*70;a.line([(x,y),(x+65,y)],'#849792',10);a.line([(x+65,y),(x+65,y-70)],'#4f6871',5)
 a.line([(220,1330),(1100,380)],'#71868c',14)
 actor(a,270+d*1.25,1690-d*56/52*1.25,t,progress=d,scale=1.25,run=True,fear=.6,stairs=True)
 a.add('</g>')

class DownCamera(Camera):
 def __init__(self,*args,down=.33,**kw):super().__init__(*args,**kw);self.down=down
 def coords(self,p):
  dx=p[0]-self.x;dz=p[2]-self.z;z=dx*math.sin(self.yaw)+dz*math.cos(self.yaw);x=dx*math.cos(self.yaw)-dz*math.sin(self.yaw);y=p[1]-self.y
  return x,y*math.cos(self.down)+z*math.sin(self.down),z*math.cos(self.down)-y*math.sin(self.down)
 def depth(self,p):return self.coords(p)[2]
 def project(self,p):
  x,y,z=self.coords(p);return 540+self.f*x/max(.65,z),self.h-self.f*y/max(.65,z)

def room(a,t,curtain=0,looking=False,phone=False,phone_hand=None,phone_visible=True):
 p=state(62);b=state(t,True);hx=p['x']+7*math.cos(p['yaw']);hz=p['z']-7*math.sin(p['yaw']);yaw=math.atan2(b['x']-hx,b['z']-hz)
 c=DownCamera(hx,hz,4.7,yaw,1060,940,down=.36)
 # The street/car share the same world projection, seen through a real masked aperture.
 a.add('<defs><clipPath id="window-aperture"><rect x="440" y="310" width="530" height="820"/></clipPath></defs><g clip-path="url(#window-aperture)"><g transform="translate(440 310) scale(.4907407 .4270833)">')
 city(a,c,t);sedan(a,c,t,True);a.add('</g></g>')
 for x,y,w,h in [(0,0,1080,310),(0,310,440,820),(970,310,110,820),(0,1130,1080,790)]:a.rect(x,y,w,h,'#122b39')
 a.line([(0,1470),(1080,1470)],'#4c6269',7)
 a.rect(430,300,550,840,'none','#85999b',12,3);a.line([(705,310),(705,1130)],'#557382',8);a.line([(440,720),(970,720)],'#557382',8)
 a.line([(390,250),(1020,250)],'#839491',13)
 edge=790-280*curtain
 a.path(f'M402 270 Q{edge+13} 245 {edge} 280 L{edge-13} 1190 Q{edge-100} 1222 402 1175Z','#264653',INK,7)
 for j in range(5):
  xx=413+j*(edge-425)/5;a.path(f'M{xx} 280 q{-8+5*curtain} 430 0 890','none','#52717c',3)
 a.path('M1003 270 L942 285 L923 1190 Q968 1220 1005 1170Z','#264653',INK,7)
 a.rect(58,1060,205,410,'#193542','#4e6470',4,9);a.line([(160,1060),(160,800)],'#8c714b',11);a.poly([(85,790),(235,790),(275,958),(45,958)],'#d7ab70','#5a4731',5);a.ellipse(160,950,280,430,'url(#lamphalo)')
 a.path('M600 1465 Q820 1310 1080 1380 V1920 H610Z','#203b4b',INK,9)
 a.rect(690,1368,160,240,'#183340','#506873',4,6);a.rect(680,1358,180,16,'#304c57','#76908b',3,4)
 if looking:
  reach=ease(t,59.4,60.1);target=(45*(1-reach)+(edge-430)/2*reach,-169*(1-reach)+(1110-1700)/2*reach);actor(a,430,1700,t,scale=2,hand_target=target,yaw=.7,fear=.8)
 elif phone:
  reaction=.65*ease(t,67.7,68.4)+.35*ease(t,74.7,75.4)
  target=phone_hand or ((79,-300) if not reaction else (79-14*reaction,-300-9*reaction))
  actor(a,430,1700,t,scale=2,hand_target=target,phone=phone_visible,yaw=.25*reaction+.85*ease(t,75,78),fear=.7+.3*reaction,reaction=reaction)
 else:actor(a,430,1700,t,scale=2,fear=.5)
