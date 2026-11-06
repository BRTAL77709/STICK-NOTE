from cameras_base_R07 import camera as base_camera
from world import Camera

def camera(shot,t,d,debug=False):
 if shot=='KEY_LOCK' and t>=2 and not debug:return Camera((-.12,1.50,-.38),(-.30,1.16,-.071),1050)
 if shot=='DRIVING_COCKPIT' and 2<=t<4 and not debug:return Camera((.10,1.38,-.50),(-.24,.96,.70),800)
 if shot=='WINDOW_CURTAIN':
  if t<1 and not debug:return Camera((-1.25,1.7,-.45),(.20,.95,-1.55),1100)
  return base_camera(shot,max(0,t-1),d,debug)
 if shot=='DOOR_ENTRY' and t>=10.8 and not debug:
  return Camera((-.25,1.50,.30),(-.30,1.16,.105),1050)
 return base_camera(shot,t,d,debug)
