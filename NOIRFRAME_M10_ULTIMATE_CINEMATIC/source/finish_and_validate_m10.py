"""Finish only completed render files, decode every video frame and verify actual outputs."""
from pathlib import Path
import subprocess,json,hashlib,time,math
from bootstrap import ROOT as R
rows=json.loads((R/'CURRENT_SHOTS.json').read_text());results={}
def check(s,row):
 p=R/row['final'];probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio');duration=row['duration'];n=round(duration*30)
 q=subprocess.run(['ffmpeg','-v','error','-threads','1','-i',str(p),'-map','0:v:0','-f','framemd5','-'],capture_output=True);assert q.returncode==0,q.stderr.decode();frame_rows=[x for x in q.stdout.decode().splitlines() if x and not x.startswith('#')];hashes=[x.split(',')[-1].strip() for x in frame_rows];maxrun=run=1
 for i in range(1,len(hashes)):
  run=run+1 if hashes[i]==hashes[i-1] else 1;maxrun=max(maxrun,run)
 b=subprocess.run(['ffmpeg','-hide_banner','-threads','1','-i',str(p),'-vf','blackdetect=d=0.05:pix_th=0.02','-an','-f','null','-'],capture_output=True);assert b.returncode==0;black=[line for line in b.stderr.decode().splitlines() if 'black_start:' in line]
 fps=v['avg_frame_rate'].split('/');fps=float(fps[0])/float(fps[1]);ok=v['codec_name']=='h264' and v['width']==1080 and v['height']==1920 and v['pix_fmt']=='yuv420p' and abs(fps-30)<1e-9 and len(hashes)==n and abs(float(v['duration'])-duration)<.04 and a['codec_name']=='aac' and not black
 assert ok,(s,v,len(hashes),black)
 result={'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'codec':v['codec_name'],'width':v['width'],'height':v['height'],'pixel_format':v['pix_fmt'],'fps':fps,'duration_s':float(v['duration']),'decoded_frames':len(hashes),'expected_frames':n,'audio_codec':a['codec_name'],'audio_duration_s':float(a['duration']),'decode_errors':q.stderr.decode(),'black_intervals':black,'maximum_exactly_identical_frame_run':maxrun,'maximum_exactly_identical_run_s':maxrun/30,'frozen_frame_scope':'Exact decoded image equality; deliberate short holds are reported, not automatically judged artistically.','technical_status':'TECHNICAL PASS','artistic_status':'USER REVIEW REQUIRED'}
 (R/'reports'/f'{s}_FINAL_MEDIA.json').write_text(json.dumps(result,indent=2));print('VERIFIED_MEDIA',s,len(hashes),'frames',flush=True);return result
for shot,row in rows.items():
 previous=R/'reports'/f'{shot}_FINAL_MEDIA.json';video=R/row['final']
 if previous.exists() and video.exists():
  saved=json.loads(previous.read_text())
  if saved.get('sha256')==hashlib.sha256(video.read_bytes()).hexdigest():results[shot]=saved
while len(results)<len(rows):
 for s,row in rows.items():
  if s in results:continue
  render=R/'reports'/f'M10_{s}_FINAL_RENDER.json'
  if not render.exists():continue
  p=R/row['final'];sound=R/'reports'/f'{s}_SOUND.json'
  if not sound.exists():
   subprocess.run(['python',str(R/'source/sound_finish.py'),'--shot',s],check=True)
  assert sound.exists() and p.exists()
  results[s]=check(s,row);(R/'reports/MEDIA_VALIDATION.json').write_text(json.dumps(results,indent=2))
 if len(results)<len(rows):time.sleep(3)
print('ALL_EIGHT_FINAL_MEDIA_VERIFIED',flush=True)
