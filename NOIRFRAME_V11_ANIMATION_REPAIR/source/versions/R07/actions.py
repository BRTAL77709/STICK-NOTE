"""New V11 authored action channels; not a retime or reuse of the rejected proof clips."""
from rig import *
HAND_ARC_U=1.60
DURATIONS={'HOUSE':11.,'STAIRS':8.5,'WINDOW':7.5}
H_INIT=[(.37,0,-.53),(.55,0,-.37)]
H_PLANS=[[(.08,.35,(.72,0,-.53),.10),(.70,.98,(1.20,0,-.53),.13),(5.30,5.65,(1.65,0,-.35),.11),(6.20,6.55,(2.02,0,.42),.12),(7.15,7.5,(1.90,0,1.22),.12),(8.60,8.95,(1.35,0,.56),.09)],[(.39,.67,(.98,0,-.37),.13),(1.02,1.28,(1.40,0,-.37),.09),(5.76,6.12,(1.95,0,.08),.12),(6.72,7.08,(2.10,0,1.10),.12),(8.05,8.42,(1.70,0,.74),.09),(9.38,9.72,(1.45,0,.60),.08)]]
def door_angle(t):return math.radians(77)*(E(t,5.70,6.95)-E(t,8.05,9.3))
def doorpoint(t,u=.75,y=1.05,z=-.055):
 a=door_angle(t);return V(2.6-u*math.cos(a)+z*math.sin(a),y,u*math.sin(a)+z*math.cos(a))
def lever(t):return -.20*math.sin(math.pi*E(t,1.55,2.05))-.27*(E(t,5.45,5.65)-E(t,6.8,7.15))
def handle(t,inside=False):
 p=doorpoint(t,y=1.05,z=.065 if inside else -.065);q=lever(t);p+=V(.055*math.cos(q)*math.cos(door_angle(t)),.055*math.sin(q),-.055*math.cos(q)*math.sin(door_angle(t)));return p

def house_arm_pole(t,root,lean,hand):
 a=door_angle(t);N=V(math.sin(a),0,math.cos(a));U=V(-math.cos(a),0,math.sin(a));sh=root+V(lean+.13,.488,-.025);sn=float(np.dot(sh-V(2.6,0,0),N));hn=float(np.dot(hand-V(2.6,0,0),N));sa=E(sn,-.30,.30);ha=E(hn,-.08,.08);fw=(1-sa)*(1-ha);bw=sa*ha;ew=1-fw-bw
 return fw*(-N-.5*U)+bw*(N-.5*U)+ew*U+V(0,-.50,0)

def house(t):
 root=keys(t,[(0,(.45,.66,-.45)),(.3,(.65,.63,-.45)),(.65,(.90,.67,-.45)),(1,(1.15,.63,-.45)),(1.3,(1.25,.66,-.45)),(5.3,(1.25,.66,-.45)),(5.75,(1.55,.64,-.30)),(6.2,(1.85,.65,.05)),(6.6,(2.0,.66,.34)),(7.15,(2.02,.66,.86)),(7.75,(1.96,.65,1.16)),(8.4,(1.88,.65,.90)),(9.3,(1.40,.65,.58)),(11,(1.40,.66,.58))]);ff=feet(t,H_INIT,H_PLANS)
 lean=.13*E(t,0,.3)*(1-E(t,1,1.35))+.11*(E(t,1.35,1.58)-E(t,2.0,2.3))+.13*(E(t,3.0,3.25)-E(t,4.7,5))+.07*(E(t,5.2,5.5)-E(t,7.1,7.6))
 rest=[root+V(.20,.12,-.02),root+V(-.10,-.03,.02)];hands=[x.copy() for x in rest];contact=None
 keyvisible=2.75<=t<5.18;keyturn=math.pi/2*(E(t,4.10,4.40)-E(t,4.55,4.70));hole=V(1.85,1.25,0);bow=hole+V(0,0,-.30+.20*E(t,3.65,4.10)-.20*E(t,4.70,4.94));pocket=root+V(.16,.04,-.075)
 if t<1.30:
  for j in range(2):hands[j]=mix(root+V((.19,-.19)[j]+.12*math.sin(t*9+j*math.pi),.18+.08*math.cos(t*9+j*math.pi),(-.04,.04)[j]),rest[j],E(t,1.0,1.3))
 elif t<2.05:
  hands[0]=mix(rest[0],handle(t),E(t,1.3,1.55));contact='lever' if t>=1.55 else None
 elif t<2.75:hands[0]=mix(handle(2.05),pocket,E(t,2.05,2.42))
 elif t<3.65:
  reveal=hole+V(-.16,-.10,-.38);bow=mix(pocket+V(.035,.025,.035),reveal,E(t,2.75,3.18));bow=mix(bow,hole+V(0,0,-.30),E(t,3.18,3.65));hands[0]=bow+V(-.035,-.025,-.035);contact='key'
 elif t<4.94:hands[0]=bow+V(-.035*math.cos(keyturn),-.025-.035*math.sin(keyturn),-.035);contact='key'
 elif t<5.18:
  bow=mix(hole+V(0,0,-.30),pocket+V(.035,.025,.035),E(t,4.94,5.18));hands[0]=bow+V(-.035,-.025,-.035);contact='key'
 elif t<5.45:hands[0]=mix(pocket,handle(t),E(t,5.18,5.45))
 elif t<7.25:hands[0]=handle(t);contact='lever'
 elif t<8.05:
  u=E(t,7.25,8.05);hands[0]=(1-u)**2*handle(7.25)+2*u*(1-u)*doorpoint(t,HAND_ARC_U,1.22,0)+u*u*handle(t,True)
 elif t<9.35:hands[0]=handle(t,True);contact='inside lever'
 elif t<10.25:
  bolt=doorpoint(t,u=.75,y=1.30,z=.065)+V(-.07*E(t,9.7,10.0),0,0);hands[0]=mix(handle(t,True),bolt,E(t,9.35,9.65));contact='bolt' if t>=9.65 else None
 else:hands[0]=mix(doorpoint(t,u=.75,y=1.30,z=.065)+V(-.07,0,0),rest[0],E(t,10.25,10.6))
 # Far hand stays relaxed during the failed pull; it braces only for the key read.
 if 2.70<t<5.35:hands[1]=mix(rest[1],V(1.67,1.42,-.045),E(t,2.70,3.30)*(1-E(t,4.70,5.35)))
 fear=.45+.32*(E(t,1.8,2.2)-E(t,5,5.5))+.2*E(t,10.2,10.7);yaw=.72-.45*E(t,10.25,10.7);pose=skeleton(root,ff,hands,lean,yaw,fear,head_tilt=4*math.sin(math.pi*E(t,2,2.4)),head_lead=.025*math.sin(t*2.1),breath=.004*math.sin(t*7),arm_poles=[house_arm_pole(t,root,lean,hands[0]),V(-1,-.35,.3)])
 return {'pose':pose,'time':t,'phase':('approach' if t<1.3 else 'failed handle' if t<2.05 else 'retrieve key' if t<3.18 else 'align' if t<3.65 else 'insert' if t<4.1 else 'rotate' if t<4.7 else 'withdraw' if t<4.94 else 'store key' if t<5.18 else 'reach handle' if t<5.45 else 'open' if t<6.95 else 'enter' if t<8.05 else 'close' if t<9.35 else 'lock and react'),'door_angle':door_angle(t),'lever':lever(t),'keyvisible':keyvisible,'keybow':bow,'keyturn':keyturn,'keytip':bow+V(0,0,.16),'contact':contact,'inside':t>=7.8}

def stair_plans():
 plans=[[],[]]
 for k in range(1,13):
  j=(k-1)%2;a=.40+(k-1)*.58;b=a+.34;plans[j].append((a,b,(-.5+(k-.5)*.24,k*.20,1.4+(-.08,.08)[j]),.18))
 return plans
S_PLANS=stair_plans();S_PLANS[0].append((7.23,7.55,(2.45,2.4,1.32),.17));S_INIT=[(-.78,0,1.32),(-.65,0,1.48)]
def stairs(t):
 ff=feet(t,S_INIT,S_PLANS);rows=[(0,(-.58,.66,1.4)),(.4,(-.60,.61,1.4))]
 for k in range(1,13):
  a=.4+(k-1)*.58;b=a+.34;rows.append((b,(-.5+(k-.5)*.24-.12,.64+(k-1)*.2,1.4)));rows.append((a+.55,(-.5+(k-.5)*.24-.03,.65+(k-1)*.2,1.4)))
 rows.extend([(7.55,(2.31,3.04,1.4)),(8.15,(2.31,3.13,1.4)),(8.5,(2.31,3.13,1.4))]);root=keys(t,rows);root[1]+=.04;lean=.10*E(t,.12,.4)*(1-E(t,7.25,7.8));sway=.018*math.sin(t*math.pi/.58);hands=[root+V(.18+.16*math.sin(t*5.4)*(1-E(t,7.1,7.65)),.03+.09*math.cos(t*5.4)*(1-E(t,7.1,7.65)),-.12),root+V(-.10,-.02,.12)];rail=V(min(2.38,root[0]+.02),.85+(min(2.38,root[0]+.02)+.5)*(.2/.24),1.94);hands[1]=mix(hands[1],rail,E(t,.1,.4)*(1-E(t,7.3,7.8)));pose=skeleton(root,ff,hands,lean,.8,.65,head_tilt=-4*math.sin(t*2)*(1-E(t,7.1,7.8)),head_lead=.025*math.sin(t*5.4-.3)*(1-E(t,7.1,7.8)),breath=.006*math.sin(t*6));return {'time':t,'pose':pose,'phase':'anticipation' if t<.4 else 'climb' if t<7.1 else 'landing and recover'}

W_INIT=[(2.35,2.4,.78),(2.54,2.4,.92)];W_PLANS=[[(.10,.45,(2.67,2.4,.62),.10),(2.95,3.32,(2.98,2.4,.40),.07),(3.85,4.22,(3.28,2.4,.40),.08),(5.15,5.52,(2.98,2.4,.65),.08)],[(.55,.90,(2.85,2.4,.76),.09),(3.38,3.75,(3.20,2.4,.55),.07),(5.62,5.98,(2.80,2.4,.77),.08)]]
def cloth(t,u=0,v=.35):
 q=E(t-.11*abs(v-.35),2.65,4.40);left=3.13+.97*q;settle=.012*math.sin(max(0,t-4.4)*13)*math.exp(-max(0,t-4.4)*4)*E(t,4.4,4.55);left+=settle
 return V(left+(4.3-left)*u,3.1+1.4*v+.025*math.sin(math.pi*u)*(1-v)*math.sin(t*4),.075+.030*math.sin(u*math.tau*8)*(1+.8*q))
def window(t):
 root=keys(t,[(0,(2.40,3.06,.85)),(.5,(2.62,3.03,.69)),(1.05,(2.73,3.06,.64)),(2.65,(2.73,3.04,.64)),(3.3,(2.92,3.02,.52)),(3.8,(3.14,3.04,.47)),(4.4,(3.26,3.04,.47)),(5.05,(3.26,3.04,.47)),(5.6,(3.05,3.02,.64)),(6.2,(2.89,3.05,.72)),(7.5,(2.89,3.06,.72))]);root[1]+=.06;ff=feet(t,W_INIT,W_PLANS);grip=cloth(t);rest=[root+V(.23,0,-.02),root+V(-.12,-.02,.02)];hands=rest.copy();contact=2.4<=t<5.05;wrist=grip+V(-.045,-.015,.025)
 if 1.5<t<2.4:hands[0]=mix(rest[0],wrist,E(t,1.5,2.4))
 elif contact:hands[0]=wrist
 elif 5.05<=t<5.70:hands[0]=root+mix(cloth(5.05)+V(-.045,-.015,.025)-V(3.26,3.10,.47),V(.23,0,-.02),E(t,5.05,5.70))
 if t>=5.70:hands[0]=mix(rest[0],root+V(.01,.39,-.10),E(t,5.70,6.35))
 lean=.12*(E(t,1.5,2.4)-E(t,5.05,5.4))-.07*(E(t,5.10,5.4)-E(t,5.8,6.4));yaw=.75-.65*E(t,5.3,6.2);fear=.35+.6*E(t,4.7,5.55);pose=skeleton(root,ff,hands,lean,yaw,fear,head_tilt=5*(E(t,4.35,4.8)-E(t,5.1,5.6)),head_lead=.04*E(t,4.35,4.8)-.04*E(t,5.1,5.45),breath=.005*math.sin(t*8));return {'time':t,'pose':pose,'phase':'approach' if t<1.5 else 'reach' if t<2.4 else 'pinch' if t<2.65 else 'pull' if t<4.4 else 'notice car' if t<5.05 else 'recoil and hold','cloth_contact':contact,'grip':grip}
STATES={'HOUSE':house,'STAIRS':stairs,'WINDOW':window}
