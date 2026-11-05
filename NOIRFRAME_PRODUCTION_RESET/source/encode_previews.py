from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1];versions={'A':'v10','B':'v11','C':'v12'};rows={}
for k,v in versions.items():
 d=json.loads((R/f'reports/SHOT_{k}_{v}_rig-data.json').read_text());folder=R/f'previews/SHOT_{k}_{v}';assert len(list(folder.glob('frame_*.png')))==d['frames'],('incomplete render',k);out=R/f'previews/SHOT_{k}_{v}_PREVIEW.mp4';assert not out.exists();subprocess.run(['ffmpeg','-v','error','-n','-framerate','30','-start_number','1','-i',str(folder/'frame_%04d.png'),'-i',str(R/f'audio/tests-v2/{k}_MIX.wav'),'-c:v','libx264','-crf','20','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-t',str(d['duration']),'-movflags','+faststart',str(out)],check=True);rows[k]={'preview':str(out.relative_to(R)),'blend':f'blender/SHOT_{k}_{v}.blend','rig_data':f'reports/SHOT_{k}_{v}_rig-data.json','frames':d['frames'],'duration':d['duration']}
(R/'CURRENT_SHOTS.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
