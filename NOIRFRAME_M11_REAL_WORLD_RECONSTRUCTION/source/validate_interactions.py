"""Measurements from evaluated native bones and shoe vertices, with explicit sampling limits."""
from pathlib import Path
import json,gzip,numpy as np,math,argparse
from bootstrap import ROOT as R
B=np.array([[0,0,1],[1,0,0],[0,1,0]],float)
def run(shot,tag):
 d=json.load(gzip.open(R/'scenes'/f'{shot}_{tag}.json.gz','rt'));frames=d['frames'];wrist=legerr=finger=length=jointgap=drift=ground=0.;anchors={};root=[];rows=[]
 for i,f in enumerate(frames):
  st=d['state'][i];p=st['pose'];root.append(f['bones']['root']['head'])
  for s,j in [('L',1),('R',0)]:
   b=f['bones'];wrist=max(wrist,float(np.linalg.norm(np.array(b['forearm.'+s]['tail'])-f['targets'][s])));legerr=max(legerr,float(np.linalg.norm(np.array(b['shin.'+s]['tail'])-B@np.array(p['legs'][j]['ankle']))))
   for pref,want in [('thigh.',.37),('shin.',.37),('upper_arm.',.34),('forearm.',.34),('digit0a.',.034),('digit0b.',.034),('digit1a.',.034),('digit1b.',.034)]:length=max(length,abs(float(np.linalg.norm(np.array(b[pref+s]['tail'])-b[pref+s]['head']))-want))
   for x,y in [('thigh.','shin.'),('shin.','foot.'),('upper_arm.','forearm.'),('forearm.','hand.'),('digit0a.','digit0b.'),('digit1a.','digit1b.')]:jointgap=max(jointgap,float(np.linalg.norm(np.array(b[x+s]['tail'])-b[y+s]['head'])))
   for k in range(2):
    if st.get('fingers') and len(st['fingers'][j])>k:finger=max(finger,float(np.linalg.norm(np.array(b[f'digit{k}b.{s}']['tail'])-f['finger_targets'][s][k])))
   foot=p['legs'][j];vv=np.array(f['meshes']['SHOE_'+s]);planted=foot['planted'];ids=[1,6] if foot.get('contact_mode')=='toe' else [0,1,5,6]
   if planted and shot not in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:
    if s not in anchors:anchors[s]=vv.copy()
    drift=max(drift,float(np.linalg.norm(vv[ids]-anchors[s][ids],axis=1).max()));floor=float(foot['sole'][1]);ground=max(ground,float(np.abs(vv[ids,2]-floor).max()))
   else:anchors.pop(s,None)
  rows.append({'time':f['time'],'wrist_target_error_m':wrist,'limb_length_variation_m':length})
 root=np.array(root);delta=np.diff(root,axis=0);acc=np.diff(root,n=2,axis=0)*900;result={'shot':shot,'sampling':'Native evaluated meshes/bones at 30Hz; dense joint cache 60Hz supplied; not continuous collision certification','max_native_wrist_IK_error_m':wrist,'max_native_leg_IK_error_m':legerr,'max_native_finger_target_error_m':finger,'max_limb_length_variation_m':length,'max_connected_joint_gap_m':jointgap,'max_stance_mesh_drift_m':drift if shot not in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC'] else None,'max_foot_ground_distance_m':ground if shot not in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC'] else None,'max_root_frame_displacement_m':float(np.linalg.norm(delta,axis=1).max()),'peak_root_acceleration_m_s2':float(np.linalg.norm(acc,axis=1).max()),'root_interpolation':'Native keyed location curves are piecewise linear and position-continuous; frame displacement is reported separately, not labelled a discontinuity','tolerances':{'native_IK_error_m':.0015,'finger_error_m':.002,'limb_length_m':.0001,'joint_gap_m':.0001,'ground_contact_m':.0015,'stance_drift_m':.0015},'artistic_status':'ARTISTIC REVIEW REQUIRED'}
 result['technical_status']='TECHNICAL PASS' if wrist<.0015 and legerr<.0015 and finger<.002 and length<.0001 and jointgap<.0001 and (shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC'] or (drift<.0015 and ground<.0015)) else 'TECHNICAL FAIL';(R/'reports'/f'{shot}_{tag}_CONTACTS.json').write_text(json.dumps(result,indent=2));print(shot,result['technical_status'],'wrist',round(wrist*1000,3),'leg',round(legerr*1000,3),'finger',round(finger*1000,3),'drift',round(drift*1000,3),'ground',round(ground*1000,3));return result
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--shot',required=True);p.add_argument('--tag',default='R02');a=p.parse_args();run(a.shot,a.tag)
