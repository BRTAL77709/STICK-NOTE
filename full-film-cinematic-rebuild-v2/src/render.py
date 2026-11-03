"""V2: seven-beat15s chase with continuous world, articulated driver and actual mirror view."""
from pathlib import Path
import math,json,argparse,subprocess,random
from illustration_engine import Art,Raster
from approved_components import begin,text
from motion_state import *
from world import Camera,city,INK
from vehicle import sedan
from driving import driver,dashboard,pedal
from graphics import hud,captions
ROOT=Path(__file__).resolve().parents[1];CAPS=json.loads((ROOT/'narration-timing.json').read_text())

def rain(a,t,glass=False):
 rng=random.Random(267);v=speed(t);yaw=state(t)['steer_rad']
 for layer,n in [(0,46),(1,45),(2,38)]:
  for j in range(n):
   x=rng.uniform(-80,1190);y=(rng.uniform(-180,2100)+t*(450+layer*360+v*8))%2200-120;ll=(16+layer*18)*(1+v*.012)
   a.path(f'M{x:.1f} {y:.1f} l{-ll*(.16+yaw):.2f} {ll:.2f}','none','#9bb9c0',.8+layer*.65,f'opacity="{.13+layer*.04}"')
 if glass:
  for j in range(13):
   x=57+j*83;y=(j*137+t*70)%1200;a.path(f'M{x} {y} q-5 22 -4 45','none','#c0d0cc',2,'opacity=".2"')

def front_camera(t):
 p=state(t);return Camera(p['x']+math.sin(p['yaw'])*1.4,p['z']+math.cos(p['yaw'])*1.4,1.23,p['yaw'],1010,690)
def ext_camera(t,mode):
 p=state(t)
 if mode=='Departure':
  q=state(t*.55);cx=q['x']-4.6;cz=q['z']-9.2;yaw=math.atan2(p['x']-cx,p['z']-cz)+.105-.14*ease(t,0,2);h=2.2;f=1550
 elif mode=='Street acceleration':
  q=state(7+(t-7)*.97);cx=q['x']-4.7;cz=q['z']-9.2;yaw=math.atan2(p['x']-cx,p['z']-cz)+.04-.09*ease(t,7,10);h=1.38;f=1610
 else:
  q=state(t-.18);angle=q['yaw'];cx=q['x']-math.cos(angle)*5.1-math.sin(angle)*4.5;cz=q['z']+math.sin(angle)*5.1-math.cos(angle)*4.5
  yaw=math.atan2(p['x']-cx,p['z']-cz)+.06-.12*ease(t,13.25,15);h=1.9;f=1510
 # Camera vibration is road/contact-driven and intentionally restrained.
 jitter=.7*math.sin(state(t)['distance_m']*2.2)
 return Camera(cx,cz,h,yaw,f,730+jitter)

def mirror(a,t,box,hero=False):
 x,y,w,h=box;p=state(t);uid='hero-mirror' if hero else 'driver-mirror'
 a.add(f'<defs><clipPath id="{uid}"><rect x="{x+8}" y="{y+8}" width="{w-16}" height="{h-16}" rx="{18 if hero else 9}"/></clipPath></defs>')
 # A physical mount/frame stays outside the clipped reflected scene.
 a.line([(x+w*.5,y-100),(x+w*.5,y)],'#192f3d',22 if hero else 12)
 a.rect(x-8,y-8,w+16,h+16,'#07111a','#81939a',7 if hero else 4,25 if hero else 14)
 c=Camera(p['x'],p['z']+1.0,1.25,p['yaw']+math.pi,1630 if hero else 1430,670)
 a.add(f'<g clip-path="url(#{uid})"><g transform="translate({x+w} {y}) scale({-w/1080} {h/660}) translate(0 -420)">')
 city(a,c,t);sedan(a,c,t,True);rain(a,t);a.add('</g></g>')
 a.path(f'M{x+20} {y+25} Q{x+w*.5} {y-12} {x+w-22} {y+22}','none','#a2b3b5',2,'opacity=".45"')
 a.path(f'M{x+w*.16} {y+10} L{x+w*.06} {y+h-10}','none','#92b2bc',2,'opacity=".11"')

def scene(t,with_caps=True):
 a=Art();begin(a);a.add('<defs><linearGradient id="citysky" x2="0" y2="1"><stop stop-color="#05111d"/><stop offset="1" stop-color="#345d6b"/></linearGradient><radialGradient id="lamphalo"><stop stop-color="#ffc476" stop-opacity=".35"/><stop offset="1" stop-color="#ffc476" stop-opacity="0"/></radialGradient></defs>')
 _,st,en,mode=shot(t)
 if mode in ['Departure','Street acceleration','Corner escape']:
  c=ext_camera(t,mode);city(a,c,t);sedan(a,c,t);rain(a,t)
  # Passing road-water contact, not a camera zoom or decorative particle layer.
  for j in range(7):
   u=(t*1.7+j*.19)%1;a.ellipse(60+j*151,1740+(j%2)*70,8+u*26,1+u*4,'none','#537984',1.2,extra=f'opacity="{.2*(1-u)}"')
 elif mode in ['Driver danger','Steering anticipation']:
  driver(a,t,front_camera(t),mirror,mode=='Steering anticipation')
 elif mode=='Pedal':pedal(a,t)
 elif mode=='Acceleration instruments':
  dashboard(a,t,True)
  # Physical cluster, one continuous needle rise, compact calibrated reveal.
  a.path('M205 806 Q540 727 866 809','none','#eead5f',2,'opacity=".6"')
  v=state(t)['speed_kmh'];a.rect(355,1373,432,4,'#263e4b');a.rect(355,1373,432*v/160,4,'#e5a552')
 elif mode=='Mirror threat':
  city(a,front_camera(t),t);a.path('M0 0 H1080 V460 Q540 360 0 460Z','#08141e',INK,8)
  mirror(a,t,(65,450,950,625),True)
  a.path('M0 1160 Q540 1020 1080 1160 V1920 H0Z','#0a1c27',INK,10)
  # Lower dash/wheel edge sets optical context; threatening reflected car is the focal action.
  a.path('M-80 1770 Q540 1170 1160 1770','none',INK,90);a.path('M-80 1770 Q540 1170 1160 1770','none','#3c5866',37)
 a.add('<rect x="0" y="0" width="1080" height="1920" fill="url(#vignette)" opacity=".70"/>')
 hud(a,t,mode)
 if with_caps:captions(a,t,CAPS,mode)
 a.add('</svg>');return ''.join(a.s)

def main():
 p=argparse.ArgumentParser();p.add_argument('--scale',type=float,default=1/3);p.add_argument('--fps',type=int,default=30);p.add_argument('--from',dest='start',type=float,default=0);p.add_argument('--to',dest='end',type=float,default=15);p.add_argument('--out',default='previews/V2_PREVIEW_01.mp4');p.add_argument('--stills',action='store_true');args=p.parse_args();out=ROOT/args.out;assert not out.exists(),out;out.parent.mkdir(parents=True,exist_ok=True)
 w=round(1080*args.scale/2)*2;h=round(1920*args.scale/2)*2;rr=Raster(w,h);num=round((args.end-args.start)*args.fps)
 proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(args.fps),'-i','pipe:0','-ss',str(args.start),'-i',str(ROOT/'audio/MIX_MASTER.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-threads','2','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t',str(args.end-args.start),'-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 try:
  for i in range(num):
   t=args.start+i/args.fps;im=rr.render(scene(t));proc.stdin.write(im.tobytes())
   if args.stills and i%15==0:im.save(ROOT/'previews'/f'{out.stem}_{i:03d}.jpg',quality=94)
   if i%60==0:print(out.name,i,num,flush=True)
 finally:proc.stdin.close()
 if proc.wait():raise RuntimeError('Encode failed')
 print('COMPLETE',out,flush=True)
if __name__=='__main__':main()
