"""Create a fresh version folder; never render over delivered files."""
from pathlib import Path
import argparse,shutil,subprocess,json
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--width',type=int,default=1080);p.add_argument('--shots',nargs='+',default=['STAIRS','HOUSE','BEDROOM','DRIVING']);a=p.parse_args();out=Path(a.output).resolve();assert not out.exists(),'Output directory must be NEW';out.mkdir(parents=True);shutil.copytree(R/'source',out/'source',ignore=shutil.ignore_patterns('__pycache__','versions'))
for n in ['previews','assets','reviews','reports']: (out/n).mkdir()
for k in a.shots:subprocess.run(['python',str(out/'source/render.py'),'--shot',k,'--width',str(a.width),'--tag','REBUILD'],check=True)
subprocess.run(['python',str(out/'source/qa.py')],check=True)
