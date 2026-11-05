"""Contact-first, mass-estimated articulated rig. Metres/Y-up. No walk-cycle playback.
The approved .37m leg and .34m arm segments and drawn head dimensions stay fixed.
"""
from rig import *
def Q(t,a,b):
 u=clamp((t-a)/(b-a));return u*u*u*(10+u*(-15+6*u))
def channel(t,rows):
 if t<=rows[0][0]:return np.asarray(rows[0][1],float)
 for (a,x),(b,y) in zip(rows,rows[1:]):
  if t<=b:return mix(x,y,Q(t,a,b))
 return np.asarray(rows[-1][1],float)
def RX(a):return np.array([[1,0,0],[0,math.cos(a),-math.sin(a)],[0,math.sin(a),math.cos(a)]])
def RY(a):return np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
def RZ(a):return np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]])
def transform(p,R,T):return np.asarray(T)+R@np.asarray(p)
def pose(root,feet,hands=None,heading=math.pi/2,pitch=0,roll=0,twist=0,pelvis_roll=0,head_lag=0,fear=.5,look=.75,knee_forward=None):
 r=np.asarray(root,float);pelvisR=RY(heading)@RZ(pelvis_roll);torsoR=RY(heading+twist)@RZ(roll)@RX(pitch);sh=r+torsoR@V(0,.50,0);h=sh+torsoR@V(0,math.sqrt(.29**2-head_lag**2),head_lag);legs=[];arms=[]
 for j,f in enumerate(feet):
  hip=r+pelvisR@V((.07,-.07)[j],0,0);ank=np.array(f.get('ankle',np.array(f['sole'])+V(0,.055,0)));pole=np.cross(-(RY(heading)@V(1,0,0)),ank-hip);knee=ik(hip,ank,.37,.37,pole);legs.append({**f,'hip':hip,'knee':knee,'ankle':ank})
 for j in range(2):
  shoulder=sh+torsoR@V((.17,-.17)[j],0,0);wrist=np.array(hands[j] if hands is not None else r+torsoR@V((.20,-.20)[j],.10,.10));pole=torsoR@V((.6,-.6)[j],-.7,-.3);elbow=ik(shoulder,wrist,.34,.34,pole);arms.append({'shoulder':shoulder,'elbow':elbow,'wrist':wrist})
 return {'hierarchy':{'root':None,'pelvis':'root','torso':'pelvis','chest':'torso','neck':'chest','head':'neck','shoulders':'chest','upper_arms':'shoulders','forearms':'upper_arms','hands':'forearms','thighs':'pelvis','shins':'thighs','feet':'shins','toes':'feet'},'chest':r+torsoR@V(0,.38,0),'neck':sh+torsoR@V(0,.07,0),'root':r,'shoulder':sh,'head':h,'legs':legs,'arms':arms,'torso_basis':torsoR,'pelvis_basis':pelvisR,'yaw':look,'fear':fear,'tilt':-roll*180/math.pi}
def com(p):
 c=.14*p['root']+.43*(p['root']+p['shoulder'])/2+.09*p['head']
 for l in p['legs']:c+=.10*(l['hip']+l['knee'])/2+.045*(l['knee']+l['ankle'])/2+.015*np.asarray(l['sole'])
 for a in p['arms']:c+=.01*(a['shoulder']+a['elbow']+a['wrist'])/3
 return c

def step(t,start,end,a,b,clearance=.16):
 start=np.array(start);end=np.array(end)
 if t<a:return {'sole':start,'planted':True,'pitch':0,'heading':math.pi/2}
 if t>=b:return {'sole':end,'planted':True,'pitch':0,'heading':math.pi/2}
 u=(t-a)/(b-a);x=Q(u,0,1);p=mix(start,end,x)
 # Lift to clear the riser before horizontal travel; arrive flat before load transfer.
 p[1]=start[1]+(end[1]-start[1])*Q(u,0,.55)+clearance*Q(u,0,.25)*(1-Q(u,.60,1))
 return {'sole':p,'planted':False,'pitch':-.20*(1-Q(u,0,.24))+.10*math.sin(math.pi*u)**2,'heading':math.pi/2}

def fingers(wrist,pads,pole,normals=None):
 out=[]
 for index,pad in enumerate(pads):
  # Articulated index/thumb, fixed phalanges. Contact targets are object-local pads.
  pad=np.asarray(pad);normal=V(0,0,-1) if normals is None else np.asarray(normals[index]);normal=normal/np.linalg.norm(normal);tip=pad+normal*.007;base=np.asarray(wrist);joint=ik(base,tip,.034,.034,np.asarray(pole)+normal*2.0);out.append({'base':base,'joint':joint,'tip_center':tip,'pad':pad,'normal':normal,'tip_radius':.007,'lengths':[.034,.034]})
 return out

def foot_geometry(f):
 F=V(math.sin(f['heading']),0,math.cos(f['heading']));a=f['pitch'];origin=np.asarray(f['sole']).copy()
 if a<0:origin+=F*.105-(F*math.cos(a)+V(0,math.sin(a),0))*.105
 f['shoe_origin']=origin;f['ankle']=origin+F*(-.015*math.cos(a)-.055*math.sin(a))+V(0,-.015*math.sin(a)+.055*math.cos(a),0)
 f['contact_mode']=('toe' if a<-.0001 else 'flat') if f['planted'] else 'flight'
 f['contact_anchor']=np.asarray(f['sole'])+(F*.105 if f['contact_mode']=='toe' else V(0,0,0))
 return f

def shoe_surface(f):
 H=np.array(f['heel']);P=np.array(f['toe']);F=P-H;F/=np.linalg.norm(F);side=np.cross(V(0,1,0),F);side/=np.linalg.norm(side);up=np.cross(F,side);normal=f.get('surface_normal');grid=[]
 for u in np.linspace(0,1,5):
  row=[]
  for v in np.linspace(-1,1,5):
   lateral=(.05-.005*u)*v;twist=0 if normal is None else -float(np.asarray(normal)@side)*lateral/float(np.asarray(normal)@up)*u**3
   row.append(H+(P-H)*u+side*lateral+up*(twist+.008*u*v*v))
  grid.append(row)
 return np.array(grid),up

def hermite(t,rows):
 ts=np.array([q[0] for q in rows]);ys=np.array([q[1] for q in rows]);slopes=np.gradient(ys,ts);slopes[0]=0;slopes[-1]=0
 if t<=ts[0]:return float(ys[0])
 if t>=ts[-1]:return float(ys[-1])
 j=int(np.searchsorted(ts,t)-1);dt=ts[j+1]-ts[j];u=(t-ts[j])/dt
 return float((2*u**3-3*u**2+1)*ys[j]+(u**3-2*u**2+u)*dt*slopes[j]+(-2*u**3+3*u**2)*ys[j+1]+(u**3-u**2)*dt*slopes[j+1])
