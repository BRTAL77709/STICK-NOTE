from pathlib import Path
import sys,json,argparse,hashlib,subprocess,math,csv
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));import physical_proofs as p
from illustration_engine import Raster
NAMES={'A':'ACCELERATOR','B':'VEHICLE','C':'DOOR_KEYS','D':'STAIRS','E':'CURTAIN'}
def clean(x):
 if isinstance(x,np.ndarray):return x.tolist()
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if not callable(v) and k not in ('camera',)}
 if isinstance(x,(tuple,list)):return [clean(v) for v in x]
 if isinstance(x,np.generic):return x.item()
 return x
def state(k,t):
 if k=='A':return p.accelerator(t)
 if k=='B':
  c=p.vehicle_camera(t);landmark=(p.motion.road_x(222)+3.08,.045,216.5);return {'time':t,'vehicle':p.vehicle_state(t),'world_camera':{'x':c.x,'y':c.y,'z':c.z,'yaw':c.yaw,'focal':c.f,'horizon':c.h},'landmark_world':landmark,'landmark_screen':c.project(landmark),'landmark_source':'world.terrain crosswalk at z=222, bar j=6, front corner'}
 if k=='C':return p.door_state(min(t,8.5))
 if k=='D':return p.stair_state(t)
 return p.curtain_state(t)
EVENTS={'A':[(0,'anticipation'),(.25,'foot approach'),(.75,'toe contact and heel plant'),(.9,'pressure begins'),(1.9,'full pressure completion'),(2.3,'partial release / body follow-through')], 'B':[(0,'rolling anticipation / tire contact'),(.4,'smooth acceleration begins'),(1,'heading changes with road'),(3.6,'acceleration completes / load release'),(3.72,'delayed body load settles'),(4,'travel completes')], 'C':[(0,'anticipation / reach'),(.6,'handle grip'),(.88,'lever rotated'),(1.03,'failed pull force'),(1.35,'recoil'),(1.95,'key pocket reach'),(2.65,'key retrieved'),(3.15,'key aligned'),(3.65,'key inserted'),(4.35,'key rotation reaches ninety degrees'),(4.425,'lock releases'),(5.1,'key withdrawn'),(5.45,'key stored'),(5.8,'handle regrip'),(6.1,'hinge rotation begins'),(6.65,'entry first step'),(7.45,'door fully open'),(8.5,'entry complete')], 'D':[(.18,'anticipation / lower pelvis'),(.6,'left swing'),(1.18,'left tread 1 plant'),(1.47,'pelvis transfer / right swing'),(2.05,'right tread 2 plant'),(2.35,'weight transfer / left swing'),(2.93,'left tread 3 plant'),(3.2,'right foot follows'),(3.72,'both feet upper tread'),(4,'settled')], 'E':[(0,'approach'),(.6,'arm reach'),(1.15,'fabric grip'),(1.45,'eyes begin tracking reveal'),(1.65,'head rotation follows eyes'),(2.7,'pull completion'),(2.95,'grip release / fabric follow-through'),(4,'fear settles')]}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['preview','final'],default='preview');ap.add_argument('--proofs',default='ABCDE');a=ap.parse_args()
 for k in a.proofs:
  d=p.DURATIONS[k];n=round(d*30);svgs=[p.svg(k,f/30) for f in range(n)];sha=hashlib.sha256(''.join(svgs).encode()).hexdigest();folder=R/'proofs'/k;folder.mkdir(exist_ok=True);w,h=(360,640) if a.stage=='preview' else (1080,1920);out=folder/f'MOTION_PROOF_{k}_{NAMES[k]}_{a.stage}_{sha[:10]}.mp4';meta=folder/(a.stage+'.json')
  if not out.exists():
   rr=Raster(w,h);pr=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','30','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','20','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
   for f,svg in enumerate(svgs):
    pr.stdin.write(rr.render(svg).tobytes())
    if f%90==0:print(k,a.stage,f,n,flush=True)
   pr.stdin.close();assert pr.wait()==0
  meta.write_text(json.dumps({'kind':k,'path':str(out.relative_to(R)),'duration':d,'frames':n,'source_svg_sha256':sha,'width':w,'height':h,'camera':'tracking independent of car' if k=='B' else 'fixed / no cuts','HUD':False,'audio':'silent to expose picture motion'},indent=2))
  if a.stage=='preview':
   data=[clean(state(k,f/30)) for f in range(n+1)];(folder/'JOINTS_TRAJECTORIES.json').write_text(json.dumps({'proof':k,'fps':30,'units':'B/D metric world; A footwell rig coordinates; C/E metric roots/contacts plus projected rig local joints','frames':data},indent=2));(folder/'CONTACT_EVENTS.json').write_text(json.dumps([{'time':t,'frame':math.ceil(t*30-1e-8),'event':name} for t,name in EVENTS[k]],indent=2))
 print('Proof render stage complete',a.stage,flush=True)
if __name__=='__main__':main()
