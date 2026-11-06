"""M09 shot-level controls. Existing native IK remains the actual geometry solver."""
import actions_M08 as B, actions_M08J as EXIT_BASE, actions_M08F as CURTAIN_BASE
from contact_rig import *
DURATIONS=dict(B.DURATIONS)
DURATIONS['KEY_LOCK']=9.
from scipy.interpolate import PchipInterpolator
KEY_CLOCK=PchipInterpolator([0,1.5,2.9,4.,4.35,5.35,6.,7.4,9.],[0,1.2,1.95,2.55,2.75,3.15,3.43,3.92,4.4])
def pulse(t,a,b,c,d):return Q(t,a,b)*(1-Q(t,c,d))
def state(shot,t):
 source_t=float(KEY_CLOCK(t))*7/4.4 if shot=='KEY_LOCK' else t
 d=(EXIT_BASE.state(shot,t) if shot=='CAR_EXIT_RUNNING' else CURTAIN_BASE.state(shot,t) if shot=='WINDOW_CURTAIN' else B.state(shot,source_t))
 d['time']=t
 if shot in ['ROAD_BUILDINGS','CAR_CHASE']:return d
 if shot=='KEY_LOCK':
  K=d['key_R'];tip=d['keytip'].copy();bow=tip-K@V(0,0,.10);old=d['keybow'];oldwr=d['pose']['arms'][1]['wrist'];wr=bow+K@V(-.025,-.018,-.035);d['keybow']=bow
  if d['key_visible']:
   d['pose']['arms'][1]['wrist']=wr;d['grip']=wr;points=[bow+K@V(.025*math.cos(q),.018*math.sin(q),-.004) for q in [math.radians(145),math.radians(-70)]];d['fingers'][1]=fingers(wr,points,K@V(-1,0,-1),[K@V(0,0,-1)]*2)
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
  active=pulse(t,5.65,6.35,9.0,10.25);pp=pose(r,ff,hands,heading=heading,pelvis_roll=math.atan2(p['pelvis_basis'][1,0],p['pelvis_basis'][1,1]),pitch=.08*active,roll=.025*pulse(t,6.25,6.45,6.7,6.9)-.025*pulse(t,6.9,7.1,7.4,7.6),look=.7,fear=.82,knee_forward=RY(heading)@V(0,.3,1));pp['head_forward']=p.get('head_forward',RY(heading)@V(0,0,1))
 else:
  # Native gripping and fabric arc-length targets are preserved exactly.
  pp=p
 d['pose']=pp
 return d
# Compatibility for sets and vehicle/camera composition.
RX=B.RX;RY=B.RY;RZ=B.RZ;Q=B.Q
def driving(t):return state('DRIVING_COCKPIT',t)

# M09H collision repair: retain the inherited tucked elbow bend during threshold crossing.
_BEFORE_ELBOW_REPAIR=state
def state(shot,t):
 d=_BEFORE_ELBOW_REPAIR(shot,t)
 if shot=='DOOR_ENTRY':
  original=B.state(shot,t)['pose']
  for j,arm in enumerate(d['pose']['arms']):
   old=original['arms'][j];bend=np.asarray(old['elbow'])-(np.asarray(old['shoulder'])+np.asarray(old['wrist']))/2
   arm['elbow']=ik(arm['shoulder'],arm['wrist'],.34,.34,bend)
 return d
