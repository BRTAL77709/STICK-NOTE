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
 from film_performance import draw
 draw(a,scene,u,t)

def scene_svg(scene_id,u):
 global a
 s=SHOTS[scene_id-1];t=s['start']+u
 if scene_id in [4,5,6]:
  q=u/6*1.95 if scene_id==4 else (1.95+u/6*4.75 if scene_id==5 else 6.7+u/4*3.3)
  return v10_trunk.scene(q)
 a=Art();begin(a);a.add(DEFS);body(scene_id,u,t);a.add('<rect x="0" y="0" width="1080" height="1920" fill="url(#vignette)" opacity=".25"/>');a.add('</svg>');return ''.join(a.s)
