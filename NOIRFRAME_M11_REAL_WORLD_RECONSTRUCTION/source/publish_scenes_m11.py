"""Publish only completed, decode-validated standalone scene files; never assembles a film."""
from pathlib import Path
import json,time,hashlib,subprocess,sys,os
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'CURRENT_SHOTS.json').read_text());D['STAIRS']['final']='renders/M11_STAIRS_M11R04_FINAL.mp4'
out=R/'DELIVERY_MANIFEST.json';rows=json.loads(out.read_text()) if out.exists() else {}
while len(rows)<len(D):
 qa_path=R/'reports/FINAL_EXPORT_QA.json';qa=json.loads(qa_path.read_text()) if qa_path.exists() else {}
 for shot,d in D.items():
  if shot in rows:continue
  p=R/d['final'];q=qa.get(p.name)
  if not q or not q['technical_pass']:continue
  receipts=[json.loads(x.read_text()) for x in (R/'checkpoints/receipts').glob('*.json')]
  if not any(x['sha256']==q['sha256'] and x.get('download_SHA256_verified') and x.get('direct_download_url') for x in receipts):continue
  dest=R/'renders'/f'M11_{shot}_FINAL.mp4'
  if dest.exists():assert hashlib.sha256(dest.read_bytes()).hexdigest()==q['sha256'],'Refuse overwrite: '+str(dest)
  else:os.link(p,dest)
  label=dest.stem
  subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'asset','--path',str(dest.relative_to(R)),'--label',label],check=True)
  matches=[json.loads(x.read_text()) for x in (R/'checkpoints/receipts').glob('*.json')];receipt=next(x for x in matches if x['label']==label and x['sha256']==q['sha256'] and x.get('direct_download_url'))
  rows[shot]={'duration':d['duration'],'versioned_source_export':d['final'],'file':str(dest.relative_to(R)),'sha256':q['sha256'],'bytes':dest.stat().st_size,'download_url':receipt['direct_download_url'],'remote_manifest':receipt['url'],'remote_download_verified':True,'decode_validated':True,'artistic_approval':'PENDING USER REVIEW'}
  temp=out.with_suffix('.tmp');temp.write_text(json.dumps(rows,indent=2));temp.replace(out);print('PUBLISHED_VERIFIED',shot,flush=True)
  lines=['# M11 standalone scene review downloads','','New reconstruction from verified M10; previous missing M11 was not recovered. No full-film assembly. Artistic approval is pending.','','Every linked MP4 was downloaded from its pinned Git commit and SHA-256 verified, and fully decoded locally.','']
  for s,x in rows.items():lines.append(f'- [{s} ({x["duration"]} s)]({x["download_url"]})')
  lines+=['','See `reports/RECONSTRUCTION_TECHNICAL_REPORT.md` for measured results, source mappings and unresolved limitations.','The expanded clips overlap in story coverage. They do not constitute an 86-second edit.']
  (R/'REVIEW_DOWNLOADS.md').write_text('\n'.join(lines)+'\n')
 time.sleep(20)
print('ALL_STANDALONE_SCENES_PUBLISHED',len(rows),flush=True)
