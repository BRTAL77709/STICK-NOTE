"""Shot-specific authored contacts. Native Blender, not these analytic poses, supplies final geometry."""
from bootstrap import ROOT
from contact_rig import *
from locomotion import ground_feet
import key_test,curtain_test,vehicle_test
import vehicle_system as VS
DURATIONS={'DRIVING_COCKPIT':8.,'ROAD_BUILDINGS':7.,'CAR_CHASE':11.,'CAR_EXIT_RUNNING':10.8,'KEY_LOCK':7.,'DOOR_ENTRY':13.,'STAIRS':5.,'WINDOW_CURTAIN':9.5}

def driving(t):
 vt=min(6,t*.75);d=vehicle_test.state(vt);car=VS.state(t);d.update(car);d['time']=t;d['phase']='road / mirror / steering / acceleration / braking';d['pose']['fear']=.35+.4*Q(t,2,4);d['pose']['yaw']=.75-.8*(Q(t,1.1,1.6)-Q(t,2.,2.4));return d

def key_lock(t):
 d=continuous_key(t*4.4/7);d['time']=t;return d

def door_entry(t):
 raw=4.4+t;d=continuous_key(min(raw,14.99));d['time']=t
 if raw>15:
  target=key_test.HINGE+V(-.75,1.16,.12);p=d['pose'];r=p['root'];wr=mix(p['arms'][1]['wrist'],target,Q(raw,15.0,15.4)*(1-Q(raw,16.6,17.0)));ff=[{k:v for k,v in f.items() if k not in ['hip','knee']} for f in p['legs']];d['pose']=pose(r,ff,[p['arms'][0]['wrist'],wr],heading=math.pi,pitch=.03,look=-.75,fear=.65,knee_forward=V(0,.1,-1));d['grip']=wr;d['contact']='inside_lock' if 15.4<=raw<=16.6 else None;d['keyturn']=math.pi/2*(Q(raw,15.5,16.0)-Q(raw,16.2,16.55));d['phase']='inside thumbturn / lock / release';d['unlocked']=raw<16.0;d['fingers']=[[],[]]
  if d['contact']=='inside_lock':
   K=RZ(d['keyturn']);pads=[V(-.30,1.16,.105)+K@V(.018,0,0),V(-.30,1.16,.105)+K@V(-.018,0,0)];d['fingers'][1]=fingers(wr,pads,V(0,-1,0),[V(0,0,1)]*2);d['hand_frames']=[None,K]
 return d

def curtain(t):
 u=max(0,(t-2)*5/6.5);d=curtain_test.state(min(5,u));d['time']=t;d['sedan_position']=VS.window_point(VS.PARK['pursuer_position']);d['sedan_yaw']=math.atan2(*( (VS.WINDOW_R.T@RY(VS.PARK['pursuer_yaw'])@V(0,0,1))[[0,2]] ))
 if t<2:
  def path(s):return V(.20,.66-.02*Q(s,1.6,1.95),-1.30+.94*Q(s,0,1.90))
  ff=[]
  for j,start in enumerate([V(.29,0,-1.30),V(.04,0,-1.48)]):
   moves=[(.08,.65,V(.23,0,-.90)),(1.,1.60,V(.19,0,-.42))] if j==0 else [(.38,.92,V(0,0,-.78)),(1.35,1.95,V(-.07,0,-.28))]
   foot={'sole':start,'heading':0,'pitch':0,'planted':True}
   for a,b,end in moves:
    if t<a:break
    u=clamp((t-a)/(b-a));foot={'sole':mix(start,end,Q(t,a,b))+V(0,.09*math.sin(math.pi*u)**2,0),'heading':0,'pitch':.08*math.sin(math.pi*u)**2,'planted':t>=b}
    if t<b:break
    foot.update(sole=end,pitch=0,planted=True);start=end
   ff.append(foot_geometry(foot))
  r=path(t)
  for f in ff:
   hor=np.linalg.norm((r-f['ankle'])[[0,2]]);r[1]=min(r[1],f['ankle'][1]+math.sqrt(max(.001,.72**2-hor**2)))
  hands=[r+V(.20,.13,.13+.09*math.sin(t*5)),r+V(-.20,.13,.13-.09*math.sin(t*5))];d['pose']=pose(r,ff,hands,heading=0,pitch=.08*(1-Q(t,1.4,2)),look=.8,fear=.45,knee_forward=V(0,.1,1));d['fingers']=[[],[]];d['grip_contact']=False;d['phase']='bedroom entry / approach / stop'
 else:d['phase']='fabric grip / fold / reveal / frightened recoil / release'
 d['hide_actor']=t>=8.5
 return d

EXIT_STEPS=[(3.75,4.70,1,V(-1.25,0,-.10)),(4.75,5.45,0,V(-1.15,0,-.32)),(5.95,6.42,1,V(-1.85,0,-.16)),(6.46,6.92,0,V(-2.55,0,-.05)),(6.96,7.42,1,V(-3.20,0,.06)),(7.46,7.92,0,V(-3.85,0,.20)),(7.96,8.42,1,V(-4.50,0,.34)),(8.46,8.96,0,V(-5.00,.13,.48)),(9.,9.52,1,V(-5.35,.13,.65))]
def exit_feet(t):
 initial=[V(-.32,.04,.40),V(-.60,.04,.28)];out=[]
 for j in range(2):
  start=initial[j];a0=0.;h=0;f={'sole':start,'pitch':0,'heading':0.,'planted':True}
  for a,b,leg,end in EXIT_STEPS:
   if leg!=j:continue
   if t<a:break
   u=clamp((t-a)/(b-a));f={'sole':mix(start,end,Q(t,a,b))+V(0,(.10 if a>5 else .13)*math.sin(math.pi*u)**2,0),'heading':h+(-math.pi/2-h)*Q(t,a,b),'pitch':.12*math.sin(math.pi*u)**2,'planted':t>=b}
   if t<b:break
   f.update(sole=end,pitch=0,heading=-math.pi/2);start=end;h=-math.pi/2
  out.append(foot_geometry(f))
 return out

def exit_state(t):
 # Vehicle parking completed at the beginning; the shot first shows settled body/brake state.
 a=math.radians(76)*Q(t,2.7,3.85);H=V(-.85,.65,.70);doorR=RY(a);handle=H+doorR@V(-.025,0,-.95);ff=exit_feet(t)
 roots=[(0,(-.38,.30,-.02)),(2.7,(-.40,.31,-.02)),(3.8,(-.58,.34,-.06)),(4.7,(-.86,.43,-.10)),(5.45,(-1.20,.63,-.20)),(5.95,(-1.37,.68,-.20)),(6.42,(-1.68,.68,-.14)),(6.92,(-2.25,.68,-.06)),(7.42,(-2.86,.68,.05)),(7.92,(-3.52,.68,.16)),(8.42,(-4.15,.68,.29)),(8.96,(-4.72,.79,.43)),(9.52,(-5.13,.84,.58)),(10.3,(-5.22,.86,.60))];r=channel(t,roots);h=-math.pi/2*Q(t,3.15,4.8)
 for j,f in enumerate(ff):
  hip=r+RY(h)@V((.07,-.07)[j],0,0);horizontal=np.linalg.norm((hip-f['ankle'])[[0,2]]);r[1]=min(r[1],f['ankle'][1]+math.sqrt(max(.001,.72**2-horizontal**2)))
 wheel=[V(-.22,.92,.53),V(-.54,.92,.53)];rest=[r+RY(h)@V(.20,.16,.12),r+RY(h)@V(-.20,.16,.12)];hands=[mix(wheel[j],rest[j],Q(t,1.5,2.2)) for j in range(2)];hands[1]=mix(hands[1],handle+V(0,.0,-.035),Q(t,2.05,2.55)*(1-Q(t,3.0,3.18)))
 if t>5.7:
  swing=.13*math.sin((t-5.7)*math.pi/.49)*(1-Q(t,9.1,10.3));hands=[rest[j]+RY(h)@V(0,.05,(1,-1)[j]*swing) for j in range(2)]
 p=pose(r,ff,hands,heading=h,pitch=.12*(Q(t,4.7,5.6)-Q(t,9.5,10.3)),look=.85,fear=.75,knee_forward=RY(h)@V(0,.5,1));fg=[[],[]]
 if 2.55<=t<=3.0:fg[1]=fingers(hands[1],[handle+V(0,.012,-.01),handle+V(0,-.012,-.01)],V(0,-1,0),[V(0,0,-1)]*2)
 return {'time':t,'pose':p,'fingers':fg,'hand_frames':[None,None],'phase':'park / wheel release / handle / door / legs out / weight transfer / run / entrance','door_angle':a,'car_handle':handle,'handle_contact':2.55<=t<=3.0,'support':[j for j,f in enumerate(ff) if f['planted']],'vehicle_stationary':True}

def state(shot,t):
 if shot=='KEY_LOCK':return key_lock(t)
 if shot=='DOOR_ENTRY':return door_entry(t)
 if shot=='WINDOW_CURTAIN':return curtain(t)
 if shot=='CAR_EXIT_RUNNING':return exit_state(t)
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:return driving(t)
 d=VS.state(t if shot=='CAR_CHASE' else t*1.1);d['time']=t;d['phase']='fixed city / independent integrated cars';return d
# M07 driving: use the authoritative state for wheel AND pedal controls.
DURATIONS['DRIVING_COCKPIT']=12.
def driving(t):
 car=VS.state(t);theta=car['steer']*12;wheelR=RX(-.28)@RZ(theta);center=V(-.38,.79,.56);wr=[];fg=[];pads=[]
 def W(a):return center+wheelR@V(.245*math.cos(a),.245*math.sin(a),0)
 for a in [math.pi/6,5*math.pi/6]:
  normal=wheelR@V(0,0,1);wrist=W(a)-normal*.05;points=[W(a-.045)-normal*.015,W(a+.045)-normal*.015];wr.append(wrist);pads.append(points);fg.append(fingers(wrist,points,wheelR@V(0,-1,-1),[-normal]*2))
 pedals=[]
 for j,press in enumerate([car['throttle'],car['brake']]):
  angle=.80-.45*press;pedals.append({'hinge':V(-.21 if j==0 else -.43,.055,.38),'angle':angle,'normal':V(0,math.cos(angle),-math.sin(angle)),'pressure':press})
 # One invariant rigid sole, heel pivots; toe solves each actual pedal plane.
 H=V(-.32,.04,.27);n=pedals[0]['normal'];q=pedals[0]['hinge'];yaw=.52;L=.21
 def on(p,yaw):
  n=p['normal'];q=p['hinge'];A=L*n[1];B=L*(n[0]*math.sin(yaw)+n[2]*math.cos(yaw));C=float(n@(q-H));angle=math.asin(clamp(C/math.sqrt(A*A+B*B),-1,1))-math.atan2(B,A);return angle
 u=Q(t,5.2,6.0);yaw=.52-1.04*u;pitch=on(pedals[0],.52)*(1-u)+on(pedals[1],-.52)*u+.14*math.sin(math.pi*u)**2;F=V(math.cos(pitch)*math.sin(yaw),math.sin(pitch),math.cos(pitch)*math.cos(yaw));up=V(-math.sin(pitch)*math.sin(yaw),math.cos(pitch),-math.sin(pitch)*math.cos(yaw));ank=H+.09*F+.055*up
 ff=[{'sole':H+.105*F,'shoe_origin':H+.105*F,'heel':H,'toe':H+.21*F,'ankle':ank,'heading':yaw,'pitch':pitch,'planted':True,'contact_mode':'pedal','contact_anchor':H},foot_geometry({'sole':V(-.6,.04,.275),'heading':0,'pitch':0,'planted':True})]
 root=V(-.38,.30,-.02);p=pose(root,ff,wr,heading=0,pitch=.07+.04*(Q(t,1.,2.)-Q(t,9.,10.5)),twist=-.045*(Q(t,1.,2.)-Q(t,9.,10.5)),look=.8-.85*(Q(t,2.,2.4)-Q(t,3.,3.5)),fear=.35+.4*Q(t,2.5,3.5),knee_forward=V(0,.5,1))
 d={**car,'time':t,'pose':p,'fingers':fg,'hand_frames':[wheelR@RZ(a) for a in [math.pi/6,5*math.pi/6]],'wheel_R':wheelR,'wheel_center':center,'grip_pads':pads,'pedals':pedals,'toe_contact':'accelerator' if t<=5.2 else 'brake' if t>=6 else None,'toe':H+.21*F,'heel':H,'phase':'seat / grip / road / mirror / fear / steering / pedal / stop'};return d

DURATIONS['DRIVER_CHASE']=11.
# Continuous key/door authoring: avoid nearest-30Hz M03 samples when slowing the key shot.
_KEY_ROOTS=None
def continuous_key(s):
 global _KEY_ROOTS
 from stabilize import CACHE
 from scipy.ndimage import minimum_filter1d,gaussian_filter1d
 key_test.state(0)
 if _KEY_ROOTS is None:
  stored=CACHE['KEY_DOOR'];roots=np.array([q['pose']['root'] for q in stored]);upper=[]
  for q in stored:
   pp=q['pose'];r=pp['root'];caps=[]
   for foot in pp['legs']:
    off=foot['hip']-r;ank=np.array(foot['ankle']);h=np.linalg.norm((r+off-ank)[[0,2]]);caps.append(ank[1]-off[1]+math.sqrt(max(.001,.724**2-h*h)))
   upper.append(min(caps))
  upper=np.array(upper);safe=np.minimum(upper,gaussian_filter1d(minimum_filter1d(upper,5,mode='nearest'),2,mode='nearest'));roots[:,1]=np.minimum(roots[:,1]+.06,safe-.001);_KEY_ROOTS=roots
 d=key_test._raw_state(min(14.999,s));p=d['pose'];times=np.arange(len(_KEY_ROOTS))/30;r=np.array([np.interp(s,times,_KEY_ROOTS[:,j]) for j in range(3)]);delta=r-p['root'];attached=max(Q(s,1,1.1)*(1-Q(s,4.3,4.4)),Q(s,4.4,4.92)*(1-Q(s,7,7.32)),Q(s,9.5,10));hands=[p['arms'][0]['wrist']+delta,p['arms'][1]['wrist']+delta*(1-attached)]
 if 1.1<=s<4.4:hands[1]=p['arms'][1]['wrist'].copy()
 elif 4.4<=s<4.85:
  held=key_test._raw_state(4.399)['pose']['arms'][1]['wrist'];hands[1]=mix(held,hands[1],Q(s,4.4,4.85))
 ff=[{k:v for k,v in f.items() if k not in ['hip','knee']} for f in p['legs']];d['pose']=pose(r,ff,hands,heading=key_test.heading(s),pitch=.02+.04*(Q(s,1.5,2.1)-Q(s,4,4.4)),look=.8 if s<9.5 else -.6,fear=.65,knee_forward=RY(key_test.heading(s))@V(0,.1,1));d['grip']=d['pose']['arms'][1]['wrist'];return d
