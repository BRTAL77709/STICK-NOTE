from pathlib import Path
import sys,json,math,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));sys.path.insert(0,str(R/'engine/composition'))
from driver_rig import pose
from motion_state import state,travel
from scene_builder import establish_camera
maxlen=0;maxrim=0;maxreach=0
for n in range(1441):
 t=n/30;p=pose(t);cx,cy,rx,ry,angle=p['wheel']
 for j in [0,1]:
  sh,el,h=p['shoulders'][j],p['elbows'][j],p['hands'][j]
  maxlen=max(maxlen,abs(math.dist(sh,el)-178),abs(math.dist(el,h)-178));maxrim=max(maxrim,abs(((h[0]-cx)/rx)**2+((h[1]-cy)/ry)**2-1));maxreach=max(maxreach,math.dist(sh,h));assert all(math.isfinite(v) for pt in [sh,el,h] for v in pt)
assert maxlen<1e-6 and maxrim<1e-10
b=json.loads((R/'reports/baseline-preservation.json').read_text());changed=[n for n,sha in b['sha256'].items() if hashlib.sha256((Path(b['root'])/n).read_bytes()).hexdigest()!=sha];assert not changed
v10=R/'engine/animation/v10_trunk.py';assert v10.read_bytes()==(Path(b['root'])/'engine/animation/v10_trunk.py').read_bytes()
car=[state(t) for t in [0,4]];cams=[establish_camera(t) for t in [0,4]]
res={'driving_samples':1441,'max_arm_segment_error_px':maxlen,'max_normalized_rim_error':maxrim,'max_shoulder_hand_distance_px':maxreach,'vehicle_travel_scene01_m':travel(4)-travel(0),'camera_translation_scene01_m':math.hypot(cams[1].x-cams[0].x,cams[1].z-cams[0].z),'mirror_gaze_head_lead_s':4.72-4.47,'alley_gaze_head_lead_s':8.17-8.03,'approved_v10_source_unchanged':True,'baseline_files_preserved':len(b['sha256']),'baseline_changes':changed,'artistic_approval':'not inferred from constraints'}
(R/'reports/driving-contact-validation.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
