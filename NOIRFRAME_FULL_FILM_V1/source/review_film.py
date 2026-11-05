from pathlib import Path
import json,base64,math
from io import BytesIO
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];video=R/'renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4';reports=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=b.new_page(viewport={'width':540,'height':960})
 for label,rate,start,end in [('FULL_NORMAL',1,0,86),('REPLACEMENTS_SLOW',.5,49.2,69.4)]:
  page.set_content('<video id="v" playsinline style="height:960px"></video>');page.evaluate('s=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(s),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(video.read_bytes()).decode());page.wait_for_function('v.readyState===4');page.wait_for_timeout(600)
  if start:page.evaluate('async t=>{v.currentTime=t;await new Promise(r=>v.onseeked=r)}',start)
  page.evaluate('r=>v.playbackRate=r',rate)
  q=page.evaluate('''async(end)=>{const samples=[],c=document.createElement('canvas');c.width=144;c.height=256;let ctx=c.getContext('2d'),last=-1,done=false,start=performance.now();function cb(now,m){if(m.mediaTime-last>=.48){last=m.mediaTime;ctx.drawImage(v,0,0,144,256);samples.push({time:m.mediaTime,jpeg:c.toDataURL('image/jpeg',.88)})}if(!done)v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb);await v.play();await new Promise((ok,fail)=>{v.onended=ok;v.onerror=()=>fail(v.error.message);v.ontimeupdate=()=>{if(end<85&&v.currentTime>=end){v.pause();ok()}};setTimeout(()=>fail('Playback timeout'),120000)});done=true;let x=v.getVideoPlaybackQuality();return {ended:v.ended,currentTime:v.currentTime,duration:v.duration,rate:v.playbackRate,wall_seconds:(performance.now()-start)/1000,totalFrames:x.totalVideoFrames,droppedFrames:x.droppedVideoFrames,corruptedFrames:x.corruptedVideoFrames,samples}}''',end)
  samples=q.pop('samples');assert q['corruptedFrames']==0 and abs(q['duration']-86)<.002
  if label=='FULL_NORMAL':assert q['ended']
  else:assert q['currentTime']>=end
  sheet=Image.new('RGB',(1008,280*math.ceil(len(samples)/7)),'#06131e');draw=ImageDraw.Draw(sheet)
  for j,x in enumerate(samples):sheet.paste(Image.open(BytesIO(base64.b64decode(x['jpeg'].split(',')[1]))),(j%7*144,j//7*280));draw.text((j%7*144+5,j//7*280+260),f"{x['time']:.2f}s",fill='white')
  path=R/f'reviews/{label}_PRESENTED.jpg';sheet.save(path,quality=94);q.update(path=str(video.relative_to(R)),interval=[start,end],presented_sheet=str(path.relative_to(R)),sample_times=[x['time'] for x in samples]);reports.append(q);print(label,'COMPLETED',q['wall_seconds'],'drops',q['droppedFrames'],flush=True)
 b.close()
(R/'reports/ACTUAL_PLAYBACK.json').write_text(json.dumps(reports,indent=2))
