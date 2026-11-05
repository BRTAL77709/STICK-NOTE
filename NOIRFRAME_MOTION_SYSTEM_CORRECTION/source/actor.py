"""Same approved head/hoodie colours and limb dimensions; torso/hips now have parent frames."""
from world import *
from approved_head import head

def actor(w,d,seated=False):
 p=d['pose'];r=p['root'];sh=p['shoulder'];R=p['torso_basis'];P=p['pelvis_basis']
 for j in [1,0]:
  l=p['legs'][j]
  w.tube([l['hip'],l['knee']],'#263e4b',.105);w.tube([l['knee'],l['ankle']],'#1b3343',.10)
  if 'heel' in l:
   grid=np.array(l['sole_mesh']);up=np.array(l['shoe_up']);top=np.array([[q+up*(.070-.015*u/4) for q in row] for u,row in enumerate(grid)])
   for u in range(4):
    for v in range(4):
     w.face([grid[u,v],grid[u+1,v],grid[u+1,v+1],grid[u,v+1]],'#101f2c',stroke='none',name='contact sole')
     w.face([top[u,v],top[u+1,v],top[u+1,v+1],top[u,v+1]],'#253f4d',stroke='none',name='shoe top')
   border=[(u,0) for u in range(5)]+[(4,v) for v in range(1,5)]+[(u,4) for u in reversed(range(4))]+[(0,v) for v in reversed(range(1,4))]
   for (u,v),(a,b) in zip(border,border[1:]+border[:1]):w.face([grid[u,v],grid[a,b],top[a,b],top[u,v]],'#1d3443',w=2,name='shoe side')
  else:
   f=l.get('shoe_origin',l['sole']);a=l.get('pitch',0);F=V(math.sin(l['heading']),0,math.cos(l['heading']));pts=[f+F*(x*math.cos(a)-y*math.sin(a))+V(0,x*math.sin(a)+y*math.cos(a),0) for x,y in [(-.105,0),(.105,0),(.12,.035),(.045,.085),(-.08,.08)]];side=np.cross(V(0,1,0),F);near=[p-side*.045 for p in pts];far=[p+side*.045 for p in pts];w.face(near,'#142733',w=3,bias=-.001,name='shoe');w.face(far,'#142733',w=3,name='shoe')
   for j in range(5):w.face([near[j],near[(j+1)%5],far[(j+1)%5],far[j]],'#1b3543',w=2,name='shoe tread volume')
   w.line([near[0]+V(0,.008,0),near[1]+V(0,.008,0)],'#8fa1a4',2)
 # Far sleeve, then hoodie as a shallow cel-shaded articulated volume, then near sleeve.
 for j in [1,0]:
  arm=p['arms'][j];w.tube([arm['shoulder'],arm['elbow']],'#294653' if j==0 else '#193342',.102);
  A=arm['elbow'];B=arm['wrist'];N=np.cross(B-A,w.cam.forward);N/=np.linalg.norm(N)
  w.face([A+N*.048,B+N*.0275,B-N*.0275,A-N*.048],'#294653' if j==0 else '#193342',w=4,name='tapered sleeve')
  palm(w,arm['wrist'],d.get('hand_frames',[None,None])[j])
 a=r+P@V(-.17,-.06,-.115);b=r+P@V(.17,-.06,-.115);c=sh+R@V(.19,0,-.13);e=sh+R@V(-.19,0,-.13)
 back=[a,b,c,e];front=[r+P@V(-.17,-.06,.115),r+P@V(.17,-.06,.115),sh+R@V(.19,0,.13),sh+R@V(-.19,0,.13)]
 w.face(back,'#172f3d',w=5,name='hoodie back');w.face(front,'#294653',w=5,name='hoodie front')
 for j in range(4):w.face([back[j],back[(j+1)%4],front[(j+1)%4],front[j]],'#1c3543',w=4,name='hoodie side')
 for x in [-.052,.052]:w.line([sh+R@V(x,.01,.142),sh+R@V(x,-.21,.142)],'#91a3a4',1.8)
 # Drawn hood at the neck retains the approved outlined silhouette.
 w.face([sh+R@V(-.17,0,.12),sh+R@V(-.12,.10,.13),sh+R@V(.12,.10,.13),sh+R@V(.17,0,.12),sh+R@V(.04,-.08,.14),sh+R@V(-.04,-.08,.14)],'#152d3b',w=3,name='hood')
 h=p['head'];x,y=w.cam(h);S=w.cam.scale(h)*.26/(61*2.62)
 def draw(a):
  a.add(f'<g transform="translate({x} {y}) scale({S})">');head(a,0,0,d['time'],p['yaw'],p['yaw'],p['fear'],p['tilt'],blink_override=0);a.add('</g>')
 w.submit([h],draw,-.045)
 for group in d.get('fingers',[]):
  for f in group:
   w.tube([f['base'],f['joint'],f.get('tip_center',f['pad'])],'#d1d7d2',.014)

def palm(w,p,R=None):
 x,y=w.cam(p);S=w.cam.scale(p)
 angle=0 if R is None else math.degrees(math.atan2(*(np.array(w.cam(np.array(p)+R@V(0,.05,0)))-V(x,y))[::-1]))-90
 def draw(a):
  a.add(f'<g transform="rotate({angle} {x} {y})">');a.ellipse(x,y,S*.032,S*.040,'#d1d7d2',INK,2.5);a.add('</g>')
 w.submit([p],draw,-.025)
