"""Original event-driven ambience, foley and score; new neural speech, never old Flite."""
from pathlib import Path
import sys,subprocess,json,wave,math
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'engine/animation'))
from motion_state import state,pursuit_distance,travel,ease
from house17 import EVENTS
from choreography import RUN_LOCAL,ENTRY_LOCAL,ENTRY_DISTANCE_UNITS,STAIRS_LOCAL,STAIRS_GLOBAL_START
SR=48000;D=86;N=SR*D

def save(p,x):
 assert not p.exists(),p
 a=np.asarray(x);ch=a.shape[1] if a.ndim==2 else 1
 with wave.open(str(p),'wb') as w:w.setnchannels(ch);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(a,-.99,.99)*32767).astype('<i2').tobytes())
def main():
 ts=np.arange(N)/SR;voice=np.zeros(N);segments=json.loads((R/'narration-timing.json').read_text());events=[]
 for s in segments:
  filt='highpass=f=75,lowpass=f=10000,acompressor=threshold=0.17:ratio=2.2:attack=5:release=100'
  if s['speaker']=='caller':filt+=',highpass=f=280,lowpass=f=3200'
  b=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/s['asset']),'-af',filt,'-ar',str(SR),'-ac','1','-f','f32le','pipe:1']);x=np.frombuffer(b,'<f4').astype(float);x*=.48/max(.01,float(abs(x).max()));start=round(s['start']*SR);voice[start:start+len(x)]+=x
 ctl=np.arange(0,D+1/120,1/120);ss=[state(float(t)) for t in ctl];interp=lambda k:np.interp(ts,ctl,[s[k] for s in ss]);rp=interp('rpm');vel=interp('speed_mps');phase=np.cumsum(rp/60*2)/SR*math.tau
 engine=(.016*np.sin(phase)+.008*np.sin(2*phase)+.004*np.sin(3*phase))*(.35+np.clip(vel/18,0,1))*(ts<49)
 rng=np.random.default_rng(71726);n1=rng.standard_normal(N);n2=rng.standard_normal(N)
 outdoors=np.ones(N);outdoors[(ts>=4)&(ts<12)]=.35;outdoors[(ts>=28)&(ts<32)]=.35;outdoors[(ts>=55)]=.12
 rain=(n1-np.roll(n1,1))*.0035*outdoors;rain2=(n2-np.roll(n2,1))*.0035*outdoors
 road=np.convolve(n1,np.ones(17)/17,mode='same')*(.005+.0011*vel)*(ts<49);road2=np.convolve(n2,np.ones(17)/17,mode='same')*(.005+.0011*vel)*(ts<49)
 wind=np.convolve(n1,np.ones(120)/120,mode='same')*.015
 bs=[state(float(t),True) for t in ctl];brp=np.interp(ts,ctl,[s['rpm'] for s in bs]);bp=np.cumsum(brp/60*2)/SR*math.tau;gap=np.interp(ts,ctl,[pursuit_distance(float(t)) for t in ctl]);pursuer=(.005*np.sin(bp)+.002*np.sin(bp*2))*np.clip(20/np.maximum(6,gap),0,2)*((ts>=32)&(ts<42))
 phone_air=n1*.0007*((ts>=66.45)&(ts<80))
 left=engine+pursuer+rain+road+wind+phone_air;right=engine*.95+pursuer*.9+rain2+road2+wind+phone_air
 def cue(t,name,kind='click',gain=.04,dur=.15):
  pos=round(t*SR);num=min(round(dur*SR),N-pos);x=np.arange(num)/SR
  if kind=='ring':y=(np.sin(2*math.pi*440*x)+.5*np.sin(2*math.pi*480*x))*.5*np.minimum(1,x/.02)*np.minimum(1,(dur-x)/.03)
  elif kind=='cloth':y=rng.standard_normal(num)*np.exp(-x*13)*.35
  elif kind=='thud':y=(np.sin(2*math.pi*73*x)+.25*rng.standard_normal(num))*np.exp(-x*22)
  elif kind=='key':y=(np.sin(2*math.pi*1800*x)+.6*np.sin(2*math.pi*2750*x))*np.exp(-x*35)
  else:y=(np.sin(2*math.pi*270*x)+.2*rng.standard_normal(num))*np.exp(-x*32)
  left[pos:pos+num]+=y*gain;right[pos:pos+num]+=y*gain*.94;events.append({'time':t,'frame':round(t*30),'name':name,'kind':kind,'source':'original procedural synthesis'})
 # V10 events are mapped from the exact preserved action clock.
 def trunk_global(q):return 12+q/1.95*6 if q<1.95 else (18+(q-1.95)/4.75*6 if q<6.7 else 24+(q-6.7)/3.3*4)
 for q,name,kind in [(1.95,'trunk hinge opening','click'),(2.6,'grip reposition','cloth'),(3.05,'coordinated lift exertion','cloth'),(6.25,'victim placed in trunk','thud'),(6.7,'hands withdraw','cloth'),(7.5,'trunk closure','thud'),(7.5,'trunk latch','click')]:cue(trunk_global(q),name,kind,.055 if kind=='thud' else .035)
 for u,name in EVENTS:
  if 'threshold footfall' in name:continue
  cue(51+u,name,'key' if 'key' in name else ('thud' if 'closes' in name or 'footfall' in name else 'click'),.035)
 # Entry contacts use the same absolute progression/phase as the projected feet.
 for distance in [53,106,159,212,265,318]:
  lo,hi=ENTRY_LOCAL
  for _ in range(30):
   mid=(lo+hi)/2
   if ease(mid,*ENTRY_LOCAL)<distance/ENTRY_DISTANCE_UNITS:lo=mid
   else:hi=mid
  cue(51+(lo+hi)/2,'entry foot plant','thud',.025,.09)
 cue(28.55,'accelerator contact','click');cue(29.42,'boot pressure settles','thud',.025);cue(38,'steering load','cloth',.03)
 for p in np.arange(53,410,53):
  q=p/410;lo,hi=RUN_LOCAL
  for _ in range(30):
   mid=(lo+hi)/2
   if ease(mid,*RUN_LOCAL)<q:lo=mid
   else:hi=mid
  cue(47+(lo+hi)/2,'run foot plant','thud',.028,.09)
 for k in range(1,11):
  lo,hi=STAIRS_LOCAL
  for _ in range(30):
   mid=(lo+hi)/2
   if ease(mid,*STAIRS_LOCAL)<k/10:lo=mid
   else:hi=mid
  cue(STAIRS_GLOBAL_START+(lo+hi)/2,'stair footfall','thud',.026,.09)
 cue(60.1,'curtain grip','cloth',.022);cue(60.6,'curtain folds slide','cloth',.03,.42)
 for t in [63.1,63.75,64.4]:cue(t,'phone vibration','thud',.028,.13);cue(t+.07,'phone ring','ring',.025,.32)
 cue(64.65,'phone grasp','cloth',.022);cue(66.45,'call answer','click',.025)
 # Low original pulse; two near-silences before the stare and the phone call.
 score=.007*np.sin(2*math.pi*64.5*ts)+.004*np.sin(2*math.pi*96.7*ts)
 pulse=(.5+.5*np.sin(2*math.pi*np.where(ts<28,1.1,1.65)*ts))**12;score+=.006*np.sin(2*math.pi*129*ts)*pulse
 silence=np.ones(N);silence[(ts>24.7)&(ts<25.35)]=.15;silence[(ts>62.55)&(ts<63.1)]=.1;score*=silence
 duck=1-.72*np.convolve(np.minimum(1,abs(voice)*7),np.ones(2401)/2401,mode='same');left*=.75+.25*duck;right*=.75+.25*duck;score*=duck
 fade=np.minimum(1,ts/.08)*np.minimum(1,(D-ts)/.15);mix=np.column_stack((voice+left+score,voice+right+score))*fade[:,None]
 save(R/'assets/audio/NARRATION.wav',voice);save(R/'assets/audio/CALLER_AND_NARRATOR.wav',voice);save(R/'assets/audio/FX.wav',np.column_stack((left,right)));save(R/'assets/audio/SCORE.wav',score);save(R/'assets/audio/MIX_UNMASTERED.wav',mix)
 inp=R/'assets/audio/MIX_UNMASTERED.wav';out=R/'assets/audio/MIX_MASTER.wav';base='loudnorm=I=-16:TP=-2:LRA=8'
 p=subprocess.run(['ffmpeg','-v','info','-i',str(inp),'-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True);d=json.JSONDecoder().raw_decode(p.stderr[p.stderr.rfind('{'):])[0];f=base+f":measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true:print_format=json"
 p=subprocess.run(['ffmpeg','-v','info','-n','-i',str(inp),'-af',f,'-ar','48000','-ac','2',str(out)],capture_output=True,text=True,check=True);d=json.JSONDecoder().raw_decode(p.stderr[p.stderr.rfind('{'):])[0];(R/'reports/audio-master.json').write_text(json.dumps(d,indent=2));(R/'sound-cues.json').write_text(json.dumps(events,indent=2))
 def stamp(t):
  ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
 (R/'THE_PRICE_OF_SILENCE_EN.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text']}" for i,s in enumerate(segments))+'\n');print('86-second mix and actual phrase captions complete',flush=True)
if __name__=='__main__':main()
