"""Fresh 30fps frames from native evaluated characters and shared world/vehicle state."""
from pathlib import Path
import argparse,json,gzip,subprocess,hashlib,math,time,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from bootstrap import ROOT as R
import actions,sets,vehicle_system as VS
from cameras import camera
from world import World,Camera
from contact_rig import V,RY
from fast_depth import FastDepth
import native_style,stair_style
from approved_head import head
native_style.P=lambda q:np.array([q[1],q[2],q[0]],float)
def Q(q):return np.array([q[1],q[2],q[0]],float)
def body(w,data,f,d):
 hand_pov=d.get('_pov_hand_only',False)
 for name,m in data['topology'].items():
  if name=='APPROVED_HEAD_CARD':continue
  if hand_pov and name not in ['SLEEVE_LOWER_L','MITTEN_L'] and not (name.startswith('M07_digit') and name.endswith('.L')):continue
  native_style.submit_mesh(w,f['meshes'][name],m['faces'],m['color'],name)
 if hand_pov:return
 card=np.array([Q(q) for q in f['meshes']['APPROVED_HEAD_CARD']]);screen=np.array([w.cam(q) for q in card]);center=screen.mean(axis=0);vx=((screen[1]+screen[2])-(screen[0]+screen[3]))/1200;vy=((screen[0]+screen[1])-(screen[2]+screen[3]))/1200
 def draw(a):
  a.add(f'<g transform="matrix({vx[0]} {vx[1]} {vy[0]} {vy[1]} {center[0]} {center[1]})">');head(a,0,0,d['time'],d['pose'].get('yaw',.8),.7,d['pose'].get('fear',.6),0,blink_override=max(0,1-abs(d['time']-1.45)/.065));a.add('</g>')
 w.submit(list(card),draw,-.015)
 # Contact shadows under evaluated soles, not offsets attached to the screen.
 if d['time']>0:
  for s in ['L','R']:
   vv=np.array([Q(q) for q in f['meshes']['SHOE_'+s]]);c=vv.mean(axis=0);z=0.13 if d.get('vehicle_stationary') and c[0]<-4.6 else 0.;height=vv[:,1].min()-z
   if -.002<=height<.24:
    pts=[V(c[0]+.08*math.cos(t),z+.002,c[2]+.10*math.sin(t)) for t in np.linspace(0,math.tau,18,endpoint=False)];w.face(pts,'#102630',stroke='none',name='evaluated shoe shadow')

def scene(shot,t,d,f=None,data=None,debug=False):
 cam=camera(shot,t,d,debug);w=World(cam,t)
 if shot in ['KEY_LOCK','DOOR_ENTRY']:
  sets.house_exterior(w);sets.door_live(w,d)
 elif shot=='WINDOW_CURTAIN':sets.bedroom(w,d)
 elif shot=='DRIVING_COCKPIT':
  ext=World(Camera((1,1,-2),(0,1,0)),t);sets.city(ext);o=d['position'];M=RY(d['yaw']);pivot=V(0,.55,0);RR=M@actions.RZ(d['roll'])@actions.RX(d['pitch'])
  for op in ext.ops:
   if op[0] in ['face','line']:w.ops.append((op[0],[pivot+RR.T@(p-o-M@pivot) for p in op[1]],*op[2:]))
  sets.cockpit(w,d)
 elif shot=='CAR_EXIT_RUNNING':
  vs=VS.state(min(11,9+t));ext=World(Camera((1,1,-2),(0,1,0)),t);sets.city(ext)
  for op in ext.ops:
   if op[0] in ['face','line']:w.ops.append((op[0],[RY(-vs['yaw'])@(p-vs['position']) for p in op[1]],*op[2:]))
  sets.exit_car(w,d)
 else:sets.city(w);sets.pair(w,d)
 if shot=='DOOR_ENTRY' and t>=10.8 and not debug:d={**d,'_pov_hand_only':True}
 if f is not None and not debug and not d.get('hide_actor',False):body(w,data,f,d)
 return w

def debug_image(shot,t,d,f,width):
 im=Image.new('RGB',(width,round(width*16/9)),'#0c2230');dr=ImageDraw.Draw(im);s=width/1080;cam=camera(shot,t,d,True)
 def xy(p):return tuple(np.array(cam(p))*s)
 def native(p):return xy(Q(p))
 if f:
  for side,col in [('L','#ffe077'),('R','#72dfff')]:
   for pref in ['thigh.','shin.','upper_arm.','forearm.','hand.','digit0a.','digit0b.','digit1a.','digit1b.']:
    name=pref+side;b=f['bones'][name];dr.line([native(b['head']),native(b['tail'])],fill=col,width=max(1,round(4*s)))
   vv=f['meshes']['SHOE_'+side];dr.polygon([native(vv[k]) for k in [0,1,2,3,4]],outline='#9dffb0',width=max(1,round(2*s)));x,y=native(f['targets'][side]);dr.line([(x-8*s,y),(x+8*s,y)],fill='#fa85dd',width=2);dr.line([(x,y-8*s),(x,y+8*s)],fill='#fa85dd',width=2)
  dr.polygon([native(q) for q in f['meshes']['APPROVED_HEAD_CARD']],outline='#c4d5d6',width=1)
 for name in ['keytip','keyhole','grip','handle_end','wheel_center','car_handle']:
  if name in d:
   x,y=xy(d[name]);dr.ellipse((x-5*s,y-5*s,x+5*s,y+5*s),fill='#6affb1')
 if 'fabric' in d:
  mesh=np.array(d['fabric'])
  for col in range(0,len(mesh[0]),6):dr.line([xy(q) for q in mesh[:,col]],fill='#bbcad0',width=1)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',max(10,round(21*s)));dr.rectangle((0,0,width,round(125*s)),fill='#061622');dr.text((10*s,10*s),f'M07 {shot} / {t:.3f}s / native evaluated joints',font=font,fill='white');dr.text((10*s,46*s),d.get('phase','')[:90],font=font,fill='#b6d3dd');dr.text((10*s,82*s),'Fixed camera / targets pink / actual bone chains yellow-blue',font=font,fill='white');return im

def main():
 global actions
 p=argparse.ArgumentParser();p.add_argument('--shot',required=True,choices=actions.DURATIONS);p.add_argument('--tag',default='R01');p.add_argument('--width',type=int,default=360);p.add_argument('--stills',action='store_true');p.add_argument('--final',action='store_true');a=p.parse_args();shot=a.shot
 revisions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text()) if (R/'reports/SHOT_REVISIONS.json').exists() else {}
 if a.final and shot!='STAIRS':a.tag=revisions.get(shot,a.tag)
 import importlib.util
 controller=R/'source'/f'actions_{a.tag}.py'
 if controller.exists():
  spec=importlib.util.spec_from_file_location('m07_locked_actions_'+a.tag,controller);actions=importlib.util.module_from_spec(spec);spec.loader.exec_module(actions)
 else:controller=R/'source/actions.py'
 width=a.width;dur=actions.DURATIONS[shot];n=round(dur*30);raster=FastDepth(width);data=None
 if shot=='STAIRS':data=json.load(gzip.open(R/'scenes/STAIRS_INHERITED.json.gz','rt'))
 elif shot not in ['ROAD_BUILDINGS','CAR_CHASE']:
  data=json.load(gzip.open(R/'scenes'/f'{shot}_{a.tag}.json.gz','rt'));assert hashlib.sha256((R/'blender'/f'{shot}_{a.tag}.blend').read_bytes()).hexdigest()==data['blend_sha256'];assert all(hashlib.sha256((controller if q=='source/actions.py' else (R/'source/bake_native_R07.py' if q=='source/bake_native.py' and hashlib.sha256((R/q).read_bytes()).hexdigest()!=data['source_sha256'][q] else (R/'source/cameras_base_R07.py' if q=='source/cameras.py' and hashlib.sha256((R/q).read_bytes()).hexdigest()!=data['source_sha256'][q] else R/q))).read_bytes()).hexdigest()==data['source_sha256'][q] for q in ['source/actions.py','source/cameras.py','source/vehicle_system.py','source/bake_native.py','source/embed_assets.py'])
 chase_driver=json.load(gzip.open(R/'scenes'/f'DRIVER_CHASE_{a.tag}.json.gz','rt')) if shot=='CAR_CHASE' else None
 def frame(i):
  t=i/30
  if shot=='CAR_CHASE' and 4.4<=t<6.3:
   dd=actions.driving(t);ff=chase_driver['frames'][i];w=scene('DRIVING_COCKPIT',t,dd,ff,chase_driver);w.cam=camera('DRIVER_CHASE',t,dd);w=World(w.cam,t)
   # Compose with the same registered city and cabin in driver-local coordinates.
   ext=World(Camera((1,1,-2),(0,1,0)),t);sets.city(ext);o=dd['position'];M=RY(dd['yaw']);pivot=V(0,.55,0);RR=M@actions.RZ(dd['roll'])@actions.RX(dd['pitch'])
   for op in ext.ops:
    if op[0] in ['face','line']:w.ops.append((op[0],[pivot+RR.T@(p-o-M@pivot) for p in op[1]],*op[2:]))
   sets.cockpit(w,dd);body(w,chase_driver,ff,dd);im=raster.render(w);debug=raster.render(scene('CAR_CHASE',t,actions.state('CAR_CHASE',t),None,None,True));return im,debug,dd
  if shot=='STAIRS':
   f=data['frames'][i];im=raster.render(stair_style.scene(data,f));debug=stair_style.diagnostic(raster.render(stair_style.scene(data,f,True)),data,f);return im,debug,{}
  d=actions.state(shot,t);f=data['frames'][i] if data else None;im=raster.render(scene(shot,t,d,f,data));debug=debug_image(shot,t,d,f,width) if data else raster.render(scene(shot,t,d,None,None,True));return im,debug,d
 stem=f'M07_{shot}_1080' if a.final else f'M07_{shot}_{a.tag}_{width}'
 if a.stills:
  for i in sorted(set([0,n//5,n//2,n*3//4,n-1])):
   im,debug,d=frame(i);im.save(R/'contact_sheets'/f'{stem}_{i:03}.png');debug.save(R/'contact_sheets'/f'{stem}_{i:03}_DEBUG.png')
  return
 paths=[R/'renders'/(stem+'.mp4'),R/'debug'/(stem+'_DEBUG.mp4')];assert not any(q.exists() for q in paths);enc=[]
 for path in paths:enc.append(subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{round(width*16/9)}','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE))
 producer_sources={str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (R/'source').rglob('*') if q.is_file() and q.suffix in ['.py','.cpp','.so']};samples=[];hashes=[];start=time.monotonic()
 for i in range(n):
  im,debug,d=frame(i)
  for proc,img in zip(enc,[im,debug]):proc.stdin.write(img.tobytes())
  hashes.append(hashlib.sha256(im.tobytes()).hexdigest())
  if i%12==0:samples.append((i,im.resize((180,320)),debug.resize((180,320))))
  if i%30==0:print(stem,i,'/',n,'elapsed',round(time.monotonic()-start,1),flush=True)
 for proc in enc:proc.stdin.close();assert proc.wait()==0
 for idx,label in [(1,'CLEAN'),(2,'DEBUG')]:
  sheet=Image.new('RGB',(900,344*math.ceil(len(samples)/5)),'#071521');dr=ImageDraw.Draw(sheet)
  for k,row in enumerate(samples):x=k%5*180;y=k//5*344;sheet.paste(row[idx],(x,y));dr.text((x+3,y+322),f'{row[0]/30:.2f}s',fill='white')
  sheet.save(R/'contact_sheets'/f'{stem}_{label}.jpg',quality=91)
 (R/'reports'/f'{stem}_RENDER.json').write_text(json.dumps({'shot':shot,'selected_native_tag':a.tag,'controller_snapshot':str(controller.relative_to(R)),'controller_sha256':hashlib.sha256(controller.read_bytes()).hexdigest(),'duration':dur,'fps':30,'frames':n,'width':width,'height':round(width*16/9),'source_frame_sha256':hashes,'outputs':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths},'source_sha256':producer_sources},indent=2));print('DONE',stem,flush=True)
if __name__=='__main__':main()
