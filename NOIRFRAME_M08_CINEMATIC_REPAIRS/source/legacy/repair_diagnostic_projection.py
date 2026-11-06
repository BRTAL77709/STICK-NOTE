"""Correct world-space grip overlays without changing/re-rendering clean animation frames."""
from pathlib import Path
import copy,gzip,json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
from render import diagnostic
from shots import SHOTS
from contact_rig import *
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'CURRENT_SHOTS.json').read_text());records={}
for name in ['STEERING','CHASE']:
 row=rows[name];clean=R/row['final'];state=json.load(gzip.open(R/'reports'/f'{name}_M03_C02_1080_STATE.json.gz','rt'));out=R/'diagnostics'/f'{name}_M03_C02_1080_DEBUG_R02.mp4';assert not out.exists();w=1080;h=1920
 dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(clean),'-f','rawvideo','-pix_fmt','rgb24','-threads','1','pipe:1'],stdout=subprocess.PIPE);enc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 for i,d in enumerate(state['state']):
  raw=dec.stdout.read(w*h*3);assert len(raw)==w*h*3;im=Image.frombytes('RGB',(w,h),raw);worlds,_=SHOTS[name][0](i/30);dd=copy.deepcopy(d)
  if d.get('diagnostic_coordinate_space')=='world':
   Rb=RY(d['yaw'])@RZ(d['roll'])@RX(d['pitch']);pivot=V(0,.55,0);o=np.array(d['position']);C=lambda p:o+RY(d['yaw'])@pivot+Rb@(np.array(p)-pivot)
   dd['wheel_center']=C(dd['wheel_center'])
   for group in dd['fingers']:
    for f in group:f['pad']=C(f['pad'])
  if d.get('hide_rig_debug'):dd['fingers']=[];dd.pop('wheel_center',None)
  debug=diagnostic(im,worlds,dd)
  if name=='CHASE':
   draw=ImageDraw.Draw(debug);cam=worlds[0].cam
   for p,yaw,col in [(np.array(d['position']),d['yaw'],'#66e6ff'),(np.array(d['pursuer_position']),d['pursuer_yaw'],'#ffba6b')]:
    a=cam(p+V(0,.8,0));b=cam(p+RY(yaw)@V(0,.8,2.));draw.line([a,b],fill=col,width=4);x,y=a;draw.ellipse((x-6,y-6,x+6,y+6),fill=col)
  enc.stdin.write(debug.tobytes())
 enc.stdin.close();assert enc.wait()==0 and dec.wait()==0;row['diagnostic']=str(out.relative_to(R));records[name]={'clean_source_sha256':hashlib.sha256(clean.read_bytes()).hexdigest(),'diagnostic_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'reason':'Contact overlays must use the same coordinate frame as the displayed world; remove unrelated cockpit points from chase view. Clean motion frames unchanged.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(R/'CURRENT_SHOTS.json').write_text(json.dumps(rows,indent=2));(R/'reports/DIAGNOSTIC_PROJECTION_REPAIR.json').write_text(json.dumps(records,indent=2))
