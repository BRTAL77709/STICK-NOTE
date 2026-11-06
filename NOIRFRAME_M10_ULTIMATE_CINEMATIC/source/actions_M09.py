"""M09 shot-level controls. Existing native IK remains the actual geometry solver."""
import actions_M08 as B, actions_M08J as E, actions_M08F as C
from contact_rig import *
DURATIONS=dict(B.DURATIONS)
def pulse(t,a,b,c,d):return Q(t,a,b)*(1-Q(t,c,d))
def state(shot,t):
 d=(E.state(shot,t) if shot=='CAR_EXIT_RUNNING' else C.state(shot,t) if shot=='WINDOW_CURTAIN' else B.state(shot,t))
 if shot in ['ROAD_BUILDINGS','CAR_CHASE']:return d
 p=d['pose'];r=p['root'].copy();heading=math.atan2(p['pelvis_basis'][0,2],p['pelvis_basis'][2,2]);ff=[{k:v for k,v in f.items() if k not in ['hip','knee']} for f in p['legs']];hands=[a['wrist'].copy() for a in p['arms']]
 # Event-shaped acting, not repeating sinusoids. Contact hands and ankles stay fixed.
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:
  attention=pulse(t,1.75,2.35,3.1,3.65);danger=Q(t,3.1,4.2);brake=pulse(t,6.2,6.65,7.25,8.05)
  pitch=.045+.065*brake-.025*Q(t,.4,1.4);roll=-.09*d['steer'];twist=-.075*attention
  pp=pose(r,ff,hands,heading=0,pitch=pitch,roll=roll,twist=twist,look=.65-attention,fear=.28+.58*danger,knee_forward=V(0,.5,1))
  mirror=V(0,1.265,.28)-pp['head'];mirror/=np.linalg.norm(mirror);pp['head_forward']=mix(V(0,0,1),mirror,attention)
 elif shot=='KEY_LOCK':
  align=pulse(t,2.1,3.1,5.8,6.6);pp=pose(r,ff,hands,heading=heading,pitch=.025+.065*align,twist=-.025*align,look=.4,fear=.72,knee_forward=RY(heading)@V(0,.1,1));pp['head_forward']=V(0,-.16,1)
 elif shot=='DOOR_ENTRY':
  glance=pulse(t,5.7,6.45,7.1,7.8);settle=pulse(t,9.6,10.3,11.0,12.0);pp=pose(r,ff,hands,heading=heading,pitch=.025+.035*settle,twist=.055*glance,look=.6,fear=.65+.25*glance,knee_forward=RY(heading)@V(0,.1,1));pp['head_forward']=RY(math.pi*glance)@V(0,0,1)
 elif shot=='CAR_EXIT_RUNNING':
  # Keep continuously solved root and individual world foot contacts; more purposeful body lean.
  active=pulse(t,5.65,6.35,9.0,10.25);pp=pose(r,ff,hands,heading=heading,pitch=.08*active,roll=.025*pulse(t,6.25,6.45,6.7,6.9)-.025*pulse(t,6.9,7.1,7.4,7.6),look=.7,fear=.82,knee_forward=RY(heading)@V(0,.3,1));pp['head_forward']=p.get('head_forward',RY(heading)@V(0,0,1))
 else:
  # Native gripping and fabric arc-length targets are preserved exactly.
  pp=p
 d['pose']=pp
 return d
# Compatibility for sets and vehicle/camera composition.
RX=B.RX;RY=B.RY;RZ=B.RZ;Q=B.Q
def driving(t):return state('DRIVING_COCKPIT',t)
