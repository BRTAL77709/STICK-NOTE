from contact_rig import *
DURATION=3.
HINGE=V(2.6,0,0);FACE=-.071

def state(t):
 angle=math.radians(9)*Q(t,2.55,3.);doorR=RY(angle)
 def D(p):return HINGE+doorR@np.array(p)
 # Door local X runs left from hinge; local Z is its true surface normal.
 depth=-.34+.16*Q(t,.25,.75);turn=math.pi/2*Q(t,1.03,1.45);K=doorR@RZ(turn);bow=D(V(-.75,1.25,depth));tip=D(V(-.75,1.25,depth+.16));grip=bow+K@V(-.040,-.025,-.043)
 keypads=[bow+K@V(.044*math.cos(a),.027*math.sin(a),-.004) for a in [math.radians(145),math.radians(-70)]]
 lever=-.30*Q(t,2.10,2.50);spindle=D(V(-.75,1.05,FACE));handleR=doorR@RZ(lever);end=spindle+handleR@V(.095,0,0);leftgrip=end+handleR@V(-.025,.016,-.045);pad=[end+handleR@V(-.025,.011,0),end+handleR@V(-.025,-.011,0)]
 r=V(1.57+.025*Q(t,2.1,2.5),.65-.018*Q(t,2.1,2.5),-.40+.08*Q(t,2.5,3));leftrest=r+V(-.09,.15,.05);left=mix(leftrest,leftgrip,Q(t,1.60,2.05));ff=[{'sole':V(1.42,0,-.48),'planted':True,'pitch':0,'heading':0},{'sole':V(1.64,0,-.30),'planted':True,'pitch':0,'heading':0}]
 # Facing the door (+Z); spine leans before the handle takes load.
 p=pose(r,ff,[grip,left],heading=0,pitch=.035+.055*Q(t,1.9,2.4),twist=.035*Q(t,1.0,1.45),look=.70,fear=.55,knee_forward=V(0,0,1));openpads=[left+handleR@V(.022,.042,.012),left+handleR@V(.025,-.021,.020)];leftpads=[mix(a,b,Q(t,1.90,2.05)) for a,b in zip(openpads,pad)];fg=[fingers(grip,keypads,K@V(-1,0,-1),[K@V(0,0,-1)]*2),fingers(left,leftpads,handleR@V(1,0,-1),[handleR@V(0,1,0),handleR@V(0,-1,0)])]
 return {'time':t,'pose':p,'door_angle':angle,'door_R':doorR,'key_R':K,'keybow':bow,'keytip':tip,'key_depth_local':depth,'keyturn':turn,'keypads':keypads,'handle_R':handleR,'spindle':spindle,'handle_end':end,'lever':lever,'fingers':fg,'hand_frames':[K,handleR],'handle_grip':t>=2.05,'latch_retraction':.025*Q(t,2.1,2.5),'bolt_retraction':.025*Q(t,1.3,1.45),'phase':'aim' if t<.25 else 'insert' if t<.75 else 'seat' if t<1.03 else 'turn to detent' if t<1.6 else 'other hand grips lever' if t<2.1 else 'depress and crack door'}
