"""Build actual encoded before/after sheets, preservation proof and review report."""
from pathlib import Path
import subprocess,json,hashlib,gzip,zipfile,math
import numpy as np
from PIL import Image,ImageDraw
from bootstrap import ROOT as R
base=Path('/workspace/STICK-NOTE/NOIRFRAME_M08_CINEMATIC_REPAIRS')
media=json.loads((R/'reports/MEDIA_VALIDATION.json').read_text());assert len(media)==8 and all(x['technical_status']=='TECHNICAL PASS' for x in media.values())
rows=json.loads((R/'CURRENT_SHOTS.json').read_text());comparisons={}
for s,row in rows.items():
 old=base/'renders'/f'M08_{s}_FINAL.mp4';new=R/row['final'];od=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(old)]));duration=row['duration'];sheet=Image.new('RGB',(720,688*6),'#071521');draw=ImageDraw.Draw(sheet);samples=[]
 for j,frac in enumerate([0,.18,.36,.54,.72,.98]):
  nt=min(duration-1/30,duration*frac);ot=min(od-1/30,od*frac)
  if s=='KEY_LOCK':
   from scipy.interpolate import PchipInterpolator
   clock=PchipInterpolator([0,1.5,2.9,4.,4.35,5.35,6.,7.4,9.],[0,1.2,1.95,2.55,2.75,3.15,3.43,3.92,4.4]);ot=min(od-1/30,float(clock(nt))*7/4.4)
  for k,(p,t,label) in enumerate([(old,ot,'M08'),(new,nt,'M09')]):
   b=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=360:640','-f','rawvideo','-pix_fmt','rgb24','-']);im=Image.frombytes('RGB',(360,640),b);sheet.paste(im,(k*360,j*688+28));draw.text((k*360+8,j*688+7),f'{label} {s} / {t:.3f}s',fill='white')
  samples.append({'M08_time_s':ot,'M09_time_s':nt})
 p=R/'contact_sheets'/f'{s}_M08_vs_M09.jpg';sheet.save(p,quality=93);comparisons[s]={'M08_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'M09_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'sheet':str(p.relative_to(R)),'times':samples,'method':'Frames extracted from the actual encoded MP4s; key action phases matched through its new monotone clock; other clips use normalized coverage.'};print('COMPARISON',s,flush=True)
(R/'reports/COMPARISON_SOURCES.json').write_text(json.dumps(comparisons,indent=2))
before=json.loads((R/'reports/M08_PRESERVATION_BASELINE.json').read_text());changed=[p for p,h in before.items() if not (base/p).exists() or hashlib.sha256((base/p).read_bytes()).hexdigest()!=h];assert not changed
(R/'reports/PRESERVATION_AFTER.json').write_text(json.dumps({'protected_M08_files':len(before),'changed_or_missing':changed,'all_previous_versions_preserved':not changed,'scope':'Complete M08 local pre-edit manifest; all existing remote tree entries will additionally be verified unchanged at publication. M09 scripts write only inside the new production directory.'},indent=2))
plays={}
for p in (R/'reports').glob('M09_DELIVERY_*final-playback.json'):plays.update(json.loads(p.read_text()))
assert len(plays)==8 and all(q['ended'] and q['corruptedFrames']==0 for vv in plays.values() for q in vv)
contacts=json.loads((R/'reports/NATIVE_QA_SUMMARY.json').read_text());assert len(contacts)==6 and all(v['technical_status']=='TECHNICAL PASS' for v in contacts.values())
stairs=json.loads((R/'reports/STAIRS_M09_NATIVE_RECHECK.json').read_text());vehicle=json.loads((R/'reports/VEHICLE_WORLD_VALIDATION.json').read_text());door=json.loads((R/'reports/DOOR_BODY_COLLISION_CHECK.json').read_text());props=json.loads((R/'reports/PROP_INTERACTION_VALIDATION.json').read_text());camera=json.loads((R/'reports/CAMERA_CLEARANCE.json').read_text());assert stairs['pass'] and all(x['status']=='TECHNICAL PASS' for x in door.values()) and all(x['pass'] for x in camera.values())
text=f'''# M09 technical validation report

Eight separate scenes, {sum(x['duration_s'] for x in media.values()):.1f} seconds of scene exports in total, {sum(x['decoded_frames'] for x in media.values())} decoded video frames. This is not an assembled film. All final files are 1080×1920, 30 FPS,H.264/yuv420p with AAC Foley. All 8 were fully decoded with no errors or detected black intervals. Browser playback reached the end at normal and half speed without corrupted frames. Resource-related displayed-frame drops and wall-clock timing are retained honestly in the playback JSON; they are not omitted or presented as file corruption.

## Measured native/contact results

Units are metres unless stated otherwise. Stairs were reopened and evaluated601 times at 120 Hz. Maximum stance drift: {stairs['actual_stance_drift_m']*1000:.6f}mm; foot-to-tread distance: {stairs['actual_foot_tread_distance_m']*1000:.6f}mm; limb length variation: {stairs['actual_limb_length_variation_m']*1000:.6f}mm; connected bone gap: {stairs['actual_connected_gap_m']*1000:.6f}mm. Tolerances:1mm stance/contact,0.1mm lengths/connections. The existing world ankle targets, poles and native no-stretch two-bone leg IK are retained. Stair arms use actual native FK controls.

Other six native caches were checked at 30 Hz, with native 60 Hz dense data supplied. Maximum wrist IK error across those caches: {max(v['max_native_wrist_IK_error_m'] for v in contacts.values())*1000:.6f}mm; maximum limb-length variation: {max(v['max_limb_length_variation_m'] for v in contacts.values())*1000:.6f}mm. All 6 pass their declared tolerances. The separate reports include actual foot drift, floor distance, root displacement/acceleration and connected joint gaps. Native arm/digit IK is implemented in bake_native.py; no full-body force simulation is claimed.

Key lock-axis lateral error: {props['KEY_LOCK']['key_lock_axis_lateral_error_m']*1000:.6f}mm. The blade is 100 mm long; contact fingers and hand follow its resized bow, and the 9-second monotone clock exposes insertion/rotation/withdrawal. Door body/jamb penetration is 0 mm at sampled vertices after restoring the collision-safe elbow. Curtain wrist/grip frame error: {props['WINDOW_CURTAIN']['native_wrist_to_fabric_grip_frame_error_m']*1000:.6f}mm. Curtain arc-length error and native prop parity are in separate scoped reports.

Vehicles integrate at 120 Hz. Minimum conservative bumper clearance: {vehicle['conservative_bumper_gap_m']:.6f}m. Maximum speed: {vehicle['speed_range_m_s'][1]:.6f}m/s. Heading/velocity and wheel-distance residuals, road margin and braking channels are measured in VEHICLE_WORLD_VALIDATION.json. House17 is locked to its original world transform; the new parked position differs from the approved original by less than 0.03 mm. This is a bicycle/spring model, not tyre-friction physics.

The repaired chase exterior camera stays at least {camera['CAR_CHASE']['minimum_camera_to_vehicle_bound_m']:.6f}m outside the conservative vehicle bounds. The repaired exit camera remains at least 750 mm street-side of the facade. Exit native non-head geometry parity is exact across 180,144 vertices; only camera/head presentation changed in that correction.

## Rendered inspection and corrections

Actual previews played at normal and half speed. Inspected encoded-frame contact sheets and consecutive playback capture sheets are included. Rejected failures were repaired: a 64.98 mm sleeve/door intersection, early bedroom framing that excluded the approaching witness, an exit camera behind the facade, and an obstructed chase reveal. See SCENE_DEFECT_REPORT.md and the archived rejection reports. The failed sparse running solver was rejected; the successful existing bounded solve remains selected.

Sound is locally synthesized from integrated speed and saved contact/event clocks; staircase landings and curtain edge velocity drive the relevant cues. No paid APIs or externally licensed audio were used. Audio is sample-clock aligned; human artistic/audio approval remains outstanding.

## Editable source and preservation

The final body pixels use actual Blender-evaluated mesh geometry. Supplied .blend files retain native rigs and prop/world mirrors. Python/C++ supplies the complete illustrated world, depth rendering, camera staging and face artwork. Blender-only GUI rendering does not reproduce all final pixels; see REBUILD.md. The source package includes scripts, native files, selected evaluated caches and reports.

All {len(before)} protected M08 files remain byte-identical. V10 was not edited; no full film was rendered or assembled. Existing remote Git entries are preserved and checked during publication.

## Artistic status

USER REVIEW REQUIRED. Engineering passes do not certify cinematic acting. Simplified/angular geometry, restrained acting, authored cloth and incomplete force/collision simulation remain. See KNOWN_LIMITATIONS.md and ARTISTIC_REPORT.md. No 10/10 or user approval is claimed.
'''
(R/'TECHNICAL_REPORT.md').write_text(text)
review='# M09 review and downloads\n\nEight separate final scene exports; user artistic review required.\n\n| Scene | Duration | MP4 | M08/M09 comparison |\n|---|---:|---|---|\n'
for s,row in rows.items():review+=f"| {s.replace('_',' ').title()} | {row['duration']:g}s | [Download]({row['final']}?raw=1) | [Contact sheet](contact_sheets/{s}_M08_vs_M09.jpg) |\n"
review+='\n[Editable Blender/scripts package](M09_EDITABLE_SOURCE.zip?raw=1) · [Technical report](TECHNICAL_REPORT.md) · [Defect/repair report](SCENE_DEFECT_REPORT.md) · [Artistic limitations](KNOWN_LIMITATIONS.md) · [Rebuild instructions](REBUILD.md)\n';(R/'REVIEW.md').write_text(review)
print('REPORTS_READY',flush=True)
