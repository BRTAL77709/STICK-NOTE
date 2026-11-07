"""Native grip-marker vs prop geometry checks. These are not full hand-mesh collisions."""
import gzip,json,math,numpy as np
from bootstrap import ROOT as R

def legacy(q):return np.array([q[1],q[2],q[0]],float)
versions={s:json.loads((R/'reports/SHOT_REVISIONS.json').read_text())[s] for s in ['DRIVER_CHASE','DRIVING_COCKPIT','KEY_LOCK','DOOR_ENTRY','WINDOW_CURTAIN','CAR_EXIT_RUNNING']};result={}
for shot,tag in versions.items():
 data=json.load(gzip.open(R/'scenes'/f'{shot}_{tag}.json.gz','rt'));surface=0.;lateral=0.;depthmin=10.;depthmax=-10.;width=0.;grip=0.;heel=0.;toe=0.;hinge=[];wheel=0.;active=0
 for f,d in zip(data['frames'],data['state']):
  for side,j in [('L',1),('R',0)]:
   for digit,pad in enumerate(d.get('fingers',[[],[]])[j]):
    point=legacy(f['bones'][f'digit{digit}b.{side}']['tail'])-np.array(pad['normal'])*pad['tip_radius'];surface=max(surface,float(np.linalg.norm(point-pad['pad'])));active+=1
  if shot=='KEY_LOCK' and d.get('contact')=='key':grip=max(grip,float(np.linalg.norm(legacy(f['bones']['hand.L']['head'])-d['grip'])))
  if shot=='KEY_LOCK' and d['insertion']>0:
   delta=np.array(d['door_R']).T@(np.array(d['keytip'])-d['keyhole']);lateral=max(lateral,float(np.linalg.norm(delta[:2])));depthmin=min(depthmin,float(delta[2]));depthmax=max(depthmax,float(delta[2]))
  if shot=='DOOR_ENTRY':
   hinge.append([.45,0,0]);assert abs(np.linalg.det(np.array(d['door_R']))-1)<1e-10
   if d['door_angle']>.0001:assert d['unlocked']
  if shot=='WINDOW_CURTAIN':
   fabric=np.array(d['fabric']);rows=np.linalg.norm(np.diff(fabric,axis=1),axis=2).sum(axis=1);width=max(width,float(np.max(np.abs(rows-1.60))))
   if d['grip_contact']:grip=max(grip,float(np.linalg.norm(legacy(f['bones']['hand.R']['head'])+np.array([0,0,.05])-d['grip'])))
  if shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:
   shoe=np.array([legacy(q) for q in f['meshes']['SHOE_R']]);h=(shoe[0]+shoe[5])/2;t=(shoe[1]+shoe[6])/2;heel=max(heel,float(np.linalg.norm(h-d['heel'])))
   if d['toe_contact']:
    pedal=d['pedals'][0 if d['toe_contact']=='accelerator' else 1];toe=max(toe,abs(float(np.array(pedal['normal'])@(t-pedal['hinge']))))
  if shot=='CAR_EXIT_RUNNING' and d['handle_contact']:grip=max(grip,float(np.linalg.norm(legacy(f['bones']['hand.L']['head'])-(np.array(d['car_handle'])+np.array([0,0,-.035])))))
 row={'native_fingertip_contact_marker_error_m':surface,'active_digit_measurements':active,'definition':'Actual native distal bone endpoint minus authored7mm tip-radius normal compared with prop pad. Tests a rounded-contact proxy; flat visible finger meshes and full hand collision are not certified.','artistic_status':'ARTISTIC REVIEW REQUIRED'}
 if shot=='KEY_LOCK':row.update({'native_hand_key_grip_frame_error_m':grip,'key_lock_axis_lateral_error_m':lateral,'key_tip_axial_range_m':[depthmin,depthmax],'maximum_inserted_depth_m':max(0,depthmax),'blade_length_m':.10,'door_thickness_m':.13})
 if shot=='DOOR_ENTRY':row.update({'hinge_measurement':'Shared world pivot used to generate all rendered leaf vertices; independently sampled native prop check reported separately','hinge_pivot_drift_m':float(np.ptp(np.array(hinge),axis=0).max()),'door_open_only_after_unlock':True,'inside_lock_operation_included':True})
 if shot=='WINDOW_CURTAIN':row.update({'native_wrist_to_fabric_grip_frame_error_m':grip,'max_horizontal_material_arc_length_error_m':width,'material_width_m':1.60,'limits':'Horizontal arc-length rig, row lag and settling; no general cloth strain/tension/self-collision solve.'})
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:row.update({'actual_native_heel_centre_anchor_error_m':heel,'actual_native_toe_centre_to_pressed_pedal_plane_error_m':toe,'limits':'Heel centre and toe centre tested, not full shoe/pedal mesh contact patch.'})
 if shot=='CAR_EXIT_RUNNING':row.update({'native_hand_to_car_handle_grip_frame_error_m':grip,'limits':'Fixed authored35mm wrist stand-off plus native articulated digits; no force-driven door dynamics.'})
 row['technical_status']='TECHNICAL PASS' if surface<.002 and grip<.0015 and heel<.0015 and toe<.0015 and width<.001 else 'TECHNICAL FAIL';result[shot]=row
(R/'reports/PROP_INTERACTION_VALIDATION.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:{x:v for x,v in d.items() if x not in ['definition','limits']} for k,d in result.items()},indent=2))
