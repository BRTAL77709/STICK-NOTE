"""Stream decoded frames into contact sheets; assemble unretimed before/after tests."""
from pathlib import Path
import subprocess,json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]; old=R.parent/'NOIRFRAME_V12_CINEMATIC_REBUILD/previews'
rows=json.loads((R/'CURRENT_SHOTS.json').read_text());index={};media={}
original={'STAIR_CONTACT':('STAIRS_V12_F01_1080.mp4',6.4),'KEY_HANDLE':('HOUSE_V12_F01_1080.mp4',5.05),'STEERING_TURN':('DRIVING_V12_F03_1080.mp4',2.5)}
def run(cmd):subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
for k,row in rows.items():
 p=R/row['final'];n=round(row['duration']*30)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));v=probe['streams'][0]
 assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],int(v['nb_read_frames']))==(1080,1920,'h264','30/1',n)
 assert abs(float(probe['format']['duration'])-row['duration'])<.001
 run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'])
 media[k]={'path':row['final'],'frames':n,'duration':row['duration'],'width':1080,'height':1920,'fps':30,'codec':'h264','full_decode':'clean','silent':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 before,start=original[k];out=R/'comparisons'/f'{k}_V12_vs_CONTACT_M01.mp4';out.parent.mkdir(exist_ok=True)
 filt="[0:v]scale=540:960,setsar=1,setpts=PTS-STARTPTS[a];[1:v]scale=540:960,setsar=1,setpts=PTS-STARTPTS[b];[a][b]hstack,pad=1080:1080:0:120:color=0x071521,drawtext=text='REJECTED V12                  CONTACT TEST - UNAPPROVED':x=20:y=25:fontsize=25:fontcolor=white,drawtext=text='Normal speed / no retiming':x=20:y=70:fontsize=24:fontcolor=white[v]"
 if not out.exists():run(['ffmpeg','-v','error','-n','-ss',str(start),'-i',str(old/before),'-i',str(p),'-filter_complex_threads','1','-filter_complex',filt,'-map','[v]','-t',str(row['duration']),'-r','30','-an','-c:v','libx264','-crf','20','-preset','fast','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(out)])
 row['comparison']=str(out.relative_to(R));row['original']={'path':str((old/before).relative_to(R.parent)),'start':start,'duration':row['duration'],'speed':1}
 # Every decoded frame, not just selected poses. Close crops supplement the full motion sheet.
 crops={'STAIR_CONTACT':{'FEET':(180,610,910,1490)},'KEY_HANDLE':{'KEY_HANDLE':(210,580,850,1280)},'STEERING_TURN':{'WHEEL':(160,180,850,750),'PEDALS':(150,480,850,960),'ROAD':(0,960,1080,1920)}}[k]
 sheets={};pages={name:[] for name in crops}
 dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(p),'-f','rawvideo','-pix_fmt','rgb24','-threads','1','pipe:1'],stdout=subprocess.PIPE)
 for f in range(n):
  raw=dec.stdout.read(1080*1920*3);assert len(raw)==1080*1920*3
  im=Image.frombytes('RGB',(1080,1920),raw)
  for name,box in crops.items():
   if f%30==0:sheets[name]=Image.new('RGB',(1000,6*262),'#071521')
   tile=im.crop(box);tile.thumbnail((200,236));x=f%5*200;y=(f%30)//5*262;sheets[name].paste(tile,(x+(200-tile.width)//2,y));ImageDraw.Draw(sheets[name]).text((x+3,y+240),f'frame {f:03} / {f/30:.3f}s',fill='white')
   if f%30==29 or f==n-1:
    dst=R/'reviews'/f'{k}_{name}_CONTACT_DETAIL_ALL_FRAMES_{f//30+1:02}.jpg';sheets[name].save(dst,quality=90);pages[name].append(str(dst.relative_to(R)))
 assert dec.wait()==0
 index[k]={'all_frames':n,'fps':30,'pages':pages,'limitation':'Cropped rendered-frame inspection, supplemented by geometric contact CSV. Hidden surfaces are not certified.'}
(R/'CURRENT_SHOTS.json').write_text(json.dumps(rows,indent=2));(R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(media,indent=2));(R/'reports/FRAME_INSPECTION.json').write_text(json.dumps(index,indent=2))
