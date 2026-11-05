from pathlib import Path
import json,numpy as np
from actions import *
R=Path(__file__).resolve().parents[1];report={}
for name,dur in DURATIONS.items():
 maxbone=0.;slip=0.;prev=None;contacterr=0.;ncontact=0
 for frame in range(round(dur*30)):
  t=frame/30;d=STATES[name](t)
  if name=='DRIVING':continue
  p=d['pose']
  for j,l in enumerate(p['legs']):
   for a,b in [('hip','knee'),('knee','ankle')]:maxbone=max(maxbone,abs(np.linalg.norm(l[a]-l[b])-.37))
   if prev and l['planted'] and prev['pose']['legs'][j]['planted']:slip=max(slip,float(np.linalg.norm(l['sole']-prev['pose']['legs'][j]['sole'])))
  for a in p['arms']:
   for aa,bb in [('shoulder','elbow'),('elbow','wrist')]:maxbone=max(maxbone,abs(np.linalg.norm(a[aa]-a[bb])-.34))
  if name=='BEDROOM' and d['cloth_contact']:
   err=np.linalg.norm(p['arms'][0]['wrist']+V(.045,.015,-.025)-d['grip']);contacterr=max(contacterr,float(err));ncontact+=1
  if name=='HOUSE' and d['contact'] in ['lever','inside lever']:
   target=contact.handle(d['contact_time'],d['contact']=='inside lever');contacterr=max(contacterr,float(np.linalg.norm(p['arms'][0]['wrist']-target)));ncontact+=1
  prev=d
 report[name]={'frames':round(dur*30),'maximum_bone_error_m':maxbone,'maximum_planted_sole_displacement_m':slip,'sampled_grip_error_m':contacterr,'contact_samples':ncontact,'constraint_checks_pass':maxbone<1e-9 and slip<1e-9 and contacterr<1e-9}
report['DRIVING'].update({'maximum_bone_error_m':None,'maximum_planted_sole_displacement_m':None,'sampled_grip_error_m':None,'articulated_pose_frames_checked':0,'scope':'Action-channel precheck only. Driver bones/grips are checked from rendered states by validate_rendered_states.py.'})
rows=DRIVE;deriv=max(abs((rows[i]['distance']-rows[i-1]['distance'])*30-rows[i]['speed_mps']) for i in range(1,len(rows)));wheel=max(abs(q['wheel_angle']*.30-q['distance']) for q in rows);gap=[q['gap'] for q in rows]
report['DRIVING'].update({'distance_speed_residual_mps':deriv,'wheel_travel_residual_m':wheel,'gap_range_m':[min(gap),max(gap)],'constraint_checks_pass':deriv<1e-9 and wheel<1e-9,'note':'Seated wheel/pedal contact is also inspected in the rendered insert. No full tyre or hand-volume simulation.'})
report['limits']='Constraints passing is not artistic approval. Silhouette, collision volume, proportions and material realism require visual review.'
(R/'reports/RIG_CHECKS.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));assert all(row['constraint_checks_pass'] for row in report.values() if isinstance(row,dict))
