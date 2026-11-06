from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'CURRENT_SHOTS.json').read_text());result={}
for shot,row in rows.items():
 p=R/row['final'];q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in q['streams'] if s['codec_type']=='video');a=next(s for s in q['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],int(v['nb_read_frames']))==(1080,1920,'30/1','h264',round(row['duration']*30));assert abs(float(q['format']['duration'])-row['duration'])<.01
 run=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True);assert run.returncode==0 and not run.stderr,run.stderr
 frames=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf','scale=180:320','-f','rawvideo','-pix_fmt','rgb24','-']);n=len(frames)//(180*320*3);black=[];same=[];previous=None
 import numpy as np
 for i in range(n):
  b=frames[i*180*320*3:(i+1)*180*320*3];im=np.frombuffer(b,np.uint8)
  if np.mean(im)<2:black.append(i)
  if previous==b:same.append(i)
  previous=b
 # All encoded diagnostic frames, ordered inspection pages; no sampling omission.
 dp=R/row['diagnostic'];dd=subprocess.check_output(['ffmpeg','-v','error','-i',str(dp),'-vf','scale=135:240','-f','rawvideo','-pix_fmt','rgb24','-']);dn=len(dd)//(135*240*3);assert dn==n
 pages=[]
 for start in range(0,n,30):
  sheet=Image.new('RGB',(810,1320),'#071521');dr=ImageDraw.Draw(sheet)
  for j in range(start,min(n,start+30)):
   tile=Image.frombytes('RGB',(135,240),dd[j*135*240*3:(j+1)*135*240*3]);x=(j-start)%6*135;y=(j-start)//6*264;sheet.paste(tile,(x,y));dr.text((x+3,y+242),f'{j:03d} / {j/30:.3f}s',fill='white')
  name=f'contact_sheets/{shot}_ALL_FRAMES_{start//30+1:02}.jpg';sheet.save(R/name,quality=86);pages.append(name)
 result[shot]={'path':row['final'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'frames':n,'duration_s':float(q['format']['duration']),'width':1080,'height':1920,'fps':30,'codec':'h264','audio_codec':a['codec_name'],'full_decode_errors':0,'black_frame_indices':black,'identical_adjacent_thumbnail_frames':same,'diagnostic_frame_count':dn,'diagnostic_all_frame_contact_sheets':pages,'technical_status':'TECHNICAL PASS' if not black else 'TECHNICAL FAIL','artistic_status':'ARTISTIC REVIEW REQUIRED'}
 print('MEDIA_CHECKED',shot,n,flush=True)
(R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(result,indent=2))
