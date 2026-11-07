"""M11 contact-first target authoring; actual Blender IK supplies rendered geometry.
Metres, Y up. Original M10 evaluated-state snapshots supply unchanged interactions.
Kinematic animation constraints, not a claim of force-based balance or friction physics.
"""
from bootstrap import ROOT as R
from contact_rig import *
import json,gzip,copy
import vehicle_system as VS
DURATIONS={'DRIVING_COCKPIT':12.,'ROAD_BUILDINGS':7.,'CAR_CHASE':11.,'CAR_EXIT_RUNNING':10.8,'KEY_LOCK':9.,'DOOR_ENTRY':20.,'STAIRS':17.,'WINDOW_CURTAIN':15.5,'DRIVER_CHASE':11.,'PHONE_CALL':13.,'UNKNOWN_CALLER':5.,'DISCOVERY':4.,'PANIC':4.,'ARRIVAL':5.,'FINAL_POLL':4.5}
REVS=json.loads((R/'configuration/M10_SELECTED_NATIVE.json').read_text());CACHE={};RISE=2.6/15;RUN=.25;STAIR_X=1.05;STAIR_START=1.5

def restore(q):
 if isinstance(q,dict):return {k:restore(v) for k,v in q.items()}
 if isinstance(q,list):
  try:
   a=np.asarray(q)
   if a.size and a.dtype.kind in 'fiu':return a
  except (TypeError,ValueError):pass
  return [restore(v) for v in q]
 return q

def baseline(shot,t):
 if shot not in CACHE:CACHE[shot]=json.load(gzip.open(R/'scenes'/f'{shot}_{REVS[shot]}.json.gz','rt'))
 data=CACHE[shot];return restore(copy.deepcopy(data['state'][min(len(data['state'])-1,max(0,round(t*30)))]))

def walk(t,initial,plans,heading=0.,height=.705):
 feet=[];active=0.
 for j in range(2):
  pos=np.array(initial[j],float);angle=heading;f={'sole':pos,'heading':angle,'pitch':0.,'planted':True}
  for a,b,end in plans[j]:
   a=round(a*30)/30;b=round(b*30)/30
   if t<a:break
   if t<b:
    u=(t-a)/(b-a);end=np.array(end);p=mix(pos,end,Q(u,.20,1.));p[1]=pos[1]+(end[1]-pos[1])*Q(u,0,.50)+.13*Q(u,0,.22)*(1-Q(u,.56,1));f={'sole':p,'heading':angle,'pitch':.09*math.sin(math.pi*u)**2,'planted':False};active=(1 if j==0 else -1)*math.sin(math.pi*u);break
   pos=np.array(end);f={'sole':pos,'heading':angle,'pitch':0.,'planted':True}
  feet.append(foot_geometry(f))
 root=(feet[0]['sole']+feet[1]['sole'])/2+V(.018*active,height-.022*abs(active),0)
 for j,f in enumerate(feet):
  off=RY(heading)@V((.07,-.07)[j],0,0);h=np.linalg.norm((root+off-f['ankle'])[[0,2]]);root[1]=min(root[1],f['ankle'][1]+math.sqrt(max(.001,.72**2-h*h)))
 hands=[root+RY(heading)@V(.22,.14,.10-.14*active),root+RY(heading)@V(-.22,.14,.10+.14*active)];p=pose(root,feet,hands,heading=heading,pitch=.08,twist=.035*active,pelvis_roll=.018*active,fear=.85,look=.65);p['head_forward']=RY(heading)@V(0,.025,1)
 return {'pose':p,'fingers':[[],[]],'hand_frames':[None,None],'contact':None,'time':t,'phase':'world-space stance / lift-before-advance / load transfer'}

def stairs(t):
 initial=[V(1.125,0,1.32),V(.975,0,1.20)];plans=[[],[]]
 for k in range(17):
  j=k%2;a=round((.55+k*.65)*30)/30;b=round((a+.44)*30)/30;n=min(k+1,15);z=1.5+(min(k,14)+.5)*RUN-.035 if k<15 else 5.25+.16+(k-15)*.16;plans[j].append((a,b,V(STAIR_X+(.075,-.075)[j],n*RISE,z)))
 for k,(x,z) in enumerate([(.70,5.97),(.35,5.97),(-.05,5.97),(-.45,5.97),(-.715,5.20),(-.885,5.05)]):
  j=(k+17)%2;a=round((11.9+k*.65)*30)/30;plans[j].append((a,round((a+.46)*30)/30,V(x,2.6,z)))
 d=walk(t,initial,plans);p=d['pose'];ff=p['legs'];orient=lambda u:-math.pi/2*Q(u,11.9,13.)-math.pi/2*Q(u,14.5,16.);heading=orient(t)
 for j,f in enumerate(ff):
  angle=0.
  for a,b,end in plans[j]:
   if t<a:break
   endangle=orient(b)
   if t<b:angle=float(mix(angle,endangle,Q(t,a,b)));break
   angle=endangle
  f['heading']=angle;foot_geometry(f)
 root=p['root'].copy()
 for j,f in enumerate(ff):
  off=RY(heading)@V((.07,-.07)[j],0,0);h=np.linalg.norm((root+off-f['ankle'])[[0,2]]);root[1]=min(root[1],f['ankle'][1]+math.sqrt(max(.001,.72**2-h*h)))
 hands=[root+RY(heading)@(p['arms'][j]['wrist']-p['root']) for j in range(2)];anticipate=Q(t,.05,.3)*(1-Q(t,.55,1.1));d['pose']=pose(root,ff,hands,heading=heading,pitch=.08+.05*anticipate,twist=.018*math.sin(t*2),fear=.85);d['pose']['head_forward']=RY(heading)@V(0,0,1);d['phase']='anticipation' if t<.55 else '15 real risers / weight transfer' if t<11.9 else 'upper landing / supported turn / bedroom entry';return d

def door_end(t):
 old=baseline('DOOR_ENTRY',15.999);initial=[f['sole'] for f in old['pose']['legs']];plans=[[(.2,.65,V(.25,0,1.40)),(1.6,2.05,V(.75,0,1.30)),(3.,3.45,V(1.125,0,1.32))],[(.9,1.35,V(.50,0,1.44)),(2.3,2.75,V(.975,0,1.20))]];d=walk(t-16,initial,plans)
 if t<16.2:
  p=d['pose'];root=mix(old['pose']['root'],p['root'],Q(t,16,16.2));hands=[mix(old['pose']['arms'][j]['wrist'],p['arms'][j]['wrist'],Q(t,16,16.2)) for j in range(2)];d['pose']=pose(root,p['legs'],hands,heading=0,pitch=.05,fear=.85)
 d.update({k:v for k,v in old.items() if k not in ['pose','fingers','hand_frames','contact','phase','time']});d['time']=t;d['phase']='planted hallway departure / approach exact stair start';return d

def bedroom(t):
 if t<5:
  plans=[[],[]]
  for k in range(10):
   j=k%2;a=.20+k*.43;b=a+.32;end=V((.085,-.085)[j],0,-5+(k+1)*.36)
   if k==8:end=V(.29,0,-1.3)
   if k==9:end=V(.04,0,-1.48)
   plans[j].append((a,b,end))
  d=walk(t,[V(.085,0,-5.05),V(-.085,0,-5.20)],plans);ref=baseline('WINDOW_CURTAIN',1.)
  if t>4.5:
   p=d['pose'];root=mix(p['root'],ref['pose']['root'],Q(t,4.5,5.));hands=[mix(p['arms'][j]['wrist'],ref['pose']['arms'][j]['wrist'],Q(t,4.5,5.)) for j in range(2)];d['pose']=pose(root,p['legs'],hands,heading=0,pitch=.04,fear=.85)
  d.update({k:v for k,v in ref.items() if k not in ['pose','fingers','hand_frames','contact','phase','time']});return d
 d=baseline('WINDOW_CURTAIN',min(10.4999,t-4.));d['time']=t;v=d['sedan_position']-d['pose']['head'];v[1]=0;v/=np.linalg.norm(v);d['pose']['head_forward']=mix(v,V(-.8,0,-.6),Q(t,12.45,13.3));return d

def phone(t,threat=False):
 t=t+10 if threat else t;ref=baseline('WINDOW_CURTAIN',10.4999);initial=[f['sole'] for f in ref['pose']['legs']];heading=math.pi*Q(t,.45,1.4);plans=[[(.5,.9,V(-.20,0,-.53))],[(1.,1.4,V(-.02,0,-.35))]];d=walk(t,initial,plans);p=d['pose'];root=mix(ref['pose']['root'],V(-.11,.705,-.44),Q(t,.45,1.4));shock=Q(t,5.,5.5)*(1-Q(t,6.4,7.));fear=Q(t,10.1,10.6);root-=V(0,.028*shock+.018*fear,0)
 # Persist shoe heading between authored airborne turns.
 for j,f in enumerate(p['legs']):
  a,b,_=plans[j][0];f['heading']=math.pi*Q(t,a,b);foot_geometry(f)
 p=pose(root,p['legs'],heading=heading,pitch=.03*Q(t,.7,1.2)-.08*shock-.055*fear,pelvis_roll=.012*shock,fear=.55+.25*shock+.20*fear);d['pose']=p;lift=Q(t,2.3,3.9);center=mix(V(-.55,.732,-.75),p['head']+V(-.235,-.035,-.025),lift);rot=RX(math.pi/2*(1-lift))@RY(-math.pi/2*lift);grip=center+rot@V(-.018,-.045,-.018);neutral=root+RY(heading)@V(.22,.14,.10);wrist=mix(neutral,grip,Q(t,.9,2.2));p['arms'][0]['wrist']=wrist;p['arms'][0]['elbow']=ik(p['arms'][0]['shoulder'],wrist,.34,.34,V(-.6,-.7,-.2));free=root+RY(heading)@V(-.20,.13+.17*shock+.12*fear,.1+.10*shock);p['arms'][1]['wrist']=free;p['arms'][1]['elbow']=ik(p['arms'][1]['shoulder'],free,.34,.34,V(.6,-.7,-.2));p['head_forward']=mix(V(0,0,-1),V(-.7,-.2,-.4),Q(t,.3,.9)*(1-Q(t,3.,4.)));p['gaze']=-.65*Q(t,.15,.5)*(1-Q(t,3.,4.))
 d.update(phone_position=center,phone_R=rot,phone_grip=grip,phone_contact=t>=2.2,fabric=ref['fabric'],sedan_position=VS.window_point(VS.PARK['pursuer_position']),sedan_yaw=VS.PARK['pursuer_yaw']-math.atan2(VS.WINDOW_R[0,2],VS.WINDOW_R[2,2]),phase='ring / attention / supported turn' if t<1.4 else 'reach / grip' if t<2.3 else 'lift / wrist rotation' if t<3.9 else 'offer / listening / threat reaction')
 if t>=2.2:
  d['hand_frames'][0]=rot;pads=[center+rot@V(-.025,-.045,-.024),center+rot@V(.025,-.045,-.024)];d['fingers'][0]=fingers(wrist,pads,V(0,-1,0),[rot@V(0,0,-1)]*2)
 return d

def state(shot,t):
 if shot in ['ROAD_BUILDINGS','CAR_CHASE','ARRIVAL']:
  d=VS.state(t*1.1 if shot=='ROAD_BUILDINGS' else 6+t if shot=='ARRIVAL' else t);d['time']=t;d['phase']='integrated bicycle-model world trajectory';return d
 if shot=='STAIRS':return stairs(t)
 if shot=='DOOR_ENTRY' and t>=16:return door_end(t)
 if shot=='WINDOW_CURTAIN':return bedroom(t)
 if shot in ['PHONE_CALL','UNKNOWN_CALLER']:return phone(t,shot=='UNKNOWN_CALLER')
 if shot in ['DISCOVERY','PANIC']:
  d=baseline('DRIVING_COCKPIT',min(11.9667,t+(6 if shot=='DISCOVERY' else 2)));d['time']=t;return d
 d=baseline(shot,t);d['time']=t
 if shot=='CAR_EXIT_RUNNING':d['vehicle_stationary']=True
 return d
