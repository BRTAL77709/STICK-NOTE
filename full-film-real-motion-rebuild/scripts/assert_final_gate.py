from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();g=json.loads((R/'FINAL_GATE.json').read_text());assert g['allow_final_export'] and g['audio_timing_integrated'],g['reason'];v=json.loads((R/'reports/source-validation.json').read_text());assert v['ok'] and v['source_frames']==2580
for p,sha in v['active_sources_sha256'].items():assert h(R/p)==sha,'Source changed after validation: '+p
for s in v['HD_scenes']:assert h(R/s['path'])==s['video_sha256'],'Changed HD input'
stamp=json.loads((R/'reports/hyperframes-source-stamp.json').read_text());assert stamp['report_sha256']==h(R/'reports/hyperframes-check-final.json')
for p,sha in stamp['files'].items():assert h(R/p)==sha,'Composition changed after check: '+p
print('All 18 current inputs, five proof gates, source and composition verified. Review export only; no artistic approval.')
