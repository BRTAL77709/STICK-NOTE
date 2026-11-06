"""10s: approach, retrieve, insert, unlock, withdraw, regrip, open, enter, close."""
from contact_rig import *
from locomotion import ground_feet
DURATION=15.;HINGE=V(.45,0,0);FACE=-.071

def door_angle(t):return math.radians(80)*(Q(t,5.25,6.55)-Q(t,10.25,14.25))
def heading(t):return math.pi*(Q(t,8.85,9.85))
def root_path(t):
 if t<7.25:return channel(t,[(0,(-.12,.65,-.74)),(.72,(-.12,.65,-.42)),(5.25,(-.12,.65,-.42)),(6.55,(-.12,.65,.24)),(7.25,(-.10,.65,.68))])
 close=HINGE+RY(door_angle(t))@V(-.70,.65,.34)
 way=[(7.25,V(-.10,.65,.68)),(8.10,V(-.05,.65,1.25)),(9.05,V(.665,.65,1.25)),(9.90,close)]
 for (a,x),(b,y) in zip(way,way[1:]):
  if t<=b:return mix(x,y,.85*clamp((t-a)/(b-a))+.15*Q(t,a,b))
 return close
SCHEDULE=[(.12,.65,0),(.38,.88,1),(5.28,5.78,0),(5.90,6.42,1),(6.53,7.05,0),(7.12,7.62,1),(7.74,8.24,0),(8.36,8.86,1),(8.98,9.48,0),(9.60,10.10,1),(10.22,10.72,0),(10.84,11.34,1),(11.46,11.96,0),(12.08,12.58,1),(12.70,13.20,0),(13.32,13.82,1),(13.94,14.44,0),(14.56,14.96,1)]
def state(t):
 a=door_angle(t);R=RY(a);D=lambda p:HINGE+R@np.array(p);root=root_path(t);h=heading(t)
 ff=ground_feet(t,root_path,heading,SCHEDULE,[V(-.03,0,-.79),V(-.21,0,-.81)])
 P=RY(h)
 caps=[]
 for j,f in enumerate(ff):
  offset=P@V((.07,-.07)[j],0,0);ank=f['ankle'];dxz=np.linalg.norm((root+offset-ank)[[0,2]]);caps.append(ank[1]+math.sqrt(max(.001,.721**2-dxz**2)))
 root[1]=min(root[1],min(caps))
 # Fixed cylinder axis, blade tip stops in cylinder. Rotation returns before withdrawal.
 insertion=Q(t,2.00,2.55)*(1-Q(t,3.45,3.92));depth=-.34+.16*insertion;turn=math.pi/2*(Q(t,2.75,3.15)-Q(t,3.20,3.43));K=R@RZ(turn);atlock=D(V(-.75,1.16,depth));pocket=root+RY(h)@V(-.18,.12,-.04);bow=mix(pocket,atlock,Q(t,1.20,1.95)*(1-Q(t,3.95,4.40)));keygrip=bow+K@V(-.040,-.025,-.043)
 if t<1.15:grip=mix(root+V(-.18,.18,.06),keygrip,Q(t,.78,1.10))
 elif t<4.40:grip=keygrip
 else:
  inside=t>=9.50;face=.071 if inside else FACE;spindle=D(V(-.75,.96,face));lever=-.38*(Q(t,4.98,5.25)-Q(t,6.65,6.95)+Q(t,10.0,10.25)-Q(t,14.25,14.75));LR=R@RZ(lever);end=spindle+LR@V(.105,0,0);normal=R@V(0,0,1 if inside else -1);target=end+LR@V(-.03,.012,0)+normal*.044;rest=root+RY(h)@V(-.19,.16,.08)
  grip=mix(rest,target,Q(t,4.40,4.92)*(1-Q(t,7.0,7.32))) if t<9.50 else mix(rest,target,Q(t,9.50,10.0))
 inside=t>=9.50;face=.071 if inside else FACE;spindle=D(V(-.75,.96,face));lever=-.38*(Q(t,4.98,5.25)-Q(t,6.65,6.95)+Q(t,10.0,10.25)-Q(t,14.25,14.75));LR=R@RZ(lever);end=spindle+LR@V(.105,0,0);normal=R@V(0,0,1 if inside else -1)
 other=root+RY(h)@V(.20,.15,.13);pitch=.02+.04*(Q(t,1.5,2.1)-Q(t,4.,4.4))
 # Body may lower to satisfy contact reach; no length scaling or wrist teleport.
 p=pose(root,ff,[other,grip],heading=h,pitch=pitch,look=.8 if t<9.50 else -.6,fear=.5,knee_forward=RY(h)@V(0,.1,1))
 fg=[[],[]];contact=None
 if 1.10<=t<4.40:
  pads=[bow+K@V(.044*math.cos(q),.027*math.sin(q),-.004) for q in [math.radians(145),math.radians(-70)]];fg[1]=fingers(grip,pads,K@V(-1,0,-1),[K@V(0,0,-1)]*2);contact='key'
 elif (4.92<=t<=7.) or t>=10.0:
  pads=[end+LR@V(-.03,.011,0),end+LR@V(-.03,-.011,0)];fg[1]=fingers(grip,pads,LR@V(0,0,-1),[LR@V(0,1,0),LR@V(0,-1,0)]);contact='handle'
 phases=[(.78,'approach and plant'),(1.2,'retrieve key'),(2.,'raise and align'),(2.55,'insert'),(2.75,'seat'),(3.2,'unlock'),(3.45,'return cylinder'),(3.95,'withdraw'),(4.4,'stow key'),(4.98,'regrip handle'),(5.25,'depress lever'),(6.55,'open door'),(9.50,'walk around open leaf'),(10.25,'inside grip'),(14.25,'close door'),(15.1,'recover')]
 return {'time':t,'pose':p,'fingers':fg,'hand_frames':[None,K if contact=='key' else LR],'door_R':R,'door_angle':a,'key_R':K,'keybow':bow,'keytip':bow+K@V(0,0,.16),'keyhole':D(V(-.75,1.16,FACE)),'key_visible':1.10<=t<=4.40,'key_depth_local':depth,'keyturn':turn,'insertion':insertion,'spindle':spindle,'handle_end':end,'handle_R':LR,'lever':lever,'contact':contact,'phase':next(v for until,v in phases if t<until),'support':[j for j,f in enumerate(ff) if f['planted']],'grip':grip,'unlocked':t>=3.15,'inside':inside}

# Predict body trajectory over the contact schedule before rendering any frame.
_raw_state=state
def state(t):
 from stabilize import stabilized
 return stabilized('KEY_DOOR',_raw_state,15,t)
