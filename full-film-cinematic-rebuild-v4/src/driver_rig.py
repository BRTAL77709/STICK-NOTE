"""V4 continuous articulated driver. Hand targets are analytic wheel contacts.
Face, cap, neck, shoulders and two-bone arms are hierarchical, not pose swaps.
"""
import math
from approved_components import limb,ik
from motion_state import *
from world import city,INK

def pose(t):
 s=state(t)
 glance=ease(t,2.06,2.67)*(1-ease(t,2.91,3.35))
 look=ease(t,11.72,12.10)*(1-.65*ease(t,12.65,13.25))
 fear=ease(t,2.14,2.60)*(1-.4*ease(t,2.85,3.35))
 # Eyes lead head, then shoulder tension; body responds to actual longitudinal/lateral load.
 eyes=ease(t,2.01,2.35)*(1-ease(t,3.02,3.30))
 lead=ease(t,11.70,11.95)*(1-.5*ease(t,12.8,13.25))
 load=clamp(s['acceleration_mps2']*5,-20,20)
 lean=s['roll']*320
 hx=535+lean+22*glance-18*look;hy=737+load-16*ease(t,2.24,2.8)
 shoulders=[(314+lean*.65,1005+load-24*fear),(770+lean*.65,1013+load-14*fear)]
 cx,cy=540,1270;rx,ry=231,167;ang=s['steering_wheel_rad']
 hands=[];elbows=[]
 for j,sh in enumerate(shoulders):
  th=([math.pi*.80,math.pi*.20][j])+ang
  hand=(cx+rx*math.cos(th),cy-ry*math.sin(th));hands.append(hand)
  elbows.append(ik(sh,hand,178,178,1 if j==0 else -1))
 return dict(state=s,head=(hx,hy),yaw=.98*glance-.93*look,gaze=.95*eyes-.85*lead,fear=fear,lean=lean,load=load,shoulders=shoulders,hands=hands,elbows=elbows,wheel=(cx,cy,rx,ry,ang))

def head(a,x,y,t,yaw,gaze,fear,tilt=0):
 # Turning changes the outline, near/far eye sizes, nose/cheek and cap perspective.
 turn=clamp(yaw,-1,1);v=abs(turn);sg=1 if turn>=0 else -1;half=61-13*v;shift=sg*15*v
 a.add(f'<g transform="translate({x:.3f} {y:.3f}) rotate({tilt:.3f}) scale(2.62)">')
 a.path(f'M{-half} -12 Q{-half-3} -65 -2 -66 Q{half} -65 {half} -8 L{half+max(0,turn)*9} 15 Q{half+max(0,turn)*9} 51 {11+shift} 64 Q{-half+5} 67 {-half-max(0,-turn)*9} 13Z','url(#face)',INK,5.5)
 # Single controlled cel shadow on the receding cheek.
 a.path(f'M{sg*(half-9)} -10 Q{sg*(half+5)} 29 {sg*(half-18)} 53 Q{sg*(half-31)} 62 {shift} 64 Q{sg*(half-8)} 36 {sg*(half-9)} -10Z','#a4b7ba','none',0)
 a.path(f'M{-half-2} -10 Q{-half-2} -77 {-shift*.35} -80 Q{half} -77 {half+2} -11Z','#142c3a','#6d8794',2.6)
 a.path(f'M{-half} -20 Q{-half+6} -60 {-half+23} -70','none','#d4a35c',3)
 # Brim extends toward the turn, narrowing the opposite end.
 brimtip=half+16+max(0,turn)*34;lefttip=-half-5-max(0,-turn)*34
 a.path(f'M{lefttip} -17 Q{shift*1.3} -40 {half+shift*.2} -15 L{brimtip} {2-8*v} Q{17+shift*1.7} -7 {lefttip} 3Z','#0b1d2a',INK,5)
 blink=max(0,1-abs(t-2.44)/.065)+max(0,1-abs(t-11.87)/.065)
 for j,ex in enumerate([-21,20]):
  far=(j==0 and turn>0) or (j==1 and turn<0);xx=ex*(1-.33*v)+shift
  h=(10+4*fear)*(1-clamp(blink))+1.3*clamp(blink);rr=4.2*(1-.60*v if far else 1)
  a.ellipse(xx+gaze*4,13-5*abs(gaze),rr,h,'#07111a')
  brow=-4 if j==0 else 4;a.path(f'M{xx-9} {-2-3*fear} l18 {brow+sg*2*v}','none','#233541',3)
 mouth=fear*(1-.45*v)
 a.path(f'M{-10+shift*.8} 46 q13 {-7+13*mouth} 24 -1','none','#273a44',3)
 if mouth>.1:a.ellipse(shift*.8+2,46,4+5*mouth,1+9*mouth,'#1a2b36',INK,1.5)
 a.path(f'M{-43+shift*.2} 22 q-8 12 -1 17 q8 1 1 -17Z','#76a7b8','#365f70',1)
 a.add('</g>')

def driver(a,t,worldcam,mirror=None,steering=False):
 p=pose(t);s=p['state'];city(a,worldcam,t)
 # Windshield structure and world-locked light are behind the body.
 a.path('M0 0 H1080 V230 Q540 100 0 230Z','#08151f',INK,8)
 for xx,sign in [(48,-1),(1030,1)]:
  a.path(f'M{xx} 190 L{xx+sign*65} 1430','none','#08131d',57);a.path(f'M{xx+7} 205 L{xx+sign*45} 1370','none','#496875',5)
 sweep=.34+.68*math.sin(t*3.3);a.line([(85,1260),(85+850*math.cos(sweep),1260-850*math.sin(sweep))],INK,12)
 a.rect(264,670,555,780,'#0b1c28','#355563',7,90)
 shL,shR=p['shoulders'];hx,hy=p['head'];lean=p['lean']
 a.path(f'M{shL[0]} {shL[1]} Q{535+lean} 916 {shR[0]} {shR[1]} L{813+lean*.4} 1420 Q540 1480 {260+lean*.4} 1420Z','url(#cloth)',INK,10)
 a.path(f'M{shL[0]+10} {shL[1]} L{690+lean*.4} 1410','none','#030d16',35);a.path(f'M{shL[0]+10} {shL[1]} L{690+lean*.4} 1410','none','#546975',20)
 a.path(f'M{hx-105} 985 Q{hx-114} 900 {hx-45} 897 L{hx+48} 898 Q{hx+112} 920 {hx+101} 990 Q{hx+61} 1028 {hx+36} 980 L{hx-35} 980 Q{hx-70} 1025 {hx-105} 985Z','#142c3b',INK,7)
 a.path(f'M{hx-35} 981 L{hx-32} {hy+130} L{hx+34} {hy+128} L{hx+45} 981Z','#1b3543',INK,6)
 for q in [-1,1]:a.path(f'M{hx+q*79} 1020 l{q*11} 175','none','#71828a',3)
 head(a,hx,hy,t,p['yaw'],p['gaze'],p['fear'],-2-p['lean']*.065)
 # All wheel geometry and hand contacts share the same ellipse and rack angle.
 cx,cy,rx,ry,ang=p['wheel'];a.ellipse(cx,cy,rx+4,ry+4,'none',INK,33);a.ellipse(cx,cy,rx+4,ry+4,'none','#4d6a77',16)
 for th in [ang,ang+2.2,ang+4.1]:a.line([(cx,cy),(cx+(rx-22)*math.cos(th),cy-(ry-22)*math.sin(th))],'#294859',24)
 a.ellipse(cx,cy,58,42,'#17303e','#647e8b',4)
 for j,(sh,el,hand) in enumerate(zip(p['shoulders'],p['elbows'],p['hands'])):
  limb(a,[sh,el,hand],'#2a4554',49)
  # Palm/fingers wrap the rim, rather than hovering as a detached oval.
  th=([math.pi*.80,math.pi*.20][j])+ang;rot=-math.degrees(math.atan2(-ry*math.cos(th),-rx*math.sin(th)))
  a.add(f'<g transform="translate({hand[0]} {hand[1]}) rotate({-rot})">')
  a.path('M-24 -19 Q-10 -35 12 -23 Q28 -15 24 12 Q13 29 -5 27 Q-26 18 -24 -19Z','#d9ded3',INK,5)
  for k in range(3):a.path(f'M{-15+k*11} -18 q-5 12 1 22','none','#758c8b',2)
  a.path('M-22 12 q25 -20 40 -4','none','#899e99',3);a.add('</g>')
 # Lower dash is behind caption space; it never hides wheel/hand contact.
 a.path('M0 1510 Q540 1390 1080 1510 V1920 H0Z','#0b1b26',INK,10)
 if mirror:mirror(a,t,(635,280,320,140),False)
 light=max(0,1-abs((s['z']%24)-12)/3)
 a.path(f'M{hx-145} {hy-85} l285 18 -6 56 -280 -18Z','#efb568','none',0,f'opacity="{light*.15}"')
