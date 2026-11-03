"""15s integrated gate; deterministic SVG/Art/librsvg pipeline preserved."""
from pathlib import Path
import math,json,argparse,subprocess,textwrap,time
from illustration_engine import Art,Raster
from approved_components import begin,text,witness_head,finish
from motion_state import *
from world import Camera,city,INK
from vehicle import sedan
from driving import driver,dashboard,pedal
ROOT=Path(__file__).resolve().parents[1]

def rain(a,t,glass=False):
 # Near/mid/far rain have different scale/velocity; repeatable without temporal state.
 import random
 rng=random.Random(21717)
 for layer,count in [(0,65),(1,65),(2,45)]:
  for j in range(count):
   x=rng.uniform(-100,1250);y=(rng.uniform(-100,2100)+t*(450+layer*300))%2200-100;ll=16+layer*19
   a.path(f'M{x:.1f} {y:.1f} l{-ll*.15:.1f} {ll}','none','#8eb0ba',.8+layer*.5,f'opacity="{.12+layer*.05}"')
 if glass:
  for j in range(17):
   x=30+j*64;y=(j*147+t*53)%1150;a.path(f'M{x} {y} q-6 28 -4 62','none','#aec4c8',2,'opacity=".27"')

def ext_camera(t,chase=False):
 s=state(t);yaw=s['yaw'];behind=(28-14*ease(t,5,11)+8) if chase else 9.5;side=-4.8 if not chase else -4.4
 x=s['x']-math.sin(yaw)*behind+math.cos(yaw)*side;z=s['z']-math.cos(yaw)*behind-math.sin(yaw)*side
 targetz=s['z']-(9 if chase else 0);targetx=road_x(targetz)+.6
 return Camera(x,z,1.25 if chase else 2.8,math.atan2(targetx-x,targetz-z),1320,820)
def front_camera(t):
 s=state(t);return Camera(s['x'],s['z']+1.8,1.15,s['yaw'],950,660)
def outer(a,t,chase=False):
 c=ext_camera(t,chase);city(a,c,t)
 # Paint far car first; pursuit position/steering comes from the same route.
 if chase:
  sedan(a,c,t,False);sedan(a,c,t,True)
 else:sedan(a,c,t,False)
 rain(a,t)
 # Deliberate foreground rain splash; road remains fixed relative to cars.
 s=state(t)
 for j in range(12):
  x=40+j*91;y=1700+(j%3)*70;u=(t*1.5+j*.13)%1;a.ellipse(x,y,10+22*u,2+4*u,'none','#486b77',1.1,extra=f'opacity="{.22*(1-u)}"')

def over_shoulder(a,t):
 c=front_camera(t);city(a,c,t)
 # OTS head/shoulders occupy left; the forward road remains visible through windscreen.
 a.path('M0 0 L1080 0 L1080 250 L980 180 L180 180 L0 460Z','#09151f',INK,9)
 a.path('M1060 170 L1010 1380','none','#0a1621',55);a.path('M1060 170 L1010 1380','none','#5a717c',5)
 a.path('M0 1300 Q540 1150 1080 1300 L1080 1920 L0 1920Z','#0b1d29',INK,10)
 a.path('M0 1920 L0 1230 Q200 1030 430 1210 L535 1920Z','url(#cloth)',INK,9)
 a.add(f'<g transform="rotate({state(t)["steer_rad"]*60} 200 1200)">');a.ellipse(200,1050,161,187,'#0d202d',INK,9);a.path('M44 1010 Q200 900 365 989 L390 1040 Q200 1010 38 1070Z','#152d3c',INK,8)
 a.path('M70 949 Q92 857 190 858','none','#d2a164',5);a.add('</g>')
 a.ellipse(700,1390,218,140,'none',INK,28);a.ellipse(700,1390,218,140,'none','#415b68',15)
 from illustration_engine import ik,limb
 ss=(360,1280);angle=state(t)['steer_rad']*16;hand=(700+210*math.cos(2.8+angle),1390-130*math.sin(2.8+angle));el=ik(ss,hand,145,135,-1);limb(a,[ss,el,hand],'#2a4453',55);a.ellipse(*hand,29,35,'#d9ddd4',INK,6)
 for q in [angle,angle+2.2,angle+4.1]:a.line([(700,1390),(700+200*math.cos(q),1390-130*math.sin(q))],'#2e4a5c',19)
 # Small actual in-dash dial and framed mirror.
 from driving import dial
 dial(a,840,1250,95,speed(t)*3.6)
 a.rect(485,250,330,125,'#091922','#647b85',7,17)
 for xx in [580,720]:a.ellipse(xx,315,15,11,'#c9e3e7')
 a.add('<g clip-path="url(#cabin-glass)">');rain(a,t,True);a.add('</g>')

def svg(t,captions=True):
 a=Art();begin(a)
 a.add('<defs><linearGradient id="citysky" x2="0" y2="1"><stop stop-color="#030d18"/><stop offset="1" stop-color="#284d5a"/></linearGradient><radialGradient id="lamphalo"><stop stop-color="#ffc476" stop-opacity=".32"/><stop offset="1" stop-color="#ffc476" stop-opacity="0"/></radialGradient><clipPath id="cabin-glass"><path d="M50 180 Q540 80 1030 180 L1060 1150 L25 1150Z"/></clipPath></defs>')
 n,st,en,title=shot(t)
 if title=='Ash Avenue tracking':outer(a,t)
 elif title in ['Witness reaction','Driver under acceleration','Mirror / driver']:
  driver(a,t,front_camera(t));a.add('<g clip-path="url(#cabin-glass)">');rain(a,t,True);a.add('</g>')
 elif title=='Pedal contact':pedal(a,t)
 elif title.startswith('Instrument'):
  dashboard(a,t,True)
  # Passing-light reflection across actual dashboard glass.
  u=(travel(t)%24)/24;a.path(f'M{u*1400-400} 770 l180 -80 300 750 -180 40Z','#8cafbb','none',0,'opacity=".035"')
 elif title=='Low pursuit / Mercer bend':outer(a,t,True)
 elif title=='Over shoulder':over_shoulder(a,t)
 a.rect(0,0,1080,1920,'url(#vignette)')
 if captions:
  seg=next((x for x in json.loads((ROOT/'narration-timing.json').read_text()) if x['start']<=t<x['end']),None)
  if seg:
   u=ease(t,seg['start'],seg['start']+.12);a.add(f'<g opacity="{u}" transform="translate(0 {12*(1-u)})">')
   lines=textwrap.wrap(seg['text'],27)
   for j,line in enumerate(lines):
    y=(450 if title=='Pedal contact' else 1500)+j*66;a.rect(110,y-52,860,70,'#07121c',rx=13);text(a,540,y,line,55,'#f1bc79' if 'gas' in line else '#eceee5',stroke=1)
   a.add('</g>')
 a.add('</svg>');return ''.join(a.s)
def main():
 p=argparse.ArgumentParser();p.add_argument('--scale',type=float,default=1/3);p.add_argument('--fps',type=int,default=30);p.add_argument('--from',dest='start',type=float,default=0);p.add_argument('--to',dest='end',type=float,default=15);p.add_argument('--out',default='previews/INTEGRATED_PREVIEW_v1.mp4');p.add_argument('--stills',action='store_true');args=p.parse_args();out=ROOT/args.out;out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists(),out
 w=round(1080*args.scale/2)*2;h=round(1920*args.scale/2)*2;rr=Raster(w,h);num=round((args.end-args.start)*args.fps)
 proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(args.fps),'-i','pipe:0','-ss',str(args.start),'-i',str(ROOT/'assets/audio/master.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-threads','2','-crf','20','-pix_fmt','yuv420p','-af','volume=-0.3dB','-c:a','aac','-b:a','160k','-t',str(args.end-args.start),'-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 try:
  for i in range(num):
   t=args.start+i/args.fps;im=rr.render(svg(t));proc.stdin.write(im.tobytes())
   if args.stills and i%15==0:im.save(ROOT/'previews'/f'{out.stem}_{i:03d}.jpg',quality=93)
   if i%60==0:print(out.name,i,num,flush=True)
 finally:proc.stdin.close()
 if proc.wait():raise RuntimeError('FFmpeg encode failed')
 print('COMPLETE',out,flush=True)
if __name__=='__main__':main()
