"""Durable M11 checkpoints. Git commits plus verified immutable GitHub Release assets.
No rendering is allowed until a real source/native-project restore drill succeeds.
"""
from pathlib import Path
import json,hashlib,subprocess,base64,tarfile,io,time,argparse,threading,os,fcntl,contextlib
R=Path(__file__).resolve().parents[1];CFG=R/'configuration/production.json';REPO='repos/BRTAL77709/STICK-NOTE';LOCK=threading.RLock()
def sha(path):
 with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def api(path,data=None,method=None):
 cmd=['gh','api',REPO+'/'+path]
 if data is not None:cmd+=['--method',method or 'POST','--input','-']
 elif method:cmd+=['--method',method]
 for attempt in range(4):
  p=subprocess.run(cmd,input=json.dumps(data).encode() if data is not None else None,capture_output=True)
  if p.returncode==0:return json.loads(p.stdout) if p.stdout else {}
  err=p.stderr.decode()
  if not any(x in err for x in ['HTTP 502','HTTP 503','HTTP 504','HTTP 429']):raise RuntimeError(err)
  time.sleep(min(2**attempt,8))
 raise RuntimeError(err)
def config():return json.loads(CFG.read_text())
def ensure_branch():
 c=config();b=c['branch'];p=subprocess.run(['gh','api',REPO+'/git/ref/heads/'+b],capture_output=True)
 if p.returncode:
  assert '404' in p.stderr.decode(),p.stderr.decode();d=api('git/refs',{'ref':'refs/heads/'+b,'sha':c['base_commit']})
 else:d=json.loads(p.stdout)
 return d['object']['sha']
def ensure_release():
 c=config();tag=c['release_tag'];p=subprocess.run(['gh','api',REPO+'/releases/tags/'+tag],capture_output=True)
 if p.returncode:
  assert '404' in p.stderr.decode(),p.stderr.decode();d=api('releases',{'tag_name':tag,'target_commitish':c['branch'],'name':'NOIRFRAME M11 — verified production checkpoints','body':'Immutable source/native-project backups, frame batches, and validation artifacts for the M11 reconstruction. Not an approved film or a full-film assembly. Each asset is content-addressed and downloaded for SHA-256 verification before its receipt is committed.','draft':False,'prerelease':True})
 else:d=json.loads(p.stdout)
 c['release_id']=d['id'];c['release_url']=d['html_url'];CFG.write_text(json.dumps(c,indent=2));return d

def verify_download(url,expected,expected_bytes):
 # Stream remote data through the hash; never trust an upload response alone.
 p=subprocess.Popen(['curl','-q','-fLsS','--retry','2','--max-time','180',url],stdout=subprocess.PIPE,stderr=subprocess.PIPE);h=hashlib.sha256();size=0
 while True:
  b=p.stdout.read(1024*1024)
  if not b:break
  h.update(b);size+=len(b)
 stderr=p.stderr.read();assert p.wait()==0,stderr.decode();assert size==expected_bytes,(size,expected_bytes);assert h.hexdigest()==expected,(h.hexdigest(),expected);return True

def store_asset(path,kind,label):
 """Verified normal-Git chunk backend; Release upload is unavailable (HTTP 401).
 Every chunk is reachable from a pushed commit before verification/receipt.
 Chunking is transport only and never changes or re-encodes the production file.
 """
 path=Path(path);digest=sha(path);c=config();head=ensure_branch();oldtree=api('git/commits/'+head)['tree']['sha'];old=api('git/trees/'+oldtree+'?recursive=1');assert not old.get('truncated');known={x['sha'] for x in old['tree'] if x['type']=='blob'};prefix=R.name+'/checkpoint_objects/'+digest+'/';parts=[];rows=[]
 with path.open('rb') as f:
  i=0
  while True:
   data=f.read(8*1024*1024)
   if not data:break
   name=f'part-{i:05d}.bin';g=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   if g not in known:
    got=api('git/blobs',{'encoding':'base64','content':base64.b64encode(data).decode()});assert got['sha']==g;known.add(g)
   rows.append({'path':prefix+name,'mode':'100644','type':'blob','sha':g});parts.append({'name':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_sha':g});i+=1
 manifest={'filename':path.name,'kind':kind,'label':label,'sha256':digest,'bytes':path.stat().st_size,'parts':parts,'format':'Concatenate parts in numeric order; no compression/quality transformation'};raw=json.dumps(manifest,indent=2).encode();g=api('git/blobs',{'encoding':'base64','content':base64.b64encode(raw).decode()})['sha'];rows.append({'path':prefix+'manifest.json','mode':'100644','type':'blob','sha':g})
 tree=api('git/trees',{'base_tree':oldtree,'tree':rows})['sha'];after=api('git/trees/'+tree+'?recursive=1');assert not after.get('truncated');lookup={x['path']:x for x in after['tree']}
 for x in old['tree']:
  if x['type']=='blob':assert lookup[x['path']]['sha']==x['sha'],x['path']
 for row in rows:assert lookup[row['path']]['sha']==row['sha']
 assert api('git/ref/heads/'+c['branch'])['object']['sha']==head
 commit=api('git/commits',{'message':'M11 durable object: '+kind+' / '+label+' / '+digest[:16],'tree':tree,'parents':[head]})['sha'];api('git/refs/heads/'+c['branch'],{'sha':commit,'force':False},'PATCH');assert api('git/ref/heads/'+c['branch'])['object']['sha']==commit
 base='https://raw.githubusercontent.com/BRTAL77709/STICK-NOTE/'+commit+'/'+prefix
 whole=hashlib.sha256();total=0
 for part in parts:
  data=subprocess.check_output(['curl','-q','-fLsS','--retry','2','--max-time','180',base+part['name']]);assert len(data)==part['bytes'];assert hashlib.sha256(data).hexdigest()==part['sha256'];whole.update(data);total+=len(data)
 assert total==manifest['bytes'] and whole.hexdigest()==digest
 receipt={'kind':kind,'label':label,'local_path':str(path.relative_to(R)),'asset_name':path.name,'url':base+'manifest.json','parts_base_url':base,'sha256':digest,'bytes':total,'backend':'GitHub committed immutable chunks','commit':commit,'download_SHA256_verified':True,'verified_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 out=R/'checkpoints/receipts';out.mkdir(exist_ok=True);(out/(kind+'-'+label+'-'+digest[:20]+'.json')).write_text(json.dumps(receipt,indent=2));return receipt

def pack(paths,label):
 out=R/'checkpoints'/('pack-'+label+'-'+str(time.time_ns())+'.tar.gz');rows=[]
 for p in sorted(set(Path(p) for p in paths)):
  assert p.is_file() and not p.is_symlink();assert p.resolve().is_relative_to(R.resolve());rows.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)})
 with tarfile.open(out,'x:gz') as t:
  for row in rows:t.add(R/row['path'],arcname=row['path'],recursive=False)
  data=json.dumps({'label':label,'files':rows},indent=2).encode();info=tarfile.TarInfo('CHECKPOINT_FILE_MANIFEST.json');info.size=len(data);t.addfile(info,io.BytesIO(data))
 with tarfile.open(out,'r:gz') as t:
  for row in rows:assert hashlib.sha256(t.extractfile(row['path']).read()).hexdigest()==row['sha256']
 return out,rows

def git_files():
 files=[]
 for folder in ['source','configuration','assets','blender','reports','checkpoints/receipts']:
  for p in (R/folder).rglob('*'):
   if not p.is_file() or p.is_symlink() or '__pycache__' in p.parts or p.suffix in ['.log','.blend1']:continue
   if p.stat().st_size<=40*1024*1024:files.append(p)
 for p in R.iterdir():
  if p.is_file() and p.suffix in ['.md','.json']:files.append(p)
 for p in (R/'baseline').glob('*.json'):files.append(p)
 return sorted(set(files))

def commit_milestone(label):
 c=config();head=ensure_branch();oldtree=api('git/commits/'+head)['tree']['sha'];old=api('git/trees/'+oldtree+'?recursive=1');assert not old.get('truncated');known={x['sha'] for x in old['tree'] if x['type']=='blob'};rows=[]
 for p in git_files():
  b=p.read_bytes();g=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();rows.append({'path':R.name+'/'+str(p.relative_to(R)),'mode':'100644','type':'blob','sha':g})
  if g not in known:
   d=api('git/blobs',{'encoding':'base64','content':base64.b64encode(b).decode()});assert d['sha']==g;known.add(g)
 tree=api('git/trees',{'base_tree':oldtree,'tree':rows})['sha'];after=api('git/trees/'+tree+'?recursive=1');assert not after.get('truncated');lookup={x['path']:x for x in after['tree']}
 # Every earlier project entry remains identical; M11 modifications have versioned Git history.
 for x in old['tree']:
  if not x['path'].startswith(R.name+'/') and x['path']!=R.name:assert lookup[x['path']]['sha']==x['sha'] and lookup[x['path']]['mode']==x['mode'],x['path']
 for row in rows:assert lookup[row['path']]['sha']==row['sha'],row['path']
 assert api('git/ref/heads/'+c['branch'])['object']['sha']==head
 if tree==oldtree:return {'commit':head,'unchanged':True}
 commit=api('git/commits',{'message':'M11 milestone: '+label+' — persistent checkpoints; preserve V10/M10; no full-film assembly','tree':tree,'parents':[head]})['sha'];api('git/refs/heads/'+c['branch'],{'sha':commit,'force':False},'PATCH');assert api('git/ref/heads/'+c['branch'])['object']['sha']==commit
 result={'label':label,'commit':commit,'tree':tree,'parent':head,'files_verified_in_remote_tree':len(rows),'previous_project_entries_preserved':True,'branch':c['branch'],'url':'https://github.com/BRTAL77709/STICK-NOTE/commit/'+commit};folder=R/'checkpoints/commits';folder.mkdir(exist_ok=True);(folder/(commit+'.json')).write_text(json.dumps(result,indent=2));return result

def restore_drill(receipt):
 manifest=json.loads(subprocess.check_output(['curl','-q','-fLsS','--retry','2','--max-time','180',receipt['url']]))
 restored=bytearray()
 for part in manifest['parts']:
  data=subprocess.check_output(['curl','-q','-fLsS','--retry','2','--max-time','180',receipt['parts_base_url']+part['name']]);assert hashlib.sha256(data).hexdigest()==part['sha256'];restored.extend(data)
 assert hashlib.sha256(restored).hexdigest()==receipt['sha256']
 with tarfile.open(fileobj=io.BytesIO(restored),mode='r:gz') as t:
  rows=json.load(t.extractfile('CHECKPOINT_FILE_MANIFEST.json'))['files']
  for row in rows:assert hashlib.sha256(t.extractfile(row['path']).read()).hexdigest()==row['sha256']
 result={'object':receipt['asset_name'],'sha256':receipt['sha256'],'members_restored_and_verified':len(rows),'passed':True,'restore_source':'Remote committed GitHub chunks downloaded again and reassembled, not local archive'};(R/'reports/BACKUP_RESTORE_DRILL.json').write_text(json.dumps(result,indent=2));return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['init','milestone','asset']);p.add_argument('--label',default='checkpoint');p.add_argument('--path');a=p.parse_args()
 with LOCK, (R/'checkpoints/BACKUP.lock').open('a') as lockfile:
  fcntl.flock(lockfile,fcntl.LOCK_EX)
  if a.command=='init':
   ensure_branch();paths=[CFG,R/'README.md',R/'source/checkpoint_store.py',R/'blender/BASELINE_M04.blend',R/'M11_MASTER_SPECIFICATION.md'];archive,rows=pack(paths,'backup-restore-drill');receipt=store_asset(archive,'source','backup-restore-drill');print(json.dumps(restore_drill(receipt),indent=2));c=config();c['rendering_permitted']=True;CFG.write_text(json.dumps(c,indent=2));print(json.dumps(commit_milestone('backup and remote restore drill passed'),indent=2))
  elif a.command=='asset':print(json.dumps(store_asset(R/a.path,'output',a.label),indent=2))
  else:
   archive,rows=pack(git_files(),a.label);receipt=store_asset(archive,'source',a.label);print(json.dumps(commit_milestone(a.label),indent=2))
