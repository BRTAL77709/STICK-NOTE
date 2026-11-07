"""Pinned, hash-verified M10 reference downloads and labeled comparison contact sheets."""
from pathlib import Path
import json,hashlib,subprocess,io
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];base=R/'baseline/m10_reference_videos';base.mkdir(exist_ok=True);plays={}
for p in (R/'baseline/m10/reports').glob('*final-playback.json'):plays.update(json.loads(p.read_text()))
rows=json.loads((R/'CURRENT_SHOTS.json').read_text());shots=['DRIVING_COCKPIT','CAR_EXIT_RUNNING','KEY_LOCK','DOOR_ENTRY','STAIRS','WINDOW_CURTAIN'];out={}
for shot in shots:
 old=plays[shot][0];path=base/Path(old['path']).name;url='https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/651b19f30ac23278445a0b74da71fff5337e895e/NOIRFRAME_M10_ULTIMATE_CINEMATIC/'+old['path']
 if not path.exists():
  data=subprocess.check_output(['curl','-q','-fLsS','--retry','2','--max-time','180',url]);assert hashlib.sha256(data).hexdigest()==old['sha256'];path.write_bytes(data)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==old['sha256']
 new=R/rows[shot]['preview']
 if shot=='STAIRS':new=R/'renders/M11_STAIRS_M11R04_PREVIEW_360.mp4'
 times=[.3,min(2.5,old['duration']-.1),min(old['duration']*.65,rows[shot]['duration']-.1),min(old['duration']-.1,rows[shot]['duration']-.1)];sheet=Image.new('RGB',(8*180,370),'#081b28');dr=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  for j,p in enumerate([path,new]):
   data=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=180:320','-f','image2pipe','-vcodec','png','-']);im=Image.open(io.BytesIO(data));x=(2*i+j)*180;sheet.paste(im,(x,35));dr.text((x+4,5),f'{"M10" if j==0 else "M11"} {t:.2f}s',fill='white')
 outpath=R/'contact_sheets'/f'{shot}_M10_VS_M11_ACTUAL_FRAMES.jpg';sheet.save(outpath,quality=95);out[shot]={'M10_url':url,'M10_sha256':old['sha256'],'M11_file':str(new.relative_to(R)),'M11_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'sheet':str(outpath.relative_to(R)),'times_s':times,'scope':'Equal elapsed shot time, not motion-retimed. Expanded M11 scenes can depict different action phases.'};print(shot,'COMPARED',flush=True)
(R/'reports/M10_VS_M11_COMPARISONS.json').write_text(json.dumps(out,indent=2))
