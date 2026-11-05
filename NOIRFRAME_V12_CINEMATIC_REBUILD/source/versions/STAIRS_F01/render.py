"""Reproducible streamed depth-rendered illustrated animation, not PNG sliding."""
from pathlib import Path
import argparse,json,hashlib,subprocess,math,wave
import numpy as np
from PIL import Image,ImageDraw
from scenes import SCENES,DURATIONS
from depth_render import DepthRaster
from vehicles import rain_overlay
R=Path(__file__).resolve().parents[1]
def conv(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,(np.floating,np.integer)):return x.item()
 if isinstance(x,dict):return {k:conv(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [conv(v) for v in x]
 return x

def main():
 p=argparse.ArgumentParser();p.add_argument('--shot',choices=SCENES,required=True);p.add_argument('--width',type=int,default=360);p.add_argument('--tag',default='P01');a=p.parse_args();k=a.shot;dur=DURATIONS[k];n=round(dur*30);w=a.width;h=round(w*16/9);name=f'{k}_V12_{a.tag}_{w}';out=R/'previews'/f'{name}.mp4';assert not out.exists(),out
 rng=np.random.default_rng(1212);sr=48000;audio=np.zeros(round(dur*sr));events=[];states=[];samples=[];rr=DepthRaster(w);prev=None
 # Diagnostic event audio created alongside evaluated movement, not arbitrary subtitles.
 enc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(out.with_suffix('.silent.mp4'))],stdin=subprocess.PIPE)
 for f in range(n):
  t=f/30;s,d,world=SCENES[k](t);overlay=(lambda art:rain_overlay(art,t,80)) if ((k=='HOUSE' and d['camera_view']=='porch') or (k=='DRIVING' and d['view']!='pedal insert')) else None
  im=rr.render(world,overlay);enc.stdin.write(im.tobytes());states.append(conv(d))
  if f%15==0:samples.append((t,im.resize((135,240))))
  if f in {0,n//4,n//2,n*3//4,n-1}:im.save(R/'reviews'/f'{name}_{f:04}.png');(R/'assets'/f'{name}_{f:04}.svg').write_text(s)
  if 'pose' in d and prev is not None:
   for j,leg in enumerate(d['pose']['legs']):
    if leg['planted'] and not prev['pose']['legs'][j]['planted']:events.append({'time':t,'kind':'foot plant','leg':j})
  prev=d
  if f%30==0:print(name,f,'/',n,flush=True)
 enc.stdin.close();assert enc.wait()==0
 if k=='HOUSE':events +=[{'time':t,'kind':v} for t,v in [(3.92,'locked handle'),(4.75,'key'),(5.94,'insert'),(6.48,'unlock'),(7.18,'store'),(11.3,'door closes'),(11.98,'bolt')]]
 if k=='BEDROOM':events +=[{'time':t,'kind':v} for t,v in [(2.35,'pinch'),(2.65,'cloth'),(4.45,'cloth settles')]]
 for ev in events:
  start=round(ev['time']*sr);count=min(round(.15*sr),len(audio)-start)
  if count<=0:continue
  tt=np.arange(count)/sr;xx=(np.sin(2*np.pi*82*tt)*.45+rng.normal(0,1,count)*.22)*np.exp(-tt*33);audio[start:start+count]+=xx*.11
 if k=='DRIVING':
  for f,d in enumerate(states):
   lo=f*1600;tt=np.arange(1600)/sr+f/30;freq=45+d['speed_mps']*3;audio[lo:lo+1600]+=.025*np.sin(2*np.pi*freq*tt)+.015*np.sin(2*np.pi*freq*2*tt)
 audio+=rng.normal(0,.004,len(audio));wav=R/'assets'/f'{name}_FX.wav'
 with wave.open(str(wav),'wb') as wf:wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(out.with_suffix('.silent.mp4')),'-i',str(wav),'-c:v','copy','-c:a','aac','-b:a','128k','-t',str(dur),'-movflags','+faststart',str(out)],check=True);out.with_suffix('.silent.mp4').unlink()
 sheet=Image.new('RGB',(945,262*math.ceil(len(samples)/7)),'#081c29');dr=ImageDraw.Draw(sheet)
 for j,(t,im) in enumerate(samples):x=j%7*135;y=j//7*262;sheet.paste(im,(x,y));dr.text((x+3,y+242),f'{t:.2f}s',fill='white')
 sheet.save(R/'reviews'/f'{name}_CONTACT.jpg',quality=92)
 (R/'reports'/f'{name}_STATE.json').write_text(json.dumps({'shot':k,'file':str(out.relative_to(R)),'fps':30,'frames':n,'duration':dur,'width':w,'height':h,'state':states,'events':events,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').rglob('*.py') if '__pycache__' not in str(p)}},indent=1));print('COMPLETE',out,flush=True)
if __name__=='__main__':main()
