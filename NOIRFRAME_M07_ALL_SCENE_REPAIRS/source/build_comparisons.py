"""Same-rate before/after comparisons. Different choreography/cameras are explicitly labelled."""
from pathlib import Path
import subprocess,json
from bootstrap import ROOT as R
base=R.parent;m03=base/'NOIRFRAME_M03/previews';rows=json.loads((R/'CURRENT_SHOTS.json').read_text());m05=base/'NOIRFRAME_M05/previews/STAIRS_M05_CINEMATIC_1080.mp4';film=base/'NOIRFRAME_FULL_FILM_REPRO_VERIFIED/renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4'
old={'DRIVING_COCKPIT':(m03/'STEERING_M03_C02_1080.mp4',0,4,'M03 C02'),'ROAD_BUILDINGS':(m03/'CHASE_M03_C02_1080.mp4',0,6,'M03 C02 chase world'),'CAR_CHASE':(m03/'CHASE_M03_C02_1080.mp4',0,6,'M03 C02'),'CAR_EXIT_RUNNING':(film,42,5,'Existing master 42-47s'),'KEY_LOCK':(m03/'KEY_DOOR_M03_C03_1080.mp4',0,4.4,'M03 C03 key'),'DOOR_ENTRY':(m03/'KEY_DOOR_M03_C03_1080.mp4',4.4,10.6,'M03 C03 entry'),'STAIRS':(m05,0,5,'M05 inherited gait'),'WINDOW_CURTAIN':(m03/'CURTAIN_M03_C02_1080.mp4',0,5,'M03 C02')};report={}
for shot,row in rows.items():
 p,start,dur,label=old[shot];assert p.exists(),p;out=R/row['comparison'];assert not out.exists();d=row['duration'];hold=max(0,d-dur)
 a=f'[0:v]trim=start={start}:duration={dur},setpts=PTS-STARTPTS,scale=540:960,tpad=stop_mode=clone:stop_duration={hold+1},trim=duration={d},drawtext=text=BEFORE - {label}:x=14:y=16:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.8'
 if hold>0:a+=f",drawtext=text=OLD ENDED - HELD FRAME:enable='gte(t,{dur})':x=12:y=920:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.8"
 a+='[a];[1:v]scale=540:960,drawtext=text=M07 - USER REVIEW REQUIRED:x=12:y=16:fontsize=19:fontcolor=white:box=1:boxcolor=black@0.8[b];[a][b]hstack=inputs=2[v]'
 subprocess.run(['ffmpeg','-v','error','-n','-threads','1','-i',str(p),'-i',str(R/row['final']),'-filter_complex_threads','1','-filter_complex',a,'-map','[v]','-an','-t',str(d),'-r','30','-c:v','libx264','-preset','fast','-crf','22','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 report[shot]={'before_path':str(p.relative_to(base)),'before_start_s':start,'before_duration_s':dur,'after_path':row['final'],'comparison':row['comparison'],'speed_multiplier_both':1,'old_end_hold_s':hold,'limits':'Different cuts/timing; not frame-aligned acting. Old ended holds labelled. Stairs is retained M05, not a new gait improvement.'};print('COMPARED',shot,flush=True)
(R/'reports/COMPARISON_SOURCES.json').write_text(json.dumps(report,indent=2))
