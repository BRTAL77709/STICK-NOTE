from bootstrap import ROOT as R
import subprocess,sys
from production_guard import ensure
from checkpoint_store import pack
ensure('native world export source checkpoint')
for shot in ['MASTER_LAYOUT','ROAD_BUILDINGS','CAR_CHASE','ARRIVAL']:
 out=R/'blender'/f'{shot}_WORLD_M11R03.blend';report=R/'reports'/f'{shot}_WORLD_SOURCE.json'
 if not out.exists():
  with (R/'reports'/f'{shot}_WORLD_EXPORT.log').open('w') as f:p=subprocess.run(['blender','-b','-t','1','--python',str(R/'source/export_world_m11.py'),'--','--shot',shot],stdout=f,stderr=subprocess.STDOUT)
 assert out.exists() and report.exists(),shot
 archive,_=pack([out,report],shot+'-world');subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'asset','--path',str(archive.relative_to(R)),'--label',shot+'-world'],check=True)
subprocess.run([sys.executable,str(R/'source/checkpoint_store.py'),'milestone','--label','complete native world and vehicle layout backed up'],check=True)
