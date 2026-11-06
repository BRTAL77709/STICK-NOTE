import math,numpy as np
V=lambda *p:np.array(p,dtype=float)
def clamp(x,a=0,b=1):return max(a,min(b,x))
def mix(a,b,u):return np.asarray(a)+(np.asarray(b)-a)*u
