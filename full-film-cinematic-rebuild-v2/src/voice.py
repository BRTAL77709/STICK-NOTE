"""Offline KokoroONNX auditions and original phrase synthesis. Existing local model only."""
from pathlib import Path
import os,json,hashlib,wave,subprocess
import numpy as np
import onnxruntime as ort
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parents[1]
MODEL=Path(os.environ.get('KOKORO_MODEL','/workspace/stick-note-dev/models/kokoro-v1.0.onnx'));VOICES=Path(os.environ.get('KOKORO_VOICES','/workspace/stick-note-dev/models/voices-v1.0.bin'))
def save(p,s,sr):
 with wave.open(str(p),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(s,-.99,.99)*32767).astype('<i2').tobytes())
def f0_estimate(x,sr):
 vals=[]
 for st in range(0,len(x)-2048,4800):
  y=x[st:st+2048];y=y-y.mean()
  if np.sqrt(np.mean(y*y))<.025:continue
  ac=np.correlate(y,y,'full')[2047:];lo=int(sr/300);hi=int(sr/65);k=lo+np.argmax(ac[lo:hi])
  if ac[k]/max(1e-9,ac[0])>.45:vals.append(sr/k)
 return float(np.median(vals)) if vals else None

def main():
 opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1;opts.log_severity_level=3
 session=ort.InferenceSession(str(MODEL),sess_options=opts,providers=['CPUExecutionProvider']);k=Kokoro.from_session(session,str(VOICES));metrics=[]
 txt='He saw me. I hit the gas. The headlights followed every turn.'
 for who,sp in [('am_onyx',.92),('am_michael',.96)]:
  path=ROOT/'audio'/f'AUDITION_{who}.wav';assert not path.exists();samples,sr=k.create(txt,voice=who,speed=sp,lang='en-us',sentence_pause=.38,clause_pause=.14)
  save(path,samples,sr);metrics.append({'voice':who,'speed':sp,'duration':len(samples)/sr,'peak':float(np.max(np.abs(samples))),'median_voiced_f0_hz_estimate':f0_estimate(samples,sr),'text':txt})
 # A stock synthetic male voice, no identifiable-person cloning or impersonation.
 chosen='am_onyx';segments=[]
 for j,(start,text) in enumerate([(.28,'He saw me.'),(3.5,'I hit the gas.'),(10.05,'The headlights followed.'),(12.75,'Every turn.')]):
  samples,sr=k.create(text,voice=chosen,speed=.95,lang='en-us',sentence_pause=.34,clause_pause=.14);path=ROOT/'assets/audio'/f'voice_{j}.wav';assert not path.exists();save(path,samples,sr)
  segments.append({'start':start,'end':start+len(samples)/sr,'text':text,'asset':str(path.relative_to(ROOT)),'voice':chosen,'sample_rate':sr})
 assert all(a['end']<=b['start'] for a,b in zip(segments,segments[1:]));assert segments[-1]['end']<15
 (ROOT/'narration-timing.json').write_text(json.dumps(segments,indent=2))
 (ROOT/'reports/voice-evaluation.json').write_text(json.dumps({'runtime':'existing localKokoroONNX CPU; no download or network call','models':[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [MODEL,VOICES]],'auditions':metrics,'selected':chosen,'selection':'Lower-register stock synthetic male delivery; explicit pauses and short sentences. Auditions supplied for user comparison; final voice performance approval remains subjective.','wording':'Original previous test wording retained; no actor imitation.','no_paid_api':True},indent=2));print(json.dumps({'auditions':metrics,'phrases':segments},indent=2),flush=True)
if __name__=='__main__':main()
