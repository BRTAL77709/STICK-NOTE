"""Verify existing scene exports without rendering or claiming artistic approval."""
from pathlib import Path
import json,hashlib,subprocess,struct,time,argparse
R=Path(__file__).resolve().parents[1]
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def inspect(p,expected=None):
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in d['streams'] if s['codec_type']=='video');a=next(s for s in d['streams'] if s['codec_type']=='audio');decode=subprocess.run(['ffmpeg','-v','error','-threads','1','-i',str(p),'-map','0:v','-map','0:a','-f','null','-'],capture_output=True)
 atoms=[]
 with p.open('rb') as f:
  while f.tell()<p.stat().st_size:
   offset=f.tell();b=f.read(8)
   if len(b)<8:break
   size,kind=struct.unpack('>I4s',b)
   if size==1:size=struct.unpack('>Q',f.read(8))[0]
   if size==0:size=p.stat().st_size-offset
   assert size>=8
   atoms.append(kind.decode('ascii','replace'));f.seek(offset+size)
 dur=float(d['format']['duration']);checks={'h264':v['codec_name']=='h264','resolution':(v['width'],v['height'])==(1080,1920),'fps':v['avg_frame_rate']=='30/1','yuv420p':v['pix_fmt']=='yuv420p','aac':a['codec_name']=='aac','complete_decode':decode.returncode==0 and not decode.stderr,'faststart':'moov' in atoms and atoms.index('moov')<atoms.index('mdat'),'duration':expected is None or abs(dur-expected)<.04,'frame_count':expected is None or int(v['nb_read_frames'])==round(expected*30)}
 return {'file':str(p.relative_to(R)),'sha256':digest(p),'bytes':p.stat().st_size,'duration':dur,'frames':int(v['nb_read_frames']),'checks':checks,'technical_pass':all(checks.values()),'decode_errors':decode.stderr.decode(),'artistic_approval':'PENDING USER REVIEW','verified_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
def main():
 p=argparse.ArgumentParser();p.add_argument('--watch',action='store_true');a=p.parse_args();out=R/'reports/FINAL_EXPORT_QA.json';results=json.loads(out.read_text()) if out.exists() else {}
 while True:
  for report in sorted((R/'reports').glob('M11_*_RENDER.json')):
   d=json.loads(report.read_text())
   if d['width']!=1080:continue
   path=R/d['file']
   if path.name in results and results[path.name]['sha256']==d['sha256']:continue
   row=inspect(path,d['duration']);assert row['sha256']==d['sha256'];results[path.name]=row;temp=out.with_suffix('.tmp');temp.write_text(json.dumps(results,indent=2));temp.replace(out);print(path.name,row['technical_pass'],flush=True)
  if not a.watch:break
  time.sleep(30)
if __name__=='__main__':main()
