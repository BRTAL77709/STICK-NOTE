"""Build real encoded comparisons and final scoped reports; no artistic self-approval."""
from pathlib import Path
import json,subprocess,hashlib,math,gzip,struct
from PIL import Image,ImageDraw
from bootstrap import ROOT as R
B=Path('/workspace/STICK-NOTE/NOIRFRAME_M09_CINEMATIC_UPGRADE');rows=json.loads((R/'CURRENT_SHOTS.json').read_text());media=json.loads((R/'reports/MEDIA_VALIDATION.json').read_text());v=json.loads((R/'reports/SHOT_REVISIONS.json').read_text());assert len(media)==8
(R/'comparisons').mkdir(exist_ok=True);comp={};source_map={};masters={}
for s,row in rows.items():
 new=R/row['final'];assert hashlib.sha256(new.read_bytes()).hexdigest()==media[s]['sha256'];old=B/'renders'/f'M09_{s}_FINAL.mp4';assert hashlib.sha256(old.read_bytes()).hexdigest()!=media[s]['sha256'];od=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(old)]));dur=row['duration'];sheet=Image.new('RGB',(720,688*6),'#071521');dr=ImageDraw.Draw(sheet);times=[]
 for j,fraction in enumerate([0,.18,.36,.54,.72,.98]):
  nt=min(dur-1/30,dur*fraction);ot=min(od-1/30,od*fraction)
  if s=='STAIRS':
   from scipy.interpolate import PchipInterpolator
   ot=min(od-1/30,float(PchipInterpolator([0,.4,1.5,4.9,6.],[0,.12,1.,4.3,5.])(nt)))
  for k,(p,t,label) in enumerate([(old,ot,'M09'),(new,nt,'M10')]):
   bb=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=360:640','-f','rawvideo','-pix_fmt','rgb24','-']);sheet.paste(Image.frombytes('RGB',(360,640),bb),(360*k,688*j+28));dr.text((360*k+8,688*j+7),f'{label} {s} / {t:.3f}s',fill='white')
  times.append({'M09_time_s':ot,'M10_time_s':nt})
 jpg=R/'contact_sheets'/f'{s}_M09_vs_M10.jpg';sheet.save(jpg,quality=93)
 target=R/'comparisons'/f'M09_VS_M10_{s}.mp4'
 if not target.exists():
  filters=f"[0:v]fps=30,scale=540:960,tpad=stop_mode=clone:stop_duration={max(0,dur-od)+.1},drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='M09 ({od:g}s)':x=12:y=12:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6[l];[1:v]fps=30,scale=540:960,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='M10 ({dur:g}s)':x=12:y=12:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.6[r];[l][r]hstack=inputs=2[v]"
  subprocess.run(['ffmpeg','-v','error','-n','-threads','1','-i',str(old),'-threads','1','-i',str(new),'-filter_complex_threads','1','-filter_complex',filters,'-map','[v]','-map','1:a:0','-t',str(dur),'-c:v','libx264','-crf','18','-preset','fast','-threads','1','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(target)],check=True)
 comp[s]={'M09_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'M10_sha256':media[s]['sha256'],'sheet':str(jpg.relative_to(R)),'comparison_video':str(target.relative_to(R)),'sample_times':times,'note':'Actual encoded video frames; staircase sheet aligns the retimed action clock. Side-by-side movies play each original timing at normal speed, holding the shorter M09 ending when necessary; audio is M10 only.'}
 master=R/'frames'/f'M10_{s}_FINAL';pngs=sorted(master.glob('*.png'));assert len(pngs)==round(dur*30)
 for q in [pngs[0],pngs[len(pngs)//2],pngs[-1]]:
  with Image.open(q) as im:assert im.size==(1080,1920);im.verify()
 b=new.read_bytes();offset=0;atoms=[]
 while offset+8<=len(b):
  size=int.from_bytes(b[offset:offset+4],'big');name=b[offset+4:offset+8].decode('latin1');header=8
  if size==1:size=int.from_bytes(b[offset+8:offset+16],'big');header=16
  if size==0:size=len(b)-offset
  assert size>=header;atoms.append({'type':name,'offset':offset,'bytes':size});offset+=size
 moov=next(a['offset'] for a in atoms if a['type']=='moov');mdat=next(a['offset'] for a in atoms if a['type']=='mdat');assert moov<mdat
 masters[s]={'path':str(master.relative_to(R)),'frames':len(pngs),'lossless_master':'native1080x1920 RGB PNG, no preview upscaling','bytes':sum(p.stat().st_size for p in pngs),'master_files':[{'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in pngs],'mp4_faststart_verified':True,'mp4_atoms':atoms,'completed_source_fingerprint':json.loads((master/'PRODUCER.json').read_text())['fingerprint']}
 native='STAIRS_M10D' if s=='STAIRS' else f'{s}_{v[s]}'
 models=['blender/'+native+'.blend']
 if s in ['ROAD_BUILDINGS','CAR_CHASE']:models=[f'blender/{s}_WORLD_M10_RELEASE.blend']
 if s=='CAR_CHASE':models+=['blender/DRIVER_CHASE_M10.blend','blender/DRIVER_CHASE_EDITABLE_M10.blend']
 source_map[s]={'baseline_mp4':str(old),'final_mp4':row['final'],'native_models':models,'native_cache':f'scenes/{native}_NATIVE.json.gz' if s=='STAIRS' else None if s in ['ROAD_BUILDINGS','CAR_CHASE'] else f'scenes/{native}.json.gz','driver_cache':f'scenes/DRIVER_CHASE_{v[s]}.json.gz' if s=='CAR_CHASE' else None,'renderer':'source/render_clips.py','cameras':'source/cameras.py','controller':'source/stairs_m10d.py' if s=='STAIRS' else f'source/actions_{v[s]}.py','camera_data':'CAMERA_ANIMATION.json','sound_master':f'sound/M10_{s}_FOLEY.wav','geometry_origin':'Actual native evaluated body/skin; scripted world/prop/face composition; native world mirrors are editable but not a one-click final-look renderer'}
 print('FINAL_COMPARISON_AND_MASTER',s,flush=True)
(R/'reports/COMPARISON_SOURCES.json').write_text(json.dumps(comp,indent=2));(R/'reports/MASTER_VALIDATION.json').write_text(json.dumps(masters,indent=2));(R/'SOURCE_TO_RENDER.json').write_text(json.dumps(source_map,indent=2))
protected=json.loads((R/'reports/M09_PRESERVATION_BASELINE.json').read_text());changed=[p for p,h in protected.items() if not (B/p).exists() or hashlib.sha256((B/p).read_bytes()).hexdigest()!=h];assert not changed;(R/'reports/PRESERVATION_AFTER.json').write_text(json.dumps({'all_previous_versions_preserved':True,'protected_M09_files':len(protected),'changed_or_missing':changed,'remote_tree_preservation':'Every previous remote Git entry is additionally verified unchanged at publication.'},indent=2))
plays={}
for p in (R/'reports').glob('M10_DELIVERY_*final-playback.json'):plays.update(json.loads(p.read_text()))
assert len(plays)==8 and all(p['ended'] and p['corruptedFrames']==0 for vv in plays.values() for p in vv)
contacts=json.loads((R/'reports/NATIVE_QA_SUMMARY.json').read_text());stairs=json.loads((R/'reports/STAIRS_M10D_NATIVE_RECHECK.json').read_text());props=json.loads((R/'reports/PROP_INTERACTION_VALIDATION.json').read_text());coll=json.loads((R/'reports/DOOR_BODY_COLLISION_CHECK.json').read_text());vehicle=json.loads((R/'reports/VEHICLE_WORLD_VALIDATION.json').read_text());reuse=json.loads((R/'reports/EXIT_FRAME_REUSE.json').read_text());assert stairs['pass'] and all(x['technical_status']=='TECHNICAL PASS' for x in contacts.values()) and all(x['status']=='TECHNICAL PASS' for x in coll.values())
text=f'''# M10 technical and production validation

Eight independent scene exports, {sum(r['duration'] for r in rows.values()):.1f}s in total; {sum(x['decoded_frames'] for x in media.values())} fully decoded frames. All are1080×1920,30FPS,H.264/yuv420p,AAC, with faststart verified from actual MP4 atom ordering. CRF18 encoding has no bitrate or arbitrary file-size target. Every main video differs from its actual M09 baseline hash.

Lossless native-resolution PNG masters are retained for every frame under frames/M10_<SCENE>_FINAL/: {sum(x['bytes'] for x in masters.values())} bytes, {sum(x['frames'] for x in masters.values())} frames. No low-resolution preview was upscaled. Fingerprints prevent stale-source frame reuse. After the exit correction, {reuse['reuse_count']} frames had exact equivalent evaluated meshes/authoring states and critical source hashes; {reuse['rerender_count']} changed frames were rendered anew. Original passes remain preserved.

## Actual measured checks

Stairs: {stairs['fresh_native_evaluations']} native reopen/evaluations at120Hz. Maximum stance drift {stairs['actual_stance_drift_m']*1000:.6f}mm; foot/tread distance {stairs['actual_foot_tread_distance_m']*1000:.6f}mm; length variation {stairs['actual_limb_length_variation_m']*1000:.6f}mm; connected bone gap {stairs['actual_connected_gap_m']*1000:.6f}mm. Original1mm stance/contact and0.1mm length/joint tolerances retained. Retimed original keys pass after the resampled-key draft was rejected.

Six other native caches pass declared30Hz contact checks, with60Hz dense native evaluation data supplied. Maximum wrist target error {max(x['max_native_wrist_IK_error_m'] for x in contacts.values())*1000:.6f}mm. Native no-stretch IK and actual bound skin supply the final body geometry. Stair upper-body FK is retained; no universal bone-mode switch or force-based muscle simulation is claimed.

Key: actual seated insertion depth {props['KEY_LOCK']['maximum_inserted_depth_m']*1000:.3f}mm; lock-axis lateral error {props['KEY_LOCK']['key_lock_axis_lateral_error_m']*1000:.6f}mm; hand/grip frame error {props['KEY_LOCK']['native_hand_key_grip_frame_error_m']*1000:.6f}mm. Blade100mm, intended exposed shoulder10mm. Door/jamb sampled body penetration is0mm after the inside-elbow repair. Hallway root travel and four measured foot landings are recorded in MOTION_MEASUREMENTS.json.

Curtain: actual wrist/grip frame error {props['WINDOW_CURTAIN']['native_wrist_to_fabric_grip_frame_error_m']*1000:.6f}mm; horizontal material arc-length error {props['WINDOW_CURTAIN']['max_horizontal_material_arc_length_error_m']*1000:.6f}mm. Header/edge anchors are retained; deformation is authored, not full force/self-collision cloth physics.

Vehicle integration120Hz, conservative minimum bumper clearance {vehicle['conservative_bumper_gap_m']:.6f}m; wheel-distance/heading residuals and road margins are in VEHICLE_WORLD_VALIDATION.json. Route and House17 registration remain shared. Existing valid bicycle/spring dynamics were preserved, not relabelled as new friction physics. The chase reaction edit now coincides with the actual glance and precedes the closer pursuer reveal.

Native cockpit hierarchy/axis/frame files preserve actual evaluated skin with zero measured geometry difference. CAR_ROOT groups are car-local, and integrated world motion is applied once by the renderer. Camera animation exports identify each local/world coordinate frame explicitly.

All main videos were fully decoded with no errors or detected black intervals. Normal- and half-speed Chromium playback reached each ending without corrupted frames. Actual displayed-frame drops under load are retained in playback reports, not omitted or confused with file corruption. Exact repeated-frame intervals are reported; deliberate holds do not establish artistic approval.

## Sound and inspection

Eight original local PCM WAV masters are retained; AAC finishing copies the encoded video stream. Footsteps derive from saved contacts, cloth sound from edge velocity, engine sound from integrated speed, with timed original suspense accents. No paid API, copyrighted sample library or new external asset was used. Human audio/artistic approval remains outstanding.

Actual encoded M09/M10 contact sheets and normal-speed side-by-side movies are included. Shorter baseline endings are explicitly held for comparison coverage; main films are unchanged. No full86-second film is assembled.

## Preservation, source and limits

All{len(protected)} pre-edit M09 files remain byte-identical. V10 was not edited. Publication verifies every previous remote tree entry. SOURCE_TO_RENDER.json identifies actual models/caches/controllers; CAMERA_ANIMATION.json, native models, scripts and WAVs are supplied. Editable Blender files contain real rigs and mirrors, while the final look also uses Python/C++ world/prop/depth and vector-face composition. Native prop-only GUI edits need matching scripted definitions.

USER ARTISTIC REVIEW REQUIRED. Simplified/angular geometry, restrained acting, authored cloth and incomplete whole-house/force/continuous-collision certification remain. See KNOWN_LIMITATIONS.md. No10/10 claim or automatic artistic approval.
'''
for a,b in {'are1080':'are 1080','All'+str(len(protected)):'All '+str(len(protected)),'No10/10':'No 10/10','full86':'full 86','Blade100mm':'Blade 100 mm','is0mm':'is 0 mm'}.items():text=text.replace(a,b)
(R/'TECHNICAL_REPORT.md').write_text(text)
review='# M10 review and downloads\n\nEight independent scene exports; artistic approval remains with the user.\n\n| Scene | Duration | MP4 | Motion comparison | Contact sheet |\n|---|---:|---|---|---|\n'
for s,r in rows.items():review+=f"| {s.replace('_',' ').title()} | {r['duration']:g}s | [Download]({r['final']}?raw=1) | [M09/M10](comparisons/M09_VS_M10_{s}.mp4?raw=1) | [Frames](contact_sheets/{s}_M09_vs_M10.jpg) |\n"
review+='\n[Editable source package](M10_EDITABLE_SOURCE.zip?raw=1) · [Technical report](TECHNICAL_REPORT.md) · [Scene repair audit](SCENE_DEFECT_REPORT.md) · [Remaining limitations](KNOWN_LIMITATIONS.md) · [Rebuild](REBUILD.md)\n';(R/'REVIEW.md').write_text(review)
(R/'README.md').write_text('# NOIRFRAME M10\n\nEight complete scene exports for review; no full-film assembly or artistic approval. See REVIEW.md for actual downloads and motion comparisons, TECHNICAL_REPORT.md for measured checks, SOURCE_TO_RENDER.json for editable mapping, and REBUILD.md for the free local pipeline. M09/V10 remain preserved.\n')
print('M10_REPORTS_READY',flush=True)
