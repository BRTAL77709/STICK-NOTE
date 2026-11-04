"""Verify anonymous byte-for-byte downloads of published review deliverables."""
from pathlib import Path
import json,subprocess,hashlib,concurrent.futures,urllib.parse
R=Path(__file__).resolve().parents[1];pub=json.loads((R/'reports/github-publication.json').read_text());commit=pub['commit'];paths=['renders/final/THE_PRICE_OF_SILENCE_REAL_MOTION_REBUILD_86s.mp4','CONTACT_SHEET_18_SCENES.jpg','ANIMATION_FAILURE_AUDIT.md','TECHNICAL_VALIDATION.md','engine/animation/physical_proofs.py','engine/animation/film_performance.py','reports/source-validation.json']
for k in 'ABCDE':
 paths.append(json.loads((R/f'proofs/{k}/final.json').read_text())['path'])
 paths.extend(f'proofs/{k}/{n}' for n in ['final_CONTACT_SHEET.jpg','MOTION_TRAJECTORY.csv','JOINT_TRANSFORMS.json','CONTACT_EVENTS.json','README.md'])
def verify(p):
 url=f'https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/{commit}/{R.name}/'+urllib.parse.quote(p,safe='/');q=subprocess.run(['curl','-fLsS','--retry','2','--max-time','180',url],capture_output=True);assert q.returncode==0,(p,q.stderr.decode());b=(R/p).read_bytes();assert q.stdout==b,('download differs',p);print('VERIFIED',p,flush=True);return {'path':p,'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'http_status':200,'anonymous':True,'matches_local':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:rows=list(e.map(verify,paths))
(R/'reports/download-verification.json').write_text(json.dumps({'commit':commit,'verified':rows},indent=2));print('ALL DOWNLOADS VERIFIED',len(rows),flush=True)
