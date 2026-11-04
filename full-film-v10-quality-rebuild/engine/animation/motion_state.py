"""V4 shared SI state: speed, spatial path, steering, wheels, suspension and RPM."""
import math,bisect
DURATION=86.;FPS=30
CUTS=[(0,2,'Departure'),(2,3.35,'Driver danger'),(3.35,4.45,'Pedal'),(4.45,6.3,'Acceleration POV'),(6.3,9,'Street acceleration'),(9,11.7,'Mirror threat'),(11.7,13.25,'Steering anticipation'),(13.25,15,'Corner escape')]
def clamp(x,a=0.,b=1.):return max(a,min(b,x))
def ease(t,a,b):
 u=clamp((t-a)/(b-a));return u*u*(3-2*u)
def derivative(t,a,b):
 u=(t-a)/(b-a);return 6*u*(1-u)/(b-a) if 0<u<1 else 0.
def integral(t,a,b):
 u=clamp((t-a)/(b-a));return (b-a)*(u**3-.5*u**4)+max(0,t-b)
def speed(t):return max(0,(22-22*ease(t,8,11.5)+96*ease(t,28.6,38)-72*ease(t,41,46)-24*ease(t,46,48))/3.6)
def acceleration(t):return (-22*derivative(t,8,11.5)+96*derivative(t,28.6,38)-72*derivative(t,41,46)-24*derivative(t,46,48))/3.6
def travel(t):return (22*t-22*integral(t,8,11.5)+96*integral(t,28.6,38)-72*integral(t,41,46)-24*integral(t,46,48))/3.6
CORNER_S=travel(38.5);STEP=.05
# Arc-length centerline: straightAsh, smooth10m curvature entry, then70m-radius left turn.
_CENTER=[];x=0.;z=-120.;heading=0.
for j in range(14401):
 s=-120+j*STEP;u=clamp((s-CORNER_S)/10);cur=-u*u*(3-2*u)/65 if heading>-.82 else 0
 if j:
  heading+=cur*STEP;x+=math.sin(heading)*STEP;z+=math.cos(heading)*STEP
 _CENTER.append((s,x,z,heading,cur))
_Z=[p[2] for p in _CENTER]
def sample_table(table,keys,q):
 j=max(1,min(len(keys)-1,bisect.bisect_left(keys,q)));u=(q-keys[j-1])/(keys[j]-keys[j-1]);return tuple(table[j-1][k]+u*(table[j][k]-table[j-1][k]) for k in range(len(table[0])))
def road_sample(z):return sample_table(_CENTER,_Z,z)
def road_x(z):return road_sample(z)[1]
def road_slope(z):return math.tan(road_sample(z)[3])
def road_curvature(z):return road_sample(z)[4]
_LANES={}
for lane in [1.55,1.15]:
 table=[];arc=-120.;last=None
 for s,x,z,hd,cur in _CENTER:
  xx=x+lane*math.cos(hd);zz=z-lane*math.sin(hd)
  if last:arc+=math.hypot(xx-last[0],zz-last[1])
  table.append((arc,xx,zz,hd,cur));last=(xx,zz)
 _LANES[lane]=(table,[r[0] for r in table])
def gap(t):return max(6,travel(t)-travel(max(0,t-1.35))+16-6*ease(t,51,60))
def throttle(t):return .20+.72*ease(t,28.6,30)-.72*ease(t,41,43)
def rpm_for(v,load):
 ratio=68-22*ease(v,42,46)-12*ease(v,68,73)
 return 950+v*ratio+250*load
def rpm(t):return rpm_for(speed(t)*3.6,throttle(t))
# Pursuer: physical alley merge, closing chase, turn behind frontage, return/park.
def black_arc(t):
 a=travel(12)-4;b=travel(40)-8;T=8.5;v=speed(40)
 if t<=31.5:return a
 if t<40:
  u=(t-31.5)/T;return a*(2*u**3-3*u**2+1)+b*(-2*u**3+3*u**2)+v*T*(u**3-u**2)
 return travel(t)-8-20*ease(t,42,46)+20*ease(t,55,61)
def black_lateral(t):return -10*(1-ease(t,31.5,33))-8*ease(t,42,45)*(1-ease(t,55,59))
def _black_position(t):
 table,keys=_LANES[1.15];_,x,z,hd,cur=sample_table(table,keys,black_arc(t));off=black_lateral(t)
 return x+off*math.cos(hd),z-off*math.sin(hd)
_BT=1/200;_BPOS=[_black_position(j*_BT) for j in range(17201)];_BVEL=[];_BHEAD=[];odo=0.;_BODO=[]
for j,p in enumerate(_BPOS):
 lo=max(0,j-1);hi=min(len(_BPOS)-1,j+1);dt=(hi-lo)*_BT;vx=(_BPOS[hi][0]-_BPOS[lo][0])/dt;vz=(_BPOS[hi][1]-_BPOS[lo][1])/dt;v=math.hypot(vx,vz)
 hd=math.atan2(vx,vz) if v>1e-6 else (_BHEAD[-1] if _BHEAD else math.pi/2)
 if j:odo+=math.dist(p,_BPOS[j-1])
 _BVEL.append((vx,vz,v));_BHEAD.append(hd);_BODO.append(odo)
_BLACK=[]
for j,p in enumerate(_BPOS):
 lo=max(0,j-1);hi=min(len(_BPOS)-1,j+1);dt=(hi-lo)*_BT;acc=(_BVEL[hi][2]-_BVEL[lo][2])/dt;cur=clamp((_BHEAD[hi]-_BHEAD[lo])/dt/max(.1,_BVEL[j][2]),-.2,.2)
 _BLACK.append((j*_BT,p[0],p[1],_BHEAD[j],*_BVEL[j],acc,_BODO[j],cur))
_BKEY=[r[0] for r in _BLACK]
def black_state(t):
 _,x,z,hd,vx,vz,v,acc,dist,cur=sample_table(_BLACK,_BKEY,clamp(t,0,86));rack=clamp(math.atan(2.7*cur),-.48,.48);bump=.012*math.sin(dist*2.2)+.006*math.sin(dist*4.7)
 return {'t':t,'x':x,'z':z,'yaw':hd,'heading':hd,'speed_mps':v,'speed_kmh':v*3.6,'velocity_x':vx,'velocity_z':vz,'acceleration_mps2':acc,'distance_m':dist,'wheel_rad':dist/.32,'steer_rad':rack,'steering_wheel_rad':rack*16,'pitch':clamp(.018*acc,-.075,.075),'roll':clamp(cur*v*v*.02,-.11,.11),'suspension_m':bump,'rpm':rpm_for(v*3.6,throttle(t)),'throttle':throttle(t)}
def pursuer_visible(t):return t>=32 and abs(black_lateral(t))<6
def state(t,black=False):
 if black:return black_state(t)
 lag=gap(t) if black else 0;lane=1.15 if black else 1.55;table,keys=_LANES[lane];s=travel(t)-lag;_,x,z,hd,cur=sample_table(table,keys,s)
 v=speed(max(0,t-1.35))+6*derivative(t,51,60) if black else speed(t);odometer=travel(t)-lag+16 if black else travel(t);acc=acceleration(max(0,t-1.35)) if black else acceleration(t)
 # Smoothed rack anticipates physical entry; lateral body load follows actual road curvature.
 cur=cur/(1-lane*cur);rack=math.atan(2.7*cur)
 bump=.012*math.sin(odometer*2.2)+.006*math.sin(odometer*4.7)
 return {'t':t,'x':x,'z':z,'yaw':hd,'heading':hd,'speed_mps':v,'speed_kmh':v*3.6,'velocity_x':v*math.sin(hd),'velocity_z':v*math.cos(hd),'acceleration_mps2':acc,'distance_m':odometer,'wheel_rad':odometer/.32,'steer_rad':rack,'steering_wheel_rad':rack*16,'pitch':clamp(.018*acc,-.075,.075),'roll':clamp(cur*v*v*.02,-.11,.11),'suspension_m':bump,'rpm':rpm_for(v*3.6,throttle(t)),'throttle':throttle(t)}
def route_z(s):
 table,keys=_LANES[1.55];return sample_table(table,keys,s)[2]
def pursuit_distance(t):
 a=state(t);b=state(t,True);return math.hypot(a['x']-b['x'],a['z']-b['z'])
def shot(t):return next((j,a,b,n) for j,(a,b,n) in enumerate(CUTS) if a<=t<b)

# Public deterministic motion-engine contract.
def vehicleState(t):
 return {**state(t),"pursuit_distance_m":pursuit_distance(t)}
