"""M11 geometry-derived cabin and enclosed-room cameras, Y-up metres."""
from cameras_m10 import camera as baseline
from world import Camera
from contact_rig import V,Q,RY
import numpy as np

def camera(shot,t,d,debug=False):
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:return Camera((.24,1.27,-.98),(-.15,1.10,1.25),780)
 if shot=='STAIRS':
  r=np.array(d['pose']['root'])
  if debug:return Camera((5.5,4.3,2.4),(.8,1.75,3.8),720)
  q=Q(t,11.9,13.);return Camera((2.03-2.83*Q(t,13.,15.),r[1]+.68,max(.22,r[2]-1.65)*(1-q)+6.25*q),r+V(0,.22,.18),1050)
 if shot in ['WINDOW_CURTAIN','PHONE_CALL','UNKNOWN_CALLER']:
  r=np.array(d['pose']['root'])
  if debug:return Camera((-.95,2.3,-4.85),(0,1.,-1.6),650)
  if shot=='WINDOW_CURTAIN' and t<5:return Camera((-.95,1.65,min(-1.05,r[2]+1.8)),r+V(0,.32,0),850)
  if shot=='WINDOW_CURTAIN':
   q=Q(t,10.5,11.2)*(1-Q(t,12.7,13.5));eye=(1-q)*V(-.78,1.65,-.95)+q*V(-.40,1.85,-.42);target=(1-q)*V(.20,1.13,.05)+q*(np.array(d['sedan_position'])+V(0,.85,0));return Camera(eye,target,650+150*q)
  return Camera((-.93,1.58,-1.65),(0,1.18,-.65),1000)
 if shot=='DOOR_ENTRY' and 10.8<=t<13:return Camera((.25,1.50,.38),(-.30,1.16,.105),1050)
 if shot=='ARRIVAL':
  p=np.array(d['position']);return Camera(p+RY(d['yaw'])@V(-4.,2.1,-5.),p+V(0,.65,0),1000)
 return baseline(shot,t,d,debug)
