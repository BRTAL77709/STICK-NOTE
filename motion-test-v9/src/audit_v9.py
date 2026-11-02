"""All-frame contact, continuity and non-negotiable action-order checks."""
from pathlib import Path
import math,json,ast,xml.etree.ElementTree as E
import render_test_v9 as m
r=Path(__file__).resolve().parents[1];rows=[];previous={};slide=0.;reach=0.;bone={};closing_gap=0.;markers=[]
for f in range(300):
 t=f/30;ps=[m.actor_pose(t,i) for i in (0,1)];v=m.victim_pose(t);hands=m.hand_targets(t,ps,v);svg=m.scene(t);ids={n.get('id'):n for n in E.fromstring(svg).iter() if n.get('id')}
 for i,p in enumerate(ps):
  assert any(on for ft,on,u in p['feet'])
  for j,(ft,on,u) in enumerate(p['feet']):
   key=i,j
   if key in previous and on and previous[key][1]:slide=max(slide,math.dist(ft,previous[key][0]))
   if on:assert ft[1]==m.GROUND[i]
   previous[key]=ft,on
  for j in (0,1):
   sg=(1 if i==0 else -1)*(1 if j==0 else -1);a=m.add(p['shoulder'],(p['side'][0]*35*sg,p['side'][1]*35*sg+12));reach=max(reach,math.dist(a,hands[i][j]));assert math.dist(a,hands[i][j])<=177.02
 for name,n in ids.items():
  if n.get('data-joints'):
   pts=[tuple(map(float,p.split(','))) for p in n.get('data-joints').split(';')];sc=v['scale'] if name.startswith('victim') else 1.
   for j in (0,1):bone.setdefault(name+':'+str(j),[]).append(math.dist(pts[j],pts[j+1])/sc)
 if 6.95<=t<=7.5:closing_gap=max(closing_gap,math.dist(hands[1][0],m.lid_contact(t)))
 yaw=float(ids['head-1'].get('data-yaw'));narrow=float(ids['head-1'].get('data-narrow'))
 if t<8:assert yaw==72 and narrow==0
 if t>=8:assert m.trunk_angle(t)==0
 if t<9.2:assert narrow==0
 markers.append([v['S'],v['P'],v['neck']]+v['knees']+v['feet'])
 rows.append({'frame':f,'time':t,'state':m.state_at(t),'lid_angle':m.trunk_angle(t),'head_yaw':yaw,'eye_narrow':narrow,'victim_shoulder':v['S'],'victim_pelvis':v['P'],'victim_feet':v['feet'],'depth':v['depth'],'hands':hands,'criminal_hips':[p['hip'] for p in ps]})
assert slide==0 and closing_gap<1e-8
assert m.trunk_angle(7.5)==0 and m.trunk_angle(7.49)>0
assert m.victim_pose(6.2)['depth']==1
assert rows[225]['state']=='TRUNK_CLOSED' and rows[240]['state']=='HEAD_TURNING'
maxstep=max(math.dist(a,b) for pp,qq in zip(markers,markers[1:]) for a,b in zip(pp,qq))
import importlib.util
sp=importlib.util.spec_from_file_location("actual_v8",r.parent/"motion-test-v8/src/render_test_v8.py");actual_v8=importlib.util.module_from_spec(sp);sp.loader.exec_module(actual_v8)
oldmarkers=[]
for f in range(240):
 v=actual_v8.victim_pose(f/30);oldmarkers.append([v['S'],v['P'],v['neck']]+v['knees']+v['feet'])
oldstep=max(math.dist(a,b) for pp,qq in zip(oldmarkers,oldmarkers[1:]) for a,b in zip(pp,qq))
# Engine snapshot is byte-identical to original V8; active smoothing is explicitly documented.
engine=(r/'src/v8_engine.py').read_bytes();original=(r.parent/'motion-test-v8/src/render_test_v8.py').read_bytes();assert engine==original
var=max(max(x)-min(x) for x in bone.values());assert var<.05
order={'required_states':[n for t,n in m.STATES],'observed_states':list(dict.fromkeys(x['state'] for x in rows)),'state_start_seconds':dict((n,t) for t,n in m.STATES),'victim_fully_inside':6.2,'last_victim_support_release_by':6.7,'closing_hand_contact_starts':6.95,'fully_closed_seconds':7.5,'fully_closed_frame':225,'latch_sound_seconds':7.5,'latch_frame':225,'witness_notice_seconds':7.75,'head_turn_seconds':8.,'eye_narrow_seconds':9.2,'head_before_closure_violations':0,'valid_order':True,'enforcement':'head_time asserts trunk_angle == 0 before any head-turn frame; source state and geometry are checked across all 300 rendered poses.'}
report={'frames':300,'world_stance_slide_max':slide,'max_criminal_shoulder_to_hand_reach':reach,'hand_to_lid_gap_during_closing':closing_gap,'max_rounded_normalized_bone_length_variation':var,'victim_markers_max_frame_displacement':maxstep,'V8_original_same_markers_max_frame_displacement':oldstep,'victim_clearance_at_4_6':[1480+j*8-p[1] for j,p in enumerate(m.victim_pose(4.6)['feet'])],'V8_engine_snapshot_unchanged':True,'note':'Source-model geometry; maximum marker displacement is not a perceptual smoothness score. Occlusion and playback are inspected separately. V8 comparison uses the original separately imported V8 source and easing.'}
(r/'pose-ledger.json').write_text(json.dumps(rows,indent=2));(r/'action-order-validation.json').write_text(json.dumps(order,indent=2));(r/'choreography-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));print(json.dumps(order,indent=2))
# Contact overlaps and continuity across all authored state boundaries.
support_gap=0.
for f in range(300):
 t=f/30;q=m.clock(t);ps=[m.actor_pose(t,i) for i in (0,1)];v=m.victim_pose(t);hs=m.hand_targets(t,ps,v)
 if 3.1<=q<=5.72:
  for i,j,p in [(0,0,v['grips'][0]),(0,1,v['back']),(1,0,v['waist']),(1,1,v['knees'][1])]:support_gap=max(support_gap,math.dist(hs[i][j],p))
assert support_gap<1e-8
hs=m.hand_targets(6.7,[m.actor_pose(6.7,i) for i in (0,1)],m.victim_pose(6.7));assert min(p[1]-17 for pair in hs for p in pair)>1312.5
jumps=[]
def allpoints(t):
 v=m.victim_pose(t);ps=[m.actor_pose(t,i) for i in (0,1)];hs=m.hand_targets(t,ps,v)
 return [v['S'],v['P'],v['neck']]+v['knees']+v['feet']+[p['hip'] for p in ps]+[h for pair in hs for h in pair]
for t in [1.4,2.3,3.,4.6,5.5,6.2,6.45,6.7,6.95,7.1,7.5,7.75,8.,9.2]:jumps.append(max(math.dist(a,b) for a,b in zip(allpoints(t-1e-5),allpoints(t+1e-5))))
assert max(jumps)<.05,max(jumps)
report.update({'max_lift_support_gap':support_gap,'withdrawn_hand_top_min_at_6_7':min(p[1]-17 for pair in hs for p in pair),'near_sill_y':1312.5,'max_pose_boundary_difference_at_plus_minus_10_microseconds':max(jumps)})
order['observed_matches_required']=order['observed_states']==order['required_states'];assert order['observed_matches_required']
(r/'action-order-validation.json').write_text(json.dumps(order,indent=2));(r/'choreography-verification.json').write_text(json.dumps(report,indent=2))
