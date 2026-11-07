"""Actual Chromium normal/half-speed playback of each published canonical scene."""
from pathlib import Path
import json,time,subprocess,sys
R=Path(__file__).resolve().parents[1];done=set()
while len(done)<14:
 p=R/'DELIVERY_MANIFEST.json';rows=json.loads(p.read_text()) if p.exists() else {}
 for shot,d in rows.items():
  if shot in done:continue
  report=R/f'reports/VERIFIED_FINAL_{shot}_final-playback.json'
  if report.exists():
   q=json.loads(report.read_text())[shot]
   if all(x['ended'] and x['corruptedFrames']==0 and x['sha256']==d['sha256'] for x in q):done.add(shot);continue
  m=R/f'configuration/REVIEW_FINAL_{shot}.json';m.write_text(json.dumps({shot:{'duration':d['duration'],'final':d['file']}},indent=2));q=subprocess.run([sys.executable,str(R/'source/review_playback.py'),'--manifest',str(m.relative_to(R)),'--stage','final','--tag','VERIFIED_FINAL_'+shot]);assert q.returncode==0,shot;done.add(shot)
 time.sleep(15)
print('ALL_FINAL_SCENES_PLAYED_NORMAL_AND_HALF_SPEED',flush=True)
