"""Direct monotone retiming of existing native contact keys; no resampled ankle channels."""
import bpy,sys,json,copy,math
from pathlib import Path
from mathutils import Quaternion,Vector
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'blender/STAIRS_M09.blend'));sc=bpy.context.scene;oldplan=json.loads((R/'assets'/sc['controls_filename']).read_text());clock=PchipInterpolator([0,.4,1.5,4.9,6.],[0,.12,1.,4.3,5.])
def inv(t):return 0. if t<=0 else 6. if t>=5 else brentq(lambda n:float(clock(n))-t,0,6,xtol=1e-12)
actions=set()
for o in sc.objects:
 for data in [o,getattr(o,'data',None)]:
  if data and data.animation_data and data.animation_data.action:actions.add(data.animation_data.action)
for action in actions:
 for fc in action.fcurves:
  for kp in fc.keyframe_points:
   old=kp.co.x/30;new=inv(old)*30;delta=new-kp.co.x;kp.co.x=new;kp.handle_left.x+=delta;kp.handle_right.x+=delta
  fc.update()
# Only the chest/spine FK layer is resampled for acting; root/ankle/pole/foot keys stay exact.
names=['CTRL_spine','CTRL_chest'];samples=[]
for i in range(181):
 sc.frame_set(i);samples.append({n:bpy.data.objects[n].rotation_quaternion.copy() for n in names})
def Q(t,a,b):
 u=max(0,min(1,(t-a)/(b-a)));return u*u*u*(10+u*(-15+6*u))
for n in names:bpy.data.objects[n].animation_data_clear()
for i,row in enumerate(samples):
 t=i/30;effort=sum((Q(t,a,a+.2)-Q(t,a+.4,a+.75))*v for a,v in [(1.1,.035),(2.2,.05),(3.3,.038),(4.4,.03)]);anticipate=.04*(Q(t,0,.25)-Q(t,.5,.85))
 for n,value in row.items():
  o=bpy.data.objects[n];o.rotation_quaternion=Quaternion(Vector((0,1,0)),anticipate+effort)@value;o.keyframe_insert('rotation_quaternion',frame=i)
for n in names:
 for fc in bpy.data.objects[n].animation_data.action.fcurves:
  for kp in fc.keyframe_points:kp.interpolation='LINEAR'
plan=copy.deepcopy(oldplan);rate=plan['rate'];plan['frames']=[copy.deepcopy(oldplan['frames'][min(len(oldplan['frames'])-1,round(float(clock(i/rate))*rate))]) for i in range(round(6*rate)+1)]
for i,f in enumerate(plan['frames']):
 if 'time' in f:f['time']=i/rate
 if 'face' in f:f['face']['fear']=.70
for k in plan['root_keys']:k['time']=inv(k['time'])
path=R/'assets/STAIRS_CONTROLS_M10D.json';path.write_text(json.dumps(plan));sc['controls_filename']=path.name;sc.frame_end=179;sc['M10_change']='Exact existing root/ankle/pole/foot key timing transformed by monotone inverse; FK anticipation and per-step effort added without resampling contact keys'
sys.argv=['export','--','--out-tag','M10D'];src=(R/'source/export_stairs_m08.py').read_text().replace('range(150)','range(180)').replace('range(601)','range(721)');exec(compile(src,str(R/'source/export_stairs_m08.py'),'exec'))
