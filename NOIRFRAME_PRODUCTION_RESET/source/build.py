"""Create editable native .blend shots and bake deterministic controls, not rendered SVG frames."""
import bpy,sys,math,json,argparse,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
from rigs import *
from world import Car,street,house17,stairs_window
from actions import *
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];p=argparse.ArgumentParser();p.add_argument('--shot',choices=list('ABC'),required=True);p.add_argument('--stage',choices=['inspect','preview','final','bake'],default='inspect');p.add_argument('--version',default='v1');a=p.parse_args(args);kind=a.shot;duration=DURATIONS[kind];N=round(duration*30)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8 if a.stage=='final' else 1;s.cycles.use_denoising=False;s.cycles.max_bounces=1;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=25 if a.stage in ['preview','inspect'] else 100;s.render.fps=30;s.frame_start=1;s.frame_end=N;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.world=bpy.data.worlds.new('Night navy');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.004,.012,.020,1)
s.render.use_freestyle=True;settings=s.view_layers[0].freestyle_settings;ls=settings.linesets[0];ls.linestyle=bpy.data.linestyles.new('Bold illustrated ink');ls.linestyle.color=(.002,.005,.009);ls.linestyle.thickness=2.3;ls.select_crease=False;ls.select_border=True;ls.select_silhouette=True
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Readable action camera';s.camera=cam;cam.data.type='PERSP' if kind=='A' else 'ORTHO';cam.data.lens=50;cam.data.ortho_scale=3.65 if kind=='B' else 4.0
actor=Character('Approved witness',1)
if kind=='A':street();car=Car('Witness driving sedan')
elif kind=='B':cube('Wet approach',(0,0,-.07),(12,10,.14),mat('Pavement','#102c3b'));hinge,spindle,keyobj=house17()
else:
 cam.data.type='PERSP';cam.data.lens=64
 outside=stairs_window();clothverts=[curtain(0,v/20,u/16) for v in range(21) for u in range(17)];cloth=mesh('Curtain articulated cloth',clothverts,[(v*17+u,v*17+u+1,(v+1)*17+u+1,(v+1)*17+u) for v in range(20) for u in range(16)],cloth_material());cloth.shape_key_add(name='Basis')
# Actual rain travels in the 3D world; its seeded positions are independent of the camera.
rng=random.Random(1702);rain=[]
raincollection=bpy.data.collections.new('Rain without ink contours');s.collection.children.link(raincollection);ls.select_by_collection=True;ls.collection=raincollection;ls.collection_negation='EXCLUSIVE'
if kind in ['A','B','C']:
 for j in range(320 if kind=='A' else 160 if kind=='B' else 60):
  x=rng.uniform(-6,34) if kind=='A' else rng.uniform(-4,5) if kind=='B' else rng.uniform(1.5,3.8);y=rng.uniform(-2.5,2.5) if kind=='A' else rng.uniform(-1.8,-.6) if kind=='B' else rng.uniform(3,10);z=rng.uniform(0,5);o=line('Rain world streak',[(0,0,0),(-.04,0,-.25)],.005,mat('Rain','#5f8091'));raincollection.objects.link(o)
  for col in list(o.users_collection):
   if col!=raincollection:col.objects.unlink(o)
  rain.append((o,x,y,z))
for o in list(bpy.data.objects):
 if o.type=='MESH' and any(tag in o.name for tag in ['hoodie','grounded shoe','fixed body shell',' roof']):
  bevel=o.modifiers.new('Illustrated rounded contour','BEVEL');bevel.width=.025 if 'hoodie' in o.name or 'shoe' in o.name else .04;bevel.segments=3
report=[];keyheld=[];foot_yaw=[None,None];last_planted=[False,False]
for f in range(1,N+1):
 t=(f-1)/30;s.frame_set(f);d=SHOTS[kind](t);actor.pose(f,d['root'],d['yaw'],d['feet'],d['hands'],d['lean'],d['head_yaw'],d['fear'])
 if kind=='A':
  q=d['car'];car.pose(f,q['x'],q['y'],q['yaw'],q['distance'],q['steer'],q['pitch']);bpy.context.view_layer.update();body=car.body.matrix_world.copy();driverroot=body@Vector((.08,-.43,-.375));driverfeet=[body@Vector((.46+.06*j,-.43+.16*(j-.5),.16)) for j in range(2)];theta=q['steer']*7;driverhands=[car.wheel.matrix_world@Vector((0,-.14 if j==0 else .14,0)) for j in range(2)];actor.pose(f,driverroot,d['yaw'],driverfeet,driverhands,d['lean'],d['head_yaw'],d['fear']);actor.root.rotation_euler.x=q['pitch'];key(actor.root,f)
  for foot in actor.feet:foot.rotation_euler.x=q['pitch'];key(foot,f,('rotation_euler',))
  d.update(root=driverroot,feet=driverfeet,hands=driverhands)
  target=Vector((.96*q['x']+.4,q['y'],.80));offset=Vector((7.0,-3.0,2.1));cam.location=target+offset;cam.data.lens=30
  if 1.40<=t<3.40:
   bpy.context.view_layer.update();target=actor.head.matrix_world.translation.copy()+Vector((0,0,-.06));cam.location=body@Vector((.85,-.43,1.17));cam.data.lens=20
  cam.data.keyframe_insert('lens',frame=f)
 elif kind=='B':
  hinge.rotation_euler.z=d['door_angle'];spindle.rotation_euler.y=-d['handle_angle'];key(hinge,f,('rotation_euler',));key(spindle,f,('rotation_euler',));keyobj.location=d['keybow'];keyobj.rotation_euler=(0,d['keyturn'],0);keyobj.scale=(1,1,1) if d['key_visible'] else (.001,)*3;key(keyobj,f,('location','rotation_euler','scale'));actor.head.rotation_euler.x=.25*ease(t,2.75,3.4)*(1-ease(t,4.48,4.65));key(actor.head,f,('rotation_euler',));actor.hands[0].rotation_euler.y=d['keyturn'] if d['key_visible'] else 0;key(actor.hands[0],f,('rotation_euler',));keyheld.append({'frame':f,'visible':d['key_visible'],'turn':d['keyturn'],'inserted':d['key_inserted']});target=Vector((float(d['root'][0])+.25,-.1,.96));cam.location=target+Vector((2.1,-6.5,1.1));cam.data.ortho_scale=3.65
  if 2.75<=t<4.55:target=Vector((1.86,-.04,1.0));cam.location=target+Vector((1.9,-5,1.1));cam.data.ortho_scale=1.65
  cam.data.keyframe_insert('ortho_scale',frame=f)
 else:
  actor.root.pose.bones['torso'].rotation_euler.z=d.get('side_lean',0);actor.root.pose.bones['torso'].keyframe_insert('rotation_euler',frame=f)
  # Per-frame shape keys preserve the draped mesh and the gripped edge in the editable file.
  if t>=4.1:
   sk=cloth.shape_key_add(name=f'Fabric pose {f:03}')
   for v in range(21):
    for u in range(17):sk.data[v*17+u].co=curtain(t,v/20,u/16)
   for ff,value in [(f-1,0),(f,1),(f+1,0)]:sk.value=value;sk.keyframe_insert('value',frame=ff)
  lookx=float(d['root'][0])+.20;target=Vector((lookx,.0,1.50));cam.location=target+Vector((.0,-7,1.35))
 if kind!='A':
  for j in range(2):
   if foot_yaw[j] is None or not d['planted'][j] or not last_planted[j]:foot_yaw[j]=d['yaw']
   actor.feet[j].rotation_euler.z=foot_yaw[j];key(actor.feet[j],f,('rotation_euler',));last_planted[j]=d['planted'][j]
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();key(cam,f)
 for o,x,y,z in rain:
  o.location=(x,y,(z-t*5.5)%5.0);key(o,f,('location',))
  if kind=='A':
   rainlocal=car.root.matrix_world.inverted()@o.location;o.hide_render=abs(rainlocal.x)<2.5 and abs(rainlocal.y)<1.05 and rainlocal.z<1.65;o.keyframe_insert('hide_render',frame=f)
 s.frame_set(f);bpy.context.view_layer.update();res=actor.residuals()
 prop_error=None
 if kind=='A':
  inverse=car.wheel.matrix_world.inverted();prop_error=max(math.hypot((inverse@h.location).x,math.hypot((inverse@h.location).y,(inverse@h.location).z)-.14) for h in actor.hands)
 elif kind=='B' and d['hand_contact']:
  actual=spindle.matrix_world@Vector((.065,0,0));prop_error=(actual-actor.hands[0].location).length
 elif kind=='C' and d['hand_contact']:
  evaluated=cloth.evaluated_get(bpy.context.evaluated_depsgraph_get());actual=cloth.matrix_world@evaluated.data.vertices[17].co;prop_error=(actual-actor.hands[0].location).length
 prop_state={}
 if kind=='A':prop_state={'car_world':list(car.root.location),'wheel_rad':[o.rotation_euler.y for _,o,_ in car.wheels],'steer_rad':[o.rotation_euler.z for o,_,_ in car.wheels],'pitch':car.body.rotation_euler.y,'speed_mps':d['car']['speed'],'distance_m':d['car']['distance']}
 elif kind=='B':prop_state={'door_hinge_rad':hinge.rotation_euler.z,'handle_rad':spindle.rotation_euler.y,'key_tip_world':list(keyobj.matrix_world@Vector((0,.15,0))),'key_bow_world':list(keyobj.location),'key_visible':d['key_visible'],'key_inserted':d['key_inserted']}
 else:prop_state={'cloth_grip_world':list(curtain(t)),'hand_holds_cloth':d['hand_contact']}
 report.append({'frame':f,'time':t,'root':list(d['root']),'feet':[list(x) for x in d['feet']],'hands':[list(x) for x in d['hands']],'planted':d['planted'],'IK_residuals_m':res,'head_yaw':d['head_yaw'],'actual_prop_contact_error_m':prop_error,'joint_world_m':{b.name:{'head':list(actor.root.matrix_world@b.head),'tail':list(actor.root.matrix_world@b.tail)} for b in actor.root.pose.bones},'foot_control_world':[list(o.matrix_world.translation) for o in actor.feet],'foot_yaw':[o.rotation_euler.z for o in actor.feet],'prop_state':prop_state,'camera':{'location':list(cam.location),'rotation':list(cam.rotation_euler),'type':cam.data.type,'lens':cam.data.lens,'ortho_scale':cam.data.ortho_scale}})
linearize();s.frame_set(1)
name=f'SHOT_{kind}_{a.version}';blend=R/'blender'/f'{name}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));(R/'reports'/f'{name}_rig-data.json').write_text(json.dumps({'shot':kind,'duration':duration,'frames':N,'Blender':bpy.app.version_string,'native_IK':True,'max_residual_m':max(max(x['IK_residuals_m']) for x in report),'samples':report,'key':keyheld},indent=2))
out=R/('renders' if a.stage=='final' else 'previews')/name;out.mkdir(exist_ok=True);s.render.filepath=str(out/'frame_')
if a.stage=='inspect':
 for sec in ([0,.8,1.7,2.2,3.8,5.5,6.6,7.6] if kind=='B' else [0,1,2,3,4] if kind=='A' else [0,.9,1.6,2.3,3.2,4.6,5.7,7.8]):
  s.frame_set(min(N,round(sec*30)+1));s.render.filepath=str(out/f'inspect_{sec:.2f}.png');bpy.ops.render.render(write_still=True)
elif a.stage in ['preview','final']:bpy.ops.render.render(animation=True)
print('SHOT_SAVED',str(blend),'MAX_IK_RESIDUAL',max(max(x['IK_residuals_m']) for x in report))
