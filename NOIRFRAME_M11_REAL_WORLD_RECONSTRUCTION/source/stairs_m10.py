"""Retime the actual M09 native rig as one unit; preserve world foot targets and rest lengths."""
import bpy,sys,json,copy,math
from pathlib import Path
from mathutils import Quaternion,Vector
from scipy.interpolate import PchipInterpolator
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'blender/STAIRS_M09.blend'));sc=bpy.context.scene;oldplan=json.loads((R/'assets'/sc['controls_filename']).read_text());clock=PchipInterpolator([0,.4,1.5,4.9,6.],[0,.12,1.,4.3,5.]);inv=PchipInterpolator([0,.12,1.,4.3,5.],[0,.4,1.5,4.9,6.])
# Re-sample every existing animated control, including root/ankles/poles/camera. No separate walk loop.
objects=[o for o in sc.objects if o.animation_data and o.animation_data.action];channels={o.name:sorted({fc.data_path for fc in o.animation_data.action.fcurves if fc.data_path in ['location','rotation_quaternion','rotation_euler','scale']}) for o in objects};sample=[]
for i in range(181):
 t=i/30;fr=float(clock(t))*30;sc.frame_set(int(fr),subframe=fr-int(fr));sample.append({o.name:{p:getattr(o,p).copy() for p in channels[o.name]} for o in objects})
for o in objects:o.animation_data_clear()
def Q(t,a,b):
 u=max(0,min(1,(t-a)/(b-a)));return u*u*u*(10+u*(-15+6*u))
for i,row in enumerate(sample):
 t=i/30
 for name,values in row.items():
  o=bpy.data.objects[name]
  for p,value in values.items():
   if p=='rotation_quaternion' and name in ['CTRL_spine','CTRL_chest']:
    effort=sum((Q(t,a,a+.2)-Q(t,a+.4,a+.75))*v for a,v in [(1.1,.035),(2.2,.05),(3.3,.038),(4.4,.03)]);anticipate=.04*(Q(t,0,.25)-Q(t,.5,.85));value=Quaternion(Vector((0,1,0)),anticipate+effort)@value
   setattr(o,p,value);o.keyframe_insert(p,frame=i)
for o in objects:
 for fc in o.animation_data.action.fcurves:
  for k in fc.keyframe_points:k.interpolation='LINEAR'
plan=copy.deepcopy(oldplan);rate=plan['rate'];plan['frames']=[copy.deepcopy(oldplan['frames'][min(len(oldplan['frames'])-1,round(float(clock(i/rate))*rate))]) for i in range(round(6*rate)+1)]
for i,f in enumerate(plan['frames']):
 if 'time' in f:f['time']=i/rate
 if 'face' in f:f['face']['fear']=.70
for k in plan['root_keys']:k['time']=float(inv(min(5,k['time'])))
path=R/'assets/STAIRS_CONTROLS_M10.json';path.write_text(json.dumps(plan));sc['controls_filename']=path.name;sc.frame_end=179;sc['M10_change']='Whole native rig nonuniform timewarp; foot/ankle/pole/root channels retimed together; keyed anticipation/individual step effort; landing recovery'
sys.argv=['export','--','--out-tag','M10'];src=(R/'source/export_stairs_m08.py').read_text().replace('range(150)','range(180)').replace('range(601)','range(721)');exec(compile(src,str(R/'source/export_stairs_m08.py'),'exec'))
