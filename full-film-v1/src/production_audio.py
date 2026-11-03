"""Original English script, local Flite voices, actual phrase timings and original soundscape."""
from pathlib import Path
import json,subprocess,wave,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
DURATIONS=[4,4,4,6,6,4,4,5,5,5,4,4,4,4,4,7,6,6]
TITLES=['2:17 AM','The driver','Something wrong','The crime','The trunk','They saw him','Panic','Pursuit','Escape','Safe?','House 17','Locked door','Inside','The window','Unknown call','The offer','The warning','The choice']
LINES=[
 ['At two seventeen,','the street should have been empty.'],
 ['I was only a few turns from home.'],
 ['Then I saw them.'],
 ['Two men.','Someone who could not stand.','A car with its engine running.'],
 ['They lifted him like luggage.','I should have kept driving.'],
 ['The trunk shut.','Then he looked straight at me.'],
 ['I hit the gas.'],
 ['The headlights behind me','turned when I did.'],
 ['Every turn. Every street.','Still there.'],
 ['One last turn.','The road behind me was empty.'],
 ['Home. Number seventeen.'],
 ['My key would not fit.','My hands would not stop shaking.'],
 ['I locked the door.','Then checked it again.'],
 ['Upstairs, I moved the curtain.','The black car was waiting.'],
 ['Then my phone rang.'],
 ['One million dollars.','All you have to do','is forget what you saw.'],
 ['Do not call the police.','We know which window you are standing at.'],
 ['A million dollars. Or the police.','What would you do?']]
def readwav(p):
 with wave.open(str(p),'rb') as w:
  assert w.getframerate()==48000;return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768

def main():
 sr=48000;total=sr*86;voice=np.zeros(total);segments=[];shots=[];start=0.
 for i,(dur,title,phrases) in enumerate(zip(DURATIONS,TITLES,LINES),1):
  shots.append({'scene':i,'start':start,'end':start+dur,'duration':dur,'title':title,'frames':dur*30})
  raw=[];speaker='caller' if i in (16,17) else 'protagonist';vname='awb' if speaker=='caller' else 'rms'
  for j,line in enumerate(phrases):
   txt=ROOT/'assets/voice-text'/f's{i:02d}_{j}.txt';txt.write_text(line)
   wav=ROOT/'assets/audio'/f's{i:02d}_{j}_raw.wav'
   if not wav.exists():subprocess.run(['ffmpeg','-v','error','-n','-f','lavfi','-i',f'flite=textfile={txt}:voice={vname}','-ar','48000','-ac','1',str(wav)],check=True)
   raw.append((line,wav,len(readwav(wav))/sr))
  budget=dur-.45;gap=.12;original=sum(d for _,_,d in raw)+gap*(len(raw)-1);speed=max(1.,original/budget)
  assert speed<1.7,(i,speed)
  clips=[]
  for j,(line,p,d) in enumerate(raw):
   out=ROOT/'assets/audio'/f's{i:02d}_{j}_{speaker}.wav'
   filters=[f'atempo={speed:.6f}','highpass=f=95','lowpass=f=7200']
   if speaker=='caller':filters+=['highpass=f=220','lowpass=f=3100']
   if not out.exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(p),'-af',','.join(filters),'-ar','48000','-ac','1',str(out)],check=True)
   samples=readwav(out);peak=max(.001,float(np.max(np.abs(samples))));samples*=.62/peak;clips.append((line,out,samples))
  voiced=sum(len(x[2])/sr for x in clips)+gap*(len(clips)-1);cursor=start+.20+max(0,(budget-voiced)*.30)
  for line,p,samples in clips:
   pos=round(cursor*sr);assert pos+len(samples)<=round((start+dur-.05)*sr)
   voice[pos:pos+len(samples)]+=samples;end=(pos+len(samples))/sr
   segments.append({'scene':i,'speaker':speaker,'voice':vname,'start':pos/sr,'end':end,'text':line,'asset':str(p.relative_to(ROOT)),'tempo':speed});cursor=end+gap
  print(f'VOICE scene {i:02d}: {voiced:.2f}s / {dur}s / tempo {speed:.3f}',flush=True);start+=dur
 assert start==86
 rng=np.random.default_rng(217);ts=np.arange(total)/sr;noise=rng.standard_normal(total)
 rain=(noise-np.roll(noise,1))*.012;wind=np.convolve(rng.standard_normal(total),np.ones(65)/65,mode='same')*.028
 # Original restrained tonal score; no sampled or copyrighted music.
 drone=.010*np.sin(2*np.pi*43*ts)+.006*np.sin(2*np.pi*64.5*ts)+.005*np.sin(2*np.pi*86.8*ts)
 tension=np.where((ts>28)&(ts<47),1.6,1.);ambient=(rain+wind+drone)*tension
 envelope=np.convolve(np.minimum(1,np.abs(voice)*9),np.ones(2401)/2401,mode='same');ambient*=1-.55*envelope
 events=[]
 def hit(t,name,gain=.08,pitch=80,length=.28):
  p=round(t*sr);n=min(int(length*sr),total-p);x=np.arange(n)/sr
  sound=gain*(np.sin(2*np.pi*(pitch*x-30*x*x))*np.exp(-x*17)+rng.standard_normal(n)*.4*np.exp(-x*35))
  ambient[p:p+n]+=sound;events.append({'time':t,'frame':round(t*30),'event':name})
 for t in [13.5,14.3,15.2,16.1,17.2,19.5,20.3,21.2,22.0,48.0,48.4,48.8,49.2,49.6,50.0,59.3,59.6,59.9,60.2]:hit(t,'wet step / contact',.055,78,.15)
 for t,n in [(18.62,'trunk opening latch'),(19.02,'trunk strut stop'),(23.43,'body settles inside'),(25.,'trunk CLOSED latch'),(51.6,'locked handle'),(52.4,'keys'),(54.0,'key in lock'),(54.6,'door opens'),(56.3,'door shuts'),(57.0,'deadbolt'),(57.8,'lock checked'),(65.5,'call answered'),(85.75,'final suspense accent')]:hit(t,n,.10,100 if 'latch' not in n else 900,.20)
 # Engines/chase move with narrative, not unrelated effects.
 active=((ts>4)&(ts<12))|((ts>28)&(ts<48));rpm=45+65*((ts>28)&(ts<42))+22*np.sin(ts*1.5)
 phase=2*np.pi*np.cumsum(rpm)/sr;engine=(np.sin(phase)+.25*np.sin(phase*2))*.022*active;ambient+=engine
 for a,z in [(32,37),(37,42),(42,46)]:
  env=np.maximum(0,np.sin(np.pi*np.clip((ts-a)/(z-a),0,1)))**2;ambient+=np.convolve(rng.standard_normal(total),np.ones(7)/7,mode='same')*.025*env
 for t in [63.5,64.05,64.60]:
  p=round(t*sr);n=int(.24*sr);x=np.arange(n)/sr;ambient[p:p+n]+=.032*np.sin(2*np.pi*140*x)*np.sin(np.pi*x/.24)**2;events.append({'time':t,'event':'phone vibration'})
 fade=np.minimum(1,ts/.08)*np.minimum(1,(86-ts)/.10);mix=(voice+ambient)*fade;stereo=np.column_stack((mix,np.roll(ambient,71)*fade+voice));peak=float(np.max(np.abs(stereo)));stereo*=min(1,.88/max(.001,peak))
 with wave.open(str(ROOT/'assets/audio/final_mix.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((stereo*32767).astype('<i2').tobytes())
 with wave.open(str(ROOT/'assets/audio/narration_stem.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((voice*32767).astype('<i2').tobytes())
 (ROOT/'narration-timing.json').write_text(json.dumps(segments,indent=2));(ROOT/'storyboard.json').write_text(json.dumps(shots,indent=2));(ROOT/'assets/audio/sound-events.json').write_text(json.dumps(events,indent=2))
 def srt_time(t):
  ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
 (ROOT/'THE_PRICE_OF_SILENCE_EN.srt').write_text('\n\n'.join(f'{n}\n{srt_time(s["start"])} --> {srt_time(s["end"])}\n{s["text"]}' for n,s in enumerate(segments,1))+'\n')
 (ROOT/'NARRATION_SCRIPT.md').write_text('# THE PRICE OF SILENCE — English narration\n\nLocal Flite RMS narrator; Flite AWB caller, with telephone filtering. Timings derive from each actual synthesized phrase.\n\n'+'\n\n'.join(f'**Scene {i:02d} — {TITLES[i-1]}** ({"caller" if i in (16,17) else "first-person narrator"})\n\n'+ ' '.join(LINES[i-1]) for i in range(1,19)))
 (ROOT/'FINAL_STORYBOARD.md').write_text('# Final storyboard — exactly 86 seconds / 2,580 frames\n\n| Scene | In | Out | Duration | Purpose |\n|---|---:|---:|---:|---|\n'+'\n'.join(f'| {s["scene"]:02d} | {s["start"]:.0f}s | {s["end"]:.0f}s | {s["duration"]}s | {s["title"]} |' for s in shots))
 print('AUDIO + SCRIPT + SRT complete',flush=True)
if __name__=='__main__':main()
