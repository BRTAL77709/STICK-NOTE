"""Reusable NOIRFRAME state facade. All values derive from the production modules."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));sys.path.insert(0,str(R/'engine/composition'))
from motion_state import vehicleState as _vehicle,state,ease,pursuit_distance
from driver_rig import pose
from house17 import doorState,hardware,HOUSE
from scene_builder import SHOTS,extcam
import v10_trunk

def sceneState(t):return next(s for s in SHOTS if s['start']<=max(0,min(86-1e-8,t))<s['end'])
def vehicleState(vehicleId,t):return {**state(t,vehicleId in ['pursuer','black']),'pursuit_distance_m':pursuit_distance(t)}
def characterState(characterId,t):
 if characterId in ['criminal01','criminal02','victim'] and 12<=t<28:
  q=(t-12)/6*1.95 if t<18 else (1.95+(t-18)/6*4.75 if t<24 else 6.7+(t-24)/4*3.3)
  return v10_trunk.victim_pose(q) if characterId=='victim' else v10_trunk.actor_pose(q,0 if characterId=='criminal01' else 1)
 if t>=47:
  return {'t':t,'mode':'on-foot','scene':sceneState(t)['scene'],'rig':'engine/animation/actor.py','phone':propState('phone',t),'curtain':propState('curtain',t),'door':propState('door',t)}
 return pose(t)
def cameraState(t):
 c=extcam(t,sceneState(t)['scene'] in [1,9]);return {'x':c.x,'z':c.z,'height':c.y,'heading':c.yaw,'focal':c.f,'horizon':c.h,'note':'Street camera; house and alley use the dedicated shared projections in their modules.'}
def environmentState(t):return {'scene':sceneState(t)['scene'],'house':HOUSE,'rain_seed':267,'route':'assets/environments/route-map.json'}
def propState(propId,t):
 if propId in ['door','key','lock','handle']:return {**doorState(t-51),'hardware':hardware(t-51,t>=55.9)}
 if propId=='curtain':return {'pull':ease(t,60.15,61.35),'edge_x':790-280*ease(t,60.15,61.35),'gripped':60.1<=t<63}
 if propId=='phone':
  q=ease(t,64.1,64.65);p=ease(t,64.65,66.45);return {'hand_local':(45+115*q-81*p,-169-31*q-100*p),'held':t>=64.65,'connected':t>=66.45}
 return {}
def lightingState(t):return {'amber_lamp_strength':math.exp(-(((state(t)['z']+192)%24-12)/4.2)**2),'rainy_night':True}
def graphicsState(t):return {'clock':0<=t<4,'pursuit':33.5<=t<37,'speed':37<=t<38.25 or 40<=t<42,'incoming_call':63.1<=t<64.6,'offer':67.3<=t<74,'choice':80<=t<86}
def audioEvents(t,tolerance=1/60):return [x for x in json.loads((R/'sound-cues.json').read_text()) if abs(x['time']-t)<=tolerance]
