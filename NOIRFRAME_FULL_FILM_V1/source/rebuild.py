"""Reproduce the complete edit in a new directory, preserving the delivered project."""
from pathlib import Path
import argparse,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();src=Path(__file__).resolve().parents[1];dst=a.out.resolve();assert not dst.exists(),'Choose a new output directory';dst.mkdir(parents=True)
shutil.copytree(src/'source',dst/'source',ignore=shutil.ignore_patterns('__pycache__'));shutil.copytree(src/'inputs',dst/'inputs',ignore=shutil.ignore_patterns('concat.txt','*.ass'));shutil.copyfile(src/'EDIT_DECISION_LIST.json',dst/'EDIT_DECISION_LIST.json')
for name in ['audio','renders','reports','reviews','blender']:(dst/name).mkdir()
(dst/'PROGRESS.md').write_text('Fresh self-contained reproduction; delivered originals untouched.\n')
for script,extra in [('build_film.py',[]),('finish_film.py',[]),('validate_film.py',['--skip-preservation'])]:subprocess.run([sys.executable,str(dst/'source'/script),*extra],check=True)
print('REBUILD_COMPLETED',dst/'renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4',flush=True)
