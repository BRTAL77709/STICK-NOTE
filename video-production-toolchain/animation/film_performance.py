"""Master integration of technically checked motion proofs; one global clock."""
import math
from motion_state import state,ease,travel
from world import Camera,city
from vehicle import sedan
from render_base import rain,mirror,front_camera
from driver_rig import driver
import house_site as site
import physical_proofs as proof
import room_actions as room
# Three visible upper risers; the cut from the hall implies the unseen lower flight.
STAIR_START=61.4;CURTAIN_START=65.4;PHONE_START=69.4;OFFER=72.5;THREAT=77.3;CHOICE=81.5
CALL_MAP=[(69.4,63.05),(69.6,63.1),(70.15,63.6),(70.65,64.15),(70.75,64.2),(71.45,64.95),(72.4,65.8),(72.5,67.7),(73.2,68.4),(74.55,69.8),(75.,70.2),(76.3,71.7),(77.2,72.4),(77.3,74.6284),(77.65,75.),(78.25,75.6),(79.,77.),(79.75,77.6),(81.5,80.)]
STAIR_END_FEET=[(p[0]-1.97,p[1],p[2]+1.3375) for p,on in proof.stair_state(4,2.16)['feet']]
def curtain_state(t):return proof.curtain_state(t-CURTAIN_START,initial_feet=STAIR_END_FEET)
def call_reference(t):return proof.remap(t,CALL_MAP)
def call_state(t):
 d=room.actor_state(call_reference(t));d['global_time']=t;return d

def passing_camera(t,start,pass_time,lateral=6.5):
 target=state(pass_time);hero=state(t);yaw=target['yaw'];cx=target['x']-lateral*math.cos(yaw);cz=target['z']+lateral*math.sin(yaw)
 # A planted curb camera pans toward the actual moving vehicle. Silhouette changes
 # front-to-side-to-rear because the car genuinely passes the fixed camera site.
 return Camera(cx,cz,1.3,math.atan2(hero['x']-cx,hero['z']-cz),1050,900)
def traffic(a,c,t,black=True):
 vehicles=[]
 for b in ([False,True] if black else [False]):
  s=state(t,b);vehicles.append(((s['x'],.8,s['z']),lambda b=b:sedan(a,c,t,b)))
 city(a,c,t,traffic=vehicles);rain(a,t)
def pursuit_camera(t):
 h=state(t);b=state(t,True);mx=(h['x']+b['x'])/2;mz=(h['z']+b['z'])/2;hd=h['yaw'];back=18+2.0*math.sin(math.pi*ease(t,32,37));cx=mx-4.5*math.cos(hd)-back*math.sin(hd);cz=mz+4.5*math.sin(hd)-back*math.cos(hd)
 return Camera(cx,cz,2.1,math.atan2(mx-cx,mz-cz),1100,725)
def corner_camera(t):
 s=state(t);yaw=s['yaw'];cx=s['x']-8*math.cos(yaw)-10*math.sin(yaw);cz=s['z']+8*math.sin(yaw)-10*math.cos(yaw);return Camera(cx,cz,1.35,math.atan2(s['x']-cx,s['z']-cz),1350,850)
def draw(a,scene,u,t):
 if scene==1:traffic(a,passing_camera(t,0,2),t,False)
 elif scene in [2,3]:driver(a,t,front_camera(t),mirror)
 elif scene==7:
  if u<3:proof.draw_accelerator(a,u)
  else:driver(a,t,front_camera(t),mirror)
 elif scene==8:traffic(a,pursuit_camera(t),t,True)
 elif scene==9:
  if u<3:driver(a,t,front_camera(t),mirror,True)
  else:traffic(a,corner_camera(t),t,True)
 elif scene==10:
  if u<2.5:traffic(a,corner_camera(t),t,False)
  else:driver(a,t,front_camera(t),mirror)
 elif scene==11:site.arrival(a,t);rain(a,t)
 elif scene in [12,13]:proof.draw_door(a,t-51)
 elif scene==14:proof.draw_stairs(a,t-STAIR_START,base=2.16)
 elif scene==15:proof.draw_curtain(a,t-CURTAIN_START,initial_feet=STAIR_END_FEET)
 elif scene in [16,17]:room.draw(a,call_reference(t),actor_override=call_state(t))
 elif scene==18:a.rect(0,0,1080,1920,'#05111d',sw=0);rain(a,t)
