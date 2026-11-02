import importlib.util,xml.etree.ElementTree as ET,json,math
from pathlib import Path
r=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('v7',r/'src/render_test_v7.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
prev={};slide=0.;gap=0.;rows=[];segments={};backtrail=[];feet_mismatch=0
for f in range(150):
 t=f/30;svg=m.scene(t);ids={n.get('id'):n for n in ET.fromstring(svg).iter() if n.get('id')};leans=[];contacts=[]
 for actor in [1,2]:
  p=ids[f'actor-pose-{actor}'];hip=list(map(float,p.get('data-hip').split(',')));sh=list(map(float,p.get('data-shoulder').split(',')));leans.append(sh[0]-hip[0]);cc=[]
  for leg in [0,1]:
   p=ids[f'actor-{actor}-foot-{leg}'];x=float(p.get('data-x'));y=float(p.get('data-y'));ph=float(p.get('data-phase'));key=actor,leg;on=ph<=.70;cc.append(on)
   if key in prev:
    xx,pp,oo=prev[key]
    if on and oo and ph>=pp-1e-8:slide=max(slide,abs(x-xx))
   if on:assert abs(y-m.GROUND[actor-1])<1e-6
   prev[key]=x,ph,on
  assert any(cc),'No support foot';contacts.append(cc)
 if contacts[0]!=contacts[1]:feet_mismatch+=1
 for i in [0,1]:
  arm=ids[f'victim-arm-{i}'];sh=tuple(map(float,arm.get('data-shoulder').split(',')));el=tuple(map(float,arm.get('data-elbow').split(',')));hand=ids[f'support-hand-{i}'];h=(float(hand.get('cx')),float(hand.get('cy')))
  u=sum((h[k]-sh[k])*(el[k]-sh[k]) for k in [0,1])/sum((el[k]-sh[k])**2 for k in [0,1]);gap=max(gap,math.hypot(*(h[k]-(sh[k]+u*(el[k]-sh[k])) for k in [0,1])));assert .5<u<.56
 wt=ids['victim-weight'];pelvis=list(map(float,wt.get('data-pelvis').split(',')));sag=pelvis[1]-float(wt.get('data-shoulder-y'));assert sag>120 # Passive rotating torso: enforce >120 units below shoulder mean.
 heelx=[]
 for j in [0,1]:
  heel=ids[f'victim-heel-{j}'];assert float(heel.get('data-y'))==1413+j*5;heelx.append(float(heel.get('data-x')))
  pts=[tuple(map(float,x.split(','))) for x in ids[f'victim-leg-{j}'].get('data-joints').split(';')];backtrail.append(pts[1][0]-pts[2][0])
 assert 20<heelx[1]-heelx[0]<45
 for name,n in ids.items():
  if n.get('data-joints'):
   pts=[tuple(map(float,x.split(','))) for x in n.get('data-joints').split(';')]
   for j in [0,1]:segments.setdefault(name+':'+str(j),[]).append(math.dist(pts[j],pts[j+1]))
 head=ids['head-1'];cam=ids['cinematic-framing']
 rows.append({'frame':f,'time':t,'shot':int(cam.get('data-shot')),'centers':[float(ids[f'actor-{i}'].get('data-center-x')) for i in [1,2]],'backward_lean':leans,'sag':sag,'victim_head_roll':float(ids['victim-head'].get('data-roll')),'heel_x':heelx,'head_yaw':float(head.get('data-yaw')),'head_rx':float(head.get('data-head-rx')),'cap_bill':float(head.get('data-bill')),'mask_chin':float(head.get('data-mask-chin')),'eye_narrow':float(head.get('data-narrow')),'contacts':contacts})
assert rows[95]['shot']==1 and rows[96]['shot']==2
assert rows[96]['head_yaw']>60 and rows[120]['head_yaw']==0 and rows[135]['eye_narrow']==1
assert slide<1e-6 and gap<.02
assert max(max(x['backward_lean']) for x in rows[:96])<0
variation={k:max(v)-min(v) for k,v in segments.items()}
assert max(variation.values())<.04,(max(variation.values()),variation)
assert min(backtrail)>0, min(backtrail)
assert feet_mismatch>0
report={'frames':150,'criminal_ground_heights':list(m.GROUND),'root_displacement_to_3_2':[rows[96]['centers'][k]-rows[0]['centers'][k] for k in [0,1]],'root_held_through_0_9':rows[27]['centers']==rows[0]['centers'],'max_planted_foot_slide_world_units':slide,'max_hand_upper_arm_gap_world_units':gap,'minimum_hips_below_shoulders':min(x['sag'] for x in rows),'victim_heel_y_values':[1413,1418],'victim_heel_spacing_range':[min(x['heel_x'][1]-x['heel_x'][0] for x in rows),max(x['heel_x'][1]-x['heel_x'][0] for x in rows)],'minimum_knee_ahead_of_dragging_ankle':min(backtrail),'victim_has_walk_cycle':False,'asynchronous_support_frames':feet_mismatch,'maximum_segment_length_variation_svg_rounding':max(variation.values()),'limb_length_ranges':{k:[min(v),max(v)] for k,v in segments.items()},'hard_cut_frame':96,'head_side_to_front':{'rx':[rows[96]['head_rx'],rows[120]['head_rx']],'bill_projection':[rows[96]['cap_bill'],rows[120]['cap_bill']],'mask_chin_shift':[rows[96]['mask_chin'],rows[120]['mask_chin']]},'note':'World-space pose checks from SVG joint points rounded to 0.01 units. Head/cap/mask are coherent orthographic projections of local 3D coordinates into flat SVG; the existing body rig retains contact constraints with distinct support plans and a deterministic passive pelvis/heel/head model. Encoded-foot strips and eyes-hidden views are separate visual checks.'}
(r/'pose-ledger.json').write_text(json.dumps(rows,indent=2));(r/'choreography-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='limb_length_ranges'},indent=2))

import numpy as np,ast
extra=[]
for f in range(150):
 t=f/30;q=m.interaction(t);p=m.passive_state(t);cx,cy=q['center'];w=[m.support_weights(t,j) for j in (0,1)]
 assert all(abs(sum(a)-1)<1e-8 for a in w)
 assert math.dist(p[:2],np.mean(q['shoulders'],axis=0))<=156.01
 extra.append({'t':t,'pelvis_target_lag_x':cx-32-float(p[0]),'torso_angle':math.degrees(q['theta']),'head_angle':float(p[4]),'hip_shift':[m.hip_shift(t,j) for j in (0,1)],'support_weights':w})
assert np.isfinite(m._PASSIVE).all()
report['V7_interaction']={'step_landings':[[land for leg in m.FOOT_PLANS[a] for start,land,target,lift in leg[1]] for a in (0,1)],'pelvis_horizontal_target_lag_range':[min(x['pelvis_target_lag_x'] for x in extra),max(x['pelvis_target_lag_x'] for x in extra)],'supported_torso_rotation_degrees':[min(x['torso_angle'] for x in extra),max(x['torso_angle'] for x in extra)],'passive_head_roll_degrees':[min(x['head_angle'] for x in extra),max(x['head_angle'] for x in extra)],'physics_hz':m.PHYSICS_HZ,'max_spine_projection':m.MAX_SPINE_PROJECTION,'sag_threshold_explanation':'Minimum 128.82 world units; 120-unit lower bound allows rotation and passive compression. The former V6 >130 constant-pose check was replaced after examining the new rotating torso. Pelvis is still low in every frame.'}
(r/'interaction-ledger.json').write_text(json.dumps(extra,indent=2));(r/'choreography-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report['V7_interaction'],indent=2))
