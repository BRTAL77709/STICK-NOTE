"""New stock-neural narrator performances. No V2Onyx audio reused."""
from pathlib import Path
import os,json,wave
import numpy as np
import onnxruntime as ort
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parents[1]
PHRASES=['I hit the gas.','But the headlights followed.','Every turn.','Every street.','They were still behind me.']
def save(p,x,sr=24000):
 assert not p.exists(),p
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(x,-.98,.98)*32767).astype('<i2').tobytes())
def main():
 op=ort.SessionOptions();op.intra_op_num_threads=2;op.inter_op_num_threads=1;op.log_severity_level=3
 model=os.environ.get('KOKORO_MODEL','/workspace/stick-note-dev/models/kokoro-v1.0.onnx');vp=os.environ.get('KOKORO_VOICES','/workspace/stick-note-dev/models/voices-v1.0.bin');session=ort.InferenceSession(model,sess_options=op,providers=['CPUExecutionProvider']);k=Kokoro.from_session(session,vp);evaluations=[];chosen=[]
 for voice,rate,pause in [('am_michael',.94,.40),('bm_george',.91,.56)]:
  clips=[];meta=[]
  for j,txt in enumerate(PHRASES):
   x,sr,timings=k.create_timed(txt,voice=voice,speed=rate,lang='en-us' if voice.startswith('a') else 'en-gb',sentence_pause=.26,clause_pause=.12);clips.append(x);meta.append({'text':txt,'duration':len(x)/sr,'timing_records':len(timings),'peak':float(abs(x).max())})
   if voice=='am_michael':save(ROOT/'assets'/f'phrase_{j}.wav',x);chosen.append((txt,len(x)/sr))
  whole=np.concatenate([part for i,x in enumerate(clips) for part in ([x,np.zeros(round(pause*sr))] if i<len(clips)-1 else [x])]);save(ROOT/'audio'/f'NARRATOR_SAMPLE_{voice}.wav',whole)
  evaluations.append({'voice':voice,'speed':rate,'phrase_pause':pause,'total_duration':len(whole)/sr,'script':' '.join(PHRASES),'phrases':meta})
 # Scene-aligned sentence clips preserve full words, natural internal prosody and real clip durations.
 starts=[2.55,5.7,9.72,11.05,12.38];segments=[]
 for j,((text,dur),start) in enumerate(zip(chosen,starts)):segments.append({'text':text,'start':start,'end':start+dur,'asset':f'assets/phrase_{j}.wav','voice':'am_michael','sample_rate':24000})
 assert all(a['end']<=b['start'] for a,b in zip(segments,segments[1:])),segments
 assert segments[-1]['end']<14.95,segments
 (ROOT/'caption-timing.json').write_text(json.dumps(segments,indent=2));(ROOT/'reports/voice-options.json').write_text(json.dumps({'candidates':evaluations,'selected':'am_michael','selection_basis':'New warmer US stock-neural performance, clearer mid-register contrast to rejected lowOnyx. George supplies a slower British alternative. Neither is an identifiable-person clone. No paidAPI.','audio_status':'Creative listening/voice approval pending; no professional-quality certification from metadata.','model_outputs':[o.name for o in session.get_outputs()],'timing_method':'Actual independently synthesized full-sentence clip boundaries; phoneme timings only if model exposes them; no guessed word timestamps.','no_v2_audio_reused':True},indent=2));print(json.dumps({'candidates':evaluations,'timeline':segments},indent=2),flush=True)
if __name__=='__main__':main()
