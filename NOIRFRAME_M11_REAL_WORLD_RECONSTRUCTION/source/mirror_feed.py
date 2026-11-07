"""Calibrated rear-facing camera. Real sedan/road coordinates, proper polygon clipping.
The mirror uses a simplified rearward environment LOD, not an unrelated static image.
"""
from world import *
from geometry import car
from contact_rig import RY
import vehicle_system as VS

def clip(poly,axis,bound,sign):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=sign*(a[axis]-bound);db=sign*(b[axis]-bound)
  if da>=0:out.append(a)
  if (da>=0)!=(db>=0):out.append(a+(b-a)*da/(da-db))
 return out

def draw(w,d):
 M=RY(-d['yaw']);rel=M@(d['pursuer_position']-d['position']);rear=World(Camera((0,1.25,-.35),(0,1.25,-20),.35,center=(0,0)),d['time']);P=lambda q:M@(np.array(q)-d['position'])
 for z in range(-64,161,5):
  if not d['position'][2]-70<z<d['position'][2]+5:continue
  rear.face([P(V(VS.roadref(zz)+x,0,zz)) for x,zz in [(-4.5,z),(4.5,z),(4.5,z+5),(-4.5,z+5)]],'#132d3c',stroke='none')
 for z in range(-60,150,10):
  if not d['position'][2]-65<z<d['position'][2]+5:continue
  idx=(z+20)//10
  for side in [-1,1]:
   if z==20 or (side==-1 and abs(z-VS.HOUSE_ORIGIN[2])<8):continue
   x=VS.roadref(z)+side*7.8-side*1.36;h=[4.8,6.2,5.2,7.5][(idx+(side==1))%4];width=[5.8,6.6,7.2][idx%3];rear.face([P(V(x,y,zz)) for y,zz in [(.13,z),(h,z),(h,z+width),(.13,z+width)]],'#29424d','#526874',.5)
   for yy in np.arange(1.45,h-.6,1.35):
    for j,zz in enumerate(np.arange(z+1,z+width-.3,1.65)):rear.face([P(V(x,yy+dy,zz+dz)) for dy,dz in [(-.37,-.37),(.37,-.37),(.37,.37),(-.37,.37)]],'#d2a16b' if (idx+j+int(yy))%4==0 else '#284e60',stroke='none')
 car(rear,rel,d['pursuer_yaw']-d['yaw'],d['pursuer_wheel_phase'],d['pursuer_steer'],True)
 for op in rear.ops:
  if op[0]!='face':continue
  poly=[]
  for q in op[1]:
   x,y=rear.cam(q);poly.append(V(-x,1.265-y,.259))
  for axis,bound,sgn in [(0,-.215,1),(0,.215,-1),(1,1.205,1),(1,1.325,-1)]:
   if not poly:break
   poly=clip(poly,axis,bound,sgn)
  if len(poly)>2:w.face(poly,op[2],op[3],.5,name='calibrated rear camera feed')
