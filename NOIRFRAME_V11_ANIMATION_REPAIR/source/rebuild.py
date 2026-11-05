"""Fresh local source-only build. No old video, pose images, model weights or network required."""
from pathlib import Path
import argparse,shutil,subprocess,sys,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--version',default='REBUILD');p.add_argument('--shots',nargs='*',default=['HOUSE','STAIRS','WINDOW']);a=p.parse_args();src=Path(__file__).resolve().parents[1];dst=a.out.resolve();assert not dst.exists(),'Preserve existing versions: choose a new output directory';dst.mkdir(parents=True)
for directory in ['source','assets','previews','reviews','reports']:(dst/directory).mkdir()
for file in (src/'source').glob('*.py'):shutil.copyfile(file,dst/'source'/file.name)
for shot in a.shots:subprocess.run([sys.executable,str(dst/'source/render.py'),'--shot',shot,'--width','1080','--version',a.version],check=True)
subprocess.run([sys.executable,str(dst/'source/qa.py')],check=True)
rows={}
for k in a.shots:
 f=dst/f'previews/{k}_V11_{a.version}_1080.mp4';h=hashlib.sha256(f.read_bytes()).hexdigest();original=src/f'previews/{k}_V11_R07_1080.mp4';rows[k]={'sha256':h,'matches_original':original.exists() and hashlib.sha256(original.read_bytes()).hexdigest()==h}
(dst/'reports/SOURCE_REBUILD.json').write_text(json.dumps(rows,indent=2));print('FRESH_REBUILD_COMPLETE',json.dumps(rows),flush=True)
