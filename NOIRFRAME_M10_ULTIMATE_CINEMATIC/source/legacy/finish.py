from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1]
for script,args in [('qa.py',['--tag','C02']),('repair_diagnostic_projection.py',[]),('export_review.py',[])]:subprocess.run(['python',str(R/'source'/script),*args],check=True)
