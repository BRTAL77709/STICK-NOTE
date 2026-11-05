from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1]
final=R/'renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4';assert not final.exists()
subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/'renders/PICTURE_86s.mp4'),'-i',str(R/'audio/FULL_FILM_MIX.flac'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','afade=t=in:d=0.08,afade=t=out:st=85.85:d=0.15','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t','86','-movflags','+faststart',str(final)],check=True)
print('DELIVERABLE',final,flush=True)
