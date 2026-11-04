from pathlib import Path
import json,subprocess,base64,math,argparse
from PIL import Image,ImageDraw
from io import BytesIO
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',default='preview');p.add_argument('--proofs',default='ABCDE');p.add_argument('--play',action='store_true');a=p.parse_args()
 for k in a.proofs:
  d=R/'proofs'/k;m=json.loads((d/(a.stage+'.json')).read_text());v=R/m['path'];probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_streams','-of','json',str(v)]))['streams'][0];assert int(probe['nb_read_frames'])==m['frames'];assert probe['r_frame_rate']=='30/1';subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],check=True)
  if not a.play:
   out=Image.new('RGB',(1296,820),'#07131e');dr=ImageDraw.Draw(out)
   for j in range(12):
    t=min(m['duration']-1/30,j*m['duration']/11);b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(v),'-frames:v','1','-vf','scale=216:384','-f','image2pipe','-vcodec','png','pipe:1']);x=j%6*216;y=j//6*410;out.paste(Image.open(BytesIO(b)),(x,y));dr.text((x+4,y+388),f'{k} {t:.2f}s',fill='white')
   out.save(d/(a.stage+'_CONTACT_SHEET.jpg'),quality=94);continue
  from playwright.sync_api import sync_playwright
  with sync_playwright() as pw:
   b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);page=b.new_page(viewport={'width':500,'height':920});page.set_content('<video id="v" style="height:880px" muted playsinline></video>');page.evaluate('data=>{v.src=URL.createObjectURL(new Blob([Uint8Array.from(atob(data),c=>c.charCodeAt(0))],{type:"video/mp4"}));v.load()}',base64.b64encode(v.read_bytes()).decode());page.wait_for_function('v.readyState===4');reports=[]
   for rate in [1,.5]:
    report=page.evaluate('''async rate=>{v.currentTime=0;v.playbackRate=rate;await new Promise(r=>{if(v.readyState>=3)r();else v.oncanplay=r});let frames=[],last=-1,done=false,start=performance.now();let c=document.createElement('canvas');c.width=144;c.height=256;let ctx=c.getContext('2d');function cb(n,m){if(m.mediaTime-last>.15){last=m.mediaTime;ctx.drawImage(v,0,0,144,256);frames.push({time:m.mediaTime,image:c.toDataURL('image/jpeg',.85)});}if(!done)v.requestVideoFrameCallback(cb);}v.requestVideoFrameCallback(cb);await v.play();await new Promise((ok,bad)=>{v.onended=ok;v.onerror=()=>bad('decode');setTimeout(()=>bad('timeout'),40000)});done=true;let q=v.getVideoPlaybackQuality();return {ended:v.ended,rate:v.playbackRate,duration:v.duration,wallTime:(performance.now()-start)/1000,totalFrames:q.totalVideoFrames,dropped:q.droppedVideoFrames,corrupted:q.corruptedVideoFrames,frames};}''',rate);frames=report.pop('frames');out=Image.new('RGB',(1152,280*math.ceil(len(frames)/8)),'#07131e');dr=ImageDraw.Draw(out)
    for j,f in enumerate(frames):x=j%8*144;y=j//8*280;out.paste(Image.open(BytesIO(base64.b64decode(f['image'].split(',')[1]))),(x,y));dr.text((x+3,y+260),f'{f["time"]:.2f}s',fill='white')
    out.save(d/f'{a.stage}_PRESENTED_{rate:g}x.jpg',quality=93);report['sample_times']=[f['time'] for f in frames];report['path']=m['path'];assert report['ended'] and report['corrupted']==0;reports.append(report)
   b.close();(d/(a.stage+'_PLAYBACK.json')).write_text(json.dumps(reports,indent=2));print(k,a.stage,'normal and slow completed',flush=True)
if __name__=='__main__':main()
