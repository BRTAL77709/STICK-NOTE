from pathlib import Path
import argparse,json,subprocess,hashlib,math
from PIL import Image,ImageDraw
import numpy as np
from shots import SHOTS
from depth_render import DepthRaster
R=Path(__file__).resolve().parents[1]
def conv(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,np.generic):return x.item()
 if isinstance(x,dict):return {k:conv(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [conv(v) for v in x]
 return x
p=argparse.ArgumentParser();p.add_argument('--test',choices=SHOTS,required=True);p.add_argument('--width',type=int,default=360);p.add_argument('--tag',default='P01');a=p.parse_args();fn,dur=SHOTS[a.test];name=f'{a.test}_{dur:g}s_{a.tag}_{a.width}';out=R/'previews'/(name+'.mp4');assert not out.exists();n=round(dur*30);w=a.width;h=round(w*16/9);encoder=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE);rasters=[DepthRaster(w,h//2 if a.test=='STEERING_TURN' else h) for _ in range(2)];states=[];samples=[];producer_snapshot={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').rglob('*.py') if '__pycache__' not in p.parts}
for f in range(n):
 worlds,d=fn(f/30);images=[rasters[j].render(world) for j,world in enumerate(worlds)];im=Image.new('RGB',(w,h),'#091b2a')
 for j,img in enumerate(images):im.paste(img,(0,j*h//2 if len(images)==2 else 0))
 if len(images)==2:
  draw=ImageDraw.Draw(im);draw.rectangle((0,h//2-1,w,h//2+1),fill='#e6bc7b');draw.text((5,5),'COCKPIT / SHARED STATE',fill='#e3d4b6');draw.text((5,h//2+5),'FIXED ROAD CAMERA / SAME TIME',fill='#e3d4b6')
 encoder.stdin.write(im.tobytes());states.append(conv(d))
 if f%6==0:samples.append((f,im.resize((135,240))))
 if f in [0,n//2,n-1]:im.save(R/'reviews'/f'{name}_{f:03}.png')
 if f%30==0:print(name,f,'/',n,flush=True)
encoder.stdin.close();assert encoder.wait()==0
sheet=Image.new('RGB',(810,262*math.ceil(len(samples)/6)),'#091b2a');dr=ImageDraw.Draw(sheet)
for j,(f,im) in enumerate(samples):x=j%6*135;y=j//6*262;sheet.paste(im,(x,y));dr.text((x+4,y+242),f'{f}/ {f/30:.2f}s',fill='white')
sheet.save(R/'reviews'/f'{name}_MOTION.jpg',quality=94)
(R/'reports'/f'{name}_STATE.json').write_text(json.dumps({'test':a.test,'file':str(out.relative_to(R)),'duration':dur,'fps':30,'frames':n,'width':w,'height':h,'silent_diagnostic':True,'state':states,'source_sha256':producer_snapshot,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=1));print('COMPLETE',out,flush=True)
