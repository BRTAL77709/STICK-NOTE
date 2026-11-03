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
  text(a,x,y+r*.46,str(round(value)),r*.25,'#f2f0e7');text(a,x,y+r*.62,label,r*.075,'#9ab1b8')

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

def pedal(a,t):
 q=ease(t,4,5);a.rect(0,0,1080,1920,'#07131d')
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

def head_rig(a,x,y,t,emotion='worried',yaw=0,scale=1,tilt=0):
 """Approved round pale face / navy cap; perspective modifies brim, face plane and eye spacing."""
 theta=yaw*.63;cs=math.cos(theta);shift=20*math.sin(theta);blink=max(0,1-abs((t-2.37)/.075)) if t<5 else max(0,1-abs((t-12.86)/.075))
 a.add(f'<g transform="translate({x} {y}) rotate({tilt}) scale({scale})">')
 a.ellipse(0,0,61,66,'url(#face)',INK,6)
 a.path(f'M{-61} -12 Q-61 -78 {-shift*.3} -80 Q58 -76 61 -16Z','#142c3a','#6d8794',2.6)
 a.path(f'M-61 -24 Q-57 -60 -36 -70','none','#d4a35c',3)
 # Curved brim has real changing side extent/depth rather than a static cap plus moving pupils.
 tip=79+21*math.sin(theta);a.path(f'M-66 -17 Q{shift} -40 {65+shift*.4} -15 L{tip} {2-8*math.sin(theta)} Q{18+shift} -6 -64 3Z','#0b1d2a',INK,5)
 a.path(f'M{45-8*cs} 8 Q70 28 41 57','none','#7c9497',1.5,'opacity=".45"')
 for j,ex in enumerate([-21,20]):
  xx=ex*cs+shift;eye_h=(14 if emotion=='shocked' else 10)*(1-blink)+1.3*blink
  a.ellipse(xx,16-5*ease(t,2.05,2.6),4.5,eye_h,'#07111a')
  sy=-1 if j==0 else 1;a.path(f'M{xx-10} {-2+4*(emotion=="worried")} l20 {sy*4}','none','#233541',3)
 if emotion=='shocked':a.ellipse(shift*.7,46,9,12,'#182731',INK,2)
 else:a.path(f'M{-10+shift*.7} 48 q12 -7 24 -1','none','#273a44',3)
 a.path('M-43 22 q-8 12 -1 17 q8 1 1 -17Z','#76a7b8','#365f70',1)
 a.add('</g>')

def driver(a,t,worldcam,mirror=None,steering=False):
 s=state(t);city(a,worldcam,t)
 # Background windshield and wiper are behind the illustrated driver/seat layers.
 sweep=-.12+.92*math.sin(t*3.3);a.line([(100,1130),(100+790*math.cos(sweep),1130-790*math.sin(sweep))],INK,13)
 a.path('M0 0 H1080 V260 Q540 90 0 260Z','#08151f',INK,8)
 for xx,sign in [(55,-1),(1025,1)]:a.path(f'M{xx} 190 L{xx+sign*65} 1440','none','#08131d',57);a.path(f'M{xx+7} 205 L{xx+sign*45} 1370','none','#496875',5)
 a.rect(270,600,540,830,'#0b1c28','#355563',7,90)
 tension=ease(t,2.1,3.1);anticipate=ease(t,12.5,12.9) if steering else 0
 settle=math.sin((t-2.1)*12)*math.exp(-max(0,t-2.1)*4)*tension if t<4 else 0
 weight=clamp(s['acceleration_mps2']*7,-28,28);roll=s['roll']*100
 shL=(310-roll-10*anticipate,940-20*tension+weight);shR=(775-roll+5*anticipate,953-32*tension+weight)
 a.path(f'M{shL[0]} {shL[1]} Q540 874 {shR[0]} {shR[1]} L823 1370 Q540 1440 255 1370Z','url(#cloth)',INK,10)
 a.path(f'M{shL[0]+10} {shL[1]} L690 1380','none','#030d16',35);a.path(f'M{shL[0]+10} {shL[1]} L690 1380','none','#546975',20)
 a.path('M410 1020 L400 1240 M650 1020 L660 1240','none','#6a8088',3)
 yaw=(-.18+.95*ease(t,2.1,2.9)-.6*ease(t,3.3,3.9)) if not steering else -.6*anticipate
 hx=538-roll+5*settle;hy=701+weight-12*tension+3*math.sin(t*3.7)
 a.path(f'M{hx-40} 920 L{hx-37} 824 L{hx+43} 824 L{hx+47} 920Z','#1b3543',INK,6)
 head_rig(a,hx,hy,t,'shocked' if 2.55<t<3.25 else 'worried',yaw,2.78,-3-4*anticipate)
 cx,cy=540,1240;ang=s['steering_wheel_rad'];grip=.10*tension
 a.ellipse(cx,cy,234,162,'none',INK,35);a.ellipse(cx,cy,234,162,'none','#4d6a77',16)
 for j,ss in enumerate([shL,shR]):
  th=(math.pi*.84-grip if j==0 else math.pi*.16+grip)+ang;hand=(cx+228*math.cos(th),cy-155*math.sin(th));el=ik(ss,hand,180,174,1 if j==0 else -1)
  limb(a,[ss,el,hand],'#2a4554',49);a.ellipse(*hand,31,38,'#d9ded3',INK,6)
  for k in range(3):a.path(f'M{hand[0]-14+k*10} {hand[1]+8} q4 -15 11 -19','none','#768e8e',2)
 for th in [ang,ang+2.2,ang+4.1]:a.line([(cx,cy),(cx+205*math.cos(th),cy-142*math.sin(th))],'#294859',24)
 a.ellipse(cx,cy,58,42,'#17303e','#647e8b',4)
 dashboard(a,t)
 if mirror:mirror(a,t,(365,260,365,155),False)
 illumination=max(0,1-abs((s['z']%24)-12)/3)
 a.path(f'M{hx-160} {hy-80} l320 15 -6 65 -320 -15Z','#efb568','none',0,f'opacity="{illumination*.11}"')
