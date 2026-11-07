"""Preserve M08 contacts, edit actual torso/arms with per-step effort and recovery."""
import bpy,sys,math
from pathlib import Path
from mathutils import Quaternion,Vector
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'blender/STAIRS_M08.blend'));sc=bpy.context.scene
names=['spine','chest','upper_arm.L','upper_arm.R','forearm.L','forearm.R','hand.L','hand.R']
def Q(t,a,b):
 u=max(0,min(1,(t-a)/(b-a)));return u*u*u*(10+u*(-15+6*u))
def P(t,a,b,c,d):return Q(t,a,b)*(1-Q(t,c,d))
samples=[]
for i in range(151):
 sc.frame_set(i);samples.append({n:bpy.data.objects['CTRL_'+n].rotation_quaternion.copy() for n in names})
for n in names:bpy.data.objects['CTRL_'+n].animation_data_clear()
for i,row in enumerate(samples):
 t=i/30;effort=sum(P(t,a,a+.22,a+.40,a+.67)*weight for a,weight in [(.85,1),(1.88,.80),(2.91,1.12),(3.94,.7)]);anticipation=P(t,0,.25,.55,.9);landing=Q(t,4.35,4.9)
 for n,q in row.items():
  if n in ['spine','chest']:angle=.045*anticipation+.032*effort-.025*landing
  else:
   s=1 if n.endswith('L') else -1;counter=sum(P(t,a,a+.25,a+.48,a+.80)*sign for a,sign in [(.65,1),(1.68,-1),(2.71,1),(3.74,-1)]);angle=s*(.085*counter+.03*anticipation)*(1-landing)
  o=bpy.data.objects['CTRL_'+n];o.rotation_mode='QUATERNION';o.rotation_quaternion=Quaternion(Vector((0,1,0)),angle)@q;o.keyframe_insert('rotation_quaternion',frame=i)
for n in names:
 for fc in bpy.data.objects['CTRL_'+n].animation_data.action.fcurves:
  for k in fc.keyframe_points:k.interpolation='LINEAR'
sc['M09_change']='Non-repeating anticipation, individual step effort, arm counter-reaction and landing recovery; original pelvis/ankles/poles/contact schedule retained.'
sys.argv=['export','--','--out-tag','M09'];exec(compile((R/'source/export_stairs_m08.py').read_text(),str(R/'source/export_stairs_m08.py'),'exec'))
