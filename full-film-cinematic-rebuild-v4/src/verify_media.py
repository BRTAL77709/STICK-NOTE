"""Independent checks on the actual encoded delivery file."""
from pathlib import Path
import subprocess,json,numpy as np
R=Path(__file__).resolve().parents[1];v=R/'THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4'
p=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(v)]));vid=next(s for s in p['streams'] if s['codec_type']=='video');aud=next(s for s in p['streams'] if s['codec_type']=='audio')
assert [vid['width'],vid['height']]==[1080,1920];assert vid['r_frame_rate']=='30/1';assert vid['codec_name']=='h264';assert int(vid['nb_read_frames'])==450;assert abs(float(p['format']['duration'])-15)<.001
assert aud['codec_name']=='aac' and aud['sample_rate']=='48000' and aud['channels']==2
assert float(vid['start_time'])==0 and float(aud['start_time'])==0
(R/'reports/final-encoding.json').write_text(json.dumps(p,indent=2))
q=subprocess.run(['ffmpeg','-v','error','-i',str(v),'-f','null','-'],capture_output=True,text=True);assert q.returncode==0;qpath=R/'reports/final-decode.txt';qpath.write_text('Full FFmpeg decode exit=0\n'+q.stderr)
b=subprocess.check_output(['ffmpeg','-v','error','-i',str(v),'-vf','scale=54:96','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);frames=np.frombuffer(b,np.uint8).reshape(-1,96,54,3);assert len(frames)==450
means=frames.mean((1,2,3));diff=np.abs(np.diff(frames.astype(float),axis=0)).mean((1,2,3));assert means.min()>5
content={'decoded_frames':len(frames),'minimum_frame_mean_255':float(means.min()),'zero_pixel_change_frame_pairs':int((diff==0).sum()),'minimum_frame_pair_mean_absolute_difference':float(diff.min()),'note':'Pixel changes are technical evidence; they do not establish subjective motion quality.'};(R/'reports/encoded-content.json').write_text(json.dumps(content,indent=2))
m=subprocess.run(['ffmpeg','-v','info','-i',str(v),'-vn','-af','loudnorm=I=-16:TP=-2:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);meter=json.JSONDecoder().raw_decode(m.stderr[m.stderr.rfind('{'):])[0];(R/'reports/final-audio-meter.json').write_text(json.dumps(meter,indent=2))
print(json.dumps({'duration':p['format']['duration'],'video':[vid['codec_name'],vid['width'],vid['height'],vid['r_frame_rate'],vid['nb_read_frames']],'audio':[aud['codec_name'],aud['sample_rate'],aud['channels']],'audio_measured_lufs':meter['input_i'],'audio_true_peak_dbtp':meter['input_tp'],**content},indent=2))
