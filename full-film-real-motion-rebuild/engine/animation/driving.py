"""V4 hinged accelerator and planted-heel contact rig. Driver lives in driver_rig.py."""
import math
from approved_components import limb,ik
from motion_state import *
from world import INK

def pedal_pose(t):
 # The ball of a rigid foot stays on the rotating pedal. Contact can roll
 # along the pedal face while a single heel pivot remains planted.
 q=clamp((throttle(t)-.20)/.72);angle=math.radians(28*q)
 hinge=(735.,1370.);heel=(470.,1530.);L=430.
 direction=(math.sin(angle),-math.cos(angle));delta=(hinge[0]-heel[0],hinge[1]-heel[1]);dot=sum(x*y for x,y in zip(delta,direction));r=-dot+math.sqrt(dot*dot-(delta[0]**2+delta[1]**2-L*L))
 toe=(hinge[0]+r*direction[0],hinge[1]+r*direction[1]);foot_angle=math.atan2(toe[1]-heel[1],toe[0]-heel[0])
 def point(x,y):return (heel[0]+x*math.cos(foot_angle)-y*math.sin(foot_angle),heel[1]+x*math.sin(foot_angle)+y*math.cos(foot_angle))
 ankle=point(70,-95);hip=(205.,420.);knee=ik(hip,ankle,620,620,-1)
 return dict(t=t,q=q,hinge=hinge,heel=heel,toe=toe,ankle=ankle,hip=hip,knee=knee,pedal_angle=angle,foot_angle=foot_angle,foot_length=L,pedal_contact_radius=r)

def pedal(a,t):
 p=pedal_pose(t);a.rect(0,0,1080,1920,'#07131d')
 a.path('M130 300 L1010 380 L1080 1740 L0 1710Z','#20343e','#526873',7)
 for j in range(12):a.line([(130+j*75,700),(20+j*92,1730)],'#172a35',8)
 a.rect(230,720,190,250,'#071018','#71828a',7,20)
 for j in range(4):a.line([(251,765+j*45),(399,765+j*45)],'#536a73',8)
 a.add(f'<g transform="rotate({math.degrees(p["pedal_angle"])} 735 1370)">');a.line([(735,1370),(735,1030)],'#6d7e82',25);a.rect(665,925,140,340,'#08121a','#879392',8,20)
 for j in range(7):a.line([(681,958+j*43),(791,958+j*43)],'#435e68',7)
 a.add('</g>');a.ellipse(735,1370,27,23,'#9aa39a',INK,6)
 a.ellipse(470,1544,83,12,'#030a11',extra='opacity=".65"')
 a.path('M0 80 H310 V470 Q190 530 0 490Z','#0b1d29','#49636e',9)
 a.path('M0 0 H210 L260 370 Q278 450 210 475 Q150 480 135 410 L0 215Z','#1c3341',INK,11)
 limb(a,[p['hip'],p['knee'],p['ankle']],'#1c3341',112)
 # Shape is constant in foot-local coordinates; only its rigid ankle angle changes.
 a.add(f'<g transform="translate({p["heel"][0]} {p["heel"][1]}) rotate({math.degrees(p["foot_angle"])})">')
 a.path('M0 0 Q-24 -58 33 -105 L105 -120 Q151 -79 253 -70 L386 -58 Q444 -48 444 -11 L430 0 L15 9Z','#152a38',INK,12)
 a.path('M5 0 Q150 15 430 0','none','#718690',7)
 for x in [140,175,210,245]:a.line([(x,-72),(x+15,-28)],'#71828b',4)
 a.path('M35 -100 Q56 -113 105 -114','none','#526e7c',5);a.add('</g>')


def dashboard(a,t,insert=False):
 a.path('M0 1320 Q540 1170 1080 1320 L1080 1920 L0 1920Z','#0b1b26',INK,10)
