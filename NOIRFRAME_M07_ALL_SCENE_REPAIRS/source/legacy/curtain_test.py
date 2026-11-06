"""Pinned-ring fabric fold rig: horizontal material arc length preserved, no rigid blinds."""
from contact_rig import *
DURATION=5.;NC=48;NR=10;MATERIAL_WIDTH=1.60

def fabric(t):
 grid=[]
 for row in range(NR+1):
  v=row/NR;delay=.10*abs(v-.5);pull=Q(t-delay,1.45,3.12);width=1.40-1.08*pull
  if t>4.10:width+=.014*math.exp(-(t-4.10)*3.0)*math.sin((t-4.10)*8.)
  u=np.linspace(0,1,NC+1);dx=width/NC;wave=np.sin(u*8*math.pi);lo=0.;hi=.25
  for _ in range(26):
   amp=(lo+hi)/2;length=np.sqrt(dx*dx+(amp*np.diff(wave))**2).sum()
   if length<MATERIAL_WIDTH:lo=amp
   else:hi=amp
  amp=(lo+hi)/2;ys=2.15-1.55*v+.018*np.sin(math.pi*u)*v;grid.append(np.stack([-.70+u*width,ys,amp*wave-.035],axis=1))
 return np.array(grid)
def state(t):
 mesh=fabric(t);edge=mesh[5,-1];root=V(.20-.31*Q(t,1.50,3.15),.64-.025*Q(t,1.3,1.6)+.025*Q(t,3.3,3.8),-.36-.08*Q(t,3.45,3.9));ff=[foot_geometry({'sole':V(.19,0,-.42),'planted':True,'pitch':0,'heading':0}),foot_geometry({'sole':V(-.07,0,-.28),'planted':True,'pitch':0,'heading':0})];normal=V(0,0,-1);target=edge+normal*.050;rest=root+V(.19,.16,.10);grip=mix(rest,target,Q(t,.55,1.32)*(1-Q(t,4.05,4.40)));other=root+V(-.18,.15,.12);pitch=.04*(Q(t,1.,1.45)-Q(t,3.35,3.65))-.10*Q(t,3.45,3.95);roll=-.055*Q(t,1.8,3.1)+.055*Q(t,3.45,4.0);fear=.2+.75*Q(t,3.32,3.90);look=.85-1.25*Q(t,3.45,4.10)
 p=pose(root,ff,[grip,other],heading=0,pitch=pitch,roll=roll,pelvis_roll=-.6*roll,twist=-.09*Q(t,1.8,3.),look=look,fear=fear,head_lag=-.025*Q(t,3.5,3.9),knee_forward=V(0,.08,1));p['head_forward']=RY(2.60*Q(t,3.45,4.10))@V(0,0,1);fg=[[],[]];contact=1.32<=t<=4.05
 close=Q(t,1.05,1.32)*(1-Q(t,4.05,4.40));free=[V(.022,.030,.015),V(-.012,-.025,.020)];held=[V(0,.015,.050),V(0,-.015,.050)];pads=[grip+mix(a,b,close) for a,b in zip(free,held)];fg[0]=fingers(grip,pads,V(0,-1,-1),[normal]*2)
 return {'time':t,'pose':p,'fingers':fg,'hand_frames':[None,None],'fabric':mesh,'grip':edge,'grip_contact':contact,'support':['L','R'],'phase':'reach' if t<1.32 else 'grip / pull' if t<3.12 else 'reveal / freeze' if t<3.45 else 'frightened reaction' if t<4.05 else 'release / fabric settle','sedan_position':V(-4.,-2.6,5.2),'fabric_material_width':MATERIAL_WIDTH,'reaction':fear}
