"""Native hierarchy, actual wheel-parented IK grip targets, shared architecture and rigid phone."""
import bpy,numpy as np
from mathutils import Vector
from embed_assets import empty,mesh,key
from world import World,Camera
from contact_rig import V
from spatial_world import house
from cameras import camera

def complete(scene,shot,states):
 world=empty(scene,'WORLD_ROOT');groups={n:empty(scene,n) for n in ['CITY','ROAD_NETWORK','HOUSE_17','WITNESS_CAR','BLACK_SEDAN','CHARACTER_RIGS','PROPS','CAMERA_RIGS','LIGHTS','AUDIO']}
 for o in groups.values():o.parent=world
 for o in list(scene.objects):
  if o==world or o in groups.values() or o.parent:continue
  if o.type=='ARMATURE' or o.name.startswith(('CTRL_','M07_','M04_','APPROVED_','SLEEVE_','SHOE_','MITTEN_','PANTS_')):o.parent=groups['CHARACTER_RIGS']
  elif o.type=='LIGHT':o.parent=groups['LIGHTS']
  elif o.type=='CAMERA':o.parent=groups['CAMERA_RIGS']
  else:o.parent=groups['PROPS']
 if shot in ['DRIVING_COCKPIT','DRIVER_CHASE','DISCOVERY','PANIC']:
  car=bpy.data.objects['CAR_ROOT'];car.parent=groups['WITNESS_CAR'];rig=empty(scene,'STABILIZED_REAR_SEAT_CAMERA');rig.parent=car;scene.camera.parent=rig;axis=bpy.data.objects['STEERING_COLUMN_AXIS']
  grips={s:empty(scene,('LEFT' if s=='L' else 'RIGHT')+'_HAND_GRIP_TARGET') for s in ['L','R']}
  for g in grips.values():g.parent=axis
  for i,d in enumerate(states):
   scene.frame_set(i);bpy.context.view_layer.update()
   for s,g in grips.items():g.location=axis.matrix_world.inverted()@bpy.data.objects['M07_WRIST_'+s].matrix_world.translation;g.keyframe_insert('location',frame=i)
  for s,g in grips.items():
   target=bpy.data.objects['M07_WRIST_'+s];c=target.constraints.new('COPY_LOCATION');c.name='M11_WHEEL_PARENTED_GRIP';c.target=g;c.owner_space='WORLD';c.target_space='WORLD'
  for g in grips.values():
   for fc in g.animation_data.action.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
 if shot=='STAIRS':
  # Export all faces by collecting opposing views, not a camera-facing cardboard set.
  seen=set()
  for eye in [(8,3,3),(-8,3,3),(0,3,-5),(0,3,12),(0,10,3),(0,-4,3)]:
   w=World(Camera(eye,(0,2,3)));house(w)
   import sets,actions
   sets.door_live(w,actions.baseline('DOOR_ENTRY',15.999))
   for g in w.geometry:
    sig=tuple(sorted(tuple(round(x,5) for x in q) for q in g['vertices']))
    if sig in seen:continue
    seen.add(sig);mesh(scene,'M11_'+g['name']+'_'+str(len(seen)),g['vertices'],[tuple(range(len(g['vertices'])))],g['color'],groups['HOUSE_17'])
 if shot in ['PHONE_CALL','UNKNOWN_CALLER']:
  phone=empty(scene,'PHONE_GRIP_ROOT');phone.parent=groups['PROPS'];mesh(scene,'PHONE_RIGID_BODY',[V(x,y,z) for z in [-.012,.012] for x,y in [(-.039,-.08),(.039,-.08),(.039,.08),(-.039,.08)]],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],'#203947',phone)
  mesh(scene,'PHONE_GLASS_CONTACT_SURFACE',[V(x,y,-.014) for x,y in [(-.033,-.071),(.033,-.071),(.033,.067),(-.033,.067)]],[(0,1,2,3)],'#568091',phone)
  for i,d in enumerate(states):key(scene,phone,i,d['phone_position'],d['phone_R'])
 # Physical area-light locations mirror the procedural cel-light sources.
 lamps=[(-2.23,1.95,1.),(-2.23,1.95,3.5),(-2.23,1.95,5.3)] if shot=='STAIRS' else [(.72,1.55,-3.9)] if shot in ['WINDOW_CURTAIN','PHONE_CALL','UNKNOWN_CALLER'] else []
 for j,p in enumerate(lamps):
  data=bpy.data.lights.new('M11_WARM_FIXTURE_'+str(j),'POINT');data.color=(1.,.58,.25);data.energy=45;data.shadow_soft_size=.1;o=bpy.data.objects.new(data.name,data);scene.collection.objects.link(o);o.parent=groups['LIGHTS'];o.location=(p[2],p[0],p[1])
 scene['M11_units']='metres; Blender XYZ = renderer ZXY';scene['M11_geometry']='Native evaluated armature/skin, actual no-stretch IK, native props and cameras. Final illustrated composition uses Python cel renderer and registered world/mirror definitions.';scene['M11_physics_scope']='Authored kinematic contacts, not force-based balance/cloth/hand friction simulation.'
