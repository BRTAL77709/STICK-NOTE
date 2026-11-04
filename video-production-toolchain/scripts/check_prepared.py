"""Fail if a prepared rig/state/audio bundle is stale; seal only after preparation/QC."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[1];inputs=['shared/timeline.json','shared/narration.wav','shared/narration-script.txt']+[str(p.relative_to(R)) for p in (R/'animation').glob('*.py')];outputs=['shared/frame-states.json','remotion/public/frames.json.gz','hyperframes/assets/shared-state.js','shared/demo-audio.wav','subtitles/script-reference.json'];sha=lambda p:hashlib.sha256((R/p).read_bytes()).hexdigest();path=R/'PREPARED_INPUTS.json'
if '--seal' in sys.argv:path.write_text(json.dumps({'inputs':{p:sha(p) for p in inputs},'outputs':{p:sha(p) for p in outputs}},indent=2));print('Prepared bundle sealed.')
else:
 d=json.loads(path.read_text())
 for table in ['inputs','outputs']:
  for p,h in d[table].items():assert sha(p)==h,'Prepared state stale: '+p+'; regenerate inputs in a fresh story workspace and review before sealing.'
 print('Prepared rig/clock/audio bundle matches current sources.')
