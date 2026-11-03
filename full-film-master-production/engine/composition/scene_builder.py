"""All 18 scenes, one global clock, shared physical vehicle and interaction state."""
from pathlib import Path
import sys,math,json
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'engine/animation'))
from illustration_engine import Art,Raster
from approved_components import begin,text
from motion_state import state,ease,travel
from world import Camera,city,INK
from vehicle import sedan
from driver_rig import driver
from driving import pedal
from actor import actor
from choreography import RUN_LOCAL
from render_base import rain,mirror,pov,front_camera
import v10_trunk
import house17
from film_components import house as facade,car_sprite
SHOTS=json.loads((R/'storyboard.json').read_text())
DEFS='<defs><linearGradient id="citysky" x2="0" y2="1"><stop stop-color="#05111d"/><stop offset="1" stop-color="#345d6b"/></linearGradient><radialGradient id="lamphalo"><stop stop-color="#ffc476" stop-opacity=".35"/><stop offset="1" stop-color="#ffc476" stop-opacity="0"/></radialGradient></defs>'
def extcam(t,low=False,side=False):
 p=state(t);ang=p['yaw'];off=5.2+.45*math.sin(t*.24);back=9.8
 cx=p['x']-math.cos(ang)*off-math.sin(ang)*back;cz=p['z']+math.sin(ang)*off-math.cos(ang)*back
 return Camera(cx,cz,.9 if low else 2.2,math.atan2(p['x']-cx,p['z']-cz),1440,750+.6*math.sin(travel(t)*2.2))
def body(scene,u,t):
 if scene==1:
  c=extcam(t,True);city(a,c,t);sedan(a,c,t);rain(a,t)
 elif scene==2:driver(a,t,front_camera(t),mirror)
 elif scene==3:
  if u<2.6:driver(a,t,front_camera(t),mirror)
  else:
   p=state(t);c=Camera(p['x'],p['z'],1.35,p['yaw']-.48*ease(u,2.6,4),1150,690);city(a,c,t);rain(a,t)
 elif scene==7:
  if u<.55 or u>=1.55:driver(a,t,front_camera(t),mirror)
  else:pedal(a,t)
 elif scene==8:
  if u<1.5:
   p=state(t);hd=p['yaw'];c=Camera(p['x']-5.5*math.cos(hd)-28*math.sin(hd),p['z']+5.5*math.sin(hd)-28*math.cos(hd),2.0,hd+.20,1440,740);city(a,c,t);sedan(a,c,t);sedan(a,c,t,True);rain(a,t)
  else:
   city(a,front_camera(t),t);a.path('M0 0 H1080 V460 Q540 360 0 460Z','#08141e',INK,8);mirror(a,t,(65,450,950,625),True);a.path('M0 1160 Q540 1020 1080 1160 V1920 H0Z','#0b1c29',INK,10)
 elif scene==9:
  if u<1.25:pov(a,t)
  elif u<3:driver(a,t,front_camera(t),mirror,True)
  else:
   c=extcam(t,True);city(a,c,t);sedan(a,c,t);sedan(a,c,t,True);rain(a,t)
 elif scene==10:
  if u<2.8:
   c=extcam(t);city(a,c,t);sedan(a,c,t);rain(a,t)
  else:
   driver(a,t,front_camera(t),mirror)
 elif scene==11:
  if u<1:
   c=extcam(t);city(a,c,t);sedan(a,c,t);rain(a,t)
  else:
   facade(a,t);q=ease(u,*RUN_LOCAL);d=410*q
   # Actor is occluded by the parked car until the exit step clears its silhouette.
   actor(a,145+d,1770-.36*d,t,d,1,True,yaw=.25,fear=.7,slope=-.36)
   car_sprite(a,130,1780,1.12,'blue','rear',travel(48)*30)
   opening=ease(u,1,1.3)*(1-ease(u,1.6,1.95));a.poly([(220,1590),(220+110*opening,1567),(220+120*opening,1710),(220,1705)],'#3b596c','#708b98',5)
 elif scene in [12,13]:
  dt=t-51
  if dt<6.25:house17.door(a,dt)
  else:house17.stairs(a,dt-6.25,t)
 elif scene==14:
  if t<59.4:house17.stairs(a,t-57.25,t)
  else:house17.room(a,t,ease(t,60.15,61.35),looking=True)
 elif scene==15:
  q=ease(t,64.1,64.65);raiseq=ease(t,64.65,66.45);target=(45+115*q-81*raiseq,-169-31*q-100*raiseq)
  house17.room(a,t,1,phone=True,phone_hand=target,phone_visible=t>=64.65)
  if t<64.65:
   vib=2*math.sin(t*65);a.add(f'<g transform="translate({750+vib} 1300) rotate(-12)">');a.rect(-24,-63,48,126,'#06131c','#a2b0b0',4,8);a.rect(-16,-48,32,94,'#314e5c');a.add('</g>')
 elif scene in [16,17]:house17.room(a,t,1,phone=True)
 elif scene==18:
  house17.room(a,t,1,phone=True);a.rect(0,0,1080,1920,'#05111d',sw=0);rain(a,t)

def scene_svg(scene_id,u):
 global a
 s=SHOTS[scene_id-1];t=s['start']+u
 if scene_id in [4,5,6]:
  q=u/6*1.95 if scene_id==4 else (1.95+u/6*4.75 if scene_id==5 else 6.7+u/4*3.3)
  return v10_trunk.scene(q)
 a=Art();begin(a);a.add(DEFS);body(scene_id,u,t);a.add('<rect x="0" y="0" width="1080" height="1920" fill="url(#vignette)" opacity=".62"/>');a.add('</svg>');return ''.join(a.s)
