"""Sampled native body vertices against actual jamb and solid door-leaf volumes."""
import json,gzip,numpy as np
from bootstrap import ROOT as R
results={}
for shot in ['KEY_LOCK','DOOR_ENTRY']:
 data=json.load(gzip.open(R/'scenes'/f'{shot}_{json.loads((R/"reports/SHOT_REVISIONS.json").read_text())[shot]}.json.gz','rt'));worst=0.;hit=None
 for f,d in zip(data['frames'],data['state']):
  mat=np.array(d['door_R']);H=np.array([.45,0,0])
  for name,vv in f['meshes'].items():
   if name=='APPROVED_HEAD_CARD' or name.startswith('M07_digit') or name.startswith('MITTEN'):continue
   points=np.array([[p[1],p[2],p[0]] for p in vv]);local=(points-H)@mat
   for p,q in zip(points,local):
    pen=0
    for x0,x1 in [(-.54,-.45),(.45,.54)]:
     if x0<p[0]<x1 and 0<p[1]<2.18 and -.10<p[2]<.10:pen=max(pen,min(p[0]-x0,x1-p[0],p[1],2.18-p[1],p[2]+.10,.10-p[2]))
    if -.9<q[0]<0 and 0<q[1]<2.1 and abs(q[2])<.065:
     if not (-.785<q[0]<-.715 and 1.125<q[1]<1.195):pen=max(pen,min(q[0]+.9,-q[0],q[1],2.1-q[1],.065-abs(q[2])))
    if pen>worst:worst=float(pen);hit={'time_s':f['time'],'mesh':name,'point':p.tolist()}
 results[shot]={'sampled_body_vertex_door_or_jamb_penetration_m':worst,'worst':hit,'scope':'Every visible body mesh vertex at30Hz except transparent head card and intentionally contacting mittens/digits. No edge, continuous swept-volume or full hand mesh collision certification.','status':'TECHNICAL PASS' if worst<.005 else 'TECHNICAL FAIL','tolerance_m':.005}
(R/'reports/DOOR_BODY_COLLISION_CHECK.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
