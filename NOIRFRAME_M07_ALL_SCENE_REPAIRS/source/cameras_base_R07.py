from bootstrap import ROOT
from world import Camera
from contact_rig import *
import vehicle_system as VS

def camera(shot,t,d,debug=False):
 if shot=='KEY_LOCK':return Camera((-.95,1.55,-2.6),(-.13,.95,-.2),1250) if t<2 else Camera((-1.05,1.45,-1.05),(-.30,1.16,-.09),1350)
 if shot=='DOOR_ENTRY':
  if debug:return Camera((-1.7,1.6,-3.5),(-.04,1.0,.35),1600)
  if t>=10.8:return Camera((-.85,1.90,.85),(-.30,1.16,.105),1250)
  return Camera((-.9,1.5,-2.8),(-.10,1.02,.20),1700) if t<3.9 else Camera((1.6,1.45,2.65),(.12,1.0,.28),1650)
 if shot=='WINDOW_CURTAIN':
  if t>=8.5 and not debug:return Camera((0,1.45,-.40),np.array(d['sedan_position'])+V(0,.8,0),1000)
  return Camera((-2.8,1.85,-2.25),(0,1.15,.20),1000)
 if shot=='CAR_EXIT_RUNNING':
  r=np.array(d['pose']['root']);target=r+V(0,.38,0)
  if debug:return Camera((-3.4,2.4,-4.4),(-2.7,.8,.0),1250)
  if t<2.05:return Camera((-3.4,2.5,-5.8),(-.65,.85,0),1150)
  return Camera((-3.4,target[1]+1.1,target[2]-3.7),target,1650)
 if shot=='DRIVER_CHASE':
  return Camera((.30,1.28,-.08),(0,1.27,.28),1250) if t<5.2 else Camera((.64,1.22,-.10),(-.35,.98,.20),750)
 if shot=='DRIVING_COCKPIT':
  angles=[((.70,1.30,-.15),(-.38,.9,.35),800),((-.40,1.22,-.48),(-.30,.87,.65),800),((.30,1.28,-.08),(0,1.27,.28),1450),((.64,1.12,.45),(-.35,.92,.20),650),((.35,.65,-.23),(-.31,.19,.40),900),((.40,1.30,-.18),(-.35,.92,.5),800)];i=0 if debug else min(5,int(t/2));a,b,f=angles[i];return Camera(a,b,f)
 p=d['position'];R=RY(d['yaw']);mid=(p+d['pursuer_position'])/2
 if shot=='ROAD_BUILDINGS':return Camera(p+R@V(4.2,2.7,-7.),p+R@V(0,1.,5.),1000)
 if debug:return Camera(mid+V(3.5,10,13),mid+V(0,.3,0),1050)
 if t<2.2:return Camera(mid+V(3.5,8.0,-17),mid+V(0,.5,2.),750)
 if t<4.4:return Camera(p+R@V(-2.8,.65,-5.),p+V(0,.65,-3),950)
 if t<6.3:return Camera(mid+V(4.5,4.,14),mid+V(0,.6,0),750)
 if t<8.6:return Camera(p+R@V(3.8,1.6,4.),p+V(0,.65,0),1150)
 return Camera(p+R@V(-6.5,3.,6),p+R@V(-2.,.6,0),1050)
