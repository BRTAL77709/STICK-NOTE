from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'));from scene_sources import evaluate;shots=json.loads((R/'storyboard.json').read_text());rows=json.loads((R/'SCENE_REPAIR_REGISTER.json').read_text());out=[]
for s in rows:
 if not s.get('replacement'):continue
 i=s['scene'];m=json.loads((R/'scenes'/f'scene_{i:02d}'/'final-cache.json').read_text());current=hashlib.sha256(''.join(evaluate(i,k/30) for k in range(shots[i-1]['frames'])).encode()).hexdigest();out.append({'scene':i,'matches_current_source':current==m['content_sha'],'current_content_sha':current,'rendered_content_sha':m['content_sha']})
(R/'reports/candidate-content-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
