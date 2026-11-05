"""Bounded geometry/contact checks. These are not an artistic approval."""
from pathlib import Path
import sys,json,math,csv
import numpy as np
from contact_rig import V,com
R=Path(__file__).resolve().parents[1]
def arr(q):return np.asarray(q,float)
def point_segment(p,a,b):
 u=b-a;return float(np.linalg.norm(p-(a+u*np.clip(np.dot(p-a,u)/np.dot(u,u),0,1))))
def hull(points):
 ps=sorted(set(tuple(x) for x in points))
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 l=[]
 for p in ps:
  while len(l)>1 and cross(l[-2],l[-1],p)<=0:l.pop()
  l.append(p)
 u=[]
 for p in reversed(ps):
  while len(u)>1 and cross(u[-2],u[-1],p)<=0:u.pop()
  u.append(p)
 return l[:-1]+u[:-1]
def outside(p,poly):
 return max(0,max(-((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))/max(1e-8,np.linalg.norm(arr(b)-a)) for a,b in zip(poly,poly[1:]+poly[:1])))
def check(k,states):
 bone=0.;slip=0.;pen=0.;paderr=0.;handdrift=0.;comerr=0.;supporterr=0.;leverpen=0.;heelerr=0.;toeerr=0.;meshpen=0.;groundpen=0.;proj=0.;prev=None;firstpads=None;csvrows=[]
 for i,d in enumerate(states):
  p=d['pose'];pts=[];contacts=[]
  for j,l in enumerate(p['legs']):
   for a,b in [('hip','knee'),('knee','ankle')]:bone=max(bone,abs(np.linalg.norm(arr(l[a])-l[b])-.37))
   if k=='STAIR_CONTACT':
    a=l['pitch'];F=V(math.sin(l['heading']),0,math.cos(l['heading']));o=arr(l['shoe_origin']);toe=o+F*(.105*math.cos(a))+V(0,.105*math.sin(a),0)
    if prev and l['planted'] and prev['legs'][j]['planted']:
     old=prev['legs'][j];b=old['pitch'];oldtoe=arr(old['shoe_origin'])+F*(.105*math.cos(b))+V(0,.105*math.sin(b),0);slip=max(slip,float(np.linalg.norm(toe-oldtoe)))
    for x,y in [(-.105,0),(.105,0),(.12,.035),(.045,.085),(-.08,.08)]:
     v=o+F*(x*math.cos(a)-y*math.sin(a))+V(0,x*math.sin(a)+y*math.cos(a),0);floor=min(12,math.ceil((v[0]+.5-1e-8)/.24))*.2;pen=max(pen,floor-v[1])
    if l['planted']:
     xs=[.105] if l['contact_mode']=='toe' else [-.105,.105]
     for x in xs:
      for z in [-.045,.045]:pts.append((l['sole'][0]+x,l['sole'][2]+z))
   elif k=='STEERING_TURN':
    sole=arr(l['sole_mesh']);groundpen=max(groundpen,.04-float(sole[:,:,1].min()));heelerr=max(heelerr,float(np.linalg.norm(arr(l['heel'])-([-.32,.04,.27] if j==0 else [-.60,.04,.17]))))
  for a in p['arms']:
   for aa,bb in [('shoulder','elbow'),('elbow','wrist')]:bone=max(bone,abs(np.linalg.norm(arr(a[aa])-a[bb])-.34))
  for group in d.get('fingers',[]):
   for f in group:
    for aa,bb in [('base','joint'),('joint','tip_center')]:bone=max(bone,abs(np.linalg.norm(arr(f[aa])-f[bb])-.034))
    paderr=max(paderr,float(np.linalg.norm(arr(f['tip_center'])-arr(f['normal'])*f['tip_radius']-f['pad'])))
  if k=='STAIR_CONTACT':
   comerr=max(comerr,float(np.linalg.norm((arr(d['com'])-d['desired_com'])[[0,2]])));supporterr=max(supporterr,outside(arr(d['support_target'])[[0,2]],hull(pts)))
   if d['rail_contact']:
    a=V(-.5,.85,1.94);b=V(2.38,3.25,1.94)
    for f in d['fingers'][1]:paderr=max(paderr,abs(point_segment(arr(f['pad']),a,b)-.0225))
  if k=='KEY_HANDLE':
   K=arr(d['key_R']);b=arr(d['keybow']);loc=[K.T@(arr(f['pad'])-b) for f in d['fingers'][0]]
   if firstpads is None:firstpads=loc
   handdrift=max(handdrift,max(float(np.linalg.norm(a-b)) for a,b in zip(loc,firstpads)))
   for q in loc:paderr=max(paderr,abs((q[0]/.044)**2+(q[1]/.027)**2-1)*.044,abs(q[2]+.004))
   if d['handle_grip']:
    a=arr(d['spindle']);b=arr(d['handle_end'])
    for f in d['fingers'][1]:
     paderr=max(paderr,abs(point_segment(arr(f['pad']),a,b)-.011))
     for aa,bb in [('base','joint'),('joint','tip_center')]:
      for u in np.linspace(0,1,31):leverpen=max(leverpen,.018-point_segment(arr(f[aa])+(arr(f[bb])-f[aa])*u,a,b))
  if k=='STEERING_TURN':
   M=arr(d['wheel_R']);ctr=arr(d['wheel_center']);local=[M.T@(arr(f['pad'])-ctr) for g in d['fingers'] for f in g]
   if firstpads is None:firstpads=local
   handdrift=max(handdrift,max(float(np.linalg.norm(a-b)) for a,b in zip(local,firstpads)))
   for q in local:paderr=max(paderr,abs(np.linalg.norm(q[:2])-.245),abs(q[2]+.015))
   if d['toe_contact']:
    ped=d['pedals'][0 if d['toe_contact']=='accelerator' else 1];n=arr(ped['normal']);q=arr(ped['hinge']);toeerr=max(toeerr,abs(float((arr(d['toe'])-q)@n)));meshpen=max(meshpen,-float(np.min((arr(p['legs'][0]['sole_mesh'])-q)@n)))
   proj=max(proj,d.get('camera_projection_agreement_px',0))
  prev=p;csvrows.append({'frame':i,'time_s':i/30,'phase':d['phase'],'pelvis_x':p['root'][0],'pelvis_y':p['root'][1],'pelvis_z':p['root'][2],'foot0':p['legs'][0].get('contact_mode',d.get('toe_contact','flat')),'foot1':p['legs'][1].get('contact_mode','flat'),'speed_mps':d.get('speed',''),'steer_radians':d.get('steer',''),'gap_arc_m':d.get('gap',''),'gap_euclidean_m':float(np.linalg.norm(arr(d['position'])-d['pursuer_position'])) if 'position' in d else ''})
 with (R/'reports'/f'{k}_FRAME_CONTACTS.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=csvrows[0].keys());w.writeheader();w.writerows(csvrows)
 result={'frames':len(states),'max_bone_length_error_m':bone,'toe_anchor_drift_while_planted_m':slip,'shoe_tread_penetration_m':max(0,pen),'finger_skin_contact_model_error_m':paderr,'hand_prop_local_slip_m':handdrift,'COM_plan_tracking_error_m':comerr,'support_pressure_outside_polygon_m':supporterr,'sampled_finger_lever_overlap_m':max(0,leverpen),'heel_floor_anchor_drift_m':heelerr,'toe_pedal_plane_error_m':toeerr,'sampled_pedal_sole_penetration_m':max(0,meshpen),'foot_floor_penetration_m':max(0,groundpen),'same_state_camera_projection_error_px':proj}
 if k=='STAIR_CONTACT':result['COM_rise_m']=states[-1]['com'][1]-states[0]['com'][1];result['pelvis_travel_m']=float(np.linalg.norm(arr(states[-1]['pose']['root'])-states[0]['pose']['root']));result['ends_on_upper_floor']=all(l['sole'][1]==2.4 and l['sole'][0]>2.38 for l in states[-1]['pose']['legs'])
 if k=='STEERING_TURN':result['actual_gap_start_end_m']=[float(np.linalg.norm(arr(s['position'])-s['pursuer_position'])) for s in [states[0],states[-1]]]
 result['bounded_checks_pass']=bool(bone<1e-8 and slip<1e-8 and pen<.0001 and paderr<.001 and handdrift<1e-8 and comerr<.001 and supporterr<.001 and leverpen<.001 and heelerr<1e-8 and toeerr<1e-8 and meshpen<.0001 and groundpen<.0001 and proj<1e-6)
 return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--tag',default='M01');p.add_argument('--width',default=1080,type=int);p.add_argument('--live',action='store_true');a=p.parse_args();out={}
 for k,dur in [('STAIR_CONTACT',3),('KEY_HANDLE',3),('STEERING_TURN',4)]:
  if a.live:
   from shots import SHOTS
   states=[SHOTS[k][0](f/30)[1] for f in range(dur*30)]
  else:states=json.loads((R/'reports'/f'{k}_{dur}s_{a.tag}_{a.width}_STATE.json').read_text())['state']
  out[k]=check(k,states)
 (R/'reports'/f'CONTACT_VALIDATION_{a.tag}.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert all(q['bounded_checks_pass'] for q in out.values())
