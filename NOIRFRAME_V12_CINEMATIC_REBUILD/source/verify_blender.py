import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];rows={}
for s in bpy.data.scenes:
 if not s.name.endswith('_V12_WORLD'):continue
 rows[s.name]={'objects':len(s.objects),'cameras':sum(o.type=='CAMERA' for o in s.objects),'mesh_surfaces':sum(len(o.data.polygons) for o in s.objects if o.type=='MESH'),'armatures':sum(o.type=='ARMATURE' for o in s.objects),'IK_constraints':sum(c.type=='IK' for o in s.objects if o.type=='ARMATURE' for b in o.pose.bones for c in b.constraints),'fps':s.render.fps,'frames':s.frame_end}
assert len(rows)==4 and all(x['IK_constraints']==4 and x['cameras']==1 for x in rows.values());(R/('reports/BLENDER_VERIFICATION_R02.json' if '_R02' in bpy.data.filepath else 'reports/BLENDER_VERIFICATION.json')).write_text(json.dumps({'Blender_version':bpy.app.version_string,'file_opened':bpy.data.filepath,'scenes':rows,'scope':'Supplemental spatial/IK editing companion. Final illustrative animation is generated from Python, not a native Blender film render.'},indent=2));print('BLEND_OPEN_IK_VALIDATED',rows)
