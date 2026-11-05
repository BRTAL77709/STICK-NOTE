"""Evaluate actual rig/sole vertices and prop geometry. Endpoint checks are not artistic approval."""
from pathlib import Path
import sys,json,math
from actions import *
R=Path(__file__).resolve().parents[1];reports={}
for kind,fn in STATES.items():
 length_error=0;stance_drift=0;penetration=0;grip_error=0;root0=None;rootlast=None;previous=None;plants=0;keymax=0;keyinsert=0;contacts=0;door_intersections=0;rail_error=0
 for n in range(round(DURATIONS[kind]*30)):
  t=n/30;d=fn(t);p=d['pose'];root0=p['root'] if root0 is None else root0;rootlast=p['root'];keymax=max(keymax,d.get('keyturn',0))
  for j,l in enumerate(p['legs']):
   for a,b in [('hip','knee'),('knee','ankle')]:length_error=max(length_error,abs(np.linalg.norm(l[b]-l[a])-.37))
   if previous is not None:
    old=previous['legs'][j]
    if old['planted'] and l['planted']:stance_drift=max(stance_drift,float(np.linalg.norm(l['sole']-old['sole'])))
    if not old['planted'] and l['planted']:plants+=1
   pitch=l['pitch'];co,si=math.cos(pitch),math.sin(pitch)
   for xx,yy in [(-.105,0),(.105,0),(.12,.035),(.045,.085),(-.08,.08)]:
    v=l['sole']+V(xx*co-yy*si,xx*si+yy*co,0);floor=2.4 if kind=='WINDOW' else 0
    if kind=='STAIRS':
     x=v[0]
     if x>=2.38-1e-8:floor=2.4
     elif x>-.5+1e-8:floor=min(12,math.ceil((x+.5-1e-8)/.24))*.2
    penetration=max(penetration,max(0,float(floor-v[1])))
  for arm in p['arms']:
   for a,b in [('shoulder','elbow'),('elbow','wrist')]:length_error=max(length_error,abs(np.linalg.norm(arm[b]-arm[a])-.34))
  if kind=='HOUSE' and d['contact']=='key':
   th=d['keyturn'];finger=p['arms'][0]['wrist']+V(.035*math.cos(th),.025+.035*math.sin(th),.035);grip_error=max(grip_error,float(np.linalg.norm(finger-d['keybow'])));contacts+=1
   if d['keytip'][2]>=0:keyinsert+=1
  if kind=='HOUSE':
   if d['contact'] in ['lever','inside lever']:grip_error=max(grip_error,float(np.linalg.norm(p['arms'][0]['wrist']-handle(t,d['contact']=='inside lever'))))
   if d['contact']=='bolt':grip_error=max(grip_error,float(np.linalg.norm(p['arms'][0]['wrist']-(doorpoint(t,u=.75,y=1.30,z=.065)+V(-.07*E(t,9.7,10),0,0)))))
   angle=door_angle(t)
   def local(q):return V(-math.cos(angle)*(q[0]-2.6)+math.sin(angle)*q[2],q[1],math.sin(angle)*(q[0]-2.6)+math.cos(angle)*q[2])
   arm=p['arms'][0]
   for aa,bb in [('shoulder','elbow'),('elbow','wrist')]:
    A=local(arm[aa]);B=local(arm[bb])
    if A[2]*B[2]<0:
     point=mix(A,B,-A[2]/(B[2]-A[2]));door_intersections+=int(0<point[0]<.9 and 0<point[1]<2.1)
  if kind=='STAIRS' and .4<=t<7.3:
   x=min(2.38,p['root'][0]+.02);actual=V(x,.85+(x+.5)*(.2/.24),1.94);rail_error=max(rail_error,float(np.linalg.norm(p['arms'][1]['wrist']-actual)))
  if kind=='WINDOW' and d['cloth_contact']:
   finger=p['arms'][0]['wrist']+V(.045,.015,-.025);surface=cloth(t,0,.35);grip_error=max(grip_error,float(np.linalg.norm(finger-surface)));contacts+=1
  previous=p
 reports[kind]={'frames':round(DURATIONS[kind]*30),'duration_s':DURATIONS[kind],'bone_length_error_m':length_error,'planted_sole_displacement_m':stance_drift,'max_sampled_shoe_vertex_penetration_m':penetration,'finger_prop_error_m':grip_error,'grip_frames':contacts,'door_arm_centerline_intersections':door_intersections,'hand_rail_error_m':rail_error,'foot_landings':plants,'root_start_m':root0.tolist(),'root_end_m':rootlast.tolist(),'root_distance_m':float(np.linalg.norm(rootlast-root0)),'key_max_degrees':math.degrees(keymax),'inserted_key_frames':keyinsert,'status':'numerical checks only; visual/user review required'}
print(json.dumps(reports,indent=2));(R/'reports/RIG_CONTACT_VALIDATION.json').write_text(json.dumps(reports,indent=2));assert all(x['door_arm_centerline_intersections']==0 and x['hand_rail_error_m']<1e-8 and x['bone_length_error_m']<1e-8 and x['planted_sole_displacement_m']<1e-8 and x['finger_prop_error_m']<1e-8 and x['max_sampled_shoe_vertex_penetration_m']<.002 for x in reports.values())
