"""Projection invariance and sampled culling image equivalence, not full camera collision certification."""
import numpy as np,json
from bootstrap import ROOT as R
import actions,sets,render_clips as render,vehicle_system as VS
from cameras import camera
from world import Camera
from contact_rig import V,RY
from fast_depth import FastDepth
error=0.;rows=[];fn=sets.in_view
for shot,t in [('DRIVING_COCKPIT',0),('DRIVING_COCKPIT',3.5),('CAR_EXIT_RUNNING',4),('ROAD_BUILDINGS',3),('CAR_CHASE',1),('CAR_CHASE',8)]:
 d=actions.state(shot,t);c=camera(shot,t,d)
 if shot=='DRIVING_COCKPIT':
  o=d['position'];M=RY(d['yaw']);pivot=V(0,.55,0);RR=M@actions.RZ(d['roll'])@actions.RX(d['pitch']);forward=lambda p:o+M@pivot+RR@(p-pivot);gc=Camera(forward(c.eye),forward(c.target),c.focal,up=RR@c.up)
  for x,y,z in [(-1,-1,3),(1,1,4),(0,0,8)]:
   p=c.eye+c.forward*z+c.right*x+c.up*y;error=max(error,float(np.linalg.norm(np.array(c(p))-gc(forward(p)))))
 raster=FastDepth(270);sets.in_view=lambda *a:True;unculled=np.array(raster.render(render.scene(shot,t,d)));sets.in_view=fn;culled=np.array(raster.render(render.scene(shot,t,d)));diff=np.abs(unculled.astype(int)-culled.astype(int));rows.append({'shot':shot,'time_s':t,'different_pixels':int(np.any(diff,axis=2).sum()),'max_channel_difference':int(diff.max())});print(rows[-1],flush=True)
sets.in_view=fn
out={'driver_local_world_projection_max_error_px':error,'projection_tolerance_px':1e-6,'sampled_culling_comparisons':rows,'technical_status':'TECHNICAL PASS' if error<1e-6 and all(q['different_pixels']==0 for q in rows) else 'TECHNICAL FAIL','limits':'Six environment-only rendered samples270px; not continuous full-resolution culling/camera collision certification.'};(R/'reports/CAMERA_SPACE_VALIDATION.json').write_text(json.dumps(out,indent=2))
