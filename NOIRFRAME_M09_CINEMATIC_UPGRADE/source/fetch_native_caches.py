"""Free public download of this delivery's exact native caches. No API key."""
from pathlib import Path
import argparse,json,hashlib,urllib.request
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--revision',default='work');a=p.parse_args()
for row in json.loads((R/'CACHES_MANIFEST.json').read_text()):
 out=R/row['path']
 if out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()==row['sha256']:
  print('VERIFIED',row['path']);continue
 assert not out.exists(),f'Refusing to overwrite existing file: {out}'
 url=f'https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/{a.revision}/NOIRFRAME_M09_CINEMATIC_UPGRADE/{row["path"]}'
 with urllib.request.urlopen(url,timeout=120) as f:content=f.read()
 assert hashlib.sha256(content).hexdigest()==row['sha256'],row['path']
 out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(content);print('DOWNLOADED_AND_VERIFIED',row['path'])
