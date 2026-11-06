"""Predictive, contact-feasible pelvis trajectories. Existing foot/grip targets stay immutable."""
import copy
import numpy as np
from scipy.ndimage import gaussian_filter1d,minimum_filter1d
from scipy.optimize import lsq_linear
from scipy.sparse import diags
from contact_rig import *
CACHE={};METRICS={}

def prepare(name,fn,duration):
 raw=[fn(i/30) for i in range(round(duration*30))];roots=np.array([d['pose']['root'] for d in raw]);n=len(raw);smooth=roots.copy()
 for axis in [0,2]:smooth[:,axis]=gaussian_filter1d(roots[:,axis],2.2 if name=='STAIRS' else 3.0,mode='nearest')
 lower=np.full(n,.44);upper=np.full(n,10.)
 for i,d in enumerate(raw):
  p=d['pose']
  for l in p['legs']:
   off=l['hip']-p['root'];ank=np.array(l['ankle']);h=np.linalg.norm((smooth[i]+off-ank)[[0,2]]);reach=np.sqrt(max(1e-5,.722**2-h*h));upper[i]=min(upper[i],ank[1]-off[1]+reach)
  if name=='KEY_DOOR' and d['contact']:
   arm=p['arms'][1];off=arm['shoulder']-p['root'];w=arm['wrist'];h=np.linalg.norm((smooth[i]+off-w)[[0,2]]);reach=np.sqrt(max(1e-5,.670**2-h*h));lower[i]=max(lower[i],w[1]-off[1]-reach);upper[i]=min(upper[i],w[1]-off[1]+reach)
 # Anticipate an upcoming reach limit instead of snapping down when it is encountered.
 conservative=gaussian_filter1d(minimum_filter1d(upper,size=11,mode='nearest'),2,mode='nearest');upper=np.minimum(upper,conservative)-.001
 if np.any(lower>upper):raise ValueError(('PELVIS_BOUNDS_INFEASIBLE',name))
 D2=diags([np.ones(n-2),-2*np.ones(n-2),np.ones(n-2)],[0,1,2],shape=(n-2,n)).tocsr();D3=diags([-np.ones(n-3),3*np.ones(n-3),-3*np.ones(n-3),np.ones(n-3)],[0,1,2,3],shape=(n-3,n)).tocsr();target=roots[:,1]
 matrix=np.vstack([np.eye(n),math.sqrt(14000)*D2.toarray(),math.sqrt(7000)*D3.toarray()]);rhs=np.concatenate([target,np.zeros(n-2),np.zeros(n-3)])
 result=lsq_linear(matrix,rhs,bounds=(lower,upper),method='bvls',tol=1e-10,max_iter=1000)
 if not result.success:raise RuntimeError(('PELVIS_SOLVE',name,result.message))
 smooth[:,1]=result.x;out=[]
 for i,d in enumerate(raw):
  d=copy.deepcopy(d);p=d['pose'];oldroot=p['root'].copy();r=smooth[i];delta=r-oldroot
  for k in ['root','shoulder','head','chest','neck']:p[k]=p[k]+delta
  forward=p['pelvis_basis']@V(0,0,1);heading=math.atan2(forward[0],forward[2]);side=RY(heading)@V(1,0,0)
  for l in p['legs']:l['hip']=l['hip']+delta;l['knee']=ik(l['hip'],l['ankle'],.37,.37,np.cross(-side,l['ankle']-l['hip']))
  t=i/30
  attached=0.
  if name=='KEY_DOOR':attached=max(Q(t,1.,1.10)*(1-Q(t,4.30,4.40)),Q(t,4.40,4.92)*(1-Q(t,7.,7.32)),Q(t,9.50,10.0))
  for j,arm in enumerate(p['arms']):
   pole=arm['elbow']-arm['shoulder'];arm['shoulder']=arm['shoulder']+delta;arm['wrist']=arm['wrist']+delta*(1-attached if j==1 else 1.);arm['elbow']=ik(arm['shoulder'],arm['wrist'],.34,.34,pole)
  if 'com' in d:d['com']=com(p)
  if name=='KEY_DOOR':d['grip']=p['arms'][1]['wrist']
  d['pelvis_solver']='predictive bounded trajectory / fixed foot and prop constraints';out.append(d)
 before=np.diff(roots,n=2,axis=0)*900;after=np.diff(smooth,n=2,axis=0)*900;METRICS[name]={'before_peak_root_acceleration_m_s2':float(np.linalg.norm(before,axis=1).max()),'after_peak_root_acceleration_m_s2':float(np.linalg.norm(after,axis=1).max()),'solver_success':bool(result.success),'solver_message':str(result.message)};CACHE[name]=out

def stabilized(name,fn,duration,t):
 if name not in CACHE:prepare(name,fn,duration)
 return copy.deepcopy(CACHE[name][min(len(CACHE[name])-1,max(0,round(t*30)))])
