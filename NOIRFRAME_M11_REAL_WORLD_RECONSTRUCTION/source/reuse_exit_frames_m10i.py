"""Reuse only pixel-equivalent inputs; changed handle/contact states are always rerendered."""
from pathlib import Path
import gzip,json,hashlib,shutil
from bootstrap import ROOT as R
a=json.load(gzip.open(R/'scenes/CAR_EXIT_RUNNING_M10.json.gz','rt'));b=json.load(gzip.open(R/'scenes/CAR_EXIT_RUNNING_M10I.json.gz','rt'));assert a['topology']==b['topology'];old=json.loads((R/'reports/M10_CAR_EXIT_RUNNING_FINAL_RENDER_REJECTED_HANDLE_TIMING.json').read_text())
for name in ['render_clips.py','cameras.py','sets.py','vehicle_system.py','native_style.py','stair_style.py','fast_depth.py','depth_render.py','approved_head.py','approved_head_view.py','view_head.py','svg.py','legacy/geometry.py','legacy/shots.py']:
 p=R/'source'/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==old['source_sha256']['source/'+name],name
src=R/'frames/M10_EXIT_HANDLE_PREVIOUS';dst=R/'frames/M10_CAR_EXIT_RUNNING_FINAL';dst.mkdir(exist_ok=True);reused=[];changed=[]
for i,(x,y,s,t) in enumerate(zip(a['frames'],b['frames'],a['state'],b['state'])):
 if x['meshes']==y['meshes'] and s==t and (src/f'{i:05}.png').exists():shutil.copyfile(src/f'{i:05}.png',dst/f'{i:05}.png');reused.append(i)
 else:changed.append(i)
(R/'reports/EXIT_FRAME_REUSE.json').write_text(json.dumps({'reused_frame_indices':reused,'rerender_frame_indices':changed,'reuse_count':len(reused),'rerender_count':len(changed),'proof':'Exact evaluated mesh arrays and full authoring state equality; identical topology and critical renderer/camera/set/shader source hashes. No approximate or interpolated frame substitution.'},indent=2));print('REUSE',len(reused),'RERENDER',len(changed))
