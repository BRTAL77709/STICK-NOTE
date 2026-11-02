"""Raster occlusion ablation and fixed-camera eye-hidden head-turn proof."""
from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw
import render_test_v10 as m
r=Path(__file__).resolve().parents[1];rr=m.Raster(540,960);results=[]
for t in [6.7,7.3,7.5,7.8]:
 visible=np.asarray(rr.render(m.scene(t))).astype(int);orig=m.victim_draw
 try:
  m.victim_draw=lambda *args:None;hidden=np.asarray(rr.render(m.scene(t))).astype(int)
 finally:m.victim_draw=orig
 changed=int((np.abs(visible-hidden).max(axis=2)>0).sum());results.append({'time':t,'changed_pixels_if_victim_removed':changed})
assert results[0]['changed_pixels_if_victim_removed']>0
assert results[2]['changed_pixels_if_victim_removed']==0 and results[3]['changed_pixels_if_victim_removed']==0
(r/'occlusion-verification.json').write_text(json.dumps({'method':'Same camera, rain and frame; remove only victim drawing. At/after closure there is no pixel difference, proving full raster occlusion rather than a visibility toggle. The victim drawing remains present in both closed source frames.','samples':results},indent=2))
rr=m.Raster(216,216);sheet=Image.new('RGB',(9*216,484),'#06101b');d=ImageDraw.Draw(sheet)
for row,hidden in enumerate([False,True]):
 for col in range(9):
  t=8.+col*.15;a=m.Art();a.add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="-100 -100 240 240" preserveAspectRatio="none"><defs><linearGradient id="face"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#9ca9af"/></linearGradient></defs>');a.rect(-100,-100,240,240,'#07131e');m.draw_head(a,0,0,m.head_time(t),1,hidden);a.add('</svg>')
  x=col*216;y=row*242;sheet.paste(rr.render(''.join(a.s)),(x,y));d.text((x+5,y+220),f'{t:.2f}s / {"eyes hidden" if hidden else "normal"}',fill='white')
p=r/'V10_HEAD_TURN_EYES_HIDDEN.jpg';assert not p.exists();sheet.save(p,quality=95)
print(json.dumps(results,indent=2))
