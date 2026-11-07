"""Cold restore from a verified checkpoint manifest; never overwrites different existing files."""
from pathlib import Path
import argparse,json,hashlib,subprocess,tarfile,io

def download(url):return subprocess.check_output(['curl','-q','-fLsS','--retry','2','--max-time','180',url])
def restore(url,destination,extract=True):
 manifest=json.loads(download(url));base=url.rsplit('/',1)[0]+'/';raw=bytearray()
 for part in manifest['parts']:
  b=download(base+part['name']);assert len(b)==part['bytes'] and hashlib.sha256(b).hexdigest()==part['sha256'];raw.extend(b)
 assert len(raw)==manifest['bytes'] and hashlib.sha256(raw).hexdigest()==manifest['sha256'];dest=Path(destination).resolve();dest.mkdir(parents=True,exist_ok=True);restored=[]
 if extract and manifest['filename'].endswith('.tar.gz'):
  with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as t:
   rows=json.load(t.extractfile('CHECKPOINT_FILE_MANIFEST.json'))['files']
   for row in rows:
    p=(dest/row['path']).resolve();assert p.is_relative_to(dest);b=t.extractfile(row['path']).read();assert hashlib.sha256(b).hexdigest()==row['sha256']
    if p.exists():assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],'Refusing to overwrite a different file: '+str(p)
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    restored.append(str(p))
 else:
  p=dest/Path(manifest['filename']).name
  if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['sha256']
  else:p.write_bytes(raw)
  restored.append(str(p))
 return {'manifest_url':url,'sha256':manifest['sha256'],'files_restored_and_verified':restored,'passed':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--manifest-url',required=True);p.add_argument('--destination',required=True);p.add_argument('--no-extract',action='store_true');a=p.parse_args();print(json.dumps(restore(a.manifest_url,a.destination,not a.no_extract),indent=2))
