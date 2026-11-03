"""18-scene, exactly86-second illustrated film. Scene caches survive interruptions/corrections."""
from pathlib import Path
import argparse,json,math,subprocess,hashlib,time,textwrap
from PIL import Image
from film_components import *
from illustration_engine import Raster
import v10_trunk as trunk
ROOT=Path(__file__).resolve().parents[1]
SHOTS=json.loads((ROOT/'storyboard.json').read_text());CAPTIONS=json.loads((ROOT/'narration-timing.json').read_text())

def apply_captions(svg,t,scene):
 if scene==18:return svg
 seg=next((s for s in CAPTIONS if s['start']<=t<s['end']),None)
 if not seg:return svg
 a=Art();lines=textwrap.wrap(seg['text'],width=29);y=235 if scene in [3,4,5,6,8,9,10,11,12,13,14,15] else 1485
 for j,line in enumerate(lines):
  yy=y+j*69;a.rect(65,yy-55,950,69,'#030b14',rx=13);text(a,540,yy,line,53,'#f4f0e6',stroke=3)
  if 'police' in line.lower() or 'million' in line.lower():
   # Whole phrase emphasis keeps position/kerning deterministic and mobile-readable.
   text(a,540,yy,line,53,'#efb15c' if 'million' in line.lower() else '#f08b7a',stroke=3)
 return svg.replace('</svg>',''.join(a.s)+'</svg>')

def integrated_ease(t,a,b):
 u=max(0,min(1,(t-a)/(b-a)));return (b-a)*(u**6-3*u**5+2.5*u**4)+max(0,t-b)

def shot01(a,u,t):
 street(a,t,24);x,y,sc=road_point(-45,1450-80*u);car_sprite(a,x,y,sc*.68,'blue','front',u*50)
 text(a,540,590,'2:17 AM',112,WHITE,stroke=5);text(a,540,668,'THE PRICE OF SILENCE',37,'#d2b184')

def shot02(a,u,t):interior_car(a,t,'neutral',65,.08*math.sin(u))
def shot03(a,u,t):
 interior_car(a,t,'worried' if u<1.5 else 'shocked',mix(65,8,ease(u,0,3)),.75*ease(u,.3,2.1),distance=520+65*u-57*integrated_ease(u,0,3))
 # Passing alley is framed at the right of the windshield; the gaze motivates the next cut.
 if u>2.6:
  a.path('M825 455 L1050 390 L1050 1050 L870 1090Z','#06131d','#34515f',4)
  for j in range(8):a.line([(850,560+j*55),(1045,522+j*56)],'#203947',3)

def shot07(a,u,t):interior_car(a,t,'panic',10+230*ease(u,0,1.4),-.4*math.sin(u*1.4),distance=10*u+230*integrated_ease(u,0,1.4))
def shot08(a,u,t):
 street(a,t,180)
 x,y,s=road_point(-35,630+15*u);car_sprite(a,x,y,s*.85,'blue','rear',170*t)
 x,y,s=road_point(-350+310*ease(u,0,3.7),80+50*u);car_sprite(a,x,y,s*1.02,'black','rear',165*t,-.6*(1-ease(u,1,4)))

def shot09(a,u,t):
 if u<2.1:
  street(a,t,265,curve=140*math.sin(u*1.2))
  for z,col,offset in [(650,'blue',40),(230,'black',-20)]:
   x,y,s=road_point(160*math.sin(u*1.35)+offset,z);car_sprite(a,x,y,s*(.85 if col=='blue' else 1.),col,'rear',240*t,.7*math.sin(u*1.35))
 elif u<3.4:
  interior_car(a,t,'panic',240,.6*math.sin(u*2));a.rect(126,380,828,425,'#06121e','#617c89',10,22)
  # Enlarged mirror insert: threatening headlights remain behind, not a disconnected title card.
  a.rect(150,405,780,375,'#102c3e',rx=14)
  for x in [350,690]:a.ellipse(x+10*math.sin(u*4),595,65,37,'#d9f1f7');a.ellipse(x,595,120,90,'url(#lamp)')
  a.path('M170 735 Q540 650 910 735','none','#345967',8)
 else:
  street(a,t,250,curve=-180*ease(u,3.4,5))
  for z,col,lag in [(420,'blue',0),(60,'black',-.35)]:
   turn=ease(u+lag,3.4,4.8);x,y,s=road_point(-270*turn,z+100*turn);car_sprite(a,x,y,s*.96,col,'rear',250*t,-turn*.85)

def shot10(a,u,t):
 if u<3.5:
  street(a,t,85-55*ease(u,0,3),distance=3500+85*u-55*integrated_ease(u,0,3));x,y,s=road_point(260*ease(u,0,3),420+230*ease(u,0,3));car_sprite(a,x,y,s,'blue','rear',95*t,.8*ease(u,.1,1.6)*(1-ease(u,2.4,3.4)))
  if u<.8:
   x,y,s=road_point(-60,80+1000*ease(u,0,.8));car_sprite(a,x,y,s*.6,'black','front',120*t)
 else:interior_car(a,t,'worried',18,.05)


def shot11(a,u,t):
 house(a,t);car_sprite(a,130,1780,1.12,'blue','rear',10*u)
 if u<.65:
  # A real hinged driver door opens, then clears the running path.
  q=ease(u,0,.55);a.poly([(220,1590),(220+110*q,1567),(220+120*q,1710),(220,1705)],'#3b596c','#708b98',5)
 d=430*ease(u,.45,3.6);x=140+d;ground=1770-.36*d;phase=d/112
 witness_body(a,x,ground,t,'run',d,'panic',scale=1.,phase=phase,floor_slope=-.36)

def hand_key(a,x,y,t,turn=0):
 a.ellipse(x,y,29,35,'#d3d7ce',OUTLINE,5);a.ellipse(x+29,y+9,22,22,'none','#bb9e61',7)
 for j in range(3):
  xx=x+42+j*15;angle=turn*50+8*math.sin(t*18+j);a.add(f'<g transform="rotate({angle} {xx} {y+30})">');a.line([(xx,y+24),(xx,y+108+j*7)],'#a9a99b',10);a.line([(xx,y+87),(xx+15,y+87)],'#bdad8d',8);a.add('</g>')

def shot12(a,u,t):
 # Door and hand share one camera transform; the key shaft reaches the real lock.
 a.add('<g transform="translate(-260 -320) scale(1.5)">')
 house(a,t)
 angle=18*math.sin(u*8)*(1-ease(u,1.0,1.4));a.add(f'<g transform="rotate({angle} 655 1172)">');a.ellipse(655,1172,16,18,'#b38c54',OUTLINE,4);a.line([(655,1172),(701,1172)],'#d6b77f',12);a.add('</g>')
 hand=(790-105*ease(u,0,.6),1205)
 if u>1.1:hand=(790-102*ease(u,1.6,3.3),1245-85*ease(u,2.4,3.6))
 ss=(900,1350);el=ik(ss,hand,155,150,-1);limb(a,[ss,el,hand],'#223b49',46)
 if u<1.15:a.ellipse(*hand,28,34,'#d2d6cc',OUTLINE,5)
 else:
  hand_key(a,*hand,t,ease(u,3.,3.8))
  if u>3.:a.line([(hand[0]-15,hand[1]+9),(655,1172)],'#bfc1b2',7)
 a.add('</g>')

def shot13(a,u,t):
 house(a,t,interior=True)
 if u<1.3:
  opening=1-ease(u,0,1.2);a.rect(278,398,524*opening,1025,'#030a11')
 witness_body(a,500,1565,t,emotion='panic' if u<2 else 'worried',scale=1.7,hand_target=(108,-200))
 # Lock close-up is inset only once the door is visibly shut.
 if u>1.6:
  q=ease(u,1.6,2.9);a.rect(635,1080,315,280,'#142d3d','#4c6572',5,16);a.rect(729,1180,112,30,'#b6975c',OUTLINE,5,8)
  a.add(f'<g transform="rotate({90*q} 785 1195)">');a.line([(752,1195),(818,1195)],'#d4b57a',14);a.add('</g>')
  a.ellipse(857-58*q,1210,36,42,'#d0d5cb',OUTLINE,5)

def shot14(a,u,t):
 if u<1.35:
  a.rect(0,0,1080,1920,'#102735');a.poly([(80,1730),(865,1730),(865,620),(80,1480)],'#142f3d','#3f5967',6)
  for j in range(8):
   yy=1660-j*115;xx=400+j*60;yy=1700-j*70;a.line([(xx,yy),(xx+220,yy)],'#6a7a7e',9)
  a.line([(200,1340),(930,400)],'#6c7e87',14);a.line([(200,1340),(200,1760)],'#314e61',12)
  d=145*ease(u,0,1.3);witness_body(a,440+1.25*d,1700-1.18*d*1.25,t,'run',d,'panic',scale=1.25,phase=d/48,floor_slope=-1.18)
 else:
  room(a,t)
  # View from the upstairs window. Parked black car is the same recurring vehicle component.
  a.rect(420,230,600,850,'#04111c','#70838d',14);a.rect(442,252,555,803,'#102b3b')
  a.poly([(442,760),(997,640),(997,1055),(442,1055)],'#17333e','none',0)
  car_sprite(a,740,915,.85,'black','front',.15*math.sin(t*5))
  rainfall(a,t,90,True)
  pull=ease(u,1.35,2.4);a.path(f'M396 180 L{675-220*pull} 200 L{657-220*pull} 1180 Q440 1250 394 1155Z','#24404e','#0a1b29',7)
  # Over-the-shoulder silhouette and hand attached to the curtain edge.
  a.path('M0 1910 L0 1170 Q150 1000 355 1160 L490 1920Z','url(#cloth)',OUTLINE,9)
  a.ellipse(190,1000,150,170,'#0b1b28',OUTLINE,8);a.path('M31 950 Q176 876 357 935 L370 984 Q201 968 30 1003Z','#102634',OUTLINE,7)
  hand=(650-220*pull,1050);limb(a,[(300,1250),(450,1180),hand],'#223c4b',44);a.ellipse(*hand,28,35,'#cbd2cb',OUTLINE,5)

def call_character(a,u,t,emotion='shocked',look=0):
 room(a,t);witness_body(a,470,1510,t,emotion=emotion,hand_target=(140,-340),scale=2.,head_yaw=look*.75)
 # Phone stays at the right-hand/ear anchor rather than floating independently.
 phone(a,747,820,t,'connected',.48)
 if look:
  a.path('M625 820 Q720 780 795 684','none','#e1bb78',2,'opacity=".35"')

def shot15(a,u,t):
 if u<2.35:
  room(a,t);witness_body(a,300,1650,t,emotion='worried',scale=1.6)
  phone(a,675,1060,t,'ring',1.25)
  if u>1.65:
   tap=ease(u,1.65,2.25);limb(a,[(1030,1650),(930,1420),(775,1290-20*tap)],'#243e4d',55);a.ellipse(775,1290-20*tap,30,40,'#ced4cb',OUTLINE,5)
 else:call_character(a,u,t,'worried')
def shot16(a,u,t):
 call_character(a,u,t,'shocked');amount=ease(u,.2,1.2);a.add(f'<g opacity="{amount}">');text(a,540,360,'$1,000,000',112,'#f2bf6b',stroke=5);text(a,540,430,'FOR YOUR SILENCE',42,'#d9dfd8',stroke=3);a.add('</g>')
 # Environmental light changes and a reaction lean, without camera shake.
 if u>3.4:a.path('M1000 260 L880 260 L300 1350 L820 1350Z','#f2bd72','none',0,'opacity=".035"')
def shot17(a,u,t):
 q=ease(u,2.0,4.5);call_character(a,u,t,'worried',q)
 a.path(f'M706 430 L{872-50*q} 430 L960 1370 L515 1370Z','#9ebcca','none',0,f'opacity="{.02+.03*q}"')
 # The glance is carried by the face/shoulders and window light; phone contact remains stable.

def shot18(a,u,t):
 a.rect(0,0,1080,1920,'#04111c');rainfall(a,t,75)
 text(a,540,220,'THE PRICE OF SILENCE',40,'#9fb6c3');text(a,540,400,'WHAT WOULD',88,WHITE,stroke=4);text(a,540,510,'YOU DO?',105,'#e85f51',stroke=4)
 for j,(top,color,lab,line1,line2) in enumerate([(690,'#19643e','A','TAKE','$1,000,000'),(1110,'#7e2631','B','CALL','THE POLICE')]):
  q=ease(u,.12+j*.12,.5+j*.12);a.add(f'<g opacity="{q}">');a.rect(100,top,880,330,'#0a241e' if j==0 else '#2a111b',color,8,35)
  text(a,210,top+195,lab,125,'#dff0d5' if j==0 else '#ffe3df');text(a,610,top+120,line1,61,WHITE);text(a,610,top+230,line2,70,WHITE)
  # Original simple money stack / shield icons.
  if j==0:
   for k in range(3):a.poly([(400+k*5,top+40-k*9),(435+k*5,top+22-k*9),(476+k*5,top+40-k*9),(441+k*5,top+59-k*9)],'#79b98d','#c1dfb5',2)
  else:a.path(f'M410 {top+26} l35 -12 35 12 -3 37 q-28 26 -34 29 q-33 -17 -34 -29Z','none','#ffe0d5',3)
  a.add('</g>')
 text(a,540,1570,'COMMENT A OR B',62,WHITE,stroke=4);text(a,540,1655,'FOR PART 2',63,'#e9b86b',stroke=4)

SCENE_FUNCS={1:shot01,2:shot02,3:shot03,7:shot07,8:shot08,9:shot09,10:shot10,11:shot11,12:shot12,13:shot13,14:shot14,15:shot15,16:shot16,17:shot17,18:shot18}
def scene_svg(scene_id,u):
 s=SHOTS[scene_id-1];t=s['start']+u
 if scene_id in (4,5,6):
  q=(u/6*1.4) if scene_id==4 else (1.4+u/6*5.3 if scene_id==5 else 6.7+u/4*3.3)
  svg=trunk.scene(q);return apply_captions(svg,t,scene_id)
 a=Art();begin(a);SCENE_FUNCS[scene_id](a,u,t);svg=finish(a,t,rain=scene_id in [1,8,9,10,11,12]);return apply_captions(svg,t,scene_id)

def fingerprint(scene_id,stage,scale):
 import ast
 h=hashlib.sha256();source=Path(__file__).read_text();funcs={n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
 for p in [ROOT/'src/film_components.py',ROOT/'src/illustration_engine.py']:h.update(p.read_bytes())
 names=['apply_captions','scene_svg']
 if scene_id in (3,7,10):names.append('integrated_ease')
 if scene_id in (4,5,6):h.update((ROOT/'src/v10_trunk.py').read_bytes())
 else:names.append('shot'+str(scene_id).zfill(2))
 if scene_id==12:names.append('hand_key')
 if scene_id in (15,16,17):names.append('call_character')
 for name in names:h.update(funcs[name].encode())
 h.update(json.dumps([s for s in CAPTIONS if s['scene']==scene_id],sort_keys=True).encode());h.update(json.dumps(SHOTS[scene_id-1],sort_keys=True).encode());h.update(f'{scene_id}/{stage}/{scale}/30'.encode());return h.hexdigest()[:12]
def render_scene(scene_id,stage,scale):
 shot=SHOTS[scene_id-1];key=fingerprint(scene_id,stage,scale);dest=ROOT/'cache'/stage/f'scene_{scene_id:02d}_{key}.mp4';frames=shot['frames'];w=round(1080*scale/2)*2;h=round(1920*scale/2)*2
 if dest.exists():
  check=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','json',str(dest)]))
  if int(check['streams'][0]['nb_read_frames'])==frames:print('CACHE',dest.name,flush=True);return dest
  raise RuntimeError('Incomplete cache file; preserve and rename before retry: '+str(dest))
 tmp=dest.with_suffix('.rendering.mp4');assert not tmp.exists(),tmp;rr=Raster(w,h)
 cmd=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','30','-i','pipe:0','-an','-c:v','libx264','-threads','2','-preset','fast','-crf','20' if stage=='final' else '24','-pix_fmt','yuv420p','-movflags','+faststart',str(tmp)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);beg=time.time()
 try:
  for f in range(frames):
   svg=scene_svg(scene_id,f/30);im=rr.render(svg);proc.stdin.write(im.tobytes())
   if f in [0,frames//2,frames-1]:im.save(ROOT/'previews'/f'{stage}_scene_{scene_id:02d}_{key}_f{f:03d}.jpg',quality=93)
   if f%60==0:print(f'{stage} SCENE {scene_id:02d} {f}/{frames}',flush=True)
 finally:proc.stdin.close()
 if proc.wait():raise RuntimeError('Encoding failed '+str(tmp))
 tmp.rename(dest);(ROOT/'cache'/stage/f'scene_{scene_id:02d}.json').write_text(json.dumps({'scene':scene_id,'path':str(dest.relative_to(ROOT)),'fingerprint':key,'frames':frames,'render_seconds':time.time()-beg},indent=2));print('DONE',dest.name,flush=True);return dest

def assemble(stage,paths,output=None):
 out=ROOT/(output if output else ('THE_PRICE_OF_SILENCE_FULL_FILM_86s.mp4' if stage=='final' else 'previews/THE_PRICE_OF_SILENCE_ANIMATIC_86s.mp4'))
 if out.exists():raise SystemExit('Refusing output overwrite '+str(out))
 listing=ROOT/'cache'/stage/'concat.txt';listing.write_text(''.join("file '"+str(p)+"'\n" for p in paths))
 subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-i',str(ROOT/('assets/audio/master_mix.wav' if (ROOT/'assets/audio/master_mix.wav').exists() else 'assets/audio/final_mix.wav')),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-t','86','-movflags','+faststart',str(out)],check=True)
 print('ASSEMBLED',out,flush=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out');p.add_argument('--stage',choices=['preview','final'],default='preview');p.add_argument('--scene',type=int);p.add_argument('--range',dest='scene_range');p.add_argument('--scale',type=float);p.add_argument('--assemble-only',action='store_true');args=p.parse_args();scale=args.scale or (1/3 if args.stage=='preview' else 1.)
 if args.scene:render_scene(args.scene,args.stage,scale);return
 if args.scene_range:
  a,b=map(int,args.scene_range.split(':'));assert 1<=a<=b<=18
  for i in range(a,b+1):render_scene(i,args.stage,scale)
  return
 paths=[]
 for scene_id in range(1,19):
  if args.assemble_only:
   key=fingerprint(scene_id,args.stage,scale);dest=ROOT/'cache'/args.stage/f'scene_{scene_id:02d}_{key}.mp4';assert dest.exists(),dest;paths.append(dest)
  else:paths.append(render_scene(scene_id,args.stage,scale))
 assemble(args.stage,paths,args.out)
if __name__=='__main__':main()
