"""Original local voice reuse and contact-clock Foley. No paid APIs."""
from pathlib import Path
import json,math,gzip,hashlib,shutil,sys
import numpy as np
from scipy.signal import lfilter,resample_poly
from scipy.io.wavfile import read,write
from bootstrap import ROOT as R
import actions,vehicle_system as VS
from dialogue_m11 import CUES
SR=24000;VOICE=Path('/workspace/STICK-NOTE/full-film-v1/assets/audio')
def make(shot,tag='M11R01'):
 dur=actions.DURATIONS[shot];n=round(dur*SR);tt=np.arange(n)/SR;rng=np.random.default_rng(1100+sum(map(ord,shot)));audio=lfilter([.1],[1,-.85],rng.standard_normal(n))*.012;events=[]
 def effect(t,kind,amp=.08):
  q=np.arange(round(.2*SR))/SR;freq={'footstep':115,'key':1700,'latch':220,'door':85,'pickup':650}.get(kind,130);sig=(.5*rng.standard_normal(len(q))+.5*np.sin(2*np.pi*freq*q))*np.exp(-q/.025)*amp;start=round(t*SR);end=min(n,start+len(sig))
  if 0<=start<end:audio[start:end]+=sig[:end-start];events.append({'time_s':t,'kind':kind})
 cache=R/'scenes'/f'{shot}_{tag}.json.gz';states=json.load(gzip.open(cache,'rt'))['state'] if cache.exists() else []
 if shot in ['DRIVING_COCKPIT','ROAD_BUILDINGS','CAR_CHASE','CAR_EXIT_RUNNING','DISCOVERY','PANIC','ARRIVAL']:
  vt=np.clip(tt+(6 if shot in ['DISCOVERY','ARRIVAL'] else 2 if shot=='PANIC' else 0),0,11);vt=np.clip(tt*1.1,0,11) if shot=='ROAD_BUILDINGS' else vt;speed=np.interp(vt,[d['time'] for d in VS.TABLE],[d['speed'] for d in VS.TABLE]);speed=np.zeros_like(speed) if shot=='CAR_EXIT_RUNNING' else speed;phase=np.cumsum(2*np.pi*(42+speed*4)/SR);audio+=(np.sin(phase)+.2*np.sin(2*phase))*(.025+.018*speed/10);audio+=lfilter([.6,-.6],[1,-.25],rng.standard_normal(n))*.01
 if states and shot not in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:
  prev=[True,True]
  for i,s in enumerate(states):
   for j,f in enumerate(s['pose']['legs']):
    if f['planted'] and not prev[j]:effect(i/30,'footstep',.095)
    prev[j]=f['planted']
 if shot=='KEY_LOCK':
  for t in [3.,4.,5.35,6.,7.4]:effect(t,'key',.04)
 if shot=='DOOR_ENTRY':
  for t,k in [(.58,'key'),(.85,'door'),(9.85,'latch'),(11.6,'key')]:effect(t,k)
 if shot=='CAR_EXIT_RUNNING':effect(2.55,'latch');effect(2.8,'door')
 if shot=='WINDOW_CURTAIN':
  edge=np.array([np.array(s['fabric'])[:,-1].mean(0) for s in states]);v=np.r_[0,np.linalg.norm(np.diff(edge,axis=0),axis=1)*30];env=np.interp(tt,np.arange(len(edge))/30,np.clip(v/.8,0,1));audio+=lfilter([.12],[1,-.75],rng.standard_normal(n))*.04*env
 if shot=='PHONE_CALL':
  ring=np.clip(np.sin(2*np.pi*2.6*tt),0,1)**3*(tt<2.15);audio+=.05*(np.sin(2*np.pi*440*tt)+.5*np.sin(2*np.pi*480*tt))*ring;effect(2.2,'pickup',.025)
 voices=[];(R/'sound/voices').mkdir(exist_ok=True)
 for start,name,text in CUES.get(shot,[]):
  src=VOICE/name;dst=R/'sound/voices'/name
  if not dst.exists():shutil.copy2(src,dst)
  rate,w=read(dst);w=w.astype(float)/32768
  if w.ndim>1:w=w.mean(axis=1)
  w=resample_poly(w,SR,rate);i=round(start*SR);j=min(n,i+len(w));audio[i:j]+=w[:j-i]*.85;voices.append({'start':start,'end':min(dur,start+len(w)/SR),'text':text,'asset':str(dst.relative_to(R)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'truncated':i+len(w)>n})
 audio*=np.minimum(1,tt/.025)*np.minimum(1,(dur-tt)/.05);peak=float(np.abs(audio).max());audio*=min(1,.92/max(.001,peak));out=R/'sound'/f'M11_{shot}_{tag}_MASTER.wav';assert not out.exists();write(out,SR,(np.clip(audio,-1,1)*32767).astype(np.int16));report={'shot':shot,'tag':tag,'sample_rate':SR,'events':events,'dialogue':voices,'peak_dBFS':20*math.log10(max(1e-9,float(np.abs(audio).max()))),'RMS_dBFS':20*math.log10(max(1e-9,float(np.sqrt(np.mean(audio**2))))),'audio_scope':'Original local voice WAV files; authored event-based engine/rain/interaction Foley, not acoustic simulation. No human listening approval claimed.'};(R/'reports'/f'{shot}_{tag}_AUDIO.json').write_text(json.dumps(report,indent=2));return out
if __name__=='__main__':
 for shot in (sys.argv[1:] or [s for s in actions.DURATIONS if s!='DRIVER_CHASE']):make(shot);print('AUDIO',shot,flush=True)
