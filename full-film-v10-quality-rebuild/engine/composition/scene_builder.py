"""All 18 scenes, one global clock, shared physical vehicle and interaction state."""
from pathlib import Path
import sys,math,json
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'engine/animation'))
from illustration_engine import Art,Raster
from approved_components import begin,text
from motion_state import state,ease,travel,road_x
from world import Camera,city,INK
from vehicle import sedan
from driver_rig import driver
from driving import pedal
from actor import actor
from choreography import RUN_LOCAL
from render_base import rain,mirror,pov,front_camera
import v10_trunk
import house17
import house_site
import house_actions
import stairs_actions
import room_actions
from film_components import house as facade,car_sprite
SHOTS=json.loads((R/'storyboard.json').read_text())
DEFS='<defs><linearGradient id="citysky" x2="0" y2="1"><stop stop-color="#05111d"/><stop offset="1" stop-color="#345d6b"/></linearGradient><radialGradient id="lamphalo"><stop stop-color="#ffc476" stop-opacity=".35"/><stop offset="1" stop-color="#ffc476" stop-opacity="0"/></radialGradient></defs>'
def extcam(t,low=False,side=False):
 p=state(t);ang=p['yaw'];off=5.2+.45*math.sin(t*.24);back=9.8
 cx=p['x']-math.cos(ang)*off-math.sin(ang)*back;cz=p['z']+math.sin(ang)*off-math.cos(ang)*back
 return Camera(cx,cz,.9 if low else 2.2,math.atan2(p['x']-cx,p['z']-cz),1440,750+.6*math.sin(travel(t)*2.2))
def establish_camera(t):
 # A curbside camera translates only 35% of the car's distance: the car truly
 # passes from a front three-quarter to a rear three-quarter silhouette.
 origin=state(0);p=state(t);cx=origin['x']-8.;cz=origin['z']+4.+.35*(travel(t)-travel(0))
 return Camera(cx,cz,1.35,math.atan2(p['x']-cx,p['z']-cz),1050,820)
def traffic_scene(a,c,t,black=False):
 actors=[]
 for is_black in ([False,True] if black else [False]):
  p=state(t,is_black);actors.append(((p['x'],.8,p['z']),lambda k=is_black:sedan(a,c,t,k)))
 city(a,c,t,traffic=actors);rain(a,t)

def pursuit_camera(t):
 hero=state(t);other=state(t,True);mx=(hero['x']+other['x'])/2;mz=(hero['z']+other['z'])/2;hd=hero['yaw'];cx=mx-4.5*math.cos(hd)-18*math.sin(hd);cz=mz+4.5*math.sin(hd)-18*math.cos(hd)
 return Camera(cx,cz,2.1,math.atan2(mx-cx,mz-cz),1100,725)

def corner_camera(t):
 hero=state(t);other=state(t,True);cz=hero['z']+6;cx=road_x(cz)-6.2;mx=(hero['x']+other['x'])/2;mz=(hero['z']+other['z'])/2
 return Camera(cx,cz,1.5,math.atan2(mx-cx,mz-cz),1350,790)

def body(scene,u,t):
 if scene==1:
  c=establish_camera(t);city(a,c,t);sedan(a,c,t);rain(a,t)
 elif scene==2:driver(a,t,front_camera(t),mirror)
 elif scene==3:
  # Stay with the witness's articulated braking/attention beat. The next
  # protected V10 shot reveals what he sees; an empty-road insert did not.
  driver(a,t,front_camera(t),mirror)
 elif scene==7:
  if u<.55 or u>=1.55:driver(a,t,front_camera(t),mirror)
  else:pedal(a,t)
 elif scene==8:
  if u<3:
   traffic_scene(a,pursuit_camera(t),t,True)
  else:
   city(a,front_camera(t),t);a.path('M0 0 H1080 V460 Q540 360 0 460Z','#08141e',INK,8);mirror(a,t,(65,450,950,625),True);a.path('M0 1160 Q540 1020 1080 1160 V1920 H0Z','#0b1c29',INK,10)
 elif scene==9:
  if u<.7:pov(a,t)
  elif u<3:driver(a,t,front_camera(t),mirror,True)
  else:traffic_scene(a,corner_camera(t),t,True)
 elif scene==10:
  if u<2.8:
   c=extcam(t);city(a,c,t);sedan(a,c,t);rain(a,t)
  else:
   driver(a,t,front_camera(t),mirror)
 elif scene==11:
  house_site.arrival(a,t);rain(a,t)
 elif scene in [12,13]:
  dt=t-51
  if dt<6.4:house_actions.door(a,dt)
  else:stairs_actions.draw(a,t)
 elif scene==14:
  if t<stairs_actions.END:stairs_actions.draw(a,t)
  else:room_actions.draw(a,t)
 elif scene in [15,16,17]:room_actions.draw(a,t)
 elif scene==18:
  a.rect(0,0,1080,1920,'#05111d',sw=0);rain(a,t)

def scene_svg(scene_id,u):
 global a
 s=SHOTS[scene_id-1];t=s['start']+u
 if scene_id in [4,5,6]:
  q=u/6*1.95 if scene_id==4 else (1.95+u/6*4.75 if scene_id==5 else 6.7+u/4*3.3)
  return v10_trunk.scene(q)
 a=Art();begin(a);a.add(DEFS);body(scene_id,u,t);a.add('<rect x="0" y="0" width="1080" height="1920" fill="url(#vignette)" opacity=".62"/>');a.add('</svg>');return ''.join(a.s)
