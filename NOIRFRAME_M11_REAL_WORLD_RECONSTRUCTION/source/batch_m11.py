from bootstrap import ROOT as R
import sys,json,subprocess,concurrent.futures,time,hashlib
import actions
SHOTS=[s for s in actions.DURATIONS if s!='DRIVER_CHASE']
FINAL='--final' in sys.argv

def job(shot):
 rev=json.loads((R/'configuration/render_revision.json').read_text())['revision'];stage='FINAL' if FINAL else 'PREVIEW_360';name=f'M11_{shot}_{rev}_{stage}';report=R/'reports'/(name+'_RENDER.json')
 if FINAL:
  while True:
   plays={}
   for p in sorted((R/'reports').glob('M11_REVIEW_*preview-playback.json'),key=lambda p:p.stat().st_mtime):plays.update(json.loads(p.read_text()))
   preview=R/'renders'/f'M11_{shot}_{rev}_PREVIEW_360.mp4'
   if shot in plays and preview.exists() and all(q['ended'] and q['corruptedFrames']==0 and q['sha256']==hashlib.sha256(preview.read_bytes()).hexdigest() for q in plays[shot]):break
   time.sleep(2)
 with (R/'reports'/(name+'.log')).open('a') as log:
  p=subprocess.run([sys.executable,str(R/'source/render_m11.py'),'--shot',shot,'--tag',rev]+(['--final'] if FINAL else []),stdout=log,stderr=subprocess.STDOUT)
 print(shot,stage,p.returncode,flush=True);return p.returncode
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:codes=list(pool.map(job,SHOTS))
 sys.exit(0 if all(c==0 for c in codes) else 1)
