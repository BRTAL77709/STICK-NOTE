"""Independent decoded-frame check: actual encoded subject regions vs raw scene inputs.
This checks that compositing delivered the authored motion, not that it is artistically convincing.
"""
from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];video=R/sys.argv[1];shots=json.loads((R/'storyboard.json').read_text());times=[.4,1.1,2,2.9,4.9,5.3,8.4,9.2,12.5,18.5,24.5,27.5,28.2,28.8,29.5,30,30.7,32.5,33.4,35.3,38,39.5,40.5,42.5,45.5,48.25,49.4,50.2,51.6,52.2,53.5,54.7,55.5,56.5,57.4,58.5,59.4,60.5,61.5,62.4,63.7,64.8,65.3,65.5,66.4,67.5,68.7,69.8,70.7,71.5,72.4,73.4,74.8,76.5,77.6,79.2,80.6];indices=sorted(set(round(t*30) for t in times));W,H=540,960
def frames(path,select):
 expr='+'.join(f'eq(n,{n})' for n in select);b=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f"select='{expr}',scale={W}:{H}",'-vsync','0','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);x=np.frombuffer(b,np.uint8).reshape(-1,H,W,3);assert len(x)==len(select);return dict(zip(select,x))
master=frames(video,indices);rows=[];pairs=[]
for s in shots:
 inds=[n for n in indices if round(s['start']*30)<=n<round(s['end']*30)]
 if not inds:continue
 meta=json.loads((R/f'scenes/scene_{s["scene"]:02d}/final-cache.json').read_text());start=round(s['start']*30);source=frames(R/meta['path'],sorted(set([0]+[n-start for n in inds])))
 n=s['scene'];rect=(40,450,1040,1480) if n in [1,2,3,7,8,9,10] else (40,450,1040,1730) if n in [4,5,6,11,12,13,14] else (40,540,1040,1660);x0,y0,x1,y1=[a//2 for a in rect];crop=lambda a:a[y0:y1,x0:x1].astype(float)
 for idx in inds:
  a=master[idx];b=source[idx-start];A=crop(a);B=crop(b);error=float(np.abs(A-B).mean());frozen=float(np.abs(A-crop(source[0])).mean());actual_move=float(np.abs(B-crop(source[0])).mean());ok=error<4.0 and (actual_move<2 or frozen-error>.5*actual_move);rows.append({'scene':n,'frame':idx,'time':idx/30,'source_frame':idx-start,'subject_crop':rect,'mean_abs_error_255':error,'frozen_first_frame_error':frozen,'source_change_from_first':actual_move,'matches_current_subject':ok})
  if len(pairs)<24:pairs.append((idx/30,Image.fromarray(b).resize((180,320)),Image.fromarray(a).resize((180,320))))
report={'ok':all(x['matches_current_subject'] for x in rows),'checks':rows,'file_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'criterion':'MAE <4/255; when source change >=2/255, correct frame must beat frozen control by >half the actual source change. This uses an additive codec-noise margin rather than halving total error, which includes re-encoding noise.','scope':'Decoded subject crop fidelity; not a subjective acting/animation grade. Captions/counter regions excluded.'};(R/'reports/encoded-subject-fidelity.json').write_text(json.dumps(report,indent=2));out=Image.new('RGB',(1440,350*((len(pairs)+3)//4)),'#07131e');d=ImageDraw.Draw(out)
for j,(t,src,final) in enumerate(pairs):x=j%4*360;y=j//4*350;out.paste(src,(x,y));out.paste(final,(x+180,y));d.text((x+4,y+325),f'{t:.2f}s SOURCE | ENCODED',fill='white')
out.save(R/'reviews/ENCODED_SUBJECT_COMPARISON.jpg',quality=94);print(json.dumps({'ok':report['ok'],'samples':len(rows),'max_error':max(x['mean_abs_error_255'] for x in rows)},indent=2));assert report['ok'],[x for x in rows if not x['matches_current_subject']]
