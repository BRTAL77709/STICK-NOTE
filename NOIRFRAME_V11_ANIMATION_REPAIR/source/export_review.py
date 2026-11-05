"""Decoded-media comparisons and dense contact strips; never substitute stills for playback."""
from pathlib import Path
import json,subprocess,io,math,hashlib
from PIL import Image,ImageDraw
from actions import *
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'CURRENT_SHOTS.json').read_text());old=R.parent/'NOIRFRAME_FULL_FILM_V1/renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4';before={'HOUSE':(49.2,12.2),'STAIRS':(61.4,4.),'WINDOW':(65.4,4.)};font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';metadata={}
for k,row in rows.items():
 movie=R/row['final'];q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]));v=next(x for x in q['streams'] if x['codec_type']=='video');assert v['width']==1080 and v['height']==1920 and v['avg_frame_rate']=='30/1' and int(v['nb_read_frames'])==row['frames'] and v['codec_name']=='h264';assert abs(float(q['format']['duration'])-row['duration'])<.002
 z=subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],capture_output=True);assert z.returncode==0 and not z.stderr
 start,bd=before[k];after=row['duration'];duration=max(bd,after);comp=R/'reviews'/f'{k}_R07_BEFORE_AFTER.mp4';assert not comp.exists()
 def filt(src,dur,label,extra):
  s=f'[{src}:v]scale=540:960,pad=540:1000:0:40:color=0x071521,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={duration-dur},drawtext=fontfile={font}:text={label}:fontsize=25:fontcolor=white:x=12:y=7'
  if duration>dur:s+=f",drawtext=fontfile={font}:text=END FRAME HELD:fontsize=20:fontcolor=0xefb569:x=15:y=958:enable='gte(t,{dur})'"
  return s+extra
 fc=filt(0,bd,'BEFORE - original','[b];')+filt(1,after,'V11 - user review','[a];')+'[b][a]hstack=inputs=2[v]'
 subprocess.run(['ffmpeg','-v','error','-n','-ss',str(start),'-t',str(bd),'-i',str(old),'-i',str(movie),'-filter_complex_threads','1','-filter_complex',fc,'-map','[v]','-an','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(comp)],check=True)
 metadata[k]={'file':row['final'],'width':1080,'height':1920,'fps':30,'frames':row['frames'],'duration_s':after,'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'full_decode':'clean','comparison':str(comp.relative_to(R)),'before_interval_s':[start,start+bd],'comparison_duration_s':duration,'source_clips_not_speed_changed':True,'comparison_end_hold_explicitly_labeled':True}
 for label,idx in [('FIRST',0),('MID',row['frames']//2),('LAST',row['frames']-1)]:
  data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(idx/30),'-i',str(movie),'-frames:v','1','-vf','scale=540:960','-f','image2pipe','-vcodec','png','-threads','1','pipe:1']);Image.open(io.BytesIO(data)).save(R/'reviews'/f'{k}_R07_{label}.png')
 print(k,'MEDIA_AND_COMPARISON_COMPLETE',flush=True)
(R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(metadata,indent=2))
strips=[('HOUSE','KEY',3.65,4.90,2),('HOUSE','BOLT',9.45,10.23,2),('HOUSE','HANDOFF',7.20,8.30,3),('STAIRS','FIRST_LANDING',.40,1.12,2),('STAIRS','UPPER_LANDING',7.18,7.58,2),('WINDOW','PINCH',2.25,2.78,2),('WINDOW','PULL',2.65,4.45,3),('WINDOW','REACTION',4.7,6.3,3)];stripdata=[]
for k,name,a,b,step in strips:
 frames=list(range(round(a*30),round(b*30)+1,step));flt='select='+ '+'.join(f'eq(n\\,{f})' for f in frames);cmd=['ffmpeg','-v','error','-i',str(R/rows[k]['final']),'-vf',flt,'-fps_mode','passthrough','-an','-pix_fmt','rgb24','-f','rawvideo','pipe:1'];p=subprocess.Popen(cmd,stdout=subprocess.PIPE);tiles=[]
 for frame in frames:
  data=p.stdout.read(1080*1920*3);assert len(data)==1080*1920*3;im=Image.frombytes('RGB',(1080,1920),data);t=frame/30
  if k=='HOUSE' and name=='HANDOFF':
   from scenes import house_camera
   d=house(t);P,S,v=house_camera(t);x,y=P(d['pose']['arms'][0]['wrist']);left=max(0,min(480,x-300));top=max(0,min(1320,y-300));box=(left,top,left+600,top+600)
  elif k=='HOUSE':box=(180,600,1020,1250) if name=='KEY' else (120,580,1020,1190)
  elif k=='STAIRS':
   d=stairs(t);root=d['pose']['root'];cx=.65*(root[0]+.58);cy=.8*max(0,root[1]-.65);pos=[(320+390*(x['sole'][0]+.58-cx)+390*.25*(x['sole'][2]-1.4),1490-390*(x['sole'][1]-cy)+390*.09*(x['sole'][2]-1.4)) for x in d['pose']['legs']];x=sum(q[0] for q in pos)/2;y=max(q[1] for q in pos);left=max(0,min(480,x-300));top=max(0,min(1500,y-340));box=(left,top,left+600,top+420)
  elif name in ['PINCH','PULL']:
   g=cloth(t);x=70+(g[0]-2.35)*460+g[2]*50;left=max(0,min(480,x-300));box=(left,650,left+600,1250)
  else:box=(120,550,900,1400)
  crop=im.crop(tuple(round(x) for x in box));crop.thumbnail((300,300));tile=Image.new('RGB',(300,324),'#071521');tile.paste(crop,((300-crop.width)//2,(300-crop.height)//2));ImageDraw.Draw(tile).text((7,304),f'{frame/30:.3f}s / frame{frame}',fill='white');tiles.append(tile)
 assert p.wait()==0;sheet=Image.new('RGB',(1800,324*math.ceil(len(tiles)/6)),'#071521')
 for j,tile in enumerate(tiles):sheet.paste(tile,(j%6*300,j//6*324))
 path=R/'reviews'/f'{k}_{name}_R07_CONTACT_STRIP.jpg';sheet.save(path,quality=95);stripdata.append({'shot':k,'action':name,'file':str(path.relative_to(R)),'frames':frames,'spacing_seconds':step/30,'source':'actual decoded1080 MP4','camera_follow_crop':k!='HOUSE'});print('STRIP',k,name,flush=True)
(R/'reports/CONTACT_STRIPS.json').write_text(json.dumps(stripdata,indent=2))
