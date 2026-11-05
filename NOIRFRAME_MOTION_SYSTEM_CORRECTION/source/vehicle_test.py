from contact_rig import *
DURATION=4.;WB=2.60;RADIUS=.30;DT=1/120

def curvature(s):return (Q(s,4,8)-Q(s,18,22))/30
# A fixed road sampled before any animation, shared by both cameras/vehicles.
ROAD=[];x=0.;z=-25.;a=0.
for s in np.arange(-25,80,.05):
 ROAD.append([float(s),x,z,a]);k=curvature(s+.025);a+=k*.05;x+=math.sin(a)*.05;z+=math.cos(a)*.05
ROAD=np.array(ROAD)
def route(s):return np.array([np.interp(s,ROAD[:,0],ROAD[:,1]),0,np.interp(s,ROAD[:,0],ROAD[:,2])])
def road_x(z):return float(np.interp(z,ROAD[:,2],ROAD[:,1]))
def controls(t):return .72*(1-Q(t,1.9,2.2)),.65*Q(t,2.8,3.25)

# Two independent advances along one fixed route, with their own speed and wheel phase.
RUN=[];s=0.;sb=-12.;v=5.2;vb=6.25;roll=0.;rv=0.;pitch=0.;pv=0.;dist=0.;distb=0.;rollb=0.;rvb=0.;pitchb=0.;pvb=0.
for n in range(481):
 t=n*DT;th,br=controls(t);acc=1.4*th-2.1*br-.10;ab=1.4*th-2.1*br*.94-.10
 steer=math.atan(WB*curvature(s));steerb=math.atan(WB*curvature(sb));yaw=float(np.interp(s,ROAD[:,0],ROAD[:,3]));yawb=float(np.interp(sb,ROAD[:,0],ROAD[:,3]));eqroll=.025*v*v*curvature(s);eqpitch=-.013*acc
 if n%4==0:RUN.append({'time':t,'s':s,'pursuer_s':sb,'position':route(s),'pursuer_position':route(sb),'yaw':yaw,'pursuer_yaw':yawb,'speed':v,'pursuer_speed':vb,'acceleration':acc,'throttle':th,'brake':br,'steer':steer,'pursuer_steer':steerb,'wheel_phase':dist/RADIUS,'pursuer_wheel_phase':distb/RADIUS,'roll':roll,'pitch':pitch,'pursuer_roll':rollb,'pursuer_pitch':pitchb,'gap':s-sb,'road_static':True})
 rollacc=12**2*(eqroll-roll)-2*.78*12*rv;rv+=rollacc*DT;roll+=rv*DT;pa=10**2*(eqpitch-pitch)-2*.8*10*pv;pv+=pa*DT;pitch+=pv*DT
 rbacc=12**2*(.025*vb*vb*curvature(sb)-rollb)-2*.78*12*rvb;rvb+=rbacc*DT;rollb+=rvb*DT;pbacc=10**2*(-.013*ab-pitchb)-2*.8*10*pvb;pvb+=pbacc*DT;pitchb+=pvb*DT
 v=max(0,v+acc*DT);vb=max(0,vb+ab*DT);ds=v*DT;db=vb*DT;s+=ds;sb+=db;dist+=ds;distb+=db

def pedal(t,kind):
 th,br=controls(t);press=th if kind==0 else br;theta=.80-.45*press;hinge=V(-.21 if kind==0 else -.43,.055,.38);normal=V(0,math.cos(theta),-math.sin(theta));return {'hinge':hinge,'angle':theta,'normal':normal,'pressure':press}
def foot_on_pedal(ped,yaw):
 H=V(-.32,.04,.27);L=.24;n=ped['normal'];q=ped['hinge'];A=L*n[1];B=L*(n[0]*math.sin(yaw)+n[2]*math.cos(yaw));C=float(n@(q-H));pitch=math.asin(C/math.sqrt(A*A+B*B))-math.atan2(B,A);toe=H+V(L*math.cos(pitch)*math.sin(yaw),L*math.sin(pitch),L*math.cos(pitch)*math.cos(yaw));return H,toe,pitch

def state(t):
 d=dict(RUN[min(120,round(t*30))]);theta=d['steer']*12;tilt=.28;wheelR=RX(-tilt)@RZ(theta);center=V(-.38,.79,.56)
 # A single rigid wheel transform supplies mesh, wrists and contact pads.
 def W(a):return center+wheelR@V(.245*math.cos(a),.245*math.sin(a),0)
 pads=[];wr=[];fg=[]
 for a in [math.pi/6,5*math.pi/6]:
  p=W(a);normal=wheelR@V(0,0,1);wrist=p-normal*.050;points=[W(a-.045)-normal*.015,W(a+.045)-normal*.015];wr.append(wrist);pads.append(points);fg.append(fingers(wrist,points,wheelR@V(0,-1,-1),[-normal,-normal]))
 ped0=pedal(t,0);ped1=pedal(t,1);H,P0,p0=foot_on_pedal(ped0,.52);_,P1,p1=foot_on_pedal(ped1,-.52)
 if t<=2.20:P=P0;contact='accelerator'
 elif t>=2.80:P=P1;contact='brake'
 else:
  u=(t-2.2)/.6;yaw=.52-1.04*Q(u,.20,.80);pitch=p0+(p1-p0)*Q(u,.0,1)+.25*math.sin(math.pi*u)**2;P=H+V(.24*math.cos(pitch)*math.sin(yaw),.24*math.sin(pitch),.24*math.cos(pitch)*math.cos(yaw));contact=None
 ankle=H+(P-H)/.24*.042+V(0,.065,0);leftH=V(-.60,.04,.17);leftP=leftH+V(0,0,.24)
 ff=[{'sole':H,'heel':H,'toe':P,'ankle':ankle,'planted':True,'pitch':0,'heading':0},{'sole':leftH,'heel':leftH,'toe':leftP,'ankle':leftH+V(0,.065,.04),'planted':True,'pitch':0,'heading':0}]
 ff[0]['surface_normal']=ped0['normal'] if contact=='accelerator' else ped1['normal'] if contact=='brake' else None
 for foot in ff:foot['sole_mesh'],foot['shoe_up']=shoe_surface(foot)
 pitch=.035+.065*(Q(t,.25,.9)-Q(t,2.9,3.6));twist=-.07*(Q(t,.25,.7)-Q(t,2.7,3.4));p=pose(V(-.38,.30,-.02),ff,wr,heading=0,pitch=pitch,roll=-.025*Q(t,.5,1.4)*(1-Q(t,2.8,3.7)),twist=twist,look=.35+.35*(Q(t,.2,.65)-Q(t,2.7,3.4)),fear=.35+.35*Q(t,2.2,2.6),head_lag=.025*Q(t,.1,.5),knee_forward=V(0,.5,1))
 d.update(pose=p,fingers=fg,hand_frames=[wheelR@RZ(a) for a in [math.pi/6,5*math.pi/6]],wheel_R=wheelR,wheel_center=center,grip_pads=pads,pedals=[ped0,ped1],toe_contact=contact,toe=P,heel=H,phase='look, steer and accelerate' if t<2.2 else 'heel pivot / coast' if t<2.8 else 'brake and unwind')
 return d
