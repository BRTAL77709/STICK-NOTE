from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'));from render_proofs import state,clean,EVENTS
import math
for kind in 'ABCDE':
 folder=R/'proofs'/kind;meta=json.loads((folder/'final.json').read_text());frames=[]
 for f in range(meta['frames']+1):
  raw=state(kind,f/30)
  if 'camera' in raw:
   c=raw['camera'];c=c.camera if hasattr(c,'camera') else c
   if not isinstance(c,dict):raw['camera_parameters_world']={a:getattr(c,a) for a in ['x','y','z','yaw','f','h']}
  if kind=='D':raw['orthographic_projection']=[[500,0,-150,320],[0,-500,65,1690+500*raw['base']]]
  frames.append(clean(raw))
 (folder/'CONTACT_EVENTS.json').write_text(json.dumps([{'time':t,'frame':math.ceil(t*30-1e-8),'event':name} for t,name in EVENTS[kind]],indent=2))
 (folder/'JOINTS_TRAJECTORIES.json').write_text(json.dumps({'proof':kind,'fps':30,'source_svg_sha256':meta['source_svg_sha256'],'units':'A footwell model coordinates; B/D metres; C/E metric roots/props with projected local joint rigs','frames':frames},indent=2))
