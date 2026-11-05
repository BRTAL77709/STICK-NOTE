from drawing import *
from actions import *

DIAGNOSTIC_WIDE=False
def house_camera(t):
 if not DIAGNOSTIC_WIDE and 9.45<=t<10.25:
  S=1500.;return lambda p:(600-S*(p[0]-1.87)+S*.46*(p[2]-.065),900-S*(p[1]-1.30)-S*.12*(p[2]-.065)),S,'interior bolt insert'
 if not DIAGNOSTIC_WIDE and 3.05<=t<4.94:
  S=1500.;return lambda p:(620+S*(p[0]-1.85)+S*.46*p[2],905-S*(p[1]-1.25)+S*.12*p[2]),S,'key insert'
 if t>=7.8:
  S=390.;return lambda p:(1450-S*p[0]-S*.46*p[2],1530-S*p[1]-S*.12*p[2]),S,'interior'
 S=350.;return lambda p:(85+S*p[0]+S*.15*p[2],1550-S*p[1]+S*.12*p[2]),S,'exterior'

def leaf(a,t,P,S,inside=False):
 def q(u,y,z=0):return doorpoint(t,u,y,z)
 poly(a,P,[q(.9,0),q(0,0),q(0,2.1),q(.9,2.1)],'url(#cloth)','#05111c',7)
 for lo,hi in [(.17,.84),(1.12,1.93)]:
  poly(a,P,[q(.78,lo),q(.12,lo),q(.12,hi),q(.78,hi)],'#1a3542','#46616e',2)
 line(a,P,[q(.9,.02),q(.9,2.08)],'#728b94',3)
 for y in [.24,1.76]:poly(a,P,[q(.015,y-.05),q(-.035,y-.05),q(-.035,y+.05),q(.015,y+.05)],'#6e848b',INK,2)
 # Both sides belong to one spindle and invariant leaf geometry.
 z=.065 if inside else -.065;center=q(.75,1.05,z);tip=handle(t,inside);r=S*.025;pc=P(center);a.ellipse(*pc,r,r,'#d4a05d',INK,2);line(a,P,[center,tip],'#dfb26b',S*.021)
 hole=q(.75,1.25,z);ph=P(hole);a.ellipse(*ph,S*.025,S*.038,'#d2a15e',INK,2);a.ellipse(*ph,S*.009,S*.023,'#04111a')
 if inside:
  bolt=q(.75,1.30,z)+V(-.07*E(t,9.7,10),0,0);line(a,P,[q(.83,1.30,z),q(.67,1.30,z)],'#879a9e',S*.025);line(a,P,[bolt+V(0,-.04,0),bolt+V(0,.04,0)],'#d8b778',S*.025)
 # Visible spring latch retracts after the completed key turn.
 deadbolt=.026*(1-E(t,4.45,4.58)+E(t,9.7,10.0));line(a,P,[q(.9,1.30),q(.9+deadbolt,1.30)],'#ddbf7e',S*.027)
 spring=.021*(1-E(t,5.45,5.65)+E(t,7.15,7.3)-E(t,9.15,9.28)+E(t,9.30,9.34));line(a,P,[q(.9,1.05),q(.9+spring,1.05)],'#b5c1bd',S*.022)

def key(a,d,P,S):
 if not d['keyvisible']:return
 b=d['keybow'];th=d['keyturn'];pts=[]
 for j in range(25):
  u=j*math.tau/24;x=.047*math.cos(u);y=.027*math.sin(u);pts.append(b+V(x*math.cos(th)-y*math.sin(th),x*math.sin(th)+y*math.cos(th),0))
 line(a,P,pts,INK,S*.014);line(a,P,pts,'#e2bb6f',S*.008)
 tip=d['keytip'].copy();tip[2]=min(0,tip[2]);line(a,P,[b,tip],INK,S*.014);line(a,P,[b,tip],'#d7ac60',S*.008)
 if d['keytip'][2]<0:
  q=d['keytip']+V(.025*math.cos(th),.025*math.sin(th),-.025);line(a,P,[d['keytip']+V(0,0,-.025),q],'#dfbc77',S*.012)

def house_scene(t):
 d=house(t);P,S,view=house_camera(t);a=begin();a.rect(0,0,1080,1920,'#0c202d');inside=d['inside'];a.rect(0,0,1080,1555,'url(#wall)');a.path('M0 1530 Q540 1490 1080 1530 V1920 H0Z','#102b37','#36515e',3)
 # Same front wall and exact aperture for both views; only material side changes.
 for y in np.arange(.25,3.2,.24):
  for x0,x1 in [(-2,1.7),(2.6,6)]:line(a,P,[V(x0,y,0),V(x1,y,0)],'#294752',1.5)
 opening=[V(1.7,0,0),V(2.6,0,0),V(2.6,2.1,0),V(1.7,2.1,0)];poly(a,P,opening,'#091d2b','#536c78',8)
 if not inside:
  for z in [.4,.8,1.2,1.6]:line(a,P,[V(1.72,0,z),V(2.6,0,z)],'#294958',2)
 else:
  # Interior wainscot and stairward light are inside; no exterior house number.
  line(a,P,[V(-.4,.9,.05),V(1.65,.9,.05)],'#47606a',3)
 leaf(a,t,P,S,inside)
 target=d['keybow'] if d['contact']=='key' else None
 character(a,d,P,S,target)
 # Key shaft stays in front of door until it passes the lock plane; fingertips cover only the bow.
 key(a,d,P,S)
 if target is not None:hand(a,P,d['pose']['arms'][0]['wrist'],S,target,True)
 if not inside:
  p=P(V(2.15,2.35,0));a.add(f'<text x="{p[0]}" y="{p[1]}" fill="#e7b26b" font-family="DejaVu Sans" font-size="46" text-anchor="middle">17</text>');p=P(V(2.85,1.8,0));a.ellipse(*p,S*.22,S*.36,'url(#amber)');a.rect(p[0]-19,p[1]-43,38,86,'#091924','#48616c',3,6);a.ellipse(p[0],p[1],11,27,'#efb46b')
 if view=='key insert':
  # Full-frame mechanism insert, same evaluated key/door/hand; no overlay labels.
  pass
 paper_details(a);return end(a),d

def stair_scene(t):
 d=stairs(t);root=d['pose']['root'];S=390.;cy=.8*max(0,root[1]-.65);cx=.65*(root[0]+.58)
 P=lambda p:(320+S*(p[0]+.58-cx)+S*.25*(p[2]-1.4),1490-S*(p[1]-cy)+S*.09*(p[2]-1.4));a=begin();a.rect(0,0,1080,1920,'url(#wall)')
 # Shared house floor plan: full twelve-riser flight rises to the actual2.4m landing.
 for k in range(12):
  x=-.5+k*.24;y=k*.2;pts=[V(x,y,1.0),V(x+.24,y,1.0),V(x+.24,y+.2,1.0),V(x,y+.2,1.0)];poly(a,P,pts,'#213d4a','#071521',3)
  poly(a,P,[V(x,y+.2,1.0),V(x+.24,y+.2,1.0),V(x+.24,y+.2,1.9),V(x,y+.2,1.9)],'#345461','#789398',2)
  line(a,P,[V(x,y+.2,1.0),V(x+.24,y+.2,1.0)],'#97a7a5',3)
 poly(a,P,[V(2.38,2.4,.9),V(4.5,2.4,.9),V(4.5,2.4,2.2),V(2.38,2.4,2.2)],'#1e3b49','#72878d',4)
 # Far railing: never covers the soles or the knee loading.
 for k in range(0,13,2):
  x=-.5+k*.24;y=k*.2;line(a,P,[V(x,y,1.94),V(x,y+.85,1.94)],'#4f707c',4)
 line(a,P,[V(-.5,.85,1.94),V(2.38,3.25,1.94)],'#82999e',7)
 line(a,P,[V(-1,0,.8),V(-.5,0,.8)],'#4e6b76',3)
 for y in [0,2.4]:line(a,P,[V(-2,y,2.2),V(5,y,2.2)],'#334f5d',3)
 character(a,d,P,S);p=P(V(2.65,3.5,2));a.ellipse(*p,140,230,'url(#amber)');paper_details(a);d['camera']={'scale':S,'track_x':cx,'track_y':cy};return end(a),d

def outside_scene(a,P):
 # Actual outside ground/car geometry projected through the upper-storey window from eyeY4.0m.
 eye=V(3.6,4.0,1.0)
 def Q(p):
  r=(0-eye[2])/(p[2]-eye[2]);v=eye+(p-eye)*r;return V(v[0],v[1],0)
 def op(pts,col,stroke=INK,w=3):poly(a,P,[Q(V(*x)) for x in pts],col,stroke,w)
 op([(0,0,-2),(7,0,-2),(7,0,-12),(0,0,-12)],'#102b38','#41616c')
 for z in [-3,-5,-7,-9]:line(a,P,[Q(V(0,0,z)),Q(V(7,0,z))],'#3c5965',2)
 # Parked sedan in real metre geometry, front towards house; no miniature scale cheat.
 x=4.1;z=-4.0
 def C(dx,y,dz):return (x+dx,y,z+dz)
 for xx in [-.84,.84]:
  wheel=[C(xx+.13*math.cos(j*math.tau/24),.28+.28*math.sin(j*math.tau/24),-.40) for j in range(25)];op(wheel,'#030c14','#3d5968',3)
 op([C(-.90,.25,0),C(.90,.25,0),C(.90,.85,0),C(-.90,.85,0)],'#0a1c29','#536c7a',4)
 op([C(-.90,.85,0),C(.90,.85,0),C(.72,1.05,-1.1),C(-.72,1.05,-1.1)],'#1d3544','#58707c',3)
 op([C(-.72,1.05,-1.1),C(.72,1.05,-1.1),C(.60,1.49,-2.0),C(-.60,1.49,-2.0)],'#3c5a69','#728895',3)
 op([C(-.60,1.49,-2),C(.60,1.49,-2),C(.62,1.47,-2.9),C(-.62,1.47,-2.9)],'#203946','#607b89',3)
 for dx in [-.66,.66]:op([C(dx-.18,.64,-.01),C(dx+.18,.64,-.01),C(dx+.16,.77,-.01),C(dx-.16,.77,-.01)],'#c5dce0','#adc4cc',2)
 op([C(-.34,.42,-.02),C(.34,.42,-.02),C(.34,.57,-.02),C(-.34,.57,-.02)],'#061420','#68808a',2)
 for j in range(5):line(a,P,[Q(V(*C(-.3,.44+j*.025,-.03))),Q(V(*C(.3,.44+j*.025,-.03)))],'#6f8996',1.5)

def window_scene(t):
 d=window(t);S=460.;P=lambda p:(70+(p[0]-2.35)*S+p[2]*50,1550-(p[1]-2.4)*S+p[2]*35);a=begin();a.rect(0,0,1080,1920,'url(#wall)');a.rect(0,1565,1080,355,'#172f3c')
 pts=[V(3.07,3.08,0),V(4.33,3.08,0),V(4.33,4.52,0),V(3.07,4.52,0)];pp=[P(p) for p in pts];a.add('<defs><clipPath id="window-hole"><polygon points="'+' '.join(f'{x},{y}' for x,y in pp)+'"/></clipPath></defs>');poly(a,P,pts,'#0b2331','#6c8994',8);a.add('<g clip-path="url(#window-hole)">');outside_scene(a,P)
 for j in range(25):
  x=3.09+(j*61%119)*.01;y=3.1+((j*.19-t*.40)%1.4);line(a,P,[V(x,y,0),V(x-.015,y-.07,0)],'#6a91a3',1.2)
 a.add('</g>')
 # Persistent cloth surface subdivided into changing folds. Rod remains fixed and rings slide.
 for j in range(40):
  u=j/40;v=(j+1)/40;points=[cloth(t,u,k/18) for k in range(19)]+[cloth(t,v,k/18) for k in reversed(range(19))];color=['#274958','#375e70','#1a3547','#305568'][j%4];poly(a,P,points,color,'none',0)
 for u in np.linspace(0,1,9):line(a,P,[cloth(t,u,k/22) for k in range(23)],'#74919b' if round(u*8)%2 else '#0c2231',1.5)
 line(a,P,[cloth(t,0,k/30) for k in range(31)],'#81979f',3)
 line(a,P,[V(2.98,4.56,.075),V(4.42,4.56,.075)],'#a8b0a7',7)
 for j in range(9):
  q=cloth(t,j/8,1);p=P(q+V(0,.04,0));a.ellipse(*p,5,9,'none','#d1c5a2',2);line(a,P,[q+V(0,.02,0),q],'#8da1a4',2)
 target=d['grip'] if d['cloth_contact'] else None;character(a,d,P,S,target)
 if target is not None:hand(a,P,d['pose']['arms'][0]['wrist'],S,target,True)
 paper_details(a);return end(a),d
SCENES={'HOUSE':house_scene,'STAIRS':stair_scene,'WINDOW':window_scene}
