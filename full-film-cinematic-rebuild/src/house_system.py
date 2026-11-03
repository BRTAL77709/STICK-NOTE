"""House17 geometry/interaction prototype; not integrated full-film footage."""
from pathlib import Path
import math,json
from illustration_engine import Art,Raster,ik,limb
from approved_components import begin,text
from motion_state import ease
from world import Camera,city
DOOR={'hinge':(0.,0.,0.),'width':1.,'height':2.1,'lock':(.84,1.1),'handle':(.84,.95),'insertion_m':.035}
HOUSE={'facade_width_m':8,'floor_to_floor_m':3,'door_facade_x_m':-1.1,'window_facade_x_m':1.4,'window_sill_m':3.8,'curb_to_facade_m':6}
def lock_state(t):
 # Explicit order: failed handle, align, insert, turn, withdraw, then open.
 insertion=ease(t,1.3,1.7)*(1-ease(t,2.4,2.7));turn=math.pi/2*ease(t,1.8,2.25);open_angle=math.radians(62)*ease(t,2.85,4)
 return {'key_insertion_m':.035*insertion,'key_turn_rad':turn,'handle_angle_deg':-18*(ease(t,0,.3)*(1-ease(t,.4,.6))+ease(t,2.7,2.9)),'latch_released':t>=2.85,'door_yaw':open_angle,'locked':t<2.25}
def door_point(x,y,z,t):
 q=lock_state(t)['door_yaw'];return x*math.cos(q)+z*math.sin(q),y,z*math.cos(q)-x*math.sin(q)
def prototype(t):
 a=Art();begin(a);a.rect(0,0,1080,1920,'#132a37');c=Camera(.45,-3.4,1.25,0,1300,970)
 # Door frame is fixed, leaf/hardware rotate about a single real hinge.
 c.poly(a,[(-.1,0,.04),(1.1,0,.04),(1.1,2.22,.04),(-.1,2.22,.04)],'#4d6671','#9aa8a4',4)
 c.poly(a,[(0,0,.02),(1,0,.02),(1,2.1,.02),(0,2.1,.02)],'#040b12','none',0)
 def pp(x,y,z=0):return door_point(x,y,z,t)
 c.poly(a,[pp(0,0),pp(1,0),pp(1,2.1),pp(0,2.1)],'#1b3544','#6b8187',5)
 for yy in [.25,1.3]:c.poly(a,[pp(.12,yy,-.015),pp(.88,yy,-.015),pp(.88,yy+.55,-.015),pp(.12,yy+.55,-.015)],'#18303e','#4c6572',2)
 for yy in [.25,1.8]:c.line(a,[pp(.015,yy,-.035),pp(.015,yy+.13,-.035)],'#b3b6a7',7)
 st=lock_state(t);hx,hy=DOOR['handle'];ang=math.radians(st['handle_angle_deg']);c.line(a,[pp(hx,hy,-.04),pp(hx+.13*math.cos(ang),hy+.13*math.sin(ang),-.04)],'#d2ac6d',10)
 # Cylinder and keyhole explicitly rotate with leaf; key shaft enters along normal.
 lx,ly=DOOR['lock'];X,Y=c.project(pp(lx,ly,-.045));a.ellipse(X,Y,19,23,'#b18e56','#06121c',4);a.path(f'M{X} {Y-7} l0 13','none','#08131c',4)
 if t<2.85:
  align=ease(t,.6,1.3);gap=.20*(1-align);depth=st['key_insertion_m'];ring=pp(lx,ly,-.16-gap+depth);tip=pp(lx,ly,-gap+depth);R=c.project(ring);T=c.project(tip)
  a.line([R,T],'#c3c8b8',8)
  # Bow/fingers held at exactly the shaft endpoint; cylinder turn rolls both.
  a.add(f'<g transform="rotate({math.degrees(st["key_turn_rad"])} {R[0]} {R[1]})">');a.ellipse(*R,20,14,'none','#c7ad78',6);a.line([(R[0]+5,R[1]-8),(T[0],T[1]-8)],'#adb3a4',4);a.add('</g>')
  hand=(R[0]+28,R[1]+8);shoulder=(940,1340);el=ik(shoulder,hand,220,215,-1);limb(a,[shoulder,el,hand],'#294452',55);a.ellipse(*hand,28,35,'#e0dfd2','#020b13',5)
  for j in range(3):a.line([(R[0]+11+j*7,R[1]-9),(R[0]+13+j*7,R[1]+8)],'#7c918d',2)
 text(a,540,330,'HOUSE 17',66,'#e2b477');text(a,540,1560,'INTERACTION PROTOTYPE',34,'#bacbcc');a.add('</svg>');return ''.join(a.s)
def main():
 root=Path(__file__).resolve().parents[1];rr=Raster(270,480)
 from PIL import Image,ImageDraw
 out=Image.new('RGB',(1620,500),'#08131c');d=ImageDraw.Draw(out)
 for j,t in enumerate([.25,1.2,1.7,2.25,2.7,3.8]):
  out.paste(rr.render(prototype(t)),(j*270,0));d.text((j*270+8,480),f'{t:.2f}s',fill='white')
 dest=root/'previews/HOUSE17_LOCK_PROTOTYPE.jpg';assert not dest.exists();out.save(dest,quality=94)
 (root/'plan/house_geometry.json').write_text(json.dumps({'house':HOUSE,'door':DOOR},indent=2))
if __name__=='__main__':main()
