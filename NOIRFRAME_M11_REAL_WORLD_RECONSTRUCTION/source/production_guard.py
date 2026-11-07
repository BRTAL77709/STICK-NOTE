"""Production gate: verified remote restore drill plus a backed-up source milestone."""
from pathlib import Path
import hashlib,json,subprocess,sys,fcntl
from bootstrap import ROOT as R

def sources():
 return {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'source').rglob('*')) if p.is_file() and p.suffix in ['.py','.cpp','.so'] and '__pycache__' not in p.parts}
def ensure(label='source change before production'):
 c=json.loads((R/'configuration/production.json').read_text());assert c.get('rendering_permitted') and json.loads((R/'reports/BACKUP_RESTORE_DRILL.json').read_text())['passed'],'Backup restore drill has not passed'
 with (R/'checkpoints/SOURCE_GATE.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);stamp=R/'reports/SOURCE_READY.json';now=sources()
  if stamp.exists() and json.loads(stamp.read_text())['source_sha256']==now:return
  subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'milestone','--label',label],check=True);commits=sorted((R/'checkpoints/commits').glob('*.json'),key=lambda p:p.stat().st_mtime);last=json.loads(commits[-1].read_text());tmp=stamp.with_suffix('.tmp');tmp.write_text(json.dumps({'source_sha256':now,'verified_source_commit':last['commit'],'branch':c['branch']},indent=2));tmp.replace(stamp)
