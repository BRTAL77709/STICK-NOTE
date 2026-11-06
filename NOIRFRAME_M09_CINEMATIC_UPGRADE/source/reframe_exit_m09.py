"""Retain native M09D rig/motion; prevent final camera crossing House17 wall."""
import bpy,sys,json,gzip
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));from cameras import camera
from actions_exit_reframe_controller import state
B=Matrix(((0,0,1),(1,0,0),(0,1,0)));bpy.ops.wm.open_mainfile(filepath=str(R/'blender/CAR_EXIT_RUNNING_M09D.blend'));sc=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];card=bpy.data.objects['APPROVED_HEAD_CARD'];vv=[v.co for v in card.data.vertices];right=(vv[1]-vv[0]).normalized();up=(vv[3]-vv[0]).normalized();normal=right.cross(up).normalized();basis=Matrix((right,up,normal)).transposed();rest=rig.data.bones['head'].matrix_local.to_quaternion();head=bpy.data.objects['CTRL_head']
for i in range(324):
 d=state('CAR_EXIT_RUNNING',i/30);c=camera('CAR_EXIT_RUNNING',i/30,d);sc.camera.location=B@Vector(c.eye);sc.camera.rotation_euler=(-(B@Vector(c.forward))).to_track_quat('Z','Y').to_euler();sc.camera.data.lens=c.focal*36/1080;sc.camera.keyframe_insert('location',frame=i);sc.camera.keyframe_insert('rotation_euler',frame=i);sc.camera.data.keyframe_insert('lens',frame=i);cr=(B@Vector(c.right)).normalized();cu=(B@Vector(c.up)).normalized();cn=cr.cross(cu).normalized();rot=Matrix((cr,cu,cn)).transposed()@basis.transposed();head.rotation_mode='QUATERNION';head.rotation_quaternion=rot.to_quaternion()@rest;head.keyframe_insert('rotation_quaternion',frame=i)
for o in [head,sc.camera]:
 for fc in o.animation_data.action.fcurves:
  for kp in fc.keyframe_points:kp.interpolation='LINEAR'
sys.argv=['export','--','--shot','CAR_EXIT_RUNNING','--tag','M09K','--controller',str(R/'source/actions_exit_reframe_controller.py')];exec(compile((R/'source/evaluate_saved.py').read_text(),str(R/'source/evaluate_saved.py'),'exec'))
