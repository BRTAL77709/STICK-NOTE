"""Normal-rate playback without JPEG capture overhead; preserve capture diagnostics separately."""
from pathlib import Path
import base64,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];v=R/'THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=b.new_page(viewport={'width':650,'height':1000});page.set_content('<video id="v" style="height:960px" playsinline preload="auto"></video>');page.evaluate('b64=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(b64),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(v.read_bytes()).decode());page.wait_for_function('v.readyState===4');page.wait_for_timeout(5000)
 result=page.evaluate('''async()=>{let start=performance.now(),times=[];let done=false;function cb(now,m){times.push(m.mediaTime);if(!done)v.requestVideoFrameCallback(cb);}v.requestVideoFrameCallback(cb);await v.play();await new Promise((ok,bad)=>{v.onended=ok;v.onerror=()=>bad(v.error.message);setTimeout(()=>bad('Playback timeout'),22000)});done=true;const q=v.getVideoPlaybackQuality();return {ended:v.ended,rate:v.playbackRate,duration:v.duration,currentTime:v.currentTime,wallTime:(performance.now()-start)/1000,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,corruptedFrames:q.corruptedVideoFrames,presentedTimes:times};}''');b.close()
(R/'reports/V4_ISOLATED_playback.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='presentedTimes'},indent=2))
