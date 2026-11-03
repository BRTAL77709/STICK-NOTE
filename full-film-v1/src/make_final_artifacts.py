"""Decode the delivered movie for complete contact sheets and per-scene frame evidence."""
from pathlib import Path
import subprocess,json,math,sys,numpy as np
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1];shots=json.loads((r/'storyboard.json').read_text());dest=r/'delivery' if '--delivery' in sys.argv else r;video=dest/'THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4'
indices=sorted(set([round((s['start']+s['duration']*u)*30) for s in shots for u in [.15,.50,.85]]+[749,750,767,768,1635,1860,1950,2130,2577]))
flt='select='+ '+'.join(f'eq(n\\,{i})' for i in indices)+',scale=216:384';raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf',flt,'-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,384,216,3);assert len(a)==len(indices)
out=Image.new('RGB',(1296,410*math.ceil(len(a)/6)),'#06101b');d=ImageDraw.Draw(out)
for j,f in enumerate(indices):
 x=j%6*216;y=j//6*410;out.paste(Image.fromarray(a[j]),(x,y));scene=next(s['scene'] for s in shots if s['start']<=f/30<s['end']);d.text((x+7,y+388),f'S{scene:02d} / {f/30:.3f}s',fill='white')
p=dest/'THE_PRICE_OF_SILENCE_FULL_FILM_CONTACT_SHEET.jpg';assert not p.exists();out.save(p,quality=95)
# Streaming full-film frame statistics, keeping memory bounded.
p=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-vf','scale=108:192','-pix_fmt','rgb24','-f','rawvideo','pipe:1'],stdout=subprocess.PIPE);previous=None;changes=[];means=[];n=0
while True:
 b=p.stdout.read(108*192*3)
 if not b:break
 assert len(b)==108*192*3
 ar=np.frombuffer(b,dtype=np.uint8);means.append(float(ar.mean()))
 if previous is not None:changes.append({'frame':n,'time':n/30,'mean_rgb_change':float(np.abs(ar.astype(np.int16)-previous.astype(np.int16)).mean())})
 previous=ar;n+=1
assert p.wait()==0 and n==2580
intentional={round(s['start']*30) for s in shots}|{768,1173,1212,1365,1811,1961};noncuts=[x for x in changes if x['frame'] not in intentional]
(dest/'encoded-visual-verification.json').write_text(json.dumps({'decoded_frames':n,'contact_sheet_frames':indices,'minimum_frame_mean':min(means),'largest_noncut_changes':sorted(noncuts,key=lambda x:x['mean_rgb_change'],reverse=True)[:15],'intentional_scene_and_insert_cut_frames':sorted(intentional),'note':'Statistics supplement actual full playback and visual inspection; not a guarantee of artistic quality or every local artifact.'},indent=2))
print('Decoded2580 frames; full contact sheet complete')
