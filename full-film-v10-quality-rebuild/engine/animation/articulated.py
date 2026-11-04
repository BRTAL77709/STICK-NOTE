"""Strict, inspectable full-body 2D joint rig; the approved head and clothes stay intact."""
import math
from approved_components import ik,limb
from driver_rig import head
INK='#030b13'
def solve_ik(origin,target,a,b,bend):
 d=math.dist(origin,target)
 if d>a+b+1e-5 or d<abs(a-b)-1e-5:raise ValueError(f'Contact unreachable: {d:.3f} not [{abs(a-b)},{a+b}]; {origin}->{target}')
 return ik(origin,target,a,b,bend)
def run_feet(distance,stride=360.):
 feet=[]
 for j in [0,1]:
  q=distance/stride+j*.5;k=math.floor(q);u=q-k;anchor=(k-j*.5+.18)*stride
  if u<.38:x=anchor-distance;y=0;on=True
  else:
   v=(u-.38)/.62;w=v*v*(3-2*v);x=anchor+stride*w-distance;y=-55*math.sin(math.pi*v);on=False
  feet.append((x,y,on))
 return feet

def walk_feet(distance,stride=140.):
 feet=[]
 for j in [0,1]:
  q=distance/stride+j*.5;k=math.floor(q);u=q-k;anchor=(k-j*.5+.28)*stride
  if u<.62:x=anchor-distance;y=0;on=True
  else:
   v=(u-.62)/.38;w=v*v*(3-2*v);x=anchor+stride*w-distance;y=-28*math.sin(math.pi*v);on=False
  feet.append((x,y,on))
 return feet

def pose(t,hip=(0,-150),lean=0,feet=None,hands=None,head_yaw=0,gaze=None,fear=.5,blink=0):
 hx,hy=hip;lean=max(-75,min(75,lean));sh=(hx+lean,hy-math.sqrt(125**2-lean**2));feet=feet or [(-23,0,True),(24,0,True)];hands=hands or {};legs=[];arms=[]
 for j,foot in enumerate(feet):
  fx,fy,on=foot[:3];shoe_scale=foot[3] if len(foot)>3 else 1.
  start=(hx-15+32*j,hy);ank=(fx,fy-12*shoe_scale);knee=solve_ik(start,ank,85,85,-1);legs.append({'hip':start,'knee':knee,'ankle':ank,'sole':(fx,fy),'planted':on,'shoe_scale':shoe_scale})
 for j in [0,1]:
  shoulder=(sh[0]-35+70*j,sh[1]+14);hand=hands.get(j,(hx-43+88*j,hy-10));elbow=solve_ik(shoulder,hand,90,87,1 if j==0 else -1);arms.append({'shoulder':shoulder,'elbow':elbow,'hand':hand})
 return {'t':t,'hip':hip,'shoulder_center':sh,'head':(sh[0]+2,sh[1]-72),'head_yaw':head_yaw,'gaze':head_yaw if gaze is None else gaze,'fear':fear,'blink':blink,'legs':legs,'arms':arms}

def draw(a,x,ground,scale,p,phone=None,back=False):
 a.add(f'<g transform="translate({x} {ground}) scale({scale})">')
 for j,l in enumerate(p['legs']):
  limb(a,[l['hip'],l['knee'],l['ankle']],'#1b3342' if j==0 else '#294653',28);fx,fy=l['sole'];a.add(f'<g transform="translate({fx} {fy}) scale({l["shoe_scale"]})">');a.path('M-22 -8 Q7 -22 32 -10 L32 0 H-22Z','#10222f',INK,5);a.add('</g>')
 hx,hy=p['hip'];sx,sy=p['shoulder_center'];a.path(f'M{sx-47} {sy-7} Q{sx-61} {sy+20} {hx-44} {hy+15} Q{hx} {hy+26} {hx+48} {hy+12} L{sx+46} {sy+5} Q{sx+25} {sy-22} {sx-47} {sy-7}Z','url(#cloth)',INK,7);a.path(f'M{sx-35} {sy-12} Q{sx} {sy+34} {sx+35} {sy-12} L{sx+20} {sy-32} L{sx-22} {sy-32}Z','#102634',INK,5)
 for side in [-1,1]:a.path(f'M{hx+side*39} {hy-35} q{side*8} 14 {-side*1} 29','none','#4b6470',2.2)
 for dx in [-14,14]:a.line([(sx+dx,sy+7),(sx+dx,sy+42)],'#738691',2)
 for hand_id,arm in enumerate(p['arms']):
  limb(a,[arm['shoulder'],arm['elbow'],arm['hand']],'#233e4e',26);px,py=arm['hand'];a.add(f'<g transform="rotate({p.get("wrist_angles",{}).get(hand_id,0)} {px} {py})">');a.ellipse(px,py,14,17,'#d8ded1',INK,4)
  for j in range(3):a.line([(px-8+j*6,py-7),(px-6+j*6,py+4)],'#7a928d',1.5)
  a.add('</g>')
 headx,heady=p['head']
 if back:
  a.ellipse(headx,heady,61,66,'#102937',INK,5);a.path(f'M{headx-61} {heady-12} Q{headx-61} {heady-80} {headx} {heady-80} Q{headx+59} {heady-76} {headx+61} {heady-16}Z','#142d3b','#6b8794',3);a.path(f'M{headx-48} {heady-49} Q{headx-40} {heady-71} {headx-22} {heady-75}','none','#d6a45e',3)
 else:
  a.add(f'<g transform="translate({headx} {heady}) scale({1/2.62})">');head(a,0,0,p['t'],p['head_yaw'],p['gaze'],p['fear'],blink_override=p['blink']);a.add('</g>')
 if phone:
  px,py=p['arms'][1]['hand'];angle=phone.get('angle',-12);a.add(f'<g transform="translate({px} {py}) rotate({angle})">');a.rect(-14,-44,28,73,'#07131d','#a2b0b0',3,5);a.rect(-9,-35,18,53,'#23414f');a.add('</g>')
 a.add('</g>');return {'hands':[(x+scale*q['hand'][0],ground+scale*q['hand'][1]) for q in p['arms']],'head':(x+scale*headx,ground+scale*heady)}