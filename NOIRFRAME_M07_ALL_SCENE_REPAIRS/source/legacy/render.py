"""Fresh native frames; separate clean and contact-overlay encoders, no footage reuse."""
from pathlib import Path
import argparse,json,subprocess,hashlib,math,gzip
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from shots import SHOTS
from contact_rig import V
from depth_render import DepthRaster
R=Path(__file__).resolve().parents[1]
def conv(q):
 if isinstance(q,np.ndarray):return q.tolist()
 if isinstance(q,np.generic):return q.item()
 if isinstance(q,dict):return {k:conv(v) for k,v in q.items()}
 if isinstance(q,(tuple,list)):return [conv(v) for v in q]
 return q
def diagnostic(im,worlds,d):
 im=im.copy();dr=ImageDraw.Draw(im);s=im.width/1080;cam=worlds[0].cam
 def pt(p):return tuple(v*s for v in cam(p))
 def dot(p,c,r=6):
  x,y=pt(p);dr.ellipse((x-r*s,y-r*s,x+r*s,y+r*s),fill=c)
 if 'pose' in d and not d.get('hide_rig_debug'):
  p=d.get('pose_world',d['pose'])
  for l in p['legs']:
   dr.line([pt(l[x]) for x in ['hip','knee','ankle']],fill='#ffdd65',width=max(1,round(4*s)))
   for x in ['hip','knee','ankle']:dot(l[x],'#ffdd65',5)
   dot(l['sole'],'#6bff99' if l['planted'] else '#f67464',9)
  for a in p['arms']:
   dr.line([pt(a[x]) for x in ['shoulder','elbow','wrist']],fill='#c48bff',width=max(1,round(3*s)))
   dot(a['wrist'],'#c48bff',6)
  dot(p['root'],'#ff8ac5',8)
  if 'com' in d:dot(d['com'],'#ffffff',7)
 if '_trajectory' in d:
  dr.line([pt(q) for q in d['_trajectory']],fill='#ff8ac5',width=max(1,round(2*s)))
 if 'keyhole' in d:
  K=np.array(d['key_R']);q=np.array(d['keyhole'])
  for v,col in [(V(.11,0,0),'#ff7167'),(V(0,.11,0),'#7dff98'),(V(0,0,.16),'#6bbaff')]:dr.line([pt(q),pt(q+K@v)],fill=col,width=max(1,round(3*s)))
 if 'fixed_targets' in d:
  for p in d['fixed_targets']:
   x,y=pt(p);dr.line([(x-8*s,y),(x+8*s,y)],fill='#42ffe4',width=max(1,round(2*s)));dr.line([(x,y-8*s),(x,y+8*s)],fill='#42ffe4',width=max(1,round(2*s)))
 if 'fabric' in d:
  mesh=d['fabric']
  for j in range(0,len(mesh[0]),6):dr.line([pt(q) for q in mesh[:,j]],fill='#ffdd65',width=max(1,round(s)))
 if 'position' in d:
  linespeed=f"v={d['speed']:.2f}m/s steer={math.degrees(d['steer']):.1f}deg gap={d['gap']:.2f}m brake={d['brake']:.2f}"
  dr.text((12*s,im.height-38*s),linespeed,fill='white')
 for name in ['keytip','keyhole','grip','wheel_center']:
  if name in d:dot(d[name],'#42ffe4',7)
 for group in d.get('fingers',[]):
  for f in group:dot(f['pad'],'#42ffe4',4)
 dr.rectangle((0,0,im.width,round(130*s)),fill='#071521');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',max(10,round(24*s)))
 lines=[f"M03 DIAGNOSTIC / {d['time']:.3f}s / {d.get('phase','')}",f"support {d.get('support','')} / treads {d.get('tread_indices','')} / green=contact red=flight"]
 for j,line in enumerate(lines):dr.text((12*s,(12+j*38)*s),line,font=font,fill='white')
 return im

def main():
 p=argparse.ArgumentParser();p.add_argument('--test',choices=SHOTS,required=True);p.add_argument('--width',type=int,default=360);p.add_argument('--tag',default='P01');a=p.parse_args();fn,dur=SHOTS[a.test];n=round(dur*30);width=a.width;height=round(width*16/9);name=f'{a.test}_M03_{a.tag}_{width}';paths=[R/'previews'/(name+'.mp4'),R/'diagnostics'/(name+'_DEBUG.mp4')];assert not any(p.exists() for p in paths)
 procs=[]
 for path in paths:procs.append(subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE))
 raster=DepthRaster(width,height);states=[];sample=[];framesha=[];sources={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').rglob('*.py')};
 trajectory=[fn(i/30)[1]['pose']['root'] for i in range(n)] if a.test=='STAIRS' else None
 for f in range(n):
  worlds,d=fn(f/30)
  if trajectory is not None:d['_trajectory']=trajectory
  im=raster.render(worlds[0]);debug=diagnostic(im,worlds,d)
  for proc,frame in zip(procs,[im,debug]):proc.stdin.write(frame.tobytes())
  d.pop('_trajectory',None);states.append(conv(d));framesha.append(hashlib.sha256(im.tobytes()).hexdigest())
  if f%6==0:sample.append((f,debug.resize((180,320))))
  if f in [0,n//2,n-1]:im.save(R/'reviews'/f'{name}_{f:03}.png')
  if f%30==0:print(name,f,'/',n,flush=True)
 for p in procs:p.stdin.close();assert p.wait()==0
 sheet=Image.new('RGB',(1080,344*math.ceil(len(sample)/6)),'#071521');dr=ImageDraw.Draw(sheet)
 for j,(f,im) in enumerate(sample):x=j%6*180;y=j//6*344;sheet.paste(im,(x,y));dr.text((x+4,y+322),f'{f} / {f/30:.3f}s',fill='white')
 sheet.save(R/'reviews'/f'{name}_STRIP.jpg',quality=92)
 with gzip.open(R/'reports'/f'{name}_STATE.json.gz','wt',compresslevel=6) as fp:fp.write(json.dumps({'test':a.test,'duration':dur,'fps':30,'frames':n,'state':states,'source_sha256':sources,'decoded_source_rgb_hashes':framesha,'video_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}},separators=(',',':')));print('DONE',name,flush=True)
if __name__=='__main__':main()
