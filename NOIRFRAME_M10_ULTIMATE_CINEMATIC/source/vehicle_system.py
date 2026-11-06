"""One authoritative 120Hz integrated state; separate witness/pursuer brake channels."""
from bootstrap import ROOT
from contact_rig import *
from vehicle_dynamics import advance,WB,RADIUS,road_x,road_yaw
DT=1/120;DURATION=11.;TABLE=[];roadref=road_x
rear=V(0,0,-1.32);yaw=0.;speed=5.5;dist=0.;wheel=np.zeros(4);prev=None;black=V(0,0,-15.32);byaw=0.;bv=7.;bw=np.zeros(4);bprev=None;roll=pitch=rv=pv=0.
for n in range(round(DURATION/DT)+1):
 t=n*DT;th=0.5634674835205079+.20*Q(t,2.8,3.6)-0.763467483520508*Q(t,4.7,5.5);br=.95*Q(t,6.2,7.0);acc=1.6*th-3.8*br-.12 if speed>0 or th else 0
 # Steering toward fixed reference geometry; route is never rebuilt per frame.
 def steering_at(p,h,v):
  target=V(roadref(p[2]+max(6.,v*.8)),0,p[2]+max(6.,v*.8));local=RY(-h)@(target-p);return clamp(math.atan2(2*WB*local[0],float(local@local)),-.22,.22)
 delta=steering_at(rear,yaw,speed);pos=rear+RY(yaw)@V(0,0,1.32);bp=black+RY(byaw)@V(0,0,1.32);gap=float(np.linalg.norm(pos-bp));desired=max(0,speed+clamp((gap-7.6)*.70,-2,1));desired=min(desired,math.sqrt(speed*speed+2*4.5*max(0,gap-5.5)));ba=clamp((desired-bv)*2.2,-5.5,1.4);bb=clamp(-ba/4,0,1);bd=steering_at(black,byaw,bv)
 def phases(p,h,prev,phase):
  coords=[p+RY(h)@V(x,0,z+1.32) for x in [-.90,.90] for z in [-1.32,1.28]]
  if prev is not None:phase+=np.array([np.linalg.norm(a-b) for a,b in zip(coords,prev)])/RADIUS
  return coords
 prev=phases(rear,yaw,prev,wheel);bprev=phases(black,byaw,bprev,bw)
 TABLE.append({'time':t,'position':pos.copy(),'rear_axle':rear.copy(),'yaw':yaw,'speed':speed,'acceleration':acc,'steer':delta,'wheel_phase':wheel.copy(),'distance':dist,'throttle':th,'brake':br,'roll':roll,'pitch':pitch,'pursuer_position':bp.copy(),'pursuer_yaw':byaw,'pursuer_speed':bv,'pursuer_steer':bd,'pursuer_wheel_phase':bw.copy(),'pursuer_brake':bb,'pursuer_acceleration':ba,'pursuer_roll':.02*bv*bv/WB*math.tan(bd),'pursuer_pitch':-.014*ba,'gap':gap})
 yawrate=speed/WB*math.tan(delta);rv+=(144*(.020*speed*yawrate-roll)-18.7*rv)*DT;roll+=rv*DT;pv+=(100*(-.014*acc-pitch)-16*pv)*DT;pitch+=pv*DT
 rear,yaw,speed,ds=advance(rear,yaw,speed,delta,acc,DT);dist+=ds;black,byaw,bv,_=advance(black,byaw,bv,bd,ba,DT)
def state(t):return dict(TABLE[min(len(TABLE)-1,max(0,round(t*120)))])
PARK=state(11);CAR_R=RY(PARK['yaw']);HOUSE_R=np.array([[-0.15603017311135373, 0.0, -0.987752289331106], [0.0, 1.0, 0.0], [0.987752289331106, 0.0, -0.15603017311135373]]);HOUSE_ORIGIN=np.array([-0.9516927453098694, 0.13, 64.60566473433754]);WINDOW_ORIGIN=HOUSE_ORIGIN+HOUSE_R@V(-.8,2.60,0);WINDOW_R=HOUSE_R@RY(math.pi)
def window_point(world):return WINDOW_R.T@(np.array(world)-WINDOW_ORIGIN)
