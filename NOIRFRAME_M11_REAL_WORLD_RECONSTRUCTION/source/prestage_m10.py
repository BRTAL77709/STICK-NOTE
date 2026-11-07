"""Stage immutable file blobs only. Publish the branch only after final media/QA is complete."""
from pathlib import Path
import json,hashlib,subprocess,base64,concurrent.futures
R=Path(__file__).resolve().parents[1];repo='repos/BRTAL77709/STICK-NOTE'
def api(p,data=None):
 cmd=['gh','api',repo+'/'+p]+(['--method','POST','--input','-'] if data is not None else [])
 for _ in range(3):
  q=subprocess.run(cmd,input=json.dumps(data).encode() if data is not None else None,capture_output=True)
  if q.returncode==0:return json.loads(q.stdout)
  if not any(x in q.stderr for x in [b'HTTP 502',b'HTTP 503',b'HTTP 504']):raise RuntimeError(q.stderr.decode())
 raise RuntimeError(q.stderr.decode())
head=api('git/ref/heads/work')['object']['sha'];tree=api('git/commits/'+head)['tree']['sha'];known={x['sha'] for x in api('git/trees/'+tree+'?recursive=1')['tree'] if x['type']=='blob'}
models={'BASELINE_M04.blend','STAIRS_M09.blend','STAIRS_M10D.blend','DRIVING_COCKPIT_M10.blend','DRIVING_COCKPIT_EDITABLE_M10.blend','DRIVER_CHASE_M10.blend','DRIVER_CHASE_M10C.blend','DRIVER_CHASE_EDITABLE_M10.blend','KEY_LOCK_M10B.blend','DOOR_ENTRY_M10G.blend','CAR_EXIT_RUNNING_M10I.blend','WINDOW_CURTAIN_M10B.blend','ROAD_BUILDINGS_WORLD_M10_RELEASE.blend','CAR_CHASE_WORLD_M10_RELEASE.blend'}
files=[p for p in (R/'source').rglob('*') if p.is_file() and p.suffix in ['.py','.cpp'] and '__pycache__' not in p.parts]+[R/'blender'/m for m in sorted(models)];cache=R/'reports/github-upload-cache.json';uploaded=json.loads(cache.read_text()) if cache.exists() else {}
def job(p):
 b=p.read_bytes();h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 if h not in known and h not in uploaded:assert api('git/blobs',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha']==h
 return h
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for i,h in enumerate(ex.map(job,files),1):uploaded[h]=True;cache.write_text(json.dumps(uploaded));print('staged',i,'/',len(files),flush=True)
