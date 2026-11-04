from pathlib import Path
import sys,json,html,textwrap,shutil,argparse,hashlib
from PIL import ImageFont
R=Path(__file__).resolve().parents[1];H=R/'hyperframes';sys.path.insert(0,str(R/'engine/graphics'))
from design import CSS,dial,gauge,clip,template
p=argparse.ArgumentParser();p.add_argument('--stage',choices=['previews','final'],default='previews');args=p.parse_args()
H.joinpath('assets/scenes').mkdir(exist_ok=True)
shots=json.loads((R/'storyboard.json').read_text());media=[]
for s in shots:
 m=json.loads((R/'scenes'/f'scene_{s["scene"]:02d}'/f'{args.stage}-cache.json').read_text());source=R/m['path'];dest=H/'assets/scenes'/source.name
 if not dest.exists():shutil.copy2(source,dest)
 media.append(f'<video id="scene-{s["scene"]:02d}" class="clip" data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="0" src="assets/scenes/{source.name}" muted playsinline style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:contain;z-index:0" data-layout-allow-overlap data-layout-allow-caption-zone></video>')
audio_meta=json.loads((R/'AUDIO_OUTPUT.json').read_text());audio_source=R/audio_meta['mix'];audio_name='mix-rebuild-'+hashlib.sha256(audio_source.read_bytes()).hexdigest()[:12]+'.flac';audio_dest=H/'assets'/audio_name
if not audio_dest.exists():shutil.copy2(audio_source,audio_dest)
HEAD='''<!doctype html><html lang="en"><head><meta charset="UTF-8"><script>window.FILM_DURATION=86;</script><script src="assets/gsap.min.js"></script><script src="assets/vehicle-state.js"></script><script src="assets/components.js"></script><script src="assets/components-v4.js"></script><style>html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#06131e}*{box-sizing:border-box}#root{position:absolute;inset:0}</style></head><body>'''
root=HEAD+'<div id="root" data-composition-id="main" data-start="0" data-duration="86" data-width="1080" data-height="1920" data-fps="30">'+''.join(media)+'''<audio id="sound-mix" class="clip" data-start="0" data-duration="86" data-track-index="1" src="assets/mix.flac" data-volume="1"></audio>'''
for i,n in enumerate(['hud','captions','story-graphics']):root+=f'<div id="{n}" class="clip" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="0" data-duration="86" data-track-index="{i+2}" data-track-kind="'+('captions' if n=='captions' else 'graphics')+'" data-width="1080" data-height="1920" style="z-index:'+str(i+2)+'"></div>'
root+='</div><script>const tl=gsap.timeline({paused:true});tl.to({t:0},{t:86,duration:86,ease:"none"});window.__timelines=window.__timelines||{};window.__timelines.main=tl;</script></body></html>'
(H/'index.html').write_text(root.replace('assets/mix.flac','assets/'+audio_name))
body=clip('clock-clip',0,4,'<section id="clock-panel" class="panel clock" style="left:108px;top:230px;width:394px;height:168px"><div class="label">LOCAL TIME</div><div id="clock-value" class="value">02:17:00</div><div class="unit">AM</div></section>')
js="""(()=>{const C=HFComponents,tl=gsap.timeline({paused:true}),clock=new C.DigitalClock('#clock-value');new C.CinematicHUDPanel('#clock-panel').animate(tl,.04,4);const p={t:0};function draw(t){clock.render(t);}tl.to(p,{t:86,duration:86,ease:'none',onUpdate:()=>draw(p.t)},0);draw(0);window.__timelines=window.__timelines||{};window.__timelines.hud=tl;})();"""
(H/'compositions/hud.html').write_text(template('hud',body,js))
caps=json.loads((R/'narration-timing.json').read_text());body='';js='const tl=gsap.timeline({paused:true});'
for j,c in enumerate(caps):
 if c['scene']==18:continue
 top=1760 if c['scene']==7 else 230 if c['scene'] in [3,4,5,6,11,12,13] else (1750 if c['scene']==14 else 1700 if c['scene'] in [15,16,17] else 1520)
 font=ImageFont.truetype(str(H/'assets/FilmSans-Bold.ttf'),52);words=[];current=''
 for word in c['text'].split():
  candidate=(current+' '+word).strip()
  if current and font.getlength(candidate)-len(candidate)>790:words.append(current);current=word
  else:current=candidate
 if current:words.append(current)
 if len(words)>1 and len(words[-1].split())==1 and len(words[-2].split())>3:
  prev=words[-2].split();words[-1]=prev.pop()+' '+words[-1];words[-2]=' '.join(prev)
 lines=[]
 for line in words:
  lines.append(' '.join('<em>'+html.escape(w)+'</em>' if w.lower().strip('.,?') in ['gas','trunk','million','police','alone','waiting'] else html.escape(w) for w in line.split()))
 inside='<br>'.join(lines);body+=clip(f'cap-{j}-clip',c['start'],c['end'],f'<div id="cap-{j}" class="caption" style="top:{top}px" data-layout-allow-caption-zone><span class="caption-body">{inside}</span></div>');js+=f"new V4Components.WordByWordCaptions('#cap-{j}').phrase(tl,{c['start']},{c['end']});tl.set('#cap-{j}',{{opacity:0,visibility:'hidden'}},{c['end']});"
js+="window.__timelines=window.__timelines||{};window.__timelines.captions=tl;"
(H/'compositions/captions.html').write_text(template('captions',body,'(()=>{'+js+'})();'))
extra=''' .call-notice{position:absolute;left:108px;top:220px;width:640px;height:160px;padding:25px 34px;background:rgba(7,21,34,.96);border:2px solid #859b9f;border-radius:16px}.caller-label{font-size:29px;letter-spacing:3px;color:#ffb15b;font-weight:700}.caller-name{font-size:44px;line-height:1.1;margin-top:12px;font-weight:700}.call-dot{position:absolute;right:30px;top:55px;width:16px;height:16px;border-radius:50%;background:#ffb15b} .offer{position:absolute;left:108px;top:230px;width:864px;height:260px}.offer .value{font-size:105px;margin-top:18px;letter-spacing:-3px}.offer .label{font-size:30px}.choice-title{position:absolute;left:108px;top:340px;width:864px;text-align:center;font-size:82px;font-weight:700;line-height:1.2}.brand{position:absolute;left:108px;top:220px;font-size:36px;color:#ffb15b;font-weight:700;letter-spacing:5px}.choice-card{position:absolute;left:108px;width:864px;height:260px;padding:48px 38px;border:2px solid #edaa5c;border-radius:20px;background:rgba(5,20,31,.96);font-size:54px;font-weight:700;line-height:1.3}.choice-card strong{color:#ffb15b;font-size:64px}.choice-cta{position:absolute;left:108px;top:1430px;width:864px;text-align:center;font-size:48px;font-weight:700;line-height:1.35}'''
body=clip('incoming-clip',69.6,70.25,'<section id="incoming" class="call-notice"><div class="caller-label">INCOMING CALL</div><div class="caller-name">UNKNOWN CALLER</div><span id="incoming-dot" class="call-dot"></span></section>')
body+=clip('offer-clip',72.47,77.3,'<section id="offer" class="panel offer"><div class="label">FOR YOUR SILENCE</div><div id="offer-value" class="value">$0</div><div class="track"><div id="offer-bar" class="fill"></div></div></section>')
body+=clip('choice-clip',81.5,86,'<div id="choices"><div class="brand">NOIRFRAME</div><div class="choice-title">WHAT WOULD<br><span style="color:#ffb15b">YOU DO?</span></div><section id="choice-a" class="choice-card" style="top:700px;border-color:#67b98b"><strong>A</strong> — TAKE<br>$1,000,000</section><section id="choice-b" class="choice-card" style="top:1040px;border-color:#db7a77"><strong>B</strong> — CALL<br>THE POLICE</section><div class="choice-cta">COMMENT A OR B<br>FOR PART 2</div></div>')
js="""(()=>{const C=HFComponents,tl=gsap.timeline({paused:true});new C.CinematicHUDPanel('#incoming').animate(tl,69.6,70.25);tl.fromTo('#incoming-dot',{opacity:.35},{opacity:1,duration:.12,repeat:3,yoyo:true,ease:'sine.inOut'},69.66);new C.CinematicHUDPanel('#offer').animate(tl,72.47,77.3);const offer=new C.MillionDollarOffer('#offer-value'),bar=new C.AnimatedProgressBar('#offer-bar',{max:1000000}),money={value:0};bar.render(0);tl.to(money,{value:1000000,duration:1.35,ease:'power2.inOut',onUpdate:()=>{offer.render(money.value);bar.render(money.value);}},72.5);tl.fromTo('#choices',{opacity:0},{opacity:1,duration:.22,ease:'power2.out'},81.5);new C.InteractiveChoiceCards('#choice-a','#choice-b').reveal(tl,81.62);window.__timelines=window.__timelines||{};window.__timelines['story-graphics']=tl;})();"""
(H/'compositions/story-graphics.html').write_text(template('story-graphics',body,js).replace(CSS,CSS+extra))
(H/'hyperframes.json').write_text(json.dumps({'$schema':'https://hyperframes.heygen.com/schema/hyperframes.json','paths':{'blocks':'compositions','components':'compositions/components','assets':'assets'},'media':{'autoProxy':False}},indent=2))
(H/'index.motion.json').write_text(json.dumps({'duration':86,'assertions':[{'kind':'appearsBy','selector':'#clock-panel','bySec':.35},{'kind':'staysInFrame','selector':'#offer'},{'kind':'staysInFrame','selector':'#choice-a'},{'kind':'staysInFrame','selector':'#choice-b'}]},indent=2))
print('Actual HyperFrames 86s / 18 scene videos / story HUD / offer / call / cards / captions built from',args.stage)
