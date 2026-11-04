"""Review ONE separately rendered replacement, never assemble the full film."""
from pathlib import Path
import json,subprocess,math,argparse,base64
from io import BytesIO
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];BASE=R.parent/'full-film-v10-quality-rebuild';MASTER=BASE/'renders/final/THE_PRICE_OF_SILENCE_V10_QUALITY_REBUILD_86s.mp4'
def frame(path,t):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=180:320','-f','image2pipe','-vcodec','png','pipe:1']);return Image.open(BytesIO(b)).convert('RGB')
def main():
 p=argparse.ArgumentParser();p.add_argument('scene',type=int);p.add_argument('--stage',default='previews');p.add_argument('--rate',type=float,default=1);args=p.parse_args();s=json.loads((R/'storyboard.json').read_text())[args.scene-1];m=json.loads((R/'scenes'/f'scene_{args.scene:02d}'/f'{args.stage}-cache.json').read_text());v=R/m['path'];tag=f'scene_{args.scene:02d}_{args.stage}_{m["fingerprint"]}'+('_slow' if args.rate!=1 else '')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_streams','-of','json',str(v)]))['streams'][0];assert int(probe['nb_read_frames'])==s['frames'] and probe['r_frame_rate']=='30/1';subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],check=True)
 from playwright.sync_api import sync_playwright
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required']);page=b.new_page(viewport={'width':400,'height':720});page.set_content('<video id="v" style="height:680px" muted playsinline></video>');page.evaluate('b=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(b),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(v.read_bytes()).decode());page.wait_for_function('v.readyState===4');page.evaluate('rate=>v.playbackRate=rate',args.rate);res=page.evaluate('''async()=>{let samples=[],last=-1,done=false,start=performance.now();let c=document.createElement('canvas');c.width=144;c.height=256;let x=c.getContext('2d');function step(n,m){if(m.mediaTime-last>.19){last=m.mediaTime;x.drawImage(v,0,0,144,256);samples.push({time:last,image:c.toDataURL('image/jpeg',.85)});}if(!done)v.requestVideoFrameCallback(step);}v.requestVideoFrameCallback(step);await v.play();await new Promise((ok,bad)=>{v.onended=ok;v.onerror=()=>bad('media error');setTimeout(()=>bad('timeout'),20000)});done=true;let q=v.getVideoPlaybackQuality();return {ended:v.ended,rate:v.playbackRate,mediaTime:v.currentTime,wallTime:(performance.now()-start)/1000,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,corruptedFrames:q.corruptedVideoFrames,samples};}''');b.close()
 samples=res.pop('samples');out=Image.new('RGB',(1152,280*math.ceil(len(samples)/8)),'#07131e');d=ImageDraw.Draw(out)
 for j,f in enumerate(samples):out.paste(Image.open(BytesIO(base64.b64decode(f['image'].split(',')[1]))),(j%8*144,j//8*280));d.text((j%8*144+3,j//8*280+260),f"{f['time']:.2f}s",fill='white')
 out.save(R/'reviews'/f'{tag}_PRESENTED.jpg',quality=94)
 out=Image.new('RGB',(1080,3*350),'#07131e');d=ImageDraw.Draw(out);times=[min(s['duration']-1/30,.06+k*(s['duration']-.10)/8) for k in range(9)]
 for j,t in enumerate(times):
  x=j%3*360;y=j//3*350;out.paste(frame(MASTER,s['start']+t),(x,y));out.paste(frame(v,t),(x+180,y));d.text((x+4,y+322),f'{t:.2f}s BASELINE | REPAIR',fill='white')
 out.save(R/'reviews'/f'{tag}_COMPARE.jpg',quality=94);res.update({'scene':args.scene,'stage':args.stage,'path':m['path'],'frames':int(probe['nb_read_frames']),'size':[probe['width'],probe['height']],'fingerprint':m['fingerprint'],'samples':[f['time'] for f in samples],'visual_approval':'requires inspection; never inferred from playback metrics'})
 (R/'reports'/f'{tag}_playback.json').write_text(json.dumps(res,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='samples'},indent=2))
if __name__=='__main__':main()
