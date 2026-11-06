"""Frame-by-frame bounded checks, intentionally separate from artistic acceptance."""
from pathlib import Path
import json,math,csv,hashlib,gzip
import numpy as np
from contact_rig import *
from shots import SHOTS
import stair_test,key_test,vehicle_dynamics as vd
R=Path(__file__).resolve().parents[1]
def check(name,states):
 report={'frames':len(states)};rows=[];bone=slip=shoe_pen=body_pen=paderr=anglejump=posjump=clotherr=0.;prev=None;rootmin=10;contacts=0;properr=0.;axiserr=0.;wristdetach=0.
 for f,d in enumerate(states):
  p=d['pose'];rootmin=min(rootmin,p['root'][1]);rr={'frame':f,'time':f/30,'phase':d['phase'],'root_x':p['root'][0],'root_y':p['root'][1],'root_z':p['root'][2]}
  for j,l in enumerate(p['legs']):
   for aa,bb in [('hip','knee'),('knee','ankle')]:bone=max(bone,abs(np.linalg.norm(np.array(l[aa])-l[bb])-.37))
   for q in ['hip','knee','ankle']:
    if prev:posjump=max(posjump,float(np.linalg.norm(np.array(l[q])-prev['legs'][j][q])))
   if l['planted'] and prev and prev['legs'][j]['planted']:
    old=prev['legs'][j];F=V(math.sin(l['heading']),0,math.cos(l['heading']));toe=np.array(l['shoe_origin'])+F*(.105*math.cos(l['pitch']))+V(0,.105*math.sin(l['pitch']),0) if 'shoe_origin' in l else np.array(l['sole']);F0=V(math.sin(old['heading']),0,math.cos(old['heading']));oldtoe=np.array(old['shoe_origin'])+F0*(.105*math.cos(old['pitch']))+V(0,.105*math.sin(old['pitch']),0) if 'shoe_origin' in old else np.array(old['sole']);slip=max(slip,float(np.linalg.norm(toe-oldtoe)))
   rr[f'foot{j}_planted']=l['planted'];rr[f'foot{j}_x']=l['sole'][0];rr[f'foot{j}_y']=l['sole'][1];rr[f'foot{j}_z']=l['sole'][2]
   if name=='STAIRS':
    a=l['pitch'];F=V(1,0,0);o=np.array(l['shoe_origin'])
    for x,y in [(-.105,0),(.105,0),(.12,.035),(.045,.085),(-.08,.08)]:
     v=o+F*(x*math.cos(a)-y*math.sin(a))+V(0,x*math.sin(a)+y*math.cos(a),0);shoe_pen=max(shoe_pen,stair_test.floor_y(v[0]-1e-8)-v[1])
    for aa,bb in [('hip','knee'),('knee','ankle')]:
     for u in np.linspace(0,1,21):
      q=np.array(l[aa])+(np.array(l[bb])-l[aa])*u
      if -.36<q[2]<.36:body_pen=max(body_pen,stair_test.floor_y(q[0])-q[1]+.03)
  for a in p['arms']:
   for aa,bb in [('shoulder','elbow'),('elbow','wrist')]:bone=max(bone,abs(np.linalg.norm(np.array(a[aa])-a[bb])-.34))
  for hand_index,group in enumerate(d.get('fingers',[])):
   for g in group:
    wristdetach=max(wristdetach,float(np.linalg.norm(np.array(g['base'])-p['arms'][hand_index]['wrist'])))
    for aa,bb in [('base','joint'),('joint','tip_center')]:bone=max(bone,abs(np.linalg.norm(np.array(g[aa])-g[bb])-.034))
    paderr=max(paderr,float(np.linalg.norm(np.array(g['tip_center'])-np.array(g['normal'])*.007-g['pad'])))
  if name=='KEY_DOOR':
   if d['contact']=='key':
    K=np.array(d['key_R'])
    for g in d['fingers'][1]:
     q=K.T@(np.array(g['pad'])-d['keybow']);properr=max(properr,abs((q[0]/.044)**2+(q[1]/.027)**2-1)*.044,abs(q[2]+.004))
   if d['contact']=='handle':
    a=np.array(d['spindle']);b=np.array(d['handle_end']);u=b-a
    for g in d['fingers'][1]:
     q=np.array(g['pad']);nearest=a+u*np.clip(np.dot(q-a,u)/np.dot(u,u),0,1);properr=max(properr,abs(np.linalg.norm(q-nearest)-.011))
   if 2.0<=d['time']<=3.92:
    axis=np.array(d['door_R'])@V(0,0,1);delta=np.array(d['keytip'])-d['keyhole'];axiserr=max(axiserr,float(np.linalg.norm(delta-axis*np.dot(axis,delta))))
   # Body spheres/capsules against the moving leaf, excluding intended hand contacts.
   DR=np.array(d['door_R'])
   for q,rad in [(p['root'],.13),(p['shoulder'],.16),(p['head'],.26)]:
    v=DR.T@(np.array(q)-key_test.HINGE);dx=max(-.9-v[0],0,v[0]);dy=max(-v[1],0,v[1]-2.1);dz=max(abs(v[2])-.065,0);dist=math.sqrt(dx*dx+dy*dy+dz*dz);body_pen=max(body_pen,rad-dist)
   rr.update(key_tip_x=d['keytip'][0],key_tip_y=d['keytip'][1],key_tip_z=d['keytip'][2],insertion=d['insertion'],key_turn=d['keyturn'],door_angle=d['door_angle'],grip=d['contact'])
  if name=='CURTAIN':
   mesh=np.array(d['fabric']);lens=np.linalg.norm(np.diff(mesh,axis=1),axis=2).sum(axis=1);clotherr=max(clotherr,float(abs(lens-d['fabric_material_width']).max()));rr['grip_contact']=d['grip_contact'];rr['curtain_edge_x']=mesh[5,-1,0]
   if d['grip_contact']:
    for g in d['fingers'][0]:paderr=max(paderr,abs(np.array(g['pad'])[0]-mesh[5,-1,0]),abs(np.array(g['pad'])[2]-mesh[5,-1,2]))
  if name in ['STEERING','CHASE']:
   M=np.array(d['wheel_R']);ctr=np.array(d['wheel_center'])
   for group in d['fingers']:
    for g in group:
     q=M.T@(np.array(g['pad'])-ctr);properr=max(properr,abs(np.linalg.norm(q[:2])-.245),abs(q[2]+.015))
  if name in ['STEERING','CHASE']:rr.update(speed=d['speed'],steer=d['steer'],gap=d['gap'],world_x=d['position'][0],world_z=d['position'][2],brake=d['brake'])
  rows.append(rr);prev=p
 report.update(max_bone_error_m=bone,max_planted_toe_drift_m=slip,max_sampled_shoe_penetration_m=max(0,shoe_pen),max_sampled_body_penetration_m=max(0,body_pen),finger_pad_model_error_m=paderr,finger_wrist_detachment_m=wristdetach,independent_prop_surface_error_m=properr,key_axis_alignment_error_m=axiserr,max_joint_frame_displacement_m=posjump,min_pelvis_y_m=rootmin,fabric_horizontal_arc_length_error_m=clotherr)
 if name=='STAIRS':report.update(COM_rise_m=states[-1]['com'][1]-states[0]['com'][1],treads_reached=sorted(set(x for d in states for x in d['tread_indices'] if x is not None)))
 if name in ['STEERING','CHASE']:report['gap_start_end_m']=[states[0]['gap'],states[-1]['gap']]
 report['geometry_status']='PASS' if bone<1e-7 and slip<1e-6 and shoe_pen<.002 and body_pen<.002 and paderr<.001 and wristdetach<.001 and properr<.001 and axiserr<.001 and clotherr<.001 else 'FAIL';report['artistic_status']='NEEDS REVIEW'
 with (R/'reports'/f'{name}_FRAME_CONTACTS.csv').open('w') as fp:
  writer=csv.DictWriter(fp,fieldnames=sorted(set().union(*(q.keys() for q in rows))));writer.writeheader();writer.writerows(rows)
 return report

def main():
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--tag',default='LIVE');p.add_argument('--width',default=1080,type=int);args=p.parse_args();reports={}
 for name,(fn,dur) in SHOTS.items():
  if args.tag=='LIVE':states=[fn(i/30)[1] for i in range(round(dur*30))]
  else:
   p=R/'reports'/((Path(json.loads((R/'CURRENT_SHOTS.json').read_text())[name]['final']).stem+'_STATE.json.gz') if args.tag=='FINAL' else f'{name}_M03_{args.tag}_{args.width}_STATE.json.gz')
   states=json.load(gzip.open(p,'rt'))['state']
  reports[name]=check(name,states)
 (R/'reports'/f'CONTACT_QA_{args.tag}.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
