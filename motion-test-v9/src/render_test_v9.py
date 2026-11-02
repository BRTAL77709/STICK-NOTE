"""V9: V8 rigs/renderer, continuous retiming and verified closed-before-reaction states."""
from v8_engine import *
import v8_engine as b
DURATION=10.;FPS=30
# Smooth quintic easing gives zero acceleration at authored holds.
def smooth(x):
 x=max(0,min(1,x));return x*x*x*(10+x*(-15+6*x))
b.smooth=smooth

def clock(t):
 # Monotonic PCHIP retiming of the existing V8 action; no pose replacement cuts.
 points=[(0,0),(1.4,1.5),(2.3,2.5),(3.,3.1),(4.6,4.35),(5.5,4.98),(6.2,5.72),(6.7,6.12),(7.1,6.35),(10.,6.35)]
 xs=[p[0] for p in points];ys=[p[1] for p in points];d=[(ys[i+1]-ys[i])/(xs[i+1]-xs[i]) for i in range(len(xs)-1)];slopes=[d[0]]
 for i in range(1,len(xs)-1):
  if d[i-1]*d[i]<=0:slopes.append(0.)
  else:
   h0=xs[i]-xs[i-1];h1=xs[i+1]-xs[i];w1=2*h1+h0;w2=h1+2*h0;slopes.append((w1+w2)/(w1/d[i-1]+w2/d[i]))
 slopes.append(0.)
 for i in range(len(xs)-1):
  if t<=xs[i+1]:
   h=xs[i+1]-xs[i];u=max(0,(t-xs[i])/h)
   return (2*u**3-3*u*u+1)*ys[i]+(u**3-2*u*u+u)*h*slopes[i]+(-2*u**3+3*u*u)*ys[i+1]+(u**3-u*u)*h*slopes[i+1]
 return ys[-1]

def ease(t,a,b):return smooth((t-a)/(b-a))
STATES=[(0.,'DRAGGING'),(1.4,'TRUNK_OPENING'),(2.3,'REPOSITIONING'),(3.,'LIFTING'),(4.6,'LOADING'),(6.2,'RELEASING'),(6.7,'TRUNK_CLOSING'),(7.5,'TRUNK_CLOSED'),(7.75,'WITNESS_NOTICED'),(8.,'HEAD_TURNING'),(9.2,'THREATENING_STARE')]
def state_at(t):return next(name for start,name in reversed(STATES) if t>=start)
def trunk_angle(t):return 102*b.ease(clock(t),1.82,2.42)*(1-ease(t,6.95,7.5))
def head_time(t):
 assert t<8 or trunk_angle(t)==0,'Head turn prohibited before verified closure'
 if t<8:return 3.2
 if t<9.2:return 3.35+(t-8)*.65/1.2
 return 4+min(.5,max(0,t-9.2))
CAR_SCALE=.75;CAR_TX=140.5;CAR_TY=442.5
CAR_TRANSFORM='translate(140.5 442.5) scale(.75)'
def cp(p):return (CAR_TX+CAR_SCALE*p[0],CAR_TY+CAR_SCALE*p[1])
def lid_contact(t,opening=False):
 # Contact on the actual rigid panel, constant local material point while closing.
 u=.88;x=530 if opening else 700
 th=math.radians(trunk_angle(t))
 return cp((562+(x-562)*(1+.20*u),1005+155*u*math.cos(th)-190*u*math.sin(th)))

def actor_pose(t,i):
 q=clock(t);p=b.actor_pose(q,i)
 # Remove V8's abrupt support-foot centroid correction; exact shoe anchors remain.
 base=190+b.drag(q)+95*b.ease(q,1.57,2.25)-70*b.ease(q,5.95,6.30) if i==0 else 600+b.drag(q)-35*b.ease(q,1.45,1.85)
 hip=(base,p['hip'][1]);angle=p['angle']
 if i==0 and t>6.2:angle=mix(angle,15-21*ease(t,7.75,8.),ease(t,6.2,6.45))
 if i==1 and t>6.2:
  hip=(base,mix(hip[1],1286+5*ease(t,7.5,7.85),ease(t,6.2,6.45)));angle=mix(angle,-3-9*ease(t,7.5,7.85),ease(t,6.2,6.45))
 if i==1 and q>5.82:
  feet=[]
  for j in (0,1):
   f,on,u=b.foot(5.82,i,j);feet.append((f,True,0.))
  p['feet']=feet
 shoulder=add(hip,rot((0,-125),angle));p.update(hip=hip,shoulder=shoulder,angle=angle,side=rot((1,0),angle))
 return p

def victim_pose(t):
 q=clock(t);v=b.victim_pose(q)
 # Continuous descent into the restaged cavity after clearing its near sill.
 drop=170*ease(q,4.92,5.72)
 for key in ['S','P','back','waist','neck']:v[key]=add(v[key],(0,drop))
 for key in ['shoulders','elbows','hands','hips','knees','feet','grips']:v[key]=[add(p,(0,drop)) for p in v[key]]
 return v

def hand_targets(t,poses,v):
 q=clock(t);hs=b.hand_targets(q,poses,v)
 if 1.60<q<2.50:
  if q<1.82:hs[0][0]=lerp(v['grips'][0],lid_contact(t,True),b.ease(q,1.60,1.82))
  elif q<1.94:hs[0][0]=lid_contact(t,True)
  else:
   # Fixed release material point, then return along a smooth handoff arc.
   th=math.radians(102*b.ease(1.94,1.82,2.42));release=cp((562+(530-562)*(1+.20*.88),1005+155*.88*math.cos(th)-190*.88*math.sin(th)))
   hs[0][0]=lerp(release,v['grips'][0],b.ease(q,1.94,2.50))
 # Withdraw below the mouth, not to V8's hip targets projected over the opening.
 freehands=[[(poses[0]['hip'][0]+25,1338.),(poses[0]['hip'][0]-25,1338.)],[(poses[1]['hip'][0]-10,1338.),(poses[1]['hip'][0]+30,1338.)]]
 for i,j,start,end,anchor in [(0,0,5.72,5.96,v['grips'][0]),(0,1,5.76,6.02,v['back']),(1,0,5.80,6.08,v['waist']),(1,1,5.82,6.12,v['knees'][1])]:
  if q>=start:hs[i][j]=lerp(anchor,freehands[i][j],b.ease(q,start,end))
 if t>=6.7:
  p=poses[1];free=freehands[1][0]
  hs[1][0]=lerp(free,lid_contact(t),ease(t,6.7,6.95))
  if t>=7.5:hs[1][0]=lerp(lid_contact(7.5),free,ease(t,7.5,7.75))
 return hs
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
 shade=ease(trunk_angle(t),5,45);fill='rgb('+','.join(str(round(mix(c,d,shade))) for c,d in zip((41,67,79),(10,23,33)))+')';a.poly(inner,fill,'#385461',3)
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
 ht=head_time(t)
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
 a=Art();rng=random.Random(717);q=clock(t)
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
 a.add(f'<g id="action-state" data-state="{state_at(t)}" data-lid-angle="{trunk_angle(t)}"/>')
 poses=[actor_pose(t,i) for i in (0,1)];v=victim_pose(t);targets=hand_targets(t,poses,v)
 cam=16*ease(t,0,1.5)
 if t<8.:scale=1.08;tx=-42;ty=-240
 else:
  scale=5.1+.18*ease(t,8.,10.);sx,sy=poses[0]['shoulder'];ht=head_time(t)
  tx=mix(430,520,reaction(ht))-scale*(sx+2-cam);ty=860-scale*(sy-72)
 a.add(f'<g id="cinematic-framing" data-shot="{1 if t<8. else 2}" transform="translate({tx},{ty}) scale({scale})"><g transform="translate({-cam},0)">')
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

 a.add(f'<g transform="{CAR_TRANSFORM}">');car_back(a,t);a.add('</g>')
 # Inside/outside split traverses the body head-first. Both use identical pose geometry.
 # No opacity fade; the actual near sill masks only parts that crossed the entry plane.
 entry=mix(320,850,b.ease(q,4.90,5.72))
 a.add(f'<defs><clipPath id="in-entry"><rect x="0" y="0" width="{entry}" height="1920"/></clipPath><clipPath id="out-entry"><rect x="{entry}" y="0" width="{1300-entry}" height="1920"/></clipPath><clipPath id="cavity-clip"><polygon points="365.5,1196.25 759.25,1196.25 796.75,1312.5 324.25,1312.5"/></clipPath></defs>')
 if q>=4.90:
  a.add('<g clip-path="url(#in-entry)"><g clip-path="url(#cavity-clip)">');victim_draw(a,t,v);a.add('</g></g>')
 a.add(f'<g transform="{CAR_TRANSFORM}">');car_front(a);car_lid(a,t);a.add('</g>')
 if q<4.5:
  a.ellipse(v['P'][0],1490,90-30*v['lift'],12-4*v['lift'],'#020a10',extra=f'opacity="{.7-.35*v["lift"]}"')
 for i in [1,0]:
  for p,on,u in poses[i]['feet']:a.ellipse(p[0],GROUND[i]+12,37,9,'#020a10')
  actor_body(a,t,i,poses[i],hide_eyes)
 if q<4.9:victim_draw(a,t,v)
 else:
  a.add('<g clip-path="url(#out-entry)">');victim_draw(a,t,v);a.add('</g>')
 # Forearms reach over the lip; gloves preserve the same contact endpoints as the victim.
 actor_arms(a,t,poses,v,targets)
 # Wet scrape trails disappear only after physical lift-off.
 if .1<q<3.2:
  for f in v['feet']:a.line([(f[0]-32,f[1]+12),(f[0]-6,f[1]+12)],'#627d87',1.5)
 for i in (0,1):
  for f,on,u in poses[i]['feet']:
   if on:a.ellipse(f[0],f[1]+9,28,4,'none','#5c7a84',1,extra='opacity=".3"')
 # Three environmental rain layers; projected close-up rain remains readable.
 if t<8.:
  for layer,count in [(0,180),(1,160),(2,80)]:
   a.add(f'<g opacity="{[.17,.26,.36][layer]}">')
   for j in range(count):
    x=rng.uniform(-100,1200);y=(rng.uniform(-100,2000)+t*[520,760,1120][layer])%2080-80
    a.line([(x,y),(x-4-layer*2,y+18+12*layer)],'#80a6b5',[1,1.4,2][layer])
   a.add('</g>')
 a.add('</g></g>')
 if t>=8.:
  for j in range(110):
   x=rng.uniform(0,1180);y=(rng.uniform(-100,1920)+t*1050)%2100-100
   a.path(f'M{x},{y} l-5 43','none','#6d96a7',1.7,'opacity=".3"')
 a.rect(0,0,1080,1920,'url(#vignette)');a.add('</svg>');return ''.join(a.s)

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
   for j,(p,on,u) in enumerate(actor_pose(t,i)['feet']):
    key=i,j
    if on and key in prev and not prev[key]:hit(t,'wet foot plant',.14,80)
    prev[key]=on
 for when,kind in [(1.65,'trunk opening latch'),(2.25,'open strut stop'),(5.5,'fabric over sill'),(6.2,'body rests inside'),(7.47,'trunk closing thump'),(8.0,'restrained reaction accent')]:hit(when,kind)
 # Distinct short latch click on the exact fully-closed frame (225).
 hit(7.5,'trunk CLOSED latch click',.16,1450,.075)
 moving=(ts>.1)&(ts<3.6);track+=np.convolve(rng.standard_normal(n),np.ones(9)/9,mode='same')*.022*moving
 track*=np.minimum(1,ts/.08)*np.minimum(1,(10-ts)/.15);stereo=np.column_stack((track,np.roll(track,97)*.97));pcm=(np.clip(stereo,-.95,.95)*32767).astype('<i2')
 dest=ROOT/'assets/original_ambience.wav'
 with wave.open(str(dest),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
 (ROOT/'assets/sound-events.json').write_text(json.dumps(events,indent=2));return dest
def main():
 p=argparse.ArgumentParser();p.add_argument('--scale',type=float,default=.5);p.add_argument('--fps',type=int,default=30);p.add_argument('--out',default='previews/V9_preview_01.mp4');p.add_argument('--stills',action='store_true');p.add_argument('--hide-eyes',action='store_true');args=p.parse_args()
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
