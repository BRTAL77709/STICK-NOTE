from pathlib import Path
import json,subprocess,argparse
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--stage',default='previews',choices=['previews','final']);a=p.parse_args();paths=[]
for i in range(1,19):
 x=json.loads((R/'scenes'/f'scene_{i:02d}'/f'{a.stage}-cache.json').read_text());paths.append(R/x['path'])
l=R/'renders'/a.stage/'concat.txt';l.write_text(''.join("file '"+str(p)+"'\n" for p in paths));out=R/'renders'/a.stage/'SCENE_BASE_86s.mp4'
assert not out.exists(),out
subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(l),'-c:v','copy','-movflags','+faststart',str(out)],check=True)
print(out)
