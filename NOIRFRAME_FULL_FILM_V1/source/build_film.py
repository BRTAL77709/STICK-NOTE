"""Best-achievable complete86s assembly. Existing masters are read-only inputs."""
from pathlib import Path
import json,subprocess,hashlib,sys
import numpy as np,soundfile as sf
R=Path(__file__).resolve().parents[1];P=R.parent;B=P/'full-film-real-motion-rebuild';N=P/'NOIRFRAME_PRODUCTION_RESET';fps=30;sr=48000;total=86*sr
assert not any((R/x).exists() for x in ['audio/EDIT_MIX_RAW.wav','audio/FULL_FILM_MIX.flac','renders/PICTURE_86s.mp4','renders/PREFIX_0_47.mp4','renders/MIDDLE_47_81_5.mp4','renders/TAIL_81_5_86.mp4']),'Preserve outputs: rebuild into a new empty directory using source/rebuild.py'
plan=json.loads((R/'EDIT_DECISION_LIST.json').read_text());master=(R/plan['baseline']).resolve();bv=(R/plan['native_B']).resolve();cv=(R/plan['native_C']).resolve();closing=(R/plan['closing_source']).resolve()
def run(cmd):subprocess.run(cmd,check=True)
def read(p,stereo=False):
 x,s=sf.read(p,dtype='float32');assert s==sr,(p,s)
 if stereo and x.ndim==1:x=np.column_stack([x,x])
 return x
A=R/'inputs';narr=read(A/'BASELINE_NARRATOR.flac');caller=read(A/'BASELINE_CALLER.flac');fx=read(A/'BASELINE_FX.flac',True);score=read(A/'BASELINE_SCORE.flac');voice=narr+caller;assert len(voice)==total
cues=[]
for k,start,dur in [('B',49.2,7.8),('C',61.4,8.0)]:
 lo=round(start*sr);hi=round((start+dur)*sr);newvoice=read(R/f'inputs/{k}_voice.wav');newfx=read(R/f'inputs/{k}_foley.wav');assert len(newvoice)==hi-lo
 if k=='B':newvoice[round(6.60*sr):]=0 # Avoid redundant "Inside" immediately before original locking narration.
 voice[lo:hi]=newvoice
 if k=='B':voice[lo:round(49.55*sr)]+=narr[lo:round(49.55*sr)] # Complete "Number seventeen", never cut mid-word.
 # Blend only the effects beds at the edit; voice timing remains sample-accurate.
 target=np.column_stack([newfx,newfx]);fade=round(.025*sr);w=np.ones(len(target),dtype='float32');w[:fade]=np.linspace(0,1,fade);w[-fade:]=np.linspace(1,0,fade);fx[lo:hi]=fx[lo:hi]*(1-w[:,None])+target*w[:,None]
 for q in json.loads((R/'inputs/native_contact-cues.json').read_text()):
  if q['shot']==k:cues.append({**q,'film_time':start+q['time']})
voice[round(60.94*sr):round(61.4*sr)]=0 # Remove checked-again phrase in full; original continuation is replaced by C.
# Keep the existing continuous original score; no new commercial music.
raw=np.column_stack([voice,voice])+fx+np.column_stack([score,score]);sf.write(R/'audio/EDIT_MIX_RAW.wav',raw,sr,subtype='PCM_16')
basefilter='loudnorm=I=-16:TP=-2:LRA=11';q=subprocess.run(['ffmpeg','-v','info','-i',str(R/'audio/EDIT_MIX_RAW.wav'),'-af',basefilter+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True);meter=json.JSONDecoder().raw_decode(q.stderr[q.stderr.rfind('{'):])[0];norm=basefilter+f":measured_I={meter['input_i']}:measured_TP={meter['input_tp']}:measured_LRA={meter['input_lra']}:measured_thresh={meter['input_thresh']}:offset={meter['target_offset']}:linear=true"
run(['ffmpeg','-v','error','-n','-i',str(R/'audio/EDIT_MIX_RAW.wav'),'-af',norm,'-ar',str(sr),'-ac','2','-c:a','flac',str(R/'audio/FULL_FILM_MIX.flac')]);(R/'reports/audio-premaster-measurement.json').write_text(json.dumps(meter,indent=2));(R/'audio/CONTACT_CUES.json').write_text(json.dumps(cues,indent=2));print('AUDIO_COMPLETE',flush=True)
original=json.loads((R/'inputs/baseline_narration-timing.json').read_text());rows=[q for q in original if q['scene'] not in [12,14,15] and not q['text'].startswith('Then checked')]
for q in json.loads((R/'inputs/native_narration-tests.json').read_text()):
 if q['shot'] not in ['B','C'] or (q['shot']=='B' and q['text']=='Inside.'):continue
 offset=49.2 if q['shot']=='B' else 61.4;rows.append({**q,'start':q['start']+offset,'end':q['end']+offset,'speaker':'narrator','asset':'native proof voice stem'})
rows.sort(key=lambda x:x['start']);(R/'audio/NARRATION_TIMING.json').write_text(json.dumps(rows,indent=2))
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(R/'THE_PRICE_OF_SILENCE_EN.srt').write_text('\n\n'.join(f"{j+1}\n{stamp(q['start'])} --> {stamp(q['end'])}\n{q['text']}" for j,q in enumerate(rows))+'\n')
def astamp(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02}:{n//100%60:02}.{n%100:02}'
header='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\nStyle: Main,DejaVu Sans,44,&H00F1EDE4,&H00F1EDE4,&HCC071521,&HCC071521,-1,0,0,0,100,100,0,0,3,10,0,8,80,80,95,1\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n'''
for name,start,end in [('B',49.2,57),('C',61.4,69.4),('CLOSING',57,61.4)]:
 events=[]
 for q in rows:
  lo=max(start,q['start']);hi=min(end,q['end'])
  if hi>lo:events.append(f"Dialogue: 0,{astamp(lo-start)},{astamp(hi-start)},Main,,0,0,0,,{q['text']}")
 (R/'inputs'/f'{name}.ass').write_text(header+'\n'.join(events)+'\n')
# Prefix/tail copy encoded packets: V10 has no generation loss.
prefix=R/'renders/PREFIX_0_47.mp4';tail=R/'renders/TAIL_81_5_86.mp4';patch=R/'renders/MIDDLE_47_81_5.mp4'
run(['ffmpeg','-v','error','-n','-i',str(master),'-map','0:v:0','-frames:v','1410','-an','-c:v','copy',str(prefix)])
run(['ffmpeg','-v','error','-n','-ss','81.5','-i',str(master),'-map','0:v:0','-frames:v','135','-an','-c:v','copy',str(tail)])
fil=f"[0:v]trim=start_frame=0:end_frame=66,setpts=N/(30*TB)[a];[1:v]trim=start_frame=0:end_frame=234,setpts=N/(30*TB),subtitles='{R}/inputs/B.ass'[b];[3:v]trim=start_frame=0:end_frame=132,setpts=N/(30*TB),subtitles='{R}/inputs/CLOSING.ass'[c];[2:v]trim=start_frame=0:end_frame=240,setpts=N/(30*TB),subtitles='{R}/inputs/C.ass'[d];[0:v]trim=start_frame=672:end_frame=1035,setpts=N/(30*TB)[e];[a][b][c][d][e]concat=n=5:v=1:a=0,setsar=1[v]"
run(['ffmpeg','-v','warning','-n','-threads','2','-ss','47','-t','34.5','-i',str(master),'-i',str(bv),'-i',str(cv),'-i',str(closing),'-filter_complex_threads','1','-filter_complex',fil,'-map','[v]','-an','-frames:v','1035','-r','30','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-profile:v','high','-level:v','4.0','-x264-params','bframes=0:ref=3:deblock=1,1:aq-mode=3:aq-strength=0.8','-threads','2','-video_track_timescale','15360',str(patch)]);print('MIDDLE_COMPLETE',flush=True)
concat=R/'inputs/concat.txt';concat.write_text(f"file '{prefix}'\nduration 47\nfile '{patch}'\nduration 34.5\nfile '{tail}'\nduration 4.5\n");picture=R/'renders/PICTURE_86s.mp4';run(['ffmpeg','-v','warning','-n','-f','concat','-safe','0','-i',str(concat),'-map','0:v:0','-c:v','copy','-movflags','+faststart',str(picture)])
final=R/'renders/THE_PRICE_OF_SILENCE_NOIRFRAME_FULL_FILM_V1_86s.mp4';run(['ffmpeg','-v','warning','-n','-i',str(picture),'-i',str(R/'audio/FULL_FILM_MIX.flac'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t','86','-movflags','+faststart',str(final)]);print('FULL_FILM_COMPLETE',final,flush=True)
inputs=[master,bv,cv,closing]+[A/f'BASELINE_{x}.flac' for x in ['NARRATOR','CALLER','FX','SCORE']]+[R/f'inputs/{k}_voice.wav' for k in 'BC']+[R/f'inputs/{k}_foley.wav' for k in 'BC']
(R/'reports/INPUT_MANIFEST.json').write_text(json.dumps([{'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs],indent=2));(R/'PROGRESS.md').write_text((R/'PROGRESS.md').read_text()+'\nFull86-second MP4 rendered. Next: actual encoded validation, exact V10 frame comparison and full playback.\n')
