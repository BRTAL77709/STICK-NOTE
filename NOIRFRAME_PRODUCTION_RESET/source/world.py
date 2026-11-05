"""Illustrated metric environments and a stable sedan hierarchy, no photoreal shaders."""
from rigs import *
def text(name,body,location,size=.2,parent=None):
 c=bpy.data.curves.new(name,'FONT');c.body=body;c.size=size;c.align_x='CENTER';o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.location=location;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat('Letter amber','#edac57'));o.parent=parent;return o
class Car:
 def __init__(self,name='Sedan',black=False):
  self.root=empty(name+' WORLD');self.body=empty(name+' suspension',parent=self.root);self.wheels=[];col=mat('Black sedan' if black else 'Witness sedan','#142d3a' if black else '#3a5c70')
  # Extruded illustrated side shell, wheel arches stay invariant in vehicle coordinates.
  profile=[(-2.25,.40),(-1.80,.40),(-1.73,.66),(-1.54,.76),(-1.16,.76),(-.98,.40),(.98,.40),(1.16,.76),(1.54,.76),(1.73,.66),(1.80,.40),(2.25,.40),(2.30,.74),(2.08,.96),(.90,1.01),(-1.02,1.01),(-2.22,.89),(-2.37,.65)]
  verts=[(x,y,z) for y in [-.91,.91] for x,z in profile];n=len(profile);faces=[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n) if j not in [5,14]];mesh(name+' fixed body shell',verts,faces,col,self.body)
  cube(name+' roof',(-.12,0,1.55),(1.58,1.61,.09),col,self.body)
  for side in [-1,1]:
   for x,top in [(-.96,-.83),(.94,.64)]:line(name+' window pillar',[(x,side*.86,1.0),(top,side*.78,1.52)],.035,col,self.body)
   line(name+' centre pillar',[(-.1,side*.86,1.01),(-.1,side*.79,1.52)],.025,col,self.body)
   for x in [-.48,.40]:line(name+' door handle',[(x-.09,side*.93,.87),(x+.09,side*.93,.87)],.015,mat('Handle','#8a9da3'),self.body)
   for x in [-1.35,1.35]:
    steering=empty(name+f' steering {side} {x}',(x,side*.90,.33),self.root);rolling=empty(name+' distance driven tire',parent=steering);self.wheels.append((steering,rolling,x))
    bpy.ops.mesh.primitive_torus_add(major_segments=16,minor_segments=6,location=(0,0,0),major_radius=.245,minor_radius=.085);t=bpy.context.object;t.name=name+' tire';t.rotation_euler=(math.pi/2,0,0);t.data.materials.append(INK());t.parent=rolling
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.205,depth=.17);rim=bpy.context.object;rim.rotation_euler=(math.pi/2,0,0);rim.data.materials.append(mat('Wheel rim','#516b78'));rim.parent=rolling
    for k in range(7):
     q=k*math.tau/7;line(name+' wheel spoke',[(0,side*.10,0),(.18*math.cos(q),side*.10,.18*math.sin(q))],.009,mat('Spoke','#a3afb0'),rolling)
  for side in [-1,1]:
   cube(name+' headlight',(2.27,side*.64,.80),(.035,.38,.10),mat('Headlight','#d3e3df'),self.body);cube(name+' tail light',(-2.28,side*.63,.73),(.03,.42,.09),mat('Tail red','#db5346'),self.body)
  if black:
   mesh(name+' front windscreen',[(.94,-.85,1.01),(.94,.85,1.01),(.64,.78,1.52),(.64,-.78,1.52)],[(0,1,2,3)],mat('Tinted windscreen','#2a4654'),self.body)
   cube(name+' front grille',(2.32,0,.59),(.025,.70,.10),mat('Grille','#526a75'),self.body)
   cube(name+' plate',(2.34,0,.47),(.025,.30,.09),mat('Plate','#bbc6bf'),self.body)
  cube(name+' real cabin floor',(0,0,.09),(1.8,1.6,.02),mat('Cabin floor','#0b1c29'),self.body)
  # Open illustrated glass regions retain the visible driver, rather than opaque window planes.
  cube(name+' seat',(.08,-.40,.23),(.52,.52,.10),mat('Seat','#102430'),self.body)
  self.wheel=empty(name+' steering wheel',(.36,-.43,.78),self.body);self.wheel.rotation_euler.y=-.20
  line(name+' steering column',[(.76,-.43,.82),(.36,-.43,.78)],.025,mat('Column','#263e4e'),self.body)
  bpy.ops.mesh.primitive_torus_add(major_radius=.14,minor_radius=.017,major_segments=20,minor_segments=6);w=bpy.context.object;w.rotation_euler=(0,math.pi/2,0);w.parent=self.wheel;w.data.materials.append(INK())
  for j in range(3):
   angle=j*math.tau/3;line(name+' steering spoke',[(0,0,0),(0,.14*math.cos(angle),.14*math.sin(angle))],.009,mat('Steering metal','#7c9098'),self.wheel)
 def pose(self,frame,x,y,yaw,distance,steer,pitch=0):
  self.root.location=(x,y,0);self.root.rotation_euler=(0,0,yaw);self.body.rotation_euler=(0,pitch,0);key(self.root,frame);key(self.body,frame,('rotation_euler',))
  for s,r,x in self.wheels:s.rotation_euler.z=steer if x>0 else 0;r.rotation_euler.y=distance/.33;key(s,frame,('rotation_euler',));key(r,frame,('rotation_euler',))
  self.wheel.rotation_euler.x=-steer*7;key(self.wheel,frame,('rotation_euler',))
def street():
 cube('Wet road',(12,0,-.06),(64,7,.12),mat('Wet navy','#0c2533'))
 for x in range(-18,46,3):cube('Road dash',(x,0,.009),(1.25,.06,.012),mat('Road paint','#97a7a5'))
 for side in [-1,1]:
  cube('Kerb',(12,side*3.6,.10),(64,.35,.20),mat('Kerb','#38505c'))
  for j,x in enumerate(range(-16,45,6)):
   y=side*(5.0+(j%2)*.3);height=3.2+(j%3)*.5;cube('Layered illustrated house',(x,y,height/2),(4.3,2.5,height),mat('House '+str(j%3),['#17313f','#1e3c49','#102633'][j%3]));mesh('Roof',[(x-2.3,y-1.4,height),(x+2.3,y-1.4,height),(x,y-1.4,height+1.0),(x-2.3,y+1.4,height),(x+2.3,y+1.4,height),(x,y+1.4,height+1)],[(0,1,2),(3,5,4),(0,3,4,1),(0,2,5,3),(1,4,5,2)],mat('Roof','#0a1c29'))
   for z in [1,2.2]:
    for dx in [-1,1]:cube('Amber window',(x+dx,y-side*1.27,z),(.55,.03,.7),mat('Window '+str((j+int(z))%2),['#a4733c','#294752'][(j+int(z))%2]))
   lampy=side*3.3;line('Street lamp',[(x,lampy,0),(x,lampy,3.7),(x,lampy-side*.6,3.9)],.035,INK());sphere('Lamp glow',(x,lampy-side*.6,3.88),(.16,.13,.04),mat('Lamp','#f0b568'))
   for k in range(8):cube('Warm wet reflection',(x+.20*math.sin(k*1.3),lampy-side*(.5+k*.25),.012),(.16+k*.05,.08,.009),mat('Reflection','#6b563c'))
def house17():
 stone=mat('House17 wall','#183744');cube('Front wall left',(.05,.16,1.6),(2.10,.30,3.2),stone);cube('Front wall right',(3.1,.16,1.6),(2.2,.30,3.2),stone);cube('Lintel',(1.55,.16,2.65),(.90,.30,1.10),stone)
 for x in [1.06,2.04]:cube('Door frame',(x,-.02,1.01),(.07,.1,2.02),mat('Frame','#70858a'))
 cube('Door head',(1.55,-.02,2.03),(1.05,.1,.07),mat('Frame','#70858a'));cube('Interior floor',(1.5,1.5,-.03),(4,3,.06),mat('Interior','#0b1e2b'));cube('Interior back',(1.5,3,1.5),(4,.12,3),mat('Interior wall','#102733'));text('House number','17',(1.56,-.10,2.30),.28);cube('Entry lamp body',(2.25,-.15,1.80),(.14,.16,.28),INK());sphere('Entry amber pane',(2.25,-.24,1.80),(.05,.02,.10),mat('Entry amber','#e4a653'));mesh('Illustrated lamp pool',[(2.1,-.1,.007),(2.4,-.1,.007),(2.9,-1.2,.007),(1.6,-1.2,.007)],[(0,1,2,3)],mat('Amber pavement','#464a38'))
 # Actual separate hinge object. Door leaf and both hardware objects are its children.
 hinge=empty('Door HINGE world',(1.10,0,0));cube('Door LEAF',(.45,0,1.0),(.90,.065,2.0),mat('Door','#234451'),hinge)
 for z in [.55,1.48]:
  for x in [.08,.80]:line('Door panel',[(x,-.04,z-.28),(x,-.04,z+.28)],.007,mat('Door panel line','#59737d'),hinge)
 spindle=empty('Handle SPINDLE',(.78,-.075,1.0),hinge);cube('Lever',(.065,0,0),(.16,.035,.035),mat('Handle brass','#d9a05b'),spindle);sphere('Keyhole',(.78,-.045,1.17),(.035,.012,.045),INK(),hinge)
 for z in [.23,1.77]:cube('Door hinge plate',(0,0,z),(.05,.10,.12),mat('Hinge','#71868b'),hinge)
 keyobj=empty('Key constrained to wrist')
 bpy.ops.mesh.primitive_torus_add(major_radius=.050,minor_radius=.006,major_segments=12,minor_segments=4);o=bpy.context.object;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat('Key metal','#d3af64'));o.parent=keyobj
 line('Key shaft',[(0,0,0),(0,.15,0)],.008,mat('Key metal','#d3af64'),keyobj);cube('Key teeth',(.012,.135,0),(.035,.025,.012),mat('Key metal','#d3af64'),keyobj)
 return hinge,spindle,keyobj

def stairs_window():
 floor=mat('Interior teal','#142f3e');cube('Ground floor',(.1,-.2,-.05),(4,4,.1),floor)
 for j in range(3):
  x=.0+j*.44;h=.2*(j+1);cube('Physical tread '+str(j+1),(x,.0,h/2),(.44,1.2,h),mat('Stairs','#284958'));line('Stair nosing'+str(j),[(x-.22,-.62,h),(x+.22,-.62,h)],.009,mat('Tread line','#8a9c9d'))
 for j in range(4):
  x=-.20+j*.44;z=.2*(j+1)+.75;line('Far railing upright',[(x,.70,max(0,z-.95)),(x,.70,z)],.018,mat('Rail','#66818c'))
 line('Far stair handrail',[(-.20,.70,.95),(1.12,.70,1.55)],.025,mat('Rail','#66818c'))
 cube('Upper landing',(2.25,.1,.55),(3.1,2.4,.10),floor)
 wall=mat('Room wall','#183744');cube('Wall left',(1.15,.15,1.8),(1.8,.25,3.6),wall);cube('Wall right',(4.3,.15,1.8),(2.3,.25,3.6),wall);cube('Wall below window',(2.6,.15,1.0),(1.2,.25,1.0),wall);cube('Wall above window',(2.6,.15,3.25),(1.2,.25,1.0),wall)
 for x in [2.0,3.2]:cube('Window jamb',(x,-.04,2.125),(.055,.1,1.35),mat('Window frame','#718a94'))
 for z in [1.45,2.8]:cube('Window horizontal',(2.6,-.04,z),(1.25,.1,.055),mat('Window frame','#718a94'))
 line('Curtain rod',[(1.95,-.12,2.87),(3.3,-.12,2.87)],.018,mat('Rod','#a7aaa1'))
 # Distant real sedan, road and lamps exist outside the actual wall aperture.
 cube('Street outside window',(3,8,-.05),(12,22,.1),mat('Outside road','#0b2331'));car=Car('Outside black sedan',True);car.root.location=(3.0,8.2,0);car.root.scale=(1,)*3;car.root.rotation_euler.z=-math.pi/2
 return car
