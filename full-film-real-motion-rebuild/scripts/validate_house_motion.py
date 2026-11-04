"""Independent geometric/contact audit of the actual new rigs, at 120 Hz."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'))
import house_site as site,house_actions as door,stairs_actions as stairs,room_actions as room
maxbone=0.;maxplant=0.;maxsole=0.;maxcontact=0.;maxear=0.;maxsupport=0.;keylen=0.;collisions=[];previous={};samples=0;maxshoe=0.;maxfixedshoe=0.;shoe_previous={};contact_counts={};stair_bounds=[1e9,-1e9,1e9,-1e9]
def residual(A,B):return math.dist(A,B)
def palm(d,j):
 p=d['pose']['arms'][j]['hand'];return d['x']+d['scale']*p[0],d['y']+d['scale']*p[1]
def audit_contact(label,A,B):
 global maxcontact
 e=residual(A,B);maxcontact=max(maxcontact,e);contact_counts[label]=contact_counts.get(label,0)+1
 assert e<1e-5,(label,e)
for k in range(round((80-48.025)*120)):
 t=48.025+k/120
 if t<51:
  stage='exit-run';c=site.exit_camera(t) if t<site.RUN_START else site.run_camera(t);d=site.actor_state(t,c);fs=d['feet_world'];project=lambda p:c.project(site.W(*p));world=lambda p:site.W(*p)
 elif t<stairs.T0:
  stage='door';d=door.actor_state(t-51);c=door.camera(t-51);fs=d['feet_world'];project=c.project;world=site.door_world
 elif t<stairs.END:
  stage='stairs';d=stairs.actor_state(t);c=d['camera'];fs=d['feet'];project=c.project;world=site.door_world
 else:
  stage='room';d=room.actor_state(t);c=d['camera'];fs=d['feet'];project=c.project;world=site.door_world
 samples+=1;p=d['pose'];s=d['scale']
 for arm in p['arms']:maxbone=max(maxbone,abs(residual(arm['shoulder'],arm['elbow'])-90),abs(residual(arm['elbow'],arm['hand'])-87))
 for j,(f,on) in enumerate(fs):
  l=p['legs'][j];maxbone=max(maxbone,abs(residual(l['hip'],l['knee'])-85),abs(residual(l['knee'],l['ankle'])-85));q=(d['x']+s*l['sole'][0],d['y']+s*l['sole'][1]);maxsole=max(maxsole,residual(q,project(f)));w=world(f)
  if j in previous and on and previous[j][0]:maxplant=max(maxplant,residual(w,previous[j][1]))
  previous[j]=(on,w)
  depth=c.depth(site.W(*f)) if stage=='exit-run' else c.depth(f);rendered_width=54*s*l['shoe_scale'];expected_width=54*site.UNIT*c.f/depth;maxshoe=max(maxshoe,abs(rendered_width-expected_width));base=c.camera if hasattr(c,'camera') else c;signature=(base.x,base.z,base.y,base.yaw,base.f,base.h)
  if j in shoe_previous and on and shoe_previous[j][0] and signature==shoe_previous[j][1]:maxfixedshoe=max(maxfixedshoe,abs(rendered_width-shoe_previous[j][2]))
  shoe_previous[j]=(on,signature,rendered_width)
  if stage=='room' and room.PHONE[0]-.25<=f[0]<=room.PHONE[0]+.25 and room.PHONE[2]-.20<=f[2]<=room.PHONE[2]+.20 and f[1]<room.FLOOR+.75:collisions.append((t,j))
 if stage=='exit-run' and t<49.14:
  target=c.project(site.car_handle(t));e=min(residual(palm(d,j),target) for j in [0,1]);audit_contact('car-door handoff',palm(d,min(range(2),key=lambda j:residual(palm(d,j),target))),target)
 if stage=='door':
  u=t-51
  if .22<=u<.65:audit_contact('locked handle',palm(d,0),c.project(door.hardware(u,False)[1]))
  if d['key']['held']:
   audit_contact('key bow grip',palm(d,0),c.project(d['key']['bow']));keylen=max(keylen,abs(residual(d['key']['bow'],d['key']['tip'])-.13))
  if 2.73<=u<3.05:audit_contact('opening lever',palm(d,0),c.project(door.hardware(u,False)[1]))
  if 3.05<=u<3.55:audit_contact('palm on leaf',palm(d,0),c.project(door.contact(u)))
  if 4.35<=u<4.95:audit_contact('inside closing grip',palm(d,0),c.project(door.hardware(u,True)[1]))
  if 5.1<=u<5.65:audit_contact('thumbturn grip',palm(d,0),c.project(door.hardware(u,True)[2]))
 if stage=='stairs':
  if d['rail_contact']:audit_contact('rail grip',palm(d,1),c.project(d['rail']))
  pts=[]
  for leg in p['legs']:pts += [leg['knee'],leg['ankle'],(leg['sole'][0]-25,leg['sole'][1]),(leg['sole'][0]+35,leg['sole'][1])]
  for arm in p['arms']:pts +=[arm['elbow'],arm['hand']]
  hx,hy=p['head'];pts += [(hx-65,hy-83),(hx+100,hy+66)]
  for xx,yy in pts:
   xx=d['x']+s*xx;yy=d['y']+s*yy;stair_bounds=[min(stair_bounds[0],xx),max(stair_bounds[1],xx),min(stair_bounds[2],yy),max(stair_bounds[3],yy)]
 if stage=='room':
  if d['cloth_contact']:audit_contact('curtain grip',palm(d,1),c.project(d['cloth']))
  if d['phone_grip']:audit_contact('phone grip',palm(d,d['phone_owner']),d['phone_pixel'])
  if d['ear_contact']:
   maxear=max(maxear,residual(p['arms'][d['phone_owner']]['hand'],d['head_ear_local']))
   ex=d['x']+s*d['ear_point_local'][0];ey=d['y']+s*d['ear_point_local'][1];edge=d['phone_pixel'][0]+14*d['phone_scale'];assert abs(edge-ex)<1e-6 and d['phone_pixel'][1]-44*d['phone_scale']<=ey<=d['phone_pixel'][1]+29*d['phone_scale'],'Phone misses ear-side face point'
  if not d['phone_held']:
   phone,angle=room.device_rest(t);bottom=abs(14*math.sin(math.radians(angle)))+29*math.cos(math.radians(angle));rendered=d['phone_pixel'][1]+bottom*d['phone_scale'];expected=c.project((phone[0],room.FLOOR+.75,phone[2]))[1];maxsupport=max(maxsupport,abs(rendered-expected))
assert maxshoe<1e-6 and maxfixedshoe<1e-6,(maxshoe,maxfixedshoe)
assert maxbone<1e-6 and maxplant<1e-6 and maxsole<1e-6 and maxear<1e-6 and maxsupport<1e-6 and keylen<1e-9 and not collisions,(maxbone,maxplant,maxsole,maxear,maxsupport,keylen,collisions[:3])
assert stair_bounds[0]>=0 and stair_bounds[1]<=1080 and stair_bounds[2]>=0 and stair_bounds[3]<=1920,stair_bounds
out={'ok':True,'audit_hz':120,'samples':samples,'max_segment_length_error_rig_units':maxbone,'max_consecutive_planted_foot_displacement_m':maxplant,'max_projected_sole_error_px':maxsole,'max_full_grip_error_px':maxcontact,'max_ear_anchor_error_rig_units':maxear,'max_phone_table_support_error_px':maxsupport,'max_key_length_error_m':keylen,'max_world_depth_shoe_width_error_px':maxshoe,'max_fixed_camera_planted_shoe_width_delta_px':maxfixedshoe,'foot_nightstand_collisions':collisions,'stair_actor_conservative_screen_bounds_px':stair_bounds,'contacts_sampled':contact_counts,'limits':'Checks rig/contact geometry and foot points, not every painted mesh vertex or subjective weight/acting quality. Foot plans are independent of camera motion.'};(R/'reports/house-motion-validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
