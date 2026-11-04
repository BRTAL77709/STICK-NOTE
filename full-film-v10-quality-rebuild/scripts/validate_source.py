"""Validate current rendered-source hashes, contact reports, state exports and preservation."""
from pathlib import Path
import sys,json,hashlib,subprocess,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));from motion_state import state,vehicleState
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
shots=json.loads((R/'storyboard.json').read_text());assert len(shots)==18 and sum(s['frames'] for s in shots)==2580
assert shots[0]['start']==0 and shots[-1]['end']==86
assert all(a['end']==b['start'] for a,b in zip(shots,shots[1:]))
content=json.loads((R/'reports/candidate-content-check.json').read_text());assert len(content)==18 and all(x['matches_current_source'] for x in content)
rows=[]
for s in shots:
 m=json.loads((R/f'scenes/scene_{s["scene"]:02d}/final-cache.json').read_text());p=R/m['path'];v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_streams','-of','json',str(p)]))['streams'][0]
 assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],int(v['nb_read_frames']))==(1080,1920,'30/1','h264',s['frames'])
 rows.append({'scene':s['scene'],'path':m['path'],'sha256':h(p),'frames':s['frames']})
b=json.loads((R/'reports/baseline-preservation.json').read_text());base=Path(b['root']);matched=0
for rel,sha in b['sha256'].items():assert h(base/rel)==sha,rel;matched+=1
vp=json.loads((R/'reports/v10-picture-preservation.json').read_text());assert vp['all_480_svg_frames_match']
for n in (4,5,6):
 m=json.loads((R/f'scenes/scene_{n:02d}/final-cache.json').read_text());assert h(R/m['path'])==h(base/m['path'])
frames=json.loads((R/'hyperframes/assets/vehicle-state.js').read_text().split('=',1)[1].rstrip(';'));export_error=0.;velocity_error=0.
for f in range(2581):
 t=f/30;s=vehicleState(t)
 for k,v in s.items():
  if isinstance(v,(int,float)):export_error=max(export_error,abs(v-frames[f][k]))
 for black in (False,True):
  p=state(t,black);assert abs(p['wheel_rad']*.32-p['distance_m'])<1e-8
 if 0<t<48:
  a=state(t-.0001);b1=state(t+.0001);velocity_error=max(velocity_error,abs(math.hypot(b1['x']-a['x'],b1['z']-a['z'])/.0002-state(t)['speed_mps']))
assert export_error<1e-8 and velocity_error<.01
mix=json.loads((R/'reports/rebuild-audio.json').read_text());assert mix['cue_source_sha256']==h(R/'CONTACT_SOUND_CUES.json') and mix['contact_cues']==96 and len(mix['voice_timing'])==30
p=R/json.loads((R/'AUDIO_OUTPUT.json').read_text())['mix'];a=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))['streams'][0];assert a['sample_rate']=='48000' and a['channels']==2 and float(a['duration'])==86
segments=json.loads((R/'narration-timing.json').read_text());assert all(0<=s['start']<s['end']<=86 for s in segments) and all(a['end']<=b['start'] for a,b in zip(segments,segments[1:]))
report={'ok':True,'source_frames':2580,'HD_replacement_scenes':rows,'V10_picture_frames_preserved':480,'baseline_files_unchanged':matched,'vehicle_samples':2581,'export_max_error':export_error,'velocity_position_max_error_mps':velocity_error,'contact_cues':96,'narration_phrases':30,'word_alignment':'measured phrase boundaries only','voice_quality':'retained performances; listening unverified','artistic_approval':'pending user review'}
report['active_source_sha256']={str(p.relative_to(R)):h(p) for pattern in ['engine/**/*.py','scenes/**/*.py','hyperframes/**/*.html','hyperframes/assets/vehicle-state.js','storyboard.json','narration-timing.json','CONTACT_SOUND_CUES.json','AUDIO_OUTPUT.json'] for p in R.glob(pattern) if p.is_file()}
(R/'reports/source-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='HD_replacement_scenes'},indent=2))
