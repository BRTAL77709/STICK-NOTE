"""M10 contact-preserving native target authoring, from actual selected M09 caches."""
from bootstrap import ROOT
from contact_rig import *
from interaction_system import restore,phase
import json,gzip,copy
import vehicle_system as VS
DURATIONS={'DRIVING_COCKPIT':12.,'ROAD_BUILDINGS':7.,'CAR_CHASE':11.,'CAR_EXIT_RUNNING':10.8,'KEY_LOCK':9.,'DOOR_ENTRY':16.,'STAIRS':6.,'WINDOW_CURTAIN':10.5,'DRIVER_CHASE':11.}
REVISIONS=json.loads((ROOT/'BASELINE_REVISIONS.json').read_text());DATA={}
def pulse(t,a,b,c,d):return Q(t,a,b)*(1-Q(t,c,d))
def baseline(shot,t):
 if shot not in DATA:DATA[shot]=json.load(gzip.open(ROOT/'scenes'/f'{shot}_{REVISIONS[shot]}.json.gz','rt'))
 data=DATA[shot];return restore(copy.deepcopy(data['state'][min(len(data['state'])-1,max(0,round(t*30)))]))

def hallway(d,t):
 start=np.array(d['pose']['root']);u=t-13;heading=math.pi*(1-Q(u,.05,.9));ff=[];steps={0:[(.25,.9,V(-.16,0,.75)),(1.65,2.3,V(-.16,0,1.45))],1:[(.95,1.6,V(-.34,0,1.13)),(2.35,2.95,V(-.34,0,1.60))]}
 for j in range(2):
  origin=np.array(d['pose']['legs'][j]['sole']);f={'sole':origin,'heading':math.pi,'pitch':0.,'planted':True}
  for a,b,end in steps[j]:
   if u<a:break
   x=clamp((u-a)/(b-a));f={'sole':mix(origin,end,Q(u,a,b))+V(0,.11*math.sin(math.pi*x)**2,0),'heading':math.pi*(1-Q(u,a,b)),'pitch':.10*math.sin(math.pi*x)**2,'planted':u>=b}
   if u<b:break
   origin=end;f.update(sole=end,heading=0,pitch=0,planted=True)
  ff.append(foot_geometry(f))
 from scipy.interpolate import PchipInterpolator
 r=start.copy();r[2]=float(PchipInterpolator([0,.2,.9,1.6,2.3,2.95,3.],[.44,.44,.68,1.06,1.38,1.50,1.50])(clamp(u,0,3)));r[0]=float(PchipInterpolator([0,.2,.9,1.6,2.3,2.95,3.],[-.25,-.25,-.22,-.28,-.22,-.25,-.25])(clamp(u,0,3)));r[1]=start[1]-.035*Q(u,0,.6)+.02*Q(u,2.6,3)
 for j,f in enumerate(ff):
  off=RY(heading)@V((.07,-.07)[j],0,0);h=np.linalg.norm((r+off-f['ankle'])[[0,2]]);r[1]=min(r[1],f['ankle'][1]+math.sqrt(max(.001,.72**2-h*h)))
 hands=[r+RY(heading)@V(.20,.12,.12),r+RY(heading)@V(-.20,.12,.12)]
 # Continuous release from the last inside-lock grip before the hallway turn.
 for j in range(2):hands[j]=mix(np.array(d['pose']['arms'][j]['wrist']),hands[j],Q(u,0,.35))
 d['pose']=pose(r,ff,hands,heading=heading,pitch=.065*pulse(u,.2,.7,2.2,2.8),look=.5,fear=.8,knee_forward=RY(heading)@V(0,.2,1));d['pose']['head_forward']=RY(math.pi*(1-Q(u,0,.45))+.6*Q(u,2.3,3))@V(0,0,1)
 for j,arm in enumerate(d['pose']['arms']):arm['elbow']=ik(arm['shoulder'],arm['wrist'],.34,.34,V((1,-1)[j]*.5,-.7,1.0))
 d['fingers']=[[],[]];d['hand_frames']=[None,None];d['contact']=None;d['phase']='recover / turn / planted hallway steps / approach staircase';return d

def state(shot,t):
 if shot in ['ROAD_BUILDINGS','CAR_CHASE']:
  d=VS.state(t if shot=='CAR_CHASE' else t*1.1);d['time']=t;d['phase']='registered pursuit and neighborhood';return d
 d=baseline(shot,min(t,12.9666667) if shot=='DOOR_ENTRY' else t);d['time']=t;d['interaction_phase']=phase(shot,t)
 if shot=='DOOR_ENTRY' and t>=13:return hallway(d,t)
 p=d['pose'];r=np.array(p['root']);h=math.atan2(p['pelvis_basis'][0,2],p['pelvis_basis'][2,2]);ff=[{k:v for k,v in f.items() if k not in ['hip','knee']} for f in p['legs']];hands=[np.array(a['wrist']) for a in p['arms']];old=p
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:
  attention=pulse(t,1.6,2.35,3.25,4.);brake=pulse(t,6.2,6.7,7.5,8.2);tension=Q(t,2.7,3.8)
  for j in range(2):hands[j]+=np.asarray(d['wheel_R'])@V(0,0,.004*attention)
  pp=pose(r,ff,hands,heading=0,pitch=.035+.085*brake-.025*Q(t,.5,1.5),roll=-.16*d['steer'],twist=-.12*attention,look=.6,fear=.25+.65*tension,knee_forward=V(0,.5,1))
  mirror=V(0,1.265,.28)-pp['head'];mirror/=np.linalg.norm(mirror);pp['head_forward']=mix(V(0,0,1),mirror,attention)
 elif shot=='CAR_EXIT_RUNNING':
  effort=pulse(t,3.5,4.5,5.1,5.65);run=pulse(t,5.6,6.3,9.2,10.3);pp=pose(r,ff,hands,heading=h,pitch=.055*effort+.12*run,twist=.035*pulse(t,4.1,4.4,4.7,5.0),pelvis_roll=math.atan2(p['pelvis_basis'][1,0],p['pelvis_basis'][1,1]),fear=.85,look=.7,knee_forward=RY(h)@V(0,.3,1));pp['head_forward']=p.get('head_forward',RY(h)@V(0,0,1))
  pull=.022*pulse(t,2.55,2.7,2.9,3.2);delta=RY(d['door_angle'])@V(-pull,0,0);d['car_handle']=np.array(d['car_handle'])+delta;d['handle_pull']=pull
  if d['handle_contact']:
   pp['arms'][1]['wrist']+=delta
   for finger in d['fingers'][1]:
    for k in ['pad','tip_center']:
     if k in finger:finger[k]+=delta
 elif shot=='KEY_LOCK':
  delta=np.asarray(d['key_R'])@V(0,0,.039*d['insertion']);d['keybow']+=delta;d['keytip']+=delta;d['grip']+=delta;hands[1]+=delta
  for finger in d['fingers'][1]:
   for key in ['pad','tip_center']:
    if key in finger:finger[key]+=delta
  focus=pulse(t,2.,3.,6.3,7.4);pp=pose(r,ff,hands,heading=h,pitch=.02+.085*focus,twist=-.04*focus,fear=.82,look=.4,knee_forward=RY(h)@V(0,.1,1));pp['head_forward']=V(0,-.20,1)
 elif shot=='DOOR_ENTRY':
  glance=pulse(t,1.1,1.6,2.,2.5);settle=pulse(t,9.7,10.2,10.7,11.2);pp=pose(r,ff,hands,heading=h,pitch=.025+.045*settle,twist=.045*glance,fear=.8,look=.6,knee_forward=RY(h)@V(0,.1,1));pp['head_forward']=RY(math.pi*glance+math.pi*pulse(t,5.7,6.3,7.1,7.8))@V(0,0,1)
 else:
  listen=pulse(t,3.15,3.55,4.0,4.5);recoil=pulse(t,7.3,7.75,8.15,8.6);T=RY(-h)@np.asarray(p['torso_basis']);pitch=math.atan2(-T[1,2],T[1,1]);pp=pose(r,ff,hands,heading=h,pitch=pitch+.045*listen-.035*recoil,twist=-.065*listen,look=.5,fear=.4+.55*Q(t,7.3,8.0),knee_forward=RY(h)@V(0,.1,1));pp['head_forward']=RY(-.45*listen)@V(0,0,1)
  mesh=np.array(d['fabric']);nr,nc=mesh.shape[:2];follow=.014*(Q(t,6.2,6.5)-1.5*Q(t,6.6,6.95)+.5*Q(t,7.15,7.55));mesh[:,:,2]+=follow*np.sin(np.linspace(0,math.pi,nr))[:,None]**2*np.sin(np.linspace(0,math.pi,nc))[None,:]**2;d['fabric']=mesh
 # Preserve the actual collision-safe elbow bend planes, including the door's tucked arm.
 for j,arm in enumerate(pp['arms']):
  a=old['arms'][j];bend=np.asarray(a['elbow'])-(np.asarray(a['shoulder'])+np.asarray(a['wrist']))/2;arm['elbow']=ik(arm['shoulder'],arm['wrist'],.34,.34,bend)
 d['pose']=pp;return d

def driving(t):return state('DRIVING_COCKPIT',t)
