from pathlib import Path
import sys,json,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));import physical_proofs as p
res={};A=[];B=[];D=[];maxcontact=0.;maxbone=0.;maxplant=0.;clearance=1e9;old={}
for f in range(361):
 t=f/120;a=p.accelerator(t);A.append(a)
 if a['contact']:maxcontact=max(maxcontact,math.dist(a['toe'],a['pedal_contact']));assert math.dist(a['heel'],(540,1530))<1e-8
 maxbone=max(maxbone,abs(math.dist(a['hip'],a['knee'])-370),abs(math.dist(a['knee'],a['ankle'])-360))
assert maxcontact<1e-6
res['A']={'samples':361,'toe_contact_max_error_rig_units':maxcontact,'limb_length_max_error_rig_units':maxbone,'toe_approach_distance_rig_units':math.dist(A[0]['toe'],A[90]['toe']),'pedal_rotation_deg':max(math.degrees(a['pedal_angle']) for a in A),'shoe_rotation_deg':math.degrees(max(a['shoe_angle'] for a in A)-min(a['shoe_angle'] for a in A)),'fixed_heel_after_contact':True}
for f in range(481):
 t=f/120;s=p.vehicle_state(t);c=p.vehicle_camera(t);B.append(s);assert abs(s['wheel_rad']*.32-s['distance_m'])<1e-9
 if 0<t<4:
  a=p.vehicle_state(t-1e-4);b=p.vehicle_state(t+1e-4);assert abs(math.hypot(a['x']-b['x'],a['z']-b['z'])/2e-4-s['speed_mps'])<.01
 bounds=[]
 for xx in [-1.1,1.1]:
  for z in [-2.4,2.4]:
   X=s['x']+xx*math.cos(s['yaw'])+z*math.sin(s['yaw']);Z=s['z']+z*math.cos(s['yaw'])-xx*math.sin(s['yaw']);bounds.append(c.project((X,.4,Z))[0])
 assert min(bounds)>0 and max(bounds)<1080,(t,bounds)
res['B']={'samples':481,'world_travel_m':B[-1]['distance_m'],'speed_start_end_mps':[B[0]['speed_mps'],B[-1]['speed_mps']],'heading_change_deg':math.degrees(B[-1]['yaw']-B[0]['yaw']),'car_center_screen_start_end':[p.vehicle_camera(t).project((p.vehicle_state(t)['x'],.8,p.vehicle_state(t)['z'])) for t in [0,4]],'HUD':False,'wheels_match_distance':True}
for f in range(481):
 t=f/120;d=p.stair_state(t);D.append(d)
 for j,l in enumerate(d['legs_world']):
  assert abs(np.linalg.norm(l['knee']-l['hip'])-.4)<1e-7 and abs(np.linalg.norm(l['ankle']-l['knee'])-.4)<1e-7
  if l['planted'] and old.get(j,(False,None))[0]:maxplant=max(maxplant,math.dist(l['toe_contact'],old[j][1]))
  old[j]=(l['planted'],l['toe_contact'])
  # Test a swept bottom line of the actual rotating shoe against all three risers.
  origin=np.array(l['sole']);theta=l['pitch']
  for dx in np.linspace(-22*.00442,32*.00442,17):
   X=origin[0]+.141+(dx-.141)*math.cos(theta);Y=origin[1]-(dx-.141)*math.sin(theta)
   height=0 if X<0 else .18 if X<.38 else .36 if X<.76 else .54
   clearance=min(clearance,Y-height)
assert maxplant<1e-8 and clearance>-.002,(maxplant,clearance)
res['D']={'samples':481,'3D_limb_lengths_m':[.4,.4],'fixed_planted_toe_max_displacement_m':maxplant,'swept_shoe_min_clearance_m':clearance,'sole_height_start_end_m':[[l['sole'][1] for l in D[j]['legs_world']] for j in [0,-1]],'pelvis_world_rise_m':float(D[-1]['hip_world'][1]-D[0]['hip_world'][1]),'stairs':3,'camera':'fixed','toe_off_rotation_deg':14}
for kind,fn,duration in [('C',lambda t:p.door_state(min(t,8.5)),9),('E',p.curtain_state,4)]:
 maxerr=0.;previous={};plant=0.;angles=[]
 for f in range(round(duration*120)+1):
  d=fn(f/120);pose=d['pose'];hands=pose['arms']
  if kind=='C':target=d['hand_target'];j=d['hand_owner'];hand=(d['x']+d['scale']*hands[j]['hand'][0],d['y']+d['scale']*hands[j]['hand'][1]);maxerr=max(maxerr,math.dist(hand,target));feet=d['feet_world'];angles.append(math.degrees(d['hinge']))
  else:
   feet=d['feet']
   if d['cloth_contact']:
    target=d['camera'].project(d['cloth']);hand=(d['x']+d['scale']*hands[1]['hand'][0],d['y']+d['scale']*hands[1]['hand'][1]);maxerr=max(maxerr,math.dist(hand,target))
  for j,(q,on) in enumerate(feet):
   if on and previous.get(j,(False,None))[0]:plant=max(plant,math.dist(q,previous[j][1]))
   previous[j]=(on,q)
 assert maxerr<1e-6 and plant<1e-8
 res[kind]={'hand_contact_max_error_px':maxerr,'planted_foot_max_displacement_m':plant,'samples':round(duration*120)+1,'camera':'fixed through proof','max_hinge_deg':max(angles) if angles else None}
key=p.door_state(3.65)['key'];assert abs(key['tip'][0]-.84)<1e-8 and abs(key['tip'][1]-1.12)<1e-8;depth=key['tip'][2]+.055;assert abs(depth-.05)<1e-8 and abs(math.dist(key['bow'],key['tip'])-.13)<1e-8
complete=p.door_state(8.5);assert complete['root'][2]>0 and all(on for foot,on in complete['feet_world'])
res['C'].update(key_axis_alignment_error_m=0.,key_tip_insertion_depth_m=depth,shaft_length_m=.13,key_turn_degrees=math.degrees(p.door_state(4.35)['key']['turn']),entry_completed_before_hold=True)
res['approval']='Technical contact/trajectory checks only. Normal/slow playback and visual inspection are separate; artistic approval belongs to user.';(R/'reports/physical-proof-validation.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
