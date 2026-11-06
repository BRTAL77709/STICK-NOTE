"""Correct inherited diagnostic titles only. Preserve original diagnostics; never alter clean films."""
import json,subprocess,hashlib,shutil,argparse
from bootstrap import ROOT as R
pa=argparse.ArgumentParser();pa.add_argument('--shots',nargs='*');pa.add_argument('--archive-name',default='diagnostics_before_M08_labels');a=pa.parse_args();rows=json.loads((R/'CURRENT_SHOTS.json').read_text());rows={s:q for s,q in rows.items() if not a.shots or s in a.shots};out=json.loads((R/'reports/DIAGNOSTIC_FINISH.json').read_text()) if (R/'reports/DIAGNOSTIC_FINISH.json').exists() else {};archive=R/'scratch'/a.archive_name;archive.mkdir(exist_ok=True)
for shot,row in rows.items():
 p=R/row['diagnostic'];raw=archive/p.name;assert p.exists() and not raw.exists();shutil.move(str(p),str(raw));vf=f"drawbox=x=0:y=0:w=iw:h=44:color=0x071521:t=fill,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='M08 {shot} / DIAGNOSTIC / %{{pts\\:hms}}':x=10:y=10:fontsize=21:fontcolor=white"
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-vf',vf,'-an','-r','30','-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-movflags','+faststart',str(p)],check=True)
 out[shot]={'before_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'final_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'change':'Diagnostic title band only; native contacts, frame timing and clean film untouched.'};print('DIAGNOSTIC_LABELLED',shot,flush=True)
(R/'reports/DIAGNOSTIC_FINISH.json').write_text(json.dumps(out,indent=2))
