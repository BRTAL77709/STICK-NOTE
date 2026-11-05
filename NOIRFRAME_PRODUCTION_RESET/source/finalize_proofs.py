from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];rows={};names={'A':('v11','DRIVING',150),'B':('v11','HOUSE17',234),'C':('v13','STAIRS_WINDOW',240)}
for k,(v,title,n) in names.items():
 report=json.loads((R/f'reports/SHOT_{k}_PROOF_R1_HD_render.json').read_text());assert report['frames']==n and report['full_decode']=='clean';src=R/report['video'];out=R/f'renders/NOIRFRAME_SHOT_{k}_{title}_PROOF_R1.mp4';assert not out.exists()
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(src),'-i',str(R/f'audio/tests-v2/{k}_MIX.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-t',str(n/30),'-movflags','+faststart',str(out)],check=True)
 q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));video=next(x for x in q['streams'] if x['codec_type']=='video');audio=next(x for x in q['streams'] if x['codec_type']=='audio');assert int(video['nb_read_frames'])==n and video['width']==1080 and video['height']==1920 and video['codec_name']=='h264' and video['avg_frame_rate']=='30/1';assert abs(float(q['format']['duration'])-n/30)<.01
 decode=subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True);assert decode.returncode==0 and not decode.stderr
 preview=R/f'previews/SHOT_{k}_PROOF_R1_REVIEW.mp4';subprocess.run(['ffmpeg','-v','error','-n','-i',str(out),'-vf','scale=270:480','-c:v','libx264','-crf','20','-c:a','copy',str(preview)],check=True)
 rows[k]={'final':str(out.relative_to(R)),'preview':str(preview.relative_to(R)),'blend':report['HD_blend'],'rig_data':f'reports/SHOT_{k}_{v}_rig-data.json','frames':n,'duration':n/30,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'codec':'h264','dimensions':[1080,1920],'fps':30,'audio_codec':audio['codec_name'],'full_decode':'clean'}
 asset=R/f'editorial/public/shot-{k}.mp4';asset.symlink_to(out)
(R/'CURRENT_SHOTS.json').write_text(json.dumps(rows,indent=2));(R/'reports/proof-media-validation.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
