"""Decode final exports, create synchronized M04 comparison and inspect every diagnostic frame."""
from pathlib import Path
import subprocess,json,hashlib,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];shots=json.loads((R/'CURRENT_SHOTS.json').read_text());shot=shots['STAIRS'];media={}
def verify(path):
 p=R/path;probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));v=probe['streams'][0];assert v['codec_name']=='h264' and v['r_frame_rate']=='30/1' and int(v['nb_read_frames'])==150;assert abs(float(probe['format']['duration'])-5)<.001;subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True);return {'path':path,'width':v['width'],'height':v['height'],'fps':30,'frames':150,'duration':5,'codec':'h264','full_decode':'clean','silent':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for k in ['final','diagnostic']:
 media[k]=verify(shot[k]);assert (media[k]['width'],media[k]['height'])==(1080,1920)
old=R.parent/'NOIRFRAME_M04/previews/STAIRS_M04_PROOF_5s_R06_1080.mp4';out=R/shot['comparison'];assert not out.exists();filt="[0:v]scale=540:960,setsar=1[a];[1:v]scale=540:960,setsar=1[b];[a][b]hstack,pad=1080:1080:0:120:color=0x071521,drawtext=text='M04 - NOT APPROVED        M05 - NEEDS REVIEW':x=22:y=18:fontsize=25:fontcolor=white,drawtext=text='Same rig and foot-contact schedule / both 1x':x=30:y=57:fontsize=22:fontcolor=white,drawtext=text='M04 fixed camera / M05 gentle follow - not a camera-matched ablation':x=30:y=92:fontsize=16:fontcolor=white[v]"
subprocess.run(['ffmpeg','-v','error','-n','-i',str(old),'-i',str(R/shot['final']),'-filter_complex_threads','1','-filter_complex',filt,'-map','[v]','-an','-t','5','-r','30','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True);media['comparison']=verify(shot['comparison'])
# Every encoded diagnostic frame appears once on these consecutively ordered pages.
decoder=subprocess.Popen(['ffmpeg','-v','error','-i',str(R/shot['diagnostic']),'-s','180x320','-pix_fmt','rgb24','-f','rawvideo','-threads','1','pipe:1'],stdout=subprocess.PIPE);pages=[]
for i in range(150):
 raw=decoder.stdout.read(180*320*3);assert len(raw)==180*320*3
 if i%30==0:sheet=Image.new('RGB',(900,344*6),'#071521')
 x=i%5*180;y=(i%30)//5*344;sheet.paste(Image.frombytes('RGB',(180,320),raw),(x,y));ImageDraw.Draw(sheet).text((x+3,y+322),f'{i:03} / {i/30:.3f}s',fill='white')
 if i%30==29:
  p=R/'reviews'/f'M05_CONTACT_FRAMES_{i//30+1:02}.jpg';sheet.save(p,quality=91);pages.append(str(p.relative_to(R)))
assert decoder.wait()==0
(R/'reports/FRAME_INSPECTION.json').write_text(json.dumps({'encoded_frames':150,'fps':30,'pages':pages,'source':shot['diagnostic']},indent=2));(R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(media,indent=2));print('FINAL_MEDIA_AND_COMPARISON_VERIFIED')
