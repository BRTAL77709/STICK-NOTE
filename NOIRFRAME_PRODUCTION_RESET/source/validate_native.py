"""Validate evaluated native joint/control samples, not just requested keyframes."""
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];versions={'A':'v11','B':'v11','C':'v13'};out={}
for k,v in versions.items():
 d=json.loads((R/f'reports/SHOT_{k}_{v}_rig-data.json').read_text());s=d['samples'];drift=[];yaw=[]
 for prev,now in zip(s,s[1:]):
  for j in range(2):
   if prev['planted'][j] and now['planted'][j]:
    drift.append(math.dist(prev['foot_control_world'][j],now['foot_control_world'][j]));yaw.append(abs(prev['foot_yaw'][j]-now['foot_yaw'][j]))
 # A has a moving support frame: road-world foot travel is expected, not sliding on cabin floor.
 lengths={name:[math.dist(x['joint_world_m'][name]['head'],x['joint_world_m'][name]['tail']) for x in s] for name in s[0]['joint_world_m']}
 row={'blend':f'blender/SHOT_{k}_{v}.blend','frames':d['frames'],'duration_s':d['duration'],'max_evaluated_IK_residual_m':d['max_residual_m'],'max_actual_prop_contact_error_m':max(x['actual_prop_contact_error_m'] or 0 for x in s),'max_bone_length_variation_m':max(max(a)-min(a) for a in lengths.values()),'stance_support':'moving car frame' if k=='A' else 'stationary world','max_consecutive_ground_stance_displacement_m':None if k=='A' else max(drift,default=0),'max_ground_stance_yaw_change_rad':None if k=='A' else max(yaw,default=0)}
 if k=='A':
  a=s[0]['prop_state'];b=s[-1]['prop_state'];row.update(car_travel_m=b['distance_m']-a['distance_m'],speed_start_mps=a['speed_mps'],speed_end_mps=b['speed_mps'],wheel_odometry_error_m=max(abs((q-a['wheel_rad'][j])*.33-(b['distance_m']-a['distance_m'])) for j,q in enumerate(b['wheel_rad'])),wheel_contact_support='Actual steering wheel local circle; body-pitch matrix applied to driver targets')
 if k=='B':row.update(max_door_open_degrees=math.degrees(max(x['prop_state']['door_hinge_rad'] for x in s)),key_inserted_frames=sum(bool(x['prop_state']['key_inserted']) for x in s))
 if k=='C':row.update(individual_riser_height_m=.2,risers=3,pelvis_rise_m=max(x['root'][2] for x in s)-s[0]['root'][2],fabric='Keyed deformed mesh; not physical cloth solver')
 row['contact_checks_pass']=row['max_evaluated_IK_residual_m']<.003 and row['max_actual_prop_contact_error_m']<.001 and (k=='A' or row['max_consecutive_ground_stance_displacement_m']<1e-6)
 out[k]=row
before=json.loads((R/'reports/preservation-before.json').read_text());missing=[];changed=[]
for p,h in before.items():
 f=R.parent/p
 if not f.is_file():missing.append(p)
 elif hashlib.sha256(f.read_bytes()).hexdigest()!=h:changed.append(p)
report={'shots':out,'preservation':{'files_checked':len(before),'missing':missing,'changed':changed},'limits':['IK residuals and fixed anchors do not prove convincing acting, silhouette, collision-free mesh surfaces, or approved style.','No blanket collision-simulation pass is claimed.','Ground stance samples validate foot controls, not every vertex of the shoe sole.'],'artistic_gate':'Requires actual rendered playback review; numeric success is insufficient.'}
(R/'reports/native-validation.json').write_text(json.dumps(report,indent=2));assert not missing and not changed;assert all(x['contact_checks_pass'] for x in out.values());print(json.dumps(report,indent=2))
