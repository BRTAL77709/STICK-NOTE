from pathlib import Path
import sys,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));import physical_proofs as p
out=[];stale=[]
for k,d in p.DURATIONS.items():
 sha=hashlib.sha256(''.join(p.svg(k,f/30) for f in range(round(d*30))).encode()).hexdigest();entry={'proof':k,'source_svg_sha256':sha,'stages':{}}
 for stage in ('preview','final'):
  m=json.loads((R/f'proofs/{k}/{stage}.json').read_text());same=m['source_svg_sha256']==sha
  if not same:stale.append((k,stage))
  review=json.loads((R/f'proofs/{k}/{stage}_PLAYBACK.json').read_text());assert all(x['ended'] and x['corrupted']==0 for x in review);assert [x['rate'] for x in review]==[1,.5];assert all(x['path']==m['path'] for x in review)
  entry['stages'][stage]={'source_matches':same,'path':m['path'],'normal_and_slow_completed':True}
 out.append(entry)
source_files={str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (R/'engine/animation').glob('*.py')}
report={'source_files_sha256':source_files,'technical_ready':not stale,'proofs':out,'stale':stale,'artistic_approval':'pending user review'};(R/'reports/proof-integration-gate.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));assert not stale,stale
