"""Approved witness identity, contact-constrained driving and in-dash instruments."""
import math
from approved_components import witness_head,text,limb,ik
from motion_state import *
from world import INK,AMBER,Camera,city

def dial(a,x,y,r,value,maximum=160,label='km/h',minor=False):
 a.ellipse(x,y,r+15,r+15,'#0b1720','#637b83',5);a.ellipse(x,y,r,r,'#06121c','#162e3c',4)
 for v in range(0,maximum+1,10 if not minor else 1):
  th=math.radians(140+260*v/maximum);major=(v%20==0) if not minor else True
  rr=r*.84 if major else r*.91
  a.line([(x+rr*math.cos(th),y+rr*math.sin(th)),(x+r*.96*math.cos(th),y+r*.96*math.sin(th))],AMBER if v>=maximum*.8 else '#b9c9c7',4 if major else 2)
  if major:
   tx=x+r*.69*math.cos(th);ty=y+r*.69*math.sin(th);text(a,tx,ty+r*.055,str(v),r*.14,'#c9d6d0',stroke=1)
 th=math.radians(140+260*clamp(value/maximum));nx=x+r*.79*math.cos(th);ny=y+r*.79*math.sin(th)
 a.line([(x-30*math.cos(th),y-30*math.sin(th)),(nx,ny)],'#080e14',12);a.line([(x-30*math.cos(th),y-30*math.sin(th)),(nx,ny)],'#ef805d',6)
 a.ellipse(x,y,r*.07,r*.07,'#d1b685',INK,3)
 if not minor:
  text(a,x,y+r*.46,str(round(value)).zfill(3),r*.22,'#e9ca91');text(a,x,y+r*.62,label,r*.075,'#9ab1b8')

def dashboard(a,t,insert=False):
 s=state(t)
 if insert:
  a.path('M0 450 Q540 230 1080 450 L1080 1920 L0 1920Z','#132b37','#020a11',12)
  a.path('M0 490 Q540 280 1080 490','none','#66808a',5)
  for x in [60,910]:
   a.rect(x,620,115,90,'#07141e','#476470',5,12)
   for j in range(4):a.line([(x+10,639+j*16),(x+105,639+j*16)],'#3e5e6b',3)
  a.rect(135,760,810,650,'#071019','#526b76',8,75)
  dial(a,570,1060,291,s['speed_kmh'])
  dial(a,215,1250,105,s['rpm']/1000,8,'RPM',True)
  text(a,215,1300,'RPM ×1000',21,'#c2b899')
  text(a,540,700,'2:17 AM',39,'#bed2d2');text(a,770,1360,'D',38,'#c8d3bc')
  a.path('M0 1680 Q540 1400 1080 1680','none','#020a10',130);a.path('M0 1680 Q540 1400 1080 1680','none','#344c59',58)
  # Glass highlight remains clipped to cluster housing.
  a.path('M190 808 Q540 710 870 815','none','#7e9d9f',3,'opacity=".4"')
 else:
  a.path('M0 1320 Q540 1170 1080 1320 L1080 1920 L0 1920Z','#0b1b26',INK,10)
  dial(a,790,1370,130,s['speed_kmh']);a.rect(170,1370,190,75,'#08131c','#3d5b6b',3,14);text(a,265,1420,'2:17',35,'#9ab5bb')

def driver(a,t,worldcam,mode='reaction'):
 s=state(t);city(a,worldcam,t)
 a.add('<defs><clipPath id="cabin-glass"><path d="M50 180 Q540 80 1030 180 L1060 1150 L25 1150Z"/></clipPath></defs>')
 th=-.26+.95*math.sin(t*3.2);a.line([(150,1120),(150+740*math.cos(th),1120-740*math.sin(th))],INK,13)
 # Upper roof, pillars and passenger seat establish a cabin rather than floating driver art.
 a.path('M0 0 L1080 0 L1080 250 Q540 80 0 250Z','#07131d',INK,7)
 for side in [-1,1]:
  x=58 if side<0 else 1020;a.path(f'M{x} 190 L{x+side*60} 1420','none','#08121b',56);a.path(f'M{x} 190 L{x+side*60} 1420','none','#4a626e',6)
 a.rect(290,600,510,840,'#0c1c28','#34515e',8,90)
 setback=acceleration(t)*9;breath=3*math.sin(t*4);lean=-16*ease(t,2.5,3.6)+setback
 shL=(315+lean,960+setback);shR=(767+lean,960+setback);hip=(545+lean,1340)
 a.path(f'M{shL[0]} {shL[1]} Q540 895 {shR[0]} {shR[1]} L820 1380 Q540 1460 260 1370Z','url(#cloth)',INK,10)
 a.path('M425 1030 L420 1245 M630 1030 L642 1245','none','#5c7380',4)
 a.path('M365 973 Q540 1080 704 970 L652 930 L425 920Z','#0b1926',INK,7)
 # Seatbelt stays on the torso; no unexplained outfit changes.
 a.path(f'M{shL[0]+10} {shL[1]-5} L690 1380','none','#040d15',36);a.path(f'M{shL[0]+10} {shL[1]-5} L690 1380','none','#415661',19)
 yaw=.15+.55*ease(t,2.55,3.1)-.5*ease(t,3.5,4.1)+.7*ease(t,13.45,14.0)
 # Character source identity remains exact; independent neck yaw, torso/arm tension and blink.
 hx=535+lean+yaw*14;hy=713+breath+setback
 a.path(f'M{hx-43} 902 L{hx-38} 830 L{hx+41} 830 L{hx+45} 902Z','#ccd1ca',INK,6)
 witness_head(a,hx,hy,t,'panic' if 3<t<4.5 else 'worried',yaw,2.8)
 blink=max(0,1-abs((t-2.75)/.085)) if t<4 else max(0,1-abs((t-14.6)/.085))
 if blink>0:
  for ex in [-21,20]:a.line([(hx+(ex-6+yaw*10)*2.8,hy+18*2.8),(hx+(ex+6+yaw*10)*2.8,hy+18*2.8)],'#aebcb7',18*blink)
 # Hands at real rotating rim anchors, fingers wrap across it.
 cx,cy=540,1260;ang=s['steer_rad']*16+.008*math.sin(s['distance_m']*1.1)
 a.ellipse(cx,cy,233,163,'none',INK,35);a.ellipse(cx,cy,233,163,'none','#3a5565',16)
 for j,ss in enumerate([shL,shR]):
  th=(math.pi*.88 if j==0 else math.pi*.12)+ang;hand=(cx+228*math.cos(th),cy-157*math.sin(th));el=ik(ss,hand,176,170,1 if j==0 else -1)
  limb(a,[ss,el,hand],'#29414e',49);a.ellipse(*hand,30,38,'#d9dcd2',INK,6)
  for k in range(3):a.path(f'M{hand[0]-15+k*10} {hand[1]+8} q5 -14 10 -18','none','#627979',2)
 for th in [ang,ang+2.25,ang+4.03]:a.line([(cx,cy),(cx+205*math.cos(th),cy-143*math.sin(th))],'#2d4858',23)
 a.ellipse(cx,cy,59,40,'#172e3c','#526c79',4)
 # Actual mirrored view cropped to mirror surface with size derived from pursuer gap.
 a.rect(380,260,340,140,'#08131d','#657b83',8,22);a.rect(395,275,310,109,'#153240',rx=15)
 gap=28-14*ease(t,5,11);spread=90/gap*17
 for xx in [550-spread,550+spread]:a.ellipse(xx,333,9+100/gap,8+65/gap,'#cfe6e7')
 a.path('M402 365 Q550 310 697 367','none','#3e5d68',2)
 # Passing amber stripe responds to actual world travel.
 illumination=max(0,1-abs((s['z']%24)-12)/2.6)
 a.add(f'<g opacity="{illumination*.16}">');a.path(f'M{hx-180} {hy-80} l360 12 -8 80 -355 -12Z','#f4ba6a','none',0);a.add('</g>')
 dashboard(a,t)


def pedal(a,t):
 q=ease(t,4.2,5.1);a.rect(0,0,1080,1920,'#07131d')
 a.path('M130 300 L1010 380 L1080 1740 L0 1710Z','#20343e','#526873',7)
 for j in range(12):a.line([(130+j*75,700),(20+j*92,1730)],'#172a35',8)
 a.rect(230,720,190,250,'#071018','#71828a',7,20)
 for j in range(4):a.line([(251,765+j*45),(399,765+j*45)],'#536a73',8)
 # Accelerator shaft rotates about its actual lower hinge. Sole follows the pedal contact.
 angle=19*q;a.add(f'<g transform="rotate({angle} 735 1370)">');a.line([(735,1370),(735,1030)],'#6d7e82',25);a.rect(665,925,140,295,'#08121a','#879392',8,20)
 for j in range(6):a.line([(681,958+j*43),(791,958+j*43)],'#435e68',7)
 a.add('</g>')
 a.ellipse(735,1370,27,23,'#9aa39a',INK,6)
 th=math.radians(angle);tx=735+math.sin(th)*210;ty=1370-math.cos(th)*210
 # Articulated lower leg/shoe uses heel planted on mat, toe presses same moving pedal surface.
 heel=(490,1535);ank=(480+25*q,1430);knee=(260,1050+45*q)
 limb(a,[(155,410),knee,ank],'#1c3341',112)
 a.path(f'M{heel[0]-80} {heel[1]} Q430 1330 {tx-55} {ty-40} Q{tx+75} {ty-85} {tx+55} {ty+22} L{heel[0]+80} {heel[1]+32} Q{heel[0]-20} {heel[1]+65} {heel[0]-80} {heel[1]}Z','#152a38',INK,12)
 a.path(f'M{heel[0]-72} {heel[1]+8} Q{heel[0]} {heel[1]+50} {tx+55} {ty+22}','none','#718690',6)
 for k in range(4):a.line([(520+k*25,1320-k*22),(565+k*25,1335-k*22)],'#4b6676',4)
 a.ellipse(495,1560,100,13,'#030a11',extra='opacity=".55"')
