"""Illustrated output of Blender-evaluated skinned meshes. No procedural joint solver here."""
from pathlib import Path
import json,gzip,math,hashlib,argparse,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from world import World
from depth_render import DepthRaster
from approved_head import head
R=Path(__file__).resolve().parents[1]
def P(q):x,y,z=q;return np.array([x,z,-y],float)
class OrthoCamera:
 def __init__(self,c,side=False):
  self.is_orthographic=True;self.eye=P(c['eye']);self.forward=P(c['forward']);self.right=P(c['right']);self.up=P(c['up']);self.s=1920/c['ortho_scale']
  if side:self.eye=np.array([.4,1.15,8.]);self.forward=np.array([0,0,-1.]);self.right=np.array([1.,0,0]);self.up=np.array([0,1.,0]);self.s=1920/3.3
 def depth(self,p):return float((np.array(p)-self.eye)@self.forward)
 def scale(self,p):return self.s
 def __call__(self,p):q=np.array(p)-self.eye;return np.array([540+self.s*(q@self.right),960-self.s*(q@self.up)])

def tint(col,factor):
 h=col.lstrip('#');v=[min(255,max(0,round(int(h[i:i+2],16)*factor))) for i in [0,2,4]];return '#'+''.join(f'{x:02x}' for x in v)

def submit_mesh(w,verts,faces,col,name):
 pts=[P(q) for q in verts];front=[];adj={};normals=[]
 for i,face in enumerate(faces):
  a,b,c=[pts[x] for x in face[:3]];n=np.cross(b-a,c-a);n/=max(1e-12,np.linalg.norm(n));normal=float(n@np.array([-.25,.6,.75]));center=np.mean([pts[x] for x in face],axis=0);visible=n@(w.cam.eye-center)>0;front.append(visible);normals.append(n)
  if visible:
   factor=1.28 if normal>.35 else .70 if normal<-.35 else 1.02
   # Ambient/key bands remain flat illustrated shading, not photorealistic material response.
   lamps=[np.array([-.67,2.02,-.53]),np.array([.80,2.37,-.53])]
   light=max(math.exp(-float(np.linalg.norm(center-l))**2/1.2) for l in lamps)
   h=col.lstrip('#');rgb=np.array([int(h[k:k+2],16) for k in (0,2,4)],float)*factor
   if not name.startswith('SCONCE_GLOW'):
    rgb=rgb*np.array([.80+.39*light,.89+.17*light,.97-.10*light])
   lit='#'+''.join(f'{int(x):02x}' for x in np.clip(rgb,0,255));w.face([pts[x] for x in face],lit,stroke='none',name=name)
  for a,b in zip(face,face[1:]+face[:1]):adj.setdefault(tuple(sorted([a,b])),[]).append(i)
 for (a,b),fids in adj.items():
  if any(front[j] for j in fids) and (len(fids)==1 or not all(front[j] for j in fids)):w.line([pts[a],pts[b]],'#06121c',2.5,bias=-.0025)
 # Crisp fixed architectural tread edges; no wireframe on the character's skin.
 if name.startswith('TREAD'):
  z=max(p[1] for p in pts);xs=[p[0] for p in pts];zs=[p[2] for p in pts];w.line([np.array([min(xs),z,max(zs)]),np.array([max(xs),z,max(zs)])],'#9aa6a5',1.8)

def scene(data,frame,side=False):
 cam=OrthoCamera(frame.get('camera',data['camera']),side);w=World(cam,frame['time'])
 for name,m in data['meshes'].items():
  if name=='APPROVED_HEAD_CARD':continue
  verts=frame['meshes'][name] if m['bound_to_armature'] else m['rest_vertices'];submit_mesh(w,verts,m['faces'],m['color'],name)
 # Foot contact shadows, projected from evaluated shoes onto actual receiving tread surfaces.
 for side_name in ['L','R']:
  shoe=np.array(frame['feet'][side_name]['vertices']);center=shoe.mean(axis=0);bottom=shoe[:,2].min()
  for tread in ['LOWER_FLOOR','TREAD_1','TREAD_2','TREAD_3_LANDING']:
   vv=np.array(data['meshes'][tread]['rest_vertices']);lo=vv.min(axis=0);hi=vv.max(axis=0);z=hi[2];height=max(0,bottom-z)
   if bottom<z-.002 or height>.45:continue
   rx=.105+.08*height;ry=.042+.10*height;cx=center[0]+height*.13;cy=center[1]+height*.09
   # Concentric polygons give a compact cel contact shadow; polygons are clipped to each actual tread.
   for layer,rad,col in [(0,1.15,'#3b4240'),(1,.85,'#27343a'),(2,.58,'#142a34')]:
    if height>.12 and layer==2:continue
    pts=[]
    for a in np.linspace(0,math.tau,20,endpoint=False):
     x=float(np.clip(cx+math.cos(a)*rx*rad,lo[0]+.001,hi[0]-.001));y=float(np.clip(cy+math.sin(a)*ry*rad,lo[1]+.001,hi[1]-.001));pts.append(P([x,y,z+.0005+layer*.0002]))
    if max(p[0] for p in pts)-min(p[0] for p in pts)>.002:w.face(pts,col,stroke='none',name='EVALUATED_SHOE_CONTACT_SHADOW')
 # Hoodie strings are drawn from the actual evaluated chest basis, not a separate animation.
 chest=np.array(frame['bones']['chest']['matrix']);tail=np.array(frame['bones']['chest']['tail']);forward=-chest[:3,0];up=chest[:3,1];lateral=chest[:3,2]
 for sign in [-1,1]:w.line([P(tail+forward*.128+lateral*.052*sign),P(tail+forward*.128+lateral*.052*sign-up*.18)],'#91a3a4',1.8)
 # Vector head texture follows the exported armature-bound head quad exactly in orthographic projection.
 card=np.array(frame['meshes']['APPROVED_HEAD_CARD']);screen=np.array([cam(P(q)) for q in card]);center=screen.mean(axis=0);vx=((screen[1]+screen[2])-(screen[0]+screen[3]))/1200;vy=((screen[0]+screen[1])-(screen[2]+screen[3]))/1200
 def face(a):
  a.add(f'<g transform="matrix({vx[0]} {vx[1]} {vy[0]} {vy[1]} {center[0]} {center[1]})">');head(a,0,0,frame['time'],frame.get('face',{}).get('yaw',.94),frame.get('face',{}).get('gaze',.94),frame.get('face',{}).get('fear',.35),0,blink_override=frame.get('face',{}).get('blink',0));a.add('</g>')
 w.submit([P(q) for q in card],face,-.012)
 return w

def diagnostic(im,data,f):
 im=im.copy();dr=ImageDraw.Draw(im);s=im.width/1080;cam=OrthoCamera(data['camera'],True);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',max(10,round(21*s)))
 def xy(p):return tuple(cam(P(p))*s)
 for side,col in [('L','#ffe077'),('R','#68e8ff')]:
  for chain in [['thigh.'+side,'shin.'+side],['upper_arm.'+side,'forearm.'+side]]:
   p=[f['bones'][chain[0]]['head'],f['bones'][chain[0]]['tail'],f['bones'][chain[1]]['tail']];dr.line([xy(q) for q in p],fill=col,width=max(1,round(3*s)))
   for q in p:x,y=xy(q);dr.ellipse((x-4*s,y-4*s,x+4*s,y+4*s),fill=col)
  foot=f['feet'][side];x,y=xy(foot['ankle_target']);dr.line([(x-8*s,y),(x+8*s,y)],fill='#ff80cf',width=max(1,round(2*s)));dr.line([(x,y-8*s),(x,y+8*s)],fill='#ff80cf',width=max(1,round(2*s)))
  ids=foot['toe_indices'] if foot['target']['contact_mode']=='TOE' else foot['sole_indices']
  for idx in ids:
   x,y=xy(foot['vertices'][idx]);dr.ellipse((x-5*s,y-5*s,x+5*s,y+5*s),fill='#78ff9d' if foot['target']['planted'] else '#ff8475')
 root=[q['bones']['root']['head'] for q in data['frames']];dr.line([xy(q) for q in root],fill='#f29bca',width=max(1,round(2*s)))
 dr.rectangle((0,0,im.width,round(126*s)),fill='#071521');states=' / '.join(f"{side}: {f['feet'][side]['target']['contact_mode']} tread {f['feet'][side]['target']['tread']}" for side in ['L','R']);dr.text((12*s,12*s),f"M05 RETAINED M04 RIG / {f['time']:.3f}s / Blender evaluated",font=font,fill='white');dr.text((12*s,48*s),states,font=font,fill='white');dr.text((12*s,84*s),'Green: evaluated contact / Pink cross: ankle target',font=font,fill='#b1cad2');return im

def main():
 pa=argparse.ArgumentParser();pa.add_argument('--tag',default='R05');pa.add_argument('--width',type=int,default=360);pa.add_argument('--name',default='P01');pa.add_argument('--stills',action='store_true');a=pa.parse_args();path=R/'assets'/f'EVALUATED_{a.tag}.json.gz';data=json.load(gzip.open(path,'rt'));assert hashlib.sha256((R/'assets'/f'STAIRCASE_M05_{a.tag}.blend').read_bytes()).hexdigest()==data['blend_sha256'];assert hashlib.sha256((R/'assets'/f'CONTROLS_{a.tag}.json').read_bytes()).hexdigest()==data['metadata']['controller_sha256'];assert all(hashlib.sha256((R/'source'/n).read_bytes()).hexdigest()==data['metadata']['source_sha256'][n] for n in ['build_rig.py','plan_stairs.py']);width=a.width;height=round(width*16/9);raster=DepthRaster(width);side_raster=DepthRaster(width);stem=f'STAIRS_M05_{a.name}_{width}'
 if a.stills:
  for i in [0,8,24,48,72,96,128,149]:raster.render(scene(data,data['frames'][i])).save(R/'reviews'/f'{stem}_{i:03}.png')
  for key,f in data['ik_mutation'].items():raster.render(scene(data,f)).save(R/'reviews'/f'{stem}_IK_{key}.png')
  return
 outputs=[R/'previews'/(stem+'.mp4'),R/'diagnostics'/(stem+'_DEBUG.mp4')];assert not any(p.exists() for p in outputs);enc=[];hashes=[];samples=[]
 for p in outputs:enc.append(subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(p)],stdin=subprocess.PIPE))
 for i,f in enumerate(data['frames']):
  clean=raster.render(scene(data,f));debug=diagnostic(side_raster.render(scene(data,f,True)),data,f)
  for proc,im in zip(enc,[clean,debug]):proc.stdin.write(im.tobytes())
  hashes.append(hashlib.sha256(clean.tobytes()).hexdigest())
  if i%6==0:samples.append((i,clean.resize((180,320)),debug.resize((180,320))))
  if i%30==0:print(stem,i,'/150',flush=True)
 for p in enc:p.stdin.close();assert p.wait()==0
 for j,label in [(1,'CLEAN'),(2,'CONTACTS')]:
  sheet=Image.new('RGB',(900,344*math.ceil(len(samples)/5)),'#071521');draw=ImageDraw.Draw(sheet)
  for k,row in enumerate(samples):x=k%5*180;y=k//5*344;sheet.paste(row[j],(x,y));draw.text((x+3,y+322),f'{row[0]:03} / {row[0]/30:.3f}s',fill='white')
  sheet.save(R/'reviews'/f'{stem}_{label}_STRIP.jpg',quality=92)
 (R/'reports'/f'{stem}_RENDER.json').write_text(json.dumps({'evaluated_blender_data_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'blend_sha256':data['blend_sha256'],'frames':150,'fps':30,'width':width,'height':height,'source_rgb_sha256':hashes,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').glob('*.py')},'outputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}},indent=2));print('DONE',stem,flush=True)
if __name__=='__main__':main()
