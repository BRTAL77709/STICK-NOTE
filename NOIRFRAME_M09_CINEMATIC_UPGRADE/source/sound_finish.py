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
  length=.24 if kind=='fabric_grip' else .18 if kind=='footstep' else .10;tt=np.arange(round(length*RATE))/RATE;noise=rng.standard_normal(len(tt));freq=140 if kind=='footstep' else 1700 if kind=='key' else 95;wave=(.6*noise+.4*np.sin(2*np.pi*freq*tt))*np.exp(-tt/(.030 if kind=='footstep' else .018));start=round(t*RATE);end=min(n,start+len(wave))
  if start>=0 and end>start:out[start:end]+=wave[:end-start]*amp;events.append({'time_s':t,'kind':kind,'amplitude':amp})
 if shot in ['DRIVING_COCKPIT','ROAD_BUILDINGS','CAR_CHASE','CAR_EXIT_RUNNING']:
  vt=np.clip(time*1.1 if shot=='ROAD_BUILDINGS' else time+(9 if shot=='CAR_EXIT_RUNNING' else 0),0,11);speed=np.interp(vt,[d['time'] for d in VS.TABLE],[d['speed'] for d in VS.TABLE]);phase=np.cumsum(2*np.pi*(42+speed*4)/RATE);engine=(np.sin(phase)+.25*np.sin(phase*2)+.15*np.sin(phase*3))*(.025+.025*np.clip(speed/10,0,1));out+=engine;out+=lfilter([.2],[1,-.8],rng.standard_normal(n))*(.010+.006*np.clip(speed/10,0,1));out+=lfilter([.6,-.6],[1,-.25],rng.standard_normal(n))*.008
 else:out+=lfilter([.1],[1,-.9],rng.standard_normal(n))*(.004 if shot=='STAIRS' else .008)
 if shot=='CAR_CHASE':
  braking=np.interp(time,[d['time'] for d in VS.TABLE],[d['brake'] for d in VS.TABLE]);speed=np.interp(time,[d['time'] for d in VS.TABLE],[d['speed'] for d in VS.TABLE]);out+=lfilter([.5,-.5],[1,-.4],rng.standard_normal(n))*.025*braking*np.clip(speed/5,0,1);event(6.2,'brake',.035)
 if shot=='STAIRS':
  stairs=json.load(gzip.open(R/'scenes/STAIRS_M09_NATIVE.json.gz','rt'));prev={s:True for s in ['L','R']}
  for frame in stairs['frames']:
   for side in ['L','R']:
    planted=frame['feet'][side]['target']['planted']
    if planted and not prev[side]:event(frame['time'],'footstep',.10)
    prev[side]=planted
 elif (R/'scenes'/f'{shot}_{a.tag}.json.gz').exists():
  data=json.load(gzip.open(R/'scenes'/f'{shot}_{a.tag}.json.gz','rt'))
  if shot!='DRIVING_COCKPIT':
   prev=[True,True]
   for i,d in enumerate(data['state']):
    for j,f in enumerate(d['pose']['legs']):
     if f['planted'] and not prev[j]:event(i/30,'footstep',.09)
     prev[j]=f['planted']
 if shot=='KEY_LOCK':
  for tt in [3.0,4.0,5.35,6.0,7.4]:event(tt,'key',.045)
 if shot=='DOOR_ENTRY':
  for t,kind in [(.58,'key'),(.85,'door'),(9.85,'door'),(11.6,'key')]:event(t,kind,.09 if kind=='door' else .05)
 if shot=='CAR_EXIT_RUNNING':event(2.55,'key',.05);event(2.8,'door',.09)
 if shot=='WINDOW_CURTAIN':
  cloth=json.load(gzip.open(R/'scenes'/f'{shot}_{a.tag}.json.gz','rt'));edge=np.array([np.asarray(s['fabric'])[:,-1].mean(axis=0) for s in cloth['state']]);velocity=np.r_[0,np.linalg.norm(np.diff(edge,axis=0),axis=1)*30];env=np.interp(time,np.arange(len(edge))/30,np.clip(velocity/.8,0,1));out+=lfilter([.12],[1,-.75],rng.standard_normal(n))*.04*env;grips=[i/30 for i,s in enumerate(cloth['state']) if s['grip_contact']];
  if grips:event(grips[0],'fabric_grip',.012)
 # Gentle endpoint fades; limiter never raises a quiet source to a loud peak.
 fade=np.minimum(1,time/.035)*np.minimum(1,(dur-time)/.06);out*=fade;out*=min(1,.75/max(.001,float(np.max(np.abs(out)))));wav=Path('/tmp')/f'M09_{shot}_FOLEY.wav';write(wav,RATE,(np.clip(out,-1,1)*32767).astype(np.int16));target=R/'renders'/f'M09_{shot}_FINAL.mp4';raw=R/'scratch'/f'M09_{shot}_FINAL_SILENT.mp4';assert target.exists() and not raw.exists();shutil.move(str(target),str(raw))
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-t',str(dur),'-movflags','+faststart',str(target)],check=True)
 report={'source_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'shot':shot,'native_contact_tag':a.tag,'audio_source':'Locally synthesized engine/rain/interaction Foley; no dialogue or paid service','events':events,'sample_rate':RATE,'peak_dBFS':20*math.log10(max(1e-9,float(np.max(np.abs(out))))),'RMS_dBFS':20*math.log10(max(1e-9,float(np.sqrt(np.mean(out*out))))),'clock_alignment_bound_s':1/30,'auditory_review':'USER REVIEW REQUIRED; waveform and synchronization numerically inspected, no claim of human listening approval','silent_video_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'final_sha256':hashlib.sha256(target.read_bytes()).hexdigest()};(R/'reports'/f'{shot}_SOUND.json').write_text(json.dumps(report,indent=2));print('SOUND_MUXED',shot)
if __name__=='__main__':main()
