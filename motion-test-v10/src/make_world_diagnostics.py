"""Review-only shared-world overlays, not included in the final film."""
from pathlib import Path
from PIL import Image,ImageDraw
import render_test_v10 as m
r=Path(__file__).resolve().parents[1];dest=r/'diagnostics';dest.mkdir(exist_ok=True);rr=m.Raster(540,960)
ts=[0.,1.4,3.,3.8,4.6,5.,5.4,5.8,6.2,6.7,7.5]
sheet=Image.new('RGB',(1080,670*4),'#06101b');d=ImageDraw.Draw(sheet)
for n,t in enumerate(ts):
 im=rr.render(m.scene(t,debug=True));p=dest/f'GROUND_{t:04.1f}s.png';assert not p.exists();im.save(p)
 x=n%3*360;y=n//3*670;sheet.paste(im.resize((360,640)),(x,y));d.text((x+8,y+646),f'{t:.1f}s / world ground + contacts',fill='white')
p=r/'V10_GROUND_PLANE_DIAGNOSTICS.jpg';assert not p.exists();sheet.save(p,quality=95)
