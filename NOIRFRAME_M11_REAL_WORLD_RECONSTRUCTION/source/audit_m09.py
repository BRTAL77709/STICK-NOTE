"""Input audit, actual native solver checks and scoped preservation measurements."""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys
import numpy as np
from bootstrap import ROOT as R
from validate_interactions import run
base=Path('/workspace/STICK-NOTE/NOIRFRAME_M08_CINEMATIC_REPAIRS')
rows={}
for shot,tag in json.loads((R/'reports/SHOT_REVISIONS.json').read_text()).items():
 if shot in ['ROAD_BUILDINGS','CAR_CHASE']:continue
 if not (R/'scenes'/f'{shot}_{tag}.json.gz').exists():continue
 rows[shot]=run(shot,tag)
(R/'reports/NATIVE_QA_SUMMARY.json').write_text(json.dumps(rows,indent=2))
inputs=[]
for p in sorted((base/'renders').glob('M08_*_FINAL.mp4')):
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));inputs.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'duration':meta['format']['duration'],'video':[{'codec':s['codec_name'],'width':s.get('width'),'height':s.get('height')} for s in meta['streams']]})
(R/'reports/INPUT_MEDIA_AUDIT.json').write_text(json.dumps(inputs,indent=2))
