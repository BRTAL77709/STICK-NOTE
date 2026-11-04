"""Record reused runtimes and preserve every pre-existing STICK-NOTE file."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[1];base=R.parent
protected={str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in base.rglob('*') if p.is_file() and R not in p.parents and '__pycache__' not in p.parts and '.git' not in p.parts}
(R/'reports/preservation-before.json').write_text(json.dumps(protected,indent=2))
src=base/'full-film-real-motion-rebuild/engine/animation';shutil.copytree(src,R/'animation',ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
shared='/workspace/stick-note-dev/stickman-horror/source/node_modules';
if not (R/'remotion/node_modules').exists():(R/'remotion/node_modules').symlink_to(shared,target_is_directory=True)
font=base/'full-film-real-motion-rebuild/hyperframes/assets/FilmSans-Bold.ttf'
for target in ['remotion/public/FilmSans-Bold.ttf','hyperframes/assets/FilmSans-Bold.ttf']:shutil.copyfile(font,R/target)
gsap=base/'full-film-real-motion-rebuild/hyperframes/assets/gsap.min.js';shutil.copyfile(gsap,R/'hyperframes/assets/gsap.min.js')
package=json.loads(Path('/workspace/stick-note-dev/stickman-horror/source/package.json').read_text());package.update(name='noirframe-local-toolchain-demo');package['scripts']={'render':'node ../scripts/render-remotion.cjs','studio':'remotion studio src/index.tsx --browser-executable=/usr/bin/chromium'};(R/'remotion/package.json').write_text(json.dumps(package,indent=2))
clips=json.loads((base/'full-film-real-motion-rebuild/narration-timing.json').read_text());speech=next(x for x in clips if x['text']=='I hit the gas.');shutil.copyfile(base/'full-film-real-motion-rebuild'/speech['asset'],R/'shared/narration.wav');(R/'shared/narration-script.txt').write_text(speech['text']+'\n');(R/'shared/speech-source.json').write_text(json.dumps(speech,indent=2))
print('Protected',len(protected),'existing files; copied approved evaluators and local runtimes.')
