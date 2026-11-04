"""Validate the current proof/scene/audio/composition sources and preserved inputs."""
from pathlib import Path
import sys,json,hashlib,subprocess,wave,re
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'));from scene_sources import evaluate
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
proof=json.loads((R/'reports/proof-integration-gate.json').read_text());assert proof['technical_ready']
for n,h in proof['source_files_sha256'].items():assert sha(R/n)==h,'Proof source changed: '+n
assert json.loads((R/'reports/physical-proof-validation.json').read_text())['D']['fixed_planted_toe_max_displacement_m']<1e-7
assert json.loads((R/'reports/master-motion-validation.json').read_text())['ok']
shots=json.loads((R/'storyboard.json').read_text());register=json.loads((R/'SCENE_REPAIR_REGISTER.json').read_text());assert len(shots)==18 and sum(s['frames'] for s in shots)==2580 and shots[-1]['end']==86;assert all(a['end']==b['start'] for a,b in zip(shots,shots[1:]));rows=[]
base=R.parent/'full-film-v10-quality-rebuild'
for s in shots:
 n=s['scene'];h=hashlib.sha256()
 for f in range(s['frames']):
  svg=evaluate(n,f/30);assert '<svg' in svg and '</svg>' in svg and not re.search(r'(?<![a-z])(?:nan|inf)(?![a-z])',svg.lower());h.update(svg.encode())
 content=h.hexdigest()
 for stage in ('previews','final'):
  meta=json.loads((R/f'scenes/scene_{n:02d}/{stage}-cache.json').read_text());assert meta['content_sha']==content,('stale rendered source',n,stage)
  if n not in (4,5,6):
   tag=f'scene_{n:02d}_{stage}_{meta["fingerprint"]}';play=json.loads((R/f'reports/{tag}_playback.json').read_text());assert play['ended'] and play['rate']==1 and play['corruptedFrames']==0 and play['path']==meta['path'] and play['frames']==s['frames']
   if stage=='final':
    slow=json.loads((R/f'reports/{tag}_slow_playback.json').read_text());assert slow['ended'] and slow['rate']==.5 and slow['corruptedFrames']==0 and slow['path']==meta['path']
 meta=json.loads((R/f'scenes/scene_{n:02d}/final-cache.json').read_text());v=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_streams','-of','json',str(R/meta['path'])]))['streams'][0];assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'],int(v['nb_read_frames']))==(1080,1920,'h264','30/1',s['frames'])
 assert register[n-1]['technical_gate'] and register[n-1]['replacement']==meta['path']
 if n in (4,5,6):
  old=json.loads((base/f'scenes/scene_{n:02d}/final-cache.json').read_text());assert old['content_sha']==content and sha(base/old['path'])==sha(R/meta['path'])
 rows.append({'scene':n,'path':meta['path'],'frames':s['frames'],'content_sha':content,'video_sha256':sha(R/meta['path'])});print('Validated scene',n,flush=True)
preserve=json.loads((R/'reports/rejected-rebuild-preservation.json').read_text())
for n,h in preserve['sha256'].items():assert sha(base/n)==h,'Baseline changed: '+n
mix=json.loads((R/'reports/rebuild-audio.json').read_text());assert mix['cue_source_sha256']==sha(R/'CONTACT_SOUND_CUES.json');assert mix['contact_cues']==len(json.loads((R/'CONTACT_SOUND_CUES.json').read_text()))
segments=json.loads((R/'narration-timing.json').read_text());assert len(segments)==30 and all(a['end']<=b['start'] for a,b in zip(segments,segments[1:])) and segments[-1]['end']<=86
for x in segments:
 with wave.open(str(R/x['asset'])) as w:duration=w.getnframes()/w.getframerate()
 assert abs(duration-(x['end']-x['start']))<.001
stamp=json.loads((R/'reports/hyperframes-source-stamp.json').read_text());assert stamp['ok'] and stamp['report_sha256']==sha(R/'reports/hyperframes-check-final.json')
for n,h in stamp['files'].items():assert sha(R/n)==h,'Composition changed: '+n
for row in rows:
 source=R/row['path'];copy=R/'hyperframes/assets/scenes'/source.name;assert sha(copy)==row['video_sha256']
active={str(p.relative_to(R)):sha(p) for pattern in ('engine/**/*.py','scenes/**/*.py','storyboard.json','narration-timing.json','CONTACT_SOUND_CUES.json','AUDIO_OUTPUT.json','HOUSE17_PLAN.json') for p in R.glob(pattern) if p.is_file()}
report={'ok':True,'source_frames':2580,'HD_scenes':rows,'baseline_files_unchanged':len(preserve['sha256']),'V10_frames_preserved':480,'contact_cues':mix['contact_cues'],'narration_phrases':30,'active_sources_sha256':active,'stair_visibility':'Three upper risers; lower flight elided.','artistic_approval':'pending user review','listening_verified':False};(R/'reports/source-validation.json').write_text(json.dumps(report,indent=2));print('All current source, media input, contact, audio and composition gates passed')
