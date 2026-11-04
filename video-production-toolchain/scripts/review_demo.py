from pathlib import Path
import json,base64,os,threading,http.server,functools
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
from io import BytesIO
R=Path(__file__).resolve().parents[1];D=Path(os.environ.get('NOIRFRAME_RUN_DIR',R/'renders'));D=D if D.is_absolute() else R/D;video=D/'NOIRFRAME_TOOLCHAIN_INTEGRATION_DEMO.mp4';states=json.loads((R/'shared/frame-states.json').read_text());checks=[];plays=[]
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=browser.new_page(viewport={'width':1080,'height':1920});page.on('pageerror',lambda e:print('BROWSER ERROR',str(e),flush=True));page.goto(f'http://127.0.0.1:{server.server_port}/hyperframes/index.html');print('HUD DIAGNOSTIC',page.evaluate('({url:location.href,gsap:typeof gsap,timeline:!!window.__timelines,HUD:window.__HUD_STATE,ready:document.readyState})'),flush=True);page.wait_for_function('!!window.__timelines?.main',polling=100)
 for frame in [90,91,105,120,150,180,209]:
  t=(frame-90)/30;page.evaluate('(t)=>{window.__timelines.main.time(t,false);}',t);actual=page.evaluate('window.__HUD_STATE');expect=states[frame]['state'];assert actual['globalFrame']==frame and abs(actual['speed']-expect['speed_kmh'])<1e-8 and abs(actual['distance']-expect['distance_m'])<1e-8;checks.append(actual)
 for rate in [1,.5]:
  page.set_content('<video id="v" playsinline style="height:960px"></video>');page.evaluate('b=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(b),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(video.read_bytes()).decode());page.wait_for_function('v.readyState===4');page.evaluate('(r)=>v.playbackRate=r',rate)
  data=page.evaluate('''async()=>{let start=performance.now(),samples=[],last=-1,done=false;const c=document.createElement('canvas');c.width=216;c.height=384;const x=c.getContext('2d');function cb(now,m){if(m.mediaTime-last>=.22){last=m.mediaTime;x.drawImage(v,0,0,216,384);samples.push({time:m.mediaTime,jpeg:c.toDataURL('image/jpeg',.85)})}if(!done)v.requestVideoFrameCallback(cb)}v.requestVideoFrameCallback(cb);await v.play();await new Promise((ok,bad)=>{v.onended=ok;v.onerror=()=>bad(v.error.message);setTimeout(()=>bad('Timeout'),22000)});done=true;let q=v.getVideoPlaybackQuality();return {ended:v.ended,rate:v.playbackRate,duration:v.duration,wallSeconds:(performance.now()-start)/1000,dropped:q.droppedVideoFrames,corrupted:q.corruptedVideoFrames,total:q.totalVideoFrames,samples}}''');samples=data.pop('samples');assert data['ended'] and data['corrupted']==0 and data['duration']==7;plays.append(data);sheet=Image.new('RGB',(1296,410*((len(samples)+5)//6)),'#071521');draw=ImageDraw.Draw(sheet)
  for j,s in enumerate(samples):sheet.paste(Image.open(BytesIO(base64.b64decode(s['jpeg'].split(',')[1]))),(j%6*216,j//6*410));draw.text((j%6*216+5,j//6*410+390),f"{s['time']:.2f}s",fill='white')
  sheet.save(R/f'reviews/PLAYBACK_{rate}x.jpg',quality=93)
 browser.close()
server.shutdown()
(R/'reports/playback-and-hud-sync.json').write_text(json.dumps({'ok':True,'HUD_shared_frame_checks':checks,'playback':plays,'listening_verified':False,'artistic_approval':'not claimed'},indent=2));print(json.dumps(plays,indent=2))
