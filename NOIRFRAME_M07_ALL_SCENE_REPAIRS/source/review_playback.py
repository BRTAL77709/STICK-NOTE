from pathlib import Path
import json,base64,math,argparse
from io import BytesIO
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--stage',choices=['preview','final','diagnostic'],default='preview');p.add_argument('--rates',type=float,nargs='*',default=[1,.5]);p.add_argument('--tag',default='');p.add_argument('--shots',nargs='*');args=p.parse_args();rows=json.loads((R/'CURRENT_SHOTS.json').read_text());reports={};rows={k:v for k,v in rows.items() if not args.shots or k in args.shots};tag=(args.tag+'_') if args.tag else ''
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=browser.new_page(viewport={'width':650,'height':1000})
 for k,row in rows.items():
  video=R/row[args.stage];plays=[]
  for rate in args.rates:
   page.set_content('<video id="v" playsinline style="height:960px"></video>');page.evaluate('b=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(b),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(video.read_bytes()).decode());page.wait_for_function('v.readyState===4');page.wait_for_timeout(600);page.evaluate('(r)=>{v.playbackRate=r;}',rate)
   d=page.evaluate('''async()=>{const samples=[],c=document.createElement('canvas');c.width=135;c.height=240;const ctx=c.getContext('2d');let last=-1,done=false,start=performance.now();function cb(now,m){if(m.mediaTime-last>=.19){last=m.mediaTime;ctx.drawImage(v,0,0,135,240);samples.push({time:m.mediaTime,jpeg:c.toDataURL('image/jpeg',.90)})}if(!done)v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb);await v.play();await new Promise((resolve,reject)=>{v.onended=resolve;v.onerror=()=>reject(v.error.message);setTimeout(()=>reject('Timeout'),60000)});done=true;let q=v.getVideoPlaybackQuality();return {ended:v.ended,rate:v.playbackRate,duration:v.duration,wallSeconds:(performance.now()-start)/1000,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,corruptedFrames:q.corruptedVideoFrames,samples}}''');samples=d.pop('samples');assert d['ended'] and d['corruptedFrames']==0 and abs(d['duration']-row['duration'])<.002
   sheet=Image.new('RGB',(945,264*math.ceil(len(samples)/7)),'#071521');draw=ImageDraw.Draw(sheet)
   for j,s in enumerate(samples):sheet.paste(Image.open(BytesIO(base64.b64decode(s['jpeg'].split(',')[1]))),(j%7*135,j//7*264));draw.text((j%7*135+4,j//7*264+242),f"{s['time']:.2f}s",fill='white')
   path=R/f'contact_sheets/{k}_{tag}{args.stage}_{rate}x_PRESENTED.jpg';sheet.save(path,quality=94);d.update(path=str(video.relative_to(R)),sample_times=[s['time'] for s in samples],presented_sheet=str(path.relative_to(R)));plays.append(d);print(k,rate,'ended',d['wallSeconds'],'drops',d['droppedFrames'],flush=True)
  reports[k]=plays
 browser.close()
(R/f'reports/{tag}{args.stage}-playback.json').write_text(json.dumps(reports,indent=2))
