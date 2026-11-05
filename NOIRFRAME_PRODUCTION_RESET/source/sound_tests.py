"""New local Kokoro voice tests + original contact-derived Foley; no paid/network calls."""
from pathlib import Path
import sys,json,math,subprocess
import numpy as np,soundfile as sf,onnxruntime as ort
from kokoro_onnx import Kokoro
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from actions import SHOTS,DURATIONS
out=R/'audio/tests-v1';out.mkdir(exist_ok=False);sr=48000;opt=ort.SessionOptions();opt.intra_op_num_threads=2;opt.inter_op_num_threads=1;session=ort.InferenceSession('/workspace/stick-note-dev/models/kokoro-v1.0.onnx',sess_options=opt,providers=['CPUExecutionProvider']);voice=Kokoro.from_session(session,'/workspace/stick-note-dev/models/voices-v1.0.bin');rng=np.random.default_rng(1705)
lines={'A':[(.12,'I hit the gas.'),(2.0,'Those headlights turned when I did.')],'B':[(1.95,'Locked.'),(2.80,"My hands wouldn't stop shaking."),(6.85,'Inside.')],'C':[(.30,'Upstairs.'),(6.25,'It was still there.')]};timings=[];events=[]
def noise(n,window):
 x=rng.normal(0,1,n);return np.convolve(x,np.ones(window)/window,'same')
def add(mix,t,x,gain):
 at=round(t*sr);n=min(len(x),len(mix)-at)
 if at>=0 and n>0:mix[at:at+n]+=x[:n]*gain
for kind,dur in DURATIONS.items():
 N=round(sr*dur);tt=np.arange(N)/sr;fx=.018*noise(N,13)+.004*noise(N,3);narr=np.zeros(N);tshot=[]
 for j,(start,text) in enumerate(lines[kind]):
  wav,vsr=voice.create(text,voice='bm_daniel',speed=1.0,lang='en-gb');active=np.flatnonzero(abs(wav)>.005)
  if len(active):wav=wav[max(0,active[0]-int(vsr*.035)):min(len(wav),active[-1]+int(vsr*.08))]
  sf.write(out/f'{kind}_line{j}.wav',wav,vsr);raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(out/f'{kind}_line{j}.wav'),'-ar',str(sr),'-ac','1','-f','f32le','pipe:1']);x=np.frombuffer(raw,np.float32);end=start+len(x)/sr
  if end>dur-.04:start=max(.04,dur-.06-len(x)/sr);end=start+len(x)/sr
  x=x*.52/max(float(abs(x).max()),.01);add(narr,start,x,1);tshot.append({'shot':kind,'start':start,'end':end,'text':text,'voice':'bm_daniel','engine':'local Kokoro ONNX','tempo_changed':False,'ASR':False})
 states=[SHOTS[kind](f/30) for f in range(round(dur*30))]
 for j in range(2):
  for f in range(1,len(states)):
   if states[f]['planted'][j] and not states[f-1]['planted'][j]:
    t=f/30;n=int(.18*sr);u=np.arange(n)/sr;x=.65*noise(n,6)*np.exp(-u*28)+.15*np.sin(2*np.pi*(78-50*u)*u)*np.exp(-u*40);add(fx,t,x,.15);events.append({'shot':kind,'time':t,'event':f'foot{j} landing','world':list(states[f]['feet'][j])})
 if kind=='A':
  speed=np.interp(tt,np.arange(len(states))/30,[d['car']['speed'] for d in states]);rpm=950+speed*180;phase=np.cumsum(rpm/60*2)*2*np.pi/sr;fx+=(.013*np.sin(phase)+.008*np.sin(phase*2)+.004*np.sin(phase*3))*(.7+speed/8);fx+=.022*noise(N,4)*speed/8
 if kind=='B':
  for t,event in [(2.14,'failed handle pull'),(2.78,'key retrieval'),(3.84,'key insertion'),(4.25,'lock unlock'),(4.8,'latch release')]:
   n=int(.09*sr);u=np.arange(n)/sr;x=(noise(n,2)+.2*np.sin(2*np.pi*1450*u))*np.exp(-u*80);add(fx,t,x,.11);events.append({'shot':kind,'time':t,'event':event})
  n=int(1.4*sr);u=np.arange(n)/sr;x=(.6*noise(n,20)+.03*np.sin(2*np.pi*(190+22*np.sin(u*9))*u))*np.sin(np.pi*u/1.4)**.8;add(fx,4.8,x,.12)
 if kind=='C':
  n=int(1.7*sr);u=np.arange(n)/sr;x=noise(n,5)*np.sin(np.pi*u/1.7)**.7;add(fx,4.65,x,.07);events.append({'shot':kind,'time':4.65,'event':'curtain fabric pull'})
 mix=narr+fx;sf.write(out/f'{kind}_voice.wav',narr,sr);sf.write(out/f'{kind}_foley.wav',fx,sr);sf.write(out/f'{kind}_raw.wav',mix,sr)
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(out/f'{kind}_raw.wav'),'-af','loudnorm=I=-16:TP=-2:LRA=8','-ar',str(sr),'-ac','2',str(out/f'{kind}_MIX.wav')],check=True);timings.extend(tshot);print(kind,'voice+Foley complete',flush=True)
(R/'audio/narration-tests.json').write_text(json.dumps(timings,indent=2));(R/'audio/contact-cues.json').write_text(json.dumps(events,indent=2));(R/'reports/audio-tests.json').write_text(json.dumps({'engine':'Kokoro ONNX CPU','voice':'bm_daniel','sample_rate':sr,'newly_synthesized':True,'paid_api':False,'licenses':'Existing Kokoro Apache2/MIT notices','listening_verified':False,'Whisper_ASR':False,'Whisper_blocker':'Prior official/HF checkpoint CONNECT403; not retried','caption_method':'source text + actual generated WAV duration','foley':'original deterministic synthesized Foley, contact-derived landing times and actual speed-derived engine'},indent=2))
