from pathlib import Path
import json,subprocess,hashlib,math,sys,argparse
from io import BytesIO
from PIL import Image,ImageDraw
from scenes import SCENES,DURATIONS
R=Path(__file__).resolve().parents[1];OLD=R.parent/'NOIRFRAME_V11_ANIMATION_REPAIR';v=json.loads((R/'CURRENT_SHOTS.json').read_text());reports=json.loads((R/'reports/MEDIA_VALIDATION.json').read_text()) if (R/'reports/MEDIA_VALIDATION.json').exists() else {};strips=json.loads((R/'reports/CONTACT_STRIPS.json').read_text()) if (R/'reports/CONTACT_STRIPS.json').exists() else [];parser=argparse.ArgumentParser();parser.add_argument('--shots',nargs='*');args=parser.parse_args()
def run(cmd):subprocess.run(['ffmpeg','-v','error','-n']+cmd,check=True)
def frame(path,t):
 q=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1'],capture_output=True,check=True);return Image.open(BytesIO(q.stdout)).convert('RGB')
for k,row in v.items():
 if args.shots and k not in args.shots:continue
 strips=[q for q in strips if q['shot']!=k]
 p=R/row['final'];dur=DURATIONS[k];q=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=width,height,r_frame_rate,nb_read_frames,codec_name','-show_entries','format=duration','-of','json',str(p)],capture_output=True,check=True);meta=json.loads(q.stdout);st=meta['streams'][0];assert st['width']==1080 and st['height']==1920 and st['r_frame_rate']=='30/1' and int(st['nb_read_frames'])==round(dur*30);subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True);reports[k]={'path':str(p.relative_to(R)),'full_decode':'clean','metadata':meta,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 if k=='DRIVING':before=R.parent/'NOIRFRAME_FULL_FILM_V1/renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4';ss=0;bdur=6;label='PREVIOUS MASTER 0-6s'
 else:
  old={'HOUSE':'HOUSE_V11_R08_1080.mp4','STAIRS':'STAIRS_V11_R07_1080.mp4','BEDROOM':'WINDOW_V11_R07_1080.mp4'}[k];before=OLD/'previews'/old;ss=0;bdur={'HOUSE':11,'STAIRS':8.5,'BEDROOM':7.5}[k];label='REJECTED V11'
 length=max(bdur,dur);suffix='_F03' if 'F03' in p.name else '_F02' if 'F02' in p.name else '';comp=R/'reviews'/f'{k}{suffix}_V11_V12_BEFORE_AFTER.mp4';fc=f"[0:v]scale=540:960,setsar=1,tpad=stop_mode=clone:stop_duration={length-bdur},trim=duration={length},pad=540:1080:0:120:color=0x091b2a,drawtext=text='{label}':x=20:y=18:fontsize=24:fontcolor=white,drawtext=text='End hold if source finishes':x=15:y=66:fontsize=17:fontcolor=white[a];[1:v]scale=540:960,setsar=1,tpad=stop_mode=clone:stop_duration={length-dur},trim=duration={length},pad=540:1080:0:120:color=0x091b2a,drawtext=text='V12 — REVIEW ONLY':x=20:y=18:fontsize=24:fontcolor=white,drawtext=text='Normal speed / no time stretching':x=15:y=66:fontsize=17:fontcolor=white[b];[a][b]hstack=inputs=2[out]"
 run(['-ss',str(ss),'-t',str(bdur),'-i',str(before),'-i',str(p),'-filter_complex',fc,'-map','[out]','-an','-r','30','-c:v','libx264','-threads','2','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(comp)]);row['comparison']=str(comp.relative_to(R));print('COMPARED',k,flush=True)
 spans={'HOUSE':[('HANDLE',3.55,4.15),('KEY',5.70,6.80),('DOOR_ENTRY',9.85,10.55),('BOLT',11.65,12.10)],'STAIRS':[('TREAD_CONTACT',.80,1.60),('UPPER_LANDING',7.65,8.35)],'BEDROOM':[('PINCH_PULL',2.25,3.25),('REACTION',5.50,6.5)],'DRIVING':[('WHEEL_HANDS',1.80,2.60),('PEDAL_PRESS',7.65,8.65),('PURSUIT',5.6,6.4)]}[k]
 for name,lo,hi in spans:
  times=[round(lo+j*.1,5) for j in range(round((hi-lo)*10)+1)];tiles=[]
  for t in times:
   im=frame(p,t);_,d,w=SCENES[k](t)
   if k=='DRIVING':box=(0,0,1080,1920)
   elif name=='KEY':
    x,y=w.cam(d['keybow']);box=(x-200,y-250,x+200,y+250)
   elif name=='BOLT':
    x,y=w.cam(d['pose']['arms'][0]['wrist']);box=(x-220,y-250,x+220,y+250)
   elif k=='STAIRS':
    ps=[w.cam(q['sole']) for q in d['pose']['legs']];x=sum(q[0] for q in ps)/2;y=sum(q[1] for q in ps)/2;box=(x-230,y-340,x+230,y+120)
   elif name=='PINCH_PULL':
    x,y=w.cam(d['grip']);box=(x-220,y-250,x+220,y+250)
   else:box=(0,0,1080,1920)
   im=im.crop(tuple(round(x) for x in box));im.thumbnail((240,320));tile=Image.new('RGB',(240,345),'#0b1e2c');tile.paste(im,((240-im.width)//2,0));ImageDraw.Draw(tile).text((7,324),f'{t:.2f}s — decoded MP4',fill='white');tiles.append(tile)
  sheet=Image.new('RGB',(1200,345*math.ceil(len(tiles)/5)),'#0b1e2c')
  for j,im in enumerate(tiles):sheet.paste(im,(j%5*240,j//5*345))
  out=R/'reviews'/f'{k}_{name}{suffix}_CONTACT_STRIP.jpg';sheet.save(out,quality=94);strips.append({'shot':k,'action':name,'path':str(out.relative_to(R)),'times':times,'spacing_seconds':.1,'source':'actual decoded final MP4'})
 (R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(reports,indent=2));(R/'reports/CONTACT_STRIPS.json').write_text(json.dumps(strips,indent=2));(R/'CURRENT_SHOTS.json').write_text(json.dumps(v,indent=2))
