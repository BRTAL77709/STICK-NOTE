from contact_rig import *
DURATION=3.
INIT=[V(2.00,2.2,1.32),V(1.76,2.0,1.50)]
PLANS=[[(1.05,1.50,V(2.52,2.4,1.32),.17),(2.50,2.93,V(3.04,2.4,1.32),.11)],[(.28,.82,V(2.24,2.4,1.50),.19),(1.80,2.25,V(2.82,2.4,1.50),.12)]]
PRESSURE=[(0,(1.94,2.15,1.40)),(.24,(2.0,2.2,1.32)),(.82,(2.0,2.2,1.32)),(1.04,(2.24,2.4,1.50)),(1.50,(2.24,2.4,1.50)),(1.78,(2.52,2.4,1.32)),(2.25,(2.52,2.4,1.32)),(2.38,(2.82,2.4,1.50)),(2.93,(2.82,2.4,1.50)),(3.25,(2.93,2.4,1.41)),(4,(2.93,2.4,1.41))]
HEIGHT=[(0,2.66),(.20,2.63),(.50,2.70),(.85,2.84),(1.20,2.94),(1.55,3.02),(2.,3.06),(2.40,3.06),(2.80,3.08),(3.40,3.10),(4.,3.10)]
# Preview-planned linearized inverted pendulum: C - h/g * C'' = support pressure.
# Continuous COM travel is solved from contacts, rather than stopping over every stance.
TIMES=np.arange(121)/30;PPLAN=np.array([channel(t,PRESSURE) for t in TIMES]);HPLAN=np.array([max(.45,hermite(t,HEIGHT)+.10-PPLAN[j,1]) for j,t in enumerate(TIMES)]);A=np.eye(len(TIMES));B=PPLAN[:,[0,2]].copy()
for j in range(1,len(TIMES)-1):
 k=HPLAN[j]/9.81*30**2;A[j,j]=1+2*k;A[j,j-1]=-k;A[j,j+1]=-k
CPLAN=np.linalg.solve(A,B)
def planned_com(t):return V(np.interp(t,TIMES,CPLAN[:,0]),0,np.interp(t,TIMES,CPLAN[:,1]))
def state(t):
 ff=[]
 for j in range(2):
  start=INIT[j];f={'sole':start,'planted':True,'pitch':0,'heading':math.pi/2}
  for a,b,target,lift in PLANS[j]:
   if t<a:break
   f=step(t,start,target,a,b,lift)
   if t<b:break
   start=target
  for a,b,target,lift in PLANS[j]:
   if a-.12<=t<a:f['pitch']=-.28*Q(t,a-.12,a)
  ff.append(foot_geometry(f))
 # Planned load shifts precede toe-off; single support targets the planted foot.
 pressure=channel(t,PRESSURE);desired=planned_com(t);target=V(desired[0],desired[2]);y=hermite(t,HEIGHT);r=V(target[0]-.04,y,target[1]);pitch=-float(channel(t,[(0,-.08),(.2,-.22),(.68,-.16),(1.05,-.08),(1.3,-.17),(1.65,-.06),(2.05,-.1),(2.4,-.05),(3,0)]));roll=float(channel(t,[(0,0),(.25,.08),(.82,.06),(1.04,-.08),(1.50,-.07),(1.78,.075),(2.25,.05),(2.41,-.07),(3,0)]));twist=float(channel(t,[(0,0),(.75,-.10),(1.45,.07),(2.1,-.06),(3,-.12)]));release=Q(t,1.55,1.95)
 for _ in range(8):
  near=r+V(.15,.17,-.16)+V(.05*Q(t,1.8,2.25),.03,0);rail=V(min(2.34,r[0]+.05),.85+(min(2.34,r[0]+.05)+.5)*(.2/.24),1.94);far=mix(rail+V(0,0,-.065),r+V(-.07,.13,.15),release);p=pose(r,ff,[near,far],pitch=pitch,roll=roll,twist=twist,pelvis_roll=-.7*roll,head_lag=-.035*Q(t,.2,.65)+.035*Q(t,2.2,2.8),look=.85-.35*Q(t,2.3,2.85));c=com(p);err=V(target[0]-c[0],0,target[1]-c[2]);r+=err*.72
 T=V(1,.2/.24,0);T/=np.linalg.norm(T);far=p['arms'][1]['wrist'];railpads=[mix(rail+T*q+V(0,0,-.0225),p['root']+V(-.07,.13,.15)+V(q,.025,.015),release) for q in [-.015,.015]];fg=fingers(far,railpads,V(0,-1,-1),[V(0,0,-1)]*2);handR=np.column_stack([V(-T[1],T[0],0),T,V(0,0,-1)])
 return {'time':t,'fingers':[[],fg],'hand_frames':[None,handR],'pose':p,'com':com(p),'support_target':pressure,'desired_com':desired,'balance_height':float(np.interp(t,TIMES,HPLAN)),'balance_model':'linearized preview / contact pressure','rail_contact':t<=1.55,'rail_target':rail,'phase':'load anticipation' if t<.28 else 'last riser' if t<1.05 else 'upper landing' if t<1.8 else 'hallway steps and recovery','body_driven_by_support':True}
