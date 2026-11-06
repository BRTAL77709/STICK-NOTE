"""Fresh evaluation of delivered M04 source, without modifying it or its reports."""
import bpy,math,json,gzip,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];old=R.parent/'NOIRFRAME_M04';bpy.ops.wm.open_mainfile(filepath=str(old/'assets/STAIRCASE_M04_R06.blend'));cache=json.load(gzip.open(old/'assets/EVALUATED_R06.json.gz','rt'));scene=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];maxdiff=drift=distance=length=gap=0.;anchors={};TREADS=[([-1.2,0],[-.5,.5],0),([0,.3],[-.45,.45],.18),([.3,.6],[-.45,.45],.36),([.6,1.6],[-.45,.45],.54)]
for i in range(601):
 t=i/120;f=t*30;j=math.floor(f);scene.frame_set(j,subframe=f-j);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();expected=cache['dense'][i]
 for s in ['L','R']:
  o=bpy.data.objects['SHOE_'+s];ev=o.evaluated_get(dep);m=ev.to_mesh();v=np.array([list(ev.matrix_world@q.co) for q in m.vertices]);ev.to_mesh_clear();maxdiff=max(maxdiff,float(np.abs(v-np.array(expected['feet'][s]['vertices'])).max()));meta=expected['feet'][s]['target'];ids=[1,6] if meta['contact_mode']=='TOE' else [0,1,5,6]
  if meta['planted']:
   if s not in anchors:anchors[s]=v.copy()
   drift=max(drift,float(np.linalg.norm(v[ids]-anchors[s][ids],axis=1).max()));xr,yr,z=TREADS[meta['tread']]
   for q in v[ids]:closest=np.array([np.clip(q[0],*xr),np.clip(q[1],*yr),z]);distance=max(distance,float(np.linalg.norm(q-closest)))
  else:anchors.pop(s,None)
  for pref,want in [('thigh.',.37),('shin.',.37),('upper_arm.',.34),('forearm.',.34)]:b=rig.pose.bones[pref+s];length=max(length,abs((b.tail-b.head).length-want))
  for a,b in [('thigh.','shin.'),('shin.','foot.'),('upper_arm.','forearm.'),('forearm.','hand.')]:gap=max(gap,(rig.pose.bones[a+s].tail-rig.pose.bones[b+s].head).length)
cons=[c for b in rig.pose.bones for c in b.constraints if c.type=='IK'];assert len(cons)==2 and all(c.chain_count==2 and not c.use_stretch for c in cons);assert maxdiff<1e-7
report={'fresh_native_evaluations':601,'sample_rate_hz':120,'native_two_bone_leg_IK_constraints':len(cons),'native_vs_stored_shoe_vertex_max_error_m':maxdiff,'actual_stance_drift_m':drift,'actual_foot_tread_distance_m':distance,'actual_limb_length_variation_m':length,'actual_connected_gap_m':gap,'pass':drift<.001 and distance<.001 and length<.0001 and gap<.0001,'artistic_approval':'NOT GRANTED'};(R/'reports/BASELINE_NATIVE_RECHECK.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
