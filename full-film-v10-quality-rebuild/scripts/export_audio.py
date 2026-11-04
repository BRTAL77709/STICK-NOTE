from pathlib import Path
import json,wave,subprocess
import numpy as np
R=Path(__file__).resolve().parents[1];A=R/'assets/audio';segments=json.loads((R/'narration-timing.json').read_text())
with wave.open(str(A/'NARRATION.wav'),'rb') as w:sr=w.getframerate();v=np.frombuffer(w.readframes(w.getnframes()),'<i2').copy()
for role in ['narrator','caller']:
 out=np.zeros_like(v)
 for s in segments:
  if s['speaker']==role:
   start=round(s['start']*sr);end=round(s['end']*sr);out[start:end]=v[start:end]
 p=A/(role.upper()+'.wav');assert not p.exists()
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(out.tobytes())
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(p),'-c:a','flac',str(A/(role.upper()+'.flac'))],check=True)
for n in ['FX','SCORE']:
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(A/(n+'.wav')),'-c:a','flac',str(A/(n+'.flac'))],check=True)
# Auditions are copied from actual new production phrases, with no old rejected speech.
for role,scene in [('NARRATOR',1),('CALLER',16)]:
 s=next(s for s in segments if s['scene']==scene);subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/s['asset']),'-c:a','flac',str(A/(role+'_SAMPLE.flac'))],check=True)
print('Separate narrator/caller/FX/score and sample assets exported')
