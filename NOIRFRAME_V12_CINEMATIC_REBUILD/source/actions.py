"""V12 authored staging and asymmetrical timing; contact math retained where valid.
The V11 screens/affine cameras are not imported. SI XYZ, Y up throughout.
"""
from rig import *
from vendor import v11_contacts as contact
DURATIONS={'HOUSE':13.,'STAIRS':9.4,'BEDROOM':8.4,'DRIVING':12.}
# Vary each landing's duration: anxious start, midflight effort, landing deceleration.
S_KNOTS=[(0,0),(.48,.4),(1.03,.98),(1.58,1.56),(2.13,2.14),(2.75,2.72),(3.37,3.30),(4.05,3.88),(4.69,4.46),(5.25,5.04),(5.82,5.62),(6.43,6.20),(7.09,6.78),(7.80,7.36),(8.45,7.75),(9.4,8.5)]
def warp(t,rows):
 for (a,x),(b,y) in zip(rows,rows[1:]):
  if t<=b:return x+(y-x)*clamp((t-a)/(b-a))
 return rows[-1][1]
def stairs(t):
 u=warp(t,S_KNOTS);d=contact.stairs(u);p=d['pose'];r=p['root'].copy();effort=E(t,.25,.65)*(1-E(t,7.8,8.5));r[2]+=.009*math.sin(t*4.6)*effort;r[1]-=.009*(.5+.5*math.sin(t*7.3))*effort
 hands=[q['wrist'] for q in p['arms']];p=skeleton(r,p['legs'],hands,.10*effort+.008*math.sin(t*4.2-.5),.76-.16*E(t,7.7,8.3),.45+.25*E(t,6,8),head_tilt=-4*math.sin(t*2.2),head_lead=.025*math.sin(t*4.3-.7),breath=.008*math.sin(t*5.3));d.update(pose=p,time=t,contact_time=u);return d
H_RUN_INITIAL=[(-.88,0,-.53),(-.68,0,-.37)]
H_RUN_PLANS=[[(.06,.39,(-.30,0,-.53),.16),(.83,1.17,(.40,0,-.53),.15),(1.69,2.06,(1.20,0,-.53),.12)],[(.43,.78,(.05,0,-.37),.17),(1.21,1.60,(.80,0,-.37),.14),(2.10,2.56,(1.40,0,-.37),.09)]]
def house(t):
 u=max(0,t-2);d=contact.house(u);d['contact_time']=u;d['time']=t
 if t<3.3:
  # A genuine approach from farther along the path, then loading/deceleration.
  if t<2.65:
   ff=feet(t,H_RUN_INITIAL,H_RUN_PLANS);x=float(keys(t,[(0,-.76),(.4,-.48),(.80,-.12),(1.2,.27),(1.65,.65),(2.12,1.04),(2.65,1.25)]));r=V(x,.65+.012*math.sin(t*12)*(1-E(t,2.1,2.65)),-.45);lean=.16*(1-E(t,2.0,2.65));hands=[r+V(.18+.15*math.sin(t*8.2+j*math.pi),.20+.06*math.cos(t*8.2+j*math.pi),(-.04,.04)[j]) for j in range(2)];p=skeleton(r,ff,hands,lean,.78,.58,head_tilt=-3*math.sin(t*4),breath=.008*math.sin(t*9));d['pose']=p;d['phase']='run, decelerate and plant'
  else:
   # Align completed run to the unchanged locked-door support stance.
   d=contact.house(1.3);d.update(time=t,contact_time=1.3)
 return d

def bedroom(t):
 u=warp(t,[(0,0),(1.3,1.5),(2.35,2.4),(2.65,2.65),(4.45,4.4),(5.3,5.05),(6.55,6.2),(8.4,7.5)]);d=contact.window(u);d.update(time=t,contact_time=u);return d

# Bicycle model in road XZ: actual metres/s, integrated speed and wheel distance.
DT=1/30;WHEEL_RADIUS=.30;WHEELBASE=2.65
DRIVE=[];x=0.;z=0.;yaw=0.;distance=0.;speed=5.
for f in range(361):
 t=f/30;acc=2.1*(1-E(t,3.0,3.6))-3.0*(E(t,8,8.4)-E(t,10,10.4))+.75*E(t,10.4,11)
 steer=.055*(E(t,3.1,3.6)-E(t,5.4,6.0))-.035*(E(t,6.2,6.7)-E(t,7.2,7.7));speed=max(1.8,speed+acc*DT);yaw+=speed/WHEELBASE*math.tan(steer)*DT;x+=math.sin(yaw)*speed*DT;z+=math.cos(yaw)*speed*DT;distance+=speed*DT
 DRIVE.append({'time':t,'position':[x,0,z],'speed_mps':speed,'speed_kmh':speed*3.6,'acceleration':acc,'steer':steer,'yaw':yaw,'wheel_angle':distance/WHEEL_RADIUS,'distance':distance,'body_roll':-.09*speed*speed/WHEELBASE*math.tan(steer),'throttle':clamp(acc/2.1),'brake':clamp(-acc/3),'gap':18-7*E(t,1,8)+4*E(t,9,12)})
def driving(t):
 d=dict(DRIVE[min(360,round(t*30))]);lag=max(0,t-.65);k=DRIVE[min(360,round(lag*30))];gap=d['gap'];q=np.array(d['position'])-V(math.sin(d['yaw']),0,math.cos(d['yaw']))*gap;d['pursuer_position']=q.tolist();d['phase']='accelerate' if t<3.1 else 'steer through bend' if t<8 else 'brake, check mirror and recover';return d
STATES={'HOUSE':house,'STAIRS':stairs,'BEDROOM':bedroom,'DRIVING':driving}
