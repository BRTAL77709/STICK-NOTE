"""Four explicit risers, landing and a fifth recovery step. Fixed world contacts."""
from contact_rig import *
DURATION=5.;RISE=.18;RUN=.30;WIDTH=.72
INIT=[V(-.30,0,-.09),V(-.14,0,.09)]
PLANS=[[(.42,1.00,V(.15,.18,-.09),.15),(2.16,2.79,V(.75,.54,-.09),.15),(4.10,4.70,V(1.37,.72,-.09),.14)],[(1.28,1.87,V(.45,.36,.09),.16),(3.12,3.80,V(1.05,.72,.09),.15)]]
PRESSURE=[(0,(-.22,0,0)),(.36,(-.14,0,.09)),(1.,(-.14,0,.09)),(1.24,(.15,.18,-.09)),(1.87,(.15,.18,-.09)),(2.12,(.45,.36,.09)),(2.79,(.45,.36,.09)),(3.08,(.75,.54,-.09)),(3.80,(.75,.54,-.09)),(4.06,(1.05,.72,.09)),(4.70,(1.05,.72,.09)),(5.2,(1.23,.72,0)),(6.,(1.23,.72,0))]
HEIGHT=[(0,.65),(.22,.625),(.58,.66),(1.0,.77),(1.45,.86),(1.87,.95),(2.4,1.05),(2.79,1.13),(3.4,1.24),(3.8,1.32),(4.3,1.36),(4.85,1.38),(6.,1.38)]
TIMES=np.arange(181)/30;PPLAN=np.array([channel(t,PRESSURE) for t in TIMES]);HPLAN=np.array([max(.45,hermite(t,HEIGHT)+.10-PPLAN[j,1]) for j,t in enumerate(TIMES)]);A=np.eye(len(TIMES));B=PPLAN[:,[0,2]].copy()
for j in range(1,len(TIMES)-1):
 k=HPLAN[j]/9.81*900;A[j,j]=1+2*k;A[j,j-1]=-k;A[j,j+1]=-k
CPLAN=np.linalg.solve(A,B)
def tread(x):return 0 if x<0 else min(4,int(x/RUN)+1)
def floor_y(x):return RISE*tread(x)
def state(t):
 feet=[]
 for j in range(2):
  f={'sole':INIT[j].copy(),'planted':True,'pitch':0,'heading':math.pi/2};start=INIT[j]
  for a,b,target,lift in PLANS[j]:
   if t<a:break
   f=step(t,start,target,a,b,lift)
   if t<b:break
   start=target
  for a,b,_,__ in PLANS[j]:
   if a-.1<t<a:f['pitch']=-.20*Q(t,a-.1,a)
  f['tread']=tread(f['sole'][0]) if f['planted'] else None;feet.append(foot_geometry(f))
 pressure=channel(t,PRESSURE);desired=V(np.interp(t,TIMES,CPLAN[:,0]),0,np.interp(t,TIMES,CPLAN[:,1]));r=V(desired[0]-.05,hermite(t,HEIGHT),desired[2]);pitch=-float(channel(t,[(0,-.02),(.25,-.17),(.75,-.12),(1.1,-.05),(1.5,-.14),(1.95,-.06),(2.45,-.13),(2.9,-.05),(3.4,-.12),(3.9,-.04),(4.7,.02),(5,0)]));roll=float(channel(t,[(0,0),(.4,-.055),(1,-.04),(1.25,.065),(1.87,.04),(2.12,-.06),(2.79,-.04),(3.08,.055),(3.8,.03),(4.06,-.045),(4.7,0)]))
 for _ in range(10):
  # Enforce the planted-foot reach envelope before solving the body, never stretch bones.
  caps=[]
  P=RY(math.pi/2)@RZ(-roll*.65)
  for j,f in enumerate(feet):
   offset=P@V((.07,-.07)[j],0,0);ank=np.array(f['ankle']);horiz=np.linalg.norm((r+offset-ank)[[0,2]]);caps.append(ank[1]+math.sqrt(max(.001,.722**2-horiz**2))-offset[1])
  r[1]=min(hermite(t,HEIGHT),min(caps))
  # Opposite arm leads each leg; offsets are body-local, not camera translations.
  swing=float(channel(t,[(0,0),(.7,.10),(1.55,-.09),(2.5,.10),(3.5,-.08),(4.5,.04),(5,0)]));R=RY(math.pi/2);hands=[r+R@V(.19,.14,swing+.10),r+R@V(-.19,.12,-swing+.10)]
  p=pose(r,feet,hands,heading=math.pi/2,pitch=pitch,roll=roll,pelvis_roll=-roll*.65,twist=swing*.45,head_lag=-.02*Q(t,.25,.6)+.02*Q(t,4.3,4.8),look=1.,fear=.32,knee_forward=V(1,.08,0));c=com(p);r+=V(desired[0]-c[0],0,desired[2]-c[2])*.8
 return {'time':t,'pose':p,'fingers':[[],[]],'hand_frames':[None,None],'com':com(p),'pressure':pressure,'phase':('anticipate' if t<.42 else 'stair ascent' if t<3.8 else 'landing / recovery'),'targets':[q['sole'] for q in feet],'fixed_targets':[target for plans in PLANS for _,__,target,___ in plans],'support':['L' if j==0 else 'R' for j,f in enumerate(feet) if f['planted']],'tread_indices':[f['tread'] for f in feet]}

# Predict body trajectory over the contact schedule before rendering any frame.
_raw_state=state
def state(t):
 from stabilize import stabilized
 return stabilized('STAIRS',_raw_state,5,t)
