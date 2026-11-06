"""Zero-cost procedural Foley; event times taken from native export contact schedules.
Waveform/sync QC is numeric; no claim of human auditory approval.
"""
from pathlib import Path
import argparse,gzip,json,math,subprocess,hashlib,shutil
import numpy as np
from scipy.signal import lfilter
from scipy.io.wavfile import write
from bootstrap import ROOT as R
import actions,vehicle_system as VS
RATE=24000
def main():
 p=argparse.ArgumentParser();p.add_argument('--shot',required=True);p.add_argument('--tag',default='R07');a=p.parse_args();shot=a.shot
 revisions=json.loads((R/'reports/SHOT_REVISIONS.json').read_text()) if (R/'reports/SHOT_REVISIONS.json').exists() else {}
 a.tag=revisions.get(shot,a.tag)
 dur=actions.DURATIONS[shot];n=round(dur*RATE);time=np.arange(n)/RATE;rng=np.random.default_rng(2007+sum(map(ord,shot)));out=np.zeros(n);events=[]
 def event(t,kind,amp=.08):
  length=.18 if kind=='footstep' else .10;tt=np.arange(round(length*RATE))/RATE;noise=rng.standard_normal(len(tt));freq=140 if kind=='footstep' else 1700 if kind=='key' else 95;wave=(.6*noise+.4*np.sin(2*np.pi*freq*tt))*np.exp(-tt/(.030 if kind=='footstep' else .018));start=round(t*RATE);end=min(n,start+len(wave))
  if start>=0 and end>start:out[start:end]+=wave[:end-start]*amp;events.append({'time_s':t,'kind':kind,'amplitude':amp})
 if shot in ['DRIVING_COCKPIT','ROAD_BUILDINGS','CAR_CHASE','CAR_EXIT_RUNNING']:
  vt=np.clip(time+(9 if shot=='CAR_EXIT_RUNNING' else 0),0,11);speed=np.interp(vt,[d['time'] for d in VS.TABLE],[d['speed'] for d in VS.TABLE]);phase=np.cumsum(2*np.pi*(42+speed*4)/RATE);engine=(np.sin(phase)+.25*np.sin(phase*2)+.15*np.sin(phase*3))*(.025+.025*np.clip(speed/10,0,1));out+=engine;out+=lfilter([.2],[1,-.8],rng.standard_normal(n))*(.010+.006*np.clip(speed/10,0,1));out+=lfilter([.6,-.6],[1,-.25],rng.standard_normal(n))*.008
 else:out+=lfilter([.1],[1,-.9],rng.standard_normal(n))*(.004 if shot=='STAIRS' else .008)
 if shot=='STAIRS':
  for t in [1.20,2.23,3.26,4.29]:event(t,'footstep',.10)
 elif (R/'scenes'/f'{shot}_{a.tag}.json.gz').exists():
  data=json.load(gzip.open(R/'scenes'/f'{shot}_{a.tag}.json.gz','rt'))
  if shot!='DRIVING_COCKPIT':
   prev=[True,True]
   for i,d in enumerate(data['state']):
    for j,f in enumerate(d['pose']['legs']):
     if f['planted'] and not prev[j]:event(i/30,'footstep',.09)
     prev[j]=f['planted']
 if shot=='KEY_LOCK':
  for s in [2.0,2.55,3.15,3.43,3.92]:event(s*7/4.4,'key',.055)
 if shot=='DOOR_ENTRY':
  for t,kind in [(.58,'key'),(.85,'door'),(9.85,'door'),(11.6,'key')]:event(t,kind,.09 if kind=='door' else .05)
 if shot=='CAR_EXIT_RUNNING':event(2.55,'key',.05);event(2.8,'door',.09)
 if shot=='WINDOW_CURTAIN':
  env=np.clip((time-4.8)/.2,0,1)*np.clip((7.2-time)/.25,0,1);out+=lfilter([.12],[1,-.75],rng.standard_normal(n))*.04*env;event(4.72,'key',.025)
 # Gentle endpoint fades; limiter never raises a quiet source to a loud peak.
 fade=np.minimum(1,time/.035)*np.minimum(1,(dur-time)/.06);out*=fade;out*=min(1,.75/max(.001,float(np.max(np.abs(out)))));wav=Path('/tmp')/f'M07_{shot}_FOLEY.wav';write(wav,RATE,(np.clip(out,-1,1)*32767).astype(np.int16));target=R/'renders'/f'M07_{shot}_1080.mp4';raw=R/'scratch'/f'M07_{shot}_1080_SILENT.mp4';assert target.exists() and not raw.exists();shutil.move(str(target),str(raw))
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-t',str(dur),'-movflags','+faststart',str(target)],check=True)
 report={'shot':shot,'native_contact_tag':a.tag,'audio_source':'Locally synthesized engine/rain/interaction Foley; no dialogue or paid service','events':events,'sample_rate':RATE,'peak_dBFS':20*math.log10(max(1e-9,float(np.max(np.abs(out))))),'RMS_dBFS':20*math.log10(max(1e-9,float(np.sqrt(np.mean(out*out))))),'clock_alignment_bound_s':1/30,'auditory_review':'USER REVIEW REQUIRED; waveform and synchronization numerically inspected, no claim of human listening approval','silent_video_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'final_sha256':hashlib.sha256(target.read_bytes()).hexdigest()};(R/'reports'/f'{shot}_SOUND.json').write_text(json.dumps(report,indent=2));print('SOUND_MUXED',shot)
if __name__=='__main__':main()
