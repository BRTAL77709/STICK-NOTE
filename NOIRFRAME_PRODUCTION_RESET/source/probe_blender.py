import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=1;s.cycles.use_denoising=False;s.cycles.device='CPU';s.render.resolution_x=270;s.render.resolution_y=480;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('World');s.world.color=(.02,.02,.02);s.render.use_freestyle=True;ls=s.view_layers[0].freestyle_settings.linesets[0];ls.linestyle=bpy.data.linestyles.new('Ink');ls.linestyle.thickness=2.5;ls.linestyle.color=(.002,.006,.01)
bpy.ops.mesh.primitive_cube_add();o=bpy.context.object
m=bpy.data.materials.new('flat');m.diffuse_color=(.03,.13,.18,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(.03,.13,.18,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);o.data.materials.append(m)
bpy.ops.object.camera_add(location=(3,-6,3));c=bpy.context.object;c.rotation_euler=((o.location-c.location).to_track_quat('-Z','Y')).to_euler();s.camera=c;s.render.filepath=str(R/'previews/engine-probe.png');bpy.ops.wm.save_as_mainfile(filepath=str(R/'blender/engine-probe.blend'));bpy.ops.render.render(write_still=True)
(R/'reports/blender-capability.json').write_text(json.dumps({'Blender':bpy.app.version_string,'Cycles_CPU_render':True,'armature':hasattr(bpy.types,'Armature'),'Grease_Pencil_v3':hasattr(bpy.types,'GreasePencilv3'),'IK_constraint':hasattr(bpy.types,'KinematicConstraint'),'render_engine':s.render.engine},indent=2))
