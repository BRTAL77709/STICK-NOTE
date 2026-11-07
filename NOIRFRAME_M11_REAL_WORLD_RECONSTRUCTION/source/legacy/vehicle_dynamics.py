"""Steering-input-driven rear-axle bicycle integration; city is built once from the route."""
from contact_rig import *
WB=2.60;RADIUS=.30;DT=1/120

def controls(t):return .62*(1-Q(t,3.9,4.20)),.68*Q(t,5.1,5.55)
def steering(t):return .105*(Q(t,.45,1.20)-Q(t,2.15,2.85))-.095*(Q(t,3.2,3.85)-Q(t,5.05,5.85))
def advance(rear,yaw,speed,delta,acc,dt):
 v1=max(0,speed+acc*dt);vm=(speed+v1)/2;dy=vm/WB*math.tan(delta)*dt;return rear+V(math.sin(yaw+dy/2),0,math.cos(yaw+dy/2))*vm*dt,yaw+dy,v1,vm*dt

def simulate():
 rear=V(0,0,-1.32);yaw=0.;v=5.5;dist=0.;roll=pitch=rv=pv=0.;run=[];phase=np.zeros(4);prev=None
 for n in range(721):
  t=n*DT;th,br=controls(t);acc=1.6*th-3.2*br-.12;delta=steering(t);o=rear+RY(yaw)@V(0,0,1.32);coords=[rear+RY(yaw)@V(x,0,z+1.32) for x in [-.90,.90] for z in [-1.32,1.28]]
  if prev is not None:phase+=np.array([np.linalg.norm(a-b) for a,b in zip(coords,prev)])/RADIUS
  prev=coords
  if n%4==0:run.append({'time':t,'position':o.copy(),'rear_axle':rear.copy(),'yaw':yaw,'speed':v,'acceleration':acc,'steer':delta,'wheel_phase':phase.copy(),'distance':dist,'throttle':th,'brake':br,'roll':roll,'pitch':pitch})
  yawrate=v/WB*math.tan(delta);rv+=(144*(.020*v*yawrate-roll)-18.7*rv)*DT;roll+=rv*DT;pv+=(100*(-.014*acc-pitch)-16*pv)*DT;pitch+=pv*DT
  rear,yaw,v,ds=advance(rear,yaw,v,delta,acc,DT);dist+=ds
 # Fixed road is the reference trajectory of the input-driven witness; no road frame animation.
 return run
RUN=simulate();ROAD=np.array([[d['position'][0],d['position'][2],d['yaw']] for d in RUN]);ROAD=np.vstack([[-0.,-25.,0.],ROAD,[ROAD[-1,0]+math.sin(ROAD[-1,2])*35,ROAD[-1,1]+math.cos(ROAD[-1,2])*35,ROAD[-1,2]]])
def road_x(z):return float(np.interp(z,ROAD[:,1],ROAD[:,0]))
def road_yaw(z):return float(np.interp(z,ROAD[:,1],ROAD[:,2]))
# Pursuer steers toward a lookahead point on that fixed road; its own integration remains causal.
brear=V(0,0,-13.32);byaw=0.;bv=6.7;phase=np.zeros(4);prev=None
for n in range(721):
 t=n*DT;i=min(180,round(t*30));lead=RUN[i];lookz=brear[2]+8.;target=V(road_x(lookz),0,lookz);relative=RY(-byaw)@(target-brear);delta=clamp(math.atan2(2*WB*relative[0],float(relative@relative)),-.20,.20);gap=float(np.linalg.norm(lead['position']-(brear+RY(byaw)@V(0,0,1.32))));acc=clamp((lead['speed']+1.15-bv)*1.4,-2.,1.) if gap>7.2 else clamp((lead['speed']-.3-bv)*2,-3.,.4);coords=[brear+RY(byaw)@V(x,0,z+1.32) for x in [-.90,.90] for z in [-1.32,1.28]]
 if prev is not None:phase+=np.array([np.linalg.norm(a-b) for a,b in zip(coords,prev)])/RADIUS
 prev=coords
 if n%4==0:lead.update(pursuer_position=brear+RY(byaw)@V(0,0,1.32),pursuer_yaw=byaw,pursuer_speed=bv,pursuer_steer=delta,pursuer_wheel_phase=phase.copy(),pursuer_roll=.02*bv*bv/WB*math.tan(delta),pursuer_pitch=-.014*acc,gap=gap)
 brear,byaw,bv,_=advance(brear,byaw,bv,delta,acc,DT)
