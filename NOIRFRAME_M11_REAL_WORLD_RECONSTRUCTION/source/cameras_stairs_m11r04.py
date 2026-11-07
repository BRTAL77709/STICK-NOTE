"""Landing framing correction only; preserves R03 native motion and fixed diagnostic camera."""
from cameras import camera as previous
from world import Camera
from contact_rig import Q,V
import numpy as np
def camera(shot,t,d,debug=False):
 if shot!='STAIRS' or debug:return previous(shot,t,d,debug)
 r=np.array(d['pose']['root']);q=Q(t,11.9,13.)
 return Camera((2.03-.08*q,r[1]+.68,max(.22,r[2]-1.65)*(1-q)+6.25*q),r+V(0,.22,.18),1050-200*Q(t,11.0,13.))
