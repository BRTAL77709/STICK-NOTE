"""Review the framing-only preview before rendering its separately versioned final."""
from pathlib import Path
import json,subprocess,sys,time
R=Path(__file__).resolve().parents[1]
p=R/'reports/M11_STAIRS_M11R04_PREVIEW_360_RENDER.json'
while not p.exists():time.sleep(5)
m={'STAIRS':{'duration':17.,'preview':'renders/M11_STAIRS_M11R04_PREVIEW_360.mp4','final':'renders/M11_STAIRS_M11R04_FINAL.mp4'}}
(R/'STAIRS_R04_REVIEW.json').write_text(json.dumps(m,indent=2))
for cmd in [[sys.executable,str(R/'source/review_playback.py'),'--manifest','STAIRS_R04_REVIEW.json','--tag','STAIRS_R04_REVIEW'],[sys.executable,str(R/'source/render_stairs_m11r04.py'),'--shot','STAIRS','--tag','M11R04','--native-tag','M11R03','--final']]:
 q=subprocess.run(cmd);assert q.returncode==0,cmd
