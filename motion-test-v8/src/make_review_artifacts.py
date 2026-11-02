"""Contact sheets decoded from the actual final MP4, including 0.1s loading views."""
from pathlib import Path
import subprocess,json,math
import numpy as np
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1];video=r/'THE_PRICE_OF_SILENCE_MOTION_TEST_V8_8s.mp4'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf','scale=540:960','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,960,540,3);assert len(a)==240
idx=sorted(set(list(range(0,192,9))+[44,45,74,75,134,135,173,174,191,192]+list(range(192,240,3))+[239]))
out=Image.new('RGB',(1296,410*math.ceil(len(idx)/6)),'#06101b');d=ImageDraw.Draw(out)
for n,f in enumerate(idx):
 x=n%6*216;y=n//6*410;out.paste(Image.fromarray(a[f]).resize((216,384)),(x,y));d.text((x+8,y+388),f'{f/30:.3f}s / f{f}',fill='white')
p=r/'THE_PRICE_OF_SILENCE_V8_CONTACT_SHEET.jpg';assert not p.exists();out.save(p,quality=94)
# Actual wide-shot action crops at 0.1s from crouch through release.
indices=list(range(75,177,3))+[185,191]
out=Image.new('RGB',(1200,242*math.ceil(len(indices)/4)),'#06101b');d=ImageDraw.Draw(out)
for n,f in enumerate(indices):
 # World-camera wide framing: illustrated body/action area, no re-rendering.
 im=Image.fromarray(a[f]).crop((100,410,500,700)).resize((300,218));x=n%4*300;y=n//4*242
 out.paste(im,(x,y));d.text((x+8,y+222),f'{f/30:.3f}s / f{f}',fill='white')
p=r/'V8_LOADING_DETAIL.jpg';assert not p.exists();out.save(p,quality=95)
# Four consecutive frames per planted foot during lifting, with registration guides.
out=Image.new('RGB',(960,4*168),'#06101b');d=ImageDraw.Draw(out)
import importlib.util
sp=importlib.util.spec_from_file_location('m',r/'src/render_test_v8.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
for row,(actor,leg) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
 for col,f in enumerate([110,111,112,113]):
  p,on,u=m.foot(f/30,actor,leg);assert on
  cx=(p[0]-16)*.54-21;cy=p[1]*.54-120
  im=Image.fromarray(a[f]).crop((round(cx)-55,round(cy)-50,round(cx)+65,round(cy)+20)).resize((240,140))
  x=col*240;y=row*168;out.paste(im,(x,y));d.line((x,y+106,x+240,y+106),fill='#5cbbbd',width=1);d.text((x+5,y+145),f'C{actor+1} leg{leg} / f{f}',fill='white')
p=r/'V8_PLANTED_FEET.jpg';assert not p.exists();out.save(p,quality=95)
diffs=np.abs(a[1:].astype(np.float32)-a[:-1]).mean(axis=(1,2,3));normal=np.delete(diffs,191)
report={'decoded_frames':len(a),'cut_frame':192,'minimum_frame_mean':float(a.mean(axis=(1,2,3)).min()),'cut_pixel_change':float(diffs[191]),'largest_noncut_change':float(normal.max()),'contact_sheet_frames':idx,'loading_detail_frames':indices,'note':'All review sheets are pixels decoded from the final H.264 MP4, not alternate renders. Foot guides cover four consecutive stance frames per leg; they are visual samples, not a general optical-flow proof.'}
(r/'encoded-visual-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
