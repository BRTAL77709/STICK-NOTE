"""V4 shared SI state: speed, spatial path, steering, wheels, suspension and RPM."""
import math,bisect
DURATION=15.;FPS=30
CUTS=[(0,2,'Departure'),(2,3.35,'Driver danger'),(3.35,4.45,'Pedal'),(4.45,6.3,'Acceleration POV'),(6.3,9,'Street acceleration'),(9,11.7,'Mirror threat'),(11.7,13.25,'Steering anticipation'),(13.25,15,'Corner escape')]
def clamp(x,a=0.,b=1.):return max(a,min(b,x))
def ease(t,a,b):
 u=clamp((t-a)/(b-a));return u*u*(3-2*u)
def derivative(t,a,b):
 u=(t-a)/(b-a);return 6*u*(1-u)/(b-a) if 0<u<1 else 0.
def integral(t,a,b):
 u=clamp((t-a)/(b-a));return (b-a)*(u**3-.5*u**4)+max(0,t-b)
def speed(t):return (18+12*ease(t,0,2)+66*ease(t,3.35,9)-32*ease(t,11.85,14.7))/3.6
def acceleration(t):return (12*derivative(t,0,2)+66*derivative(t,3.35,9)-32*derivative(t,11.85,14.7))/3.6
def travel(t):return (18*t+12*integral(t,0,2)+66*integral(t,3.35,9)-32*integral(t,11.85,14.7))/3.6
CORNER_S=travel(11.65);STEP=.05
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
def gap(t):return 31-22*ease(t,2,13)
def throttle(t):return .28+.64*ease(t,3.35,4.35)-.60*ease(t,11.85,13)
def rpm_for(v,load):
 ratio=68-22*ease(v,42,46)-12*ease(v,68,73)
 return 950+v*ratio+250*load
def rpm(t):return rpm_for(speed(t)*3.6,throttle(t))
def state(t,black=False):
 lag=gap(t) if black else 0;lane=1.15 if black else 1.55;table,keys=_LANES[lane];s=travel(t)-lag;_,x,z,hd,cur=sample_table(table,keys,s)
 closing=22*derivative(t,2,13) if black else 0;v=speed(t)+closing;odometer=travel(t)+31-lag if black else travel(t);acc=acceleration(t)+(22*6*(1-2*(t-2)/11)/121 if black and 2<t<13 else 0)
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
