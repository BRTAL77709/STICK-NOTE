from pathlib import Path
import subprocess,json,base64,math,argparse
from PIL import Image,ImageDraw
from io import BytesIO
R=Path(__file__).resolve().parents[1]
def one(v,t,w=216,h=384):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(v),'-frames:v','1','-vf',f'scale={w}:{h}','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);return Image.frombytes('RGB',(w,h),b)
def sheets(v):
 shots=json.loads((R/'storyboard.json').read_text());out=Image.new('RGB',(1296,1230),'#07131e');d=ImageDraw.Draw(out)
 for j,s in enumerate(shots):
  t=(s['start']+s['end'])/2;out.paste(one(v,t),(j%6*216,j//6*410));d.text((j%6*216+5,j//6*410+388),f"S{s['scene']:02d} / {t:.2f}s",fill='white')
 out.save(R/'CONTACT_SHEET_18_SCENES.jpg',quality=94)
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-vf','fps=1,scale=216:384','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);n=216*384*3;frames=[Image.frombytes('RGB',(216,384),b[i:i+n]) for i in range(0,len(b),n)];out=Image.new('RGB',(1296,410*math.ceil(len(frames)/6)),'#07131e');d=ImageDraw.Draw(out)
 for j,im in enumerate(frames):out.paste(im,(j%6*216,j//6*410));d.text((j%6*216+5,j//6*410+388),f'{j+.5:.1f}s',fill='white')
 out.save(R/'CONTACT_SHEET_FULL.jpg',quality=93)
 # Quarter-second action strips cover the interacting systems and physical chase.
 groups=[(28.5,30),(32,33.5),(38.25,39.75),(48,49.5),(49.2,50.7),(51.1,52.6),(53.1,54.6),(54.5,56),(56,57.5),(57.4,58.9),(59.2,60.7),(61.35,62.85),(63.6,65.1),(65.5,67),(67.8,69.3),(76.8,78.3)];out=Image.new('RGB',(1512,len(groups)*410),'#07131e');d=ImageDraw.Draw(out)
 for row,(start,end) in enumerate(groups):
  for j in range(7):
   t=start+j*.25;out.paste(one(v,t),(j*216,row*410));d.text((j*216+4,row*410+388),f'{t:.2f}s',fill='white')
 out.save(R/'ACTION_CONTACT_STRIPS.jpg',quality=93)
def playback(v,label):
 from playwright.sync_api import sync_playwright
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=b.new_page(viewport={'width':650,'height':1000});page.set_content('<video id="v" style="height:960px" playsinline preload="auto"></video>');page.evaluate('b64=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(v.read_bytes()).decode());page.wait_for_function('v.readyState===4');page.wait_for_timeout(5000)
  res=page.evaluate('''async()=>{let start=performance.now(),samples=[],last=-1,done=false;const c=document.createElement('canvas');c.width=144;c.height=256;const x=c.getContext('2d');function cb(now,m){if(m.mediaTime-last>=1.9){last=m.mediaTime;x.drawImage(v,0,0,144,256);samples.push({time:m.mediaTime,jpeg:c.toDataURL('image/jpeg',.80)});}if(!done)v.requestVideoFrameCallback(cb);}v.requestVideoFrameCallback(cb);await v.play();await new Promise((ok,bad)=>{v.onended=ok;v.onerror=()=>bad(v.error.message);setTimeout(()=>bad('Playback timeout'),102000)});done=true;const q=v.getVideoPlaybackQuality();return {ended:v.ended,rate:v.playbackRate,currentTime:v.currentTime,duration:v.duration,wallTime:(performance.now()-start)/1000,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,corruptedFrames:q.corruptedVideoFrames,samples};}''');b.close()
 samples=res.pop('samples');out=Image.new('RGB',(1152,280*math.ceil(len(samples)/8)),'#07131e');d=ImageDraw.Draw(out)
 for j,s in enumerate(samples):out.paste(Image.open(BytesIO(base64.b64decode(s['jpeg'].split(',')[1]))),(j%8*144,j//8*280));d.text((j%8*144+4,j//8*280+260),f"{s['time']:.2f}s",fill='white')
 out.save(R/'renders/previews'/f'{label}_PRESENTED.jpg',quality=93);res['presented_sample_times']=[s['time'] for s in samples];(R/'reports'/f'{label}_playback.json').write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='presented_sample_times'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--play',action='store_true');p.add_argument('--label',default='MASTER');a=p.parse_args();v=R/a.video
 if a.play:playback(v,a.label)
 else:sheets(v)
