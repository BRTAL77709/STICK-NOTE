from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1];H=R/'hyperframes';report=R/'reports/hyperframes-check-final.json';s=report.read_text();check=json.loads(s[s.index('{'):]);assert check['ok'];files={H/'index.html',H/'hyperframes.json',H/'index.motion.json',*H.glob('compositions/*.html')}
for f in list(files):
 for name in re.findall(r'''(?:src=["']|url\(['"]?)(assets/[^"'\s)]+)''',f.read_text()):files.add(H/name)
assert all(f.exists() for f in files)
(R/'reports/hyperframes-source-stamp.json').write_text(json.dumps({'ok':True,'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'files':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(files)},'craft_findings':check.get('craft',{}).get('findings',[])},indent=2));print('Stamped',len(files),'checked composition inputs')
