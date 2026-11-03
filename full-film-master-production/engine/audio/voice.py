"""New local stock voices; exact measured phrase windows. Creative listening remains pending."""
from pathlib import Path
import os,json,wave,subprocess
import numpy as np
import onnxruntime as ort
from kokoro_onnx import Kokoro
R=Path(__file__).resolve().parents[2]
LINES=[['Two seventeen.','I thought I was alone.'],['Four turns from home.'],['Then something moved in the alley.'],['Two men.','Dragging someone who couldn\'t walk.'],['They lifted him into the trunk.','I froze.'],['The lid shut.','Then he saw me.'],['I hit the gas.'],['Those headlights turned when I did.'],['Every turn. Every street.','Still behind me.'],['One last turn.','Nothing in the mirror.'],['Home. Number seventeen.'],['Locked.','My hands wouldn\'t stop shaking.'],['Inside. I locked it.','Then checked it again.'],['Upstairs...','The black car was waiting.'],['Then my phone rang.'],['One million dollars.','All you have to do is forget what you saw.'],['Call the police, and you\'ll regret it.','We know where you live.'],['A million dollars... or the police.','What would you do?']]
def save(p,a,sr):
 assert not p.exists(),p
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(a,-.99,.99)*32767).astype('<i2').tobytes())
def main():
 op=ort.SessionOptions();op.intra_op_num_threads=2;op.inter_op_num_threads=1;op.log_severity_level=3
 session=ort.InferenceSession(os.environ.get('KOKORO_MODEL','/workspace/stick-note-dev/models/kokoro-v1.0.onnx'),sess_options=op,providers=['CPUExecutionProvider']);k=Kokoro.from_session(session,os.environ.get('KOKORO_VOICES','/workspace/stick-note-dev/models/voices-v1.0.bin'));shots=json.loads((R/'storyboard.json').read_text());segments=[];script=[]
 for s,lines in zip(shots,LINES):
  i=s['scene'];caller=i in [16,17];name='am_echo' if caller else 'bm_daniel';base=.98 if caller else 1.02;clips=[]
  for j,line in enumerate(lines):
   p=R/'assets/audio'/f'scene_{i:02d}_phrase_{j}.wav'
   if p.exists():
    with wave.open(str(p)) as w:sr=w.getframerate();x=np.frombuffer(w.readframes(w.getnframes()),'<i2')/32768.
   else:
    x,sr=k.create(line,voice=name,speed=base,lang='en-us' if caller else 'en-gb');save(p,x,sr)
   clips.append((p,line,len(x)/sr))
  voiced=sum(d for _,_,d in clips)+.12*(len(clips)-1);budget=s['duration']-.42
  if voiced>budget:
   raise RuntimeError(f'Scene {i}: speech {voiced:.2f}s exceeds {budget:.2f}s. Shorten text locally; do not silently time-stretch.')
  cursor=s['start']+.20+max(0,(budget-voiced)*.30)
  for p,line,d in clips:
   segments.append({'scene':i,'start':cursor,'end':cursor+d,'text':line,'speaker':'caller' if caller else 'narrator','voice':name,'asset':str(p.relative_to(R)),'sample_rate':sr});cursor+=d+.12
  script.append(f'## Scene {i:02d} — '+s['title']+'\n\n'+' '.join(lines)+'\n');print('VOICE',i,round(voiced,2),'/',s['duration'],flush=True)
 (R/'narration-timing.json').write_text(json.dumps(segments,indent=2));(R/'NARRATION_SCRIPT.md').write_text('# New English narration / dialogue\n\n'+'\n'.join(script));(R/'reports/voice-evaluation.json').write_text(json.dumps({'narrator':'bm_daniel','caller':'am_echo','new_performances':True,'old_rejected_audio_reused':False,'timing':'Measured whole-phrase sample counts','voice_quality':'NOT CERTIFIED: auditory input unavailable; listening review pending','paid_api':False,'model_outputs':[x.name for x in session.get_outputs()]},indent=2))
if __name__=='__main__':main()
