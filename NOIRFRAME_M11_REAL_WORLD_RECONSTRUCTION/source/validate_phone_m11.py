from bootstrap import ROOT as R
import json,gzip,numpy as np
from render_clips import Q
selected=json.loads((R/'configuration/selected_native.json').read_text());out={}
for shot in ['PHONE_CALL','UNKNOWN_CALLER']:
 data=json.load(gzip.open(R/'scenes'/f'{shot}_{selected[shot]}.json.gz','rt'));pad=surface=grip=0.;headgap=100.;tablegap=[];n=0
 for i,(f,s) in enumerate(zip(data['frames'],data['state'])):
  center=np.array(s['phone_position']);rot=np.array(s['phone_R']);points=np.array([center+rot@np.array([x,y,z]) for z in [-.012,.012] for x,y in [(-.039,-.08),(.039,-.08),(.039,.08),(-.039,.08)]]);head=Q(f['bones']['head']['head']);headgap=min(headgap,float(np.linalg.norm(points-head,axis=1).min())-.22)
  if shot=='PHONE_CALL' and i/30<=2.3:tablegap.append(float(points[:,1].min()-.72))
  if s['phone_contact']:
   grip=max(grip,float(np.linalg.norm(Q(f['bones']['hand.R']['head'])-s['phone_grip'])))
   for j,target in enumerate(s['fingers'][0]):
    p=Q(f['bones'][f'digit{j}b.R']['tail'])-np.array(target['normal'])*target['tip_radius'];pad=max(pad,float(np.linalg.norm(p-target['pad'])));local=rot.T@(p-center);surface=max(surface,abs(float(local[2]+.014)));n+=1
 out[shot]={'native_revision':selected[shot],'native_contact_samples':n,'actual_native_fingertip_proxy_to_authored_glass_pad_m':pad,'actual_native_contact_point_to_glass_plane_m':surface,'actual_native_wrist_grip_frame_error_m':grip,'minimum_phone_vertex_to_head_sphere_clearance_m':headgap,'table_contact_gap_range_m':[min(tablegap),max(tablegap)] if tablegap else None,'contact_tolerance_m':.002,'technical_status':'TECHNICAL PASS' if pad<.002 and surface<.002 and grip<.0015 and (not tablegap or max(abs(x) for x in tablegap)<.0015) else 'TECHNICAL FAIL','scope':'Actual evaluated distal bones with authored 7mm rounded tip proxy versus actual phone glass plane. Head clearance uses explicit .22m envelope, not volumetric face collision. No friction simulation.'}
(R/'reports/PHONE_CONTACT_VALIDATION.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
