from pathlib import Path
import sys
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import scene_svg,Raster
rows=[(12,[.2,.85,1.5,2.,2.8,3.6]),(13,[.2,.95,1.3,1.6,2.5,3.3]),(14,[.5,1.2,2,3.2]),(15,[0,1.5,2.8,3.8])];out=Image.new('RGB',(1440,1808),'#081521');d=ImageDraw.Draw(out);rr=Raster(240,426)
for row,(scene,times) in enumerate(rows):
 for j,t in enumerate(times):
  out.paste(rr.render(scene_svg(scene,t)),(j*240,row*452));d.text((j*240+5,row*452+431),f'S{scene:02d} +{t:.2f}s',fill='white')
out.save(R/'renders/previews/HOUSE_INTERACTION_GATE.jpg',quality=95)
