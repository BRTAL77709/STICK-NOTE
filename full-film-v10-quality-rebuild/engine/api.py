"""Public facade over the actual scene rigs and their shared 86-second clock."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));sys.path.insert(0,str(R/'engine/composition'))
from motion_state import state,ease,pursuit_distance
from driver_rig import pose as driver_pose
from scene_builder import SHOTS,extcam,establish_camera,pursuit_camera,corner_camera
from render_base import front_camera
import v10_trunk,house_site as site,house_actions as door,stairs_actions as stairs,room_actions as room

def sceneState(t):return next(s for s in SHOTS if s['start']<=max(0,min(86-1e-8,t))<s['end'])
def _q(t):return (t-12)/6*1.95 if t<18 else 1.95+(t-18)/6*4.75 if t<24 else 6.7+(t-24)/4*3.3
def _camera(c):
 b=c.camera if hasattr(c,'camera') else c
 return {'x':b.x,'z':b.z,'height':b.y,'heading':b.yaw,'focal':b.f,'horizon':b.h,'space':'world metres'}
def vehicleState(vehicleId,t):return {**state(t,vehicleId in ['pursuer','black']),'pursuit_distance_m':pursuit_distance(t)}
def characterState(characterId,t):
 if characterId in ['criminal01','criminal02','victim'] and 12<=t<28:
  return v10_trunk.victim_pose(_q(t)) if characterId=='victim' else v10_trunk.actor_pose(_q(t),0 if characterId=='criminal01' else 1)
 if characterId not in ['witness','protagonist']:return {'mode':'offscreen','character':characterId}
 if t<48.02:return {'mode':'seated','rig':driver_pose(t)}
 if t<51:
  c=site.exit_camera(t) if t<site.RUN_START else site.run_camera(t);d=site.actor_state(t,c);r=site.W(*d['root_site']);fs=[(site.W(*p),on) for p,on in d['feet_world']]
 elif t<stairs.T0:
  d=door.actor_state(t-51);r=site.door_world(d['root']);fs=[(site.door_world(p),on) for p,on in d['feet_world']]
 elif t<stairs.END:
  d=stairs.actor_state(t);r=site.door_world(d['root']);fs=[(site.door_world(p),on) for p,on in d['feet']]
 else:
  d=room.actor_state(min(t,80));r=site.door_world(d['root']);fs=[(site.door_world(p),on) for p,on in d['feet']]
 return {'mode':'on-foot' if t<80 else 'offscreen during choice','root_world':r,'feet_world':fs,'pose':d['pose'],'projection_origin_px':[d['x'],d['y']],'rig_scale':d['scale'],'rig':'engine/animation/articulated.py'}
def cameraState(t):
 scene=sceneState(t)['scene'];u=t-sceneState(t)['start']
 if scene in [4,5,6]:return {'type':'preserved V10 orthographic/cinematic projection','approved_time':_q(t)}
 if scene==1:c=establish_camera(t)
 elif scene in [2,3]:c=front_camera(t)
 elif scene==7:
  if .55<=u<1.55:return {'type':'articulated footwell insert','rig':'driving.pedal_pose','global_time':t}
  c=front_camera(t)
 elif scene==8:c=pursuit_camera(t) if u<3 else front_camera(t)
 elif scene==9:c=front_camera(t) if u<3 else corner_camera(t)
 elif scene==10:c=extcam(t) if u<2.8 else front_camera(t)
 elif scene==11:c=site.wide_camera(t) if t<48.02 else site.exit_camera(t) if t<site.RUN_START else site.run_camera(t)
 elif scene in [12,13]:c=door.camera(t-51) if t<stairs.T0 else stairs.camera(t)
 elif scene==14:c=stairs.camera(t) if t<stairs.END else room.camera(t)
 elif scene in [15,16,17]:c=room.camera(t)
 else:return {'type':'preserved choice graphics / animated rain'}
 return _camera(c)
def environmentState(t):return {'scene':sceneState(t)['scene'],'house':json.loads((R/'HOUSE17_PLAN.json').read_text()),'rain_seed':267,'route':'assets/environments/route-map.json'}
def propState(propId,t):
 if propId in ['door','lock','handle']:return {**door.doorState(t-51),'hardware_door_local':door.hardware(t-51,t>=55.3),'frame':'house_site.door_world'}
 if propId=='key':return door.actor_state(t-51)['key'] if 51<=t<=53.55 else {'location':'pocket','rendered':False}
 if propId=='driver_door':return {'angle':site.car_door_angle(t),'handle_world':site.car_handle(t),'hand_handoff':48.82<=t<48.94}
 if propId=='trunk':return {'angle':v10_trunk.lid_angle(_q(t)),'approved_time':_q(t)} if 12<=t<28 else {'visible':False}
 if propId=='curtain':return {'edge_door_local':room.curtain_edge(t),'pull':ease(t,61.6,62.2),'gripped':61.6<=t<62.35}
 if propId=='phone':
  if t<room.ENTER:return {'visible':False}
  d=room.actor_state(min(t,80));return {k:d[k] for k in ['phone_pixel','phone_scale','phone_angle','phone_held','phone_grip','phone_owner','ear_contact']}
 return {}
def lightingState(t):return {'amber_lamp_strength':math.exp(-(((state(t)['z']+192)%24-12)/4.2)**2),'rainy_night':True}
def graphicsState(t):return {'clock':0<=t<4,'pursuit':33.5<=t<37,'speed_rpm':32<=t<33.4,'velocity':40<=t<42,'incoming_call':63.1<=t<63.8,'offer':67.65<=t<74,'counter_start':67.762,'choice':80<=t<86}
def audioEvents(t,tolerance=1/60):return [x for x in json.loads((R/'CONTACT_SOUND_CUES.json').read_text()) if abs(x['time']-t)<=tolerance]
