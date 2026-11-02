"""Actual H.264 frame sheets at short action intervals, including all feet."""
from pathlib import Path
import subprocess,math,json,numpy as np
from PIL import Image,ImageDraw
import render_test_v10 as m
r=Path(__file__).resolve().parents[1];v=r/'THE_PRICE_OF_SILENCE_MOTION_TEST_V10_10s.mp4';raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-vf','scale=540:960','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,960,540,3);assert len(a)==300
idx=sorted(set(list(range(0,240,9))+[41,42,68,69,89,90,137,138,185,186,200,201,224,225,239,240]+list(range(240,300,3))+[299]))
out=Image.new('RGB',(1296,410*math.ceil(len(idx)/6)),'#06101b');d=ImageDraw.Draw(out)
for n,f in enumerate(idx):
 x=n%6*216;y=n//6*410;out.paste(Image.fromarray(a[f]).resize((216,384)),(x,y));d.text((x+8,y+388),f'{f/30:.3f}s / f{f}',fill='white')
p=r/'THE_PRICE_OF_SILENCE_V10_CONTACT_SHEET.jpg';assert not p.exists();out.save(p,quality=94)
indices=list(range(69,237,3))+[239];out=Image.new('RGB',(1200,326*math.ceil(len(indices)/4)),'#06101b');d=ImageDraw.Draw(out)
for n,f in enumerate(indices):
 im=Image.fromarray(a[f]).crop((80,360,540,820)).resize((300,300));x=n%4*300;y=n//4*326;out.paste(im,(x,y));d.text((x+8,y+306),f'{f/30:.3f}s / f{f}',fill='white')
p=r/'V10_LIFTING_LOADING_DETAIL.jpg';assert not p.exists();out.save(p,quality=95)
out=Image.new('RGB',(960,4*168),'#06101b');d=ImageDraw.Draw(out)
for row,(i,j) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
 for col,f in enumerate([110,111,112,113]):
  p,on=m.foot_world(f/30,i,j);assert on;xw,yw=m.P(p);cam=12*m.ease(f/30,0,1.4);cx=(xw-cam)*.54-9;cy=yw*.54-90
  im=Image.fromarray(a[f]).crop((round(cx)-55,round(cy)-50,round(cx)+65,round(cy)+20)).resize((240,140));x=col*240;y=row*168;out.paste(im,(x,y));d.line((x,y+100,x+240,y+100),fill='#5cbbbd',width=1);d.text((x+6,y+145),f'C{i+1} leg{j} / f{f}',fill='white')
p=r/'V10_ENCODED_PLANTED_FEET.jpg';assert not p.exists();out.save(p,quality=95)
diff=np.abs(a[1:].astype(np.float32)-a[:-1]).mean(axis=(1,2,3));normal=np.delete(diff,239)
report={'decoded_frames':len(a),'cut_frame':240,'minimum_frame_mean':float(a.mean(axis=(1,2,3)).min()),'cut_pixel_change':float(diff[239]),'largest_noncut_change':float(normal.max()),'contact_sheet_frames':idx,'loading_detail_frames':indices,'method':'All sheets except the explicitly labeled world overlays are decoded pixels from the final MP4. Four consecutive stance crops per leg are visual samples, not a universal optical-flow guarantee.'}
(r/'encoded-visual-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
