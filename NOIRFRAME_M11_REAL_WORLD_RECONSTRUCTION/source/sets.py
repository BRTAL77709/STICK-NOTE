"""M11 set geometry: shared city and House17, permanent enclosed bedroom, consistent sedan."""
from sets_m10 import *
import sets_m10 as base
from spatial_world import house as connected_house,bedroom as bedroom_shell,cabin as cabin_completion

def house_exterior(w):
 base._HOUSE_M09(w)
 if getattr(w,'full_detail',False) or np.linalg.norm(w.cam.eye)<25:connected_house(w)
base.house_exterior=house_exterior

def append_transform(w,other,R,T):
 for g in other.geometry:w.geometry.append({**g,'vertices':[(np.array(T)+R@np.array(q)).tolist() for q in g['vertices']]})
 for op in other.ops:
  if op[0] in ['face','line']:w.ops.append((op[0],[np.array(T)+R@np.array(p) for p in op[1]],*op[2:]))
base.append_transform=append_transform

def city(w):base.city(w)
def cockpit(w,d):base.cockpit(w,d);cabin_completion(w)
def exit_car(w,d):
 base.exit_car(w,d);cabin_completion(w);w.box(.16,.08,-.36,.48,.18,.55,'#294654','passenger cushion');w.box(.16,.25,-.46,.48,.72,.12,'#1c3543','passenger back')
 for x in [-.38,.4]:w.box(x-.15,.95,-.43,.30,.22,.10,'#31505c','front headrest')

def bedroom(w,d):
 bedroom_shell(w)
 # The parked sedan is registered to the actual exterior road, 2.73m below this floor.
 w.face([V(-12,-2.73,2),V(12,-2.73,2),V(12,-2.73,15),V(-12,-2.73,15)],'#142f3f',stroke='none',name='registered street outside');basecar(w,d['sedan_position'],d['sedan_yaw'],VS.PARK['pursuer_wheel_phase'],0,True)
 for j in range(65):
  x=-9+(j*3.17)%18;z=2+(j*2.37)%13;y=-2.73+(j*.23-w.t*4.1)%6;w.line([V(x,y,z),V(x-.025,y-.24,z+.03)],'#607f90',1)
 for x in [-.76,.73]:w.box(x,.60,.03,.03,1.60,.09,'#83958e','window jamb')
 for y in [.60,2.17]:w.box(-.76,y,.03,1.52,.035,.09,'#83958e','window lintel')
 w.box(-.82,.56,-.08,1.64,.05,.20,'#9a9e8b','window sill');w.tube([V(-.86,2.23,-.21),V(.86,2.23,-.21)],'#bea977',.025)
 for x in [-.86,.86]:w.tube([V(x,2.23,.03),V(x,2.23,-.21)],'#8c815f',.018)
 mesh=np.array(d['fabric']);nr,nc=mesh.shape[:2]
 for row in range(nr-1):
  for col in range(nc-1):
   a,b,c,e=mesh[row,col],mesh[row,col+1],mesh[row+1,col+1],mesh[row+1,col];n=np.cross(b-a,e-a);n/=max(1e-10,np.linalg.norm(n));v=float(n@V(.65,.15,-.72));palette=['#243e4d','#304d5c','#3a5968','#486b78','#5b7b87','#708d96'];w.face([a,b,c,e],palette[int(np.clip((v+1)*2.5,0,5))],stroke='none',name='connected curtain fold')
 for col in range(0,nc,6):w.tube([mesh[0,col],mesh[0,col]+V(0,.08,0)],'#c5b68f',.009)
 w.line(list(mesh[-1]),'#748892',2);w.line(list(mesh[:,-1]),'#8194a0',2)
 if 'phone_position' in d:
  C=np.array(d['phone_position']);M=np.array(d['phone_R']);P=lambda q:C+M@np.array(q);pts=[P(V(x,y,z)) for z in [-.012,.012] for x,y in [(-.039,-.08),(.039,-.08),(.039,.08),(-.039,.08)]]
  for f in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:w.face([pts[i] for i in f],'#102330','#a0aaa6',1,name='rigid phone body')
  w.face([P(V(x,y,-.014)) for x,y in [(-.033,-.071),(.033,-.071),(.033,.067),(-.033,.067)]],'#568091',name='caller screen')
  if float((M@V(0,0,-1))@(w.cam.eye-C))>0:
   w.text(P(V(0,.025,-.016)),'UNKNOWN',.008,'#eff2df');w.text(P(V(0,.010,-.016)),'NUMBER',.008,'#eff2df')
