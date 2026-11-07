"""Native Blender-evaluated geometry, cel world raster, persistent/resumable lossless frame batches.
Each completed 60-frame batch is committed remotely and SHA256-verified before continuing.
"""
from pathlib import Path
import argparse,json,gzip,hashlib,subprocess,time,math,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from bootstrap import ROOT as R
import actions,sets,vehicle_system as VS
from contact_rig import V,RY,RZ,RX
from world import World,Camera
from cameras import camera
from spatial_world import house
from fast_depth import FastDepth
from render_clips import body,restore_state
from production_guard import ensure
NATIVE=set(actions.DURATIONS)-{'CAR_CHASE','ROAD_BUILDINGS','ARRIVAL','FINAL_POLL'}

def external_into_cabin(w,d):
 o=d['position'];M=RY(d['yaw']);pivot=V(0,.55,0);RR=M@RZ(d['roll'])@RX(d['pitch']);WC=lambda q:o+M@pivot+RR@(q-pivot);ext=World(Camera(WC(w.cam.eye),WC(w.cam.target),w.cam.focal,up=RR@w.cam.up),w.t);ext.render_frustum=True;sets.city(ext)
 for op in ext.ops:
  if op[0] in ['face','line','glyph']:w.ops.append((op[0],[pivot+RR.T@(p-o-M@pivot) for p in op[1]],*op[2:]))

def make_world(shot,t,d,f=None,data=None,diagnostic=False):
 cam=camera(shot,t,d,diagnostic);w=World(cam,t);w.render_frustum=True;w.light_sources=[]
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:
  external_into_cabin(w,d);sets.cockpit(w,d);w.light_sources=[((-.38,.95,.75),.7,.55)]
 elif shot=='CAR_EXIT_RUNNING':
  v=VS.PARK;M=RY(v['yaw']);ext=World(Camera(v['position']+M@cam.eye,v['position']+M@cam.target,cam.focal),t);ext.render_frustum=True;sets.city(ext)
  for op in ext.ops:
   if op[0] in ['face','line','glyph']:w.ops.append((op[0],[M.T@(p-v['position']) for p in op[1]],*op[2:]))
  sets.exit_car(w,d)
 elif shot in ['KEY_LOCK','DOOR_ENTRY']:
  sets.house_exterior(w);sets.door_live(w,d);w.light_sources=[((-.67,2.02,-.53),1.5,1.),((-.55,1.85,2.),1.3,.8)]
 elif shot=='STAIRS':
  if diagnostic:
   tmp=World(cam,t);house(tmp)
   for g in tmp.geometry:
    if 'stair' in g['name']:w.face(g['vertices'],g['color'],name=g['name'])
  else:house(w)
  w.light_sources=[((-2.23,1.95,z),2.8,1.) for z in [1.,3.5,5.3]]
 elif shot in ['WINDOW_CURTAIN','PHONE_CALL','UNKNOWN_CALLER']:
  sets.bedroom(w,d);w.light_sources=[((.72,1.55,-3.9),3.,1.)]
 else:sets.city(w);sets.pair(w,d)
 if data is not None:
  body(w,data,f,d)
  if shot=='STAIRS':
   for leg in d['pose']['legs']:
    if leg['planted']:
     c=leg['sole'];w.face([c+V(.07*math.cos(a),.001,.10*math.sin(a)) for a in np.linspace(0,math.tau,16)],'#14262e',stroke='none',name='actual tread contact shadow')
 return w

def poll(t,width):
 h=round(width*16/9);im=Image.new('RGB',(width,h),'#061722');dr=ImageDraw.Draw(im);s=width/1080
 def text(x,y,v,size,col='white'):
  f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',round(size*s));dr.text((x*s,y*s),v,font=f,fill=col,anchor='mm')
 for k in range(100):
  x=(k*71)%1080;y=(k*113+t*440)%1920;dr.line([(x*s,y*s),((x-8)*s,(y+43)*s)],fill='#264555',width=max(1,round(s)))
 text(540,470,'WHAT WOULD',76);text(540,570,'YOU DO?',100,'#ed453c')
 for j,(col,title,sub) in enumerate([('#49dd8d','A · TAKE','$1,000,000'),('#ef5d53','B · CALL','THE POLICE')]):
  y=790+j*280
  if actions.Q(t,.4+j*.35,.9+j*.35)<=0:continue
  dr.rounded_rectangle((100*s,y*s,980*s,(y+220)*s),radius=25*s,fill='#123b36' if j==0 else '#3e1b27',outline=col,width=max(2,round(5*s)));text(540,y+66,title,55,col);text(540,y+147,sub,62)
 text(540,1470,'COMMENT A OR B',54);text(540,1540,'FOR PART 2',42,'#b6c6c8');return im

def backup_batch(directory,paths,start,end,fingerprint):
 from checkpoint_store import pack
 label=f'{directory.name}-{start:05d}-{end:05d}';report=R/'reports'/(label+'_BACKUP.json')
 if report.exists():
  old=json.loads(report.read_text());assert old['fingerprint']==fingerprint and old['verified'];return
 manifest=directory/f'BATCH_{start:05d}_{end:05d}.json';manifest.write_text(json.dumps({'fingerprint':fingerprint,'start':start,'end':end,'files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]},indent=2));archive,_=pack([directory/'PRODUCER.json',manifest,*paths],label)
 subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'asset','--path',str(archive.relative_to(R)),'--label',label],check=True)
 report.write_text(json.dumps({'label':label,'fingerprint':fingerprint,'verified':True,'archive':str(archive.relative_to(R)),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))

def main():
 p=argparse.ArgumentParser();p.add_argument('--shot',required=True);p.add_argument('--tag',default='M11R01');p.add_argument('--width',type=int,default=360);p.add_argument('--diagnostic',action='store_true');p.add_argument('--stills',action='store_true');p.add_argument('--final',action='store_true');a=p.parse_args();ensure('source checkpoint before '+a.shot+' render');shot=a.shot;width=1080 if a.final else a.width;dur=actions.DURATIONS[shot];n=round(dur*30);data=chase=None
 if shot in NATIVE:
  data=json.load(gzip.open(R/'scenes'/f'{shot}_{a.tag}.json.gz','rt'));assert hashlib.sha256((R/'blender'/f'{shot}_{a.tag}.blend').read_bytes()).hexdigest()==data['blend_sha256']
 if shot=='CAR_CHASE':chase=json.load(gzip.open(R/'scenes'/f'DRIVER_CHASE_{a.tag}.json.gz','rt'))
 stage='FINAL' if a.final else 'DIAGNOSTIC' if a.diagnostic else f'PREVIEW_{width}';stem=f'M11_{shot}_{a.tag}_{stage}';raster=FastDepth(round(width*1.5) if a.final else width)
 def frame(i):
  t=i/30
  from overlays_m11 import apply
  if shot=='FINAL_POLL':return apply(poll(t,width),shot,t),None
  dd=data;ss=shot
  if shot=='CAR_CHASE' and 1.6<=t<3.6:dd=chase;ss='DRIVER_CHASE'
  d=restore_state(dd['state'][i]) if dd else actions.state(shot,t);f=dd['frames'][i] if dd else None;w=make_world(ss,t,d,f,dd,a.diagnostic);im=raster.render(w)
  if a.final:im=im.resize((1080,1920),Image.Resampling.LANCZOS)
  im=apply(im,shot,t)
  if a.diagnostic and f is not None:
   dr=ImageDraw.Draw(im);scale=width/1080
   for side,j in [('L',1),('R',0)]:
    leg=d['pose']['legs'][j];x,y=w.cam(leg['sole']);col='#69eea1' if leg['planted'] else '#edb960';dr.ellipse(((x-14)*scale,(y-14)*scale,(x+14)*scale,(y+14)*scale),outline=col,width=2)
   dr.rectangle((0,0,width,70),fill='#071923');dr.text((10,10),f'M11 {shot} / {t:.3f}s',fill='white');dr.text((10,30),'GREEN: STANCE / AMBER: SWING',fill='white');dr.text((10,50),'Diagnostic walls omitted only here',fill='white')
  return im,w
 if a.stills:
  for i in [0,n//4,n//2,3*n//4,n-1]:frame(i)[0].save(R/'contact_sheets'/f'{stem}_{i:04d}.png')
  return
 out=R/'renders'/(stem+'.mp4');report=R/'reports'/(stem+'_RENDER.json')
 if report.exists():print('COMPLETED_PRESERVED',stem);return
 if out.exists():out.rename(R/'scratch'/f'{stem}_INTERRUPTED_{time.time_ns()}.mp4')
 from production_guard import sources
 all_sources=sources();deps={k:v for k,v in all_sources.items() if k.startswith('source/legacy/') or k.split('/')[-1] in ['render_m11.py','render_clips.py','actions.py','sets.py','sets_m10.py','cameras.py','cameras_m10.py','cameras_base_R07.py','vehicle_system.py','spatial_world.py','mirror_feed.py','native_style.py','stair_style.py','world.py','fast_depth.py','depth_render.py','fast_raster.so','approved_head.py','approved_head_view.py','view_head.py','svg.py','overlays_m11.py','dialogue_m11.py']};fp=hashlib.sha256(json.dumps({'sources':deps,'width':width,'shot':shot,'native_blend':data.get('blend_sha256') if data else None,'driver_blend':chase.get('blend_sha256') if chase else None,'duration':dur},sort_keys=True).encode()).hexdigest();directory=R/'frames'/stem;directory.mkdir(exist_ok=True);stamp=directory/'PRODUCER.json'
 if stamp.exists():assert json.loads(stamp.read_text())['fingerprint']==fp,'Source changed. Use a NEW revision tag; preserve these completed frames.'
 else:stamp.write_text(json.dumps({'fingerprint':fp,'width':width,'height':round(width*16/9),'fps':30,'dependency_sha256':deps,'native_blend_sha256':data.get('blend_sha256') if data else None,'batch_frames':60,'persistence':'/workspace plus SHA256-verified committed remote chunks'},indent=2))
 wav=R/'sound'/f'M11_{shot}_{a.tag}_MASTER.wav'
 if not wav.exists():
  from sound_m11 import make
  make(shot,a.tag)
 cmd=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{round(width*16/9)}','-r','30','-i','pipe:0','-i',str(wav),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-t',str(dur),'-movflags','+faststart',str(out)];proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);hashes=[];checks=[];samples=[];start=time.monotonic();last=None;batch=[]
 for i in range(n):
  path=directory/f'{i:05d}.png'
  if a.final and path.exists():im=Image.open(path).convert('RGB')
  else:
   im,w=frame(i)
   if a.final:im.save(path)
  arr=np.asarray(im);hashes.append(hashlib.sha256(arr.tobytes()).hexdigest());diff=float(np.abs(arr.astype(np.int16)-last).mean()) if last is not None else None;checks.append({'frame':i,'mean_luminance':float(arr.mean()),'mean_frame_difference':diff,'black_fraction':float(np.mean(arr.max(axis=2)<3))});last=arr.astype(np.int16)
  if i%30==0:print(stem,i,n,round(time.monotonic()-start,1),flush=True);samples.append((i,im.resize((180,320))))
  proc.stdin.write(im.tobytes())
  if a.final:
   batch.append(path)
   if (i+1)%60==0 or i==n-1:
    backup_batch(directory,batch,i-len(batch)+1,i,fp);batch=[]
 proc.stdin.close();assert proc.wait()==0
 sheet=Image.new('RGB',(900,344*math.ceil(len(samples)/5)),'#071521');dr=ImageDraw.Draw(sheet)
 for k,(i,im) in enumerate(samples):x=k%5*180;y=k//5*344;sheet.paste(im,(x,y));dr.text((x+4,y+322),f'{i/30:.2f}s',fill='white')
 sheet.save(R/'contact_sheets'/f'{stem}.jpg',quality=92);rp={'shot':shot,'native_tag':a.tag,'duration':dur,'fps':30,'width':width,'height':round(width*16/9),'frames':n,'native_blend_sha256':data.get('blend_sha256') if data else None,'source_sha256':all_sources,'source_frame_sha256':hashes,'pixel_checks':checks,'spatial_samples':1.5 if a.final else 1.,'file':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'render_command':cmd,'master_frames_persistent':a.final,'remote_frame_batch_verification_required':a.final};report.write_text(json.dumps(rp,indent=2))
 subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'asset','--path',str(out.relative_to(R)),'--label',stem],check=True);print('DONE_BACKED_UP',stem,flush=True)
if __name__=='__main__':main()
