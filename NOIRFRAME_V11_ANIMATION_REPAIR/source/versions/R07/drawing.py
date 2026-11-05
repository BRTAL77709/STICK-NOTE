"""Common approved illustrated witness/ink/palette across all new shots; no footage input."""
from svg import Art,Raster
from rig import *
from approved_head import head
INK='#030b12'
def begin():
 a=Art();a.add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">');a.add('''<defs><linearGradient id="face"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#a6b7bd"/></linearGradient><linearGradient id="cloth" x2="1" y2=".3"><stop stop-color="#294451"/><stop offset=".6" stop-color="#172c39"/><stop offset="1" stop-color="#0e1d28"/></linearGradient><linearGradient id="wall" x2="0" y2="1"><stop stop-color="#102633"/><stop offset="1" stop-color="#1e3c49"/></linearGradient><radialGradient id="amber"><stop stop-color="#f5b563" stop-opacity=".30"/><stop offset="1" stop-color="#efab4f" stop-opacity="0"/></radialGradient><linearGradient id="glass" x2="1" y2="1"><stop stop-color="#234754"/><stop offset="1" stop-color="#071521"/></linearGradient></defs>''');return a

def poly(a,P,pts,fill,stroke=INK,w=5):a.poly([P(p) for p in pts],fill,stroke,w)
def line(a,P,pts,col,w):a.line([P(p) for p in pts],col,w)
def limb(a,P,pts,col,S,width=.10):
 pp=[P(p) for p in pts];a.line(pp,INK,S*width+9);a.line(pp,col,S*width);a.line([(x-3,y-2) for x,y in pp],'#54717b',2.0)
def hand(a,P,wrist,S,target=None,pinch=False):
 p=np.array(P(wrist));r=S*.047
 a.ellipse(*p,r*.8,r,'#cdd7d3',INK,3)
 if target is not None:
  q=np.array(P(target));v=q-p;d=np.linalg.norm(v)
  if d>1:
   n=np.array([-v[1],v[0]])/d
   for side in [-1,1]:
    s=p+n*r*.65*side;c=(p+q)*.5+n*r*.6*side;a.path(f'M{s[0]} {s[1]} Q{c[0]} {c[1]} {q[0]+n[0]*1.5*side} {q[1]+n[1]*1.5*side}','none','#cad5d2',max(4,S*.016));a.path(f'M{s[0]} {s[1]} Q{c[0]} {c[1]} {q[0]} {q[1]}','none',INK,1.5)
 else:
  for j in range(3):a.path(f'M{p[0]-r*.4+j*r*.35} {p[1]+r*.1} q{-r*.15} {r*.4} {r*.15} {r*.55}','none','#647d85',1.5)

def character(a,d,P,S,contact=None):
 p=d['pose'];root=p['root'];sh=p['shoulder'];L=p['legs'];A=p['arms'];far=1
 for j in [1,0]:
  q=L[j];foot=q['sole'];screen=P(foot)
  if q['planted']:a.ellipse(screen[0],screen[1]+3,S*.135,S*.018,'#030c14',extra='opacity=".7"')
  limb(a,P,[q['hip'],q['knee'],q['ankle']],'#1c3543' if j==0 else '#152a38',S,.105)
  ang=q['pitch'];co,si=math.cos(ang),math.sin(ang)
  pts=[]
  for x,y in [(-.105,0),(.105,0),(.12,.035),(.045,.085),(-.08,.08)]:pts.append(foot+V(x*co-y*si,x*si+y*co,0))
  poly(a,P,pts,'#132733','#020a12',5);line(a,P,[pts[0]+V(0,.012,0),pts[1]+V(0,.012,0)],'#8b9c9d',2)
 # Far sleeve behind a single continuous hoodie silhouette.
 limb(a,P,[A[1]['shoulder'],A[1]['elbow'],A[1]['wrist']],'#192e3d',S,.095);hand(a,P,A[1]['wrist'],S)
 verts=[sh+V(-.20,.02,0),sh+V(.18,.02,0),root+V(.20,-.04,0),root+V(.12,-.10,0),root+V(-.19,-.07,0)]
 poly(a,P,verts,'url(#cloth)',INK,6);line(a,P,[sh+V(-.14,-.04,-.01),root+V(-.14,-.04,-.01)],'#4c6973',2)
 poly(a,P,[sh+V(-.18,.02,0),sh+V(-.12,.13,0),sh+V(.11,.13,0),sh+V(.19,.01,0),sh+V(.05,-.10,-.01),sh+V(-.06,-.10,-.01)],'#132b39',INK,4)
 for dx in [-.055,.055]:line(a,P,[sh+V(dx,-.05,-.015),sh+V(dx,-.25,-.015)],'#8b9a9c',1.7)
 line(a,P,[root+V(-.13,.11,-.025),root+V(.12,.11,-.025)],'#3c5965',2)
 h=np.array(P(p['head']));a.add(f'<g transform="translate({h[0]} {h[1]}) scale({S*.26/(61*2.62)})">');head(a,0,0,d['time'],p['yaw'],p['yaw'],p['fear'],p['tilt'],blink_override=max(0,1-abs(d['time']-1.1)/.065));a.add('</g>')
 limb(a,P,[A[0]['shoulder'],A[0]['elbow'],A[0]['wrist']],'#294653',S,.105);hand(a,P,A[0]['wrist'],S,contact,contact is not None)

def paper_details(a):
 # Fixed drawn strokes; not animated grain that could fake motion.
 for j in range(14):
  x=(j*173+73)%1080;y=(j*131+39)%1920;a.line([(x,y),(x+12,y+2)],'#52707a',.7)
def end(a):a.add('</svg>');return ''.join(a.s)
