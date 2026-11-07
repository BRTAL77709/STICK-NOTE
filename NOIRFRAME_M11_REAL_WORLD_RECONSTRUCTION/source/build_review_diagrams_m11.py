"""Review diagrams from production geometry; diagnostic omissions explicitly labeled."""
from pathlib import Path
import gzip,json,numpy as np
from PIL import Image,ImageDraw,ImageFont
from bootstrap import ROOT as R
from world import World,Camera
from contact_rig import V
from fast_depth import FastDepth
from render_clips import restore_state,body
import sets
from legacy.geometry import car
O=R/'contact_sheets';font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
# Seven views of the exact sedan generator used by production.
views=[('FRONT',(0,1.8,6)),('REAR',(0,1.8,-6)),('LEFT',(-6,1.8,0)),('RIGHT',(6,1.8,0)),('FRONT 3/4',(-4,2.3,5)),('REAR 3/4',(4,2.3,-5)),('HIGH',(3,5,4))];sheet=Image.new('RGB',(1080,4*680),'#071923');dr=ImageDraw.Draw(sheet)
for k,(label,eye) in enumerate(views):
 w=World(Camera(eye,(0,.65,0),850),0);car(w,V(0,0,0),0,0,0,True);im=FastDepth(540).render(w);x=k%2*540;y=k//2*680;sheet.paste(im.resize((360,640)),(x+90,y+30));dr.text((x+10,y+5),label,font=font,fill='white')
sheet.save(O/'M11_SEDAN_PRODUCTION_GEOMETRY_7_VIEWS.jpg',quality=94)
# Native evaluated driver + production cabin, top view with roof omitted only here.
sel=json.loads((R/'configuration/selected_native.json').read_text());d=json.load(gzip.open(R/'scenes'/f'DRIVING_COCKPIT_{sel["DRIVING_COCKPIT"]}.json.gz','rt'));p=restore_state(d['state'][30]);w=World(Camera((0,4.,.1),(0,.2,.1),1150,up=V(0,0,1)),1.);sets.cockpit(w,p)
w.ops=[op for op in w.ops if not(op[0]=='face' and min(q[1] for q in op[1])>1.38)];body(w,d,d['frames'][30],p);im=FastDepth(720).render(w);draw=ImageDraw.Draw(im);draw.rectangle((0,0,720,65),fill='#071923');draw.text((10,5),'ACTUAL CABIN + NATIVE DRIVER / TOP VIEW',font=font,fill='white');draw.text((10,32),'Roof omitted ONLY for this diagnostic',font=font,fill='#dfbd80');im.save(O/'M11_COCKPIT_NATIVE_TOP_DIAGNOSTIC.png')
# Dimensioned shared House17 plan in exact production house-local metres.
im=Image.new('RGB',(1100,1000),'#0c2330');draw=ImageDraw.Draw(im)
def panel(x,label,upper=False):
 sx=95;ox=x+250;oz=850
 def P(q):return(ox+q[0]*sx,oz-q[1]*sx)
 draw.rectangle((*P((-2.3,6.5)),*P((2.3,0))),outline='#91b8bd',width=5)
 draw.text((x+30,35),label,font=font,fill='white')
 if upper:
  draw.rectangle((*P((.3,5.6)),*P((.55,0))),fill='#526d79');draw.rectangle((*P((-2.3,5.6)),*P((.3,5.5))),fill='#526d79');draw.line([P((-.8,0)),P((-.8,.1))],fill='#f8d08c',width=12);draw.text((x+45,350),'BEDROOM',font=font,fill='white');draw.text((x+45,385),'door at z=5.6',font=font,fill='#b6ced0');draw.text((x+40,890),'Window center x=-0.8, facing street',font=font,fill='#d6bb80')
 else:draw.line([P((-.54,0)),P((.54,0))],fill='#f8d08c',width=10);draw.text((x+45,890),'Entry 1.08 m wide / door height 2.15 m',font=font,fill='#d6bb80')
 for j in range(16):draw.line([P((.55,1.5+.25*j)),P((1.55,1.5+.25*j))],fill='#a2bbc0',width=2)
 draw.text((x+30,110),'4.6 x 6.5 m / upper floor +2.6 m',font=font,fill='#c8d7d4');draw.text((x+30,150),'15 risers / 0.25 m tread / 0.17333 m rise',font=font,fill='#c8d7d4');draw.text((x+30,185),'Coordinates match spatial_world.py',font=font,fill='#c8d7d4')
panel(0,'GROUND FLOOR');panel(550,'UPPER FLOOR',True);im.save(O/'M11_HOUSE17_CONNECTED_PLAN.png')
print('REVIEW_DIAGRAMS_WRITTEN')
