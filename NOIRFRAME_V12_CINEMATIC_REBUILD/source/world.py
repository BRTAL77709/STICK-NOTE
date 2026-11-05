"""Perspective illustrated world: metres, Y up, camera space, depth-sorted cel surfaces.
No image planes used for environments. Every architecture vertex has a fixed world position.
"""
from rig import *
from svg import Art
INK='#06121c'
class Camera:
 def __init__(self,eye,target,focal=1300,center=(540,960)):
  self.eye=np.array(eye);self.target=np.array(target);self.focal=focal;self.center=center;self.forward=self.target-self.eye;self.forward/=np.linalg.norm(self.forward);self.right=np.cross(V(0,1,0),self.forward);self.right/=np.linalg.norm(self.right);self.up=np.cross(self.forward,self.right)
 def depth(self,p):return float(np.dot(np.array(p)-self.eye,self.forward))
 def scale(self,p):return self.focal/max(.12,self.depth(p))
 def __call__(self,p):
  q=np.array(p)-self.eye;s=self.scale(p);return (self.center[0]+s*np.dot(q,self.right),self.center[1]-s*np.dot(q,self.up))
class World:
 def __init__(self,cam,t=0):self.cam=cam;self.t=t;self.q=[];self.geometry=[];self.ops=[]
 def clip(self,pts):
  out=[]
  for a,b in zip(pts,pts[1:]+pts[:1]):
   da=self.cam.depth(a)-.10;db=self.cam.depth(b)-.10
   if da>=0:out.append(a)
   if (da>=0)!=(db>=0):out.append(a+(b-a)*da/(da-db))
  return out
 def clipline(self,pts):
  out=[]
  for a,b in zip(pts,pts[1:]):
   da=self.cam.depth(a)-.10;db=self.cam.depth(b)-.10
   if da>=0:out.append(a)
   if (da>=0)!=(db>=0):out.append(a+(b-a)*da/(da-db))
  if self.cam.depth(pts[-1])>=.1:out.append(pts[-1])
  return out
 def submit(self,pts,fn,bias=0):
  if min(self.cam.depth(p) for p in pts)<.08:return False
  self.q.append((sum(self.cam.depth(p) for p in pts)/len(pts)+bias,len(self.q),fn));self.ops.append(('glyph',pts,fn,bias));return True
 def face(self,pts,col,stroke=INK,w=2,bias=0,name='surface'):
  pts=self.clip([np.array(p,float) for p in pts]);
  if len(pts)<3:return
  self.geometry.append({'name':name,'vertices':[p.tolist() for p in pts],'color':col});self.submit(pts,lambda a:a.poly([self.cam(p) for p in pts],col,stroke,w),bias)
  if self.ops and self.ops[-1][0]=='glyph':self.ops[-1]=('face',pts,col,stroke,w)
 def line(self,pts,col,w=3,bias=-.006):
  pts=self.clipline([np.array(p,float) for p in pts]);
  if len(pts)<2:return
  self.submit(pts,lambda a:a.line([self.cam(p) for p in pts],col,w),bias)
  if self.ops and self.ops[-1][0]=='glyph':self.ops[-1]=('line',pts,col,w,bias)
 def tube(self,pts,col,width=.06):
  pts=[np.array(p,float) for p in pts];S=self.cam.scale(np.mean(pts,axis=0));self.line(pts,INK,S*width+5,0);self.line(pts,col,S*width,-.008)
 def box(self,x,y,z,dx,dy,dz,col='#254452',name='box'):
  # Per-face flat shading, no glossy realistic materials.
  p=[V(x+i*dx,y+j*dy,z+k*dz) for i,j,k in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]]
  colors=[col,'#162c39','#35515d',col,'#405c65','#102632']
  for ii,cc in zip([(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(3,2,6,7),(0,3,7,4)],colors):
   ps=[p[n] for n in ii];center=np.mean(ps,axis=0);out=center-V(x+dx/2,y+dy/2,z+dz/2)
   if np.dot(out,self.cam.eye-center)>0:self.face(ps,cc,name=name)
 def text(self,p,s,size=.12,col='#eac38a'):
  p=np.array(p);S=self.cam.scale(p);x,y=self.cam(p);self.submit([p],lambda a:a.add(f'<text x="{x}" y="{y}" font-size="{S*size}" fill="{col}" font-family="DejaVu Sans" text-anchor="middle">{s}</text>'),-.03)
 def glow(self,p,r=.5):
  x,y=self.cam(p);S=self.cam.scale(p);self.submit([p],lambda a:a.ellipse(x,y,S*r,S*r*1.3,'url(#amber)'),-.03)
 def render(self,overlay=None):
  a=Art();a.add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920"><defs><linearGradient id="face"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#a6b7bd"/></linearGradient><radialGradient id="amber"><stop stop-color="#f2b56d" stop-opacity=".30"/><stop offset="1" stop-color="#f2b56d" stop-opacity="0"/></radialGradient><radialGradient id="vignette"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".46"/></radialGradient></defs>');a.rect(0,0,1080,1920,'#091b2a')
  for _,__,fn in sorted(self.q,key=lambda q:(-q[0],q[1])):fn(a)
  if overlay:overlay(a)
  a.rect(0,0,1080,1920,'url(#vignette)');a.add('</svg>');return ''.join(a.s)

def floor(w,x0,x1,z0,z1,y=0):
 start=len(w.q)
 w.face([V(x0,y,z0),V(x1,y,z0),V(x1,y,z1),V(x0,y,z1)],'#263b43',name='floor')
 for z in np.arange(z0,z1,.28):w.line([V(x0,y+.003,z),V(x1,y+.003,z)],'#50616a',1)
 for k,x in enumerate(np.arange(x0,x1,.62)):
  for z in np.arange(z0+(k%2)*.14,z1,.84):w.line([V(x,y+.004,z),V(x,y+.004,min(z+.28,z1))],'#172b35',1)

 for j in range(start,len(w.q)):
  depth,idx,fn=w.q[j];w.q[j]=(depth+1000,idx,fn)

def wall(w,a,b,height,base=0):
 a=np.array(a);b=np.array(b);u=V(0,height,0);w.face([a+V(0,base,0),b+V(0,base,0),b+V(0,base,0)+u,a+V(0,base,0)+u],'#243e4b',name='wall')
 for y in [.08,.87,.94,height-.12]:w.line([a+V(0,base+y,0),b+V(0,base+y,0)],'#5a7179',4)
 for f in np.arange(.05,.98,.12):
  q=mix(a,b,f)+V(0,base,0);w.line([q+V(0,.1,0),q+V(0,.86,0)],'#38535e',2)

def sconce(w,p):
 p=np.array(p);w.glow(p,.57);w.box(*(p+V(-.065,-.13,0)),.13,.26,.055,'#182c38','sconce');w.face([p+V(-.04,-.08,-.01),p+V(.04,-.08,-.01),p+V(.04,.08,-.01),p+V(-.04,.08,-.01)],'#edb875',w=1,bias=-.03);w.line([p+V(0,-.12,-.02),p+V(0,.12,-.02)],'#2e2b29',3)

def frame(w,x,y,z,width=.5,height=.7):
 w.box(x,y,z,width,height,.045,'#887754','picture frame');w.face([V(x+.045,y+.05,z-.005),V(x+width-.045,y+.05,z-.005),V(x+width-.045,y+height-.05,z-.005),V(x+.045,y+height-.05,z-.005)],'#153444',w=1,bias=-.02)
 for j in range(4):w.line([V(x+.07,y+.08+j*.07,z-.012),V(x+width-.07,y+.15+j*.10,z-.012)],'#486273',2)

def_unused=0
