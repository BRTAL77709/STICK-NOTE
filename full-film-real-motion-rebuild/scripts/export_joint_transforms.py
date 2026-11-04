from pathlib import Path
import json,math,csv
R=Path(__file__).resolve().parents[1]
for k in 'ABCDE':
 folder=R/'proofs'/k;data=json.loads((folder/'JOINTS_TRAJECTORIES.json').read_text());rows=[];trajectory=[]
 for n,p in enumerate(data['frames']):
  if k=='A':pairs=[('hip-knee',p['hip'],p['knee']),('knee-ankle',p['knee'],p['ankle']),('ankle-toe',p['ankle'],p['toe'])];root=p['hip'];extra={'pedal_rotation_rad':p['pedal_angle'],'shoe_rotation_rad':p['shoe_angle'],'contact':p['contact']}
  elif k=='B':
   v=p['vehicle'];root=[v['x'],0,v['z']];extra={a:v[a] for a in ['yaw','wheel_rad','steer_rad','speed_mps']};rows.append({'frame':n,'time':n/30,'root_world':root,'camera_world':p['world_camera'],**extra});trajectory.append({'frame':n,'time':n/30,'root_x':root[0],'root_y':root[1],'root_z':root[2],'camera_x':p['world_camera']['x'],'camera_z':p['world_camera']['z'],'camera_heading':p['world_camera']['yaw'],'landmark_screen_x':p['landmark_screen'][0],'landmark_screen_y':p['landmark_screen'][1],**extra});continue
  else:
   pp=p if k=='D' else p['pose'];pairs=[]
   for j,q in enumerate(pp['legs_world'] if k=='D' else pp['legs']):pairs.extend([(f'hip-knee-{j}',q['hip'],q['knee']),(f'knee-ankle-{j}',q['knee'],q['ankle'])])
   for j,q in enumerate(pp['arms_world'] if k=='D' else pp['arms']):pairs.extend([(f'shoulder-elbow-{j}',q['shoulder'],q['elbow']),(f'elbow-hand-{j}',q['elbow'],q['hand'])])
   root=p['root'];extra={}
  bones=[]
  for name,A,B in pairs:
   v=[y-x for x,y in zip(A,B)];L=math.sqrt(sum(x*x for x in v));bones.append({'name':name,'parent_joint':A,'child_joint':B,'relative_translation':v,'length':L,'axis':[x/L for x in v],'rotation_2d_rad':math.atan2(v[1],v[0]) if len(v)==2 else None})
  rows.append({'frame':n,'time':n/30,'bones':bones,'owner_projection':{a:p[a] for a in ['x','y','scale','root'] if a in p},**extra});tr={'frame':n,'time':n/30,'root_x':root[0],'root_y':root[1],'root_z':root[2] if len(root)>2 else '',**extra}
  feet=p.get('feet_world',p.get('feet',[]))
  for j,(pos,on) in enumerate(feet):tr.update({f'foot{j}_{a}':pos[i] for i,a in enumerate('xyz')});tr[f'foot{j}_planted']=on
  trajectory.append(tr)
 (folder/'JOINT_TRANSFORMS.json').write_text(json.dumps({'representation':'Parent/child translations, fixed segment lengths and bone axes; A footwell coordinates, C/E projected 2D rigs with metric root/prop tracks, D true metric 3D.','frames':rows},indent=2))
 fields=list(dict.fromkeys(a for row in trajectory for a in row))
 with (folder/'MOTION_TRAJECTORY.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(trajectory)
