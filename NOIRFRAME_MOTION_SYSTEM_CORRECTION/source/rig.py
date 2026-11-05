"""Math-only compatibility helpers and fixed-length two-bone IK. Old cycle/skeleton functions removed."""
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
 u=(b-a)/d;p=np.array(pole,dtype=float,copy=True);p-=u*np.dot(p,u)
 if np.linalg.norm(p)<1e-6:p=np.cross(u,V(0,0,1))
 p/=np.linalg.norm(p);q=(l1*l1-l2*l2+d*d)/(2*d);return a+q*u+math.sqrt(max(0,l1*l1-q*q))*p

