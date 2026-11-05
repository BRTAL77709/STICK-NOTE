"""Refresh Foley from the current native action plans; retain the newly generated voice performances."""
from pathlib import Path
import sys,json,subprocess
import numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from actions import SHOTS,DURATIONS
sr=48000;out=R/'audio/tests-v2';out.mkdir(exist_ok=False);rng=np.random.default_rng(1705);events=[]
def noise(n,w):return np.convolve(rng.normal(0,1,n),np.ones(w)/w,'same')
def add(m,t,x,g):
 a=round(t*sr);n=min(len(x),len(m)-a)
 if a>=0 and n>0:m[a:a+n]+=x[:n]*g
for kind,dur in DURATIONS.items():
 voice,vsr=sf.read(R/f'audio/tests-v1/{kind}_voice.wav');assert vsr==sr;N=round(dur*sr);tt=np.arange(N)/sr;fx=.018*noise(N,13)+.004*noise(N,3);states=[SHOTS[kind](f/30) for f in range(round(dur*30))]
 for j in range(2):
  for f in range(1,len(states)):
   if states[f]['planted'][j] and not states[f-1]['planted'][j]:
    t=f/30;n=int(.18*sr);u=np.arange(n)/sr;x=.65*noise(n,6)*np.exp(-u*28)+.15*np.sin(2*np.pi*(78-50*u)*u)*np.exp(-u*40);add(fx,t,x,.15);events.append({'shot':kind,'time':t,'event':f'foot{j} landing','world':list(states[f]['feet'][j])})
 if kind=='A':
  speed=np.interp(tt,np.arange(len(states))/30,[s['car']['speed'] for s in states]);rpm=950+speed*180;phase=np.cumsum(rpm/60*2)*2*np.pi/sr;fx+=(.013*np.sin(phase)+.008*np.sin(phase*2)+.004*np.sin(phase*3))*(.7+speed/8);fx+=.022*noise(N,4)*speed/8
 if kind=='B':
  for t,event in [(2.14,'failed handle pull'),(2.78,'key retrieval'),(3.06,'keyring tremor'),(3.27,'keyring tremor'),(3.84,'key insertion'),(4.25,'lock unlock'),(4.8,'latch release')]:
   n=int(.09*sr);u=np.arange(n)/sr;add(fx,t,(noise(n,2)+.2*np.sin(2*np.pi*1450*u))*np.exp(-u*80),.11);events.append({'shot':kind,'time':t,'event':event})
  n=int(1.4*sr);u=np.arange(n)/sr;add(fx,4.8,(.6*noise(n,20)+.03*np.sin(2*np.pi*(190+22*np.sin(u*9))*u))*np.sin(np.pi*u/1.4)**.8,.12)
 if kind=='C':
  n=int(1.6*sr);u=np.arange(n)/sr;add(fx,4.65,noise(n,5)*np.sin(np.pi*u/1.6)**.7,.07);events.append({'shot':kind,'time':4.65,'event':'curtain fabric pull'})
 sf.write(out/f'{kind}_foley.wav',fx,sr);sf.write(out/f'{kind}_raw.wav',voice+fx,sr);subprocess.run(['ffmpeg','-v','error','-n','-i',str(out/f'{kind}_raw.wav'),'-af','loudnorm=I=-16:TP=-2:LRA=8','-ar',str(sr),'-ac','2',str(out/f'{kind}_MIX.wav')],check=True);print(kind,'new contact mix complete',flush=True)
(R/'audio/contact-cues-v2.json').write_text(json.dumps(events,indent=2))
