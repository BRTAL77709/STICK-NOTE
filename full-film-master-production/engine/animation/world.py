"""Layered cel-illustrated city. Shared metric projection; no rendered 3D assets."""
import math,random
from motion_state import *
INK='#030b13';AMBER='#f4bd70'
class Camera:
 def __init__(self,x,z,y=2.8,yaw=0,focal=1150,horizon=770):self.x=x;self.z=z;self.y=y;self.yaw=yaw;self.f=focal;self.h=horizon
 def depth(self,p):return (p[0]-self.x)*math.sin(self.yaw)+(p[2]-self.z)*math.cos(self.yaw)
 def project(self,p):
  dx=p[0]-self.x;dz=p[2]-self.z;zz=dx*math.sin(self.yaw)+dz*math.cos(self.yaw);xx=dx*math.cos(self.yaw)-dz*math.sin(self.yaw)
  zz=max(.65,zz);return 540+self.f*xx/zz,self.h-self.f*(p[1]-self.y)/zz
 def clip(self,ps):
  # Sutherland-Hodgman against camera near plane; passing facades/curbs must not pop.
  out=[]
  for prev,cur in zip(ps[-1:]+ps[:-1],ps):
   dp=self.depth(prev);dc=self.depth(cur);pin=dp>=.9;cin=dc>=.9
   if pin!=cin:
    u=(.9-dp)/(dc-dp);out.append(tuple(prev[j]+u*(cur[j]-prev[j]) for j in range(3)))
   if cin:out.append(cur)
  return out
 def poly(self,a,ps,fill,stroke=INK,w=3,extra=''):
  clipped=self.clip(list(ps))
  if len(clipped)<3:return
  a.poly([self.project(p) for p in clipped],fill,stroke,w)
 def line(self,a,ps,col,w=2):
  for q,r in zip(ps,ps[1:]):
   dq=self.depth(q);dr=self.depth(r)
   if dq<.9 and dr<.9:continue
   if (dq<.9)!=(dr<.9):
    u=(.9-dq)/(dr-dq);hit=tuple(q[j]+u*(r[j]-q[j]) for j in range(3))
    if dq<.9:q=hit
    else:r=hit
   a.line([self.project(q),self.project(r)],col,w)

def terrain(a,c,t):
 a.rect(0,0,1080,1920,'#0a1d2a');a.rect(0,0,1080,750,'url(#citysky)')
 # Distant skyline: stable world coordinates give genuine parallax.
 rng=random.Random(73)
 for j in range(18):
  z=225+j%3*17;x=(j-8.5)*11;h=rng.uniform(15,30);w=rng.uniform(5,11)
  c.poly(a,[(x,0,z),(x+w,0,z),(x+w,h,z),(x,h,z)],'#132e3d','#274452',1)
  for k in range(3):
   for m in range(6):
    if (j+k+m)%3==0:c.poly(a,[(x+1+k*2,h-2-m*2,z-.02),(x+1.7+k*2,h-2-m*2,z-.02),(x+1.7+k*2,h-3-m*2,z-.02),(x+1+k*2,h-3-m*2,z-.02)],'#50605a','none',0)
 # Far-to-near continuous road/sidewalk strips, not displacement of a single painted lane.
 for z in sorted(range(3*math.floor((c.z-180)/3),3*math.ceil((c.z+180)/3),3),key=lambda z:-c.depth((road_x(z),0,z))):
  if not .8<c.depth((road_x(z),0,z))<190:continue
  z2=z+3.1;xc=road_x(z);xd=road_x(z2)
  c.poly(a,[(xc-22,0,z),(xc+22,0,z),(xd+22,0,z2),(xd-22,0,z2)],'#142a33','none',0)
  c.poly(a,[(xc-4.5,0.015,z),(xc+4.5,0.015,z),(xd+4.5,0.015,z2),(xd-4.5,0.015,z2)],'#132e3b' if z%2 else '#173543','none',0)
  for side in [-1,1]:
   c.poly(a,[(xc+side*4.5,.15,z),(xc+side*6.5,.15,z),(xd+side*6.5,.15,z2),(xd+side*4.5,.15,z2)],'#30434a','#41565b',.8)
   c.line(a,[(xc+side*4.5,.15,z),(xd+side*4.5,.15,z2)],'#77908b',1.6)
  if z%12<4:c.poly(a,[(xc-.065,.03,z),(xc+.065,.03,z),(xd+.065,.03,z2),(xd-.065,.03,z2)],'#c5c9b6','none',0)
  # Asphalt broken glints from fixed puddles; ripple phase independent of car motion.
  if z%6==0:
   for side in [-1,1]:
    xx=xc+side*2.9;c.line(a,[(xx-.9,0.04,z),(xx+.6,0.04,z+.13)],'#557b87',1.2)
 # True crossing geometry + zebra bars at fixed world route coordinates.
 for cross in [45,130,222,310]:
  xx=road_x(cross);c.poly(a,[(xx-35,.035,cross-4),(xx+35,.035,cross-4),(xx+35,.035,cross+4),(xx-35,.035,cross+4)],'#182f38','none',0)
  for j in range(7):
   x=xx-3.7+j*1.13;c.poly(a,[(x,.045,cross-5.5),(x+.52,.045,cross-5.5),(x+.52,.045,cross-3.9),(x,.045,cross-3.9)],'#9caea4','none',0)
 # Street details remain world-locked.
 for z in range(-180,500,8):
  xc=road_x(z)
  if z%16==0:
   x=xc+4.1;c.poly(a,[(x-.25,.04,z-.45),(x+.25,.04,z-.45),(x+.25,.04,z+.45),(x-.25,.04,z+.45)],'#08151e','#53676c',1)
   for k in range(5):c.line(a,[(x-.2,.05,z-.32+k*.15),(x+.2,.05,z-.32+k*.15)],'#415b66',1)
  if z%24==0:
   for side in [-1,1]:
    x=xc+side*3.4
    for j in range(6):
     z1=z+j*.28;c.line(a,[(x-.6-j*.025,.045,z1),(x+.7+j*.04,.045,z1)],'#836345',2)

def box(a,c,x,z,w,d,h,col):
 front=[(x,0,z),(x+w,0,z),(x+w,h,z),(x,h,z)]
 # street-facing frontage, side and flat cel roof planes
 c.poly(a,front,col,'#08151d',3);c.poly(a,[(x+w,0,z),(x+w,0,z+d),(x+w,h,z+d),(x+w,h,z)],'#102a38','#06141e',2)
 c.poly(a,[(x,h,z),(x+w,h,z),(x+w,h,z+d),(x,h,z+d)],'#2d454e','#071620',2)

def building(a,c,side,z,index):
 rng=random.Random(index*73+side);x=road_x(z)+side*8;w=6.5;d=9;h=(7.5+index%3*2) if z<160 else (5.9+index%2*.6)
 if side<0:x-=w
 col=['#243e48','#1b3542','#293d48','#1b3440'][index%4];box(a,c,x,z,w,d,h,col)
 # facade faces toward advancing camera; architectural variants, not identical repeated windows.
 cols=2 if index%3 else 3;rows=2 if h<8 else 3
 for row in range(rows):
  for j in range(cols):
   xx=x+.65+j*(w-.8)/cols;yy=1.8+row*2.3;ww=1.2;hh=1.4
   c.poly(a,[(xx,yy,z-.03),(xx+ww,yy,z-.03),(xx+ww,yy+hh,z-.03),(xx,yy+hh,z-.03)],'#8e744d' if (index+j+row)%4==0 else '#0c2433','#67818a',2)
   c.line(a,[(xx+ww/2,yy,z-.05),(xx+ww/2,yy+hh,z-.05)],'#425a68',2);c.line(a,[(xx,yy+hh*.55,z-.05),(xx+ww,yy+hh*.55,z-.05)],'#425a68',1.5)
   c.line(a,[(xx-.1,yy-.08,z-.12),(xx+ww+.12,yy-.08,z-.12)],'#718389',3)
   c.line(a,[(xx+.12,yy+hh-.1,z-.08),(xx+.5,yy+.1,z-.08)],'#63818b',1)
 # Framed door, handle, upper lintel; adjacent storefront shutter or porch.
 doorx=x+w*.43;c.poly(a,[(doorx,0,z-.04),(doorx+1.15,0,z-.04),(doorx+1.15,2.2,z-.04),(doorx,2.2,z-.04)],'#0b1d29','#61767b',2)
 c.line(a,[(doorx+.9,1,z-.08),(doorx+1.05,1,z-.08)],'#d1a369',3)
 if index%3==0:
  c.poly(a,[(x-.3,2.6,z-.7),(x+w+.3,2.6,z-.7),(x+w+.3,3.05,z),(x-.3,3.05,z)],'#2e4c54','#06131e',2)
  for yy in [i*.26 for i in range(1,10)]:c.line(a,[(x+.4,yy,z-.05),(x+1.8,yy,z-.05)],'#5b6e71',1)
 if h<8:
  c.poly(a,[(x-.3,h,z-.15),(x+w*.5,h+2,z-.15),(x+w+.3,h,z-.15)],'#19313e','#546970',2)
 # Gutters/downpipes, foundation blocks, brick courses, pavement fence.
 c.line(a,[(x-.1,h,z-.18),(x+w+.1,h,z-.18)],'#688083',3)
 c.line(a,[(x+w-.2,h,z-.18),(x+w-.2,.15,z-.18),(x+w-.5,.15,z-.4)],'#57747d',3)
 for j in range(int(h/.65)):
  y=j*.65;c.line(a,[(x,y,z-.025),(x+w,y,z-.025)],'#39505a',.65)
  for k in range(5):
   xx=x+k*1.3+(j%2)*.65
   if xx<x+w:c.line(a,[(xx,y,z-.03),(xx,y+.6,z-.03)],'#3b515a',.55)
 # Tree/bush mass planted beside frontage; outlined foliage silhouettes.
 if index%2:
  tx=x+w+.7;c.line(a,[(tx,0,z+.3),(tx,4.8,z+.3)],'#08151b',7)
  for dx,yy in [(-.6,4.2),(.6,4.5),(0,5.2)]:
   if c.depth((tx,yy,z+.3))>1:
    sx,sy=c.project((tx+dx,yy,z+.3));sc=c.f/c.depth((tx,yy,z+.3));a.ellipse(sx,sy,sc*.85,sc*1.3,'#102e32','#28473f',1.8)

def lamp(a,c,z,side):
 x=road_x(z)+side*5.4;c.line(a,[(x,.15,z),(x,7.5,z),(x-side*.8,7.8,z)],'#08151d',9)
 c.line(a,[(x+.04,.15,z),(x+.04,7.45,z)],'#5a727a',2)
 if c.depth((x,7.7,z))<1:return
 xx,yy=c.project((x-side*.8,7.7,z));sc=c.f/c.depth((x,7.7,z));a.ellipse(xx,yy,sc*.45,sc*.1,AMBER)
 a.ellipse(xx,yy,sc*2,sc*2.8,'url(#lamphalo)')
 for j in range(9):
  zz=z+j*.38;c.line(a,[(x-side*.8-.7,.05,zz),(x-side*.8+.6,.05,zz)],'#94734e',max(1,sc*.018))
 # runoff under lamp, three distinct depths
 if c.depth((x,.3,z))>1:
  xx,yy=c.project((x,.2,z));a.line([(xx,yy-5),(xx-2,yy+8)],'#7b9aa1',1.2)

def city(a,c,t):
 terrain(a,c,t)
 objects=[]
 for i,z in enumerate(range(-180,500,15)):
  for side in [-1,1]:objects.append((z+4,building,(side,z,i+int(side>0)*31)))
 for i,z in enumerate(range(-180,500,24)):
  objects.append((z,lamp,(z,-1 if i%2 else 1)))
 for zz,fn,args in sorted(objects,key=lambda x:-c.depth((road_x(x[0]),0,x[0]))):
  if 1<c.depth((road_x(zz),0,zz))<190:fn(a,c,*args)
 # Electric wire sag, pole insulators, named junctions.
 for z in range(-180,500,40):
  x=road_x(z)-6.6;c.line(a,[(x,0,z),(x,9.8,z)],'#0a1821',6)
  c.line(a,[(x-.7,8.8,z),(x+.7,8.8,z)],'#45616a',4)
  for j in range(6):
   zz=z+j*40/6;zz2=z+(j+1)*40/6
   c.line(a,[(x,9.1-.65*math.sin(j*math.pi/6),zz),(x,9.1-.65*math.sin((j+1)*math.pi/6),zz2)],'#1c3541',1.5)
 for z,name in [(45,'MERCER ST'),(130,'CEDAR LANE'),(222,'ASH AVENUE')]:
  x=road_x(z)+5.7;c.line(a,[(x,0,z),(x,3.5,z)],'#75908e',4)
  if c.depth((x,3,z))>2:
   xx,yy=c.project((x,3.1,z));sc=min(1.3,c.f/c.depth((x,3,z))/90);a.rect(xx-100*sc,yy-22*sc,200*sc,44*sc,'#21463f','#a4b4a2',2,3);a.add(f'<text x="{xx}" y="{yy+7*sc}" fill="#d8dfcf" font-family="DejaVu Sans" font-size="{18*sc}" text-anchor="middle">{name}</text>')
