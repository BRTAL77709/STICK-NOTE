"""Play the complete86-second encoded film at1x; retain actual presented-frame evidence."""
import sys,json,base64,math
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1];video=Path(sys.argv[1]).resolve();label=sys.argv[2];shots=json.loads((r/'storyboard.json').read_text())
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-crash-reporter','--disable-breakpad','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=b.new_page(viewport={'width':600,'height':1000});page.set_content('<video id="v" style="height:960px" playsinline preload="auto"></video>')
 page.evaluate('b64=>{const a=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));v.src=URL.createObjectURL(new Blob([a],{type:"video/mp4"}));v.load();}',base64.b64encode(video.read_bytes()).decode());page.wait_for_function('v.readyState>=4');page.wait_for_timeout(1800)
 result=page.evaluate('''async()=>{const v=document.querySelector('video');const c=document.createElement('canvas');c.width=216;c.height=384;const ctx=c.getContext('2d');const frames=[];let next=0;let last=-1;const start=performance.now();v.playbackRate=1;
 const cb=(now,m)=>{if(m.mediaTime>=next){ctx.drawImage(v,0,0,216,384);frames.push({time:m.mediaTime,presented:m.presentedFrames,image:c.toDataURL('image/png')});next=m.mediaTime+.45;}last=m.mediaTime;if(!v.ended)v.requestVideoFrameCallback(cb);};v.requestVideoFrameCallback(cb);
 const done=new Promise((resolve,reject)=>{v.onended=resolve;v.onerror=()=>reject(new Error('video error '+v.error.code));});await v.play();await done;const q=v.getVideoPlaybackQuality();return {ended:v.ended,currentTime:v.currentTime,duration:v.duration,rate:v.playbackRate,wallTime:(performance.now()-start)/1000,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,corruptedFrames:q.corruptedVideoFrames,lastPresentedTime:last,frames};}''');b.close()
frames=result.pop('frames');assert result['ended'] and abs(result['duration']-86)<.03
folder=r/'previews'/f'{label}_presented';folder.mkdir(exist_ok=True);selected=[]
for shot in shots:
 chosen=[f for f in frames if shot['start']<=f['time']<shot['end']];assert chosen,shot
 sheet=Image.new('RGB',(216*5,410*math.ceil(len(chosen)/5)),'#06101b');d=ImageDraw.Draw(sheet)
 for j,f in enumerate(chosen):
  im=Image.open(BytesIO(base64.b64decode(f['image'].split(',')[1])));x=j%5*216;y=j//5*410;sheet.paste(im,(x,y));d.text((x+7,y+388),f'{f["time"]:.3f}s',fill='white')
 sheet.save(folder/f'scene_{shot["scene"]:02d}.jpg',quality=92)
 for fraction in [.2,.5,.8]:selected.append(min(chosen,key=lambda f:abs(f['time']-(shot['start']+shot['duration']*fraction))))
sheet=Image.new('RGB',(1296,410*9),'#06101b');d=ImageDraw.Draw(sheet)
for j,f in enumerate(selected):
 im=Image.open(BytesIO(base64.b64decode(f['image'].split(',')[1])));x=j%6*216;y=j//6*410;sheet.paste(im,(x,y));d.text((x+7,y+388),f'{f["time"]:.3f}s',fill='white')
sheet.save(r/'previews'/f'{label}_playback_contact.jpg',quality=94)
result['sampled_presented_frames']=[{'time':f['time'],'presented':f['presented']} for f in frames];(r/'previews'/f'{label}_playback.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='sampled_presented_frames'},indent=2))
