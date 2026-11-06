from pathlib import Path
import subprocess,json,hashlib,math,argparse
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'CURRENT_SHOTS.json').read_text());old=R.parent/'NOIRFRAME_MOTION_SYSTEM_CORRECTION';v12=R.parent/'NOIRFRAME_V12_CINEMATIC_REBUILD'
original={'STAIRS':(old/'previews/STAIR_CONTACT_3s_M01_1080.mp4',0,3,'REJECTED M01'),'KEY_DOOR':(old/'previews/KEY_HANDLE_3s_M01_1080.mp4',0,3,'REJECTED M01'),'STEERING':(old/'previews/STEERING_TURN_4s_M01_1080.mp4',0,4,'REJECTED M01'),'CHASE':(v12/'previews/DRIVING_V12_F03_1080.mp4',0,6,'REJECTED V12'),'CURTAIN':(v12/'previews/BEDROOM_V12_F02_1080.mp4',3.4,5,'REJECTED V12')};parser=argparse.ArgumentParser();parser.add_argument('--shots',nargs='*');args=parser.parse_args();media=json.loads((R/'reports/MEDIA_VALIDATION.json').read_text()) if (R/'reports/MEDIA_VALIDATION.json').exists() else {};sheets=json.loads((R/'reports/FRAME_INSPECTION.json').read_text()) if (R/'reports/FRAME_INSPECTION.json').exists() else {}
def run(cmd):subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
for k,row in rows.items():
 if args.shots and k not in args.shots:continue
 tag='C03' if '_C03_' in row['final'] else 'C02'
 for variant in ['final','diagnostic']:
  p=R/row[variant];probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));v=probe['streams'][0];n=round(row['duration']*30)
  assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],int(v['nb_read_frames']))==(1080,1920,'h264','30/1',n);assert abs(float(probe['format']['duration'])-row['duration'])<.002
  run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-']);media[k+'_'+variant]={'path':row[variant],'frames':n,'duration':row['duration'],'width':1080,'height':1920,'fps':30,'codec':'h264','full_decode':'clean','silent':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 before,start,old_d,label=original[k];out=R/'comparisons'/f'{k}_BEFORE_AFTER_M03_{tag}.mp4';duration=row['duration'];extra=max(0,duration-old_d)
 # The rejected original plays at 1x, then a labeled black panel. Never loop or retime it.
 left=f"[0:v]scale=540:960,setsar=1,setpts=PTS-STARTPTS,tpad=stop_mode=add:stop_duration={extra}:color=0x071521,drawtext=text='ORIGINAL ENDED':enable='gte(t,{old_d})':x=50:y=450:fontsize=30:fontcolor=white[a]"
 filt=left+";[1:v]scale=540:960,setsar=1,setpts=PTS-STARTPTS[b];[a][b]hstack,pad=1080:1080:0:120:color=0x071521,drawtext=text='"+label+"                      M03 - UNAPPROVED':x=20:y=25:fontsize=25:fontcolor=white,drawtext=text='Original speed / source ended = black panel':x=20:y=70:fontsize=23:fontcolor=white[v]"
 run(['ffmpeg','-v','error','-n','-ss',str(start),'-t',str(old_d),'-i',str(before),'-i',str(R/row['final']),'-filter_complex_threads','1','-filter_complex',filt,'-map','[v]','-t',str(duration),'-r','30','-an','-c:v','libx264','-crf','20','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]);run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
 row.update(comparison=str(out.relative_to(R)),original={'path':str(before.relative_to(R.parent)),'start':start,'duration':old_d,'speed':1,'after_end':'labeled black panel'})
 # Every diagnostic frame in ordered sheets. One raw stream, no PNG frame cache.
 pages=[];dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(R/row['diagnostic']),'-f','rawvideo','-s','180x320','-pix_fmt','rgb24','-threads','1','pipe:1'],stdout=subprocess.PIPE)
 for f in range(n):
  raw=dec.stdout.read(180*320*3);assert len(raw)==180*320*3;im=Image.frombytes('RGB',(180,320),raw)
  if f%36==0:sheet=Image.new('RGB',(1080,344*6),'#071521')
  x=f%6*180;y=(f%36)//6*344;sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x+3,y+322),f'{f:03} / {f/30:.3f}s',fill='white')
  if f%36==35 or f==n-1:
   dest=R/'reviews'/f'{k}_{tag}_ALL_FRAMES_{f//36+1:02}.jpg';sheet.save(dest,quality=86);pages.append(str(dest.relative_to(R)))
 assert dec.wait()==0;sheets[k]={'frames':n,'fps':30,'pages':pages,'source':row['diagnostic']};print('EXPORT',k,n,flush=True)
(R/'CURRENT_SHOTS.json').write_text(json.dumps(rows,indent=2));(R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(media,indent=2));(R/'reports/FRAME_INSPECTION.json').write_text(json.dumps(sheets,indent=2))
