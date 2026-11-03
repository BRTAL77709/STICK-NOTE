"""Single SI-unit truth for road, vehicle, camera, instruments and sound."""
import math,bisect
DURATION=15.;FPS=30
CUTS=[(0,2.4,'Ash Avenue tracking'),(2.4,4.2,'Witness reaction'),(4.2,5.1,'Pedal contact'),(5.1,6.5,'Instrument acceleration'),(6.5,7.4,'Driver under acceleration'),(7.4,9.6,'Low pursuit / Mercer bend'),(9.6,11.3,'Instrument under load'),(11.3,12.3,'Over shoulder'),(12.3,13.4,'Instrument culmination'),(13.4,15.,'Mirror / driver')]
def clamp(x,a=0.,b=1.):return max(a,min(b,x))
def ease(t,a,b):
 u=clamp((t-a)/(b-a));return u*u*(3-2*u)
def speed(t):return (20+80*ease(t,4.2,12.8))/3.6
def acceleration(t):
 u=clamp((t-4.2)/8.6);return (80/3.6)*6*u*(1-u)/8.6 if 4.2<t<12.8 else 0.
def travel(t):
 u=clamp((t-4.2)/8.6);return 20/3.6*t+80/3.6*(8.6*(u**3-.5*u**4)+max(0,t-12.8))
def road_x(z):return 8*math.sin(z/95)-5*math.sin(z/42)
def road_slope(z):return 8/95*math.cos(z/95)-5/42*math.cos(z/42)
def road_curvature(z):return (-8/95**2*math.sin(z/95)+5/42**2*math.sin(z/42))/(1+road_slope(z)**2)**1.5
# Arc-length lookup keeps road speed, tire travel and instruments in physical agreement.
_Z=[-120+i*.1 for i in range(9201)];_S=[0.]
for _a,_b in zip(_Z,_Z[1:]):_S.append(_S[-1]+.1*math.sqrt(1+road_slope((_a+_b)/2)**2))
_zero=_S[1200];_S=[s-_zero for s in _S]
def route_z(distance):
 j=max(1,min(len(_S)-1,bisect.bisect_left(_S,distance)));u=(distance-_S[j-1])/(_S[j]-_S[j-1]);return _Z[j-1]+u*.1

def throttle(t):return .18+.78*ease(t,4.2,5.1)
def rpm(t):
 v=speed(t)*3.6;ratio=65 if v<48 else 46 if v<78 else 34
 # Smooth gear transitions, never a random instrument value.
 ratio=65-19*ease(v,46,50)-12*ease(v,76,80)
 return 950+v*ratio

def state(t,black=False):
 gap=28-14*ease(t,5,11) if black else 0
 s=route_z(travel(t)-gap);u=clamp((t-5)/6)
 catchup=14*u*(1-u) if black and 5<t<11 else 0
 catch_acc=14/6*(1-2*u) if black and 5<t<11 else 0
 odometer=travel(t)+28-gap if black else travel(t)
 x=road_x(s)+(-1.55 if black else 1.55);yaw=math.atan(road_slope(s));v=speed(t)+catchup;cur=road_curvature(s)
 return {'t':t,'x':x,'z':s,'yaw':yaw,'speed_mps':v,'speed_kmh':v*3.6,'distance_m':odometer,'wheel_rad':odometer/.32,'steer_rad':math.atan(2.7*cur),'pitch':-.015*(acceleration(t)+catch_acc),'roll':clamp(cur*v*v*.018,-.08,.08),'rpm':rpm(t),'throttle':throttle(t)}
def shot(t):return next((n,a,b,s) for n,(a,b,s) in enumerate(CUTS) if a<=t<b)
