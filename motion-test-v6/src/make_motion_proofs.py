"""Fixed-camera eye ablation + camera-registered strips of actual encoded feet."""
from pathlib import Path
import importlib.util,subprocess,json,math
import numpy as np
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1];sp=importlib.util.spec_from_file_location('v6',r/'src/render_test_v6.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
# The same projected head, no camera reframe or body translation in this diagnostic.
rr=m.Raster(216,216);sheet=Image.new('RGB',(9*216,2*242),'#06101b');d=ImageDraw.Draw(sheet)
for row,hidden in enumerate([False,True]):
 for col in range(9):
  t=3.2+col*.1;a=m.Art();a.add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="-100 -100 240 240" preserveAspectRatio="none"><defs><linearGradient id="face"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#9ca9af"/></linearGradient></defs>');a.rect(-100,-100,240,240,'#07131e');m.draw_head(a,0,0,t,1,hidden);a.add('</svg>')
  im=rr.render(''.join(a.s));x=col*216;y=row*242;sheet.paste(im,(x,y));d.text((x+6,y+220),f'{t:.1f}s / {"eyes hidden" if hidden else "normal"}',fill='white')
out=r/'V6_HEAD_TURN_EYES_HIDDEN.png'
if out.exists():raise SystemExit('Refusing head-proof overwrite')
sheet.save(out)
# Pixels decoded from the final MP4. Ground and feet receive the same inverse camera translation.
v=r/'THE_PRICE_OF_SILENCE_MOTION_TEST_V6_5s.mp4';raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-vf','scale=540:960','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,960,540,3);assert len(frames)==150
sheet=Image.new('RGB',(4*240,6*198),'#06101b');draw=ImageDraw.Draw(sheet);report=[]
for row,(actor,leg) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
 intervals=[];cur=[];lastx=None
 for f in range(30,96):
  x,y,phase=m.foot_state(f/30,actor,leg);on=phase<=.70
  if on and (lastx is None or abs(x-lastx)<1e-7):cur.append(f)
  else:
   if cur:intervals.append(cur)
   cur=[f] if on else []
  lastx=x if on else None
 if cur:intervals.append(cur)
 intervals=[q for q in intervals if len(q)>=7 and m.foot_state(q[0]/30,actor,leg)[0]>130]
 block=max(intervals,key=len);idx=max(0,len(block)//2-2);chosen=block[idx:idx+4];sole_rows=[]
 for col,f in enumerate(chosen):
  t=f/30;fx,fy,_=m.foot_state(t,actor,leg);cam=m.travel(t)*.28+8*m.smooth(t/.8)
  im=Image.fromarray(frames[f]);registered=im.transform(im.size,Image.Transform.AFFINE,(1,0,-cam*.54,0,1,0),Image.Resampling.BILINEAR)
  cx=fx*.54;sole=(fy+3)*.54-125
  pix=np.asarray(registered);x0=max(0,round(cx-8));x1=min(540,round(cx+12));y0=round(sole)-3;y1=round(sole)+4
  scores=pix[y0:y1,x0:x1,:].min(axis=2).mean(axis=1);measured=y0+int(np.argmax(scores));sole_rows.append(measured)
  crop=registered.crop((round(cx)-55,round(sole)-60,round(cx)+55,round(sole)+20)).resize((220,160));x=col*240+10;y=row*198
  sheet.paste(crop,(x,y));draw.line((x,y+120,x+220,y+120),fill='#56c3c4',width=1);draw.line((x+110,y+109,x+110,y+131),fill='#56c3c4',width=1)
  draw.text((x,y+166),f'C{actor+1} leg {leg} / f{f} / {t:.3f}s',fill='white')
 report.append({'actor':actor+1,'leg':leg,'frames':chosen,'world_foot_x':m.foot_state(chosen[0]/30,actor,leg)[0],'encoded_sole_peak_rows_half_resolution':sole_rows,'observed_sole_row_range_pixels':max(sole_rows)-min(sole_rows)})
# Actual grip crops through the first load impulse; guides mark the support anchor.
for actor in (0,1):
 for col,f in enumerate([39,40,41,42]):
  t=f/30;gx,gy=m.upper_arm_targets(t)[4][actor];cam=m.travel(t)*.28+8*m.smooth(t/.8)
  cx=(gx-cam)*.54;cy=gy*.54-125
  crop=Image.fromarray(frames[f]).crop((round(cx)-40,round(cy)-30,round(cx)+40,round(cy)+30)).resize((220,160))
  x=col*240+10;y=(4+actor)*198;sheet.paste(crop,(x,y));draw.line((x+101,y+80,x+119,y+80),fill='#d4bd7e',width=1);draw.line((x+110,y+71,x+110,y+89),fill='#d4bd7e',width=1);draw.text((x,y+166),f'C{actor+1} upper-arm grip / f{f}',fill='white')
out=r/'V6_ENCODED_CONTACTS.png'
if out.exists():raise SystemExit('Refusing foot-proof overwrite')
sheet.save(out);(r/'encoded-foot-verification.json').write_text(json.dumps({'method':'Consecutive actual decoded frames; inverse camera translation registers pavement and planted feet to world space. Cyan guides show fixed predicted sole height/anchor. Brightest sole row is measured locally at half resolution in the displayed samples; not a universal optical-flow guarantee.','samples':report},indent=2));print(json.dumps(report,indent=2))
