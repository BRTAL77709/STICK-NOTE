"""Approved illustrated witness assembled from articulated world-space joint primitives."""
from world import *
from approved_head import head

def actor(w,d,grip=None):
 p=d['pose'];r=p['root'];sh=p['shoulder'];S=w.cam.scale(r)
 for j in [1,0]:
  leg=p['legs'][j];f=leg['sole'];a=leg['pitch'];co,si=math.cos(a),math.sin(a)
  for aa,bb in [(leg['hip'],leg['knee']),(leg['knee'],leg['ankle'])]:w.tube([aa,bb],'#172d3b' if j else '#263e4b',.10)
  pts=[f+(V(0,x*si+y*co,x*co-y*si) if d.get('seated') else V(x*co-y*si,x*si+y*co,0)) for x,y in [(-.105,0),(.105,0),(.12,.035),(.045,.085),(-.08,.08)]];w.face(pts,'#142733',w=4,bias=-.015,name='shoe');w.line([pts[0]+V(0,.009,0),pts[1]+V(0,.009,0)],'#99a6a3',2,-.02)
  if leg['planted']:
   w.face([f+V(-.14,.002,-.055),f+V(.16,.002,-.055),f+V(.13,.002,.055),f+V(-.13,.002,.055)],'#0b1b25',stroke='none',bias=.02,name='contact shadow')
 for j in [1,0]:
  a=p['arms'][j]
  for aa,bb in [(a['shoulder'],a['elbow']),(a['elbow'],a['wrist'])]:w.tube([aa,bb],'#1b3444' if j else '#2b4654',.098)
  hand(w,a['wrist'],grip if j==0 else None)
 pts=[sh+V(-.20,.015,0),sh+V(.18,.015,0),r+V(.20,-.04,0),r+V(.12,-.10,0),r+V(-.19,-.07,0)]
 w.face(pts,'#1a303e',w=5,bias=.005,name='hoodie');w.face([sh+V(-.18,.01,-.008),sh+V(-.11,.13,-.008),sh+V(.10,.13,-.008),sh+V(.18,.01,-.008),sh+V(.05,-.09,-.008),sh+V(-.06,-.09,-.008)],'#263e4a',w=3,bias=-.01,name='hood')
 for dx in [-.055,.055]:w.line([sh+V(dx,-.06,-.02),sh+V(dx,-.25,-.02)],'#94a5a6',1.7)
 w.line([r+V(-.13,.11,-.025),r+V(.12,.11,-.025)],'#57707b',2)
 h=p['head'];x,y=w.cam(h);scale=w.cam.scale(h)*.26/(61*2.62)
 def draw(a):
  a.add(f'<g transform="translate({x} {y}) scale({-scale if d.get('mirror_head') else scale} {scale})">');head(a,0,0,d['time'],p['yaw'],p['yaw'],p['fear'],p['tilt'],blink_override=max(0,1-abs(d['time']%3.7-1.1)/.065));a.add('</g>')
 w.submit([h],draw,-.05)

def hand(w,p,target=None):
 p=np.array(p);S=w.cam.scale(p);x,y=w.cam(p);r=S*.047
 def draw(a):
  a.ellipse(x,y,r*.8,r,'#d1d7d2',INK,2.5)
  if target is not None:
   q=np.array(w.cam(target));v=q-V(x,y);nn=np.linalg.norm(v)
   if nn>1:
    n=V(-v[1],v[0])/nn
    for j in [-1,1]:
     u=V(x,y)+n*r*.65*j;c=(V(x,y)+q)/2+n*r*.6*j;a.path(f'M{u[0]} {u[1]} Q{c[0]} {c[1]} {q[0]} {q[1]}','none','#d1d7d2',max(3,S*.016))
  else:
   for j in range(3):a.path(f'M{x-r*.4+j*r*.35} {y} q{-r*.15} {r*.4} {r*.15} {r*.55}','none','#6b858c',1.3)
 w.submit([p],draw,-.04)
