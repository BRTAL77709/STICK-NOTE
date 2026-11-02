from pathlib import Path
import subprocess,math,json
import numpy as np
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1];v=r/'THE_PRICE_OF_SILENCE_MOTION_TEST_V6_5s.mp4'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-vf','scale=216:384','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,384,216,3);assert len(a)==150
indices=list(range(0,96,6))+[95]+list(range(96,150,3))+[149]
sheet=Image.new('RGB',(1296,410*math.ceil(len(indices)/6)),'#06101b');draw=ImageDraw.Draw(sheet)
for i,f in enumerate(indices):
 x=i%6*216;y=i//6*410;sheet.paste(Image.fromarray(a[f]),(x,y));draw.text((x+7,y+387),f'{f/30:.3f}s / f{f}',fill='white')
p=r/'THE_PRICE_OF_SILENCE_V6_CONTACT_SHEET.png'
if p.exists():raise SystemExit('Refusing contact sheet overwrite')
sheet.save(p)
diffs=[float(np.abs(a[i].astype(np.float32)-a[i-1]).mean()) for i in range(1,150)];normal=[d for i,d in enumerate(diffs,1) if i!=96]
result={'decoded_frames':len(a),'cut_frame':96,'cut_pixel_change':diffs[95],'median_noncut_change':float(np.median(normal)),'cut_vs_typical':diffs[95]/max(.001,float(np.median(normal))),'minimum_frame_mean':float(a.mean(axis=(1,2,3)).min()),'contact_sheet_frames':indices}
(r/'encoded-visual-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
