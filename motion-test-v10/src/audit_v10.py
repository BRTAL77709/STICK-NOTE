"""World plane, projected bumper separation, 3D limb/contact and trajectory audit."""
from pathlib import Path
import json,math,numpy as np
import render_test_v10 as m
r=Path(__file__).resolve().parents[1]
def polygons_overlap(a,b):
 for poly in [a,b]:
  for p,q in zip(poly,poly[1:]+poly[:1]):
   axis=np.array([q[1]-p[1],p[0]-q[0]],float);aa=[np.dot(x,axis) for x in a];bb=[np.dot(x,axis) for x in b]
   if max(aa)<min(bb) or max(bb)<min(aa):return False
 return True
bumper=[m.P(m.V(x,-16,z)) for x,z in [(350,72),(850,72),(850,100),(350,100)]]
prev={};slide=0.;reach=0.;lengths={};overlaps=[];points=[];rows=[];handoff_gaps=[];ground_errors=[];world_car_intrusions=[]
for f in range(300):
 t=f/30;ps=[m.actor_pose(t,i) for i in (0,1)];v=m.victim_pose(t);hands=m.contacts(t,ps,v);m.scene(t)
 for i,p in enumerate(ps):
  assert any(on for ft,on in p['feet'])
  lengths.setdefault('criminal-spine',[]).append(np.linalg.norm(p['shoulder']-p['hip']))
  for j,(ft,on) in enumerate(p['feet']):
   if on:
    ground_errors.append(abs(ft[2]));assert abs(ft[2])<1e-8
    if (i,j) in prev and prev[i,j][1]:slide=max(slide,float(np.linalg.norm(ft-prev[i,j][0])))
   prev[i,j]=(ft,on)
   # Full shoe quadrilateral and the whole projected bumper, same camera projection.
   shoe=[m.P(ft+m.V(dx,dy,0)) for dx,dy in [(-18,-10),(29,-10),(33,13),(-19,13)]]
   if polygons_overlap(shoe,bumper):overlaps.append((f,i,j))
   if ft[0]+33>350 and ft[0]-19<850 and ft[1]+13>=0:world_car_intrusions.append((f,i,j))
   hip=p['hip']+m.V(-15 if j==0 else 17,0,0);ank=ft+m.V(0,0,11);kn=p['knees'][j]
   for k,(a,b) in enumerate([(hip,kn),(kn,ank)]):lengths.setdefault(f'criminal-leg-{k}',[]).append(np.linalg.norm(a-b))
   sg=(1 if i==0 else -1)*(1 if j==0 else -1);sh=p['shoulder']+m.V(sg*35,-3,-12);el=m.ik3(sh,hands[i][j],90,87,m.elbow_bend(t,sg,hands[i][j]));reach=max(reach,float(np.linalg.norm(sh-hands[i][j])))
   for k,(a,b) in enumerate([(sh,el),(el,hands[i][j])]):lengths.setdefault(f'criminal-arm-{k}',[]).append(np.linalg.norm(a-b))
 for j in (0,1):
  for k,(a,b) in enumerate([(v['hips'][j],v['knees'][j]),(v['knees'][j],v['feet'][j])]):lengths.setdefault(f'victim-leg-{k}',[]).append(np.linalg.norm(a-b))
 if 6.95<=t<=7.5:handoff_gaps.append(float(np.linalg.norm(hands[1][0]-m.lid_world(t))))
 if 3<=t<=4.6:assert all(on for p in ps for ft,on in p['feet'])
 if t>=8:assert m.lid_angle(t)==0 and m.head_time(t)>=3.35
 if t<8:assert m.head_time(t)==3.2
 markers=[v['S'],v['P'],v['neck']]+v['knees']+v['feet'];points.append(markers)
 rows.append({'frame':f,'time':t,'state':m.state_at(t),'lid_angle':m.lid_angle(t),'victim_shoulder':v['S'].tolist(),'victim_pelvis':v['P'].tolist(),'victim_angle':v['angle'],'victim_knees':[p.tolist() for p in v['knees']],'victim_feet':[p.tolist() for p in v['feet']],'feet':[[{'world':p.tolist(),'stance':on} for p,on in a['feet']] for a in ps]})
assert slide<1e-8 and not overlaps and not world_car_intrusions,(slide,overlaps,world_car_intrusions)
var=max(float(max(x)-min(x)) for x in lengths.values());assert var<1e-5
maxstep=max(float(np.linalg.norm(a-b)) for pp,qq in zip(points,points[1:]) for a,b in zip(pp,qq))
# Explicit final placement fit: all skeletal anchors are inside the cavity footprint.
v=m.victim_pose(6.2);body=[v['S'],v['P'],v['neck']]+v['shoulders']+v['elbows']+v['hands']+v['hips']+v['knees']+v['feet']
assert all(380<=p[0]<=840 and 12<=p[1]<=135 and 85<=p[2]<=235 for p in body),[p.tolist() for p in body if not(380<=p[0]<=840 and 12<=p[1]<=135 and 85<=p[2]<=235)]
report={'frames':300,'world_axes':'X=car width; Y=forward along sedan; Z=height. Pavement Z=0.','projection':'Orthographic yaw20°, elevation35°; same fixed basis for car and all articulated joints.','max_stance_Z_error':max(ground_errors),'max_world_stance_displacement':slide,'projected_shoe_bumper_polygon_overlaps':len(overlaps),'shoe_car_ground_footprint_intrusions':len(world_car_intrusions),'all_four_feet_planted_through_lift_3_to_4_6':True,'max_shoulder_to_hand_reach':reach,'max_3D_bone_length_variation':var,'victim_torso_angle_range':[min(x['victim_angle'] for x in rows),max(x['victim_angle'] for x in rows)],'maximum_victim_marker_3D_frame_step':maxstep,'final_skeletal_anchors_inside_cavity':True,'final_shoulder':v['S'].tolist(),'final_pelvis':v['P'].tolist(),'max_closing_hand_lid_gap':max(handoff_gaps),'trunk_closed_time':7.5,'trunk_closed_frame':225,'head_turn_start':8.,'latch_sound_time':7.5,'limits':'Shoe and bumper polygon separation is a projected-geometry check; articulated capsule/silhouette overlaps and 2.5D interior holdouts also need encoded visual review. Not a full dynamic/collision simulation.'}
(r/'world-contact-verification.json').write_text(json.dumps(report,indent=2));(r/'pose-ledger.json').write_text(json.dumps(rows,indent=2));print(json.dumps(report,indent=2))

# Arm centerlines must cross the actual rear plane above the opening sill.
rim=[];bad=[]
for f in range(300):
 t=f/30;ps=[m.actor_pose(t,i) for i in (0,1)];v=m.victim_pose(t);hs=m.contacts(t,ps,v)
 for i in (0,1):
  for j in (0,1):
   sg=(1 if i==0 else -1)*(1 if j==0 else -1);sh=ps[i]['shoulder']+m.V(sg*35,-3,-12);el=m.ik3(sh,hs[i][j],90,87,m.elbow_bend(t,sg,hs[i][j]));pp=[sh,el,hs[i][j]]
   for a,b in zip(pp,pp[1:]):
    if a[1]*b[1]<=0 and abs(a[1]-b[1])>.001:
     p=a+(b-a)*(-a[1])/(b[1]-a[1])
     if 350<=p[0]<=850:
      rim.append(float(p[2]))
      if p[2]<235-1e-7:bad.append((f,i,j,float(p[2])))
assert not bad,bad
report['arm_centerline_below_sill_crossings']=len(bad);report['minimum_arm_rear_plane_crossing_height']=min(rim);report['sill_height']=235
(r/'world-contact-verification.json').write_text(json.dumps(report,indent=2))
