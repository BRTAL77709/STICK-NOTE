"""One connected House17 and consistent vehicle interior, renderer Y-up metres."""
from world import *
from contact_rig import *
import vehicle_system as VS
RISE=2.6/15;ROOM=(-1.1,1.5,-5.6,.1);HOUSE_HEIGHT=5.4

def house(w):
 floor(w,-2.3,2.3,0,6.5)
 for x in [-2.3,2.3]:w.box(x-.04,0,0,.08,5.4,6.5,'#294653','House17 permanent side wall')
 w.box(-2.3,0,6.5,4.6,5.4,.08,'#1d3746','House17 rear wall');w.box(-2.3,2.5,0,2.6,.10,6.5,'#3a4e57','upper bedroom floor');w.box(.3,2.5,5.25,2.,.10,1.25,'#3a4e57','stair upper landing');w.box(-2.3,2.5,5.6,4.6,.10,.9,'#3a4e57','rear landing connection')
 w.box(.30,2.6,0,.08,2.8,5.6,'#203b48','bedroom partition')
 for i in range(15):
  w.box(.55,0,1.5+i*.25,1.,(i+1)*RISE,.25,'#435963','stair tread '+str(i+1));w.line([V(.55,(i+1)*RISE+.002,1.5+i*.25),V(1.55,(i+1)*RISE+.002,1.5+i*.25)],'#b09d7a',2)
 for i in range(0,16,2):
  z=1.5+i*.25;y=min(i+1,15)*RISE;w.tube([V(1.57,y,z),V(1.57,y+.78,z)],'#5b6e72',.022)
 w.tube([V(1.57,RISE+.78,1.5),V(1.57,3.38,5.25)],'#b8a278',.035)
 for z in [1.,3.5,5.3]:sconce(w,V(-2.23,1.95,z))
 w.box(-2.3,5.36,0,4.6,.08,6.5,'#172e3d','permanent ceiling')
 # Door in bedroom rear wall, shared with the upper landing route.
 for x,dx in [(-2.3,1.05),(-.35,.65)]:w.box(x,2.6,5.6,dx,2.8,.06,'#233e4b','bedroom rear partition')
 w.box(-1.25,4.72,5.6,.9,.68,.06,'#233e4b','bedroom rear doorway lintel')

def bedroom(w):
 x0,x1,z0,z1=ROOM;floor(w,x0,x1,z0,z1)
 for a,b,c,e in [(x0,-.77,0,2.8),(.77,x1,0,2.8),(-.77,.77,0,.60),(-.77,.77,2.2,2.8)]:w.face([V(a,c,.1),V(b,c,.1),V(b,e,.1),V(a,e,.1)],'#294651',name='permanent window wall')
 for x in [x0,x1]:w.face([V(x,0,z0),V(x,0,z1),V(x,2.8,z1),V(x,2.8,z0)],'#233e4b',name='permanent bedroom side wall')
 for a,b in [(x0,-.45),(.45,x1)]:w.face([V(a,0,z0),V(b,0,z0),V(b,2.8,z0),V(a,2.8,z0)],'#1d3744',name='permanent bedroom rear wall')
 w.box(-.45,2.12,z0-.025,.9,.68,.05,'#233e4b','bedroom door lintel');w.face([V(x0,2.8,z0),V(x1,2.8,z0),V(x1,2.8,z1),V(x0,2.8,z1)],'#172e39',name='permanent bedroom ceiling')
 for x in [-.45,.45]:w.box(x-.025,0,z0-.02,.05,2.12,.06,'#b09a75','bedroom doorway trim')
 w.box(.76,0,-4.2,.65,.36,1.7,'#1d3443','bed');w.box(.74,.36,-4.2,.69,.14,1.7,'#4a6170','mattress');w.box(.80,.5,-4.1,.55,.09,.34,'#a4aea3','pillow');w.box(-.72,0,-.92,.34,.72,.34,'#3a4f55','phone nightstand');sconce(w,V(.72,1.55,-3.9))
 for z in [-4.6,-2.9]:w.box(.94,0,z,.08,.10,.45,'#1c3038','bed leg')
 # A fixed warm pool from the actual bedside fixture, not random exposure changes.
 w.face([V(.76,.004,-4.7),V(1.45,.004,-4.7),V(1.45,.004,-2.3),V(.55,.004,-2.5)],'#3b4546',stroke='none',name='bedside warm light pool')

def cabin(w):
 w.box(-.75,.08,-1.35,1.5,.22,.55,'#253f4d','rear bench cushion');w.box(-.73,.30,-1.41,1.46,.72,.10,'#1d3543','rear bench back')
 for x in [-.46,.46]:w.box(x-.14,1.0,-1.40,.28,.17,.10,'#344f5a','rear headrest')
 w.face([V(-.61,1.445,.10),V(.61,1.445,.10),V(.63,1.425,-.92),V(-.63,1.425,-.92)],'#152b38',name='roof lining');w.box(-.10,.18,-.32,.20,.20,.93,'#263e4b','center console');w.box(-.04,.36,.28,.08,.12,.12,'#a3aaa1','gear selector')
 for side in [-1,1]:w.tube([V(side*.78,.70,-.23),V(side*.78,.70,-.05)],'#a9b0a6',.018)
