"""Contact-derived zero-cost mix. Existing speech performances, revised placement and new synchronized foley."""
from pathlib import Path
import sys,json,math,wave,subprocess,argparse,hashlib
import numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'engine/animation'))
from motion_state import state,pursuit_distance
SR=48000;D=86;N=SR*D

def smooth(t,a,b):
 u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
def average(x,n):
 p=n//2;y=np.pad(x,(p,p));cs=np.r_[0.,np.cumsum(y,dtype=np.float64)];return (cs[n:]-cs[:-n])/n

def save(p,x):
 assert not p.exists(),p
 a=np.asarray(x);ch=a.shape[1] if a.ndim==2 else 1
 with wave.open(str(p),'wb') as f:f.setnchannels(ch);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(a,-.99,.99)*32767).astype('<i2').tobytes())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='assets/audio-rebuild-v1');args=ap.parse_args();out=R/args.out;assert not out.exists(),'Preserve earlier mix; choose a NEW output directory';out.mkdir(parents=True)
 ts=np.arange(N)/SR;roles={'narrator':np.zeros(N),'caller':np.zeros(N)};segments=json.loads((R/'narration-timing.json').read_text());timing=[]
 for seg in segments:
  with wave.open(str(R/seg['asset'])) as f:duration=f.getnframes()/f.getframerate()
  assert abs(duration-(seg['end']-seg['start']))<.001
  filt='highpass=f=75,lowpass=f=10000,acompressor=threshold=0.17:ratio=2.2:attack=5:release=100'
  if seg['speaker']=='caller':filt+=',highpass=f=280,lowpass=f=3200'
  b=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/seg['asset']),'-af',filt,'-ar',str(SR),'-ac','1','-f','f32le','pipe:1']);x=np.frombuffer(b,'<f4').astype(float);x*=.48/max(.01,float(abs(x).max()));fade=min(240,len(x)//4);x[:fade]*=np.linspace(0,1,fade);x[-fade:]*=np.linspace(1,0,fade);a=round(seg['start']*SR);assert a+len(x)<=N;roles[seg['speaker']][a:a+len(x)]+=x;timing.append({'asset':seg['asset'],'actual_start':a/SR,'actual_end':(a+len(x))/SR,'samples':len(x),'speech_performance':'retained stock Kokoro; listening unverified'})
 voice=roles['narrator']+roles['caller'];ctl=np.arange(0,D+1/120,1/120);ss=[state(float(t)) for t in ctl];interp=lambda key:np.interp(ts,ctl,[s[key] for s in ss]);vel=interp('speed_mps');rp=interp('rpm');phase=np.cumsum(rp/60*2)/SR*math.tau
 engine=(.016*np.sin(phase)+.008*np.sin(2*phase)+.004*np.sin(3*phase))*(.35+np.clip(vel/18,0,1))*(1-smooth(ts,48.7,49.15))
 rng=np.random.default_rng(71726);n1=rng.standard_normal(N);n2=rng.standard_normal(N);outside=np.ones(N)
 for a,b in [(4,12),(28,32),(35,40),(44.8,47)]:outside[(ts>=a)&(ts<b)]=.35
 inside=ts>=55.3;outside[inside]=.12+.88*(1-smooth(ts[inside],55.35,55.95))
 rain1=(n1-np.roll(n1,1))*.0035*outside;rain2=(n2-np.roll(n2,1))*.0035*outside
 road1=average(n1,17)*(.005+.0011*vel)*(ts<49);road2=average(n2,17)*(.005+.0011*vel)*(ts<49);wind=average(n1,121)*.015
 bs=[state(float(t),True) for t in ctl];brp=np.interp(ts,ctl,[s['rpm'] for s in bs]);bp=np.cumsum(brp/60*2)/SR*math.tau;gap=np.interp(ts,ctl,[pursuit_distance(float(t)) for t in ctl]);chase=((ts>=32)&(ts<42)).astype(float);park=((ts>=59)&(ts<80)).astype(float)*.10;pursuer=(.005*np.sin(bp)+.002*np.sin(bp*2))*np.clip(20/np.maximum(6,gap),0,2)*(chase+park)
 phone_air=n1*.0007*((ts>=65.8)&(ts<80));left=engine+pursuer+rain1+road1+wind+phone_air;right=engine*.95+pursuer*.9+rain2+road2+wind+phone_air
 del n1,n2,rain1,rain2,road1,road2,wind,phone_air
 events=json.loads((R/'CONTACT_SOUND_CUES.json').read_text())
 for e in events:
  a=round(e['time']*SR);dur=e['duration'];nn=min(round(dur*SR),N-a);tt=np.arange(nn)/SR;kind=e['kind']
  if kind=='ring':y=(np.sin(2*math.pi*440*tt)+.5*np.sin(2*math.pi*480*tt))*.5*np.minimum(1,tt/.02)*np.minimum(1,(dur-tt)/.03)
  elif kind=='cloth':y=rng.standard_normal(nn)*np.exp(-tt*13)*.35
  elif kind=='thud':
   pitch=75 if e.get('material')=='wet' else 105;y=(np.sin(2*math.pi*pitch*tt)+.23*rng.standard_normal(nn))*np.exp(-tt*24)
   if e.get('material')=='wet':y+=rng.standard_normal(nn)*.25*np.exp(-tt*35)
  elif kind=='key':y=(np.sin(2*math.pi*1800*tt)+.6*np.sin(2*math.pi*2750*tt))*np.exp(-tt*35)
  else:y=(np.sin(2*math.pi*270*tt)+.2*rng.standard_normal(nn))*np.exp(-tt*32)
  left[a:a+nn]+=y*e['gain'];right[a:a+nn]+=y*e['gain']*.94
 buzz_gate=smooth(ts,63.1,63.18)*(1-smooth(ts,64.05,64.15));buzz=.009*np.sin(2*math.pi*220*ts)*(.7+.3*np.sin(66*ts))*buzz_gate;left+=buzz;right+=buzz*.94
 score=.007*np.sin(2*math.pi*64.5*ts)+.004*np.sin(2*math.pi*96.7*ts);pulse=(.5+.5*np.sin(2*math.pi*np.where(ts<28,1.1,1.65)*ts))**12;score+=.006*np.sin(2*math.pi*129*ts)*pulse
 quiet=np.ones(N);quiet[(ts>24.7)&(ts<25.35)]=.15;quiet[(ts>62.55)&(ts<63.1)]=.10;score*=quiet
 duck=1-.72*average(np.minimum(1,abs(voice)*7),2401);left*=.75+.25*duck;right*=.75+.25*duck;score*=duck;fade=np.minimum(1,ts/.08)*np.minimum(1,(D-ts)/.15)
 mix=np.column_stack((voice+left+score,voice+right+score))*fade[:,None]
 save(out/'NARRATOR.wav',roles['narrator']);save(out/'CALLER.wav',roles['caller']);save(out/'FX.wav',np.column_stack((left,right)));save(out/'SCORE.wav',score);save(out/'MIX_UNMASTERED.wav',mix)
 norm='loudnorm=I=-16:TP=-2:LRA=8';inp=out/'MIX_UNMASTERED.wav';p=subprocess.run(['ffmpeg','-v','info','-i',str(inp),'-af',norm+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True);meter=json.JSONDecoder().raw_decode(p.stderr[p.stderr.rfind('{'):])[0];f=norm+f":measured_I={meter['input_i']}:measured_TP={meter['input_tp']}:measured_LRA={meter['input_lra']}:measured_thresh={meter['input_thresh']}:offset={meter['target_offset']}:linear=true:print_format=json"
 p=subprocess.run(['ffmpeg','-v','info','-n','-i',str(inp),'-af',f,'-ar','48000','-ac','2',str(out/'MIX_MASTER.wav')],capture_output=True,text=True,check=True);normalized=json.JSONDecoder().raw_decode(p.stderr[p.stderr.rfind('{'):])[0]
 for n in ['NARRATOR','CALLER','FX','SCORE','MIX_MASTER']:subprocess.run(['ffmpeg','-v','error','-n','-i',str(out/f'{n}.wav'),'-c:a','flac','-compression_level','8',str(out/f'{n}.flac')],check=True)
 report={'output_directory':args.out,'sample_rate':SR,'duration':D,'contact_cues':len(events),'cue_source_sha256':hashlib.sha256((R/'CONTACT_SOUND_CUES.json').read_bytes()).hexdigest(),'voice_timing':timing,'normalization_report':normalized,'speech':'Existing stock performances retained, phrase placement revised; no new paid generation.','listening':'UNVERIFIED: no auditory input; signal measurements do not certify professional audio quality.','buzz':'Same 63.1–64.15 envelope and 66 rad/s motion modulation as the supported device.'};(R/'reports/rebuild-audio.json').write_text(json.dumps(report,indent=2));(R/'AUDIO_OUTPUT.json').write_text(json.dumps({'directory':args.out,'mix':args.out+'/MIX_MASTER.flac','cue_source':'CONTACT_SOUND_CUES.json','listening_verified':False},indent=2));print('86s synchronized mix/stems encoded; listening review remains unverified')
if __name__=='__main__':main()
