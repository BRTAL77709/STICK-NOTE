"""Continuous view-relative cap/face construction, using the approved drawing proportions."""
from head_25d import head
from contact_rig import *
def draw_head(a,t,p,cam):
 f=p.get('head_forward',p['torso_basis']@V(0,0,1));to=cam.eye-p['head'];to/=np.linalg.norm(to);side=float(f@cam.right);front=float(f@to);rear=Q(front,-.10,-.70);yaw=clamp(side,-1,1)
 head(a,0,0,t,yaw,yaw,p['fear'],p['tilt'],blink_override=0,rear=rear)
