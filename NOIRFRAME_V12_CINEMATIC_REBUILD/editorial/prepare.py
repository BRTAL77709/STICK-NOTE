"""Prepare an empty editorial public directory from delivered proof files. No media overwrite."""
from pathlib import Path
import os,json,subprocess,argparse
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--directory',default='public-final');a=p.parse_args();out=R/'editorial'/a.directory;assert not out.exists(),'Choose a NEW public directory';out.mkdir();shots=json.loads((R/'CURRENT_SHOTS.json').read_text());rows=[];start=0
for k in ['HOUSE','STAIRS','BEDROOM','DRIVING']:
 row=shots[k];after=R/row['final'];assert after.exists();os.link(after,out/(k+'_AFTER.mp4'));n=round(row['duration']*30)
 if k=='DRIVING':
  before=R.parent/'NOIRFRAME_FULL_FILM_V1/renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4';subprocess.run(['ffmpeg','-v','error','-n','-i',str(before),'-t','6','-an','-c:v','libx264','-preset','fast','-crf','22','-threads','2',str(out/(k+'_BEFORE.mp4'))],check=True);bn=180
 else:
  name={'HOUSE':'HOUSE_V11_R08_1080.mp4','STAIRS':'STAIRS_V11_R07_1080.mp4','BEDROOM':'WINDOW_V11_R07_1080.mp4'}[k];os.link(R.parent/'NOIRFRAME_V11_ANIMATION_REPAIR/previews'/name,out/(k+'_BEFORE.mp4'));bn={'HOUSE':330,'STAIRS':255,'BEDROOM':225}[k]
 rows.append({'shot':k,'before':k+'_BEFORE.mp4','after':k+'_AFTER.mp4','frames':n,'beforeFrames':bn,'start':start});start+=n
(R/'editorial/manifest.json').write_text(json.dumps(rows,indent=2));print('EDITORIAL_PREPARED',out)
