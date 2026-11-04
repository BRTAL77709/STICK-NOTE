from pathlib import Path
import json,subprocess,hashlib,gzip,os
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=Path(os.environ.get('NOIRFRAME_RUN_DIR',R/'renders'));D=D if D.is_absolute() else R/D;T=json.loads((R/'shared/timeline.json').read_text());V=D/'NOIRFRAME_TOOLCHAIN_INTEGRATION_DEMO.mp4'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]))
p=probe(V);v=next(s for s in p['streams'] if s['codec_type']=='video');a=next(s for s in p['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],int(v['nb_read_frames']))==(1080,1920,'30/1','h264',210);assert abs(float(p['format']['duration'])-7)<.001;assert a['sample_rate']=='48000' and a['codec_name']=='aac'
q=subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],capture_output=True,text=True);assert q.returncode==0 and not q.stderr
b=subprocess.check_output(['ffmpeg','-v','error','-i',str(V),'-vf','scale=108:192','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);f=np.frombuffer(b,np.uint8).reshape(210,192,108,3);means=f.mean((1,2,3));assert means.min()>3;diff=abs(np.diff(f.astype(float),axis=0)).mean((1,2,3));dups=np.flatnonzero(diff==0)+1
source=json.loads(gzip.decompress((R/'remotion/public/frames.json.gz').read_bytes()));expected=[n for n in range(1,len(source)) if source[n]==source[n-1]];unexpected=[int(n) for n in dups if int(n) not in expected];assert not unexpected,('unexpected duplicate frames',unexpected)
h=probe(D/'hyperframes-hud.mov')['streams'][0];assert h['codec_name']=='prores' and 'a' in h['pix_fmt'] and int(h['nb_read_frames'])==120
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(D/'hyperframes-hud.mov'),'-frames:v','1','-pix_fmt','rgba','-f','rawvideo','pipe:1']);alpha=np.frombuffer(raw,np.uint8).reshape(300,920,4)[:,:,3];assert alpha.min()==0 and alpha.max()==255 and ((alpha>0)&(alpha<255)).any()
# Sample exact authored subject frame regions; exclude top HUD and bottom captions.
def image_frame(path,n):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f"select='eq(n,{n})',scale=540:960",'-vsync','0','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);return np.frombuffer(data,np.uint8).reshape(960,540,3)
rows=[]
for n in [10,30,60,88,90,105,135,165,195,209]:
 encoded=image_frame(V,n);original=image_frame(D/'remotion-scene.mp4',n);err=float(abs(encoded[250:850].astype(float)-original[250:850]).mean());assert err<4;rows.append({'frame':n,'time':n/30,'subject_MAE_255':err})
# Audio correlation verifies waveform alignment on the shared sample clock, not subjective listening.
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','pipe:1']),np.float32)
actual=pcm(V);ref=pcm(R/'shared/demo-audio.wav');n=min(len(actual),len(ref));corr=float(np.corrcoef(actual[:n],ref[:n])[0,1]);assert corr>.98
out=Image.new('RGB',(1296,820),'#071521');draw=ImageDraw.Draw(out)
for j,n in enumerate([0,15,30,45,60,89,90,108,132,156,180,209]):
 im=Image.fromarray(f[n]).resize((216,384));out.paste(im,(j%6*216,j//6*410));draw.text((j%6*216+5,j//6*410+390),f'{n/30:.2f}s',fill='white')
out.save(R/'CONTACT_SHEET.jpg',quality=94)
old=json.loads((R/'reports/preservation-before.json').read_text())
for path,hsh in old.items():assert hashlib.sha256((R.parent/path).read_bytes()).hexdigest()==hsh,('prior file changed',path)
report={'ok':True,'format':p,'full_decode':'passed, zero errors','frames':210,'duration':7,'minimum_frame_mean':float(means.min()),'identical_frame_indices':[int(x) for x in dups],'intentional_source_hold_frame_indices':expected,'unexpected_duplicate_frames':unexpected,'hold_note':'Initial 0.25s planted anticipation is deliberately held in the approved pedal source.','transparent_overlay':{'codec':h['codec_name'],'pix_fmt':h['pix_fmt'],'alpha_min':int(alpha.min()),'alpha_max':int(alpha.max()),'partial_alpha_present':True},'subject_checks':rows,'audio_zero_lag_correlation':corr,'subtitle_source':'measured source-script, NOT Whisper; inference blocked','whisper_inference':False,'yt_dlp_downloads':0,'previous_files_unchanged':len(old),'video_sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'artistic_approval':'not claimed'};(R/'reports/demo-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['format','subject_checks']},indent=2))
