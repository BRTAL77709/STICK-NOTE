from pathlib import Path
import json,subprocess,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'CURRENT_SHOTS.json').read_text());row=rows['STAIRS'];media={}
for variant in ['final','diagnostic']:
 p=R/row[variant];q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));v=q['streams'][0];assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']),v['codec_name'])==(1080,1920,'30/1',150,'h264');assert abs(float(q['format']['duration'])-5)<.001;subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True);media[variant]={'path':row[variant],'width':1080,'height':1920,'fps':30,'frames':150,'duration':5,'codec':'h264','full_decode':'clean','silent':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
old=R.parent/'NOIRFRAME_M03/previews/STAIR_CONTACT_3s_M01_1080.mp4';old=R.parent/'NOIRFRAME_M03/previews/STAIRS_M03_C03_1080.mp4';comp=R/'comparisons/STAIRS_M03_C03_vs_M04_5s.mp4';assert not comp.exists();filt="[0:v]scale=540:960,setsar=1[a];[1:v]scale=540:960,setsar=1[b];[a][b]hstack,pad=1080:1080:0:120:color=0x071521,drawtext=text='M03 C03 - REJECTED             M04 - NEEDS REVIEW':x=20:y=20:fontsize=25:fontcolor=white,drawtext=text='4 risers                              3 risers + landing':x=35:y=58:fontsize=23:fontcolor=white,drawtext=text='Both 1x / no retiming / fixed cameras':x=35:y=92:fontsize=18:fontcolor=white[v]"
subprocess.run(['ffmpeg','-v','error','-n','-i',str(old),'-i',str(R/row['final']),'-filter_complex_threads','1','-filter_complex',filt,'-map','[v]','-an','-t','5','-r','30','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(comp)],check=True);subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(comp),'-f','null','-'],check=True);row['comparison']=str(comp.relative_to(R));row['original_comparison_source']='NOIRFRAME_M03/previews/STAIRS_M03_C03_1080.mp4';row['comparison_note']='Original M03 has four risers; new proof has three plus landing. Both real-time 5s, no cuts/retiming. Not a controlled solver-only ablation.'
# Every diagnostic frame: ordered consecutive pages, no omitted contact phases.
pages=[];decoder=subprocess.Popen(['ffmpeg','-v','error','-i',str(R/row['diagnostic']),'-s','180x320','-pix_fmt','rgb24','-f','rawvideo','-threads','1','pipe:1'],stdout=subprocess.PIPE)
for i in range(150):
 raw=decoder.stdout.read(180*320*3);assert len(raw)==180*320*3
 if i%30==0:sheet=Image.new('RGB',(900,344*6),'#071521')
 x=i%5*180;y=(i%30)//5*344;sheet.paste(Image.frombytes('RGB',(180,320),raw),(x,y));ImageDraw.Draw(sheet).text((x+3,y+322),f'{i:03} / {i/30:.3f}s',fill='white')
 if i%30==29:
  p=R/'reviews'/f'M04_CONTACT_FRAMES_{i//30+1:02}.jpg';sheet.save(p,quality=89);pages.append(str(p.relative_to(R)))
assert decoder.wait()==0
(R/'reports/FRAME_INSPECTION.json').write_text(json.dumps({'frames':150,'fps':30,'pages':pages,'source':row['diagnostic']},indent=2));(R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(media,indent=2));(R/'CURRENT_SHOTS.json').write_text(json.dumps(rows,indent=2));print('MEDIA_AND_COMPARISON_VERIFIED',flush=True)
