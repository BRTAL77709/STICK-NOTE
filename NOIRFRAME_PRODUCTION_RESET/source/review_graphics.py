from pathlib import Path
import json,math
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];rows=[];native=json.loads((R/'reports/SHOT_A_v11_rig-data.json').read_text())['samples']
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);page=b.new_page(viewport={'width':920,'height':300})
 for mode in ['speed','clock','pursuit','phone','offer','choice']:
  import re
  html=(R/'graphics/index.html').read_text().replace("new URLSearchParams(location.search).get('mode')||'speed'",repr(mode))
  main=re.findall(r'<script>([\s\S]*?)</script>',html)[-1]
  page.set_content(re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',html))
  for asset in ['assets/gsap.min.js','assets/vehicle-state.js']:page.evaluate('(s)=>{(0,eval)(s)}',(R/'graphics'/asset).read_text())
  page.evaluate('(s)=>{(new Function(s))()}',main)
  page.wait_for_function('Boolean(window.__timelines?.main)',timeout=5000)
  for t in [0,1,2.5,4.9]:
   state=page.evaluate('(t)=>{__timelines.main.seek(t,false);return window.__GRAPHICS_STATE}',t);assert state['mode']==mode;assert abs(state['time']-t)<.001
   if mode=='speed':assert abs(state['distance_m']-native[math.floor(t*30)]['prop_state']['distance_m'])<1e-8
   rows.append(state)
  page.screenshot(path=str(R/f'reviews/GRAPHICS_DRAFT_{mode}.png'))
 b.close()
(R/'reports/graphics-state-validation.json').write_text(json.dumps({'clock_seek_checks_pass':True,'actual_vehicle_binding':'speed only','other_modes':'storyboard prototypes, not completed film integration','samples':rows},indent=2));print('GRAPHICS_STATE_SEEKS_PASS')
