from pathlib import Path
import subprocess,concurrent.futures,sys,json
R=Path(__file__).resolve().parents[1]
def job(shot):
 log=R/'reports'/f'{shot}_BAKE_D.log'
 with log.open('w') as f:
  p=subprocess.run(['blender','-b','-t','1','--python',str(R/'source/bake_native.py'),'--','--shot',shot,'--tag','M09D'],stdout=f,stderr=subprocess.STDOUT)
 return shot,p.returncode
if __name__=='__main__':
 shots=['DRIVING_COCKPIT','DRIVER_CHASE','CAR_EXIT_RUNNING','KEY_LOCK','DOOR_ENTRY','WINDOW_CURTAIN']
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
  for q in e.map(job,shots):print(q,flush=True)
