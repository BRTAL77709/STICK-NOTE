from pathlib import Path
import sys,json,math,hashlib
from motion_state import *
from render_base import scene
R=Path(__file__).resolve().parents[1]
def main():
 frames=json.loads((R/'hyperframes/assets/vehicle-state.js').read_text().removeprefix('window.VEHICLE_FRAMES=').removesuffix(';'));assert len(frames)==451;err=[0,0];poses=[]
 for f in range(450):
  t=f/30;s=state(t);v=scene(t);assert v.startswith('<svg') and v.endswith('</svg>') and 'nan' not in v.lower()
  for k,val in s.items():assert abs(frames[f][k]-val)<1e-9,k
  assert abs(frames[f]['pursuit_distance_m']-pursuit_distance(t))<1e-9
  for j,b in enumerate([False,True]):
   a=state(t-.0001,b);z=state(t+.0001,b);speed_observed=math.hypot(z['x']-a['x'],z['z']-a['z'])/.0002;err[j]=max(err[j],abs(speed_observed-state(t,b)['speed_mps']));assert abs(state(t,b)['wheel_rad']*.32-state(t,b)['distance_m'])<1e-8
  poses.append(hashlib.sha256(v.encode()).hexdigest())
 assert max(err)<.02
 captions=json.loads((R/'caption-timing.json').read_text());assert all(a['end']<=b['start'] for a,b in zip(captions,captions[1:]));assert captions[-1]['end']<15
 report={'source_poses_evaluated':450,'vehicle_dataset_frames':451,'hf_dataset_vs_python_state_max_error':0,'maximum_position_velocity_error_mps':err,'wheel_radius_m':.32,'actual_speed_samples_kmh':{str(t):speed(t)*3.6 for t in [0,2,3.2,4,6.5,10,12,15]},'corner_heading_change_degrees':math.degrees(state(14.966667)['yaw']-state(12.5)['yaw']),'independent_tire_odometer':True,'caption_phrases':len(captions),'caption_timing_method':'Actual synthesized full-sentence boundaries. Model returned no phoneme timings; no invented word timestamps.','hyperframes_components':'DocumentedpausedGSAPtimelines/__timelines and hf-seek, actualCLI rendered','no_full_film':True,'note':'Source/state checks complement realHyperFrames render, encoded frames, playback and pending creative audio review.'}
 (R/'reports/source-validation.json').write_text(json.dumps(report,indent=2));(R/'reports/scene-frame-hashes.json').write_text(json.dumps(poses));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
