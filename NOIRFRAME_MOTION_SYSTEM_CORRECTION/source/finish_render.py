from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1]
for p in [R/'source/validate.py',R/'source/export_review.py']:
 cmd=['python',str(p)]+(['--tag','M01','--width','1080'] if p.name=='validate.py' else [])
 subprocess.run(cmd,check=True)
