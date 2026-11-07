from world import *
from contact_rig import RX,RY,RZ
from functools import lru_cache
def car(w,origin,yaw=0,wheel=0,steer=0,black=True,roll=0,pitch=0,brake=0):
 o=np.array(origin);c,s=math.cos(yaw),math.sin(yaw)
 bodyR=RZ(roll)@RX(pitch);yawR=RY(yaw);pivot=V(0,.55,0)
 def C(x,y,z):return o+yawR@(pivot+bodyR@(V(x,y,z)-pivot))
 body='#102838' if black else '#26485b'
 for xx in [-.90,.90]:
  for zz in [-1.32,1.28]:
   # Wheel plane with rotation derived from traveled distance, visible spokes.
   turn=(math.atan(2.60/(2.60/math.tan(steer)-xx)) if abs(steer)>1e-7 else 0) if zz>0 else 0
   wheelangle=wheel[([- .90,.90].index(xx))*2+[-1.32,1.28].index(zz)] if isinstance(wheel,(list,np.ndarray)) else wheel
   def WC(y,dz):
    return o+yawR@V(xx+dz*math.sin(turn),y,zz+dz*math.cos(turn))
   pts=[WC(.30+.30*math.sin(j*math.tau/24),.30*math.cos(j*math.tau/24)) for j in range(25)];w.face(pts,'#060f1b','#78909d',2,name='wheel')
   for j in range(5):
    a=wheelangle+j*math.tau/5;w.line([WC(.30,0),WC(.30+.23*math.sin(a),.23*math.cos(a))],'#84979b',2)
 w.face([C(-.85,.35,-2.15),C(.85,.35,-2.15),C(.85,.35,2.15),C(-.85,.35,2.15)],'#0c1b29',name='underbody')
 for side in [-1,1]:
  x=side*.85;w.face([C(x,.38,-2.15),C(x,.38,2.15),C(x,.88,2.05),C(x,.96,-1.85)],body,'#54717f',3,name='car side')
  w.line([C(x,.72,-1.45),C(x,.72,1.35)],'#64808d',2)
  for z in [-.66,.55]:w.line([C(x*1.005,.89,z),C(x*1.005,.89,z+.20)],'#a1acac',2)
 w.face([C(-.85,.88,2.05),C(.85,.88,2.05),C(.70,1.04,.84),C(-.70,1.04,.84)],'#335361','#73909d',2,name='hood')
 w.face([C(-.70,1.04,.84),C(.70,1.04,.84),C(.62,1.48,.10),C(-.62,1.48,.10)],'#4a6977','#98a5a7',3,name='windshield')
 w.face([C(-.62,1.48,.10),C(.62,1.48,.10),C(.64,1.46,-.92),C(-.64,1.46,-.92)],body,'#65838e',2,name='roof')
 # Complete the existing sedan shell: M08 omitted side glazing and rear deck.
 for side in [-1,1]:
  x0=side*.85;x1=side*.63
  panes=[(-1.40,-.64,-1.02,-.66),(-.60,.78,-.60,.08)]
  for panel,(z0,z1,top0,top1) in enumerate(panes):
   if side==-1 and panel==1 and getattr(w,'open_driver',False):continue
   w.face([C(x0,.96,z0),C(x0,1.02,z1),C(x1,1.46,top1),C(x1,1.46,top0)],'#183746' if black else '#345665','#78909b',2,name='sedan side glazing')
  if not (side==-1 and getattr(w,'open_driver',False)):
   w.line([C(x0,.97,-.62),C(x1,1.47,-.63)],'#0b202d',9)
 w.face([C(-.78,.95,-1.52),C(.78,.95,-1.52),C(.85,.92,-2.15),C(-.85,.92,-2.15)],body,'#65818b',2,name='sedan rear deck')
 w.line([C(-.65,.52,2.145),C(.65,.52,2.145)],'#091b27',10)
 w.face([C(-.64,1.46,-.92),C(.64,1.46,-.92),C(.78,.95,-1.52),C(-.78,.95,-1.52)],'#233f51','#758c97',2,name='rear glass')
 w.face([C(-.85,.38,-2.15),C(.85,.38,-2.15),C(.85,.92,-2.15),C(-.85,.92,-2.15)],body,'#66818e',2,name='trunk closed')
 w.face([C(-.85,.38,2.15),C(.85,.38,2.15),C(.85,.88,2.05),C(-.85,.88,2.05)],body,'#66818e',2,name='front fascia')
 for side in [-1,1]:
  x=side*.58
  w.face([C(x-.20,.67,2.12),C(x+.20,.67,2.12),C(x+.18,.80,2.08),C(x-.18,.80,2.08)],'#c7e1dc','#f0ece0',2,bias=-.03,name='headlamp')
  w.face([C(x-.21,.70,-2.16),C(x+.21,.70,-2.16),C(x+.18,.82,-2.16),C(x-.18,.82,-2.16)],('#ff4a43' if brake>.05 else '#922e38'),'#ed5e50',2,bias=-.03,name='taillamp')

def city(w,zcenter=0,half_range=55,night=True):
 start_ops=len(w.ops)
 # All addresses are deterministic fixed world locations, never a scrolling image.
 low=math.floor((zcenter-half_range)/9)*9;high=zcenter+half_range
 for za in np.arange(low,high,9):
  zb=za+9
  w.face([V(-4.5,.0,za),V(4.5,0,za),V(4.5,0,zb),V(-4.5,0,zb)],'#132c3b',name='road tile')
  w.line([V(0,.012,za+1),V(0,.012,za+5)],'#9faaa1',3)
  for side in [-1,1]:
   x=side*4.65;w.box(x-.15,0,za,.30,.14,9,'#4e6069','curb');w.face([V(side*4.8,.14,za),V(side*7.8,.14,za),V(side*7.8,.14,zb),V(side*4.8,.14,zb)],'#304650',name='sidewalk')
   bx=-9.4 if side<0 else 6.2;height=5+(int(za)//9%4)*1.15
   w.box(bx,.14,za+1,3.1,height,6.6,'#233d4c','building '+str(int(za))+' '+str(side))
   # Front windows face road, full stable architecture.
   wallx=-6.28 if side<0 else 6.18
   for y in np.arange(1.35,height-.3,1.35):
    for zz in [za+1.8,za+3.7,za+5.6]:
     pts=[V(wallx,y-.38,zz-.35),V(wallx,y+.38,zz-.35),V(wallx,y+.38,zz+.35),V(wallx,y-.38,zz+.35)];w.face(pts,'#b38b60' if (int(za+y*3+zz)%4)==0 else '#2c5064','#102b3b',2,name='city window')
   pole=V(side*5.05,.14,za+7);w.tube([pole,pole+V(0,4.6,0)],'#49616e',.045);w.tube([pole+V(0,4.6,0),pole+V(-side*.55,4.6,0)],'#7b8584',.045);w.glow(pole+V(-side*.55,4.55,0),.52)
   w.face([V(side*4.05,.015,za+4),V(side*4.45,.015,za+4),V(side*4.15,.015,za+8),V(side*3.7,.015,za+8)],'#426273',stroke='none',name='wet reflected light')
 # Real perpendicular street/open intersection at z48.
 w.face([V(-25,.018,45),V(25,.018,45),V(25,.018,51),V(-25,.018,51)],'#152f3e',name='intersection')
 for x in np.arange(-4.2,4.3,.8):w.face([V(x,.025,44.4),V(x+.35,.025,44.4),V(x+.35,.025,45.5),V(x,.025,45.5)],'#7d969b',stroke='none',name='crosswalk')

 for j in range(start_ops,len(w.ops)):
  op=w.ops[j]
  if op[0] in ['face','line']:
   w.ops[j]=(op[0],[p+V(road_x(p[2]),0,0) for p in op[1]],*op[2:])

def rain_overlay(a,t,density=100):
 for j in range(density):
  x=(j*137.1+t*34)%1120-20;y=(j*293.7+t*(690+j%7*28))%2000-40;a.line([(x,y),(x-9,y+32)],'#779daf',1+(j%4==0))

# Immutable road definition shared with vehicle integration.
@lru_cache(maxsize=20000)
def road_x(z):
 from vehicle_test import road_x as fixed_road
 return fixed_road(z)
