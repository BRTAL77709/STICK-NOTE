from world import *

def staircase(w):
 floor(w,-1.8,4.8,.1,5.8)
 wall(w,V(-1.8,0,3.1),V(4.8,0,3.1),5.15)
 wall(w,V(-1.8,0,0),V(-1.8,0,3.1),5.15)
 # Ceiling soffit, trim, complete upstairs hall and visible doorway.
 w.face([V(-1.8,5.15,0),V(4.8,5.15,0),V(4.8,5.15,3.1),V(-1.8,5.15,3.1)],'#142c3a',name='ceiling')
 for x in [-1.75,4.75]:w.box(x,0,2.95,.07,5.15,.10,'#4b626a','corner moulding')
 # Side skirt follows the flight, instead of isolated rectangles.
 w.face([V(-.5,0,1.97),V(2.38,2.4,1.97),V(2.38,2.18,1.97),V(-.5,0,1.97)],'#0d2432',w=4,name='stair stringer')
 for k in range(12):
  x=-.5+k*.24;y=k*.20
  w.box(x,y,1.0,.24,.20,.96,'#2d4149','riser '+str(k+1))
  w.face([V(x,y+.2,1),V(x+.24,y+.2,1),V(x+.24,y+.2,1.96),V(x,y+.2,1.96)],'#82735d',w=2,bias=-.008,name='tread '+str(k+1))
  w.line([V(x,y+.204,1),V(x,y+.204,1.96)],'#b9a989',2)
  for z in [1.13,1.76]:w.line([V(x+.025,y+.205,z),V(x+.22,y+.205,z)],'#695b4d',1)
  # Far balusters and lower near rail preserve sole visibility.
  for z in [1.96]:
   w.tube([V(x+.12,y+.20,z),V(x+.12,y+1.12,z)],'#61747b',.024)
 w.tube([V(-.5,.85,1.94),V(2.38,3.25,1.94)],'#a3a18c',.045)
 w.box(2.38,2.25,.75,2.42,.15,2.35,'#42525a','upper floor thickness');floor(w,2.38,4.8,.75,3.1,2.4)
 for x in [2.47,2.8,3.13]:w.tube([V(x,2.4,.77),V(x,3.26,.77)],'#607781',.025)
 w.tube([V(2.4,3.28,.77),V(3.25,3.28,.77)],'#a6a591',.045)
 # Hall door into actual bedroom, with jamb, inset panels and handle.
 w.box(3.60,2.4,2.93,.82,1.93,.08,'#122936','bedroom door');w.box(3.53,2.4,2.87,.07,2.02,.12,'#78858a','door jamb');w.box(4.42,2.4,2.87,.07,2.02,.12,'#78858a','door jamb');w.box(3.53,4.42,2.87,.96,.08,.12,'#78858a','door lintel')
 for yy in [2.66,3.56]:w.face([V(3.72,yy,2.91),V(4.3,yy,2.91),V(4.3,yy+.54,2.91),V(3.72,yy+.54,2.91)],'#24434f','#55717b',2,bias=-.01)
 w.tube([V(4.25,3.35,2.86),V(4.12,3.35,2.86)],'#deb47b',.025)
 for x,y in [(-.9,1.5),(.8,2.8),(2.6,4.1)]:sconce(w,V(x,y,3.02))
 for x,y in [(-.5,1.6),(1.25,3.1)]:frame(w,x,y,3.0,.52,.76)
 # Architectural seam and cast rail shadows on the rear wall.
 for k in range(9):w.line([V(-.4+k*.32,.65+k*.24,3.085),V(-.15+k*.32,1.52+k*.24,3.085)],'#18303d',7)

def entrance(w,inside=False):
 floor(w,-3.2,5.4,-3.8,4.6)
 # Same exact aperture/brick wall dimensions viewed from either side.
 z=.12 if inside else .0
 for x0,x1 in [(-3.2,1.7),(2.6,5.4)]:
  w.face([V(x0,0,z),V(x1,0,z),V(x1,4.9,z),V(x0,4.9,z)],'#243d49',name='House 17 facade')
  for y in np.arange(.18,4.9,.18):
   w.line([V(x0,y,z-.008),V(x1,y,z-.008)],'#435460',1)
   for x in np.arange(x0+(.28 if round(y/.18)%2 else .0),x1,.56):w.line([V(x,y,z-.009),V(x,y+.18,z-.009)],'#394f5b',1)
 w.face([V(1.7,2.1,z),V(2.6,2.1,z),V(2.6,4.9,z),V(1.7,4.9,z)],'#28434f',name='above doorway')
 for x in [1.61,2.60]:w.box(x,0,-.095,.09,2.20,.20,'#9c9b89','front door jamb')
 w.box(1.61,2.10,-.095,1.08,.10,.20,'#9c9b89','front door lintel')
 w.face([V(1.7,0,0),V(2.6,0,0),V(2.6,2.1,0),V(1.7,2.1,0)],'#07131e',stroke='none',bias=.15,name='open doorway interior')
 if not inside:
  # Porch, canopy, downpipe, windows, decorative side panels and runner.
  w.box(1.33,2.62,-.65,1.65,.16,.86,'#294351','porch canopy')
  w.box(3.7,0,-.04,.065,4.9,.08,'#102b3c','downpipe')
  for x in [.38,3.2]:
   w.box(x,.65,-.06,.73,1.2,.08,'#a2a795','sash frame');w.face([V(x+.06,.72,-.08),V(x+.67,.72,-.08),V(x+.67,1.78,-.08),V(x+.06,1.78,-.08)],'#193b50',w=2,bias=-.1)
   w.line([V(x+.36,.72,-.1),V(x+.36,1.78,-.1)],'#85938e',5)
   w.line([V(x+.06,1.2,-.1),V(x+.67,1.2,-.1)],'#85938e',5)
  w.box(1.86,2.27,-.06,.58,.23,.045,'#132c3b','number plaque');w.text(V(2.15,2.30,-.085),'17',.17)
  sconce(w,V(2.96,1.9,-.12));w.face([V(1.60,.006,-.92),V(2.64,.006,-.92),V(2.64,.006,-.15),V(1.60,.006,-.15)],'#0d2633','#58636a',3,bias=-.03,name='doormat')
  for j in range(8):w.line([V(1.65+j*.12,.01,-.88),V(1.65+j*.12,.01,-.19)],'#42515a',1)
 else:
  wall(w,V(-1.8,0,3.1),V(4.8,0,3.1),2.4);wall(w,V(-1.8,0,0),V(-1.8,0,3.1),2.4)
  w.box(.15,.10,1.9,.85,.45,.35,'#223d49','hall bench');sconce(w,V(.1,1.65,3.02));frame(w,1,1.05,3.0,.6,.85)

def bedroom(w):
 floor(w,.25,5.1,.0,5.1,2.4)
 wall(w,V(.25,0,0),V(.25,0,5.1),2.7,2.4)
 # Window is a genuine aperture; four wall polygons leave its opening clear.
 for xa,xb,ya,yb in [(.25,3.07,2.4,5.1),(4.33,5.1,2.4,5.1),(3.07,4.33,2.4,3.08),(3.07,4.33,4.52,5.1)]:w.face([V(xa,ya,0),V(xb,ya,0),V(xb,yb,0),V(xa,yb,0)],'#294653',name='bedroom window wall')
 for x in [3.,4.33]:w.box(x,3.03,-.025,.07,1.55,.18,'#a3aca4','window jamb')
 w.box(3.,3.03,-.03,1.40,.07,.30,'#8c9c98','sill');w.box(3.,4.52,-.03,1.4,.07,.18,'#96a6a1','window lintel')
 w.line([V(3.7,3.10,.045),V(3.7,4.52,.045)],'#8da2a0',4)
 # Bed with frame, mattress, folds, pillow, headboard and side table.
 w.box(.65,2.4,1.15,1.3,.30,2.20,'#173341','bed frame');w.box(.61,2.70,1.12,1.38,.23,2.22,'#72858a','mattress');w.box(.66,2.92,1.78,1.28,.035,1.50,'#395b6b','blanket');w.box(.65,2.93,1.22,1.28,.12,.46,'#a4aca6','pillow');w.box(.60,2.4,1.06,1.40,.92,.09,'#284452','headboard')
 for z in np.arange(1.92,3.25,.22):w.line([V(.68,2.96,z),V(1.90,2.96,z+.025)],'#5b7885',2)
 w.box(2.04,2.4,1.10,.50,.60,.46,'#2d424a','nightstand');sconce(w,V(2.30,3.36,.06));frame(w,.40,3.70,.07,.56,.68)
 # Door on return wall, visible in the establishing composition.
 w.box(.26,2.4,3.70,.035,2.05,.84,'#142e3d','bedroom entry');w.tube([V(.315,3.35,4.34),V(.315,3.35,4.20)],'#d0ac79',.025)
 w.face([V(.25,5.1,0),V(5.1,5.1,0),V(5.1,5.1,5.1),V(.25,5.1,5.1)],'#162e3e',name='bedroom ceiling')
