"""Encoded contact sheets and actual1x playback, independent of source frame generation."""
from pathlib import Path
import argparse,subprocess,json,math,base64
from io import BytesIO
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def contact(video,label,step=.5):
 fps=30;duration=15
 vf=f'fps={1/step},scale=216:384';raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf',vf,'-pix_fmt','rgb24','-f','rawvideo','pipe:1'])
 frames=[Image.frombytes('RGB',(216,384),raw[i:i+216*384*3]) for i in range(0,len(raw),216*384*3)];out=Image.new('RGB',(1296,410*math.ceil(len(frames)/6)),'#08131c');d=ImageDraw.Draw(out)
 for j,im in enumerate(frames):
  x=j%6*216;y=j//6*410;out.paste(im,(x,y));d.text((x+7,y+388),f'{j*step+step/2:.3f}s',fill='white')
 dest=ROOT/'previews'/f'{label}_contact.jpg';assert not dest.exists();out.save(dest,quality=95);return dest

def playback(video,label):
 from playwright.sync_api import sync_playwright
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-crash-reporter','--disable-breakpad','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=b.new_page(viewport={'width':650,'height':1000});page.set_content('<video id="v" style="height:960px" playsinline preload="auto"></video>')
  page.evaluate('b64=>{const a=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));v.src=URL.createObjectURL(new Blob([a],{type:"video/mp4"}));v.load();}',base64.b64encode(video.read_bytes()).decode());page.wait_for_function('v.readyState>=4');page.wait_for_timeout(3000)
  result=page.evaluate('''async()=>{let snaps=[];let done=false;let t0=performance.now();let last=-1;let c=document.createElement('canvas');c.width=216;c.height=384;let x=c.getContext('2d');function cb(now,m){if(m.mediaTime-last>.23){last=m.mediaTime;x.drawImage(v,0,0,216,384);snaps.push({time:m.mediaTime,jpeg:c.toDataURL('image/jpeg',.88)});}if(!done)v.requestVideoFrameCallback(cb);}v.requestVideoFrameCallback(cb);await v.play();await new Promise((ok,bad)=>{v.onended=ok;v.onerror=()=>bad(v.error?.message);setTimeout(()=>bad('Playback timeout'),22000);});done=true;let q=v.getVideoPlaybackQuality();return {ended:v.ended,currentTime:v.currentTime,duration:v.duration,rate:v.playbackRate,wallTime:(performance.now()-t0)/1000,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,corruptedFrames:q.corruptedVideoFrames,snaps};}''')
  b.close()
 snaps=result.pop('snaps');out=Image.new('RGB',(1296,410*math.ceil(len(snaps)/6)),'#06101b');d=ImageDraw.Draw(out)
 for j,s in enumerate(snaps):
  im=Image.open(BytesIO(base64.b64decode(s['jpeg'].split(',')[1])));x=j%6*216;y=j//6*410;out.paste(im,(x,y));d.text((x+6,y+388),f"{s['time']:.3f}s",fill='white')
 out.save(ROOT/'previews'/f'{label}_presented.jpg',quality=94);result['presented_sample_times']=[s['time'] for s in snaps];dest=ROOT/'reports'/f'{label}_playback.json';assert not dest.exists();dest.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='presented_sample_times'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('label');p.add_argument('--play',action='store_true');p.add_argument('--step',type=float,default=.5);a=p.parse_args();video=ROOT/a.video
 if a.play:playback(video,a.label)
 else:print(contact(video,a.label,a.step))
