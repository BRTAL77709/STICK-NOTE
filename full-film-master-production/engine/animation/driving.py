"""V4 hinged accelerator and planted-heel contact rig. Driver lives in driver_rig.py."""
import math
from approved_components import limb
from motion_state import *
from world import INK

def pedal(a,t):
 q=ease(t,28.55,29.45);a.rect(0,0,1080,1920,'#07131d')
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


def dashboard(a,t,insert=False):
 a.path('M0 1320 Q540 1170 1080 1320 L1080 1920 L0 1920Z','#0b1b26',INK,10)
