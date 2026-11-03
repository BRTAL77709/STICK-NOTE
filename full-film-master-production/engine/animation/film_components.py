"""Reusable illustrated noir environments, witness rig, vehicles and mobile typography."""
from illustration_engine import Art,OUTLINE,ik,limb,pt,draw_head_legacy
import math,random,re
from xml.sax.saxutils import escape
NAVY='#071521';TEAL='#173844';AMBER='#efaa52';WHITE='#eeeae0'
def smooth(x):
 x=max(0,min(1,x));return x*x*x*(10+x*(-15+6*x))
def mix(a,b,u):return a+(b-a)*u
def ease(t,a,b):return smooth((t-a)/(b-a))
def text(a,x,y,s,size=50,fill=WHITE,anchor='middle',weight='bold',stroke=0):
 a.add(f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" stroke="#020910" stroke-width="{stroke}" paint-order="stroke" stroke-linejoin="round">{escape(s)}</text>')
def begin(a):
 a.add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">')
 a.add('''<defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#020a12"/><stop offset="1" stop-color="#143544"/></linearGradient><linearGradient id="road" x2=".2" y2="1"><stop stop-color="#19343e"/><stop offset="1" stop-color="#030b14"/></linearGradient><linearGradient id="face"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#9ca9af"/></linearGradient><linearGradient id="metal" x2=".2" y2="1"><stop stop-color="#2d4655"/><stop offset=".45" stop-color="#10212e"/><stop offset="1" stop-color="#050e18"/></linearGradient><linearGradient id="cloth" x2="1" y2=".3"><stop stop-color="#293944"/><stop offset=".6" stop-color="#14232e"/><stop offset="1" stop-color="#0b1620"/></linearGradient><radialGradient id="lamp"><stop stop-color="#ffc36c" stop-opacity=".34"/><stop offset="1" stop-color="#ffad4a" stop-opacity="0"/></radialGradient><radialGradient id="vignette"><stop offset=".42" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#01070d" stop-opacity=".66"/></radialGradient></defs>''')
def finish(a,t,rain=False):
 if rain:rainfall(a,t)
 a.rect(0,0,1080,1920,'url(#vignette)');a.add('</svg>');return ''.join(a.s)
def rainfall(a,t,density=170,glass=False):
 rng=random.Random(217)
 for j in range(density):
  x=rng.uniform(-40,1120);y=(rng.uniform(-200,1920)+t*(760 if not glass else 200))%2160-150
  a.path(f'M{x:.1f} {y:.1f} l-6 {34 if not glass else 58}','none','#7fa4b2',1.6,'opacity=".24"')
 if glass:
  for j in range(24):
   x=60+j*43;y=(j*137+t*90)%1900;a.ellipse(x,y,2.4,9,'#95b2be',extra='opacity=".28"')
def street(a,t,speed=80,curve=0,quiet=False,distance=None):
 motion=speed*t if distance is None else distance
 a.rect(0,0,1080,1920,'url(#sky)');a.rect(0,680,1080,1240,'url(#road)')
 rng=random.Random(77)
 for x,y,w,h in [(200,330,150,400),(360,250,130,460),(510,170,180,550),(730,350,200,390)]:
  a.rect(x,y,w,h,'#0a202e','#15323f',2)
  for yy in range(y+30,690,65):
   for xx in range(x+20,x+w-15,38):
    if rng.random()>.55:a.rect(xx,yy,12,19,'#3a4c49' if rng.random()>.3 else '#8c622f')
 for side in [-1,1]:
  a.path(f'M{540+side*58} 680 L{540+side*760} 1920','none','#35525d',5)
  for j in range(5):
   z=(j*270+100-motion)%1450;sc=700/(700+z);y=680+1170*sc;cx=540+side*(460*sc+25);w=310*sc;h=370*sc
   a.rect(cx-w/2,y-h,w,h,'#102735','#344e5a',3)
   a.poly([(cx-w*.57,y-h),(cx,y-h-85*sc),(cx+w*.57,y-h)],'#0b1b29','#3d5662',3)
   a.rect(cx-w*.34,y-h*.65,w*.22,h*.24,'#b87c3d' if j%3==0 else '#213e4c','#06131f',3)
   a.rect(cx+w*.13,y-h*.65,w*.22,h*.24,'#203b49','#06131f',3)
   a.rect(cx-w*.12,y-h*.34,w*.24,h*.34,'#081822','#3d5360',3)
   lx=cx-side*w*.57;ly=y-h*.78
   a.path(f'M{lx} {y} L{lx} {ly} q{-side*12*sc} {-25*sc} {-side*48*sc} {-22*sc}','none','#07131d',8*sc)
   a.ellipse(lx-side*42*sc,ly-20*sc,21*sc,8*sc,'#ffc36b')
   a.ellipse(lx-side*42*sc,ly-20*sc,130*sc,190*sc,'url(#lamp)')
   for k in range(8):
    yy=y+k*16*sc;a.line([(lx-30*sc,yy),(lx+(35+12*math.sin(k+t))*sc,yy)],'#6d563a',2*sc)
 for j in range(12):
  z=(j*150-motion)%1800;sc=700/(700+z);y=680+1170*sc;dx=curve*sc*sc
  a.line([(540+dx,y),(540+dx,y+40*sc)],'#81938e',5*sc)
 for j in range(22):
  x=70+j*47;y=1070+(j%7)*105;u=(t*.8+j*.19)%1;a.ellipse(x,y,5+u*20,1+u*4,'none','#4d7380',1.1,extra=f'opacity="{.30*(1-u)}"')
def road_point(x,z,h=0):
 sc=700/(700+max(-200,z));return 540+x*sc,680+1170*sc-h*sc,sc

def car_sprite(a,cx,cy,scale=1,color='black',view='rear',distance=0,steer=0):
 body='#3b596c' if color=='blue' else '#0d1d29';rim='#718b99' if color=='blue' else '#405966';roll=steer*7;bounce=1.5*math.sin(distance*.08)
 a.ellipse(cx,cy+11*scale,160*scale,22*scale,'#02090e',extra='opacity=".8"')
 a.add(f'<g transform="translate({cx} {cy+bounce*scale}) rotate({roll}) scale({scale})">')
 for x,y in [(-112,-20),(112,-20)]:
  a.ellipse(x,y,27,47,'#030a11','#354b57',4);a.ellipse(x,y,15,29,'#253c49',OUTLINE,3)
  phase=distance/26
  for j in range(6):
   th=phase+j*math.pi/3;a.line([(x,y),(x+13*math.cos(th),y+25*math.sin(th))],'#7c929c',2)
 a.path('M-143 -34 L-133 -109 L-92 -174 Q-75 -197 -35 -198 L49 -198 Q86 -190 104 -165 L138 -109 L150 -24 Q10 20 -143 -12Z',body,OUTLINE,7)
 a.path('M-101 -111 L-76 -167 Q-64 -180 -34 -180 L44 -180 Q68 -176 81 -161 L112 -110Z','#081720',rim,4)
 a.line([(-25,-180),(-26,-111)],'#2a4454',4)
 a.path('M-128 -98 Q10 -74 137 -99 L141 -33 Q-9 4 -135 -23Z',body,rim,3)
 if view=='rear':
  a.poly([(-127,-77),(-66,-69),(-59,-52),(-127,-59)],'#ee514c','#65252c',3);a.poly([(67,-69),(132,-80),(133,-62),(67,-52)],'#f26050','#65252c',3)
  a.rect(-30,-39,60,20,'#9aa6a4',OUTLINE,3,2);a.line([(-112,-65),(-71,-59)],'#ffb18e',2)
 else:
  for x in [-93,93]:
   a.path(f'M{x-28} -72 L{x+25} -70 L{x+28} -48 L{x-29} -51Z','#d9edf4','#344956',3)
   a.ellipse(x,-59,40,25,'#b5e3f0',extra='opacity=".10"')
  a.path('M-58 -49 Q0 -39 58 -49 L53 -23 L-51 -23Z','#050e17','#45616f',3)
 a.path('M-135 -11 Q0 22 144 -12','none',rim,4);a.line([(-116,-103),(118,-102)],'#526b79',2);a.add('</g>')
 # Restrained wet-road light reflections follow the actual car position.
 for j in range(7):
  y=cy+(22+j*14)*scale;w=(15+j*4)*scale
  for side in [-1,1]:a.line([(cx+side*95*scale-w,y),(cx+side*95*scale+w,y)],'#703a39' if view=='rear' else '#516f7d',2*scale)

def witness_head(a,x,y,t,emotion='neutral',yaw=0,scale=1):
 a.add(f'<g transform="translate({x} {y}) scale({scale}) rotate({-5*yaw})">')
 a.ellipse(0,0,61,66,'url(#face)',OUTLINE,6)
 a.path('M-61 -12 Q-62 -78 -2 -80 Q56 -76 61 -16Z','#132735','#6b8795',2)
 a.path('M-66 -17 Q0 -40 70 -15 L82 1 Q18 -8 -64 3Z','#0b1d2a',OUTLINE,5)
 a.path('M-61 -24 Q-57 -60 -36 -70','none','#d4a35c',3)
 shift=10*yaw;shock=1 if emotion in ['shocked','panic'] else 0;worry=1 if emotion in ['worried','panic'] else 0
 for ex in [-21,20]:
  a.ellipse(ex+shift,18,4.5,10+4*shock,'#07111a')
  a.path(f'M{ex-10} {1+5*worry} l20 {-3 if ex<0 else 3}','none','#1b2931',3)
 if shock:a.ellipse(4,48,10,13,'#1c2930',OUTLINE,2)
 else:a.path('M-9 48 q12 -6 23 0','none','#25323a',3)
 if worry:a.path('M-42 25 q-8 10 -2 16 q8 2 2 -16Z','#6c9fad','#315c71',1)
 a.add('</g>')

def witness_body(a,x,ground,t,mode='stand',progress=0,emotion='worried',hand_target=None,scale=1,phase=0,floor_slope=0,head_yaw=None):
 a.add(f'<g transform="translate({x} {ground}) scale({scale})">')
 # Local articulated body. Running uses world-locked foot anchors supplied below.
 hip=(0,(-140 if mode=='run' else -159)+4*math.sin(t*3));sh=(12 if mode=='run' else -4,hip[1]-125)
 feet=[(-23,0),(24,0)]
 if mode=='run':
  # Explicit half-cycle stance locks in the character's world track.
  stride=48. if abs(floor_slope)>.7 else 112.;speed=progress;root=speed
  for j in (0,1):
   q=phase+j*.5;step=math.floor(q);u=q-step;anchor=step*stride
   if u<.62:fx=anchor-root;fy=0
   else:
    v=(u-.62)/.38;fx=mix(anchor,anchor+stride,smooth(v))-root;fy=-30*math.sin(math.pi*v)
   feet[j]=(fx,fy+floor_slope*fx)
   if abs(floor_slope)>.7:
    base=-56*step
    stair=base if u<.62 else mix(base,base-56,smooth((u-.62)/.38))-30*math.sin(math.pi*(u-.62)/.38)
    feet[j]=(fx,stair-floor_slope*root)
 for j,f in enumerate(feet):
  h=(hip[0]+(-15 if j==0 else 17),hip[1]);ank=(f[0],f[1]-10);k=ik(h,ank,85,85,-1)
  limb(a,[h,k,ank],'#182d39' if j==0 else '#29424e',28)
  a.path(f'M{f[0]-19} {f[1]-9} Q{f[0]+7} {f[1]-20} {f[0]+31} {f[1]-3} L{f[0]+32} {f[1]+7} L{f[0]-20} {f[1]+7}Z','#10222f',OUTLINE,5)
 sx,sy=sh;hx,hy=hip
 a.path(f'M{sx-44} {sy-8} Q{sx-60} {sy+14} {hx-45} {hy+15} Q{hx} {hy+30} {hx+48} {hy+12} L{sx+45} {sy+7} Q{sx+27} {sy-19} {sx-44} {sy-8}Z','url(#cloth)',OUTLINE,7)
 a.path(f'M{sx-30} {sy+15} L{hx-27} {hy+10} M{sx+20} {sy+20} L{hx+25} {hy+7}','none','#3a5360',2)
 a.path(f'M{sx-35} {sy-12} Q{sx} {sy+35} {sx+36} {sy-12} L{sx+20} {sy-32} L{sx-22} {sy-32}Z','#0b1a27',OUTLINE,5)
 a.line([(sx-13,sy+8),(sx-15,sy+45)],'#60747d',2);a.line([(sx+14,sy+8),(sx+16,sy+46)],'#60747d',2)
 for j in (0,1):
  ss=(sx+(-35 if j==0 else 35),sy+14)
  if hand_target is not None and j==1:hand=hand_target
  elif mode=='run':hand=(sx+(-55 if j==0 else 55)+25*math.sin(phase*math.tau+j*math.pi),sy+60+25*math.cos(phase*math.tau+j*math.pi))
  else:hand=(hx+(-43 if j==0 else 45),hy-10)
  el=ik(ss,hand,90,87,1 if j==0 else -1);limb(a,[ss,el,hand],'#203947',26);a.ellipse(*hand,14,17,'#d4d7cf',OUTLINE,4)
 witness_head(a,sx+2,sy-72,t,emotion,math.sin(t*.7)*.15 if head_yaw is None else head_yaw);a.add('</g>')

def interior_car(a,t,emotion='neutral',speed=50,look=0,distance=None):
 street(a,t,speed,distance=distance);a.add('<defs><clipPath id="windshield"><path d="M75 285 Q540 120 1000 285 L1035 1230 L40 1230Z"/></clipPath></defs>')
 a.poly([(0,0),(1080,0),(1080,330),(980,260),(85,260),(0,340)],'#06111b',w=0)
 a.path('M72 275 L16 1420 M1001 275 L1065 1420','none','#030b13',45);a.path('M82 275 L40 1370 M990 275 L1040 1370','none','#344d5c',6)
 # Dashboard, seat, torso and steering wheel; head and hands react independently.
 a.path('M0 1200 Q540 1110 1080 1200 L1080 1920 L0 1920Z','#091924',OUTLINE,8)
 bob=2*math.sin(t*5);a.path(f'M239 1090 Q260 952 434 970 L650 985 Q777 1050 800 1355 L247 1370Z','url(#cloth)',OUTLINE,8)
 a.path('M350 1070 L380 1260 M632 1063 L615 1260','none','#3e5662',4)
 witness_head(a,520+look*12,787+bob,t,emotion,look,2.5)
 # Grip anchors stay on the rotating steering rim.
 angle=.11*math.sin(t*1.5)+look*.18;cx,cy=535,1265
 a.ellipse(cx,cy,215,142,'none',OUTLINE,29);a.ellipse(cx,cy,215,142,'none','#314b5b',13)
 for j in (0,1):
  th=(math.pi*.88 if j==0 else math.pi*.12)+angle;hand=(cx+205*math.cos(th),cy-135*math.sin(th));ss=(290 if j==0 else 745,1110)
  el=ik(ss,hand,155,155,1 if j==0 else -1);limb(a,[ss,el,hand],'#203a49',48);a.ellipse(*hand,30,37,'#c5cfca',OUTLINE,6)
 a.line([(cx,cy),(cx-120*math.cos(angle),cy-60*math.sin(angle))],'#203a4c',18)
 text(a,900,1460,'2:17',32,'#7aa3b5')
 # Wiper pivots sweep actual arcs across the glass.
 th=-.8+1.1*math.sin(t*2.4);a.line([(170,1160),(170+650*math.cos(th),1160-650*math.sin(th))],'#03101a',13)
 rainfall(a,t,110,True)
 # Rearview mirror establishes headlights behind the witness.
 a.rect(430,262,270,105,'#07111c','#4e6673',7,18)
 if emotion in ['panic','worried']:
  for x in [505,625]:a.ellipse(x,318,17,13,'#d8eff5')


def house(a,t,door_open=0,interior=False):
 if not interior:
  a.rect(0,0,1080,1920,'#061521');a.rect(0,1430,1080,490,'url(#road)')
  a.poly([(75,1430),(75,480),(540,250),(1008,480),(1008,1430)],'#17303e','#06121d',9)
  a.poly([(30,490),(540,210),(1050,490),(1010,550),(540,305),(70,550)],'#0b1c2a','#4a626e',6)
  for y in range(560,1420,74):a.line([(80,y),(1000,y)],'#29424e',2)
  for x in [180,770]:
   a.rect(x,640,150,230,'#0a1c2a','#667b85',7);a.line([(x+75,645),(x+75,865)],'#546e7c',5);a.line([(x,755),(x+150,755)],'#546e7c',5)
  a.rect(430,835,285,595,'#05111b','#66808b',10)
  a.rect(454,860,237,560,'#263a43','#0b1824',6)
  a.rect(477,900,190,185,'#1b303d','#526977',3);a.rect(477,1125,190,250,'#1b303d','#526977',3)
  text(a,574,807,'17',76,AMBER,stroke=3)
  if door_open:
   a.rect(442,850,268,576,'#02080f');w=237*(1-.87*door_open);a.poly([(454,860),(454+w,860+25*door_open),(454+w,1420-15*door_open),(454,1420)],'#263b47','#6a8089',6)
  a.ellipse(655,1172,16,18,'#b38c54',OUTLINE,4)
  a.rect(732,876,46,80,'#f3b25d','#4b412b',4,7);a.ellipse(755,928,210,350,'url(#lamp)')
  for j in range(3):a.poly([(405-j*27,1432+j*40),(737+j*27,1432+j*40),(760+j*29,1472+j*40),(382-j*29,1472+j*40)],'#233f4b','#48626b',3)
  for x in [85,940]:
   for j in range(9):a.ellipse(x+25*math.sin(j*2),1400-j*25,30,37,'#102d31','#243c39',2)
 else:
  a.rect(0,0,1080,1920,'#102632');a.rect(0,1460,1080,460,'#162e3c')
  for x in [180,460,740]:a.line([(x,0),(x,1440)],'#29424c',3)
  a.rect(250,370,580,1080,'#06141f','#6e8087',12);a.rect(278,398,524,1025,'#213541','#0b1924',7)
  a.rect(325,460,430,360,'#19313e','#526671',4);a.rect(325,875,430,475,'#19313e','#526671',4)
  a.ellipse(735,952,25,26,'#bb975e',OUTLINE,4);a.rect(691,1040,72,25,'#a28250',OUTLINE,4,6)
  a.rect(65,500,68,130,'#d9a45e','#4c4432',6,9);a.ellipse(99,574,330,500,'url(#lamp)')
  for j in range(10):a.line([(0,1540+j*37),(1080,1540+j*37)],'#233c4b',2)


def phone(a,x,y,t,mode='ring',scale=1,amount=False):
 a.add(f'<g transform="translate({x} {y}) rotate({2*math.sin(t*65) if mode=="ring" else -7}) scale({scale})">')
 a.rect(-165,-310,330,620,'#020a12','#8b9ba0',8,42);a.rect(-143,-270,286,540,'#102b3d','#2c5064',3,18);a.rect(-52,-290,104,15,'#000',rx=7)
 text(a,0,-160,'UNKNOWN',28);text(a,0,-117,'CALLER',28)
 if amount:
  text(a,0,-15,'$1,000,000',34,'#c6e6ef');text(a,0,40,'FOR YOUR SILENCE',21,'#e8c58c')
 else:text(a,0,10,'PRIVATE NUMBER',19,'#789eaf')
 if mode=='ring':
  for xx,col,lab in [(-78,'#a62b36','×'),(78,'#20804c','✓')]:a.ellipse(xx,180,42,42,col,'#07121a',3);text(a,xx,193,lab,36)
 else:text(a,0,190,'CONNECTED',24,'#67b9a0')
 a.add('</g>')

def room(a,t):
 a.rect(0,0,1080,1920,'#102532');a.rect(0,1430,1080,490,'#0a1d2b');a.line([(0,1430),(1080,1430)],'#324a56',6)
 a.rect(650,230,330,700,'#030d17','#71828a',12);a.rect(673,253,284,651,'#0a2031','#19384d',3)
 for j in range(30):
  x=680+(j*29)%270;y=260+(j*97+t*90)%630;a.line([(x,y),(x-5,y+36)],'#648c9f',1.4)
 a.line([(814,250),(814,905)],'#4d6b7d',9);a.line([(672,565),(959,565)],'#4d6b7d',9)
 a.path('M600 170 L660 185 L687 1070 Q622 1115 590 1060Z','#24404d','#091b29',6)
 a.rect(70,1050,200,390,'#172d3c','#415865',4,9);a.line([(95,1180),(246,1180)],'#0b1c29',4)
 a.line([(160,1050),(160,780)],'#785d3e',11);a.poly([(85,770),(235,770),(280,945),(39,945)],'#dfad6c','#59472e',5);a.ellipse(160,940,340,450,'url(#lamp)')
 a.path('M420 1450 Q650 1270 1080 1370 L1080 1880 L430 1880Z','#1b3545','#0b1925',8)
 a.path('M590 1455 Q788 1360 1080 1418','none','#3c5261',6)
