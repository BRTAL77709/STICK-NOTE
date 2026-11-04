"""Illustrated sedan rig with metric tires, steering, suspension, pitch and roll."""
import math
from motion_state import *
from world import INK

def sedan(a,c,t,black=False,reflection=False):
 s=state(t,black);sx,sz=s['x'],s['z'];yaw=s['yaw'];body='#122b39' if black else '#3a5d70';hi='#526f7c' if black else '#7d9aa4'
 def p(x,y,z,flat=False):
  # pitch and roll deform the suspended body; wheels retain their road-contact radius.
  if not flat:
   y+=s['pitch']*z+s['roll']*x+s['suspension_m']
  return sx+x*math.cos(yaw)+z*math.sin(yaw),y,sz+z*math.cos(yaw)-x*math.sin(yaw)
 def poly(ps,col,stroke=INK,w=3):
  points=camera_points(ps)
  if min(c.depth(q) for q in points)<.9:return
  pp=[c.project(q) for q in points]
  # Rounded ink contour avoids a faceted toy-car silhouette, retains fixed world geometry.
  paths=[]
  for j,cur in enumerate(pp):
   prev=pp[j-1];nxt=pp[(j+1)%len(pp)];u=.12
   pin=(cur[0]*(1-u)+prev[0]*u,cur[1]*(1-u)+prev[1]*u);pout=(cur[0]*(1-u)+nxt[0]*u,cur[1]*(1-u)+nxt[1]*u)
   paths.append(('M' if j==0 else 'L')+f'{pin[0]:.2f} {pin[1]:.2f} Q{cur[0]:.2f} {cur[1]:.2f} {pout[0]:.2f} {pout[1]:.2f}')
  a.path(' '.join(paths)+'Z',col,stroke,w)
 def camera_points(ps):return [p(*q) for q in ps]
 # Tire shadows and actual light footprints on wet ground.
 for side in [-1,1]:
  c.poly(a,[p(side*.9,.025,-2.2,True),p(side*1.4,.025,-2.2,True),p(side*1.4,.025,2.1,True),p(side*.9,.025,2.1,True)],'#07121a','none',0)
  a.add('<g opacity=".12">');c.poly(a,[p(side*.72,.04,2.25,True),p(side*.6-1.5,.04,13,True),p(side*.6+1.5,.04,13,True)],'#bfdae1','none',0);a.add('</g>')
 # Mirrored broad paint mass is tied to the same car, not a screen-space duplicate.
 a.add('<g opacity=".16">');c.poly(a,[p(-.95,-.1,-2.2,True),p(.95,-.1,-2.2,True),p(.95,-.65,2.2,True),p(-.95,-.65,2.2,True)],hi,'none',0);a.add('</g>')
 near=1 if (c.x-sx)*math.cos(yaw)-(c.z-sz)*math.sin(yaw)>0 else -1
 def wheel(side,z):
  steer=s['steer_rad'] if z>0 else 0;center=(side*1.02,.32,z)
  def wp(angle,r):
   yy=.32+r*math.cos(angle);zz=z+r*math.sin(angle)*math.cos(steer);xx=side*1.035+math.sin(steer)*r*math.sin(angle)
   return p(xx,yy,zz,True)
  pp=[wp(j*math.tau/24,.32) for j in range(24)];c.poly(a,pp,'#050b10','#101b24',3)
  c.poly(a,[wp(j*math.tau/24,.22) for j in range(24)],'#263d4a','#73848a',2)
  for j in range(7):
   th=s['wheel_rad']+j*math.tau/7;c.line(a,[wp(th,.05),wp(th,.205)],'#a2b0ac',2.3)
  # road-water spray begins behind each physically moving contact patch
  if s['speed_kmh']>25:
   for j in range(7):
    u=(t*3+j*.137)%1;pt=p(side*1.1+side*u*.24,.05+u*.18,z-.3-u*.9,True)
    if c.depth(pt)>1:
     xx,yy=c.project(pt);a.line([(xx,yy),(xx-3,yy-5)],'#8da6ab',1.2)
 for z in [-1.35,1.35]:wheel(-near,z)
 # Flat illustrated planes; painter order changes with viewing angle.
 faces=[
 ([(-.98,.4,-2.35),(.98,.4,-2.35),(.96,.95,-2.1),(-.96,.95,-2.1)],body),
 ([(-.98,.4,2.35),(.98,.4,2.35),(.95,.92,2.2),(-.95,.92,2.2)],body),
 ([(-.96,.9,-2.15),(.96,.9,-2.15),(.91,1.02,-1.1),(-.91,1.02,-1.1)],hi),
 ([(-.95,.92,2.2),(.95,.92,2.2),(.87,1.04,.85),(-.87,1.04,.85)],hi),
 ([(-.78,1.5,-.6),(.78,1.5,-.6),(.77,1.5,.4),(-.77,1.5,.4)],body),
 ([(-.91,1.02,-1.1),(.91,1.02,-1.1),(.78,1.5,-.6),(-.78,1.5,-.6)],'#0c2331'),
 ([(-.87,1.04,.85),(.87,1.04,.85),(.77,1.5,.4),(-.77,1.5,.4)],'#153947')]
 for side in [-1,1]:
  faces += [([(side*.98,y,z) for z,y in [(-2.35,.4),(-1.76,.4),(-1.65,.65),(-1.52,.76),(-1.35,.79),(-1.17,.76),(-1.04,.65),(-.94,.4),(.94,.4),(1.04,.65),(1.17,.76),(1.35,.79),(1.53,.76),(1.66,.65),(1.76,.4),(2.35,.4),(2.4,.6),(2.28,.91),(.85,1.04),(-1.1,1.02),(-2.1,.95),(-2.39,.72)]],body),
  ([(side*.91,1.02,-1.1),(side*.87,1.04,.85),(side*.77,1.5,.4),(side*.78,1.5,-.6)],'#112a38')]
 for ps,col in sorted(faces,key=lambda f:-sum(c.depth(p(*q)) for q in f[0])/len(f[0])):poly(ps,col,INK,3.8)
 # Window mullions, side mirrors, handles, body/door seams and amber rim.
 for side in [-1,1]:
  c.line(a,[p(side*.84,1.06,-.12),p(side*.775,1.48,-.12)],'#6a828b',3)
  c.line(a,[p(side*.98,.46,-.14),p(side*.90,1.01,-.14)],'#152e3b',2)
  c.line(a,[p(side*1.01,.85,-.45),p(side*1.01,.85,-.72)],'#a9aaa0',2)
  poly([(side*.9,1.05,.65),(side*1.2,1.08,.58),(side*1.22,.94,.58),(side*.93,.95,.65)],body)
  c.line(a,[p(side*.97,.96,-2.12),p(side*.91,1.02,-1.1),p(side*.78,1.51,-.6),p(side*.77,1.51,.4)],'#a3a79a' if side<0 else '#526e7b',2)
 # Authored curved side-shell: cap roof, glass, fenders and wheel arches retain illustration character.
 def sidepath(commands,col,stroke=INK,w=4):
  path=[]
  for cmd,coords in commands:
   if cmd=='Z':path.append('Z');continue
   pp=[c.project(p(near*.995,y,z)) for z,y in coords]
   path.append(cmd+' '.join(f'{x:.2f} {y:.2f}' for x,y in pp))
  if c.depth(p(0,.8,0))>2:a.path(' '.join(path),col,stroke,w)
 sidepath([('M',[(-2.35,.4)]),('Q',[(-2.55,.74),(-2.26,.99)]),('L',[(-1.15,1.08)]),('Q',[(-.82,1.57),(-.40,1.59)]),('L',[(.53,1.59)]),('Q',[(.98,1.54),(1.28,1.06)]),('Q',[(2.08,1.04),(2.39,.78)]),('Q',[(2.46,.59),(2.31,.40)]),('L',[(1.79,.37)]),('C',[(1.78,.89),(.93,.89),(.91,.37)]),('L',[(-.91,.37)]),('C',[(-.93,.89),(-1.78,.89),(-1.79,.37)]),('Z',[])],body,INK,4.8)
 sidepath([('M',[(-.99,1.09)]),('Q',[(-.71,1.5),(-.37,1.51)]),('L',[(-.15,1.51),(-.15,1.09)]),('Z',[])],'#102b3b','#718c96',2.4)
 sidepath([('M',[(.02,1.09)]),('L',[(.02,1.51),(.51,1.51)]),('Q',[(.86,1.48),(1.10,1.09)]),('Z',[])],'#12313f','#718c96',2.4)
 sidepath([('M',[(-2.18,.92)]),('Q',[(-.4,1.02),(1.2,1.01)]),('L',[(2.19,.83)])],'none',hi,2)
 sidepath([('M',[(-.09,.45)]),('L',[(-.09,1.06)])],'none','#0a1b28',2.4)
 sidepath([('M',[(-.62,.9)]),('L',[(-.37,.9)])],'none','#b4b8ab',3)
 sidepath([('M',[(.52,.9)]),('L',[(.75,.9)])],'none','#b4b8ab',3)
 sidepath([('M',[(-.83,1.15)]),('L',[(-.43,1.46)])],'none','#607f8e',1.6)
 # Fixed-world amber lamps sweep across the suspended illustrated body.
 light=math.exp(-(((s['z']+180+12)%24-12)/4.2)**2)
 a.add(f'<g opacity="{light*.22:.4f}">')
 poly([(-.95,.93,2.2),(.95,.93,2.2),(.87,1.05,.85),(-.87,1.05,.85)],'#e2aa63','none',0)
 poly([(near*.996,.90,-1.9),(near*.996,.92,1.95),(near*.996,1.03,.85),(near*.996,1.02,-1.1)],'#e2aa63','none',0)
 a.add('</g>')
 # Two distinctive rear lamps and physical front lamps.
 for side in [-1,1]:
  for z,co in ([(2.36,'#eff6f0')] if ((c.x-sx)*math.sin(yaw)+(c.z-sz)*math.cos(yaw))>0 else [(-2.36,'#ff8e71' if s['acceleration_mps2']<-.2 else '#f66b59')]):
   ps=[(side*.47,.66,z),(side*.90,.68,z),(side*.90,.79,z),(side*.48,.77,z)];poly(ps,co,INK,2)
  for j in range(5):
   zz=-2.5-j*.35;c.line(a,[p(side*.7-.18,.035,zz,True),p(side*.7+.18,.035,zz,True)],'#8e4543',2)
 if ((c.x-sx)*math.sin(yaw)+(c.z-sz)*math.cos(yaw))>0:
  poly([(-.5,.41,2.40),(.5,.41,2.40),(.58,.61,2.40),(-.58,.61,2.40)],'#041019','#52707c',2)
  for xx in [-.36,-.18,0,.18,.36]:c.line(a,[p(xx,.44,2.42),p(xx,.58,2.42)],'#3b5968',1.5)
  for side in [-1,1]:
   pp=p(side*.72,.735,2.38);xx,yy=c.project(pp);sc=c.f/max(2,c.depth(pp));a.ellipse(xx,yy,sc*.32,sc*.18,'#d1eff2',extra='opacity=".22"')
 else:
  poly([(-.25,.46,-2.37),(.25,.46,-2.37),(.25,.59,-2.37),(-.25,.59,-2.37)],'#b8c0b8','#0a1620',1)
 for z in [-1.35,1.35]:wheel(near,z)
