"""Independent native Blender dependency-graph sampling at 120Hz; actual evaluated shoe vertices."""
import bpy,sys,json,math,numpy as np,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));import actions
model=R/'blender/STAIRS_M11R01.blend';bpy.ops.wm.open_mainfile(filepath=str(model));sc=bpy.context.scene;rig=bpy.data.objects['M04_WITNESS_RIG'];anchors={};drift=distance=penetration=length=gap=0.;rows=[];roots=[]
def terrain(x,z):
 if .55<=x<=1.55 and 1.5<=z<5.25:return (math.floor((z-1.5)/.25)+1)*actions.RISE
 if z>=5.25 or x<.3:return 2.6
 return 0.
for i in range(round(actions.DURATIONS['STAIRS']*120)):
 t=i/120;f=t*30;sc.frame_set(math.floor(f),subframe=f-math.floor(f));bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();r=rig.evaluated_get(dep);state=actions.stairs(t);roots.append(np.array(r.matrix_world@r.pose.bones['root'].head));row={'time_s':t,'feet':{}}
 for side,j in [('L',1),('R',0)]:
  ob=bpy.data.objects['SHOE_'+side];e=ob.evaluated_get(dep);m=e.to_mesh();vv=np.array([tuple(e.matrix_world@v.co) for v in m.vertices]);e.to_mesh_clear();sole=vv[[0,1,5,6]];planted=state['pose']['legs'][j]['planted']
  if planted:
   if side not in anchors:anchors[side]=sole.copy()
   drift=max(drift,float(np.linalg.norm(sole-anchors[side],axis=1).max()));distance=max(distance,float(np.abs(sole[:,2]-state['pose']['legs'][j]['sole'][1]).max()))
  else:anchors.pop(side,None)
  for q in vv:penetration=max(penetration,terrain(q[1],q[0])-q[2])
  row['feet'][side]={'stance':planted,'sole_center_blender_m':sole.mean(0).tolist()}
  for pref,want in [('thigh.',.37),('shin.',.37),('upper_arm.',.34),('forearm.',.34)]:b=r.pose.bones[pref+side];length=max(length,abs((b.tail-b.head).length-want))
  for a,b in [('thigh.','shin.'),('shin.','foot.'),('upper_arm.','forearm.'),('forearm.','hand.')]:gap=max(gap,(r.pose.bones[a+side].tail-r.pose.bones[b+side].head).length)
 rows.append(row)
roots=np.array(roots);step=np.linalg.norm(np.diff(roots,axis=0),axis=1);report={'source_blend':str(model.relative_to(R)),'source_blend_sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'samples':len(rows),'frequency_Hz':120,'units':'metres; Blender XYZ = renderer ZXY','stance_mesh_drift_m':drift,'sole_to_target_tread_m':distance,'maximum_sampled_stair_penetration_m':max(0,float(penetration)),'limb_length_variation_m':length,'connected_bone_gap_m':gap,'root_height_gain_m':float(roots[-1,2]-roots[0,2]),'max_root_120Hz_displacement_m':float(step.max()),'tolerances':{'contact_drift_m':.0015,'tread_m':.0015,'penetration_m':.0015,'limb_m':.0001,'bone_gap_m':.0001},'technical_status':'TECHNICAL PASS' if drift<.0015 and distance<.0015 and penetration<.0015 and length<.0001 and gap<.0001 else 'TECHNICAL FAIL','scope':'Actual native shoes/bones. Shared 15-tread terrain. Not a force-based balance simulation or universal body collision certification.','samples_per_foot':rows};(R/'reports/STAIRS_NATIVE_120HZ.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!='samples_per_foot'})
