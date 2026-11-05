"""Deliberate 3D action staging. Feet hold world anchors; contacts drive wrists and props."""
import math
import numpy as np
DURATIONS={'A':5.,'B':7.8,'C':8.}
def ease(t,a,b):
 u=max(0,min(1,(t-a)/(b-a)));return u*u*u*(10+u*(-15+6*u))
def mix(a,b,u):return np.array(a)*(1-u)+np.array(b)*u
def transform(p,origin,yaw):
 x,y,z=p;c=math.cos(yaw);s=math.sin(yaw);return np.array(origin)+[x*c-y*s,x*s+y*c,z]
def feet_plan(t,initial,plans):
 out=[];planted=[]
 for j in range(2):
  A=np.array(initial[j],float);on=True
  for a,b,B,height in plans[j]:
   if t<a:break
   if t<b:
    q=(t-a)/(b-a);A=mix(A,B,ease(t,a,b));A[2]+=height*math.sin(math.pi*q)**1.5;on=False;break
   A=np.array(B,float)
  out.append(A);planted.append(on)
 return out,planted

def freehands(root,yaw,phase=0,energy=0):
 return [transform((s*.25,-.13+(.18*math.sin(phase+j*math.pi)*energy),.80+.04*math.cos(phase+j*math.pi)*energy),root,yaw) for j,s in enumerate([-1,1])]
def car_state(t):
 u=max(0,min(1,(t-.5)/3.8));speed=2+5.5*(1-math.cos(math.pi*u))/2
 grid=np.linspace(0,t,240);us=np.clip((grid-.5)/3.8,0,1);vs=2+5.5*(1-np.cos(np.pi*us))/2;distance=float((np.trapezoid if hasattr(np,'trapezoid') else np.trapz)(vs,grid))
 # Reparameterize a metric curved centreline using arc length.
 xs=np.linspace(0,40,2001);ys=.7*np.sin(xs/9);ds=np.r_[0,np.cumsum(np.hypot(np.diff(xs),np.diff(ys)))];x=float(np.interp(distance,ds,xs));y=.7*math.sin(x/9);dy=.7/9*math.cos(x/9);ddy=-.7/81*math.sin(x/9);curvature=ddy/(1+dy*dy)**1.5;yaw=math.atan(dy);acc=(5.5*math.pi/(2*3.8)*math.sin(math.pi*u)) if 0<u<1 else 0
 return {'x':x,'y':y,'yaw':yaw,'speed':speed,'distance':distance,'curvature':curvature,'steer':math.atan(2.7*curvature),'pitch':-.012*acc,'acceleration':acc}
def shot_a(t):
 s=car_state(t);base=transform((.13,-.43,.10),(s['x'],s['y'],0),s['yaw']);yaw=s['yaw']+math.pi/2
 feet=[transform((.38+.06*j,-.43+.16*(j-.5),.245),(s['x'],s['y'],0),s['yaw']) for j in range(2)]
 steer=s['steer']*7;hands=[transform((.34,-.43-.14*math.cos(steer+j*math.pi),.94+.14*math.sin(steer+j*math.pi)),(s['x'],s['y'],0),s['yaw']) for j in range(2)]
 look=ease(t,1.45,2.25)*(1-ease(t,3.15,4.0));return {'root':base,'yaw':yaw,'feet':feet,'planted':[True,True],'hands':hands,'lean':-.12*ease(t,.5,1.5)+.03*ease(t,3.5,5),'head_yaw':yaw-1.05*look,'fear':.6+.3*look,'car':s}

def run_x(t):
 u=max(0,min(1,(t-1.4)/.4));return -1.9+2.21875*(min(t,1.4)+.2*(u+math.sin(math.pi*u)/math.pi))
B_INITIAL=[(-1.72,-.74,.06),(-2.16375,-.52,.06)]
B_PLANS=[[],[]]
for j,landings in enumerate([[.4,.8,1.2,1.6],[.2,.6,1.,1.4,1.8]]):
 for touchdown in landings:
  end=(1.75,-.42,.06) if j==0 and touchdown==1.6 else (1.55,-.46,.06) if j==1 and touchdown==1.8 else (run_x(touchdown)+.18,-.74 if j==0 else -.52,.06)
  B_PLANS[j].append((touchdown-.26,touchdown,end,.20))
# Additional planted steps support the door pull and the final entrance.
B_PLANS[0]+=[(5.05,5.30,(1.68,-.10,.06),.12),(5.55,5.85,(1.68,.48,.06),.14),(6.65,6.95,(1.68,1.10,.06),.12)]
B_PLANS[1]+=[(5.30,5.55,(1.38,.15,.06),.12),(6.10,6.40,(1.38,.80,.06),.14),(7.10,7.45,(1.38,1.38,.06),.12)]
def shot_b(t):
 root=np.array([run_x(t),-.63+.21*ease(t,.6,1.8),-.10+.025*math.sin(t*math.tau/.53)* (1-ease(t,1.4,1.8))]);root[0]-=.20*ease(t,4.85,5.55);root[1]+=.88*math.sin(math.radians(77)*ease(t,4.8,6.2))+1.0*ease(t,6.2,7.8);root[2]-=.03*ease(t,4.8,5.2)
 yaw=math.pi/2+math.pi/2*ease(t,1.3,1.8);feet,on=feet_plan(t,B_INITIAL,B_PLANS);hands=freehands(root,yaw,t*math.tau/.4,1-ease(t,1.4,1.8))
 angle=math.radians(77)*ease(t,4.8,6.2);lever=-.25*ease(t,2.1,2.3)*(1-ease(t,2.45,2.65))-.20*ease(t,4.55,4.8)*(1-ease(t,6.1,6.3))
 handle=transform((.78+.065*math.cos(lever),-.075,1.0+.065*math.sin(lever)),(1.10,0,0),angle)
 lock=np.array([1.88,-.055,1.17]);pocket=transform((-.20,-.10,.75),root,yaw);pre=lock+np.array([0,-.28,0]);keybow=pre.copy();keybow[1]+=.18*ease(t,3.55,3.85)-.16*ease(t,4.25,4.48);keyturn=math.pi/2*ease(t,3.85,4.25)*(1-ease(t,4.25,4.48))
 if t<1.8:pass
 elif t<2.10:hands[0]=mix(freehands(root,yaw)[0],handle,ease(t,1.8,2.1))
 elif t<2.48:hands[0]=handle
 elif t<2.75:hands[0]=mix(handle,pocket,ease(t,2.48,2.75))
 elif t<3.55:hands[0]=mix(pocket,pre,ease(t,2.75,3.55))
 elif t<4.48:hands[0]=keybow
 elif t<4.55:hands[0]=mix(keybow,handle,ease(t,4.48,4.55))
 elif t<6.20:hands[0]=handle
 elif t<6.45:hands[0]=mix(handle,freehands(root,yaw)[0],ease(t,6.2,6.45))
 if 2.8<t<3.55:
  tremor=math.sin(math.pi*ease(t,2.8,3.55));hands[0]+=np.array([.006*math.sin(t*math.tau*7),0,.005*math.sin(t*math.tau*8.2)])*tremor
 # Lean into the failed pull, recoil, then load the shoulder against the opening door.
 lean=.20*(1-ease(t,1.4,1.8))-.14*math.sin(math.pi*ease(t,2.15,2.65))+.13*ease(t,4.55,5.3)*(1-ease(t,6.1,6.6));look=1-ease(t,1.25,1.9)
 return {'root':root,'yaw':yaw,'feet':feet,'planted':on,'hands':hands,'lean':lean,'head_yaw':yaw+.15*math.sin(math.pi*ease(t,2.4,2.85)),'fear':.7,'door_angle':angle,'handle_angle':lever,'keybow':np.array(hands[0]),'keyturn':keyturn,'key_visible':2.75<=t<4.48,'key_inserted':3.85<=t<=4.25,'hand_contact':2.1<=t<2.48 or 4.55<=t<=6.2}
C_INITIAL=[(-.55,-.54,.06),(-.28,-.32,.06)]
C_PLANS=[[(.35,.9,(.12,-.54,.26),.24),(1.75,2.30,(1.0,-.54,.66),.24),(3.10,3.32,(1.55,-.54,.66),.11),(3.60,3.83,(2.25,-.54,.66),.11)],[(1.05,1.60,(.56,-.32,.46),.24),(2.50,3.05,(1.10,-.32,.66),.16),(3.34,3.57,(1.90,-.32,.66),.11),(3.83,4.08,(2.05,-.43,.66),.10)]]
C_PLANS[0]+=[(4.95,5.25,(2.65,-.54,.66),.08),(5.75,6.05,(2.85,-.54,.66),.08)]
C_PLANS[1]+=[(5.35,5.65,(2.45,-.43,.66),.08)]
C_PLANS[0]+=[(6.30,6.62,(2.36,-.54,.66),.10),(6.94,7.20,(1.85,-.54,.66),.10)]
C_PLANS[1]+=[(6.62,6.94,(2.05,-.43,.66),.10)]
def curtain(t,v=.05,u=0):
 delayed=t-.10*abs(v-.05);pull=ease(delayed,4.65,6.15);settle=.012*math.sin(max(0,t-6.5)*12)*math.exp(-max(0,t-6.5)*4)*ease(t,6.5,6.6);left=2.05+.90*pull+settle;return np.array([left+(3.15-left)*u,-.10-.045*math.sin(math.tau*7*u)*(1+.4*pull),1.50+1.25*v])
def shot_c(t):
 x=-.42+.39*ease(t,.35,1.05)+.42*ease(t,1.05,1.75)+.42*ease(t,1.75,2.50)+.27*ease(t,2.50,3.05)+1.07*ease(t,3.05,4.16)+.61*ease(t,4.65,6.15)
 rise=.08*ease(t,.9,1.05)+.12*ease(t,1.05,1.45)+.08*ease(t,1.6,1.75)+.12*ease(t,1.75,2.15)+.08*ease(t,2.3,2.5)+.12*ease(t,2.5,2.9);root=np.array([x-.81*ease(t,6.30,7.20),-.43+.08*ease(t,4.1,4.65),-.10+rise-.025*ease(t,.35,.55)*(1-ease(t,2.9,3.1))]);yaw=math.pi/2+math.pi/2*ease(t,3.6,4.12)-math.pi/2*ease(t,6.3,7.2);feet,on=feet_plan(t,C_INITIAL,C_PLANS);hands=freehands(root,yaw,t*5,.7*(1-ease(t,3.8,4.1)))
 grip=curtain(t)
 if 4.10<=t<4.65:hands[0]=mix(freehands(root,yaw)[0],grip,ease(t,4.1,4.65))
 elif 4.65<=t<6.25:hands[0]=grip
 elif 6.25<=t<6.6:hands[0]=mix(grip,freehands(root,yaw)[0],ease(t,6.25,6.6))
 lean=.10*math.sin(math.pi*ease(t,.35,3.05))+.10*ease(t,4.1,4.65)-.17*ease(t,6.25,7.0);headyaw=(yaw-.20*ease(t,5.8,6.2))*(1-ease(t,6.25,7.2))+.30*ease(t,6.25,7.2)
 return {'root':root,'yaw':yaw,'feet':feet,'planted':on,'hands':hands,'lean':lean,'head_yaw':headyaw,'fear':.25+.75*ease(t,6.15,6.85),'side_lean':.14*math.sin(math.pi*ease(t,5.25,5.65))-.12*math.sin(math.pi*ease(t,5.75,6.05)),'hand_contact':4.65<=t<6.25}
SHOTS={'A':shot_a,'B':shot_b,'C':shot_c}
