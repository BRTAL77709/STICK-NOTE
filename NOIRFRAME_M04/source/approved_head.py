"""Approved existing witness head, unchanged geometry from driver_rig.head; new acting is supplied by V11 state."""
from rig import clamp
INK="#030b12"
def head(a,x,y,t,yaw,gaze,fear,tilt=0,blink_override=None):
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
 blink=max(0,1-abs(t-8.44)/.065)+max(0,1-abs(t-37.87)/.065)+max(0,1-abs(t-5.17)/.075)
 if blink_override is not None:blink=clamp(blink_override)
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
