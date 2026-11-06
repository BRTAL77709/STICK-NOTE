from contact_rig import *
from vehicle_dynamics import RUN,controls,road_x
DURATION=6.
def pedal(t,kind):
 th,br=controls(t);press=th if kind==0 else br;theta=.80-.45*press;hinge=V(-.21 if kind==0 else -.43,.055,.38);normal=V(0,math.cos(theta),-math.sin(theta));return {'hinge':hinge,'angle':theta,'normal':normal,'pressure':press}
def foot_on_pedal(ped,yaw):
 H=V(-.32,.04,.27);L=.24;n=ped['normal'];q=ped['hinge'];A=L*n[1];B=L*(n[0]*math.sin(yaw)+n[2]*math.cos(yaw));C=float(n@(q-H));pitch=math.asin(C/math.sqrt(A*A+B*B))-math.atan2(B,A);toe=H+V(L*math.cos(pitch)*math.sin(yaw),L*math.sin(pitch),L*math.cos(pitch)*math.cos(yaw));return H,toe,pitch

def state(t):
 d=dict(RUN[min(180,round(t*30))]);theta=d['steer']*12;tilt=.28;wheelR=RX(-tilt)@RZ(theta);center=V(-.38,.79,.56)
 # A single rigid wheel transform supplies mesh, wrists and contact pads.
 def W(a):return center+wheelR@V(.245*math.cos(a),.245*math.sin(a),0)
 pads=[];wr=[];fg=[]
 for a in [math.pi/6,5*math.pi/6]:
  p=W(a);normal=wheelR@V(0,0,1);wrist=p-normal*.050;points=[W(a-.045)-normal*.015,W(a+.045)-normal*.015];wr.append(wrist);pads.append(points);fg.append(fingers(wrist,points,wheelR@V(0,-1,-1),[-normal,-normal]))
 ped0=pedal(t,0);ped1=pedal(t,1);H,P0,p0=foot_on_pedal(ped0,.52);_,P1,p1=foot_on_pedal(ped1,-.52)
 if t<=4.20:P=P0;contact='accelerator'
 elif t>=4.80:P=P1;contact='brake'
 else:
  u=(t-4.2)/.6;yaw=.52-1.04*Q(u,.20,.80);pitch=p0+(p1-p0)*Q(u,.0,1)+.25*math.sin(math.pi*u)**2;P=H+V(.24*math.cos(pitch)*math.sin(yaw),.24*math.sin(pitch),.24*math.cos(pitch)*math.cos(yaw));contact=None
 ankle=H+(P-H)/.24*.042+V(0,.065,0);leftH=V(-.60,.04,.17);leftP=leftH+V(0,0,.24)
 ff=[{'sole':H,'heel':H,'toe':P,'ankle':ankle,'planted':True,'pitch':0,'heading':0},{'sole':leftH,'heel':leftH,'toe':leftP,'ankle':leftH+V(0,.065,.04),'planted':True,'pitch':0,'heading':0}]
 ff[0]['surface_normal']=ped0['normal'] if contact=='accelerator' else ped1['normal'] if contact=='brake' else None
 for foot in ff:foot['sole_mesh'],foot['shoe_up']=shoe_surface(foot)
 pitch=.035+.065*(Q(t,.25,.9)-Q(t,5.1,5.9));twist=-.07*(Q(t,.25,.7)-Q(t,4.7,5.4));p=pose(V(-.38,.30,-.02),ff,wr,heading=0,pitch=pitch,roll=-.025*Q(t,.5,1.4)*(1-Q(t,4.8,5.7)),twist=twist,look=.35+.35*(Q(t,.2,.65)-Q(t,4.7,5.4)),fear=.35+.35*Q(t,4.2,4.6),head_lag=.025*Q(t,.1,.5),knee_forward=V(0,.5,1))
 d.update(pose=p,fingers=fg,hand_frames=[wheelR@RZ(a) for a in [math.pi/6,5*math.pi/6]],wheel_R=wheelR,wheel_center=center,grip_pads=pads,pedals=[ped0,ped1],toe_contact=contact,toe=P,heel=H,phase='look, steer and accelerate' if t<4.2 else 'heel pivot / coast' if t<4.8 else 'brake and unwind')
 return d
