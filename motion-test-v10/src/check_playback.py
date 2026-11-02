"""Play the actual encoded MP4 at 1x in Chromium; capture frames presented by playback."""
import sys,json,base64,math
from pathlib import Path
from PIL import Image,ImageDraw
from io import BytesIO
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
(root/'previews').mkdir(parents=True,exist_ok=True)
video=Path(sys.argv[1]).resolve();label=sys.argv[2]
player=root/'previews'/f'{label}_player.html'
player.write_text('<!doctype html><meta charset="utf-8"><body style="margin:0;background:#06101b"><video id="v" style="height:960px" preload="auto" playsinline src="'+video.as_uri()+'"></video>')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-crash-reporter','--disable-breakpad','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
 page=b.new_page(viewport={'width':600,'height':1000});page.set_content('<video id="v" style="height:960px" playsinline preload="auto"></video>')
 page.evaluate('b64=>{const a=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));v.src=URL.createObjectURL(new Blob([a],{type:"video/mp4"}));v.load();}',base64.b64encode(video.read_bytes()).decode());page.wait_for_function('v.readyState>=4');page.wait_for_timeout(1500)
 result=page.evaluate('''async()=>{
 const v=document.querySelector('video');const c=document.createElement('canvas');c.width=216;c.height=384;const ctx=c.getContext('2d');const frames=[];let next=0;let last=-1;
 const start=performance.now();v.playbackRate=1;
 const cb=(now,m)=>{if(m.mediaTime>=next){ctx.drawImage(v,0,0,216,384);frames.push({time:m.mediaTime,presented:m.presentedFrames,image:c.toDataURL('image/png')});next=m.mediaTime+.095;}last=m.mediaTime;if(!v.ended)v.requestVideoFrameCallback(cb);};
 v.requestVideoFrameCallback(cb);
 const done=new Promise((resolve,reject)=>{v.onended=resolve;v.onerror=()=>reject(new Error('video playback error '+v.error.code));});
 await v.play();await done;const q=v.getVideoPlaybackQuality();return {ended:v.ended,currentTime:v.currentTime,duration:v.duration,rate:v.playbackRate,wallTime:(performance.now()-start)/1000,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,corruptedFrames:q.corruptedVideoFrames,lastPresentedTime:last,frames};
}''')
 b.close()
frames=result.pop('frames');assert result['ended'] and abs(result['duration']-10)<.05
for title,chosen,cols in [('playback',frames,5),('reaction',[x for x in frames if 7.95<=x['time']<=9.95],5)]:
 sheet=Image.new('RGB',(216*cols,410*math.ceil(len(chosen)/cols)),'#06101b');draw=ImageDraw.Draw(sheet)
 for i,f in enumerate(chosen):
  im=Image.open(BytesIO(base64.b64decode(f['image'].split(',')[1])));x=i%cols*216;y=i//cols*410;sheet.paste(im,(x,y));draw.text((x+8,y+388),f"{f['time']:.3f}s",fill='white')
 sheet.save(root/'previews'/f'{label}_{title}.jpg',quality=93)
result['sampled_presented_frames']=[{'time':f['time'],'presented':f['presented']} for f in frames]
(root/'previews'/f'{label}_playback.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='sampled_presented_frames'},indent=2))
