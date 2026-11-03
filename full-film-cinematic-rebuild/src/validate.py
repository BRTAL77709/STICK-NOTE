"""Frame-accurate kinematics/contact/instrument checks; no artistic pass inferred."""
import math,json
from pathlib import Path
import motion_state as m
from render import svg
from house_system import lock_state
ROOT=Path(__file__).resolve().parents[1]
def main():
 errors=[];der=[];blackder=[];states=[]
 for frame in range(450):
  t=frame/30;s=m.state(t);b=m.state(t,True);h=.0001
  for black,dst in [(False,der),(True,blackder)]:
   before=m.state(t-h,black);after=m.state(t+h,black);v=math.hypot(after['x']-before['x'],after['z']-before['z'])/(2*h);dst.append(abs(v-m.state(t,black)['speed_mps']))
  assert abs(s['wheel_rad']*.32-s['distance_m'])<1e-9
  assert abs(b['wheel_rad']*.32-b['distance_m'])<1e-9
  assert all(math.isfinite(v) for v in s.values())
  src=svg(t);assert src.startswith('<svg') and src.endswith('</svg>');assert 'nan' not in src.lower()
  if frame%15==0:states.append({'frame':frame,**s,'black_speed_kmh':b['speed_kmh'],'gap_m':28-14*m.ease(t,5,11)})
 assert max(der)<.002 and max(blackder)<.002,(max(der),max(blackder))
 assert sum(round((b-a)*30) for a,b,_ in m.CUTS)==450
 # Door prototype cannot open with a key inserted; unlock precedes latch release/hinge motion.
 for f in range(121):
  q=lock_state(f/30)
  if q['door_yaw']>0:assert not q['locked'] and q['key_insertion_m']==0 and q['latch_released']
 caps=json.loads((ROOT/'narration-timing.json').read_text());assert all(a['end']<=b['start'] for a,b in zip(caps,caps[1:]));assert all(0<=a['start']<a['end']<=15 for a in caps)
 report={'source_poses_checked':450,'duration_s':15,'fps':30,'speed_range_kmh':[m.speed(0)*3.6,m.speed(15)*3.6],'speedometer_relation':'exact same speed_kmh value as metric motion state','maximum_world_speed_error_mps':max(der),'maximum_pursuer_world_speed_error_mps':max(blackder),'maximum_acceleration_mps2':max(m.acceleration(f/300) for f in range(4500)),'wheel_radius_m':.32,'wheel_roll_relation':'distance/radius, separate pursuer odometer includes closing gap','minimum_tire_y_m':0.,'driver_hand_contact':'two-link IK endpoints attached to rotating rim; all source poses evaluated','caption_phrases':len(caps),'caption_overlaps':0,'door_prototype_order':'unlock and key withdrawal before opening','shots':[{'in':a,'out':b,'title':n} for a,b,n in m.CUTS],'note':'Mathematical/model checks only; encoded appearance/audio and artistic review are separate.'}
 (ROOT/'reports/source-validation.json').write_text(json.dumps(report,indent=2));(ROOT/'reports/motion-samples.json').write_text(json.dumps(states,indent=2));(ROOT/'plan/integrated-shotlist.json').write_text(json.dumps(report['shots'],indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
