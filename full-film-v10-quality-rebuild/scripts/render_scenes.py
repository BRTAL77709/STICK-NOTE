from pathlib import Path
import sys,argparse,hashlib,json,subprocess,time
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import scene_svg,SHOTS,Raster
from scene_sources import evaluate as scene_svg

def render(i,scale,stage):
 s=SHOTS[i-1];h=hashlib.sha256();svgs=[scene_svg(i,f/30) for f in range(s['frames'])];content=hashlib.sha256(''.join(svgs).encode()).hexdigest();cachemeta=R/'scenes'/f'scene_{i:02d}'/f'{stage}-cache.json'
 if cachemeta.exists():
  old=json.loads(cachemeta.read_text())
  if old.get('content_sha')==content and old.get('scale')==scale and (R/old['path']).exists():
   meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','json',str(R/old['path'])]))['streams'][0]
   assert int(meta['nb_read_frames'])==s['frames'];print('CONTENT CACHE',i,old['path'],flush=True);return R/old['path']
 import ast
 base=R/'engine/animation'
 deps=['illustration_engine.py']
 if i in [4,5,6]:deps+=['v10_trunk.py']
 else:
  deps+=['approved_components.py','motion_state.py','world.py','vehicle.py','driver_rig.py','driving.py','render_base.py']
  if i>=11:deps+=['actor.py','house17.py','film_components.py']
 for n in deps:h.update((base/n).read_bytes())
 tree=ast.parse((R/'engine/composition/scene_builder.py').read_text());functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 h.update(ast.unparse(functions['scene_svg']).encode());h.update(ast.unparse(functions['extcam']).encode())
 if i not in [4,5,6]:
  branch=functions['body'].body[0]
  while isinstance(branch,ast.If):
   if eval(compile(ast.Expression(branch.test),'scene-condition','eval'),{}, {'scene':i}):h.update(ast.unparse(ast.Module(body=branch.body,type_ignores=[])).encode());break
   branch=branch.orelse[0] if branch.orelse else None
 h.update(json.dumps(s,sort_keys=True).encode());h.update(str(scale).encode());h.update(content.encode());key=h.hexdigest()[:12];folder=R/'renders'/stage;folder.mkdir(exist_ok=True);out=folder/f'scene_{i:02d}_{key}.mp4'
 if out.exists():
  meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height,r_frame_rate','-of','json',str(out)]))['streams'][0]
  assert int(meta['nb_read_frames'])==s['frames'] and meta['r_frame_rate']=='30/1','Invalid completed cache; preserve it and investigate: '+str(out)
  print('CACHE',out.name,flush=True);return out
 tmp=out.with_suffix('.rendering.mp4')
 if tmp.exists():tmp.rename(R/'renders/previews'/('interrupted_'+str(time.time_ns())+'_'+tmp.name))
 w=round(1080*scale/2)*2;hh=round(1920*scale/2)*2;rr=Raster(w,hh)
 pr=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{hh}','-r','30','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-threads','2','-crf','22' if stage=='final' else '24','-pix_fmt','yuv420p','-movflags','+faststart',str(tmp)],stdin=subprocess.PIPE)
 try:
  for f in range(s['frames']):
   im=rr.render(svgs[f]);pr.stdin.write(im.tobytes())
   if f in [0,s['frames']//2,s['frames']-1]:im.save(R/'renders/previews'/f'{stage}_scene_{i:02d}_{f:03d}_{key}.jpg',quality=94)
   if f%90==0:print(stage,i,f,s['frames'],flush=True)
 finally:pr.stdin.close()
 if pr.wait():raise RuntimeError('Encode failed')
 tmp.rename(out);(R/'scenes'/f'scene_{i:02d}'/f'{stage}-cache.json').write_text(json.dumps({'path':str(out.relative_to(R)),'fingerprint':key,'frames':s['frames'],'content_sha':content,'scale':scale},indent=2));return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--stage',choices=['previews','final'],default='previews');p.add_argument('--scale',type=float);p.add_argument('--scenes',default='1:18');args=p.parse_args();lo,hi=map(int,args.scenes.split(':'));scale=args.scale or (1 if args.stage=='final' else 1/3)
 for i in range(lo,hi+1):render(i,scale,args.stage)
if __name__=='__main__':main()
