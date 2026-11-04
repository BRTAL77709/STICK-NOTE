from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];g=json.loads((R/'FINAL_GATE.json').read_text());s=json.loads((R/'SCENE_REPAIR_REGISTER.json').read_text())
assert g['allow_final_export'] and g['audio_timing_integrated'],'Final export locked: '+g['reason']
assert all(x.get('technical_gate') and x.get('replacement') for x in s),'Some scenes lack validated replacements'
v=json.loads((R/'reports/source-validation.json').read_text());assert v['ok'] and v['source_frames']==2580
for p,sha in v['active_source_sha256'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==sha,'Source changed after validation: '+p
for item in v['HD_replacement_scenes']:assert hashlib.sha256((R/item['path']).read_bytes()).hexdigest()==item['sha256'],'HD input changed'
s=(R/'reports/hyperframes-check-final.json').read_text();check=json.loads(s[s.index(chr(123)):]);assert check['ok'],'HyperFrames check failed'
print('Final review export unlocked: all 18 validated HD inputs and current source verified. Artistic approval remains pending.')
