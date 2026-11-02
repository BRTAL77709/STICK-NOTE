"""Deterministic all-frame contact, reach, hinge and articulation checks."""
import importlib.util,xml.etree.ElementTree as E,json,math,ast
from pathlib import Path
r=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('v8',r/'src/render_test_v8.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
rows=[];prev={};slide=0.;contacts=0.;bone={};sag=[]
for f in range(240):
 t=f/30;ps=[m.actor_pose(t,i) for i in (0,1)];v=m.victim_pose(t);hands=m.hand_targets(t,ps,v)
 svg=m.scene(t);ids={n.get('id'):n for n in E.fromstring(svg).iter() if n.get('id')}
 for i in (0,1):
  assert any(on for foot,on,u in ps[i]['feet'])
  assert abs(math.dist(ps[i]['hip'],ps[i]['shoulder'])-125)<1e-7
  for j,(foot,on,u) in enumerate(ps[i]['feet']):
   key=(i,j)
   if on:
    assert abs(foot[1]-m.GROUND[i])<1e-7
    if key in prev and prev[key][1]:slide=max(slide,math.dist(foot,prev[key][0]))
   prev[key]=(foot,on)
 for i,j,target,active in [(0,0,v['grips'][0],t<=1.6 or 2.5<=t<=5.72),(0,1,v['back'],2.88<=t<=5.76),(1,0,v['grips'][1],t<=2.5),(1,0,v['waist'],2.86<=t<=5.80),(1,1,v['waist'],1.58<=t<=2.67),(1,1,v['knees'][1],3.05<=t<=5.82)]:
  if active:contacts=max(contacts,math.dist(hands[i][j],target))
 # Explicit overlap: C2 waist received before C1 leaves victim; all four support grips before lift.
 if 1.6<=t<=2.5:assert math.dist(hands[1][1],v['waist'])<1e-7
 if 3.1<=t<=4.5:assert all(math.dist(hands[i][j],target)<1e-7 for i,j,target in [(0,0,v['grips'][0]),(0,1,v['back']),(1,0,v['waist']),(1,1,v['knees'][1])])
 for name,n in ids.items():
  if n.get('data-joints'):
   pts=[tuple(map(float,p.split(','))) for p in n.get('data-joints').split(';')];scale=v['scale'] if name.startswith('victim') else 1.
   for j in (0,1):bone.setdefault(name+':'+str(j),[]).append(math.dist(pts[j],pts[j+1])/scale)
 if t<=3.1:
  sag.append(v['P'][1]-v['S'][1]);assert all(abs(p[1]-(1480+j*8))<.001 for j,p in enumerate(v['feet']))
 head=ids['head-1'];rows.append({'frame':f,'time':t,'lid_angle':m.trunk_angle(t),'victim_pelvis':v['P'],'victim_shoulders':v['S'],'victim_feet':v['feet'],'victim_knees':v['knees'],'victim_angle':v['angle'],'depth':v['depth'],'perspective_scale':v['scale'],'glove_targets':hands,'criminal_hips':[p['hip'] for p in ps],'criminal_shoulders':[p['shoulder'] for p in ps],'criminal_foot_stances':[[on for ft,on,u in p['feet']] for p in ps],'head_yaw':float(head.get('data-yaw')),'eye_narrow':float(head.get('data-narrow'))})
assert slide<1e-7 and contacts<1e-7
assert m.trunk_angle(1.5)==0 and m.trunk_angle(2.5)==102
assert all(row['victim_feet'][j][1]<1400 for row in rows if 4.0<=row['time']<=4.5 for j in (0,1))
assert rows[192]['head_yaw']>60 and rows[216]['head_yaw']<2 and rows[230]['eye_narrow']>.99
variations={k:max(v)-min(v) for k,v in bone.items()};assert max(variations.values())<.05
# V7 head geometry code is preserved verbatim. Only its input clock is remapped in V8.
old=(r.parent/'motion-test-v7/src/render_test_v7.py').read_text();new=(r/'src/render_test_v8.py').read_text()
def funcs(s):return {n.name:ast.get_source_segment(s,n) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
a,b=funcs(old),funcs(new);pres={name:a[name]==b[name] for name in ['draw_head','draw_head_legacy','hull','curved_outline','reaction']};assert all(pres.values())
# Loading is articulated: pelvis-relative-to-shoulder and knee angles change while depth increases.
def kneeangle(row,j):
 t=row['time'];v=m.victim_pose(t);a=m.sub(v['hips'][j],v['knees'][j]);b=m.sub(v['feet'][j],v['knees'][j]);return math.degrees(math.acos(max(-1,min(1,sum(x*y for x,y in zip(a,b))/(math.hypot(*a)*math.hypot(*b))))))
lo=[x for x in rows if 4.5<=x['time']<=5.72];kr=[kneeangle(x,1) for x in lo]
report={'frames_checked':240,'duration':8,'world_stance_slide_max':slide,'named_support_contact_gap_max':contacts,'minimum_dragging_pelvis_below_shoulders':min(sag),'trunk_angles_at_1_5_and_2_5':[m.trunk_angle(1.5),m.trunk_angle(2.5)],'hinge_axis_world':[[300,1005],[825,1005]],'lid_geometry':'One fixed pivot and one rigid rotating panel; gas struts finish opening after C1 release at 1.94 s.','victim_heel_heights_at_3_1':m.victim_pose(3.1)['feet'],'victim_heel_heights_at_4_5':m.victim_pose(4.5)['feet'],'lift_effort_starts':3.1,'both_feet_clear_by_1_world_unit_at':next(x['time'] for x in rows if x['time']>3.1 and all(x['victim_feet'][j][1]<1480+j*8-1 for j in (0,1))),'loading_knee_angle_range_degrees':[min(kr),max(kr)],'loading_torso_angle_range_degrees':[min(x['victim_angle'] for x in lo),max(x['victim_angle'] for x in lo)],'max_limb_length_variation_after_projection_normalization':max(variations.values()),'head_functions_byte_identical_to_V7':pres,'head_clock':'3.2 + (V8_time - 6.4) * 1.125; turn precedes narrowing.','depth_order':'Head-first entry split, identical inside/outside pose, cavity clip, fixed foreground sill. No opacity fade of victim.','limits':'Deterministic 2.5D projection and authored key poses, not a collision-certified 3D simulation. Pixel occlusion and actual playback require separate visual review.'}
(r/'pose-ledger.json').write_text(json.dumps(rows,indent=2));(r/'choreography-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
