from cameras_base_R07 import camera as base_camera
from world import Camera

def camera(shot,t,d,debug=False):
 if shot=='KEY_LOCK' and t>=2 and not debug:return Camera((-.12,1.50,-.38),(-.30,1.16,-.071),1050)
 if shot=='DRIVING_COCKPIT' and not debug:
  if t<3.0:return Camera((.78,1.20,-.04),(-.33,.90,.30),720)
  if t<5.1:return Camera((.18,1.30,-.12),(0,1.26,.28),1180)
  if t<8.0:return Camera((.54,1.04,.26),(-.38,.83,.48),720)
  if t<9.6:return Camera((.32,.59,-.16),(-.31,.17,.40),760)
  return Camera((.72,1.24,-.02),(-.34,1.03,.08),850)
 if shot=='WINDOW_CURTAIN':
  if not debug and 1<=t<9.5:return Camera((-1.65,1.55,-1.85),(-.04,1.1,-.14),1150)
  if t<1 and not debug:return Camera((-1.25,1.7,-.45),(.20,.95,-1.55),1100)
  return base_camera(shot,max(0,t-1),d,debug)
 if shot=='DOOR_ENTRY' and t>=10.8 and not debug:
  return Camera((-.25,1.50,.30),(-.30,1.16,.105),1050)
 return base_camera(shot,t,d,debug)
