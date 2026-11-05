import bpy,time,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_percentage=100;s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.use_freestyle=False;sh=s.display.shading;sh.light='FLAT';sh.color_type='MATERIAL';sh.show_shadows=False;sh.show_cavity=False;sh.show_object_outline=True;sh.object_outline_color=(.002,.005,.009);sh.background_type='WORLD';s.display.render_aa='FXAA';times=[]
for f in [61,62,63]:
 start=time.monotonic();s.frame_set(f);s.render.filepath=str(R/f'previews/workbench-fxaa-{f}.png');bpy.ops.render.render(write_still=True);times.append(time.monotonic()-start);print('FAST_FRAME',f,times[-1],flush=True)
(R/'reports/workbench-fxaa.json').write_text(json.dumps({'engine':s.render.engine,'AA':s.display.render_aa,'frame_seconds':times},indent=2))
