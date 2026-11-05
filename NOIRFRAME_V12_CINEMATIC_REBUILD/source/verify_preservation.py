from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];base=R.parent;rows=json.loads((R/'reports/PRESERVATION_BEFORE.json').read_text());changed=[];missing=[]
for rel,sha in rows.items():
 p=base/rel
 if not p.exists():missing.append(rel)
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=sha:changed.append(rel)
out={'files_checked':len(rows),'changed':changed,'missing':missing,'previous_versions_preserved':not changed and not missing};(R/'reports/PRESERVATION_AFTER.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));assert not changed and not missing
