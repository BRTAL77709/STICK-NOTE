from pathlib import Path
import base64,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];video=R/'renders/NOIRFRAME_THREE_SHOT_REVIEW_540_R2.mp4'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=b.new_page(viewport={'width':540,'height':960});page.set_content('<video id="v" playsinline style="width:540px;height:960px"></video>');page.evaluate('s=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(s),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(video.read_bytes()).decode());page.wait_for_function('v.readyState===4');page.wait_for_timeout(600)
 r=page.evaluate('''async()=>{let start=performance.now();await v.play();await new Promise((ok,fail)=>{v.onended=ok;v.onerror=()=>fail(v.error.message);setTimeout(()=>fail('Playback timeout'),30000)});let q=v.getVideoPlaybackQuality();return {ended:v.ended,duration:v.duration,wall_seconds:(performance.now()-start)/1000,total_frames:q.totalVideoFrames,dropped_frames:q.droppedVideoFrames,corrupted_frames:q.corruptedVideoFrames}}''');assert r['ended'] and r['corrupted_frames']==0 and abs(r['duration']-20.8)<.05
 for t in [.5,7.3,19.5]:
  page.evaluate('async t=>{v.currentTime=t;await new Promise(r=>v.onseeked=r)}',t);page.screenshot(path=str(R/f'reviews/REVIEW_REEL_CAPTION_{t}.png'))
 b.close()
r.update(path=str(video.relative_to(R)),rate=1);(R/'reports/remotion-reel-playback.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
