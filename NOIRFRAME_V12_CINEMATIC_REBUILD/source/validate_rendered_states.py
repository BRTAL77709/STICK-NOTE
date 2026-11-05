from pathlib import Path
import json,math,numpy as np
from actions import *
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'CURRENT_SHOTS.json').read_text());out={}
for k,v in rows.items():
 p=R/'reports'/(Path(v['final']).stem+'_STATE.json');data=json.loads(p.read_text());bone=0.;slip=0.;penetration=0.;hand=0.;contacts=0;prev=None;posecount=0;doorcross=0;seat=0;capmax=0.
 for d in data['state']:
  if 'pose' not in d:prev=None;continue
  pose=d['pose'];posecount+=1;u=d.get('contact_time',d['time'])
  for j,l in enumerate(pose['legs']):
   for aa,bb in [('hip','knee'),('knee','ankle')]:bone=max(bone,abs(np.linalg.norm(np.array(l[aa])-l[bb])-.37))
   if prev and l['planted'] and prev['legs'][j]['planted']:slip=max(slip,float(np.linalg.norm(np.array(l['sole'])-prev['legs'][j]['sole'])))
   if k!='DRIVING':
    co,si=math.cos(l['pitch']),math.sin(l['pitch'])
    for xx,yy in [(-.105,0),(.105,0),(.12,.035),(.045,.085),(-.08,.08)]:
     p=np.array(l['sole'])+V(xx*co-yy*si,xx*si+yy*co,0);floor=2.4 if k=='BEDROOM' else 0
     if k=='STAIRS' and p[0]>-.5+1e-8:floor=min(12,math.ceil((p[0]+.5-1e-8)/.24))*.2
     penetration=max(penetration,max(0,float(floor-p[1])))
  for a in pose['arms']:
   for aa,bb in [('shoulder','elbow'),('elbow','wrist')]:bone=max(bone,abs(np.linalg.norm(np.array(a[aa])-a[bb])-.34))
  if k=='STAIRS' and .4<=u<7.3:
   x=min(2.38,pose['root'][0]+.02);target=V(x,.85+(x+.5)*(.2/.24),1.94);hand=max(hand,float(np.linalg.norm(np.array(pose['arms'][1]['wrist'])-target)));contacts+=1
  if k=='DRIVING':
   angle=d['steer']*12;center=V(-.38,.79,.56)
   for j,a in enumerate([math.pi/6,5*math.pi/6]):
    target=center+V(.245*math.cos(a+angle),.245*math.sin(a+angle),-.07*math.sin(a+angle));hand=max(hand,float(np.linalg.norm(np.array(pose['arms'][j]['wrist'])-target)));contacts+=1
   seat=max(seat,abs(pose['root'][1]-.30),abs(pose['root'][2]+.02))
   yaw=pose['yaw'];half=61-13*abs(yaw);shift=15*yaw;ang=math.radians(pose['tilt']);start=V(-half-2,-10);joint=V(-shift*.35,-80);end=V(half+2,-11);hat=[]
   for a,b,c in [(start,V(-half-2,-77),joint),(joint,V(half,-77),end)]:
    for z in np.linspace(0,1,41):
     pt=(1-z)**2*a+2*z*(1-z)*b+z*z*c;hat.append(-(pt[0]*math.sin(ang)+pt[1]*math.cos(ang))*.26/61)
   capmax=max(capmax,pose['head'][1]+max(hat)+.006)
  if k=='BEDROOM' and d['cloth_contact']:hand=max(hand,float(np.linalg.norm(np.array(pose['arms'][0]['wrist'])+V(.045,.015,-.025)-contact.cloth(u))));contacts+=1
  if k=='HOUSE':
   if d['contact']=='key':
    th=d['keyturn'];finger=np.array(pose['arms'][0]['wrist'])+V(.035*math.cos(th),.025+.035*math.sin(th),.035);hand=max(hand,float(np.linalg.norm(finger-d['keybow'])));contacts+=1
   if d['contact'] in ['lever','inside lever']:hand=max(hand,float(np.linalg.norm(np.array(pose['arms'][0]['wrist'])-contact.handle(u,d['contact']=='inside lever'))));contacts+=1
   a=contact.door_angle(u)
   def local(q):return V(-math.cos(a)*(q[0]-2.6)+math.sin(a)*q[2],q[1],math.sin(a)*(q[0]-2.6)+math.cos(a)*q[2])
   ar=pose['arms'][0]
   for aa,bb in [('shoulder','elbow'),('elbow','wrist')]:
    A=local(ar[aa]);B=local(ar[bb])
    if A[2]*B[2]<0:
     q=mix(A,B,-A[2]/(B[2]-A[2]));doorcross+=int(0<q[0]<.9 and 0<q[1]<2.1)
  prev=pose
 out[k]={'evaluated_frames':data['frames'],'articulated_pose_frames':posecount,'max_bone_error_m':bone,'max_planted_sole_displacement_m':slip,'sampled_shoe_surface_penetration_m':penetration if k!='DRIVING' else None,'max_grip_error_m':hand,'grip_samples':contacts,'door_arm_centerline_crossings':doorcross if k=='HOUSE' else None,'seat_root_drift_m':seat if k=='DRIVING' else None,'cap_height_upper_bound_m':capmax if k=='DRIVING' else None,'interior_roof_y_m':1.46 if k=='DRIVING' else None,'bounded_checks_pass':bone<1e-9 and slip<1e-9 and penetration<.002 and hand<1e-9 and doorcross==0 and (k!='DRIVING' or capmax<1.46)}
(R/'reports/RENDERED_STATE_VALIDATION.json').write_text(json.dumps(out,indent=2,default=lambda x:x.item()));print(json.dumps(out,indent=2,default=lambda x:x.item()));assert all(q['bounded_checks_pass'] for q in out.values())
