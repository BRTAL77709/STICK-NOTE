from pathlib import Path
import sys,json,math,hashlib,subprocess
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'));sys.path.insert(0,str(R/'engine'))
from scene_builder import scene_svg,SHOTS
from scene_sources import evaluate as scene_svg
from motion_state import state,vehicleState,pursuit_distance
from actor import stair_gait
from house17 import doorState
import v10_trunk
frames=json.loads((R/'hyperframes/assets/vehicle-state.js').read_text().split('=',1)[1].rstrip(';'));errors=[];velocity=[];pitch=[]
for f in range(2581):
 t=f/30;s=vehicleState(t)
 for k,v in s.items():
  if isinstance(v,(int,float)):errors.append(abs(v-frames[f][k]))
 for black in [False,True]:
  p=state(t,black);assert abs(p['wheel_rad']*.32-p['distance_m'])<1e-8
  if 0<t<48 and not black:
   d=.0001;l=state(t-d);r=state(t+d);velocity.append(abs(math.hypot(r['x']-l['x'],r['z']-l['z'])/(2*d)-p['speed_mps']))
  if p['acceleration_mps2']!=0:pitch.append(p['pitch']*p['acceleration_mps2'])
assert max(errors)<1e-8 and min(pitch)>=0 and max(velocity)<.01
sampled=0
for s in SHOTS:
 for f in range(s['frames']):
  svg=scene_svg(s['scene'],f/30);assert '<svg' in svg and '</svg>' in svg and 'nan' not in svg.lower();sampled+=1
 print('SOURCE VALIDATED',s['scene'],flush=True)
# Trunk action remains monotone and closed before the preserved turn.
assert v10_trunk.lid_angle(7.5)==0 and v10_trunk.head_time(7.99)==3.2
assert doorState(2.11)['locked'] and not doorState(2.12)['locked'];assert doorState(2.84)['angle']==0;assert doorState(4.95)['angle']==0 and doorState(5.55)['locked']
missing=[];changed=[];matched=0
for item in json.loads((R/'reports/previous-version-hashes.json').read_text()):
 p=R.parent/item['path']
 if not p.exists():missing.append(item['path']);continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:changed.append(item['path'])
 else:matched+=1
assert not changed,changed
segments=json.loads((R/'narration-timing.json').read_text());assert all(0<=s['start']<s['end']<=86 for s in segments);assert all(a['end']<=b['start'] for a,b in zip(segments,segments[1:]));assert len(SHOTS)==18 and sum(s['frames'] for s in SHOTS)==2580
report={'ok':True,'source_frames':sampled,'vehicle_samples':2581,'export_max_error':max(errors),'velocity_position_max_error_mps':max(velocity),'correct_pitch_sign':True,'trunk_close_before_turn':True,'door_unlock_before_open':True,'door_close_before_relock':True,'prior_files_matched':matched,'prior_files_missing_in_checkout':len(missing),'prior_files_changed':len(changed),'narration_phrases':len(segments),'word_alignment':'not available; measured phrases used','voice_quality':'listening unverified; creative approval pending'}
(R/'reports/source-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
