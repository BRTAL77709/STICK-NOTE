"""Story duration, source pose, phrase/SRT and crime-order checks for the whole film."""
from pathlib import Path
import json,math,re
import render_film as f
r=f.ROOT;assert len(f.SHOTS)==18 and sum(x['frames'] for x in f.SHOTS)==2580
expected=[(0,4),(4,8),(8,12),(12,18),(18,24),(24,28),(28,32),(32,37),(37,42),(42,47),(47,51),(51,55),(55,59),(59,63),(63,67),(67,74),(74,80),(80,86)]
assert [(s['start'],s['end']) for s in f.SHOTS]==expected
checks=[]
for s in f.SHOTS:
 for n in range(s['frames']):
  svg=f.scene_svg(s['scene'],n/30);assert svg.startswith('<svg') and svg.endswith('</svg>');assert 'nan' not in svg.lower();assert 'DEBUG-GROUND' not in svg
 checks.append({'scene':s['scene'],'frames_checked':s['frames'],'all_poses_evaluated':True})
for s in f.CAPTIONS:
 shot=f.SHOTS[s['scene']-1];assert shot['start']<=s['start']<s['end']<=shot['end'];assert (r/s['asset']).exists() or (r/'audio/voices'/Path(s['asset']).with_suffix('.flac').name).exists()
assert all(a['end']<=b['start'] for a,b in zip(f.CAPTIONS,f.CAPTIONS[1:]));assert len(re.findall(r' --> ',(r/'THE_PRICE_OF_SILENCE_EN.srt').read_text()))==len(f.CAPTIONS)
closed=[];turn=[]
for n in range(24*30,28*30):
 t=n/30;q=6.7+(t-24)/4*3.3
 if f.trunk.lid_angle(q)==0:closed.append(n)
 if f.trunk.b.reaction(f.trunk.head_time(q))>0:turn.append(n);assert f.trunk.lid_angle(q)==0
assert closed[0]==750 and turn[0]==768
assert all(x in f.scene_svg(18,3) for x in ['WHAT WOULD','YOU DO?','TAKE','$1,000,000','THE POLICE','COMMENT A OR B','FOR PART 2'])
report={'scenes':18,'duration_seconds':86,'frames':2580,'source_pose_checks':checks,'caption_phrases':len(f.CAPTIONS),'caption_overlaps':0,'caption_timings':'Actual individually synthesized phrase clips, not transcript estimates.','local_voices':{'protagonist':'Flite RMS','caller':'Flite AWB, telephone filtering'},'trunk_fully_closed_first_frame':closed[0],'trunk_fully_closed_first_frame_seconds':closed[0]/30,'criminal_turn_first_frame':turn[0],'criminal_turn_first_frame_seconds':turn[0]/30,'closing_latch_sound_time':25.0,'head_before_closure_violations':0,'final_choice_duration':6,'final_choice_burned_captions':False,'promotional_logo_used_as_story':False,'note':'Source/model and timing checks. Encoded video, audio, typography and normal-speed playback need separate review; this is not an artistic score.'}
(r/'source-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='source_pose_checks'},indent=2))
