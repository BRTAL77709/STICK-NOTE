from pathlib import Path
import sys,json,math,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));import motion_state as m,physical_proofs as p,film_performance as film,house_site as site,driver_rig as driver
old={};exec(compile((R.parent/'full-film-v10-quality-rebuild/engine/animation/motion_state.py').read_text(),'baseline_motion','exec'),old)
maxvel=0.;maxbone=0.;after=0.;pos=[]
for f in range(10321):
 t=f/120;s=m.state(t)
 assert abs(s['wheel_rad']*.32-s['distance_m'])<1e-8
 if 0<t<48:
  a=m.state(t-.0001);b=m.state(t+.0001);maxvel=max(maxvel,abs(math.dist((a['x'],a['z']),(b['x'],b['z']))/.0002-s['speed_mps']))
 if t>=38:
  b=old['state'](t);after=max(after,math.dist((s['x'],s['z']),(b['x'],b['z'])))
 if t<48:
  d=driver.pose(t)
  for sh,el,hand in zip(d['shoulders'],d['elbows'],d['hands']):maxbone=max(maxbone,abs(math.dist(sh,el)-178),abs(math.dist(el,hand)-178))
 if 48.025<=t<51:site.actor_state(t,site.exit_camera(t) if t<site.RUN_START else site.run_camera(t))
 if film.CURTAIN_START<=t<film.PHONE_START:film.curtain_state(t)
 if film.PHONE_START<=t<film.CHOICE:film.call_state(t)
assert maxvel<.01 and after<1e-7 and maxbone<1e-6
assert m.speed(28.89)==0 and m.acceleration(28.91)>0 and p.accelerator(.75)['contact'] and p.accelerator(.9)['phase']=='pressure'
preserve=json.loads((R/'reports/rejected-rebuild-preservation.json').read_text());base=R.parent/'full-film-v10-quality-rebuild';changed=[n for n,sha in preserve['sha256'].items() if hashlib.sha256((base/n).read_bytes()).hexdigest()!=sha];assert not changed
out={'ok':True,'samples_120Hz':10321,'velocity_position_max_error_mps':maxvel,'wheel_distance_identity':True,'driver_limb_max_error_px':maxbone,'toe_contact_global':28.75,'pressure_and_car_acceleration_start':28.9,'after38_route_max_change_m':after,'baseline_files_unchanged':len(preserve['sha256']),'new_scene_boundaries':[61.4,65.4,69.4,77.3,81.5,86],'stair_visibility':'Three complete upper risers; lower flight elided by a narrative cut, not represented as a visible complete ascent.','artistic_approval':'pending'};(R/'reports/master-motion-validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
