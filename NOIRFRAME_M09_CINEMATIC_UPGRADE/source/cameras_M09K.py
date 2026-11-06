from cameras_base_R07 import camera as base_camera
from world import Camera

def inherited_camera(shot,t,d,debug=False):
 if shot=='KEY_LOCK' and t>=2 and not debug:return Camera((-.12,1.50,-.38),(-.30,1.16,-.071),1050)
 if shot=='DRIVING_COCKPIT' and not debug:
  if t<3.0:return Camera((.78,1.20,-.04),(-.33,.90,.30),720)
  if t<5.1:return Camera((.18,1.30,-.12),(0,1.26,.28),1180)
  if t<8.0:return Camera((.54,1.04,.26),(-.38,.83,.48),720)
  if t<9.6:return Camera((.32,.59,-.16),(-.31,.17,.40),760)
  return Camera((.72,1.24,-.02),(-.34,1.03,.08),850)
 if shot=='WINDOW_CURTAIN':
  if not debug and 1<=t<9.5:return Camera((.95,1.60,-.85),(.05,1.15,-.05),650)
  if t<1 and not debug:return Camera((-1.25,1.7,-.45),(.20,.95,-1.55),1100)
  return base_camera(shot,max(0,t-1),d,debug)
 if shot=='DOOR_ENTRY' and t>=10.8 and not debug:
  return Camera((-.25,1.50,.30),(-.30,1.16,.105),1050)
 return base_camera(shot,t,d,debug)

from contact_rig import V,Q,RY
import numpy as np
def camera(shot,t,d,debug=False):
 if debug:return inherited_camera(shot,t,d,True)
 if shot=='KEY_LOCK':
  if t<1.85:return Camera((-.85,1.58,-2.5),(-.16,.98,-.23),1350)
  return Camera((-.70,1.46,-.42),(-.30,1.16,-.15),1000+50*Q(t,1.85,8.0))
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:
  if t<3.15:return Camera((.65,1.23,.17),(-.34,1.0,.19),760)
  if t<4.35:return Camera((.12,1.31,-.13),(0,1.265,.28),1150)
  if t<7.8:return Camera((.58,1.12,.31),(-.36,.93,.39),745)
  if t<9.2:return Camera((.30,.57,-.12),(-.30,.18,.40),780)
  return Camera((.61,1.24,.22),(-.34,1.04,.09),820+40*Q(t,9.2,11.8))
 if shot=='WINDOW_CURTAIN':
  if t<1:return inherited_camera(shot,t,d,False)
  if t<3.2:return Camera((1.65,2.05,-2.85),(.10,.95,-.75),1100)
  if t<8.2:return Camera((.92,1.62,-.93+ .14*Q(t,3.8,7.5)),(.04,1.14,-.04),700)
  if t<9.5:return Camera((.78,1.56,-.88),(.10,1.19,-.18),900)
  return inherited_camera(shot,t,d,False)
 if shot=='CAR_EXIT_RUNNING':
  r=np.array(d['pose']['root']);target=r+V(0,.42,0)
  if t<2.05:return Camera((-3.8,2.05,-5.3),(-.65,.80,0),1200)
  return Camera((max(-5.25,r[0]-2.8),target[1]+.74,target[2]-3.9),target,1550)
 if shot=='ROAD_BUILDINGS':
  p=d['position'];M=RY(d['yaw']);return Camera(p+M@V(3.8,2.25,-6.5),p+M@V(0,.8,4.6),1050)
 return inherited_camera(shot,t,d,False)
