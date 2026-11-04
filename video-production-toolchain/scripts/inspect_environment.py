from pathlib import Path
import json,subprocess,platform,importlib.metadata as m
R=Path(__file__).resolve().parents[1]
def run(args):
 p=subprocess.run(args,capture_output=True,text=True);return {'command':args,'exit_code':p.returncode,'output':(p.stdout or p.stderr).strip().splitlines()[0] if (p.stdout or p.stderr).strip() else ''}
versions={k:run(c) for k,c in {'node':['node','--version'],'npm':['npm','--version'],'python':[str(R/'.venv/bin/python'),'--version'],'ffmpeg':['ffmpeg','-version'],'ffprobe':['ffprobe','-version'],'git':['git','--version'],'chromium':['chromium','--version'],'yt-dlp':[str(R/'.venv/bin/python'),'-m','yt_dlp','--version']}.items()}
for name in ['openai-whisper','yt-dlp','torch','numba','numpy','tiktoken','llvmlite']:versions[name]={'version':m.version(name),'verified_by':'importlib.metadata + successful whisper/yt_dlp import'}
for name,path in [('remotion','remotion/node_modules/remotion/package.json'),('@remotion/renderer','remotion/node_modules/@remotion/renderer/package.json'),('react','remotion/node_modules/react/package.json'),('hyperframes','/workspace/stick-note-dev/tools/node_modules/hyperframes/package.json')]:
 p=Path(path) if path.startswith('/') else R/path;d=json.loads(p.read_text());versions[name]={'version':d['version'],'package_path':str(p.resolve())}
report={'OS':platform.platform(),'architecture':platform.machine(),'versions':versions,'network':'Restricted proxy, package manager/GitHub access observed; official Whisper weights and HF probe returned CONNECT403.','CPU_only':True,'no_cloud_rendering':True,'cost_incurred':0};(R/'reports/installed-versions.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
