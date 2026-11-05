"""V11 shared illustrated skeleton. SI world XYZ (Y up), explicit planted soles, independent IK poles."""
import math,numpy as np
V=lambda *p:np.array(p,dtype=float)
def clamp(x,a=0,b=1):return max(a,min(b,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def E(t,a,b):return smooth((t-a)/(b-a))
def mix(a,b,u):return np.asarray(a)+(np.asarray(b)-a)*u

def keys(t,rows):
 if t<=rows[0][0]:return np.asarray(rows[0][1],float)
 for (a,x),(b,y) in zip(rows,rows[1:]):
  if t<=b:return mix(x,y,E(t,a,b))
 return np.asarray(rows[-1][1],float)
def ik(a,b,l1,l2,pole):
 a=np.asarray(a);b=np.asarray(b);d=np.linalg.norm(b-a)
 if not abs(l1-l2)+1e-6<d<l1+l2-1e-6:raise ValueError(('UNREACHABLE',a.tolist(),b.tolist(),float(d),l1+l2))
 u=(b-a)/d;p=np.asarray(pole,float);p-=u*np.dot(p,u)
 if np.linalg.norm(p)<1e-6:p=np.cross(u,V(0,0,1))
 p/=np.linalg.norm(p);q=(l1*l1-l2*l2+d*d)/(2*d);return a+q*u+math.sqrt(max(0,l1*l1-q*q))*p

def feet(t,initial,plans):
 out=[]
 for j in range(2):
  p=np.asarray(initial[j],float);on=True;pitch=0
  for a,b,target,lift in plans[j]:
   if t<a:break
   if t<b:
    u=(t-a)/(b-a);q=mix(p,target,E(u,.28 if target[1]>p[1]+.05 else .1,.95));q[1]=p[1]+(target[1]-p[1])*E(u,0,.55)+lift*math.sin(math.pi*u)**1.2;p=q;on=False;pitch=.22*math.sin(math.pi*u);break
   p=np.asarray(target,float)
  out.append({'sole':p,'planted':on,'pitch':pitch})
 return out

def skeleton(root,ff,hands=None,lean=0,yaw=.7,fear=.6,head_tilt=0,head_lead=0,breath=0,arm_poles=None):
 root=np.asarray(root,float);shoulder=root+V(lean,.50+breath,0);head=shoulder+V(.025+head_lead,.29,0);legs=[];arms=[]
 for j in range(2):
  h=root+V((.035,-.035)[j],0,(-.07,.07)[j]);f=ff[j];ank=f['sole']+V(0,.055,0);k=ik(h,ank,.37,.37,V(1,0,.13));legs.append({**f,'hip':h,'knee':k,'ankle':ank})
  sh=shoulder+V((.13,-.13)[j],(-.012,.012)[j],(-.025,.025)[j]);hand=np.asarray(hands[j] if hands is not None else root+V((.18,-.18)[j],.16,(-.05,.05)[j]),float);el=ik(sh,hand,.34,.34,V((1,-1)[j],-.35,(-.3,.3)[j]) if arm_poles is None else arm_poles[j]);arms.append({'shoulder':sh,'elbow':el,'wrist':hand})
 return {'root':root,'shoulder':shoulder,'head':head,'legs':legs,'arms':arms,'yaw':yaw,'fear':fear,'tilt':head_tilt}
