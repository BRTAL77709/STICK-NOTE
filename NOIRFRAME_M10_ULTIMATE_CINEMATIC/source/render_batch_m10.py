from pathlib import Path
import subprocess,concurrent.futures,argparse,json
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=360);p.add_argument('--final',action='store_true');p.add_argument('--shots',nargs='*');a=p.parse_args()
shots=['DRIVING_COCKPIT','ROAD_BUILDINGS','CAR_CHASE','CAR_EXIT_RUNNING','KEY_LOCK','DOOR_ENTRY','STAIRS','WINDOW_CURTAIN'];shots=a.shots or shots
revs=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());results={}
def job(s):
 tag=revs.get(s,'M10');cmd=['python',str(R/'source/render_clips.py'),'--shot',s,'--tag',tag,'--width',str(a.width)]+(['--final'] if a.final else ['--step','3'])
 log=R/'reports'/f'{s}_{a.width}_{"FINAL" if a.final else "PREVIEW"}.log'
 with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 # Blender may return success after a Python exception; renderer output existence is independently enforced.
 expected=R/'renders'/(f'M10_{s}_FINAL.mp4' if a.final else f'M10_{s}_{tag}_{a.width}.mp4');ok=r.returncode==0 and expected.exists()
 print(s,'PASS' if ok else 'FAIL',flush=True);return s,ok
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
 for s,ok in e.map(job,shots):results[s]=ok
(R/'reports'/f'BATCH_{a.width}_{a.final}.json').write_text(json.dumps(results,indent=2))
assert all(results.values()),results
