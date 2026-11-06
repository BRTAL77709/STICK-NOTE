"""Contact-first running: continuous root velocity, short stance/long swing, fixed landing targets.
No force-simulation claim. Source metres/Y up; actual native IK is baked afterwards.
"""
import math,numpy as np
from contact_rig import V,RY,RZ,Q,mix,clamp,pose,foot_geometry
from scipy.interpolate import PchipInterpolator,CubicHermiteSpline
from scipy.optimize import lsq_linear
from scipy.sparse import diags,csr_matrix
import vehicle_system as VS
PLAN=None
class RunPlan:
 def __init__(self,baseline,initial_feet):
  self.baseline=baseline;self.initial=initial_feet(5.45);self.heading=-math.pi/2;self.F=V(-1,0,0);self.S=V(0,0,1);self.M=RY(VS.PARK['yaw']);self.O=np.array(VS.PARK['position'])
  ts=np.array([5.45,5.95,6.42,6.92,7.42,7.92,8.42,8.96,9.52,10.30]);values=np.array([[-1.20,.63,-.20],[-1.37,.68,-.20],[-1.68,.68,-.14],[-2.25,.68,-.06],[-2.86,.68,.05],[-3.52,.68,.16],[-4.15,.68,.29],[-4.72,.79,.43],[-5.13,.84,.58],[-5.22,.86,.60]])
  values[0]=baseline(5.45)['pose']['root'];values[-1]=baseline(10.3)['pose']['root'];vel=PchipInterpolator(ts,values,axis=0).derivative()(ts);vel[0]=vel[-1]=0;self.path=CubicHermiteSpline(ts,values,vel,axis=0);self.events={0:[],1:[]}
  contacts=[(5.90,1),(6.24,0),(6.58,1),(6.92,0),(7.26,1),(7.60,0),(7.94,1),(8.28,0),(8.62,1),(8.96,0),(9.30,1),(9.72,0),(10.18,1)]
  for t,j in contacts:
   r=self.path(t);lead=.02+.14*min(1,abs(float(self.path(t,1)[0]))/.8);p=r+self.F*lead+self.S*(.07,-.07)[j];p[1]=0;p=self.flat_landing(p);a=max(5.52,t-(.40 if t>9.4 else .46));self.events[j].append((a,t,p))
  self.times=np.linspace(5.45,10.3,583);roots=self.path(self.times);caps=[]
  for t,r in zip(self.times,roots):
   cap=r[1];roll=self.roll(t)
   for j,f in enumerate(self.feet(t)):
    off=RY(self.heading)@RZ(roll)@V((.07,-.07)[j],0,0);h=np.linalg.norm((r+off-f['ankle'])[[0,2]]);cap=min(cap,f['ankle'][1]-off[1]+math.sqrt(max(.001,.72**2-h*h)))
   caps.append(cap)
  caps=np.array(caps);n=len(self.times);D2=diags([np.ones(n-2),-2*np.ones(n-2),np.ones(n-2)],[0,1,2],shape=(n-2,n)).toarray();D3=diags([-np.ones(n-3),3*np.ones(n-3),-3*np.ones(n-3),np.ones(n-3)],[0,1,2,3],shape=(n-3,n)).toarray();A=np.vstack([np.eye(n),math.sqrt(4e6)*D2,math.sqrt(1e7)*D3]);rhs=np.r_[roots[:,1],np.zeros(n-2),np.zeros(n-3)];fixed=np.zeros(n);fixed[:3]=values[0,1];fixed[-3:]=values[-1,1];rhs-=A@fixed;upper=caps[3:-3]-.002
  if upper.min()<=.35:raise RuntimeError(('RUN_CONTACT_ENVELOPE_INFEASIBLE',float(upper.min())))
  result=lsq_linear(csr_matrix(A[:,3:-3]),rhs,bounds=(np.full(n-6,.35),upper),method='trf',lsq_solver='lsmr',lsmr_tol=1e-11,tol=1e-8,max_iter=300)
  if not result.success:raise RuntimeError(('RUN_VERTICAL_SOLVE',result.message))
  roots[:,1]=fixed;roots[3:-3,1]=result.x;self.roots=roots
 def ground(self,p):
  q=self.O+self.M@np.array(p);z0=-24+5*math.floor((q[2]+24)/5);u=(q[2]-z0)/5;center=VS.roadref(z0)*(1-u)+VS.roadref(z0+5)*u;x=abs(q[0]-center);return 0 if x<=4.5 else .13*min(1,(x-4.5)/.2)
 def corners(self,f):
  F=self.F*math.cos(f['pitch'])+V(0,math.sin(f['pitch']),0);return [f['shoe_origin']+F*x+self.S*z for x in [-.12,.12] for z in [-.055,.055]]
 def flat_landing(self,p):
  p=p.copy();heights=[self.ground(p+self.F*x+self.S*z) for x in [-.12,.12] for z in [-.055,.055]]
  if max(heights)-min(heights)>.0005:
   direction=1 if self.ground(p)>.06 else -1
   for _ in range(20):
    p+=self.F*.02*direction;heights=[self.ground(p+self.F*x+self.S*z) for x in [-.12,.12] for z in [-.055,.055]]
    if max(heights)-min(heights)<.0005:break
  p[1]=max(heights);return p
 def envelope(self,t):return Q(t,5.45,5.8)*(1-Q(t,9.6,10.3))*min(1,abs(float(self.path(np.clip(t,5.45,10.3),1)[0]))/1.0)
 def roll(self,t):return .015*self.envelope(t)*math.cos(math.pi*(t-6.24)/.34)
 def feet(self,t):
  out=[]
  for j in range(2):
   start=np.array(self.initial[j]['sole']).copy();f={'sole':start,'pitch':0.,'heading':self.heading,'planted':True}
   for a,b,target in self.events[j]:
    if t<=a:
     f={'sole':start,'pitch':-.10*Q(t,a-.04,a),'heading':self.heading,'planted':True};break
    if t<b:
     u=clamp((t-a)/(b-a));p=mix(start,target,Q(t,a,b));p[1]+=.12*math.sin(math.pi*u)**2;pitch=(-.10*(1-Q(u,0,.22))+.075*math.sin(math.pi*u))*(1-Q(u,.88,1));f=foot_geometry({'sole':p,'pitch':pitch,'heading':self.heading,'planted':False});raise_y=max(0,max(self.ground(q)-q[1] for q in self.corners(f)));p=p+V(0,raise_y+.003*math.sin(math.pi*u)**2,0);f={'sole':p,'pitch':pitch,'heading':self.heading,'planted':False};break
    start=target.copy();f={'sole':start,'pitch':0.,'heading':self.heading,'planted':True}
   out.append(foot_geometry(f))
  return out
 def root(self,t):return np.array([np.interp(t,self.times,self.roots[:,j]) for j in range(3)])
def repair(d,t,baseline,initial_feet):
 global PLAN
 if t<5.45:return d
 if PLAN is None:PLAN=RunPlan(baseline,initial_feet)
 p=d['pose'];r=PLAN.root(t);w=PLAN.envelope(t);swing=.11*w*math.cos(math.pi*(t-6.24)/.34);h=-math.pi/2;hands=[r+RY(h)@V(.20,.16+.02*w,.12-swing),r+RY(h)@V(-.20,.16+.02*w,.12+swing)];roll=PLAN.roll(t);pp=pose(r,PLAN.feet(t),hands,heading=h,pitch=.12*(Q(t,4.7,5.6)-Q(t,9.5,10.3)),roll=-roll*.5,pelvis_roll=roll,twist=-.035*w*math.cos(math.pi*(t-6.24)/.34),fear=p.get('fear',.75),look=.85,knee_forward=RY(h)@V(0,.5,1));pp['head_forward']=p.get('head_forward',V(-1,0,0));d['pose']=pp;d['support']=[j for j,f in enumerate(pp['legs']) if f['planted']];d['phase']='continuous root momentum / short planted stance / articulated swing / weight transfer / stop';return d
