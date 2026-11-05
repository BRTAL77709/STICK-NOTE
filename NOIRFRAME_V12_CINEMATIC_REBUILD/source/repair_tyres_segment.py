"""Targeted native-HD rerender of the complete exterior passage; no concealed action/camera cuts.
Reuse unchanged F02 cabin frames/audio, replace frames165..224 with grounded wheel geometry.
"""
from pathlib import Path
import json,subprocess,hashlib
from scenes import driving_scene
from depth_render import DepthRaster
from vehicles import rain_overlay
R=Path(__file__).resolve().parents[1];old=R/'previews/DRIVING_V12_F02_1080.mp4';insert=R/'previews/DRIVING_V12_GROUNDED_TYRES_1080.mp4';out=R/'previews/DRIVING_V12_F03_1080.mp4';assert old.exists() and not insert.exists() and not out.exists();rr=DepthRaster(1080)
enc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(insert)],stdin=subprocess.PIPE)
for f in range(165,225):
 t=f/30;s,d,w=driving_scene(t);im=rr.render(w,lambda a:rain_overlay(a,t,80));enc.stdin.write(im.tobytes())
 if f%15==0:print('TYRE_FRAME',f,flush=True)
enc.stdin.close();assert enc.wait()==0
fc='[0:v]split=2[a][b];[a]trim=end_frame=165,setpts=PTS-STARTPTS[x];[b]trim=start_frame=225,setpts=PTS-STARTPTS[y];[1:v]setpts=PTS-STARTPTS[p];[x][p][y]concat=n=3:v=1:a=0[v]'
subprocess.run(['ffmpeg','-v','error','-n','-i',str(old),'-i',str(insert),'-filter_complex',fc,'-map','[v]','-map','0:a','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-t','12','-movflags','+faststart',str(out)],check=True)
report=json.loads((R/'reports/DRIVING_V12_F02_1080_STATE.json').read_text());report['file']=str(out.relative_to(R));report['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();report['targeted_repair']={'reused_F02_frames':[[0,164],[225,359]],'rerendered_native_HD_frames':[165,224],'new_cuts':False,'audio':'unchanged synchronized F02 diagnostic track','wheel_center_y_m':.30,'wheel_radius_m':.30,'body_roll_applies_to_tyres':False}
for d in report['state']:
 if d['view']=='exterior pursuit':d['tyre_lowest_point_m']=0.;d['tyres_unsprung']=True
report['source_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'source').rglob('*.py') if '__pycache__' not in str(p)};(R/'reports/DRIVING_V12_F03_1080_STATE.json').write_text(json.dumps(report,indent=1));print('COMPLETE',out,flush=True)
