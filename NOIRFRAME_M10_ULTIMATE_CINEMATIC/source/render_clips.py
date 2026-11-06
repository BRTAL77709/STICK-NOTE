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
from view_head import draw as view_head
native_style.P=lambda q:np.array([q[1],q[2],q[0]],float)
def Q(q):return np.array([q[1],q[2],q[0]],float)
def body(w,data,f,d):
 hand_pov=d.get('_pov_hand_only',False)
 for name,m in data['topology'].items():
  if name=='APPROVED_HEAD_CARD':continue
  if hand_pov and not (name in ['SLEEVE_UPPER_L','SLEEVE_LOWER_L','MITTEN_L'] or name.startswith('M07_digit') and name.endswith('.L')):continue
  native_style.submit_mesh(w,f['meshes'][name],m['faces'],m['color'],name)
 if hand_pov:return
 card=np.array([Q(q) for q in f['meshes']['APPROVED_HEAD_CARD']]);screen=np.array([w.cam(q) for q in card]);center=screen.mean(axis=0);vx=((screen[1]+screen[2])-(screen[0]+screen[3]))/1200;vy=((screen[0]+screen[1])-(screen[2]+screen[3]))/1200
 def draw(a):
  a.add(f'<g transform="matrix({vx[0]} {vx[1]} {vy[0]} {vy[1]} {center[0]} {center[1]})">');view_head(a,d['time'],d['pose'],w.cam,np.mean(card,axis=0));a.add('</g>')
 w.submit(list(card),draw,-.015)
 # Contact shadows under evaluated soles, not offsets attached to the screen.
 if d['time']>0:
  for s in ['L','R']:
   vv=np.array([Q(q) for q in f['meshes']['SHOE_'+s]]);c=vv.mean(axis=0);z=0.13 if d.get('vehicle_stationary') and c[0]<-4.6 else 0.;height=vv[:,1].min()-z
   if -.002<=height<.24:
    pts=[V(c[0]+.08*math.cos(t),z+.002,c[2]+.10*math.sin(t)) for t in np.linspace(0,math.tau,18,endpoint=False)];w.face(pts,'#102630',stroke='none',name='evaluated shoe shadow')

def scene(shot,t,d,f=None,data=None,debug=False):
 cam=camera(shot,t,d,debug);w=World(cam,t);w.render_frustum=True
 if shot in ['KEY_LOCK','DOOR_ENTRY']:
  sets.house_exterior(w);sets.door_live(w,d)
 elif shot=='WINDOW_CURTAIN':sets.bedroom(w,d)
 elif shot=='DRIVING_COCKPIT':
  o=d['position'];M=RY(d['yaw']);pivot=V(0,.55,0);RR=M@actions.RZ(d['roll'])@actions.RX(d['pitch']);WC=lambda q:o+M@pivot+RR@(q-pivot);ext=World(Camera(WC(cam.eye),WC(cam.target),cam.focal,up=RR@cam.up),t);ext.render_frustum=True;sets.city(ext)
  for op in ext.ops:
   if op[0] in ['face','line']:w.ops.append((op[0],[pivot+RR.T@(p-o-M@pivot) for p in op[1]],*op[2:]))
   elif op[0]=='glyph':w.ops.append(('glyph',[pivot+RR.T@(p-o-M@pivot) for p in op[1]],*op[2:]))
  sets.cockpit(w,d)
 elif shot=='CAR_EXIT_RUNNING':
  vs=VS.state(min(11,9+t));M=RY(vs['yaw']);ext=World(Camera(vs['position']+M@cam.eye,vs['position']+M@cam.target,cam.focal,up=M@cam.up),t);ext.render_frustum=True;sets.city(ext)
  for op in ext.ops:
   if op[0] in ['face','line']:w.ops.append((op[0],[RY(-vs['yaw'])@(p-vs['position']) for p in op[1]],*op[2:]))
   elif op[0]=='glyph':w.ops.append(('glyph',[RY(-vs['yaw'])@(p-vs['position']) for p in op[1]],*op[2:]))
  sets.exit_car(w,d)
 else:sets.city(w);sets.pair(w,d)
 if shot=='WINDOW_CURTAIN' and t>=3 and f is not None:
  # Target-aware illustrated head look: find the registered sedan, then recoil toward the room.
  h=Q(f['bones']['head']['head']);delta=np.array(d['sedan_position'])-h;car_angle=math.atan2(delta[0],delta[2]);angle=-.45*(actions.Q(t,3.15,3.55)-actions.Q(t,4.,4.5))+car_angle*actions.Q(t,5.5,7.05);react=actions.Q(t,7.45,8.3);angle=angle*(1-react)+math.pi*react;pose={**d['pose'],'head_forward':V(math.sin(angle),0,math.cos(angle))};d={**d,'pose':pose}
 if ((shot=='DOOR_ENTRY' and 10.8<=t<13) or (shot=='KEY_LOCK' and t>=1.85)) and not debug:d={**d,'_pov_hand_only':True}
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
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',max(10,round(21*s)));dr.rectangle((0,0,width,round(125*s)),fill='#061622');dr.text((10*s,10*s),f'M10 {shot} / {t:.3f}s / native evaluated joints',font=font,fill='white');dr.text((10*s,46*s),d.get('phase','')[:90],font=font,fill='#b6d3dd');dr.text((10*s,82*s),'Fixed camera / targets pink / actual bone chains yellow-blue',font=font,fill='white');return im

def restore_state(q):
 """Use the exact saved authoring state that produced this evaluated Blender frame."""
 if isinstance(q,dict):return {k:restore_state(v) for k,v in q.items()}
 if isinstance(q,list):
  try:
   a=np.asarray(q)
   if a.size and a.dtype.kind in 'fiu':return a
  except (ValueError,TypeError):pass
  return [restore_state(v) for v in q]
 return q

def main():
 global actions
 p=argparse.ArgumentParser();p.add_argument('--shot',required=True,choices=actions.DURATIONS);p.add_argument('--tag',default='R01');p.add_argument('--width',type=int,default=360);p.add_argument('--stills',action='store_true');p.add_argument('--step',type=int,choices=[1,3],default=1);p.add_argument('--resume',action='store_true');p.add_argument('--final',action='store_true');a=p.parse_args();assert not a.final or a.step==1;shot=a.shot
 revisions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text()) if (R/'reports/SHOT_REVISIONS.json').exists() else {}
 if a.final and shot!='STAIRS':a.tag=revisions.get(shot,a.tag)
 import importlib.util
 controller=R/'source'/f'actions_{a.tag}.py'
 if controller.exists():
  spec=importlib.util.spec_from_file_location('m07_locked_actions_'+a.tag,controller);actions=importlib.util.module_from_spec(spec);spec.loader.exec_module(actions)
 else:controller=R/'source/actions.py'
 width=a.width;dur=actions.DURATIONS[shot];n=round(dur*30);raster=FastDepth(width);data=None
 if shot=='STAIRS':data=json.load(gzip.open(R/'scenes/STAIRS_M10D_NATIVE.json.gz','rt'))
 elif shot not in ['ROAD_BUILDINGS','CAR_CHASE']:
  data=json.load(gzip.open(R/'scenes'/f'{shot}_{a.tag}.json.gz','rt'));assert hashlib.sha256((R/'blender'/f'{shot}_{a.tag}.blend').read_bytes()).hexdigest()==data['blend_sha256']
  for q in ['source/actions.py','source/cameras.py','source/vehicle_system.py','source/bake_native.py','source/embed_assets.py']:
   paths=[controller] if q=='source/actions.py' else [R/q]
   if q=='source/cameras.py':paths += [R/'source/cameras_base_R07.py',R/'source/cameras_R11.py',R/'source/cameras_R12.py',R/'source/cameras_M08A.py',R/'source/cameras_M08E.py',R/'source/cameras_M09D.py',R/'source/cameras_M09E.py',R/'source/cameras_M09G.py',R/'source/cameras_M09K.py',R/'source/cameras_M10A.py']
   if q=='source/bake_native.py':paths += [R/'source/bake_native_R07.py']
   assert any(p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==data['source_sha256'][q] for p in paths),('producer snapshot unavailable',q)
 chase_driver=json.load(gzip.open(R/'scenes'/f'DRIVER_CHASE_{a.tag}.json.gz','rt')) if shot=='CAR_CHASE' else None
 def frame(i):
  t=i/30
  if shot=='CAR_CHASE' and 1.6<=t<3.6:
   dd=restore_state(chase_driver['state'][i]);ff=chase_driver['frames'][i];w=scene('DRIVING_COCKPIT',t,dd,ff,chase_driver);w.cam=camera('DRIVER_CHASE',t,dd);w=World(w.cam,t)
   # Compose with the same registered city and cabin in driver-local coordinates.
   o=dd['position'];M=RY(dd['yaw']);pivot=V(0,.55,0);RR=M@actions.RZ(dd['roll'])@actions.RX(dd['pitch']);WC=lambda q:o+M@pivot+RR@(q-pivot);ext=World(Camera(WC(w.cam.eye),WC(w.cam.target),w.cam.focal,up=RR@w.cam.up),t);ext.render_frustum=True;sets.city(ext)
   for op in ext.ops:
    if op[0] in ['face','line']:w.ops.append((op[0],[pivot+RR.T@(p-o-M@pivot) for p in op[1]],*op[2:]))
    elif op[0]=='glyph':w.ops.append(('glyph',[pivot+RR.T@(p-o-M@pivot) for p in op[1]],*op[2:]))
   sets.cockpit(w,dd);body(w,chase_driver,ff,dd);im=raster.render(w);debug=None if a.final else raster.render(scene('CAR_CHASE',t,actions.state('CAR_CHASE',t),None,None,True));return im,debug,dd
  if shot=='STAIRS':
   f=data['frames'][i];im=raster.render(stair_style.scene(data,f));debug=None if a.final else stair_style.diagnostic(raster.render(stair_style.scene(data,f,True)),data,f);return im,debug,{}
  d=restore_state(data['state'][i]) if data else actions.state(shot,t);f=data['frames'][i] if data else None;im=raster.render(scene(shot,t,d,f,data));debug=None if a.final else (debug_image(shot,t,d,f,width) if data else raster.render(scene(shot,t,d,None,None,True)));return im,debug,d
 stem=f'M10_{shot}_FINAL' if a.final else f'M10_{shot}_{a.tag}_{width}'
 if a.stills:
  for i in sorted(set([0,n//5,n//2,n*3//4,n-1])):
   im,debug,d=frame(i);im.save(R/'contact_sheets'/f'{stem}_{i:03}.png');debug.save(R/'contact_sheets'/f'{stem}_{i:03}_DEBUG.png')
  return
 paths=[R/'renders'/(stem+'.mp4')]+([] if a.final else [R/'debug'/(stem+'_DEBUG.mp4')]);
 if a.resume:
  assert a.final and not (R/'reports'/f'{stem}_RENDER.json').exists(),'Completed exports cannot be overwritten'
  for q in paths:
   if q.exists():q.rename(R/'scratch'/(q.stem+'_INTERRUPTED_'+str(time.time_ns())+'.mp4'))
 assert not any(q.exists() for q in paths);enc=[]
 for path in paths:enc.append(subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{round(width*16/9)}','-r',str(30/a.step),'-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE))
 producer_sources={str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in (R/'source').rglob('*') if q.is_file() and q.suffix in ['.py','.cpp','.so']};samples=[];hashes=[];start=time.monotonic()
 if a.final:
  cache_root=R/'frames'/stem;cache_root.mkdir(exist_ok=True)
  native_cache=R/'scenes'/('STAIRS_M10D_NATIVE.json.gz' if shot=='STAIRS' else f'DRIVER_CHASE_{a.tag}.json.gz' if shot=='CAR_CHASE' else f'{shot}_{a.tag}.json.gz')
  fingerprint=hashlib.sha256(json.dumps({'sources':{k:v for k,v in producer_sources.items() if k.startswith('source/legacy/') or k.split('/')[-1] in ['render_clips.py','cameras.py','sets.py','vehicle_system.py','native_style.py','stair_style.py','fast_depth.py','depth_render.py','fast_raster.so','approved_head.py','approved_head_view.py','view_head.py','svg.py',controller.name]},'width':width,'duration':dur,'native_cache_sha256':hashlib.sha256(native_cache.read_bytes()).hexdigest() if native_cache.exists() else None},sort_keys=True).encode()).hexdigest()
  stamp=cache_root/'PRODUCER.json'
  if stamp.exists():assert json.loads(stamp.read_text())['fingerprint']==fingerprint,'Source changed: preserve old frames in a separate history folder before rendering a new revision'
  else:stamp.write_text(json.dumps({'fingerprint':fingerprint,'width':width,'height':round(width*16/9),'fps':30,'master':'native-resolution lossless PNG frames'},indent=2))
 for i in range(0,n,a.step):
  cache_dir=R/'frames'/stem;cache_dir.mkdir(exist_ok=True);cached=cache_dir/f'{i:05}.png'
  if a.final and cached.exists():im=Image.open(cached).convert('RGB');debug=None;d={}
  else:
   im,debug,d=frame(i)
   if a.final:im.save(cached)
  for proc,img in zip(enc,[im,debug]):proc.stdin.write(img.tobytes())
  hashes.append(hashlib.sha256(im.tobytes()).hexdigest())
  if i%12==0:samples.append((i,im.resize((180,320)),debug.resize((180,320)) if debug is not None else None))
  if i%30==0:print(stem,i,'/',n,'elapsed',round(time.monotonic()-start,1),flush=True)
 for proc in enc:proc.stdin.close();assert proc.wait()==0
 for idx,label in ([(1,'CLEAN')] if a.final else [(1,'CLEAN'),(2,'DEBUG')]):
  sheet=Image.new('RGB',(900,344*math.ceil(len(samples)/5)),'#071521');dr=ImageDraw.Draw(sheet)
  for k,row in enumerate(samples):x=k%5*180;y=k//5*344;sheet.paste(row[idx],(x,y));dr.text((x+3,y+322),f'{row[0]/30:.2f}s',fill='white')
  sheet.save(R/'contact_sheets'/f'{stem}_{label}.jpg',quality=91)
 (R/'reports'/f'{stem}_RENDER.json').write_text(json.dumps({'shot':shot,'selected_native_tag':a.tag,'controller_snapshot':str(controller.relative_to(R)),'controller_sha256':hashlib.sha256(controller.read_bytes()).hexdigest(),'duration':dur,'fps':30/a.step,'frames':len(hashes),'width':width,'height':round(width*16/9),'source_frame_sha256':hashes,'outputs':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths},'source_sha256':producer_sources},indent=2));print('DONE',stem,flush=True)
if __name__=='__main__':main()
