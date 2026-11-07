"""Same-time, same-rate M07/M08 encoded frame comparisons. No retiming or camera alignment claim."""
from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
from bootstrap import ROOT as R
old=R.parent/'NOIRFRAME_M07_ALL_SCENE_REPAIRS';rows=json.loads((R/'CURRENT_SHOTS.json').read_text());out={}
for s,row in rows.items():
 p=R/row['final'];a=old/'renders'/f'M07_{s}_1080.mp4';dur=row['duration'];times=[0,dur*.2,dur*.4,dur*.6,dur*.8,dur-1/30];sheet=Image.new('RGB',(720,680*len(times)),'#071521');dr=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  for j,q in enumerate([a,p]):
   raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(q),'-frames:v','1','-vf','scale=360:640','-f','rawvideo','-pix_fmt','rgb24','-threads','1','-']);sheet.paste(Image.frombytes('RGB',(360,640),raw),(j*360,i*680));dr.text((j*360+8,i*680+646),f'{"M07" if j==0 else "M08"} / {t:.3f}s',fill='white')
 path=R/'contact_sheets'/f'{s}_M07_vs_M08.jpg';sheet.save(path,quality=92);out[s]={'before':str(a),'after':row['final'],'same_timestamps_s':times,'sheet':str(path.relative_to(R)),'limits':'Same story time, different cinematic framing; numerical change report separately identifies inherited trajectories.'};print('COMPARED',s,flush=True)
(R/'reports/COMPARISON_SOURCES.json').write_text(json.dumps(out,indent=2))
