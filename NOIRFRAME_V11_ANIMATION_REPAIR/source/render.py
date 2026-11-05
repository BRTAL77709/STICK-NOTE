"""Stream newly evaluated vector rigs to MP4; no images or old film drive animation."""
from pathlib import Path
import sys,argparse,json,subprocess,hashlib,math,wave
import numpy as np
from PIL import Image,ImageDraw
import scenes
from scenes import SCENES,Raster,house,stairs,window,DURATIONS,H_PLANS,S_PLANS,W_PLANS
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--shot',choices=SCENES,required=True);p.add_argument('--width',type=int,default=540);p.add_argument('--version',default='R01');p.add_argument('--wide',action='store_true');a=p.parse_args();k=a.shot;dur=DURATIONS[k];w=a.width;h=round(w*16/9);name=f'{k}_V11_{a.version}_{w}'+('_WIDE' if a.wide else '');out=R/'previews'/f'{name}.mp4';assert not out.exists();scenes.DIAGNOSTIC_WIDE=a.wide
plans={'HOUSE':H_PLANS,'STAIRS':S_PLANS,'WINDOW':W_PLANS}[k];events=[{'time':b,'event':'foot plant','leg':j} for j,row in enumerate(plans) for st,b,target,lift in row]
if k=='HOUSE':events +=[{'time':t,'event':v} for t,v in [(1.92,'locked lever stop'),(2.75,'key leaves pocket'),(3.94,'key enters lock'),(4.48,'lock releases'),(5.18,'key stored'),(5.60,'latch retracts'),(6.95,'door opening stop'),(9.3,'door closes'),(9.98,'inside bolt seats')]]
if k=='WINDOW':events +=[{'time':2.4,'event':'fabric pinch'},{'time':2.65,'event':'fabric pull begins'},{'time':4.4,'event':'fabric settles'},{'time':5.05,'event':'grip releases'}]
sr=48000;n=round(dur*sr);rng=np.random.default_rng(117);noise=lambda nn:rng.normal(0,1,nn);audio=np.convolve(noise(n),np.ones(13)/13,'same')*.007
for e in events:
 pos=round(e['time']*sr);length=min(round(.19*sr),n-pos)
 if length<=0:continue
 t=np.arange(length)/sr
 if e['event']=='foot plant':x=(np.sin(2*np.pi*(76*t-40*t*t))*.45+np.convolve(noise(length),np.ones(5)/5,'same')*.5)*np.exp(-t*31);gain=.08 if k=='HOUSE' else .075
 elif 'fabric' in e['event'] or 'grip' in e['event']:x=np.convolve(noise(length),np.ones(9)/9,'same')*np.exp(-t*20);gain=.055
 else:x=(noise(length)*.6+np.sin(2*np.pi*1200*t)*.2)*np.exp(-t*70);gain=.045 if 'key' in e['event'] else .065
 audio[pos:pos+length]+=x*gain
if k=='WINDOW':
 lo=round(2.65*sr);hi=round(4.4*sr);u=np.arange(hi-lo)/sr;audio[lo:hi]+=np.convolve(noise(hi-lo),np.ones(7)/7,'same')*.025*np.sin(np.pi*u/1.75)
audio*=np.minimum(1,np.arange(n)/(.03*sr))*np.minimum(1,(n-np.arange(n))/(.06*sr));wav=R/'assets'/f'{k}_CONTACT_FX.wav'
if not wav.exists():
 with wave.open(str(wav),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(audio,-.95,.95)*32767).astype('<i2').tobytes())
cmd=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','30','-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-c:a','aac','-b:a','160k','-t',str(dur),'-movflags','+faststart',str(out)];enc=subprocess.Popen(cmd,stdin=subprocess.PIPE);r=Raster(w,h);samples=[];keytimes={'HOUSE':[0,1.8,3.90,4.4,5.15,6.6,7.5,8.8,9.95,10.9],'STAIRS':[0,.74,2.48,4.22,5.96,7.55,8.4],'WINDOW':[0,2.4,3.25,4.4,4.9,5.5,6.7,7.4]}[k];wanted={min(round(dur*30)-1,round(t*30)) for t in keytimes}
def conv(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,(np.floating,np.integer)):return x.item()
 if isinstance(x,dict):return {s:conv(q) for s,q in x.items()}
 if isinstance(x,(tuple,list)):return [conv(q) for q in x]
 return x
states=[]
for f in range(round(dur*30)):
 t=f/30;svg,d=SCENES[k](t);im=r.render(svg);enc.stdin.write(im.tobytes());states.append(conv(d))
 if f in wanted:im.save(R/'reviews'/f'{name}_FRAME_{f:04}.png');(R/'assets'/f'{name}_{f:04}.svg').write_text(svg)
 if f%9==0:samples.append((t,im.resize((144,256))))
 if f%30==0:print(name,f,'/',round(dur*30),flush=True)
enc.stdin.close();assert enc.wait()==0
sheet=Image.new('RGB',(1008,280*math.ceil(len(samples)/7)),'#071521');draw=ImageDraw.Draw(sheet)
for j,(t,im) in enumerate(samples):sheet.paste(im,(j%7*144,j//7*280));draw.text((j%7*144+4,j//7*280+261),f'{t:.2f}s',fill='white')
sheet.save(R/'reviews'/f'{name}_CONTACT.jpg',quality=94);(R/'reports'/f'{name}_WORLD_STATE.json').write_text(json.dumps({'shot':k,'duration':dur,'width':w,'height':h,'fps':30,'frames':len(states),'state':states,'sound_events':events,'file':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_sha256':{f:hashlib.sha256((R/'source'/f).read_bytes()).hexdigest() for f in ['rig.py','actions.py','scenes.py','drawing.py','approved_head.py','svg.py','render.py']}},indent=2));print('COMPLETE',out,flush=True)
