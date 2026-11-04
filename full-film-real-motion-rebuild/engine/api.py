"""State facade for the actual real-motion film and the independently rendered proofs."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'))
import motion_state as motion,physical_proofs as proof,film_performance as film,house_site as site,house_actions as door,room_actions as room,v10_trunk as v10
from driver_rig import pose as driver_pose
from render_base import front_camera
SHOTS=json.loads((R/'storyboard.json').read_text())
def sceneState(t):return next(s for s in SHOTS if s['start']<=max(0,min(85.999999,t))<s['end'])
def _q(t):return (t-12)/6*1.95 if t<18 else 1.95+(t-18)/6*4.75 if t<24 else 6.7+(t-24)/4*3.3
def vehicleState(vehicleId,t):return {**motion.state(t,vehicleId in ('black','pursuer')),'pursuit_distance_m':motion.pursuit_distance(t)}
def characterState(characterId,t):
 if characterId in ('criminal01','criminal02','victim'):
  if not 12<=t<28:return {'mode':'offscreen'}
  return v10.victim_pose(_q(t)) if characterId=='victim' else v10.actor_pose(_q(t),int(characterId=='criminal02'))
 if t>=film.CHOICE:return {'mode':'offscreen / choice'}
 if 28<=t<31:return {'mode':'footwell performance','rig':proof.accelerator(t-28)}
 if t<48.02:return {'mode':'seated','rig':driver_pose(t)}
 if t<51:
  c=site.exit_camera(t) if t<site.RUN_START else site.run_camera(t);return {'mode':'exit/run','rig':site.actor_state(t,c),'space':'metric house_site plus projected local joints'}
 if t<film.STAIR_START:return {'mode':'door/key/entry','rig':proof.door_state(t-51),'space':'door-local metres / projected local joints'}
 if t<film.CURTAIN_START:
  d=proof.stair_state(t-film.STAIR_START,2.16);return {'mode':'upper-three-stairs','rig':d,'space':'metric upper flight; floor 2.7 m','door_local_registration_offset':[-1.97,0,1.3375],'continuity':'Cut implies the unshown lower flight; three upper steps are animated in full.'}
 if t<film.PHONE_START:return {'mode':'curtain','rig':film.curtain_state(t)}
 return {'mode':'phone/offer/threat','rig':film.call_state(t)}
def cameraState(t):
 n=sceneState(t)['scene'];u=t-sceneState(t)['start']
 if n in [4,5,6]:return {'type':'preserved V10 projection','reference_time':_q(t)}
 if n==1:c=film.passing_camera(t,0,2)
 elif n in [2,3] or n==7 and u>=3:c=front_camera(t)
 elif n==7:return {'type':'fixed footwell / continuous 3 s'}
 elif n==8:c=film.pursuit_camera(t)
 elif n==9:c=front_camera(t) if u<3 else film.corner_camera(t)
 elif n==10:c=film.corner_camera(t) if u<2.5 else front_camera(t)
 elif n==11:c=site.wide_camera(t) if t<48.02 else site.exit_camera(t) if t<site.RUN_START else site.run_camera(t)
 elif n in [12,13]:c=proof.door_state(t-51)['camera']
 elif n==14:return {'type':'fixed upper-flight orthographic projection','formula':'physical_proofs.stair_state.project','upper_floor':2.7}
 elif n==15:c=film.curtain_state(t)['camera']
 elif n in [16,17]:c=film.call_state(t)['camera']
 else:return {'type':'choice graphics'}
 c=c.camera if hasattr(c,'camera') else c;return {'x':c.x,'z':c.z,'height':c.y,'heading':c.yaw,'focal':c.f,'horizon':c.h}
def propState(propId,t):
 if propId in ('door','handle','lock','key'):
  d=proof.door_state(max(0,min(10.4,t-51)));return d['key'] if propId=='key' else {'state':door.doorState(d['reference_time']),'hardware':door.hardware(d['reference_time'],t>59.5)}
 if propId=='trunk':return {'angle':v10.lid_angle(_q(t))} if 12<=t<28 else {'visible':False}
 if propId=='driver_door':return {'angle':site.car_door_angle(t),'handle':site.car_handle(t)}
 if propId=='curtain':return {'edge':room.curtain_edge(proof.remap(t-film.CURTAIN_START,proof.CLOTH_KNOTS)),'reference':'physical_proofs.curtain_state'}
 if propId=='phone':
  d=film.call_state(max(film.PHONE_START,min(film.CHOICE,t)));return {k:d[k] for k in ('phone_pixel','phone_scale','phone_angle','phone_grip','phone_held','ear_contact')}
 return {}
def graphicsState(t):return {'clock':0<=t<4,'speed_rpm':False,'pursuit_dashboard':False,'incoming':69.6<=t<70.25,'offer':72.47<=t<77.3,'choice':81.5<=t<86}
def environmentState(t):return {'house':json.loads((R/'HOUSE17_PLAN.json').read_text()),'rainy_night':True,'scene':sceneState(t)['scene']}
def lightingState(t):return {'amber_lamp_strength':math.exp(-(((motion.state(t)['z']+192)%24-12)/4.2)**2)}
def audioEvents(t,tolerance=1/60):return [x for x in json.loads((R/'CONTACT_SOUND_CUES.json').read_text()) if abs(x['time']-t)<=tolerance]
