"""Independent measurements of Blender-evaluated bones/mesh vertices, not planned markers."""
from pathlib import Path
import gzip,json,numpy as np,math,csv,argparse
R=Path(__file__).resolve().parents[1]
TREADS={0:([-1.2,0],[-.5,.5],0),1:([0,.3],[-.45,.45],.18),2:([.3,.6],[-.45,.45],.36),3:([.6,1.6],[-.45,.45],.54)}
def rectangle_distance(p,tread):
 xr,yr,z=TREADS[tread];q=np.array([np.clip(p[0],*xr),np.clip(p[1],*yr),z]);return float(np.linalg.norm(np.array(p)-q))
def run(tag):
 d=json.load(gzip.open(R/'assets'/f'EVALUATED_{tag}.json.gz','rt'));global TREADS;TREADS={}
 for i,name in enumerate(['LOWER_FLOOR','TREAD_1','TREAD_2','TREAD_3_LANDING']):
  vv=np.array(d['meshes'][name]['rest_vertices']);TREADS[i]=([float(vv[:,0].min()),float(vv[:,0].max())],[float(vv[:,1].min()),float(vv[:,1].max())],float(vv[:,2].max()))
 drift=distance=bonevar=jointgap=ankerr=0.;anchors={};rows=[];knee_angles=[];root=[];modes={}
 for f in d['dense']:
  bones=f['bones'];root.append(bones['root']['head'])
  for side in ['L','R']:
   q=f['feet'][side];target=q['target'];v=np.array(q['vertices']);mode=target['contact_mode'];contact=v[q['toe_indices'] if mode=='TOE' else q['sole_indices']];key=side
   if target['planted']:
    if key not in anchors:anchors[key]=v.copy()
    ids=q['toe_indices'] if mode=='TOE' else q['sole_indices'];current=float(np.linalg.norm(contact-anchors[key][ids],axis=1).max());drift=max(drift,current);dist=max(rectangle_distance(p,target['tread']) for p in contact);distance=max(distance,dist)
   else:current=dist=0.;anchors.pop(side,None)
   modes[side]=mode;ankerr=max(ankerr,float(np.linalg.norm(np.array(bones['shin.'+side]['tail'])-q['ankle_target'])))
   hip=np.array(bones['thigh.'+side]['head']);knee=np.array(bones['thigh.'+side]['tail']);ank=np.array(bones['shin.'+side]['tail']);a=hip-knee;b=ank-knee;flex=180-math.degrees(math.acos(np.clip(a@b/(np.linalg.norm(a)*np.linalg.norm(b)),-1,1)));knee_angles.append(flex)
   for name,expected in [('thigh',.37),('shin',.37),('upper_arm',.34),('forearm',.34)]:
    bone=bones[name+'.'+side];bonevar=max(bonevar,abs(np.linalg.norm(np.array(bone['tail'])-bone['head'])-expected))
   for a,b in [('thigh','shin'),('shin','foot'),('upper_arm','forearm'),('forearm','hand')]:jointgap=max(jointgap,float(np.linalg.norm(np.array(bones[a+'.'+side]['tail'])-bones[b+'.'+side]['head'])))
   rows.append({'time_s':f['time'],'side':side,'mode':mode,'tread':target['tread'],'actual_stance_drift_m':current if target['planted'] else '', 'actual_contact_distance_m':dist if target['planted'] else '', 'knee_flexion_deg':flex,'ankle_target_error_m':float(np.linalg.norm(ank-q['ankle_target']))})
 root=np.array(root);vel=np.diff(root,axis=0)*120;acc=np.diff(vel,axis=0)*120;normal=np.array([f['bones']['root']['head'] for f in d['frames']]);times=np.array([f['time'] for f in d['dense']]);vels=np.gradient(root,times,axis=0);jump=0.
 for probe in d['root_key_probes']:
  velocity=np.array([np.interp(probe['time'],times,vels[:,j]) for j in range(3)]);gap=np.array(probe['after'])-probe['before'];jump=max(jump,float(np.linalg.norm(gap-2e-5*velocity)))
 mutation=d['ik_mutation'];mutdelta=float(np.linalg.norm(np.array(mutation['baseline']['feet']['L']['vertices'])-mutation['disabled_left_IK']['feet']['L']['vertices'],axis=1).max())
 # Collision checks against actual exported tread/ground solids, on evaluated mesh vertices.
 penetration=0.;worst=None
 for f in d['frames']:
  for name,verts in f['meshes'].items():
   if name=='APPROVED_HEAD_CARD':continue
   for p in verts:
    for idx,(xr,yr,z) in TREADS.items():
     if xr[0]+1e-6<p[0]<xr[1]-1e-6 and yr[0]<p[1]<yr[1] and p[2]<z-1e-6:
      depth=min(z-p[2],p[0]-xr[0],xr[1]-p[0],p[1]-yr[0],yr[1]-p[1]);
      if depth>penetration:penetration=depth;worst={'time':f['time'],'mesh':name,'point':p,'tread':idx}
 # Edge/riser intersections complement vertex tests; all points come from evaluated meshes.
 edge_pen=0.;edge_worst=None
 for f in d['frames']:
  for name,mesh in d['meshes'].items():
   if not mesh['bound_to_armature'] or name=='APPROVED_HEAD_CARD':continue
   verts=np.array(f['meshes'][name]);edges={tuple(sorted([a,b])) for face in mesh['faces'] for a,b in zip(face,face[1:]+face[:1])}
   for a,b in edges:
    pa=verts[a];pb=verts[b]
    for idx,(xr,yr,h) in TREADS.items():
     if idx==0:continue
     rx=xr[0]
     if min(pa[0],pb[0])+1e-8<rx<max(pa[0],pb[0])-1e-8:
      q=pa+(pb-pa)*(rx-pa[0])/(pb[0]-pa[0]);pen=h-q[2]
      if yr[0]<q[1]<yr[1] and pen>edge_pen:edge_pen=float(pen);edge_worst={'time':f['time'],'mesh':name,'riser':idx,'point':q.tolist()}
 result={'units':'metres, seconds, degrees; Blender Z up','sample_rate_hz':120,'render_fps':30,'stance_contact_definition':'FLAT: four evaluated sole vertices; TOE: two evaluated front sole vertices. Heel lift during TOE is intended rotation, not sliding.','max_stance_contact_drift_m':drift,'max_foot_to_tread_distance_m':distance,'max_limb_length_variation_m':bonevar,'max_connected_joint_gap_m':jointgap,'max_native_IK_target_error_m':ankerr,'max_root_frame_displacement_m':float(np.linalg.norm(np.diff(normal,axis=0),axis=1).max()),'max_root_key_limit_residual_m':jump,'peak_root_speed_m_s':float(np.linalg.norm(vel,axis=1).max()),'peak_root_acceleration_m_s2':float(np.linalg.norm(acc,axis=1).max()),'knee_flexion_range_deg':[min(knee_angles),max(knee_angles)],'max_mesh_edge_riser_penetration_m':edge_pen,'worst_edge_penetration':edge_worst,'max_sampled_mesh_stair_penetration_m':penetration,'worst_sampled_penetration':worst,'IK_disable_changes_bound_shoe_m':mutdelta,'tolerances':{'stance_drift_m':.001,'foot_tread_distance_m':.001,'limb_variation_m':.0001,'connected_joint_gap_m':.0001,'root_key_limit_residual_m':.00001,'root_frame_displacement_m':.035,'sampled_penetration_m':.001},'visual_approval':'PENDING USER REVIEW'}
 result['required_numeric_checks_pass']=bool(drift<.001 and distance<.001 and bonevar<.0001 and jointgap<.0001 and jump<.00001 and result['max_root_frame_displacement_m']<.035 and penetration<.001 and edge_pen<.001 and mutdelta>.01)
 (R/'reports'/f'VALIDATION_{tag}.json').write_text(json.dumps(result,indent=2))
 with (R/'reports'/f'CONTACTS_{tag}.csv').open('w') as fp:w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps(result,indent=2));return result
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--tag',default='R04');a=p.parse_args();run(a.tag)
