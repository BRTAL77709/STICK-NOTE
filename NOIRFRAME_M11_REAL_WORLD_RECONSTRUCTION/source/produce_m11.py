from pathlib import Path
import subprocess,json,gzip,hashlib,sys,argparse
from bootstrap import ROOT as R
from production_guard import ensure
SHOTS=['DRIVING_COCKPIT','DRIVER_CHASE','CAR_EXIT_RUNNING','KEY_LOCK','DOOR_ENTRY','STAIRS','WINDOW_CURTAIN','PHONE_CALL','UNKNOWN_CALLER','DISCOVERY','PANIC']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--tag',default='M11R01');p.add_argument('shots',nargs='*');a=p.parse_args();ensure('source checkpoint before native '+a.tag)
 for shot in (a.shots or SHOTS):
  tag=a.tag;cache=R/'scenes'/f'{shot}_{tag}.json.gz';model=R/'blender'/f'{shot}_{tag}.blend';log=R/'reports'/f'{shot}_{tag}_BAKE.log'
  if not cache.exists():
   with log.open('w') as f:p=subprocess.run(['blender','-b','-t','1','--python',str(R/'source/bake_native.py'),'--','--shot',shot,'--tag',tag],stdout=f,stderr=subprocess.STDOUT)
   assert cache.exists() and model.exists() and 'NATIVE_BAKED' in log.read_text(),log.read_text()[-3000:]
  data=json.load(gzip.open(cache,'rt'));assert hashlib.sha256(model.read_bytes()).hexdigest()==data['blend_sha256'];print('VERIFIED_NATIVE',shot,flush=True)
  # Native outputs are irreplaceable milestone material: remote backup now, before the next shot.
  from checkpoint_store import pack
  archive,rows=pack([cache,model],shot+'-'+tag)
  subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'asset','--path',str(archive.relative_to(R)),'--label',shot+'-'+tag],check=True)
 subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'milestone','--label','native rigs and evaluated caches baked and remotely verified'],check=True)
