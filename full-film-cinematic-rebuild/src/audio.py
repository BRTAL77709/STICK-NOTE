"""Original locally synthesized driving mix, scheduled from shared motion units."""
from pathlib import Path
import json,subprocess,wave,math
import numpy as np
from motion_state import *
ROOT=Path(__file__).resolve().parents[1];SR=48000
LINES=[(.30,'He saw me.'),(3.0,'I hit the gas.'),(8.1,'The headlights followed.'),(12.9,'Every turn.')]
def save(p,arr):
 arr=np.asarray(arr);channels=arr.shape[1] if arr.ndim==2 else 1
 with wave.open(str(p),'wb') as w:w.setnchannels(channels);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(arr,-.99,.99)*32767).astype('<i2').tobytes())
def main():
 n=round(DURATION*SR);ts=np.arange(n)/SR;rng=np.random.default_rng(21780);voice=np.zeros(n);segments=[]
 for j,(start,line) in enumerate(LINES):
  tx=ROOT/'assets/audio'/f'phrase_{j}.txt';tx.write_text(line);wav=ROOT/'assets/audio'/f'phrase_{j}.wav'
  if not wav.exists():subprocess.run(['ffmpeg','-v','error','-n','-f','lavfi','-i',f'flite=textfile={tx}:voice=rms','-af','highpass=f=95,lowpass=f=6800','-ar',str(SR),'-ac','1',str(wav)],check=True)
  with wave.open(str(wav),'rb') as w:s=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
  s=s*.54/max(.001,max(abs(s)));off=round(start*SR);assert off+len(s)<n;voice[off:off+len(s)]+=s;segments.append({'start':start,'end':(off+len(s))/SR,'text':line,'asset':str(wav.relative_to(ROOT))})
 (ROOT/'narration-timing.json').write_text(json.dumps(segments,indent=2))
 def stamp(t):
  ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
 (ROOT/'INTEGRATED_TEST_EN.srt').write_text('\n\n'.join(f"{j+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text']}" for j,s in enumerate(segments))+'\n')
 # Shared state evaluated at240Hz and interpolated for audio-rate continuous phase.
 control=np.arange(0,DURATION+1/240,1/240);rp=np.interp(ts,control,[rpm(t) for t in control]);v=np.interp(ts,control,[speed(t) for t in control]);th=np.interp(ts,control,[throttle(t) for t in control]);phase=np.cumsum(rp/60*2)/SR*math.tau
 engine=(np.sin(phase)*.022+np.sin(phase*2)*.010+np.sin(phase*3)*.004)*(.75+th*.55)
 noise=rng.standard_normal(n);road=np.convolve(noise,np.ones(9)/9,mode='same')*(.018+v*.0011)
 rain=(noise-np.roll(noise,1))*.008;wash=np.convolve(rng.standard_normal(n),np.ones(91)/91,mode='same')*.04
 # Wet poles/lamp passes derived from route crossing, not fixed unrelated swishes.
 events=[];dist=np.array([route_z(travel(t)) for t in control]);fx=engine+road+rain+wash
 for z in range(12,220,24):
  if z>travel(DURATION):break
  t=float(np.interp(z,dist,control));env=np.exp(-((ts-t)/.16)**2);fx+=noise*.012*env;events.append({'time':t,'frame':round(t*30),'event':'wet lamp/pole pass','route_z_m':z})
 for t in [4.2,4.66]:
  x=ts-t;env=np.where(x>=0,np.exp(-np.maximum(0,x)*30),0);fx+=.025*np.sin(2*math.pi*350*x)*env
 events.append({'time':4.2,'frame':126,'event':'accelerator press starts; shared throttle/engine load'})
 # Original restrained suspense, no third-party samples.
 score=.010*np.sin(2*math.pi*43*ts)+.007*np.sin(2*math.pi*64.5*ts)
 pulse=(.5+.5*np.sin(2*math.pi*1.1*ts))**8;score+=.014*np.sin(2*math.pi*86*ts)*pulse*ease_array(ts,5,10)
 duck=1-.65*np.convolve(np.minimum(1,np.abs(voice)*8),np.ones(3601)/3601,mode='same');score*=duck;fx*=.65+.35*duck
 fade=np.minimum(1,ts/.15)*np.minimum(1,(DURATION-ts)/.45)
 stereo=np.column_stack((voice+fx+score,voice+np.roll(fx,37)*.96+score))*fade[:,None]
 save(ROOT/'assets/audio/voice_stem.wav',voice);save(ROOT/'assets/audio/fx_stem.wav',np.column_stack((fx,np.roll(fx,37))));save(ROOT/'assets/audio/score_stem.wav',score);save(ROOT/'assets/audio/mix_unmastered.wav',stereo)
 inp=ROOT/'assets/audio/mix_unmastered.wav';out=ROOT/'assets/audio/master.wav'
 r=subprocess.run(['ffmpeg','-v','info','-i',str(inp),'-af','loudnorm=I=-16:TP=-1.5:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);d=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0];(ROOT/'reports/audio-loudness-input.json').write_text(json.dumps(d,indent=2))
 af=f"loudnorm=I=-16:TP=-1.5:LRA=8:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true:print_format=json"
 r=subprocess.run(['ffmpeg','-v','info','-n','-i',str(inp),'-af',af,'-ar',str(SR),'-ac','2',str(out)],capture_output=True,text=True,check=True);(ROOT/'reports/audio-master.json').write_text(json.dumps(json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0],indent=2))
 (ROOT/'audio-cues.json').write_text(json.dumps(events,indent=2));print('Original soundscape,4 phrases, shared RPM engine and mastered stereo complete')
def ease_array(t,a,b):
 u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
if __name__=='__main__':main()
