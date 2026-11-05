"""Render the saved native Blender scene to a lossless-PNG pipe; retain .blend and video caches."""
import bpy,sys,argparse,json,hashlib,subprocess,tempfile,time,os,ctypes,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--shot',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--engine',choices=['cycles','workbench'],default='cycles');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);s=bpy.context.scene;src=Path(bpy.data.filepath);source_hash=hashlib.sha256(src.read_bytes()).hexdigest();out=R/a.out;out.mkdir(parents=True,exist_ok=True);video=out/'NATIVE_1080.mp4';assert not video.exists(),'Preserve existing output; use a new job name';hd=R/f'blender/SHOT_{a.shot}_HD.blend';assert not hd.exists(),'HD .blend already exists; choose a new shot/job ID'
s.render.resolution_percentage=100;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.fps=30;s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';s.render.filepath=f'//../{a.out}/frame_'
if a.engine=='workbench':
 s.render.engine='BLENDER_WORKBENCH';s.render.use_freestyle=False;sh=s.display.shading;sh.light='FLAT';sh.color_type='MATERIAL';sh.show_shadows=False;sh.show_cavity=False;sh.show_object_outline=True;sh.object_outline_color=(.002,.005,.009);sh.background_type='WORLD';s.display.render_aa='FXAA'
bpy.ops.wm.save_as_mainfile(filepath=str(hd),compress=True)
cmd=['ffmpeg','-v','error','-n','-framerate','30','-f','image2pipe','-vcodec','png','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(video)];encoder=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE);frames=[];start=time.monotonic();libc=ctypes.CDLL(None)
with tempfile.TemporaryDirectory(prefix='noirframe-native-') as directory:
 tmp=Path(directory);png=tmp/'frame.png';render_log=tmp/'native-frame.log'
 for f in range(s.frame_start,s.frame_end+1):
  s.frame_set(f);s.render.filepath=str(png);sys.stdout.flush();sys.stderr.flush();libc.fflush(None);saveout=os.dup(1);saveerr=os.dup(2);failure=None
  try:
   with render_log.open('wb') as log:
    os.dup2(log.fileno(),1);os.dup2(log.fileno(),2)
    try:
     result=bpy.ops.render.render(write_still=True)
     if 'FINISHED' not in result:raise RuntimeError(f'Native render did not finish frame {f}: {result}')
    except Exception as exc:failure=exc
    finally:libc.fflush(None);os.dup2(saveout,1);os.dup2(saveerr,2)
  finally:os.close(saveout);os.close(saveerr)
  if failure:
   shutil.copyfile(render_log,R/f'reports/{a.shot}_HD_NATIVE_ERROR.txt');raise failure
  b=png.read_bytes();encoder.stdin.write(b);frames.append({'frame':f,'sha256':hashlib.sha256(b).hexdigest()})
  if f%10==0 or f==s.frame_end:print(a.shot,'native HD',f,'/',s.frame_end,'elapsed',round(time.monotonic()-start,1),flush=True)
 encoder.stdin.close();err=encoder.stderr.read();code=encoder.wait();assert code==0,err.decode()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]));stream=probe['streams'][0];assert int(stream['nb_read_frames'])==s.frame_end-s.frame_start+1;assert stream['width']==1080 and stream['height']==1920;assert abs(float(probe['format']['duration'])-len(frames)/30)<.002
q=subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],capture_output=True);assert q.returncode==0 and not q.stderr,q.stderr.decode();report={'shot':a.shot,'source_blend':str(src.relative_to(R)),'source_blend_sha256':source_hash,'HD_blend':str(hd.relative_to(R)),'HD_blend_sha256':hashlib.sha256(hd.read_bytes()).hexdigest(),'video':str(video.relative_to(R)),'video_sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'frames':len(frames),'render_seconds':time.monotonic()-start,'samples':a.samples,'engine':s.render.engine,'anti_aliasing':s.display.render_aa if a.engine=='workbench' else 'Cycles samples','Blender':bpy.app.version_string,'full_decode':'clean','native_PNG_frame_hashes':frames};(R/f'reports/SHOT_{a.shot}_HD_render.json').write_text(json.dumps(report,indent=2));print('NATIVE HD COMPLETE',a.shot,str(video),flush=True)
