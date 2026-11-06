"""Artistic control edits on actual M05 armature. Foot/contact actions untouched."""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Quaternion,Vector
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'blender/STAIRS_M05_BASE.blend'));sc=bpy.context.scene;sc['controls_filename']='STAIRS_CONTROLS.json';names=['spine','chest','upper_arm.L','upper_arm.R','forearm.L','forearm.R','hand.L','hand.R'];samples=[]
for i in range(151):
 sc.frame_set(i);t=i/30;row={}
 for name in names:row[name]=bpy.data.objects['CTRL_'+name].rotation_quaternion.copy()
 samples.append(row)
for name in names:bpy.data.objects['CTRL_'+name].animation_data_clear()
for i,row in enumerate(samples):
 t=i/30;envelope=min(1,t/.7)*min(1,(5-t)/.7);pulse=math.sin((t-.8)*math.pi*1.9)
 for name,q in row.items():
  o=bpy.data.objects['CTRL_'+name];angle=(.035+.012*pulse)*envelope if name in ['spine','chest'] else ((1 if name.endswith('L') else -1)*.045*pulse*envelope)
  o.rotation_mode='QUATERNION';o.rotation_quaternion=Quaternion(Vector((0,1,0)),angle)@q;o.keyframe_insert('rotation_quaternion',frame=i)
for name in names:
 for fc in bpy.data.objects['CTRL_'+name].animation_data.action.fcurves:
  for k in fc.keyframe_points:k.interpolation='LINEAR'
sc['M08_change']='Torso urgency and arm counter-swing polish only; original root/feet/IK/poles/rest lengths retained';sc.frame_set(0)
# Export using preserved M05 evaluated-mesh schema, not reconstructed meshes.
sys.argv=['export','--','--out-tag','M08'];exec(compile((R/'source/export_stairs_m08.py').read_text(),str(R/'source/export_stairs_m08.py'),'exec'))
