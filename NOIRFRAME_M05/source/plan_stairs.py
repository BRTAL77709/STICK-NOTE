"""M04 authored support/pose plan. Kinematics, not force simulation. Blender solves the rig."""
from pathlib import Path
import json,math,argparse
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import lsq_linear
from scipy.sparse import diags
R=Path(__file__).resolve().parents[1]
FPS=30;RATE=120;DURATION=5.;PROFILE=[[-.105,0],[.105,0],[.120,.035],[.045,.085],[-.080,.080]]
INITIAL=[[-.30,-.09,0],[-.14,.09,0]]
STEPS=[{'leg':0,'lift':.35,'land':1.20,'target':[.15,-.09,.18],'tread':1},{'leg':1,'lift':1.38,'land':2.23,'target':[.45,.09,.36],'tread':2},{'leg':0,'lift':2.41,'land':3.26,'target':[.75,-.09,.54],'tread':3},{'leg':1,'lift':3.44,'land':4.29,'target':[1.05,.09,.54],'tread':3}]
ROOT=[(0,[-.22,0,.760]),(.20,[-.217,.025,.750]),(.35,[-.20,.055,.748]),(.80,[-.12,.055,.752]),(1.20,[-.055,.055,.765]),(1.38,[.005,-.055,.770]),(1.80,[.15,-.055,.900]),(2.23,[.245,-.055,.940]),(2.41,[.31,.055,.950]),(2.80,[.46,.055,1.080]),(3.26,[.545,.055,1.120]),(3.44,[.61,-.055,1.130]),(3.90,[.76,-.055,1.255]),(4.29,[.86,-.045,1.290]),(4.70,[.90,-.010,1.305]),(5.,[.90,0,1.305])]
BASE_SPLINE=CubicSpline([t for t,p in ROOT],[p for t,p in ROOT],bc_type=((1,[0,0,0]),(1,[0,0,0])))
def s5(u):u=np.clip(u,0,1);return u*u*u*(10-15*u+6*u*u)
# Smooth lateral mass transfer, rather than moving 11cm during a short double-support interval.
root_times=sorted(set([t for t,p in ROOT]+list(np.linspace(0,5,35))));ROOT=[(t,BASE_SPLINE(t).tolist()) for t in root_times]
for t,p in ROOT:p[1]=.045*math.cos(math.pi*(t-.75)/1.03)*s5(t/.4)*(1-s5((t-4.1)/.9))
ROOT_SPLINE=CubicSpline([t for t,p in ROOT],[p for t,p in ROOT],bc_type=((1,[0,0,0]),(1,[0,0,0])))
def floor_height(x):return 0 if x<0 else .18 if x<.3 else .36 if x<.6 else .54

def make_swing(start,end,a,b):
 n=round((b-a)*RATE)+1;u=np.linspace(0,1,n);start_origin_x=start[0]+.105-.105*math.cos(-.20);start_origin_z=start[2]-.105*math.sin(-.20);x=start_origin_x+(end[0]-start_origin_x)*s5(u);pitch=-.20*(1-s5(u/.30))+.14*np.sin(math.pi*u)**2;pitch[-3:]=0
 lower=[]
 for j in range(n):
  c,s=math.cos(pitch[j]),math.sin(pitch[j]);shape=[(x[j]+vx*c-vz*s,vx*s+vz*c) for vx,vz in PROFILE];minz=max(floor_height(px)-pz for px,pz in shape)
  # Profile edges can cut a riser even if their endpoints clear it. Check exact crossings.
  for (xa,za),(xb,zb) in zip(shape,shape[1:]+shape[:1]):
   for rx,h in [(0,.18),(.3,.36),(.6,.54)]:
    if min(xa,xb)<rx<max(xa,xb):minz=max(minz,h-(za+(zb-za)*(rx-xa)/(xb-xa)))
  margin=.008*s5((u[j]-.05)/.10)*(1-s5((u[j]-.90)/.09));lower.append(minz+margin)
 lower=np.array(lower);fixed=np.r_[0,1,2,n-3,n-2,n-1];free=np.arange(3,n-3);values=np.zeros(n);values[:3]=start_origin_z;values[-3:]=end[2]
 D2=diags([np.ones(n-2),-2*np.ones(n-2),np.ones(n-2)],[0,1,2],shape=(n-2,n)).toarray();D3=diags([-np.ones(n-3),3*np.ones(n-3),-3*np.ones(n-3),np.ones(n-3)],[0,1,2,3],shape=(n-3,n)).toarray();A=np.vstack([np.eye(n),math.sqrt(120)*D2,math.sqrt(150000)*D3]);preferred=start_origin_z+(end[2]-start_origin_z)*s5(u)+.025*np.sin(math.pi*u)**2;rhs=np.r_[preferred,np.zeros(n-2),np.zeros(n-3)]-A[:,fixed]@values[fixed]
 result=lsq_linear(A[:,free],rhs,bounds=(lower[free]+.0002,np.full(len(free),max(start[2],end[2])+.07)),method='bvls',tol=1e-10,max_iter=1000)
 if not result.success:raise RuntimeError(result.message)
 values[free]=result.x;return {'times':(a+u*(b-a)).tolist(),'x':x.tolist(),'z':values.tolist(),'pitch':pitch.tolist(),'start':start,'end':end}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--tag',default='R01');args=parser.parse_args();swings=[];feet=[list(p) for p in INITIAL]
 for step in STEPS:
  j=step['leg'];sw=make_swing(feet[j],step['target'],step['lift'],step['land']);swings.append({**step,**sw});feet[j]=step['target']
 def foot_at(t,j):
  p=np.array(INITIAL[j],float);pitch=0;planted=True;tread=0
  for sw in swings:
   if sw['leg']!=j:continue
   if t<sw['lift']:
    if t>=sw['lift']-.10:
     pitch=-.20*float(s5((t-(sw['lift']-.10))/.10));p=p+np.array([.105-.105*math.cos(pitch),0,-.105*math.sin(pitch)])
    break
   if t>=sw['land']:p=np.array(sw['end']);pitch=0;tread=sw['tread'];continue
   p=np.array([np.interp(t,sw['times'],sw['x']),INITIAL[j][1],np.interp(t,sw['times'],sw['z'])]);pitch=float(np.interp(t,sw['times'],sw['pitch']));planted=False;tread=None;break
  ankle=p+np.array([-.015*math.cos(pitch)-.055*math.sin(pitch),0,-.015*math.sin(pitch)+.055*math.cos(pitch)])
  return {'sole':p.tolist(),'ankle':ankle.tolist(),'pitch':pitch,'planted':planted,'tread':tread,'contact_mode':('TOE' if pitch<-.002 else 'FLAT') if planted else 'SWING'}
 frames=[]
 for i in range(round(DURATION*RATE)+1):
  t=i/RATE;root=ROOT_SPLINE(t);phase=(t-.35)/1.03;arm=.29*math.cos(math.pi*phase);torso_pitch=math.radians(7+3.5*math.sin(math.pi*np.clip((t-.2)/4.5,0,1))**2)*float(s5(t/.4))*(1-float(s5((t-4.2)/.8)));pelvis_roll=math.radians(2.2)*math.cos(math.pi*(t-.75)/1.03)*float(s5(t/.4))*(1-float(s5((t-4.1)/.9)));settle=1-s5((t-4.25)/.65)
  frames.append({'time':t,'root':root.tolist(),'feet':[foot_at(t,j) for j in range(2)],'pelvis_roll':pelvis_roll,'spine_pitch':torso_pitch,'chest_pitch':torso_pitch*.65,'chest_twist':arm*.18*settle,'arm_swing':[arm*settle,-arm*settle],'elbow_extra':[.07*math.sin(math.pi*phase-.3)*settle,-.07*math.sin(math.pi*phase-.3)*settle],'head_pitch':math.radians(-1.0)*math.sin(math.pi*min(1,t/5))})
 out=R/'assets'/f'CONTROLS_{args.tag}.json';assert not out.exists();data={'duration':DURATION,'fps':FPS,'rate':RATE,'units':'metres; Blender Z up; X ascent; Y lateral','initial':INITIAL,'shoe_profile':PROFILE,'steps':STEPS,'root_keys':[{'time':t,'value':p,'derivative':ROOT_SPLINE(t,1).tolist()} for t,p in ROOT],'frames':frames,'method':'Authored C2 support-relative root poses; constrained clearance-minimizing swing paths. No mass/force simulation.'};out.write_text(json.dumps(data,separators=(',',':')));print(out)
 # Independent reach preflight using preserved limb lengths, before native IK.
 maxreach=0
 for d in frames:
  r=np.array(d['root'])
  for j,f in enumerate(d['feet']):maxreach=max(maxreach,float(np.linalg.norm(r+np.array([0,(-.07,.07)[j],0])-f['ankle'])))
 print('preflight leg reach max',maxreach,'of .74m')
if __name__=='__main__':main()
