"""V6 projected-head and uneven-load acting revision. Reuses the existing illustrated assets, constrained rigs and SVG renderer."""
import math,random,ctypes as C,ctypes.util,subprocess,argparse,json,wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUTLINE='#030b12'
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,t):return a+(b-a)*t
def pt(p):return f'{p[0]:.2f},{p[1]:.2f}'
class Art:
 def __init__(self):self.s=[]
 def add(self,s):self.s.append(s)
 def path(self,d,fill='none',stroke=OUTLINE,w=5,extra=''):
  self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
 def poly(self,ps,fill,stroke=OUTLINE,w=5):self.add(f'<polygon points="{" ".join(pt(p) for p in ps)}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>')
 def line(self,ps,color,w):self.path('M'+' L'.join(pt(p) for p in ps),'none',color,w)
 def ellipse(self,x,y,rx,ry,fill,stroke='none',w=3,extra=''):self.add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>')
 def rect(self,x,y,w,h,fill,stroke='none',sw=3,rx=0):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def ik(a,b,l1,l2,side=1):
 dx,dy=b[0]-a[0],b[1]-a[1];d=max(.001,math.hypot(dx,dy));q=min(d,l1+l2-.001)
 if d>l1+l2+.02:raise ValueError(f'Unreachable IK: {d} > {l1+l2}')
 along=(l1*l1-l2*l2+q*q)/(2*q);height=math.sqrt(max(0,l1*l1-along*along));ux,uy=dx/d,dy/d
 return (a[0]+ux*along-side*uy*height,a[1]+uy*along+side*ux*height)
def limb(a,points,color,width,tag=''):
 if tag:a.add(f'<g id="{tag}" data-joints="{";".join(pt(p) for p in points)}">')
 a.line(points,OUTLINE,width+9);a.line(points,color,width)
 # restrained top-edge cel highlight, preserving continuous joint contour
 a.line([(x-3,y-3) for x,y in points], '#64818c' if color!='#bdc0bf' else '#e4dfd3',2.5)
 if tag:a.add('</g>')

# World units match the 1080-wide SVG. No camera transform enters choreography.
STRIDE=100.0
TRAVEL=300.0
BASES=(100.0,520.0)
GROUND=(1384.,1404.)
VICTIM_X=300.0

def travel(t):
 # Establish .00-.45; anticipation .45-.90; drag .90-2.70; decelerate 2.70-3.20.
 u=max(0.,min(2.3,t-.9));acc=.2;dec=.5;v=TRAVEL/(2.3-(acc+dec)/2)
 if u<acc:return .5*v/acc*u*u
 if u>2.3-dec:return TRAVEL-.5*v/dec*(2.3-u)**2
 return v*(u-acc/2)

def reaction(t):return smooth((t-3.35)/.65)

def preparation(t):
 return smooth((t-.45)/.45)*(1-smooth((t-.9)/.25))

def posture(t,who):
 phase=travel(t)/STRIDE+(who-1)*.12
 activity=smooth((t-.9)/.2)*(1-smooth((t-2.7)/.5))
 load=math.cos(phase*2*math.pi)
 # Hip drop and shoulder bracing precede the pull, then transfer between stance feet.
 lean=-18-12*preparation(t)-5*load*activity
 bob=16*preparation(t)+2.5*math.cos(phase*4*math.pi)*activity-1.2*impulse(t,(who-1)*.06)
 tau=max(0,t-3.2)
 if t>=3.2:bob+=2.8*math.sin(tau*11)*math.exp(-tau*7)+.6*math.sin(tau*3)
 return lean,bob

def hip_shift(t,actor):
 act=smooth((t-.9)/.2)*(1-smooth((t-2.7)/.5))
 return -6*math.cos((travel(t)/STRIDE+actor*.12)*2*math.pi)*act

def inverse_travel(distance):
 lo,hi=.9,3.2
 for _ in range(32):
  mid=(lo+hi)/2
  if travel(mid)<distance:lo=mid
  else:hi=mid
 return (lo+hi)/2

PULL_TIMES=tuple(inverse_travel(d) for d in (50,150,250))
CATCH_TIMES=tuple(inverse_travel(d)+.13 for d in (75,210))

def impulse(t,delay=0):
 return sum(math.exp(-((t-at-delay)/.11)**2) for at in PULL_TIMES)

def catches(t,leg=0):
 return sum((12 if leg==0 else 4)*math.exp(-((t-at-(.025 if leg else 0))/.09)**2) for at in CATCH_TIMES)

def upper_arm_targets(t):
 vx=VICTIM_X+travel(max(0,t-.055))+2.0*impulse(t)
 vy=1156-5*impulse(t)+3*preparation(t)
 shoulders=[(vx-39,vy+5),(vx+35,vy+7)]
 elbows=[(vx-84,vy+68),(vx+84,vy+68)]
 grips=[tuple(mix(sh[j],el[j],.53) for j in (0,1)) for sh,el in zip(shoulders,elbows)]
 return vx,vy,shoulders,elbows,grips

def victim_weight(t):
 # Suspended upper body responds first; pelvis and heels follow with inertia.
 pelvis=(VICTIM_X+travel(max(0,t-.14))-32+2*impulse(t,.12)-.25*catches(t-.04),1156+143-3*impulse(t,.12)+.15*catches(t-.04)+2*preparation(t))
 heels=[(VICTIM_X+travel(max(0,t-.13))-145+j*30-catches(t,j),1413+j*5) for j in (0,1)]
 head_roll=27
 for at in PULL_TIMES:
  u=t-at-.12
  if u>0:head_roll+=17*math.exp(-8*u)*math.sin(13*u)
 return pelvis,heels,head_roll

def foot_state(t,actor,leg):
 phase=.12*actor;off=(0 if leg==0 else .5)+phase
 base=BASES[actor]+(-35 if leg==0 else 50)+phase*STRIDE
 return foot(travel(t),off,base,GROUND[actor])

def foot(d,offset,x,y):
 v=d/STRIDE+offset;n=math.floor(v);f=v-n
 sx=x+(n-offset)*STRIDE+20
 if f>.70:
  u=(f-.70)/.30;sx+=STRIDE*smooth(u);y-=31*math.sin(math.pi*u)
 return sx,y,f

def draw_head_legacy(a,hx,hy,t,who):
  sx=hx-2;sy=hy+72
  hx=sx+2;hy=sy-72;turn=reaction(t) if who==1 else 0
  narrow=smooth((t-3.9)/.55) if who==1 else 0
  a.add(f'<g id="head-{who}" data-turn="{turn}" data-narrow="{narrow}" transform="translate({-8*turn},0) rotate({-20+20*turn if who==1 else 5} {hx} {hy})">')
  a.ellipse(hx,hy,61,65,'#06121d',OUTLINE,6)
  # pale eye opening becomes broader as criminal 01 looks at camera
  eyeW=mix(34,49,turn);eyeX=hx+mix(21,-2,turn)
  a.path(f'M{eyeX-eyeW},{hy-4} Q{eyeX},{hy-17} {eyeX+eyeW},{hy-6} L{eyeX+eyeW-5},{hy+16} Q{eyeX},{hy+30} {eyeX-eyeW+4},{hy+11}Z','url(#face)',OUTLINE,3)
  for ex in [mix(hx+16,hx-20,turn),mix(hx+42,hx+20,turn)]:
   a.ellipse(ex,hy+5,4,10,'#03090f')
  if narrow>0:
   a.path(f'M{eyeX-eyeW},{hy-7} Q{eyeX-20},{hy-13} {eyeX},{hy-6+12*narrow} Q{eyeX+20},{hy-13} {eyeX+eyeW},{hy-7} L{eyeX+eyeW},{hy-19} L{eyeX-eyeW},{hy-21}Z','#0b1721',OUTLINE,2)
  a.path(f'M{hx-53},{hy+15} Q{hx+7},{hy+33} {hx+54},{hy+16} Q{hx+46},{hy+65} {hx},{hy+66} Q{hx-46},{hy+54} {hx-53},{hy+15}Z','#0b1721',OUTLINE,4)
  a.path(f'M{hx-33},{hy+37} Q{hx},{hy+49} {hx+28},{hy+38}','none','#263946',2)
  a.path(f'M{hx-60},{hy-14} Q{hx-58},{hy-78} {hx-1},{hy-79} Q{hx+53},{hy-75} {hx+58},{hy-15}Z','#142532','#6c8994',2)
  if who==1:
   a.path(f'M{hx-66},{hy-17} Q{hx+5},{hy-34} {hx+70},{hy-12} L{hx+76},{hy+1} Q{hx+21},{hy-3} {hx-64},{hy+2}Z','#091923',OUTLINE,5)
   a.path(f'M{hx+mix(25,0,turn)},{hy-73} Q{hx+mix(42,1,turn)},{hy-45} {hx+mix(35,0,turn)},{hy-26}','none','#354956',2)
   a.path(f'M{hx-62},{hy-22} Q{hx-61},{hy-58} {hx-37},{hy-68}','none','#ecab54',3)
  else:
   a.path(f'M{hx-61},{hy-23} Q{hx},{hy-40} {hx+60},{hy-20} L{hx+61},{hy-4} Q{hx},{hy-18} {hx-61},{hy-5}Z','#102331',OUTLINE,4)
   for q in range(-45,50,13):a.line([(hx+q,hy-29),(hx+q+1,hy-10)],'#304756',1.5)
  a.add('</g>')

def hull(points):
 pts=sorted(set((round(x,5),round(y,5)) for x,y in points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[];upper=[]
 for q in pts:
  while len(lower)>1 and cross(lower[-2],lower[-1],q)<=0:lower.pop()
  lower.append(q)
 for q in reversed(pts):
  while len(upper)>1 and cross(upper[-2],upper[-1],q)<=0:upper.pop()
  upper.append(q)
 return lower[:-1]+upper[:-1]

def curved_outline(a,points,fill,stroke=OUTLINE,width=4):
 n=len(points);d='M'+pt(points[0])
 for j in range(n):
  p0,p1,p2,p3=points[(j-1)%n],points[j],points[(j+1)%n],points[(j+2)%n]
  c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
  c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
  d+=' C'+pt(c1)+' '+pt(c2)+' '+pt(p2)
 a.path(d+'Z',fill,stroke,width)

def draw_head(a,hx,hy,t,who,hide_eyes=False):
 if who==2:return draw_head_legacy(a,hx,hy,t,who)
 turn=reaction(t);theta=math.radians(72*(1-turn));narrow=smooth((t-4)/.5)
 c,ss=math.cos(theta),math.sin(theta)
 def project(x,y,z):
  depth=-x*ss+z*c
  return hx+x*c+z*ss,hy+y+.16*depth
 def surface(y,lon,mask=False):
  lat=math.asin(max(-.9999,min(.9999,y/65)));q=math.cos(lat);l=math.radians(lon)
  z=54*q*math.cos(l)
  if mask:z+=8*q*max(0,math.cos(l))
  return project(61*q*math.sin(l),y,z)
 def visible_span(lo,hi):
  angle=math.degrees(theta)
  return max(lo,-angle-89.8),min(hi,-angle+89.8)
 def patch(lo,hi,top,bottom,mask=False):
  lo,hi=visible_span(lo,hi)
  if lo>=hi:return []
  ls=[mix(lo,hi,i/32) for i in range(33)]
  return ([surface(top(l),l,mask) for l in ls]
   +[surface(mix(top(hi),bottom(hi),j/16),hi,mask) for j in range(1,16)]
   +[surface(bottom(l),l,mask) for l in reversed(ls)]
   +[surface(mix(bottom(lo),top(lo),j/16),lo,mask) for j in range(1,16)])
 bill3=[(-68,-20,12),(-75,-20,45),(-55,-20,99),(0,-20,114),(55,-20,99),(75,-20,45),(68,-20,12),(0,-20,-3)]
 bill=[project(*q) for q in bill3]
 rx=math.sqrt((61*c)**2+(54*ss)**2)
 chin=surface(61,0,True)[0]-hx
 a.add(f'<g id="head-1" data-turn="{turn}" data-yaw="{math.degrees(theta)}" data-head-rx="{rx}" data-bill="{max(x for x,y in bill)-hx}" data-mask-chin="{chin}" data-narrow="{narrow}">')
 # Parent neck turns under the jaw; the chest/shoulder frame stays planted.
 neck=[project(-19,54,6),project(19,54,6),project(18,81,3),project(-20,78,3)]
 a.poly(neck,'#0b1721',OUTLINE,3)
 a.line([project(9,59,18),project(8,78,15)],'#34505b',2)
 a.ellipse(hx,hy,rx,65,'#06121d',OUTLINE,6)
 mask=patch(-180,180,lambda l:14,lambda l:64,True)
 a.poly(mask,'#0b1721',OUTLINE,3.5)
 # Curved eye opening and irises project on the head surface, not a sliding 2D face.
 top=lambda l:-8+8*narrow*(1-abs(l)/54)
 bottom=lambda l:17-5*narrow
 eye=patch(-54,54,top,bottom)
 if not hide_eyes:
  a.poly(eye,'url(#face)',OUTLINE,2)
  d='M'+' L'.join(pt(q) for q in eye)+'Z'
  a.add(f'<defs><clipPath id="eye-window-1"><path d="{d}"/></clipPath></defs><g clip-path="url(#eye-window-1)">')
  for center in [-20,20]:
   if math.cos(math.radians(center)+theta)<.015:continue
   pupil=[surface(4+(9-3*narrow)*math.cos(j*math.pi/12),center+4*math.sin(j*math.pi/12)) for j in range(24)]
   a.poly(pupil,'#03090f','none',0)
  a.poly(patch(-7,7,lambda l:-14,lambda l:25,True),'#0b1721','none',0)
  if narrow>0:
   for lo,hi in [(-46,-9),(9,46)]:
    points=[surface(-7+7*narrow*(1-abs(mix(lo,hi,j/10))/46),mix(lo,hi,j/10),True) for j in range(11)]
    a.line(points,'#030b12',3)
  a.add('</g>')
 # Small cloth fold on the curved mask, not a mouth or smile.
 lo,hi=visible_span(-40,40)
 fold=[surface(38+3*math.cos(math.radians(l*2)),l,True) for l in [mix(lo,hi,j/20) for j in range(21)]]
 a.line(fold,'#263946',2)
 # Cap dome silhouette is the hull of a rotated ellipsoidal shell.
 dome=[]
 for lat in range(-90,1,6):
  q=math.cos(math.radians(lat));yy=-15+65*math.sin(math.radians(lat))
  for lon in range(-180,180,6):
   l=math.radians(lon);dome.append(project(63*q*math.sin(l),yy,55*q*math.cos(l)-10))
 curved_outline(a,hull(dome),'#142532','#6c8994',2)
 lo,hi=visible_span(-180,180)
 ls=[mix(lo,hi,j/40) for j in range(41)]
 band=[project(63*math.sin(math.radians(l)),-18,55*math.cos(math.radians(l))-10) for l in ls]
 band+=[project(63*math.sin(math.radians(l)),-4,55*math.cos(math.radians(l))-10) for l in reversed(ls)]
 a.poly(band,'#102331',OUTLINE,3)
 # Cap panel seams stay fixed in 3D while the whole cap turns.
 for lon in [-32,32]:
  if math.cos(math.radians(lon)+theta)<0:continue
  seam=[]
  for lat in range(-78,-9,5):
   q=math.cos(math.radians(lat));l=math.radians(lon)
   seam.append(project(63*q*math.sin(l),-15+65*math.sin(math.radians(lat)),55*q*math.cos(l)-10))
  a.line(seam,'#354956',1.6)
 # The same rigid visor changes direction and foreshortening through yaw.
 curved_outline(a,[(x,y+4) for x,y in bill],'#030b12',OUTLINE,4)
 curved_outline(a,bill,'#0d1e29',OUTLINE,4)
 a.line(bill[:4],'#304956',1.2)
 # Consistent amber rim on the lit contour; no photorealistic lighting.
 rim=[project(-63*math.cos(math.radians(lat)),-15+65*math.sin(math.radians(lat)),-10) for lat in range(-62,-12,6)]
 a.line(rim,'#d29b50',2.5)
 a.add('</g>')

def scene(t,hide_eyes=False):
 a=Art();rng=random.Random(717)
 a.add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">')
 a.add('''<defs>
 <linearGradient id="sky" x2="0" y2="1"><stop stop-color="#020a12"/><stop offset="1" stop-color="#153443"/></linearGradient>
 <linearGradient id="road" x2="0.25" y2="1"><stop stop-color="#142c34"/><stop offset="1" stop-color="#040d16"/></linearGradient>
 <linearGradient id="metal" x2="0.2" y2="1"><stop stop-color="#29414c"/><stop offset=".3" stop-color="#101e2a"/><stop offset="1" stop-color="#040c14"/></linearGradient>
 <linearGradient id="cloth" x2="1" y2=".3"><stop stop-color="#253540"/><stop offset=".55" stop-color="#14222d"/><stop offset="1" stop-color="#0b151e"/></linearGradient>
 <linearGradient id="face" x2="1" y2="1"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#9ca9af"/></linearGradient>
 <radialGradient id="lamp"><stop stop-color="#ffb254" stop-opacity=".4"/><stop offset="1" stop-color="#ff9c37" stop-opacity="0"/></radialGradient>
 <radialGradient id="vignette"><stop offset=".4" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#01070e" stop-opacity=".72"/></radialGradient>
 </defs>''')
 a.rect(0,0,1080,1920,'url(#sky)')
 if t<3.2:
  scale=1.08;tx=0;ty=-250
 else:
  push=smooth((t-3.2)/1.8);scale=5.1+.18*push
  cam_final=TRAVEL*.28+8
  focus_x=BASES[0]+TRAVEL-18+2
  target_x=mix(430,520,reaction(t));tx=target_x-scale*(focus_x-cam_final);ty=900-scale*(GROUND[0]-356)
 a.add(f'<g id="cinematic-framing" data-shot="{1 if t<3.2 else 2}" transform="translate({tx},{ty}) scale({scale})">')
 cam=travel(t)*.28+8*smooth(t/.8)
 a.add(f'<g id="world-camera" transform="translate({-cam},0)">')
 a.add(f'<g id="far-city" transform="translate({cam*.7},0)">')
 for x,y,w,h in [(370,310,110,590),(490,190,115,720),(625,350,130,560),(780,280,180,650)]:
  a.rect(x,y,w,h,'#0a1c2b','#1a3543',2)
  for yy in range(y+35,y+h,57):
   for xx in range(x+15,x+w-12,32):
    if rng.random()>.4:a.rect(xx,yy,11,22,'#344744' if rng.random()>.3 else '#97632d')
 a.add('</g>')
 a.poly([(0,900),(530,845),(1080,960),(1080,1920),(0,1920)],'url(#road)',w=0)
 # illustrated masonry, layers converge toward vanishing point
 a.add(f'<g id="alley-walls" transform="translate({cam*.1},0)">')
 a.poly([(0,0),(300,0),(430,860),(0,1120)],'#102331','#020b13',6)
 a.poly([(0,0),(105,0),(190,1020),(0,1120)],'#081722',w=0)
 a.poly([(1080,0),(850,0),(700,865),(1080,1090)],'#142b36','#020b13',6)
 for y in range(95,1130,55):
  end=300+min(y,860)*.15
  a.line([(0,y),(end,y*.78+70)],'#29404a',2)
  for x in range(30,360,85):
   if x<end:a.line([(x,y-30),(x+8,y+10)],'#203642',2)
 for y in range(120,1000,60):a.line([(780,y),(1100,y+50)],'#31434a',2)
 a.poly([(72,340),(237,385),(270,918),(100,987)],'#06121b','#41606b',4)
 for x in [110,142,174,206]:a.line([(x,400),(x+33,931)],'#1b313e',4)
 a.line([(30,90),(40,810),(71,860),(85,1035)],'#06111a',20)
 a.line([(28,90),(38,810),(69,860)],'#3b5159',4)
 # door and barrel / refuse anchor the perspective
 a.poly([(869,470),(1040,400),(1040,1080),(804,990)],'#07141e','#3c535b',5)
 a.poly([(895,507),(1014,460),(1014,1017),(844,964)],'#142831','#07111a',4)
 a.line([(903,550),(1000,516)],'#29434e',3)
 a.ellipse(989,781,6,10,'#a77d41')
 a.rect(112,1030,169,161,'#11272b',OUTLINE,5,8);a.rect(101,1014,187,29,'#30423e',OUTLINE,5,7)
 for y in [1080,1140]:a.line([(116,y),(275,y)],'#3f5146',4)
 a.path('M0 1225 Q85 1120 154 1210 Q190 1250 125 1280 L0 1300Z','#07111a')
 # Illustrated service placard and fire escape; unchanged character designs.
 a.poly([(876,605),(970,570),(970,674),(851,710)],'#1b333e','#4d6266',3)
 a.add('<text x="884" y="635" fill="#c9b88a" font-size="18" font-family="DejaVu Sans" transform="rotate(-12 884 635)">SERVICE</text>')
 a.add('<text x="885" y="664" fill="#e2c18a" font-size="19" font-family="DejaVu Sans" transform="rotate(-12 885 664)">BAY 04</text>')
 for yy in [210,340]:
  a.line([(800,yy),(1060,yy-45)],'#06121b',13)
  a.line([(804,yy+6),(1057,yy-39)],'#40515a',3)
  for xx in range(830,1060,33):a.line([(xx,yy-60),(xx,yy-5-(xx-800)*.17)],'#263f4b',4)
 a.line([(848,218),(848,530)],'#132b37',9);a.line([(875,215),(875,519)],'#132b37',9)
 for yy in range(245,520,29):a.line([(848,yy),(875,yy-5)],'#4a5b61',3)
 a.add('</g>')
 # lamps and stylized reflection strokes
 flick= .93+.04*math.sin(t*3.1)+.025*math.sin(t*8)
 a.add(f'<g opacity="{flick}">');a.ellipse(810,460,280,350,'url(#lamp)')
 a.path('M875 320 L817 342 L807 452','none','#06121a',15)
 a.path('M790 449 Q808 422 829 447 L833 461 L788 461Z','#f8b158','#493a24',3)
 a.ellipse(809,461,26,6,'#ffe3a4');a.add('</g>')
 a.path('M799 470 L819 470 L980 1220 L450 1220Z','#ffc26a','none',0,'opacity=".045"')
 for i in range(95):
  y=rng.uniform(1010,1880);x=790+(y-1010)*-.12+rng.uniform(-100,100)*(y/1400)
  a.line([(x,y),(x+rng.uniform(12,80),y)],['#715337','#9c7040','#254550','#3c6571'][i%4],rng.uniform(1,4))
 for i in range(40):
  x=rng.uniform(50,1080);y=rng.uniform(1130,1880)
  a.line([(x,y),(x+rng.uniform(12,110),y-2)],'#183641',2)
 # Fixed pavement detail makes the world displacement directly readable.
 a.ellipse(515,1495,115,26,'#0b1b25','#37515b',3)
 for xx in range(435,600,18):a.line([(xx,1482),(xx+6,1507)],'#28424e',3)
 a.poly([(70,1500),(150,1486),(188,1550),(91,1562)],'#06151f','#314954',3)
 for yy in range(1508,1548,8):a.line([(89,yy),(156,yy-8)],'#52616a',2)
 a.path('M310 925 L325 1040 L310 1210 L339 1450 L330 1780','none','#27414c',2)
 for j in range(12):
  x=110+j*79;y=1460+(j%4)*83;phase=(t*.8+j*.173)%1
  a.ellipse(x,y,5+phase*24,1+phase*4,'none','#527984',1.3,extra=f'opacity="{.40*(1-phase)}"')
 # sedan three-quarter rear, behind action; coherent illustrative contours
 a.add(f'<g id="black-sedan" transform="translate(290,329) scale(.85)">')
 a.ellipse(834,1290,268,39,'#020a10')
 for x,y in [(647,1226),(1004,1170)]:
  a.ellipse(x,y,37,80,'#02070d','#30434a',5);a.ellipse(x+2,y,20,47,'#1c2b35','#080f18',4)
  for ang in range(0,360,60):
   rad=math.radians(ang);a.line([(x,y),(x+17*math.sin(rad),y+39*math.cos(rad))],'#42505a',3)
 a.path('M596 1100 L668 975 Q701 935 802 934 L902 948 L1018 1059 L1041 1193 Q965 1258 638 1282 L596 1230Z','url(#metal)',OUTLINE,8)
 a.path('M684 980 Q755 948 801 957 L895 972 L958 1042 L667 1067Z','#07151e','#4b616a',4)
 a.path('M804 961 L808 1054 M699 981 L687 1059','none','#263b48',5)
 a.path('M615 1103 Q811 1134 1010 1061 L1020 1150 Q822 1226 615 1195Z','#111e29','#43515c',4)
 a.path('M634 1134 L728 1142 L742 1160 L635 1152Z','#f34d49','#631e26',3)
 a.path('M937 1104 L1003 1084 L1009 1101 L939 1121Z','#ff6251','#631e26',3)
 a.line([(644,1140),(721,1147)],'#ffa183',3);a.line([(943,1110),(999,1094)],'#ffa183',3)
 a.path('M618 1218 Q800 1246 1030 1170','none','#405360',4)
 a.poly([(787,1175),(873,1164),(875,1190),(789,1200)],'#b4b5a3','#111c24',4)
 a.line([(811,1183),(851,1178)],'#3b484a',3)
 a.path('M634 1260 L626 1280 M1015 1190 L1011 1215','none','#020911',13)
 a.add('</g>')
 # World-space pulling follows the .90–3.20 s acceleration/deceleration schedule.
 d=travel(t)
 settle=smooth((t-3.2)/.5);_,bounce=posture(t,2)
 camx=0
 a.add(f'<g id="character-action" transform="translate({camx},0)">')
 a.add('<defs><radialGradient id="contact-light"><stop stop-color="#41727e" stop-opacity=".22"/><stop offset="1" stop-color="#41727e" stop-opacity="0"/></radialGradient></defs>')
 a.ellipse(430+d,1370,380,110,'url(#contact-light)')
 # contact shadows change with body positions, never detached from ground
 for x,rx,yy in [(105+d,87,GROUND[0]+12),(275+d,100,1416),(530+d,84,GROUND[1]+12)]:a.ellipse(x,yy,rx,18,'#02090e',extra='opacity=".85"')
 # Heel contact shadows and short wet scrape trails remain on the pavement.
 _,heel_contacts,_=victim_weight(t)
 for heelx,heely in heel_contacts:
  a.ellipse(heelx,heely+8,32,5,'#020a10')
  if .9<t<3.35:a.line([(heelx-29,heely+7),(heelx-7,heely+7)],'#6d8991',1.5)
 # victim shared joints; grip endpoints consumed by both actor rigs
 vx,vy,victim_shoulders,victim_elbows,grips=upper_arm_targets(t)
 # rear actor body first, arms later so contact reads on top
 def criminal(x,base,who):
  a.add(f'<g id="actor-{who}" data-center-x="{x}" data-time="{t}">')
  lean,bob=posture(t,who);hip=(x+hip_shift(t,who-1),base-159+bob*.65)
  shoulder=(x+lean,base-284+bob)
  a.add(f'<g id="actor-pose-{who}" data-hip="{pt(hip)}" data-shoulder="{pt(shoulder)}"/>')
  ankles=[foot_state(t,who-1,0),foot_state(t,who-1,1)]
  for j in [0,1]:
   h=(hip[0]+(-15 if j==0 else 17),hip[1]);f=(ankles[j][0],ankles[j][1]);k=ik(h,(f[0],f[1]-11),85,85,-1)
   limb(a,[h,k,(f[0],f[1]-11)],'#172833' if j==0 else '#243945',28,tag=f'actor-{who}-leg-{j}')
   a.path(f'M{f[0]-18},{f[1]-10} Q{f[0]+8},{f[1]-20} {f[0]+33},{f[1]-5} L{f[0]+34},{f[1]+7} L{f[0]-20},{f[1]+7}Z','#1a2a34',OUTLINE,5,f'id="actor-{who}-foot-{j}" data-x="{f[0]}" data-y="{f[1]}" data-phase="{ankles[j][2]}"')
   a.line([(f[0]-14,f[1]+3),(f[0]+28,f[1]+3)],'#8d9c9e',2.5)
  sx,sy=shoulder
  a.path(f'M{sx-44},{sy-8} Q{sx-61},{sy+15} {hip[0]-45},{hip[1]+15} Q{hip[0]},{hip[1]+30} {hip[0]+48},{hip[1]+12} L{sx+45},{sy+7} Q{sx+27},{sy-19} {sx-44},{sy-8}Z','url(#cloth)',OUTLINE,7)
  a.path(f'M{sx-32},{sy+18} L{hip[0]-30},{hip[1]+9} M{sx+21},{sy+27} L{hip[0]+24},{hip[1]-4}','none','#3c4d56',2)
  a.path(f'M{sx-3},{sy+20} L{hip[0]+1},{hip[1]+17} M{hip[0]-25},{hip[1]-26} Q{hip[0]},{hip[1]-16} {hip[0]+25},{hip[1]-27}','none','#07121c',4)
  # hood collar and hanging drawstrings
  a.path(f'M{sx-37},{sy-13} Q{sx},{sy+42} {sx+36},{sy-12} L{sx+21},{sy-37} L{sx-25},{sy-35}Z','#0b1722',OUTLINE,5)
  a.line([(sx-15,sy+12),(sx-17,sy+51)],'#617079',2);a.line([(sx+14,sy+12),(sx+16,sy+47)],'#617079',2)
  # far, free hand braces against their own thigh
  freeS=(sx+(-35 if who==1 else 34),sy+17);freeH=(hip[0]+(-39 if who==1 else 42),hip[1]-12)
  elbow=ik(freeS,freeH,65,63,1 if who==1 else -1)
  limb(a,[freeS,elbow,freeH],'#172732',26,tag=f'actor-{who}-free-arm');a.ellipse(*freeH,15,18,'#09141d',OUTLINE,4)
  draw_head(a,sx+2,sy-72,t,who,hide_eyes)
  a.path(f'M{sx-43},{sy+7} Q{sx-53},{sy+35} {hip[0]-44},{hip[1]-2}','none','#da9a4b',3)
  a.add('</g>')
  return shoulder
 s1=criminal(BASES[0]+d,GROUND[0],1)
 s2=criminal(BASES[1]+d,GROUND[1],2)
 # victim, visibly sagging between two independently loaded grips
 pelvis,passive_heels,head_roll=victim_weight(t);shoulders=victim_shoulders
 a.add(f'<g id="victim-weight" data-pelvis="{pt(pelvis)}" data-shoulder-y="{vy+6}"/>')
 for j in [0,1]:
  h=(pelvis[0]+(-18 if j==0 else 18),pelvis[1]);toe=passive_heels[j]
  knee=ik(h,(toe[0]+12,toe[1]-9),77,80,-1)
  limb(a,[h,knee,(toe[0]+12,toe[1]-9)],'#213b47',26,tag=f'victim-leg-{j}')
  a.path(f'M{toe[0]-20},{toe[1]-12} Q{toe[0]+7},{toe[1]-23} {toe[0]+29},{toe[1]-3} L{toe[0]+27},{toe[1]+6} L{toe[0]-22},{toe[1]+6}Z','#08151e',OUTLINE,5,f'id="victim-heel-{j}" data-x="{toe[0]}" data-y="{toe[1]}"')
 a.path(f'M{vx-38},{vy-9} Q{vx-58},{vy+50} {pelvis[0]-39},{pelvis[1]+2} Q{pelvis[0]},{pelvis[1]+23} {pelvis[0]+39},{pelvis[1]} L{vx+38},{vy-7}Z','#b8bdbb',OUTLINE,6)
 a.path(f'M{vx+14},{vy+13} L{pelvis[0]+29},{pelvis[1]-1} L{pelvis[0]+38},{pelvis[1]} L{vx+37},{vy+7}Z','#74848b','none',0)
 a.path(f'M{vx-3},{vy+30} l-13 25 8 11 -4 27 11 -18 3 -17 10 -4 -7 -22Z','#8d3037','none',0)
 for i in [0,1]:
  a.add(f'<g id="victim-arm-{i}" data-shoulder="{pt(shoulders[i])}" data-elbow="{pt(victim_elbows[i])}">')
  g=victim_elbows[i];h=(g[0]+(-6 if i==0 else 6),g[1]+42)
  limb(a,[shoulders[i],g,h],'#bdc0bf',23,tag=f'victim-arm-bones-{i}');a.ellipse(*h,12,16,'#c1c6c3',OUTLINE,3)
  a.add('</g>')
 a.add(f'<g id="victim-head" data-roll="{head_roll}" transform="translate(-2,{6+2*math.cos(travel(t)/STRIDE*2*math.pi-1)}) rotate({head_roll} {vx} {vy-56})">')
 a.ellipse(vx,vy-58,51,58,'url(#face)',OUTLINE,5)
 a.path(f'M{vx-51},{vy-68} Q{vx-57},{vy-118} {vx-7},{vy-121} Q{vx+48},{vy-122} {vx+52},{vy-69} L{vx+48},{vy-52} Q{vx-4},{vy-67} {vx-51},{vy-68}Z','#111f2a',OUTLINE,5)
 a.line([(vx-35,vy-95),(vx+39,vy-71)],'#b78343',2)
 a.path(f'M{vx-27},{vy-43} l14 4 M{vx+10},{vy-39} l12 -1 M{vx-8},{vy-20} q10 -4 16 1','none','#18222b',3)
 a.path(f'M{vx+30},{vy-47} l-5 21','none','#a33f43',3);a.add('</g>')
 # Criminal grip arms over victim sleeves; shared endpoints guarantee no grip drift
 for i,s in enumerate([s1,s2]):
  sh=(s[0]+(37 if i==0 else -37),s[1]+13);g=grips[i]
  elbow=ik(sh,g,90,87,1 if i==0 else -1)
  limb(a,[sh,elbow,g],'#1a2b37',26,tag=f'actor-{i+1}-support-arm')
  a.ellipse(sh[0],sh[1],12,13,'#1a2b37')
  a.ellipse(g[0],g[1],18,15,'#1b2d39',OUTLINE,4,extra=f'id="support-hand-{i}"')
  a.path(f'M{g[0]-12},{g[1]+4} Q{g[0]-15},{g[1]-9} {g[0]+3},{g[1]-11}','none','#94afb3',2)
  for finger in [-5,1,7]:a.path(f'M{g[0]+finger},{g[1]+1} l4 5','none','#5f818b',1.7)
 # splashes triggered during planted contact; small crown ripples, not constant sparkles
 for actor,baseX in enumerate(BASES):
  for off in [0,.5]:
   fx,fy,phase=foot_state(t,actor,0 if off==0 else 1)
   if phase<.14 and .9<t<3.3:
    r=4+phase*95;a.ellipse(fx,fy+8,r,r*.17,'none','#6d9aa8',1.5,extra=f'opacity="{1-phase/.18}"')
    for q in [-1,1]:a.line([(fx+q*7,fy+4),(fx+q*(10+r*.4),fy-4-r*.2)],'#7aa3ae',1.5)
 a.add('</g>')
 # deterministic rain at three depths; no changing identity from random samples
 for layer,count in ([(0,300),(1,220),(2,85)] if t<3.2 else []):
  a.add(f'<g id="rain-{layer}" opacity="{[.20,.32,.46][layer]}">')
  for i in range(count):
   x0=rng.uniform(-150,1230);y0=rng.uniform(-100,2000);speed=[520,760,1120][layer]
   y=(y0+t*speed)%2080-80;x=x0+(y-y0)*-.10-cam*[.2,.7,1.5][layer];x=(x+100)%1280-100
   length=[15,25,42][layer];a.line([(x,y),(x-3-layer*2,y+length)],'#80a6b5', [1,1.4,2][layer])
  a.add('</g>')
 # foreground framing contributes parallax without obscuring contacts
 a.add(f'<g id="foreground" transform="translate({-cam*1.8},0)">')
 a.poly([(0,0),(25,0),(15,1920),(0,1920)],'#020a11',w=0)
 a.line([(23,0),(14,1920)],'#1d3440',4)
 a.poly([(1260,0),(1235,0),(1246,1920),(1260,1920)],'#020a11',w=0);a.add('</g>')
 a.add('</g></g>')
 if t>=3.2:
  rain_rng=random.Random(424)
  for j in range(125):
   x=rain_rng.uniform(0,1180);y=(rain_rng.uniform(-200,1920)+t*1050)%2100-100
   a.path(f'M{x},{y} l-5 43','none','#6d96a7',1.7,'opacity=".3"')
 a.rect(0,0,1080,1920,'url(#vignette)')
 a.add('</svg>');return ''.join(a.s)

class Raster:
 def __init__(self,w,h):
  self.w=w;self.h=h;self.r=C.CDLL(ctypes.util.find_library('rsvg-2'));self.c=C.CDLL(ctypes.util.find_library('cairo'));self.g=C.CDLL(ctypes.util.find_library('gobject-2.0'))
  self.r.rsvg_handle_new_from_data.argtypes=[C.c_char_p,C.c_size_t,C.c_void_p];self.r.rsvg_handle_new_from_data.restype=C.c_void_p
  self.r.rsvg_handle_render_cairo.argtypes=[C.c_void_p,C.c_void_p];self.r.rsvg_handle_render_cairo.restype=C.c_int
  for name,args,ret in [('cairo_image_surface_create',[C.c_int,C.c_int,C.c_int],C.c_void_p),('cairo_create',[C.c_void_p],C.c_void_p),('cairo_scale',[C.c_void_p,C.c_double,C.c_double],None),('cairo_image_surface_get_data',[C.c_void_p],C.c_void_p),('cairo_surface_flush',[C.c_void_p],None),('cairo_destroy',[C.c_void_p],None),('cairo_surface_destroy',[C.c_void_p],None)]:
   f=getattr(self.c,name);f.argtypes=args;f.restype=ret
  self.g.g_object_unref.argtypes=[C.c_void_p]
 def render(self,svg):
  b=svg.encode();handle=self.r.rsvg_handle_new_from_data(b,len(b),None)
  surf=self.c.cairo_image_surface_create(0,self.w,self.h);ctx=self.c.cairo_create(surf);self.c.cairo_scale(ctx,self.w/1080,self.h/1920)
  if not self.r.rsvg_handle_render_cairo(handle,ctx):raise RuntimeError('SVG render failed')
  self.c.cairo_surface_flush(surf);buf=C.string_at(self.c.cairo_image_surface_get_data(surf),self.w*self.h*4)
  im=Image.frombytes('RGBA',(self.w,self.h),buf,'raw','BGRA').convert('RGB')
  self.c.cairo_destroy(ctx);self.c.cairo_surface_destroy(surf);self.g.g_object_unref(handle);return im

def audio():
 sr=48000;n=sr*5;rng=np.random.default_rng(117);noise=rng.standard_normal(n)
 rain=(noise-np.roll(noise,1))*.022
 # low rumble beneath rain, generated locally rather than sampled
 ts=np.arange(n)/sr;track=rain+.016*np.sin(2*np.pi*43*ts)*(.7+.3*np.sin(ts*1.8))
 events=[]
 # Individual footfall events, not duplicated synchronized sounds.
 for actor in (0,1):
  for leg in (0,1):
   offset=leg*.5+actor*.12
   for cycle in range(5):
    target=(cycle-offset)*STRIDE
    if target<=0 or target>TRAVEL:continue
    lo,hi=.9,3.2
    for _ in range(40):
     mid=(lo+hi)/2
     if travel(mid)<target:lo=mid
     else:hi=mid
    when=(lo+hi)/2;start=round(when*sr);nn=min(int(.19*sr),n-start);tt=np.arange(nn)/sr
    sound=.15*np.sin(2*np.pi*(83*tt-60*tt*tt))*np.exp(-tt*27)+rng.standard_normal(nn)*.06*np.exp(-tt*40)
    track[start:start+nn]+=sound;events.append({'time':when,'actor':actor+1,'leg':leg,'event':'wet foot plant'})
 # subtle friction while victim heels drag
 moving=(ts>.9)&(ts<3.33);friction=np.convolve(rng.standard_normal(n),np.ones(9)/9,mode='same')*.022
 track+=friction*moving
 cut=round(3.2*sr);nn=int(.45*sr);tt=np.arange(nn)/sr
 track[cut:cut+nn]+=.055*np.sin(2*np.pi*(54*tt-14*tt*tt))*np.exp(-tt*10)
 fade=np.minimum(1,ts/.08)*np.minimum(1,(5-ts)/.15);track*=fade*1.8
 stereo=np.column_stack((track,np.roll(track,97)*.97));stereo*=.60/max(.60,float(np.max(np.abs(stereo))));pcm=(np.clip(stereo,-.95,.95)*32767).astype('<i2')
 dest=ROOT/'assets'/'original_ambience.wav'
 with wave.open(str(dest),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
 (ROOT/'assets'/'sound-events.json').write_text(json.dumps(events,indent=2));return dest

def main():
 p=argparse.ArgumentParser();p.add_argument('--scale',type=float,default=.5);p.add_argument('--fps',type=int,default=30);p.add_argument('--out',default='previews/preview_v1.mp4');p.add_argument('--stills',action='store_true');p.add_argument('--hide-eyes',action='store_true');args=p.parse_args()
 w=round(1080*args.scale/2)*2;h=round(1920*args.scale/2)*2;r=Raster(w,h)
 out=ROOT/args.out
 if out.exists():raise SystemExit('Refusing to overwrite '+str(out))
 out.parent.mkdir(parents=True,exist_ok=True)
 wav=audio()
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(args.fps),'-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','5','-movflags','+faststart',str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 samples=[]
 for i in range(5*args.fps):
  t=i/args.fps;svg=scene(t,hide_eyes=args.hide_eyes);im=r.render(svg);proc.stdin.write(im.tobytes())
  if args.stills and i%max(1,args.fps//4)==0:
   thumb=im.resize((216,384));samples.append((t,thumb))
  if i in [0,args.fps*2,args.fps*4,5*args.fps-1]:
   im.save(ROOT/'previews'/f'frame_{i:03d}_{w}.png')
   (ROOT/'assets'/f'scene_{t:.3f}.svg').write_text(svg)
  if i%args.fps==0:print(f'{i}/{5*args.fps}',flush=True)
 proc.stdin.close()
 if proc.wait():raise RuntimeError('ffmpeg failed')
 if samples:
  cols=5;sheet=Image.new('RGB',(cols*216,math.ceil(len(samples)/cols)*410),'#07121d');draw=ImageDraw.Draw(sheet)
  for j,(t,im) in enumerate(samples):
   x=j%cols*216;y=j//cols*410;sheet.paste(im,(x,y));draw.text((x+8,y+387),f'{t:.2f}s',fill='white')
  sheet.save(ROOT/'previews'/f'contact_{w}.jpg',quality=90)
 print(out)
if __name__=='__main__':main()
