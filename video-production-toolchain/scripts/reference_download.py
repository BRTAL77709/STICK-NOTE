"""Explicit authorized reference import; no downloads run during setup."""
from pathlib import Path
import argparse,subprocess,json,sys
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--url');p.add_argument('--rights-note');p.add_argument('--style-analysis-only',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();cmd=[sys.executable,'-m','yt_dlp']
if a.check:subprocess.run(cmd+['--version'],check=True);sys.exit(0)
if not a.url or not a.rights_note or not a.style_analysis_only:p.error('Provide --url, --rights-note and --style-analysis-only for a reference you are authorized to access/use.')
refs=R/'references';refs.mkdir(exist_ok=True);job={'url':a.url,'rights_note':a.rights_note,'purpose':'style analysis only; no footage/music reuse authorization implied'};(refs/'authorization.jsonl').open('a').write(json.dumps(job)+'\n');subprocess.run(cmd+['--no-playlist','--no-overwrites','--restrict-filenames','--write-info-json','--download-archive',str(refs/'archive.txt'),'--paths',str(refs),'-o','%(id)s.%(ext)s','--format','bv*[height<=1080]+ba/b[height<=1080]','--merge-output-format','mp4','--js-runtimes','node',a.url],check=True)
