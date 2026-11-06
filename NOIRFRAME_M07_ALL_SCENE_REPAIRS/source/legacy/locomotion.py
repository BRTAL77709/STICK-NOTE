"""Explicit per-foot contacts for a supplied floor route; no rotating-leg loop."""
from contact_rig import *
def ground_feet(t,path,heading,schedule,initial):
 feet=[]
 for j in range(2):
  start=np.array(initial[j]);h0=0.;f={'sole':start,'heading':h0,'pitch':0,'planted':True}
  for a,b,leg in schedule:
   if leg!=j:continue
   angle=float(heading(b));end=path(b)+RY(angle)@V((.09,-.09)[j],-path(b)[1],.035)
   if t<a:break
   u=Q(t,a,b);f={'sole':mix(start,end,u)+V(0,.10*math.sin(math.pi*clamp((t-a)/(b-a)))**2,0),'heading':h0+(angle-h0)*u,'pitch':.1*math.sin(math.pi*clamp((t-a)/(b-a)))**2,'planted':t>=b}
   if t<b:break
   f.update(sole=end,pitch=0,heading=angle,planted=True);start=end;h0=angle
  feet.append(foot_geometry(f))
 return feet
