"""Reusable contact-aware full-body witness; approved cap/hoodie/head renderer."""
import math
from approved_components import limb,ik
from driver_rig import head
from motion_state import ease
INK='#030b13'
def gait(progress,j,stride=106):
 q=progress/stride+j*.5;k=math.floor(q);u=q-k;anchor=(k-j*.5+.26)*stride
 if u<.60:return anchor-progress,0,True
 v=(u-.60)/.40;w=v*v*(3-2*v)
 return anchor+stride*w-progress,-35*math.sin(math.pi*v),False

def stair_gait(progress,j):
 stride=104.;rise=112.;q=progress/stride+j*.5;k=math.floor(q);u=q-k;anchor=(k-j*.5+.26)*stride
 level=lambda x:-56*math.floor(x/52)
 if u<.60:return anchor-progress,level(anchor)+rise/stride*progress,True
 v=(u-.60)/.40;w=v*v*(3-2*v);xx=anchor+stride*w
 return xx-progress,level(anchor)*(1-w)+level(anchor+stride)*w+rise/stride*progress-32*math.sin(math.pi*v),False

def actor(a,x,ground,t,progress=0,scale=1,run=False,yaw=0,fear=.4,hand_target=None,phone=False,slope=0,stairs=False,feet_override=None,back=False,reaction=0):
 a.add(f'<g transform="translate({x} {ground}) scale({scale})">')
 hip=(12 if run else 0,-90 if stairs else (-140 if run else -157));bob=3*math.sin(progress/106*math.tau) if run else 1.4*math.sin(t*3)
 if reaction:bob+=2*reaction*math.sin((t-67)*5.2)
 hip=(hip[0],hip[1]+bob);sh=(hip[0]+(28 if run else 0),hip[1]-123)
 if reaction:
  hip=(hip[0]-6*reaction,hip[1]-4*reaction);sh=(sh[0]-14*reaction,sh[1]-9*reaction)
 for j in (0,1):
  fx,fy,on=feet_override[j] if feet_override else ((stair_gait(progress,j) if stairs else gait(progress,j)) if run else (-23+47*j,0,True));fy+=slope*fx;ank=(fx,fy-10);h=(hip[0]-15+32*j,hip[1]);k=ik(h,ank,85,85,-1)
  limb(a,[h,k,ank],'#1b3342' if j==0 else '#294653',28)
  a.path(f'M{fx-20} {fy-9} Q{fx+8} {fy-21} {fx+31} {fy-3} L{fx+32} {fy+7} H{fx-20}Z','#10222f',INK,5)
 sx,sy=sh;hx,hy=hip
 a.path(f'M{sx-47} {sy-7} Q{sx-61} {sy+20} {hx-44} {hy+15} Q{hx} {hy+26} {hx+48} {hy+12} L{sx+46} {sy+5} Q{sx+25} {sy-22} {sx-47} {sy-7}Z','url(#cloth)',INK,7)
 a.path(f'M{sx-35} {sy-12} Q{sx} {sy+34} {sx+35} {sy-12} L{sx+20} {sy-32} L{sx-22} {sy-32}Z','#102634',INK,5)
 for dx in [-14,14]:a.line([(sx+dx,sy+7),(sx+dx,sy+42)],'#738691',2)
 hands=[]
 for j in (0,1):
  shoulder=(sx-35+70*j,sy+14)
  if j==1 and hand_target is not None:hand=hand_target
  elif run:hand=(sx+(-55 if j==0 else 55)+25*math.sin(progress/106*math.tau+j*math.pi),sy+60+25*math.cos(progress/106*math.tau+j*math.pi))
  else:hand=(hx-43+88*j,hy-10)
  elbow=ik(shoulder,hand,90,87,1 if j==0 else -1);limb(a,[shoulder,elbow,hand],'#233e4e',26);a.ellipse(*hand,14,17,'#d8ded1',INK,4);hands.append(hand)
 # Cancel head renderer's scene scale, preserving approved proportions in full-body rig.
 if back:
  a.ellipse(sx+2,sy-72,61,66,'#102937',INK,5);a.path(f'M{sx-59} {sy-84} Q{sx-59} {sy-152} {sx+2} {sy-152} Q{sx+61} {sy-148} {sx+63} {sy-88}Z','#142d3b','#6b8794',3);a.path(f'M{sx-46} {sy-121} Q{sx-38} {sy-143} {sx-20} {sy-147}','none','#d6a45e',3)
 else:
  a.add(f'<g transform="translate({sx+2} {sy-72}) scale({1/2.62})">');head(a,0,0,t,yaw,yaw,fear);a.add('</g>')
 if phone:
  px,py=hands[1];a.add(f'<g transform="translate({px} {py}) rotate(-12)">');a.rect(-14,-44,28,73,'#07131d','#a2b0b0',3,5);a.rect(-9,-35,18,53,'#23414f');a.add('</g>')
 a.add('</g>');return {'hands':[(x+scale*q[0],ground+scale*q[1]) for q in hands],'head':(x+scale*(sx+2),ground+scale*(sy-72))}
