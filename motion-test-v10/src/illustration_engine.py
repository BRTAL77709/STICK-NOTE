"""V8 eight-second trunk loading. V7 illustrated assets, head projection and local renderer preserved."""
import math,random,ctypes as C,ctypes.util,subprocess,argparse,json,wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUTLINE='#030b12'
def smooth(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,t):return a+(b-a)*t
def pt(p):return f'{p[0]:.2f},{p[1]:.2f}'
class Art:
 def __init__(self):self.s=[]
 def add(self,s):self.s.append(s)
 def path(self,d,fill='none',stroke=OUTLINE,w=5,extra=''):
  self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
 def poly(self,ps,fill,stroke=OUTLINE,w=5):self.add(f'<polygon points="{" ".join(pt(p) for p in ps)}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>')
 def line(self,ps,color,w):self.path('M'+' L'.join(pt(p) for p in ps),'none',color,w)
 def ellipse(self,x,y,rx,ry,fill,stroke='none',w=3,extra=''):self.add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>')
 def rect(self,x,y,w,h,fill,stroke='none',sw=3,rx=0):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def ik(a,b,l1,l2,side=1):
 dx,dy=b[0]-a[0],b[1]-a[1];d=max(.001,math.hypot(dx,dy));q=min(d,l1+l2-.001)
 if d>l1+l2+.02:raise ValueError(f'Unreachable IK: {d} > {l1+l2}')
 along=(l1*l1-l2*l2+q*q)/(2*q);height=math.sqrt(max(0,l1*l1-along*along));ux,uy=dx/d,dy/d
 return (a[0]+ux*along-side*uy*height,a[1]+uy*along+side*ux*height)
def limb(a,points,color,width,tag=''):
 if tag:a.add(f'<g id="{tag}" data-joints="{";".join(pt(p) for p in points)}">')
 a.line(points,OUTLINE,width+9);a.line(points,color,width)
 # restrained top-edge cel highlight, preserving continuous joint contour
 a.line([(x-3,y-3) for x,y in points], '#64818c' if color!='#bdc0bf' else '#e4dfd3',2.5)
 if tag:a.add('</g>')


DURATION=8.;FPS=30;GROUND=(1470.,1450.)
def reaction(t):return smooth((t-3.35)/.65) # V6/V7 head module time domain

def ease(t,a,b):return smooth((t-a)/(b-a))
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def lerp(p,q,u):return tuple(mix(x,y,u) for x,y in zip(p,q))
def rot(p,degrees):
 c=math.cos(math.radians(degrees));s=math.sin(math.radians(degrees));return (c*p[0]-s*p[1],s*p[0]+c*p[1])
def keys(t,kk):
 for (a,p),(b,q) in zip(kk,kk[1:]):
  if t<=b:return mix(p,q,ease(t,a,b))
 return kk[-1][1]

def drag(t):return 110*ease(t,.1,1.4)
# Independent world-space foot placements; all holds are exact anchors.
FOOT_PLANS=(
 ((170.,((.15,.42,240.,24.),(.80,1.10,286.,25.),(1.57,1.89,365.,24.),(2.45,2.78,382.,18.),(5.96,6.10,300.,18.))),
  (220.,((.48,.76,282.,26.),(1.14,1.43,330.,23.),(1.94,2.25,420.,22.),(6.12,6.30,345.,18.)))),
 ((578.,((.30,.61,648.,22.),(.96,1.28,690.,24.),(1.54,1.82,637.,18.),(5.90,6.10,740.,19.))),
  (625.,((.66,.94,708.,24.),(1.29,1.51,729.,20.),(6.15,6.35,810.,20.))))
)
def foot(t,actor,leg):
 x,plan=FOOT_PLANS[actor][leg];land=0.
 for start,end,target,lift in plan:
  if t<start:return (x,GROUND[actor]),True,0.
  if t<end:
   u=(t-start)/(end-start);return (mix(x,target,smooth(u)),GROUND[actor]-lift*math.sin(math.pi*u)**1.25),False,u
  x=target;land=end
 return (x,GROUND[actor]),True,0.

def actor_pose(t,i):
 if i==0:
  x=190+drag(t)+95*ease(t,1.57,2.25)-70*ease(t,5.95,6.30)
  hipy=keys(t,[(0,1342),(1.5,1310),(2.25,1310),(2.5,1330),(3.1,1388),(4.35,1311),(5.55,1313),(5.9,1311),(6.2,1305),(8,1305)])
  angle=keys(t,[(0,-10),(1.5,-10),(1.86,20),(2.25,20),(2.5,5),(3.1,25),(4.35,14),(5.45,30),(5.8,15),(6.2,-6),(8,-6)])
 else:
  x=600+drag(t)-35*ease(t,1.45,1.85)+100*ease(t,5.95,6.35)
  hipy=keys(t,[(0,1322),(1.15,1322),(1.55,1390),(2.5,1390),(3.1,1390),(4.35,1291),(4.85,1280),(5.5,1280),(5.9,1291),(8,1291)])
  angle=keys(t,[(0,-10),(1.15,-10),(1.55,-45),(2.5,-45),(3.1,-65),(3.35,-65),(4.35,-12),(4.85,0),(5.55,0),(5.9,-12),(8,-12)])
 # Small support-weight shift follows the planted foot. No locomotion clock.
 ff=[foot(t,i,j) for j in (0,1)];planted=[p[0] for p,on,u in ff if on]
 dx=3*math.tanh((sum(planted)/len(planted)-x)/25)
 hip=(x+dx,hipy);shoulder=add(hip,rot((0,-125),angle));side=rot((1,0),angle)
 return {'hip':hip,'shoulder':shoulder,'angle':angle,'side':side,'feet':ff}

def trunk_angle(t):return 102*ease(t,1.82,2.42)
def lid_point(t,u=.88):
 th=math.radians(trunk_angle(t));return (mix(562,562,u),1005+155*u*math.cos(th)-190*u*math.sin(th))

def victim_pose(t):
 # Hierarchical torso rotation, delayed pelvis and passive articulated legs.
 lift=ease(t,3.1,4.35);tuck=ease(t,4.48,4.98);load=ease(t,4.92,5.72)
 angle=-82*ease(t,3.,4.3)-6*tuck-8*load
 cx=375+drag(max(0,t-.10))+15*ease(t,1.5,2.5)
 sy=1255-155*lift-20*tuck+12*load
 S=(cx,sy)
 # Pelvis follows the shoulder frame 0.10 seconds later; proportional torso length.
 pang=-82*ease(t-.10,3.,4.3)-6*ease(t-.08,4.48,4.98)-8*ease(t-.08,4.92,5.72)
 P=add(S,rot((-30,138),pang))
 sh=[add(S,rot(p,angle)) for p in [(-39,5),(35,7)]]
 elbows=[];hands=[]
 for j,p in enumerate([(-45,63),(49,61)]):
  # Gravity dominates upper-arm fall as torso approaches horizontal.
  v=rot(p,angle*.20);el=add(sh[j],v);elbows.append(el)
  fore=rot(((-6 if j==0 else 6),42),-80*load if j==1 else -30*load)
  hands.append(add(el,fore))
 heels=[];knees=[];hips=[]
 for j in (0,1):
  h=add(P,rot(((-18 if j==0 else 18),0),pang));hips.append(h)
  dragshoe=(cx-111+j*30,1480+j*8)
  hanging=add(P,(59+j*18,125+j*7))
  ankle=lerp(dragshoe,hanging,lift)
  ankle=(ankle[0],min(dragshoe[1],ankle[1]))
  # Supporting knee lift folds the lower leg over the sill; no walking cycle.
  folded=add(P,(104+j*12-20*load,18+j*11+12*load))
  ankle=lerp(ankle,folded,tuck)
  delta=sub(ankle,h);length=math.hypot(*delta)
  if length>156.5:ankle=add(h,(delta[0]*156.5/length,delta[1]*156.5/length))
  heels.append(ankle);knees.append(ik(h,ankle,77,80,-1))
 # Depth projection increases only after the shoes clear the near sill.
 # The body remains visibly inside the open cavity, never alpha-fades away.
 z=load;scale=1-.12*z
 def project(p):return (562+(p[0]-562)*scale,1100+(p[1]-1100)*scale-12*z)
 S,P=project(S),project(P);sh=[project(p) for p in sh];elbows=[project(p) for p in elbows];hands=[project(p) for p in hands]
 hips=[project(p) for p in hips];knees=[project(p) for p in knees];heels=[project(p) for p in heels]
 grips=[lerp(sh[j],elbows[j],.53) for j in (0,1)]
 back=project(add((cx,sy),rot((-32,8),angle)))
 waist=project(add((cx,sy),rot((35,126),pang)))
 neck=project(add((cx,sy),rot((0,-61),angle)))
 return {'S':S,'P':P,'shoulders':sh,'elbows':elbows,'hands':hands,'hips':hips,'knees':knees,'feet':heels,'grips':grips,'back':back,'waist':waist,'angle':angle,'head_angle':angle+22-9*math.sin(math.pi*ease(t,3.1,4.45)),'neck':neck,'scale':scale,'depth':load,'lift':lift,'tuck':tuck}

def hand_targets(t,poses,v):
 # Named, timed handoffs: C2 receives waist before C1 releases upper arm.
 def free(i,j):
  p=poses[i];return add(p['hip'],rot(((-39 if j else 42),-12),p['angle']))
 c1a=v['grips'][0]
 if 1.60<t<2.50:
  if t<1.82:c1a=lerp(v['grips'][0],lid_point(t),ease(t,1.60,1.82))
  elif t<1.94:c1a=lid_point(t)
  else:c1a=lerp(lid_point(1.94),v['grips'][0],ease(t,1.94,2.50))
 c1b=lerp(free(0,1),v['back'],ease(t,2.42,2.88))
 c2a=lerp(v['grips'][1],v['waist'],ease(t,2.50,2.86))
 c2b=lerp(free(1,1),v['waist'],ease(t,1.25,1.58))
 c2b=lerp(c2b,v['knees'][1],ease(t,2.67,3.05))
 # Release after the interior floor has received the whole body.
 c1a=lerp(c1a,free(0,0),ease(t,5.72,5.96));c1b=lerp(c1b,free(0,1),ease(t,5.76,6.02))
 c2a=lerp(c2a,free(1,0),ease(t,5.80,6.08));c2b=lerp(c2b,free(1,1),ease(t,5.82,6.12))
 return [[c1a,c1b],[c2a,c2b]]
def draw_head_legacy(a,hx,hy,t,who):
  sx=hx-2;sy=hy+72
  hx=sx+2;hy=sy-72;turn=reaction(t) if who==1 else 0
  narrow=smooth((t-3.9)/.55) if who==1 else 0
  a.add(f'<g id="head-{who}" data-turn="{turn}" data-narrow="{narrow}" transform="translate({-8*turn},0) rotate({-20+20*turn if who==1 else 5} {hx} {hy})">')
  a.ellipse(hx,hy,61,65,'#06121d',OUTLINE,6)
  # pale eye opening becomes broader as criminal 01 looks at camera
  eyeW=mix(34,49,turn);eyeX=hx+mix(21,-2,turn)
  a.path(f'M{eyeX-eyeW},{hy-4} Q{eyeX},{hy-17} {eyeX+eyeW},{hy-6} L{eyeX+eyeW-5},{hy+16} Q{eyeX},{hy+30} {eyeX-eyeW+4},{hy+11}Z','url(#face)',OUTLINE,3)
  for ex in [mix(hx+16,hx-20,turn),mix(hx+42,hx+20,turn)]:
   a.ellipse(ex,hy+5,4,10,'#03090f')
  if narrow>0:
   a.path(f'M{eyeX-eyeW},{hy-7} Q{eyeX-20},{hy-13} {eyeX},{hy-6+12*narrow} Q{eyeX+20},{hy-13} {eyeX+eyeW},{hy-7} L{eyeX+eyeW},{hy-19} L{eyeX-eyeW},{hy-21}Z','#0b1721',OUTLINE,2)
  a.path(f'M{hx-53},{hy+15} Q{hx+7},{hy+33} {hx+54},{hy+16} Q{hx+46},{hy+65} {hx},{hy+66} Q{hx-46},{hy+54} {hx-53},{hy+15}Z','#0b1721',OUTLINE,4)
  a.path(f'M{hx-33},{hy+37} Q{hx},{hy+49} {hx+28},{hy+38}','none','#263946',2)
  a.path(f'M{hx-60},{hy-14} Q{hx-58},{hy-78} {hx-1},{hy-79} Q{hx+53},{hy-75} {hx+58},{hy-15}Z','#142532','#6c8994',2)
  if who==1:
   a.path(f'M{hx-66},{hy-17} Q{hx+5},{hy-34} {hx+70},{hy-12} L{hx+76},{hy+1} Q{hx+21},{hy-3} {hx-64},{hy+2}Z','#091923',OUTLINE,5)
   a.path(f'M{hx+mix(25,0,turn)},{hy-73} Q{hx+mix(42,1,turn)},{hy-45} {hx+mix(35,0,turn)},{hy-26}','none','#354956',2)
   a.path(f'M{hx-62},{hy-22} Q{hx-61},{hy-58} {hx-37},{hy-68}','none','#ecab54',3)
  else:
   a.path(f'M{hx-61},{hy-23} Q{hx},{hy-40} {hx+60},{hy-20} L{hx+61},{hy-4} Q{hx},{hy-18} {hx-61},{hy-5}Z','#102331',OUTLINE,4)
   for q in range(-45,50,13):a.line([(hx+q,hy-29),(hx+q+1,hy-10)],'#304756',1.5)
  a.add('</g>')

def hull(points):
 pts=sorted(set((round(x,5),round(y,5)) for x,y in points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[];upper=[]
 for q in pts:
  while len(lower)>1 and cross(lower[-2],lower[-1],q)<=0:lower.pop()
  lower.append(q)
 for q in reversed(pts):
  while len(upper)>1 and cross(upper[-2],upper[-1],q)<=0:upper.pop()
  upper.append(q)
 return lower[:-1]+upper[:-1]

def curved_outline(a,points,fill,stroke=OUTLINE,width=4):
 n=len(points);d='M'+pt(points[0])
 for j in range(n):
  p0,p1,p2,p3=points[(j-1)%n],points[j],points[(j+1)%n],points[(j+2)%n]
  c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6)
  c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
  d+=' C'+pt(c1)+' '+pt(c2)+' '+pt(p2)
 a.path(d+'Z',fill,stroke,width)

def draw_head(a,hx,hy,t,who,hide_eyes=False):
 if who==2:return draw_head_legacy(a,hx,hy,t,who)
 turn=reaction(t);theta=math.radians(72*(1-turn));narrow=smooth((t-4)/.5)
 c,ss=math.cos(theta),math.sin(theta)
 def project(x,y,z):
  depth=-x*ss+z*c
  return hx+x*c+z*ss,hy+y+.16*depth
 def surface(y,lon,mask=False):
  lat=math.asin(max(-.9999,min(.9999,y/65)));q=math.cos(lat);l=math.radians(lon)
  z=54*q*math.cos(l)
  if mask:z+=8*q*max(0,math.cos(l))
  return project(61*q*math.sin(l),y,z)
 def visible_span(lo,hi):
  angle=math.degrees(theta)
  return max(lo,-angle-89.8),min(hi,-angle+89.8)
 def patch(lo,hi,top,bottom,mask=False):
  lo,hi=visible_span(lo,hi)
  if lo>=hi:return []
  ls=[mix(lo,hi,i/32) for i in range(33)]
  return ([surface(top(l),l,mask) for l in ls]
   +[surface(mix(top(hi),bottom(hi),j/16),hi,mask) for j in range(1,16)]
   +[surface(bottom(l),l,mask) for l in reversed(ls)]
   +[surface(mix(bottom(lo),top(lo),j/16),lo,mask) for j in range(1,16)])
 bill3=[(-68,-20,12),(-75,-20,45),(-55,-20,99),(0,-20,114),(55,-20,99),(75,-20,45),(68,-20,12),(0,-20,-3)]
 bill=[project(*q) for q in bill3]
 rx=math.sqrt((61*c)**2+(54*ss)**2)
 chin=surface(61,0,True)[0]-hx
 a.add(f'<g id="head-1" data-turn="{turn}" data-yaw="{math.degrees(theta)}" data-head-rx="{rx}" data-bill="{max(x for x,y in bill)-hx}" data-mask-chin="{chin}" data-narrow="{narrow}">')
 # Parent neck turns under the jaw; the chest/shoulder frame stays planted.
 neck=[project(-19,54,6),project(19,54,6),project(18,81,3),project(-20,78,3)]
 a.poly(neck,'#0b1721',OUTLINE,3)
 a.line([project(9,59,18),project(8,78,15)],'#34505b',2)
 a.ellipse(hx,hy,rx,65,'#06121d',OUTLINE,6)
 mask=patch(-180,180,lambda l:14,lambda l:64,True)
 a.poly(mask,'#0b1721',OUTLINE,3.5)
 # Curved eye opening and irises project on the head surface, not a sliding 2D face.
 top=lambda l:-8+8*narrow*(1-abs(l)/54)
 bottom=lambda l:17-5*narrow
 eye=patch(-54,54,top,bottom)
 if not hide_eyes:
  a.poly(eye,'url(#face)',OUTLINE,2)
  d='M'+' L'.join(pt(q) for q in eye)+'Z'
  a.add(f'<defs><clipPath id="eye-window-1"><path d="{d}"/></clipPath></defs><g clip-path="url(#eye-window-1)">')
  for center in [-20,20]:
   if math.cos(math.radians(center)+theta)<.015:continue
   pupil=[surface(4+(9-3*narrow)*math.cos(j*math.pi/12),center+4*math.sin(j*math.pi/12)) for j in range(24)]
   a.poly(pupil,'#03090f','none',0)
  a.poly(patch(-7,7,lambda l:-14,lambda l:25,True),'#0b1721','none',0)
  if narrow>0:
   for lo,hi in [(-46,-9),(9,46)]:
    points=[surface(-7+7*narrow*(1-abs(mix(lo,hi,j/10))/46),mix(lo,hi,j/10),True) for j in range(11)]
    a.line(points,'#030b12',3)
  a.add('</g>')
 # Small cloth fold on the curved mask, not a mouth or smile.
 lo,hi=visible_span(-40,40)
 fold=[surface(38+3*math.cos(math.radians(l*2)),l,True) for l in [mix(lo,hi,j/20) for j in range(21)]]
 a.line(fold,'#263946',2)
 # Cap dome silhouette is the hull of a rotated ellipsoidal shell.
 dome=[]
 for lat in range(-90,1,6):
  q=math.cos(math.radians(lat));yy=-15+65*math.sin(math.radians(lat))
  for lon in range(-180,180,6):
   l=math.radians(lon);dome.append(project(63*q*math.sin(l),yy,55*q*math.cos(l)-10))
 curved_outline(a,hull(dome),'#142532','#6c8994',2)
 lo,hi=visible_span(-180,180)
 ls=[mix(lo,hi,j/40) for j in range(41)]
 band=[project(63*math.sin(math.radians(l)),-18,55*math.cos(math.radians(l))-10) for l in ls]
 band+=[project(63*math.sin(math.radians(l)),-4,55*math.cos(math.radians(l))-10) for l in reversed(ls)]
 a.poly(band,'#102331',OUTLINE,3)
 # Cap panel seams stay fixed in 3D while the whole cap turns.
 for lon in [-32,32]:
  if math.cos(math.radians(lon)+theta)<0:continue
  seam=[]
  for lat in range(-78,-9,5):
   q=math.cos(math.radians(lat));l=math.radians(lon)
   seam.append(project(63*q*math.sin(l),-15+65*math.sin(math.radians(lat)),55*q*math.cos(l)-10))
  a.line(seam,'#354956',1.6)
 # The same rigid visor changes direction and foreshortening through yaw.
 curved_outline(a,[(x,y+4) for x,y in bill],'#030b12',OUTLINE,4)
 curved_outline(a,bill,'#0d1e29',OUTLINE,4)
 a.line(bill[:4],'#304956',1.2)
 # Consistent amber rim on the lit contour; no photorealistic lighting.
 rim=[project(-63*math.cos(math.radians(lat)),-15+65*math.sin(math.radians(lat)),-10) for lat in range(-62,-12,6)]
 a.line(rim,'#d29b50',2.5)
 a.add('</g>')


def car_back(a,t):
 a.add('<g id="black-sedan" data-geometry="fixed-rear-three-quarter">')
 a.ellipse(575,1430,390,43,'#02090f')
 for x in [234,882]:
  a.ellipse(x,1349,42,94,'#02070d','#344650',5);a.ellipse(x,1349,23,59,'#14232d','#060e16',4)
  for ang in range(0,360,60):a.line([(x,1349),(x+19*math.sin(math.radians(ang)),1349+49*math.cos(math.radians(ang)))],'#3b4d57',3)
 a.path('M219 1162 L278 908 Q326 802 457 783 L680 783 Q810 800 853 908 L918 1162 L918 1359 Q586 1445 206 1370Z','url(#metal)',OUTLINE,8)
 a.path('M306 909 Q350 827 459 820 L678 820 Q777 832 821 911 L840 986 L286 986Z','#07151f','#445e6b',5)
 a.path('M459 825 L465 984 M681 825 L686 984','none','#243d4b',4)
 a.path('M317 914 Q480 849 641 864','none','#37525f',4)
 a.path('M846 1010 L890 1154 L902 1328','none','#3e5360',3)
 a.add('</g>')
 # The same rigid rim/cavity is exposed as the lid rises.
 a.add('<g id="trunk-cavity">')
 a.poly([(300,1005),(825,1005),(875,1160),(245,1160)],'#02070c','#526974',7)
 a.poly([(320,1020),(805,1020),(848,1145),(272,1145)],'#09141c','#182d37',3)
 a.poly([(320,1020),(805,1020),(794,1083),(336,1083)],'#030a11','none',0)
 for x in [345,780]:a.line([(x,1043),(x+(-15 if x<500 else 15),1128)],'#172a34',4)
 a.line([(336,1110),(792,1110)],'#243944',3)
 a.add('</g>')

def car_lid(a,t):
 th=math.radians(trunk_angle(t));cs,sn=math.cos(th),math.sin(th)
 def p(x,u):return (562+(x-562)*(1+.20*u),1005+155*u*cs-190*u*sn)
 a.add(f'<g id="trunk-lid" data-angle="{trunk_angle(t)}" data-hinge="300,1005;825,1005">')
 # Struts attach at invariant hinge brackets and the same rotating lid points.
 if trunk_angle(t)>2:
  for x in [320,805]:a.line([(x,1085),p(x,.80)],'#627581',6)
 poly=[p(300,0),p(825,0),p(825,1),p(300,1)]
 a.poly(poly,'#172933' if trunk_angle(t)>45 else 'url(#metal)','#52636d',5)
 inner=[p(330,.15),p(795,.15),p(795,.88),p(330,.88)]
 a.poly(inner,'#0a1721','#2f4653',3)
 if trunk_angle(t)>20:
  a.line([p(365,.18),p(385,.80),p(735,.80),p(760,.18)],'#2b414d',3)
  a.line([p(340,.52),p(785,.52)],'#263c48',5)
 latch=p(562,.88);a.rect(latch[0]-18,latch[1]-5,36,10,'#53656b',OUTLINE,2,3)
 a.line([p(300,0),p(825,0)],'#8b9b9c',3)
 a.add('</g>')

def car_front(a):
 # Near sill/bumper are foreground holdouts over the portion already in the cavity.
 a.add('<g id="trunk-near-occluder">')
 a.path('M245 1160 Q562 1178 875 1160 L918 1200 L918 1359 Q586 1445 206 1370 L211 1207Z','url(#metal)',OUTLINE,7)
 a.path('M245 1160 Q562 1178 875 1160','none','#6d858e',8)
 a.path('M226 1222 L352 1236 L371 1260 L231 1244Z','#e34c48','#60242a',4)
 a.path('M765 1235 L896 1215 L891 1240 L766 1258Z','#ed594d','#60242a',4)
 a.line([(241,1234),(349,1247)],'#ffad86',3);a.line([(777,1245),(883,1230)],'#ffad86',3)
 a.poly([(517,1280),(641,1278),(644,1315),(519,1319)],'#929e9c','#08121a',4)
 a.line([(545,1296),(616,1293)],'#32434a',4)
 a.path('M227 1351 Q570 1412 903 1340','none','#405965',5)
 a.path('M245 1384 l-4 19 M869 1384 l-4 17','none','#050c13',16)
 a.add('</g>')

def shoe(a,f,pitch=0.,color='#172a35',tag=''):
 x,y=f;a.add(f'<g transform="rotate({pitch} {x} {y})">')
 a.path(f'M{x-18},{y-10} Q{x+8},{y-20} {x+33},{y-5} L{x+34},{y+7} L{x-20},{y+7}Z',color,OUTLINE,5,f'id="{tag}" data-x="{x}" data-y="{y}"')
 a.line([(x-14,y+3),(x+28,y+3)],'#8d9c9e',2.5);a.add('</g>')

def actor_body(a,t,i,p,hide_eyes=False):
 hip=p['hip'];sx,sy=p['shoulder'];side=p['side'];who=i+1
 a.add(f'<g id="actor-{who}" data-hip="{pt(hip)}" data-shoulder="{pt((sx,sy))}">')
 for j,(f,on,u) in enumerate(p['feet']):
  h=add(hip,rot(((-15 if j==0 else 17),0),p['angle']*.10));ank=(f[0],f[1]-11);k=ik(h,ank,85,85,1 if i==0 else -1)
  limb(a,[h,k,ank],'#172833' if j==0 else '#243945',28,f'actor-{who}-leg-{j}')
  a.add(f'<g id="foot-state-{who}-{j}" data-stance="{int(on)}" data-world="{pt(f)}">')
  shoe(a,f,-9*math.sin(math.pi*u) if not on else 0.,tag=f'actor-{who}-shoe-{j}');a.add('</g>')
 # V7 hoodie contours and cel palette, now deformed around the torso hierarchy.
 a.path(f'M{sx-44},{sy-8} Q{sx-61},{sy+15} {hip[0]-45},{hip[1]+15} Q{hip[0]},{hip[1]+30} {hip[0]+48},{hip[1]+12} L{sx+45},{sy+7} Q{sx+27},{sy-19} {sx-44},{sy-8}Z','url(#cloth)',OUTLINE,7)
 a.path(f'M{sx-32},{sy+18} L{hip[0]-30},{hip[1]+9} M{sx+21},{sy+27} L{hip[0]+24},{hip[1]-4}','none','#3c4d56',2)
 a.path(f'M{sx-3},{sy+20} L{hip[0]+1},{hip[1]+17} M{hip[0]-25},{hip[1]-26} Q{hip[0]},{hip[1]-16} {hip[0]+25},{hip[1]-27}','none','#07121c',4)
 a.path(f'M{sx-37},{sy-13} Q{sx},{sy+42} {sx+36},{sy-12} L{sx+21},{sy-37} L{sx-25},{sy-35}Z','#0b1722',OUTLINE,5)
 a.line([(sx-15,sy+12),(sx-17,sy+51)],'#617079',2);a.line([(sx+14,sy+12),(sx+16,sy+47)],'#617079',2)
 a.path(f'M{sx-43},{sy+7} Q{sx-53},{sy+35} {hip[0]-44},{hip[1]-2}','none','#da9a4b',3)
 ht=3.2+(t-6.4)*1.125 if t>=6.4 else 0.
 # The head geometry module is untouched. A small shoulder/neck attention change precedes the cut.
 draw_head(a,sx+2,sy-72,ht,who,hide_eyes);a.add('</g>')

def victim_draw(a,t,v):
 P=v['P'];S=v['S'];sl,sr=v['shoulders'];sc=v['scale']
 a.add(f'<g id="victim" data-pelvis="{pt(P)}" data-shoulder="{pt(S)}" data-depth="{v["depth"]}" data-angle="{v["angle"]}">')
 for j in (0,1):
  limb(a,[v['hips'][j],v['knees'][j],v['feet'][j]],'#213b47',26*sc,f'victim-leg-{j}')
  shoe(a,v['feet'][j],-12*v['lift']-43*v['tuck'],color='#08151e',tag=f'victim-shoe-{j}')
 # Shirt local width rotates with the torso; the lower edge follows lagging pelvis.
 left=add(P,rot((-39*sc,2),v['angle']));right=add(P,rot((39*sc,0),v['angle']));mid=lerp(S,P,.48)
 a.path(f'M{pt(add(sl,rot((0,-14*sc),v["angle"])))} Q{pt(add(mid,rot((-46*sc,0),v["angle"])))} {pt(left)} Q{pt(add(P,rot((0,23*sc),v["angle"])))} {pt(right)} Q{pt(add(mid,rot((43*sc,0),v["angle"])))} {pt(add(sr,rot((0,-14*sc),v["angle"])))}Z','#b8bdbb',OUTLINE,6)
 a.line([sr,add(mid,rot((25*sc,0),v['angle'])),right],'#74848b',15*sc)
 # Existing blood mark stays attached to the chest, not the screen.
 a.add(f'<g transform="translate({S[0]} {S[1]}) rotate({v["angle"]}) scale({sc})">')
 a.path('M-3 30 l-13 25 8 11 -4 27 11 -18 3 -17 10 -4 -7 -22Z','#8d3037','none',0)
 a.line([(-25,115),(5,101),(25,114)],'#86979c',2);a.add('</g>')
 for j in (0,1):
  limb(a,[v['shoulders'][j],v['elbows'][j],v['hands'][j]],'#bdc0bf',23*sc,f'victim-arm-{j}');a.ellipse(*v['hands'][j],12*sc,16*sc,'#c1c6c3',OUTLINE,3)
 hx,hy=v['neck'];a.add(f'<g id="victim-head" transform="translate({hx} {hy}) rotate({v["head_angle"]}) scale({sc})">')
 a.ellipse(0,0,51,58,'url(#face)',OUTLINE,5)
 a.path('M-51 -10 Q-57 -60 -7 -63 Q48 -64 52 -11 L48 6 Q-4 -9 -51 -10Z','#111f2a',OUTLINE,5)
 a.line([(-35,-37),(39,-13)],'#b78343',2)
 a.path('M-27 15 l14 4 M10 19 l12 -1 M-8 38 q10 -4 16 1','none','#18222b',3)
 a.path('M30 29 l-7 9','none','#9e4345',3);a.add('</g></g>')

def actor_arms(a,t,poses,v,targets):
 for i in [1,0]:
  p=poses[i];sx,sy=p['shoulder'];side=p['side']
  for j in [1,0]:
   # Inner supporting arm and outer receiving/bracing arm, both articulated.
   sign=(1 if i==0 else -1)*(1 if j==0 else -1)
   shoulder=add((sx,sy),(side[0]*35*sign,side[1]*35*sign+12));hand=targets[i][j]
   el=ik(shoulder,hand,90,87,1 if i==0 else -1)
   limb(a,[shoulder,el,hand],'#203440' if j==0 else '#172833',27,f'actor-{i+1}-arm-{j}')
   angle=math.degrees(math.atan2(hand[1]-el[1],hand[0]-el[0]))-90
   a.add(f'<g id="grip-{i+1}-{j}" data-center="{pt(hand)}" transform="rotate({angle} {hand[0]} {hand[1]})">')
   a.ellipse(*hand,15,17,'#0a1720','#59717a',3)
   a.line([(hand[0]-6,hand[1]-6),(hand[0]-5,hand[1]+5)],'#70878d',1.5);a.line([(hand[0]+1,hand[1]-7),(hand[0]+2,hand[1]+4)],'#70878d',1.5);a.add('</g>')

def scene(t,hide_eyes=False):
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
 poses=[actor_pose(t,i) for i in (0,1)];v=victim_pose(t);targets=hand_targets(t,poses,v)
 cam=16*ease(t,0,1.5)
 if t<6.4:scale=1.08;tx=-42;ty=-240
 else:
  scale=5.1+.18*ease(t,6.4,8.);sx,sy=poses[0]['shoulder'];ht=3.2+(t-6.4)*1.125
  tx=mix(430,520,reaction(ht))-scale*(sx+2-cam);ty=860-scale*(sy-72)
 a.add(f'<g id="cinematic-framing" data-shot="{1 if t<6.4 else 2}" transform="translate({tx},{ty}) scale({scale})"><g transform="translate({-cam},0)">')
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

 car_back(a,t)
 car_lid(a,t)
 # Inside/outside split traverses the body head-first. Both use identical pose geometry.
 # No opacity fade; the actual near sill masks only parts that crossed the entry plane.
 entry=mix(320,850,ease(t,4.90,5.72))
 a.add(f'<defs><clipPath id="in-entry"><rect x="0" y="0" width="{entry}" height="1920"/></clipPath><clipPath id="out-entry"><rect x="{entry}" y="0" width="{1300-entry}" height="1920"/></clipPath><clipPath id="cavity-clip"><polygon points="300,1005 825,1005 875,1160 245,1160"/></clipPath></defs>')
 if t>=4.90:
  a.add('<g clip-path="url(#in-entry)"><g clip-path="url(#cavity-clip)">');victim_draw(a,t,v);a.add('</g></g>')
 car_front(a)
 if t<4.5:
  a.ellipse(v['P'][0],1490,90-30*v['lift'],12-4*v['lift'],'#020a10',extra=f'opacity="{.7-.35*v["lift"]}"')
 for i in [1,0]:
  for p,on,u in poses[i]['feet']:a.ellipse(p[0],GROUND[i]+12,37,9,'#020a10')
  actor_body(a,t,i,poses[i],hide_eyes)
 if t<4.9:victim_draw(a,t,v)
 else:
  a.add('<g clip-path="url(#out-entry)">');victim_draw(a,t,v);a.add('</g>')
 # Forearms reach over the lip; gloves preserve the same contact endpoints as the victim.
 actor_arms(a,t,poses,v,targets)
 # Wet scrape trails disappear only after physical lift-off.
 if .1<t<3.2:
  for f in v['feet']:a.line([(f[0]-32,f[1]+12),(f[0]-6,f[1]+12)],'#627d87',1.5)
 for i in (0,1):
  for f,on,u in poses[i]['feet']:
   if on:a.ellipse(f[0],f[1]+9,28,4,'none','#5c7a84',1,extra='opacity=".3"')
 # Three environmental rain layers; projected close-up rain remains readable.
 if t<6.4:
  for layer,count in [(0,180),(1,160),(2,80)]:
   a.add(f'<g opacity="{[.17,.26,.36][layer]}">')
   for j in range(count):
    x=rng.uniform(-100,1200);y=(rng.uniform(-100,2000)+t*[520,760,1120][layer])%2080-80
    a.line([(x,y),(x-4-layer*2,y+18+12*layer)],'#80a6b5',[1,1.4,2][layer])
   a.add('</g>')
 a.add('</g></g>')
 if t>=6.4:
  for j in range(110):
   x=rng.uniform(0,1180);y=(rng.uniform(-100,1920)+t*1050)%2100-100
   a.path(f'M{x},{y} l-5 43','none','#6d96a7',1.7,'opacity=".3"')
 a.rect(0,0,1080,1920,'url(#vignette)');a.add('</svg>');return ''.join(a.s)
class Raster:
 def __init__(self,w,h):
  self.w=w;self.h=h;self.r=C.CDLL(ctypes.util.find_library('rsvg-2'));self.c=C.CDLL(ctypes.util.find_library('cairo'));self.g=C.CDLL(ctypes.util.find_library('gobject-2.0'))
  self.r.rsvg_handle_new_from_data.argtypes=[C.c_char_p,C.c_size_t,C.c_void_p];self.r.rsvg_handle_new_from_data.restype=C.c_void_p
  self.r.rsvg_handle_render_cairo.argtypes=[C.c_void_p,C.c_void_p];self.r.rsvg_handle_render_cairo.restype=C.c_int
  for name,args,ret in [('cairo_image_surface_create',[C.c_int,C.c_int,C.c_int],C.c_void_p),('cairo_create',[C.c_void_p],C.c_void_p),('cairo_scale',[C.c_void_p,C.c_double,C.c_double],None),('cairo_image_surface_get_data',[C.c_void_p],C.c_void_p),('cairo_surface_flush',[C.c_void_p],None),('cairo_destroy',[C.c_void_p],None),('cairo_surface_destroy',[C.c_void_p],None)]:
   f=getattr(self.c,name);f.argtypes=args;f.restype=ret
  self.g.g_object_unref.argtypes=[C.c_void_p]
 def render(self,svg):
  b=svg.encode();handle=self.r.rsvg_handle_new_from_data(b,len(b),None)
  surf=self.c.cairo_image_surface_create(0,self.w,self.h);ctx=self.c.cairo_create(surf);self.c.cairo_scale(ctx,self.w/1080,self.h/1920)
  if not self.r.rsvg_handle_render_cairo(handle,ctx):raise RuntimeError('SVG render failed')
  self.c.cairo_surface_flush(surf);buf=C.string_at(self.c.cairo_image_surface_get_data(surf),self.w*self.h*4)
  im=Image.frombytes('RGBA',(self.w,self.h),buf,'raw','BGRA').convert('RGB')
  self.c.cairo_destroy(ctx);self.c.cairo_surface_destroy(surf);self.g.g_object_unref(handle);return im


def audio():
 sr=48000;n=sr*8;rng=np.random.default_rng(117);ts=np.arange(n)/sr;noise=rng.standard_normal(n)
 track=(noise-np.roll(noise,1))*.03+.018*np.sin(2*np.pi*43*ts)
 events=[]
 for i in (0,1):
  for j in (0,1):
   for start,end,target,lift in FOOT_PLANS[i][j][1]:
    nn=int(.18*sr);tt=np.arange(nn)/sr;pos=round(end*sr)
    track[pos:pos+nn]+=.18*np.sin(2*np.pi*(80*tt-50*tt*tt))*np.exp(-tt*28)+rng.standard_normal(nn)*.06*np.exp(-tt*40)
    events.append({'time':end,'event':'wet foot plant','actor':i+1,'leg':j})
 for when,kind in [(1.82,'trunk latch'),(2.42,'lid stop'),(4.95,'fabric over sill'),(5.72,'body settles'),(6.4,'reaction cut')]:
  pos=round(when*sr);nn=int(.32*sr);tt=np.arange(nn)/sr
  track[pos:pos+nn]+=.06*np.sin(2*np.pi*(62*tt-25*tt*tt))*np.exp(-tt*18)+rng.standard_normal(nn)*.04*np.exp(-tt*32)
  events.append({'time':when,'event':kind})
 track+=np.convolve(rng.standard_normal(n),np.ones(9)/9,mode='same')*.032*((ts>.1)&(ts<3.2))
 track*=np.minimum(1,ts/.08)*np.minimum(1,(8-ts)/.15)
 stereo=np.column_stack((track,np.roll(track,97)*.97));pcm=(np.clip(stereo,-.95,.95)*32767).astype('<i2')
 dest=ROOT/'assets/original_ambience.wav'
 with wave.open(str(dest),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
 (ROOT/'assets/sound-events.json').write_text(json.dumps(events,indent=2));return dest
def main():
 p=argparse.ArgumentParser();p.add_argument('--scale',type=float,default=.5);p.add_argument('--fps',type=int,default=30);p.add_argument('--out',default='previews/V8_preview_01.mp4');p.add_argument('--stills',action='store_true');p.add_argument('--hide-eyes',action='store_true');args=p.parse_args()
 w=round(1080*args.scale/2)*2;h=round(1920*args.scale/2)*2;r=Raster(w,h)
 out=ROOT/args.out
 if out.exists():raise SystemExit('Refusing to overwrite '+str(out))
 out.parent.mkdir(parents=True,exist_ok=True)
 (ROOT/'assets').mkdir(parents=True,exist_ok=True)
 (ROOT/'previews').mkdir(parents=True,exist_ok=True)
 wav=audio()
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(args.fps),'-i','pipe:0','-i',str(wav),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','8','-movflags','+faststart',str(out)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 samples=[]
 for i in range(8*args.fps):
  t=i/args.fps;svg=scene(t,hide_eyes=args.hide_eyes);im=r.render(svg);proc.stdin.write(im.tobytes())
  if args.stills and i%max(1,args.fps//4)==0:
   thumb=im.resize((216,384));samples.append((t,thumb))
  if i in [0,args.fps*2,args.fps*4,8*args.fps-1]:
   im.save(ROOT/'previews'/f'frame_{i:03d}_{w}.png')
   (ROOT/'assets'/f'scene_{t:.3f}.svg').write_text(svg)
  if i%args.fps==0:print(f'{i}/{8*args.fps}',flush=True)
 proc.stdin.close()
 if proc.wait():raise RuntimeError('ffmpeg failed')
 if samples:
  cols=5;sheet=Image.new('RGB',(cols*216,math.ceil(len(samples)/cols)*410),'#07121d');draw=ImageDraw.Draw(sheet)
  for j,(t,im) in enumerate(samples):
   x=j%cols*216;y=j//cols*410;sheet.paste(im,(x,y));draw.text((x+8,y+387),f'{t:.2f}s',fill='white')
  sheet.save(ROOT/'previews'/f'contact_{w}.jpg',quality=90)
 print(out)
if __name__=='__main__':main()
