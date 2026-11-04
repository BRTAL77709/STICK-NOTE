"""Append this review package to work using Git data API; preserve existing tree."""
from pathlib import Path
import subprocess,json,hashlib,base64,concurrent.futures,re,sys
R=Path(__file__).resolve().parents[1];repo='repos/BRTAL77709/STICK-NOTE';prefix=R.name+'/'
def api(p,data=None):
 c=['gh','api',repo+'/'+p]
 if data is not None:c+=['--method','POST','--input','-']
 for attempt in range(3):
  q=subprocess.run(c,input=json.dumps(data).encode() if data is not None else None,capture_output=True)
  if q.returncode==0:return json.loads(q.stdout)
  if not any(code in q.stderr for code in [b'HTTP 502',b'HTTP 503',b'HTTP 504']):raise RuntimeError(q.stderr.decode())
  print('Transient GitHub gateway error; retry',attempt+1,flush=True)
 raise RuntimeError(q.stderr.decode())
if '--stage-only' not in sys.argv:
 for label,rate in [('REAL_MOTION_NORMAL',1),('REAL_MOTION_SLOW',.5)]:
  p=json.loads((R/f'reports/{label}_playback.json').read_text());assert p['ended'] and p['rate']==rate and p['corruptedFrames']==0 and p['duration']==86
 fidelity=json.loads((R/'reports/encoded-subject-fidelity.json').read_text());assert fidelity['ok'];assert fidelity['file_sha256']==hashlib.sha256((R/'renders/final/THE_PRICE_OF_SILENCE_REAL_MOTION_REBUILD_86s.mp4').read_bytes()).hexdigest()
 assert (R/'reports/real-motion-final-decode.txt').read_text().startswith('Full FFmpeg decode exit=0')
head=api('git/ref/heads/work')['object']['sha'];expected='202eff93a966b08f6d70baea86e39cf325db35da';assert head==expected,('branch changed',head)
base=api('git/commits/'+head)['tree']['sha'];old=api('git/trees/'+base+'?recursive=1');assert not old.get('truncated');assert not any(x['path'].startswith(prefix) for x in old['tree']);known={x['sha'] for x in old['tree'] if x['type']=='blob'}
files=set()
def add(p):
 if p.is_file() and '__pycache__' not in p.parts and p.name!='DELIVERY_MANIFEST.json':files.add(p)
for p in R.iterdir():
 if p.suffix in ['.md','.json','.srt','.sh']:add(p)
for folder in ['engine','scripts','scenes']:
 for p in (R/folder).rglob('*'):
  if p.suffix in ['.py','.json']:add(p)
for folder in ['assets','reports']:
 for p in (R/folder).rglob('*'):
  rel=str(p.relative_to(R))
  if not p.is_file() or '__pycache__' in p.parts:continue
  if folder=='assets' and ('audio-real-motion' in rel and 'audio-real-motion-v3/' not in rel):continue
  if folder=='assets' and p.suffix in ['.wav'] and 'audio-real-motion' in rel:continue
  if folder=='reports' and (p.suffix not in ['.json','.txt'] or 'github' in p.name):continue
  add(p)
for p in (R/'proofs').glob('*/*'):
 if p.suffix!='.mp4':add(p)
for k in 'ABCDE':
 for stage in ['preview','final']:add(R/json.loads((R/f'proofs/{k}/{stage}.json').read_text())['path'])
for n in range(1,19):
 for stage in ['previews','final']:add(R/json.loads((R/f'scenes/scene_{n:02d}/{stage}-cache.json').read_text())['path'])
tags=[]
for n in range(1,19):
 for stage in ['previews','final']:
  m=json.loads((R/f'scenes/scene_{n:02d}/{stage}-cache.json').read_text());tags.append(f'scene_{n:02d}_{stage}_{m["fingerprint"]}')
for p in (R/'reviews').rglob('*'):
 if p.suffix in ['.jpg','.png'] and ('composite-final' in p.parts or p.name in ['CITY_DEPTH_BEFORE_AFTER.jpg','ENCODED_SUBJECT_COMPARISON.jpg','ENCODED_DOOR_ACTION.jpg','ENCODED_STAIRS_CURTAIN.jpg','ENCODED_DRIVING_ACTION.jpg','fidelity-frame-53.5.jpg'] or any(p.name.startswith(t+'_') for t in tags)):add(p)
for p in (R/'renders/previews').glob('*PRESENTED.jpg'):add(p)
add(R/'renders/final/THE_PRICE_OF_SILENCE_REAL_MOTION_REBUILD_86s.mp4')
for p in R.glob('*CONTACT*jpg'):add(p)
for p in [R/'CONTACT_SHEET_FULL.jpg',R/'ACTION_CONTACT_STRIPS.jpg']:add(p)
stamp=json.loads((R/'reports/hyperframes-source-stamp.json').read_text())
for p in stamp['files']:add(R/p)
for p in ['hyperframes/index.html','hyperframes/hyperframes.json']:add(R/p)
rows=[]
for p in sorted(files):
 b=p.read_bytes();rows.append({'path':str(p.relative_to(R)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
manifest=R/'DELIVERY_MANIFEST.json';manifest.write_text(json.dumps({'files':rows,'base_commit':head},indent=2));b=manifest.read_bytes();rows.append({'path':manifest.name,'git_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
cache=R/'reports/github-upload-cache.json';uploaded=json.loads(cache.read_text()) if cache.exists() else {}
def upload(row):
 sha=row['git_sha']
 if sha not in known and sha not in uploaded:
  out=api('git/blobs',{'encoding':'base64','content':base64.b64encode((R/row['path']).read_bytes()).decode()});assert out['sha']==sha
 return sha
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for i,sha in enumerate(ex.map(upload,rows)):
  uploaded[sha]=True;cache.write_text(json.dumps(uploaded));print('blob',i+1,'/',len(rows),flush=True)
if '--stage-only' in sys.argv:
 print('Blobs staged only; no branch mutation.',flush=True);sys.exit(0)
nested={}
for row in rows:
 parts=row['path'].split('/');owner=nested
 for part in parts[:-1]:owner=owner.setdefault(part,{})
 owner[parts[-1]]=row['git_sha']
def directory(node,path=''):
 entries=[]
 for name,item in sorted(node.items()):
  if isinstance(item,dict):entries.append({'path':name,'mode':'040000','type':'tree','sha':directory(item,path+name+'/')})
  else:entries.append({'path':name,'mode':'100644','type':'blob','sha':item})
 out=api('git/trees',{'tree':entries})['sha'];print('tree',path or '.',out,flush=True);return out
subtree=directory(nested)
tree=api('git/trees',{'base_tree':base,'tree':[{'path':R.name,'mode':'040000','type':'tree','sha':subtree}]})['sha']
new=api('git/trees/'+tree+'?recursive=1');assert not new.get('truncated');lookup={x['path']:x for x in new['tree']}
for x in old['tree']:assert lookup[x['path']]['sha']==x['sha'] and lookup[x['path']]['mode']==x['mode']
assert api('git/ref/heads/work')['object']['sha']==head
commit=api('git/commits',{'message':'Add real motion rebuild, five physical proofs and verified review film','tree':tree,'parents':[head]})['sha']
p=subprocess.run(['gh','api',repo+'/git/refs/heads/work','--method','PATCH','--input','-'],input=json.dumps({'sha':commit,'force':False}).encode(),capture_output=True,check=True)
assert api('git/ref/heads/work')['object']['sha']==commit
(R/'reports/github-publication.json').write_text(json.dumps({'commit':commit,'tree':tree,'files':len(rows),'prior_entries_preserved':len(old['tree'])},indent=2));print('PUBLISHED',commit,flush=True)
