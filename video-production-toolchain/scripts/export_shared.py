"""One integer-frame clock -> true per-frame rig geometry, state, and HF data."""
from pathlib import Path
import sys,json,hashlib,subprocess,wave,gzip,re
R=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'animation'))
import physical_proofs as p
T=json.loads((R/'shared/timeline.json').read_text());FPS=T['fps'];frames=[];states=[]
# Compile layer metadata from the master frame clock; no independent HUD timeline.
hud_duration=(T['hud']['endFrame']-T['hud']['startFrame'])/FPS
html=R/'hyperframes/index.html';markup=html.read_text()
for ident in ['main','hud']:
 markup=re.sub(r'(id="'+ident+r'"[^>]*data-duration=")[^"]+',lambda m:m.group(1)+str(hud_duration),markup)
html.write_text(markup)
(R/'hyperframes/hyperframes.json').write_text(json.dumps({'name':'noirframe-vehicle-state-overlay',**T['hud']['region'],'fps':FPS,'duration':hud_duration},indent=2))
for frame in range(T['frames']):
 shot=next(s for s in T['shots'] if s['startFrame']<=frame<s['startFrame']+s['frames']);local=(frame-shot['startFrame'])/FPS
 state=p.accelerator(local) if shot['kind']=='A' else p.vehicle_state(local)
 frames.append(p.svg(shot['kind'],local));states.append({'frame':frame,'time':frame/FPS,'shot':shot['id'],'localTime':local,'state':state})
serialize=lambda v:json.dumps(v,separators=(',',':'),default=lambda x:x.tolist())
(R/'remotion/public/frames.json.gz').write_bytes(gzip.compress(serialize(frames).encode(),mtime=0));(R/'shared/frame-states.json').write_text(serialize(states));(R/'hyperframes/assets/shared-state.js').write_text('window.SHARED_TIMELINE='+serialize(T)+';window.FRAME_STATES='+serialize(states)+';')
with wave.open(str(R/'shared/narration.wav')) as w:dur=w.getnframes()/w.getframerate()
start=T['speechStartFrame']/FPS
(R/'subtitles/script-reference.json').write_text(json.dumps([{'start':start,'end':start+dur,'text':(R/'shared/narration-script.txt').read_text().strip(),'origin':'source script + measured WAV duration; NOT Whisper transcription'}],indent=2))
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
(R/'subtitles/script-reference.srt').write_text(f'1\n{stamp(start)} --> {stamp(start+dur)}\nI hit the gas.\n')
# Real narration at exact shared-clock offset; no purchased speech/audio calls.
subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/'shared/narration.wav'),'-af',f'adelay={round(start*1000)}:all=1,apad,atrim=duration={T["duration"]}', '-ar','48000','-ac','2',str(R/'shared/demo-audio.wav')],check=True)
report={'frames':len(frames),'fps':FPS,'duration':T['duration'],'SVG_sequence_sha256':hashlib.sha256(''.join(frames).encode()).hexdigest(),'pedal_toe_contact_max_error':max(__import__('math').dist(x['state']['toe'],x['state']['pedal_contact']) for x in states if x['shot']=='pedal' and x['state']['contact']),'vehicle_distance_m':p.vehicle_state(4)['distance_m'],'wheel_rule':'wheel_rad=distance_m/0.32','speech_start':start,'speech_end':start+dur,'source':'copied approved physical_proofs.py + articulated/driver/vehicle/world modules','Remotion_role':'Selects per-frame SVG DOM from evaluated hierarchical rigs; not a held image with transforms.'}
(R/'reports/shared-clock.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

subprocess.run([sys.executable,str(R/'scripts/check_prepared.py'),'--seal'],check=True)
