from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
code='''from pathlib import Path
import sys,hashlib,json
R=Path(sys.argv[1]);sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import scene_svg,Raster
r=Raster(360,640);h=hashlib.sha256()
for i in range(180):h.update(r.render(scene_svg(18,i/30)).tobytes())
print(json.dumps({'frames':180,'size':[360,640],'pixel_sha256':h.hexdigest()}))'''
a=json.loads(subprocess.check_output([sys.executable,'-c',code,str(R.parent/'full-film-master-production')]));b=json.loads(subprocess.check_output([sys.executable,'-c',code,str(R)]));assert a==b
(R/'reports/choice-background-preservation.json').write_text(json.dumps({'all_180_preview_pixel_frames_match':True,'baseline':a,'rebuild':b,'design':'Choice-card HTML/GSAP design retained for later official composite checks'},indent=2));print('All 180 choice-background pixel frames match the baseline')
