"""Original stereo sound design with neural voice stems and shared vehicle state."""
from pathlib import Path
import subprocess,json,wave,math
import numpy as np
from motion_state import *
ROOT=Path(__file__).resolve().parents[1];SR=48000;N=SR*15

def wav(p,samples):
 a=np.asarray(samples);ch=a.shape[1] if a.ndim==2 else 1
 with wave.open(str(p),'wb') as w:w.setnchannels(ch);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(a,-.99,.99)*32767).astype('<i2').tobytes())
def ea(t,a,b):
 u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
def main():
 ts=np.arange(N)/SR;voice=np.zeros(N);segments=json.loads((ROOT/'narration-timing.json').read_text())
 for s in segments:
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/s['asset']),'-af','highpass=f=75,lowpass=f=10000,acompressor=threshold=0.20:ratio=2:attack=6:release=110','-ar',str(SR),'-ac','1','-f','f32le','pipe:1']);v=np.frombuffer(raw,dtype='<f4').astype(float);start=round(s['start']*SR);voice[start:start+len(v)]+=v*.95
 # Control evaluated at240Hz, interpolated without pitch/displacement jumps.
 ctl=np.arange(0,15+1/240,1/240);states=[state(t) for t in ctl];black=[state(t,True) for t in ctl]
 def interp(k,items=states):return np.interp(ts,ctl,[s[k] for s in items])
 rp=interp('rpm');speedv=interp('speed_mps');load=interp('throttle');phase=np.cumsum(rp/60*2)/SR*math.tau
 motor=(.025*np.sin(phase)+.012*np.sin(phase*2+.2)+.005*np.sin(phase*3))*(.55+.65*load)
 bp=interp('rpm',black);bphase=np.cumsum(bp/60*2)/SR*math.tau;distance=np.interp(ts,ctl,[pursuit_distance(t) for t in ctl])
 pursuing=(np.sin(bphase)*.008+np.sin(bphase*2)*.004)*np.clip(18/distance,0,2)*(ea(ts,9.8,10.5))
 rng=np.random.default_rng(26717);noise=rng.standard_normal(N);noise2=rng.standard_normal(N)
 outside=(1-ea(ts,1.9,2.1))+(ea(ts,6.9,7.1)*(1-ea(ts,9.9,10.1)))+ea(ts,13.2,13.4);outside=np.clip(outside,0,1)
 rain=(noise-np.roll(noise,1))*.0045;rain2=(noise2-np.roll(noise2,1))*.0045
 road=np.convolve(noise,np.ones(15)/15,mode='same')*(.008+speedv*.0016);road2=np.convolve(noise2,np.ones(15)/15,mode='same')*(.008+speedv*.0016)
 body=np.convolve(noise,np.ones(90)/90,mode='same')*.012
 left=motor*.88+pursuing+road*(.50+.50*outside)+rain*(.40+.60*outside)+body
 right=motor*.91+pursuing*.93+road2*(.50+.50*outside)+rain2*(.40+.60*outside)+body
 events=[]
 def cue(t,label,gain=.04,freq=140,dur=.18,pan=0):
  off=round(t*SR);n=min(round(dur*SR),N-off);x=np.arange(n)/SR;sig=gain*(np.sin(2*math.pi*freq*x)*np.exp(-x*25)+rng.standard_normal(n)*.30*np.exp(-x*40));left[off:off+n]+=sig*(1-pan*.5);right[off:off+n]+=sig*(1+pan*.5);events.append({'t':t,'frame':round(t*30),'event':label})
 cue(4,'accelerator pressure / hinge',.035,230,.12);cue(4.7,'boot/pedal settle',.024,110,.14)
 cue(2.15,'danger recognition low accent',.055,54,.23);cue(12.5,'steering load and body cloth',.025,150,.18);cue(14.7,'suspense cut accent',.08,43,.29)
 # Wet street passes and chassis joints use actual fixed-world crossings.
 zpos=np.array([s['z'] for s in states])
 for z in range(12,int(zpos[-1]),24):
  t=float(np.interp(z,zpos,ctl));env=np.exp(-((ts-t)/.13)**2);left+=noise*.012*env;right+=noise2*.012*np.exp(-((ts-t-.035)/.14)**2);events.append({'t':t,'frame':round(t*30),'event':'fixed lamp/pole wet pass','world_z_m':z})
 # Muted contact beats, not arbitrary transition swishes.
 for d in range(22,int(travel(15)),28):
  t=float(np.interp(d,[travel(x) for x in ctl],ctl));cue(t,'road expansion joint / chassis',.014,65,.10,-.25)
 corner=ea(ts,12.4,13.3);left+=noise*.008*corner*(1-ea(ts,14.5,15));right+=noise2*.008*corner*(1-ea(ts,14.5,15))
 score=(.008*np.sin(2*math.pi*43*ts)+.005*np.sin(2*math.pi*64.5*ts));pulse=(.5+.5*np.sin(2*math.pi*1.25*ts))**9
 score+=.012*np.sin(2*math.pi*86*ts)*pulse*(.3+.7*ea(ts,5,11))
 duck=1-.72*np.convolve(np.minimum(1,abs(voice)*7),np.ones(2401)/2401,mode='same');left*=.7+.3*duck;right*=.7+.3*duck;score*=duck
 fade=np.minimum(1,ts/.07)*np.minimum(1,(15-ts)/.12)
 mix=np.column_stack((voice+left+score,voice+right+score))*fade[:,None]
 wav(ROOT/'audio/NARRATION_ONLY.wav',voice);wav(ROOT/'assets/audio/FX.wav',np.column_stack((left,right)));wav(ROOT/'assets/audio/SCORE.wav',score);wav(ROOT/'assets/audio/MIX_UNMASTERED.wav',mix)
 inp=ROOT/'assets/audio/MIX_UNMASTERED.wav';out=ROOT/'audio/MIX_MASTER.wav'
 r=subprocess.run(['ffmpeg','-v','info','-i',str(inp),'-af','loudnorm=I=-16:TP=-2:LRA=8:print_format=json','-f','null','-'],text=True,capture_output=True,check=True);d=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
 af=f"loudnorm=I=-16:TP=-2:LRA=8:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true:print_format=json"
 r=subprocess.run(['ffmpeg','-v','info','-n','-i',str(inp),'-af',af,'-ar',str(SR),'-ac','2',str(out)],text=True,capture_output=True,check=True);meter=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0];(ROOT/'reports/audio-master.json').write_text(json.dumps(meter,indent=2));(ROOT/'audio-cues.json').write_text(json.dumps(events,indent=2))
 def stamp(t):
  n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
 (ROOT/'NARRATION_EN.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text']}" for i,s in enumerate(segments))+'\n');print('Neural narration-only / shared-state stereo engine / wet road / score / master complete',flush=True)
if __name__=='__main__':main()
