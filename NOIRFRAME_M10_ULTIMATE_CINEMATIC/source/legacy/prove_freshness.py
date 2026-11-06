"""Source-edit sensitivity in two isolated source copies, never touching old productions."""
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='m03-source-proof-') as tmp:
 q=Path(tmp);results=[]
 for name in ['original','edited']:
  folder=q/name;shutil.copytree(R/'source',folder,ignore=shutil.ignore_patterns('__pycache__'));p=folder/'stair_test.py'
  if name=='edited':p.write_text(p.read_text().replace('HEIGHT=[(0,.65)','HEIGHT=[(0,.63)'))
  out=q/(name+'.png');program="import sys;sys.path.insert(0,sys.argv[1]);from shots import stair;from depth_render import DepthRaster;w,d=stair(0);DepthRaster(360).render(w[0]).save(sys.argv[2])"
  subprocess.run(['python','-B','-c',program,str(folder),str(out)],check=True);results.append({'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'render_sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
 a=np.array(Image.open(q/'original.png'));b=np.array(Image.open(q/'edited.png'));count=int(np.any(a!=b,axis=2).sum());assert count>0 and results[0]['source_sha256']!=results[1]['source_sha256']
 (R/'reports/SOURCE_EDIT_RENDER_PROOF.json').write_text(json.dumps({'method':'Two isolated source copies, 0.65m versus 0.63m initial pelvis height. Separate fresh Python processes and depth raster instances. No video or cached-frame input.','results':results,'changed_pixels_at_360x640':count,'source_edit_affects_actual_render':True},indent=2));print('freshness changed pixels',count)
