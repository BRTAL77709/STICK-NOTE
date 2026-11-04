"""V10: shared orthographic world/ground plane; V8–V9 illustrated renderer and head assets."""
from illustration_engine import *
import illustration_engine as b
DURATION=10.;FPS=30
ROOT=Path(__file__).resolve().parents[1]
def smooth(x):
 x=max(0,min(1,x));return x*x*x*(10+x*(-15+6*x))
def ease(t,a,z):return smooth((t-a)/(z-a))
def V(x,y,z):return np.array([x,y,z],dtype=float)
def lerp(a,b,u):return np.asarray(a)+(np.asarray(b)-a)*u
def P(p):
 x,y,z=p;return (.9396926*x+.3420201*y,1320+.1961747*x-.5389855*y-.8191520*z)
def text3(p):return ','.join(f'{x:.5f}' for x in p)
def ik3(a,z,l1,l2,bend):
 v=z-a;d=float(np.linalg.norm(v))
 if d>l1+l2+.02 or d<abs(l1-l2)-.02:raise ValueError(f'IK reach {d:.3f} not [{abs(l1-l2)},{l1+l2}]')
 u=v/max(.001,d);q=min(l1+l2-.001,max(.001,d));along=(l1*l1-l2*l2+q*q)/(2*q);h=math.sqrt(max(0,l1*l1-along*along));bv=np.array(bend,float);bv-=u*np.dot(bv,u)
 if np.linalg.norm(bv)<.001:bv=np.cross(u,V(1,0,0))
 return a+along*u+h*bv/np.linalg.norm(bv)
def xz(v,a):
 x,down=v;c=math.cos(math.radians(a));s=math.sin(math.radians(a));return V(x*c+down*s,0,x*s-down*c)
def head_time(t):
 assert t<8 or lid_angle(t)==0
 if t<8:return 3.2
 if t<9.2:return 3.35+(t-8)*.65/1.2
 return 4+min(.5,t-9.2)
def lid_angle(t):return 72*ease(t,1.95,2.3)*(1-ease(t,6.95,7.5))
def lid_world(t,x=750,u=.88):
 a=math.radians(lid_angle(t));return V(x,135-123*u*math.cos(a),235+123*u*math.sin(a))
STATES=[(0,'DRAGGING'),(1.4,'TRUNK_OPENING'),(2.3,'TRUNK_OPEN'),(3,'LIFTING'),(4.6,'LOADING'),(6.2,'VICTIM_FULLY_INSIDE'),(6.7,'HANDS_WITHDRAWN'),(6.95,'TRUNK_CLOSING'),(7.5,'TRUNK_CLOSED'),(7.75,'WITNESS_NOTICED'),(8,'HEAD_TURN'),(9.2,'THREATENING_STARE')]
def state_at(t):return next(n for s,n in reversed(STATES) if t>=s)
# x,y positions on z=0. Holds are world anchors; only explicit swings can move them.
PLANS=(
 ((285,-435,((.15,.43,285,-340,24),(.85,1.12,285,-250,26),(1.78,2.02,285,-100,22),(2.32,2.52,275,-225,20),(4.70,5.10,295,-105,22))),
  (320,-395,((.50,.78,320,-305,24),(1.17,1.40,320,-215,24),(1.48,1.72,320,-125,22),(2.65,2.90,330,-200,20),(5.20,5.60,340,-35,22)))),
 ((705,-440,((.58,.86,705,-300,25),(1.23,1.42,705,-215,23),(2.60,2.85,700,-210,19),(4.65,4.95,850,-95,23))),
  (740,-390,((.25,.52,740,-335,22),(.93,1.20,740,-245,23),(2.32,2.53,830,-240,20),(5.00,5.35,885,-35,23))))
)
def foot_world(t,i,j):
 x,y,plan=PLANS[i][j]
 for start,end,xx,yy,lift in plan:
  if t<start:return V(x,y,0),True
  if t<end:
   u=(t-start)/(end-start);return V(mix(x,xx,smooth(u)),mix(y,yy,smooth(u)),lift*math.sin(math.pi*u)**1.3),False
  x,y=xx,yy
 return V(x,y,0),True

def actor_pose(t,i):
 approach=180*ease(t,.05,1.4);yy=-420+approach
 if i==0:
  x=300+33*ease(t,4.7,5.6);yy+=125*ease(t,1.48,2.02)-105*ease(t,2.32,2.9)+160*ease(t,4.7,5.6)
  hz=135-50*ease(t,2.3,3)+74*ease(t,3,4.6)
  lx=20+30*ease(t,2.3,3)+10*ease(t,4.7,5.6)-45*ease(t,7.75,8)
  ly=30+30*ease(t,4.7,5.6)
 else:
  x=720+60*ease(t,3,4.6)+50*ease(t,4.65,4.95)+30*ease(t,5.0,5.35)
  hz=135-45*ease(t,1.3,1.65)+69*ease(t,3,4.6)
  lx=-25-60*ease(t,1.3,1.65)-25*ease(t,3,4.6)+65*ease(t,4.65,5.35)+20*ease(t,7.5,7.85)
  ly=35+25*ease(t,4.65,5.35)
  yy+=20*ease(t,2.3,2.85)+70*ease(t,4.65,4.95)+90*ease(t,5.,5.35)
 if i==1:hz-=14*math.sin(math.pi*ease(t,4.65,5.35))
 hip=V(x,yy,hz);shoulder=hip+V(lx,ly,math.sqrt(max(1,125**2-lx*lx-ly*ly)))
 feet=[foot_world(t,i,j) for j in (0,1)];knees=[]
 for j,(ft,on) in enumerate(feet):
  h=hip+V(-15 if j==0 else 17,0,0);ank=ft+V(0,0,11);knees.append(ik3(h,ank,85,85,V(0,-1,0)))
 return {'hip':hip,'shoulder':shoulder,'feet':feet,'knees':knees,'lean':(lx,ly)}

def core(t):
 u=ease(t,3.,4.6);load=ease(t,4.6,5.5);lower=ease(t,5.5,6.2);a=90*ease(t,3.12,4.6)
 return V(500-50*u+55*load,-420+180*ease(t,.05,1.4)+20*ease(t,2.3,3)+285*load,215+115*u+12*ease(t,4.6,5.0)-187*lower),a

def victim_pose(t):
 S,a=core(t);past,aa=core(max(0,t-.10));vec=xz((-30,138),aa)+(past-S)*.3;vec*=math.hypot(30,138)/np.linalg.norm(vec);pelvis=S+vec
 sh=[S+xz(q,a) for q in [(-39,5),(35,7)]];el=[];hands=[];fold=ease(t,5.0,5.85)
 for j,(dx,down) in enumerate([(-45,63),(49,61)]):
  initial=xz((dx,down),a*.25);target=V(math.hypot(dx,down),0,0 if j==0 else -12)
  target*=math.hypot(dx,down)/np.linalg.norm(target);direction=lerp(initial,target,fold);direction*=math.hypot(dx,down)/np.linalg.norm(direction)
  e=sh[j]+direction;el.append(e);fore=V((-6 if j==0 else 6),0,-42)
  rest=V(-36,0,22 if j==0 else -22);rest*=math.hypot(6,42)/np.linalg.norm(rest);fv=lerp(fore,rest,fold);fv*=math.hypot(6,42)/np.linalg.norm(fv);hands.append(e+fv)
 hips=[];knees=[];feet=[];u=ease(t,3,4.6);tuck=ease(t,4.6,5.0)
 for j in (0,1):
  h=pelvis+xz((-18 if j==0 else 18,0),aa);hips.append(h)
  ground=V(S[0]-85+j*22,S[1]-70-j*10,11)
  hang=pelvis+V(60+j*18,-12-j*8,-115-j*4)
  ankle=lerp(ground,hang,u);ankle[2]=max(11,ankle[2]);tucked=pelvis+V(100+j*16,-28-j*5,-35+j*8);ankle=lerp(ankle,tucked,tuck)
  # Legs trail torso into the same opening, then settle on the cavity floor.
  ankle[1]=mix(ankle[1],core(max(0,t-.15))[0][1]-10*(1-ease(t,4.6,5.5))+j*12,ease(t,4.6,4.95));ankle[2]=mix(ankle[2],115+j*12,ease(t,5.5,6.2))
  delta=ankle-h;dist=np.linalg.norm(delta)
  if dist>156.5:ankle=h+delta*156.5/dist
  feet.append(ankle);knees.append(ik3(h,ankle,77,80,V(0,.1+1.0*ease(t,5.5,6.2),-1+1.7*ease(t,5.5,6.2))))
 grips=[lerp(sh[j],el[j],.53) for j in (0,1)]
 initialwaist=S+xz((30,80),a);waist=lerp(initialwaist,pelvis+V(15,0,10),ease(t,3.8,4.3))
 return {'S':S,'P':pelvis,'angle':a,'shoulders':sh,'elbows':el,'hands':hands,'hips':hips,'knees':knees,'feet':feet,'grips':grips,'back':S+xz((-25,5-35*ease(t,4.6,5.5)),a),'waist':waist,'neck':S+xz((0,-61),core(max(0,t-.12))[1]),'fold':fold}

def hand_arc(a,b,u):
 c=V((a[0]+b[0])/2,-5,400);return (1-u)**2*a+2*u*(1-u)*c+u*u*b

def contacts(t,ps,v):
 free=[[ps[0]['hip']+V(25,-20,-28),ps[0]['hip']+V(-30,-20,-28)],[ps[1]['hip']+V(-25,-20,-28),ps[1]['hip']+V(30,-20,-28)]]
 hs=[[v['grips'][0],lerp(free[0][1],v['back'],ease(t,2.3,2.9))],[v['grips'][1],lerp(free[1][1],v['waist'],ease(t,1.25,1.55))]]
 if 1.7<t<2.8:
  contact=lid_world(t,430)
  if t<1.95:hs[0][0]=hand_arc(v['grips'][0],contact,ease(t,1.7,1.95))
  elif t<2.10:hs[0][0]=contact
  else:hs[0][0]=lerp(lid_world(2.10,430),v['grips'][0],ease(t,2.10,2.8))
 hs[0][0]=lerp(hs[0][0],v['S']+xz((0,20),v['angle']),ease(t,4.6,5.5))
 hs[1][0]=lerp(hs[1][0],v['waist'],ease(t,3.15,3.5))
 hs[1][1]=lerp(hs[1][1],v['knees'][1],ease(t,3.8,4.2))
 hs[1][0]=lerp(hs[1][0],v['knees'][1],ease(t,4.65,5.25))
 hs[1][1]=lerp(hs[1][1],v['feet'][1],ease(t,4.9,5.45))
 for i,j,start,end in [(0,0,6.2,6.55),(0,1,6.25,6.65),(1,0,6.2,6.6),(1,1,6.25,6.7)]:hs[i][j]=hand_arc(hs[i][j],free[i][j],ease(t,start,end))
 if t>=6.7:
  hs[1][0]=hand_arc(free[1][0],lid_world(t),ease(t,6.7,6.95))
  if t>=7.5:hs[1][0]=hand_arc(lid_world(7.5),free[1][0],ease(t,7.5,7.75))
 return hs

def limb3(a,points,color,width,tag):
 a.add(f'<g id="{tag}" data-world-joints="{";".join(text3(p) for p in points)}">');limb(a,[P(p) for p in points],color,width);a.add('</g>')
def poly3(a,points,fill,stroke=OUTLINE,w=5):a.poly([P(p) for p in points],fill,stroke,w)
def line3(a,points,color,w):a.line([P(p) for p in points],color,w)
def shoe3(a,p,tag,color='#172a35'):
 x,y,z=p;a.add(f'<g id="{tag}" data-world="{text3(p)}">')
 poly3(a,[V(x-18,y-10,z),V(x+29,y-10,z),V(x+33,y+13,z),V(x-19,y+13,z)],color,OUTLINE,5)
 line3(a,[V(x-15,y-11,z+3),V(x+28,y-11,z+3)],'#8d9c9e',2.5);a.add('</g>')

# Sedan is a stable object in the same metric world as all articulated joints.
OPENING=[V(380,12,235),V(840,12,235),V(825,135,235),V(395,135,235)]
def car(a,t,layer):
 if layer=='back':
  # Ground shadow and far wheels.
  a.ellipse(*P(V(610,230,0)),300,50,'#02090f')
  for x,y in [(360,75),(840,75),(840,485)]:
   center=V(x,y,66);outer=[P(center+V(0,66*math.cos(k*math.pi/16),66*math.sin(k*math.pi/16))) for k in range(32)];inner=[P(center+V(0,42*math.cos(k*math.pi/16),42*math.sin(k*math.pi/16))) for k in range(32)];b.curved_outline(a,outer,'#02070d','#354951',4);b.curved_outline(a,inner,'#24343f',OUTLINE,3)
  poly3(a,[V(360,0,80),V(840,0,80),V(840,600,80),V(385,600,80),V(360,0,210)],'#0a1721')
  poly3(a,[V(840,0,80),V(840,0,220),V(800,600,205),V(800,600,85)],'#152a36','#3b5460',4)
  poly3(a,[V(360,0,220),V(840,0,220),V(800,600,205),V(385,600,205)],'url(#metal)')
  # Cabin, rear window and right-side windows.
  poly3(a,[V(395,160,235),V(825,160,235),V(795,340,350),V(425,340,350)],'#0b1b28','#4a6370',5)
  poly3(a,[V(420,180,253),V(801,180,253),V(777,325,335),V(444,325,335)],'#07131e','#344d5c',3)
  poly3(a,[V(425,340,350),V(795,340,350),V(760,500,345),V(455,500,345)],'#1b303c','#445c68',4)
  poly3(a,[V(825,160,235),V(795,340,350),V(760,500,345),V(800,570,220)],'#102431','#405c6b',4)
  poly3(a,[V(817,190,253),V(782,342,334),V(752,479,328),V(789,532,242)],'#06141f','#324b59',3)
  line3(a,[V(785,347,333),V(798,385,240)],'#39505f',5)
  line3(a,[V(842,160,180),V(807,545,175)],'#3d5460',3)
  line3(a,[V(840,325,180),V(832,325,94)],'#06111a',4)
  line3(a,[V(837,350,175),V(836,390,175)],'#839297',3)
  poly3(a,OPENING,'#03080e','#617782',7)
  poly3(a,[V(395,22,90),V(825,22,90),V(811,128,90),V(409,128,90)],'#0b1a24','#223843',3)
  for x in [405,815]:line3(a,[V(x,22,100),V(x,120,100)],'#273c47',3)
 if layer=='front':
  poly3(a,[V(360,0,80),V(840,0,80),V(840,0,220),V(360,0,220)],'url(#metal)',OUTLINE,6)
  line3(a,[V(380,12,235),V(840,12,235)],'#7d9198',7)
  for x0,x1 in [(375,480),(725,828)]:
   poly3(a,[V(x0,-3,181),V(x1,-3,181),V(x1,-3,161),V(x0,-3,165)],'#df504b','#68252d',3)
   line3(a,[V(x0+7,-4,175),V(x1-9,-4,175)],'#ffb08d',3)
  poly3(a,[V(550,-4,136),V(648,-4,136),V(648,-4,108),V(550,-4,108)],'#a4aeaa',OUTLINE,3)
  line3(a,[V(570,-5,121),V(626,-5,121)],'#374a52',3)
  poly3(a,[V(350,-16,100),V(850,-16,100),V(850,-16,72),V(350,-16,72)],'#10212d','#3a535f',4)
 if layer=='lid':
  th=math.radians(lid_angle(t))
  def L(x,y):return V(x,135-(135-y)*math.cos(th),235+(135-y)*math.sin(th))
  a.add(f'<g id="trunk-lid" data-angle="{lid_angle(t)}" data-hinge="380,135,235;840,135,235">')
  for x in [397,823]:line3(a,[V(x,100,170),L(x,30)],'#657985',4)
  sh=ease(lid_angle(t),5,40);fill='rgb('+','.join(str(round(mix(c,d,sh))) for c,d in zip((39,62,75),(11,25,35)))+')'
  poly3(a,[L(380,12),L(840,12),L(825,135),L(395,135)],fill,'#59717e',5)
  line3(a,[L(401,28),L(818,28)],'#314c5b',3)
  line3(a,[L(405,118),L(813,118)],'#354e5a',2)
  line3(a,[L(597,27),L(625,27)],'#96a1a2',4);a.add('</g>')


def elbow_bend(t,sign,hand):
 u=ease(hand[1],-15,20);return V(sign,mix(-.7,1.3,u),mix(.1,1.2,u))

def actor_draw(a,t,i,p,hs,part='body',hide_eyes=False):
 hip=p['hip'];sh=p['shoulder'];sx,sy=P(sh);hx,hy=P(hip)
 if part=='body':
  a.add(f'<g id="actor-{i+1}" data-hip-world="{text3(hip)}" data-shoulder-world="{text3(sh)}">')
  for j,(ft,on) in enumerate(p['feet']):
   h=hip+V(-15 if j==0 else 17,0,0);ank=ft+V(0,0,11);limb3(a,[h,p['knees'][j],ank],'#172833' if j==0 else '#243945',28,f'actor-{i+1}-leg-{j}')
   shoe3(a,ft,f'actor-{i+1}-foot-{j}')
  a.path(f'M{sx-44},{sy-8} Q{sx-61},{sy+15} {hx-45},{hy+15} Q{hx},{hy+30} {hx+48},{hy+12} L{sx+45},{sy+7} Q{sx+27},{sy-19} {sx-44},{sy-8}Z','url(#cloth)',OUTLINE,7)
  a.path(f'M{sx-32},{sy+18} L{hx-30},{hy+9} M{sx+21},{sy+27} L{hx+24},{hy-4}','none','#3c4d56',2)
  a.path(f'M{sx-3},{sy+20} L{hx+1},{hy+17} M{hx-25},{hy-26} Q{hx},{hy-16} {hx+25},{hy-27}','none','#07121c',4)
  a.path(f'M{sx-37},{sy-13} Q{sx},{sy+42} {sx+36},{sy-12} L{sx+21},{sy-37} L{sx-25},{sy-35}Z','#0b1722',OUTLINE,5)
  a.line([(sx-15,sy+12),(sx-17,sy+51)],'#617079',2);a.line([(sx+14,sy+12),(sx+16,sy+47)],'#617079',2)
  effort=ease(t,3,4.6)*(1-ease(t,6.7,7.75));head=sh+V((-23 if i==0 else 18)*effort,-15*effort,72)
  xx,yy=P(head);a.path(f'M{sx-18},{sy-14} L{xx-17},{yy+58} L{xx+17},{yy+58} L{sx+18},{sy-12}Z','#0b1721',OUTLINE,3)
  b.draw_head(a,xx,yy,head_time(t),i+1,hide_eyes)
  a.path(f'M{sx-43},{sy+7} Q{sx-53},{sy+35} {hx-44},{hy-2}','none','#da9a4b',3);a.add('</g>')
 else:
  for j in [1,0]:
   sign=(1 if i==0 else -1)*(1 if j==0 else -1);ss=sh+V(sign*35,-3,-12);hand=hs[j];el=ik3(ss,hand,90,87,elbow_bend(t,sign,hand))
   limb3(a,[ss,el,hand],'#203440' if j==0 else '#172833',27,f'actor-{i+1}-arm-{j}');px,py=P(hand)
   a.ellipse(px,py,15,17,'#0a1720','#5c7680',3,extra=f'id="grip-{i+1}-{j}" data-world="{text3(hand)}"')
   a.line([(px-6,py-6),(px-5,py+5)],'#71888e',1.5);a.line([(px+1,py-7),(px+2,py+4)],'#71888e',1.5)


def victim_draw(a,t,v):
 S=v['S'];pel=v['P'];angle=v['angle'];a.add(f'<g id="victim" data-shoulder-world="{text3(S)}" data-pelvis-world="{text3(pel)}" data-angle="{angle}">')
 for j in (0,1):
  limb3(a,[v['hips'][j],v['knees'][j],v['feet'][j]],'#213b47',26,f'victim-leg-{j}');shoe3(a,v['feet'][j]-V(0,0,11),f'victim-shoe-{j}',color='#08151e')
 sl,sr=[P(p) for p in v['shoulders']];left=P(pel+xz((-39,2),angle));right=P(pel+xz((39,0),angle));mid=lerp(S,pel,.48)
 a.path(f'M{pt(sl)} Q{pt(P(mid+xz((-46,0),angle)))} {pt(left)} Q{pt(P(pel+xz((0,23),angle)))} {pt(right)} Q{pt(P(mid+xz((43,0),angle)))} {pt(sr)}Z','#b8bdbb',OUTLINE,6)
 a.line([sr,P(mid+xz((25,0),angle)),right],'#74848b',12)
 # Blood and folds follow the same torso hierarchy through the world projection.
 blood=[(-3,30),(-16,55),(-8,66),(-12,93),(-1,75),(2,58),(12,54),(5,32)]
 poly3(a,[S+xz(p,angle) for p in blood],'#8d3037','none',0)
 line3(a,[pel+xz((-28,-18),angle),mid+xz((0,16),angle),pel+xz((9,-23),angle)],'#86979c',2)
 for j in (0,1):
  limb3(a,[v['shoulders'][j],v['elbows'][j],v['hands'][j]],'#bdc0bf',23,f'victim-arm-{j}');a.ellipse(*P(v['hands'][j]),12,16,'#c1c6c3',OUTLINE,3)
 hx,hy=P(v['neck']);roll=22-v['angle']+6*math.sin(math.pi*ease(t,3.,4.7))
 a.add(f'<g id="victim-head" transform="translate({hx} {hy}) rotate({roll})">')
 a.ellipse(0,0,51,58,'url(#face)',OUTLINE,5);a.path('M-51 -10 Q-57 -60 -7 -63 Q48 -64 52 -11 L48 6 Q-4 -9 -51 -10Z','#111f2a',OUTLINE,5)
 a.line([(-35,-37),(39,-13)],'#b78343',2);a.path('M-27 15 l14 4 M10 19 l12 -1 M-8 38 q10 -4 16 1','none','#18222b',3);a.path('M30 29 l-7 9','none','#9e4345',3);a.add('</g></g>')

def scene(t,hide_eyes=False,debug=False):
 a=Art();rng=random.Random(717)
 a.add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">')
 a.add('''<defs>
 <linearGradient id="sky" x2="0" y2="1"><stop stop-color="#020a12"/><stop offset="1" stop-color="#153443"/></linearGradient>
 <linearGradient id="road" x2="0.25" y2="1"><stop stop-color="#142c34"/><stop offset="1" stop-color="#040d16"/></linearGradient>
 <linearGradient id="metal" x2="0.2" y2="1"><stop stop-color="#29414c"/><stop offset=".3" stop-color="#101e2a"/><stop offset="1" stop-color="#040c14"/></linearGradient>
 <linearGradient id="cloth" x2="1" y2=".3"><stop stop-color="#253540"/><stop offset=".55" stop-color="#14222d"/><stop offset="1" stop-color="#0b151e"/></linearGradient>
 <linearGradient id="face" x2="1" y2="1"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#9ca9af"/></linearGradient>
 <radialGradient id="lamp"><stop stop-color="#ffb254" stop-opacity=".4"/><stop offset="1" stop-color="#ff9c37" stop-opacity="0"/></radialGradient>
 <radialGradient id="vignette"><stop offset=".4" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#01070e" stop-opacity=".72"/></radialGradient>
 </defs>''')


 a.rect(0,0,1080,1920,'url(#sky)')
 ps=[actor_pose(t,i) for i in (0,1)];v=victim_pose(t);hs=contacts(t,ps,v);cam=12*ease(t,0,1.4)
 if t<8:scale=1.08;tx=-18;ty=-180
 else:
  head=ps[0]['shoulder']+V(0,0,72);xx,yy=P(head);scale=4.5+.15*ease(t,8,10);tx=mix(430,520,b.reaction(head_time(t)))-scale*(xx-cam);ty=850-scale*yy
 a.add(f'<g id="action-state" data-state="{state_at(t)}" data-lid-angle="{lid_angle(t)}"/>')
 a.add(f'<g id="cinematic-framing" data-shot="{1 if t<8 else 2}" transform="translate({tx} {ty}) scale({scale})"><g transform="translate({-cam} 0)">')
 a.add(f'<g id="far-city" transform="translate({cam*.7},0)">')
 for x,y,w,h in [(370,310,110,590),(490,190,115,720),(625,350,130,560),(780,280,180,650)]:
  a.rect(x,y,w,h,'#0a1c2b','#1a3543',2)
  for yy in range(y+35,y+h,57):
   for xx in range(x+15,x+w-12,32):
    if rng.random()>.4:a.rect(xx,yy,11,22,'#344744' if rng.random()>.3 else '#97632d')
 a.add('</g>')
 a.poly([(0,900),(530,845),(1080,960),(1080,1920),(0,1920)],'url(#road)',w=0)
 # illustrated masonry, layers converge toward vanishing point
 a.add(f'<g id="alley-walls" transform="translate({cam*.1},0)">')
 a.poly([(0,0),(300,0),(430,860),(0,1120)],'#102331','#020b13',6)
 a.poly([(0,0),(105,0),(190,1020),(0,1120)],'#081722',w=0)
 a.poly([(1080,0),(850,0),(700,865),(1080,1090)],'#142b36','#020b13',6)
 for y in range(95,1130,55):
  end=300+min(y,860)*.15
  a.line([(0,y),(end,y*.78+70)],'#29404a',2)
  for x in range(30,360,85):
   if x<end:a.line([(x,y-30),(x+8,y+10)],'#203642',2)
 for y in range(120,1000,60):a.line([(780,y),(1100,y+50)],'#31434a',2)
 a.poly([(72,340),(237,385),(270,918),(100,987)],'#06121b','#41606b',4)
 for x in [110,142,174,206]:a.line([(x,400),(x+33,931)],'#1b313e',4)
 a.line([(30,90),(40,810),(71,860),(85,1035)],'#06111a',20)
 a.line([(28,90),(38,810),(69,860)],'#3b5159',4)
 # door and barrel / refuse anchor the perspective
 a.poly([(869,470),(1040,400),(1040,1080),(804,990)],'#07141e','#3c535b',5)
 a.poly([(895,507),(1014,460),(1014,1017),(844,964)],'#142831','#07111a',4)
 a.line([(903,550),(1000,516)],'#29434e',3)
 a.ellipse(989,781,6,10,'#a77d41')
 a.rect(112,1030,169,161,'#11272b',OUTLINE,5,8);a.rect(101,1014,187,29,'#30423e',OUTLINE,5,7)
 for y in [1080,1140]:a.line([(116,y),(275,y)],'#3f5146',4)
 a.path('M0 1225 Q85 1120 154 1210 Q190 1250 125 1280 L0 1300Z','#07111a')
 # Illustrated service placard and fire escape; unchanged character designs.
 a.poly([(876,605),(970,570),(970,674),(851,710)],'#1b333e','#4d6266',3)
 a.add('<text x="884" y="635" fill="#c9b88a" font-size="18" font-family="DejaVu Sans" transform="rotate(-12 884 635)">SERVICE</text>')
 a.add('<text x="885" y="664" fill="#e2c18a" font-size="19" font-family="DejaVu Sans" transform="rotate(-12 885 664)">BAY 04</text>')
 for yy in [210,340]:
  a.line([(800,yy),(1060,yy-45)],'#06121b',13)
  a.line([(804,yy+6),(1057,yy-39)],'#40515a',3)
  for xx in range(830,1060,33):a.line([(xx,yy-60),(xx,yy-5-(xx-800)*.17)],'#263f4b',4)
 a.line([(848,218),(848,530)],'#132b37',9);a.line([(875,215),(875,519)],'#132b37',9)
 for yy in range(245,520,29):a.line([(848,yy),(875,yy-5)],'#4a5b61',3)
 a.add('</g>')
 # lamps and stylized reflection strokes
 flick= .93+.04*math.sin(t*3.1)+.025*math.sin(t*8)
 a.add(f'<g opacity="{flick}">');a.ellipse(810,460,280,350,'url(#lamp)')
 a.path('M875 320 L817 342 L807 452','none','#06121a',15)
 a.path('M790 449 Q808 422 829 447 L833 461 L788 461Z','#f8b158','#493a24',3)
 a.ellipse(809,461,26,6,'#ffe3a4');a.add('</g>')
 a.path('M799 470 L819 470 L980 1220 L450 1220Z','#ffc26a','none',0,'opacity=".045"')
 for i in range(95):
  y=rng.uniform(1010,1880);x=790+(y-1010)*-.12+rng.uniform(-100,100)*(y/1400)
  a.line([(x,y),(x+rng.uniform(12,80),y)],['#715337','#9c7040','#254550','#3c6571'][i%4],rng.uniform(1,4))
 for i in range(40):
  x=rng.uniform(50,1080);y=rng.uniform(1130,1880)
  a.line([(x,y),(x+rng.uniform(12,110),y-2)],'#183641',2)
 # Fixed pavement detail makes the world displacement directly readable.
 a.ellipse(515,1495,115,26,'#0b1b25','#37515b',3)
 for xx in range(435,600,18):a.line([(xx,1482),(xx+6,1507)],'#28424e',3)
 a.poly([(70,1500),(150,1486),(188,1550),(91,1562)],'#06151f','#314954',3)
 for yy in range(1508,1548,8):a.line([(89,yy),(156,yy-8)],'#52616a',2)
 a.path('M310 925 L325 1040 L310 1210 L339 1450 L330 1780','none','#27414c',2)
 for j in range(12):
  x=110+j*79;y=1460+(j%4)*83;phase=(t*.8+j*.173)%1
  a.ellipse(x,y,5+phase*24,1+phase*4,'none','#527984',1.3,extra=f'opacity="{.40*(1-phase)}"')


 # World-space pavement contacts/shadows precede every solid object.
 for i,p in enumerate(ps):
  for ft,on in p['feet']:
   ground=ft.copy();ground[2]=0;px,py=P(ground);a.ellipse(px,py+3,35,7,'#02090e',extra='opacity=".85"')
 car(a,t,'back')
 if t<6.95:car(a,t,'lid')
 if t>=5.5:
  ceiling=max(235.,v['S'][2]+70,v['neck'][2]+65,max(p[2]+18 for p in v['knees']))
  prism=[P(p) for p in OPENING]+[P(V(p[0],p[1],ceiling)) for p in OPENING]
  hull=b.hull(prism);a.add('<defs><clipPath id="interior-corridor"><polygon points="'+' '.join(pt(p) for p in hull)+'"/></clipPath></defs><g clip-path="url(#interior-corridor)">')
  victim_draw(a,t,v);a.add('</g>')
 car(a,t,'front')
 if t>=6.95:car(a,t,'lid')
 # Both criminals stand in the foreground/on the sides of the fixed car footprint.
 for i in (1,0):actor_draw(a,t,i,ps[i],hs[i],'body',hide_eyes)
 if t<5.5:victim_draw(a,t,v)
 for i in (1,0):actor_draw(a,t,i,ps[i],hs[i],'arms',hide_eyes)
 if t<3.4:
  for foot in v['feet']:
   ground=foot.copy();ground[2]=0;line3(a,[ground+V(-7,-28,1),ground+V(5,-4,1)],'#627f88',1.5)
 if debug:
  a.add('<g id="DEBUG-GROUND-CONTACTS">')
  for x in range(100,1101,100):line3(a,[V(x,-520,0),V(x,620,0)],'#326e75',1)
  for y in range(-500,601,100):line3(a,[V(100,y,0),V(1100,y,0)],'#326e75',1)
  poly3(a,[V(350,0,0),V(850,0,0),V(810,600,0),V(385,600,0)],'none','#e8675e',3)
  poly3(a,OPENING,'none','#47d5da',4)
  for i in (0,1):
   for j,(foot,on) in enumerate(ps[i]['feet']):
    a.ellipse(*P(foot),8,8,'#8cff91' if on else '#ffbc67',OUTLINE,2)
    x,y=P(foot);a.add(f'<text x="{x+10}" y="{y+18}" fill="#c9f8ec" font-size="13">C{i+1}/{j} z={foot[2]:.1f}</text>')
   for h in hs[i]:a.ellipse(*P(h),8,8,'none','#fff0aa',2)
  path=[P(victim_pose(q/30)['P']) for q in range(round(t*30)+1)]
  if len(path)>1:a.line(path,'#df78ed',2)
  a.ellipse(*P(v['P']),9,9,'none','#df78ed',3);a.add('</g>')
 if t<8:
  for layer,count in [(0,180),(1,160),(2,80)]:
   a.add(f'<g opacity="{[.17,.26,.36][layer]}">')
   for j in range(count):
    x=rng.uniform(-100,1200);y=(rng.uniform(-100,2000)+t*[520,760,1120][layer])%2080-80
    a.line([(x,y),(x-4-layer*2,y+18+12*layer)],'#80a6b5',[1,1.4,2][layer])
   a.add('</g>')
 a.add('</g></g>')
 if t>=8:
  for j in range(110):
   x=rng.uniform(0,1180);y=(rng.uniform(-100,1920)+t*1050)%2100-100;a.path(f'M{x},{y} l-5 43','none','#6d96a7',1.7,'opacity=".3"')
 a.rect(0,0,1080,1920,'url(#vignette)')
 if debug:a.add(f'<text x="40" y="80" fill="#9bf6ed" font-size="25">WORLD Z=0 / {t:.2f}s / {state_at(t)}</text>')
 a.add('</svg>');return ''.join(a.s)
def audio():
 sr=48000;n=sr*10;rng=np.random.default_rng(119);ts=np.arange(n)/sr;noise=rng.standard_normal(n)
 track=(noise-np.roll(noise,1))*.027+.016*np.sin(2*np.pi*43*ts);events=[]
 def hit(when,kind,amp=.08,pitch=62,duration=.24):
  pos=round(when*sr);nn=min(int(duration*sr),n-pos);tt=np.arange(nn)/sr
  track[pos:pos+nn][:]+=amp*np.sin(2*np.pi*(pitch*tt-25*tt*tt))*np.exp(-tt*22)+rng.standard_normal(nn)*amp*.6*np.exp(-tt*45)
  events.append({'time':when,'frame':round(when*30),'event':kind})
 prev={}
 for f in range(1201):
  t=f/120
  for i in (0,1):
   for j,(p,on) in enumerate(actor_pose(t,i)['feet']):
    key=i,j
    if on and key in prev and not prev[key]:hit(t,'wet foot plant',.14,80)
    prev[key]=on
 for when,kind in [(1.95,'trunk opening latch'),(2.3,'open strut stop'),(5.5,'fabric over sill'),(6.2,'body rests inside'),(7.47,'trunk closing thump'),(8.0,'restrained reaction accent')]:hit(when,kind)
 # Distinct short latch click on the exact fully-closed frame (225).
 hit(7.5,'trunk CLOSED latch click',.16,1450,.075)
 moving=(ts>.1)&(ts<3.6);track+=np.convolve(rng.standard_normal(n),np.ones(9)/9,mode='same')*.022*moving
 track*=np.minimum(1,ts/.08)*np.minimum(1,(10-ts)/.15);stereo=np.column_stack((track,np.roll(track,97)*.97));pcm=(np.clip(stereo,-.95,.95)*32767).astype('<i2')
 dest=ROOT/'assets/original_ambience.wav'
 with wave.open(str(dest),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
 (ROOT/'assets/sound-events.json').write_text(json.dumps(events,indent=2));return dest
def main():
 p=argparse.ArgumentParser();p.add_argument('--scale',type=float,default=.5);p.add_argument('--fps',type=int,default=30);p.add_argument('--out',default='previews/V10_preview_01.mp4');p.add_argument('--stills',action='store_true');p.add_argument('--hide-eyes',action='store_true');args=p.parse_args()
 w=round(1080*args.scale/2)*2;h=round(1920*args.scale/2)*2;r=Raster(w,h)
 out=ROOT/args.out
 if out.exists():raise SystemExit('Refusing to overwrite '+str(out))
 out.parent.mkdir(parents=True,exist_ok=True)
 (ROOT/'assets').mkdir(parents=True,exist_ok=True)
 (ROOT/'previews').mkdir(parents=True,exist_ok=True)
 wav=audio()
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(args.fps),'-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','10','-movflags','+faststart',str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 samples=[]
 for i in range(10*args.fps):
  t=i/args.fps;svg=scene(t,hide_eyes=args.hide_eyes);im=r.render(svg);proc.stdin.write(im.tobytes())
  if args.stills and i%max(1,args.fps//4)==0:
   thumb=im.resize((216,384));samples.append((t,thumb))
  if i in [0,args.fps*2,args.fps*4,10*args.fps-1]:
   im.save(ROOT/'previews'/f'frame_{i:03d}_{w}.png')
   (ROOT/'assets'/f'scene_{t:.3f}.svg').write_text(svg)
  if i%args.fps==0:print(f'{i}/{10*args.fps}',flush=True)
 proc.stdin.close()
 if proc.wait():raise RuntimeError('ffmpeg failed')
 if samples:
  cols=5;sheet=Image.new('RGB',(cols*216,math.ceil(len(samples)/cols)*410),'#07121d');draw=ImageDraw.Draw(sheet)
  for j,(t,im) in enumerate(samples):
   x=j%cols*216;y=j//cols*410;sheet.paste(im,(x,y));draw.text((x+8,y+387),f'{t:.2f}s',fill='white')
  sheet.save(ROOT/'previews'/f'contact_{w}.jpg',quality=90)
 print(out)
if __name__=='__main__':main()
