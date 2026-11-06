"""View-conditioned morph of the approved head; no volumetric facial-physics claim."""
import math,numpy as np
from approved_head_view import head

def draw(a,t,pose,cam,center):
 F=np.array(pose.get('head_forward',np.array(pose['torso_basis'])@np.array([0,0,1.])),float);F[1]=0;F/=max(1e-12,np.linalg.norm(F));V=np.array(cam.eye)-center;V[1]=0;V/=max(1e-12,np.linalg.norm(V));cos=float(np.clip(F@V,-1,1));sign=1 if F@np.array(cam.right)>=0 else -1
 u=float(np.clip(-cos/.85,0,1));back=u*u*(3-2*u);yaw=sign*math.sqrt(max(0,1-cos*cos))*(1-back);opacity=max(0,1-3*back)
 head(a,0,0,t,yaw,.25,pose.get('fear',.6),0,blink_override=max(0,1-abs(t-1.45)/.065),feature_opacity=opacity,backstrap=back)
