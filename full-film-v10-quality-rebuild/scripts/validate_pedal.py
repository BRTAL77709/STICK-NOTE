import sys,math,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'));from driving import pedal_pose
errors=[];contacts=[];radii=[];heels=[];angles=[]
for k in range(121):
 p=pedal_pose(28+k/30);errors += [abs(math.dist(p['heel'],p['toe'])-430),abs(math.dist(p['hip'],p['knee'])-620),abs(math.dist(p['knee'],p['ankle'])-620)];radii.append(p['pedal_contact_radius']);th=p['pedal_angle'];h=p['hinge'];toe=p['toe'];contacts.append(abs((toe[0]-h[0])*math.cos(th)+(toe[1]-h[1])*math.sin(th)));heels.append(p['heel']);angles.append(p['foot_angle'])
assert max(errors)<1e-6 and max(contacts)<1e-6 and min(radii)>=105 and max(radii)<=445 and len(set(heels))==1
out={'samples':121,'max_rigid_foot_and_leg_segment_error_px':max(errors),'max_pedal_plane_contact_error_px':max(contacts),'heel_fixed':heels[0],'pedal_contact_radius_range':[min(radii),max(radii)],'shoe_rotation_degrees':math.degrees(max(angles)-min(angles)),'shared_driver':'motion_state.throttle','artistic_approval':'not inferred'};(R/'reports/pedal-contact-validation.json').write_text(json.dumps(out,indent=2));print(out)
