from pathlib import Path
import sys,hashlib,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import SHOTS,scene_svg
for s in SHOTS:
 h=hashlib.sha256()
 for f in range(s['frames']):h.update(scene_svg(s['scene'],f/30).encode())
 p=R/'scenes'/f'scene_{s["scene"]:02d}'/'final-cache.json';m=json.loads(p.read_text());m['content_sha']=h.hexdigest();m['scale']=1.;p.write_text(json.dumps(m,indent=2));print('STAMP',s['scene'],flush=True)
