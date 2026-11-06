"""Editable car-local hierarchy, aligned native column/glazing frame, and actual skin parity."""
import bpy,json,gzip,hashlib,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];results={}
def B(q):return Vector((q[2],q[0],q[1]))
for shot in ['DRIVING_COCKPIT','DRIVER_CHASE']:
 data=json.load(gzip.open(R/'scenes'/f'{shot}_M10.json.gz','rt'));bpy.ops.wm.open_mainfile(filepath=str(R/'blender'/f'{shot}_M10.blend'));sc=bpy.context.scene
 for o in list(sc.objects):
  if o.parent==bpy.data.objects['INTERIOR'] and any(k in o.name.lower() for k in ['door card','footwell floor']):
   m=o.matrix_world.copy();o.parent=bpy.data.objects['BODY'];o.matrix_world=m
 def curve(name,coords,parent):
  c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=.009;c.bevel_resolution=0;sp=c.splines.new('POLY');sp.points.add(len(coords)-1)
  for p,q in zip(sp.points,coords):v=B(q);p.co=(*v,1)
  o=bpy.data.objects.new(name,c);sc.collection.objects.link(o);o.parent=bpy.data.objects[parent];return o
 curve('M10_WINDSHIELD_PHYSICAL_FRAME',[(-.70,1.02,.84),(-.62,1.46,.10),(.62,1.46,.10),(.70,1.02,.84)],'WINDSHIELD');curve('M10_COLUMN_AXIS',[(-.38,.70,.90),(-.38,.79,.56)],'STEERING_COLUMN')
 names=['CAR_ROOT','BODY','INTERIOR','DRIVER_SEAT','DASHBOARD','STEERING_COLUMN','STEERING_WHEEL','WINDSHIELD','REARVIEW_MIRROR','SIDE_MIRRORS','DRIVER_RIG'];hierarchy={n:{'parent':bpy.data.objects[n].parent.name if bpy.data.objects[n].parent else None,'direct_children':len(bpy.data.objects[n].children),'space':'car local'} for n in names};error=0;count=0
 for i in sorted({0,60,120,180,len(data['frames'])-1}):
  sc.frame_set(i);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
  for name,vv in data['frames'][i]['meshes'].items():
   o=bpy.data.objects[name];ev=o.evaluated_get(dep);mesh=ev.to_mesh()
   for v,q in zip(mesh.vertices,vv):error=max(error,(ev.matrix_world@v.co-Vector(q)).length);count+=1
   ev.to_mesh_clear()
 assert error<1e-6;sc.frame_set(0);out=R/'blender'/f'{shot}_EDITABLE_M10.blend';assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);results[shot]={'hierarchy':hierarchy,'native_mesh_vertices_checked':count,'geometry_difference_m':error,'file':str(out.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'world_mapping':'Native rig/interior use car-local units; source renderer applies the same integrated vehicle world pose once. No double world transform.'}
(R/'reports/COCKPIT_NATIVE_HIERARCHY.json').write_text(json.dumps(results,indent=2))
