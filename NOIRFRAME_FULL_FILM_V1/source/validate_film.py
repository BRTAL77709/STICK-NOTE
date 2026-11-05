from pathlib import Path
import json,subprocess,hashlib,concurrent.futures,argparse
import numpy as np
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser();ap.add_argument('--skip-preservation',action='store_true');args=ap.parse_args();R=Path(__file__).resolve().parents[1];P=R.parent;plan=json.loads((R/'EDIT_DECISION_LIST.json').read_text());base=(R/plan['baseline']).resolve();final=R/'renders/THE_PRICE_OF_SILENCE_NOIRFRAME_COMPLETE_86s.mp4'
q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(final)]));v=next(x for x in q['streams'] if x['codec_type']=='video');a=next(x for x in q['streams'] if x['codec_type']=='audio');assert v['width']==1080 and v['height']==1920 and v['avg_frame_rate']=='30/1' and int(v['nb_read_frames'])==2580 and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p';assert abs(float(q['format']['duration'])-86)<.002 and a['codec_name']=='aac' and int(a['sample_rate'])==48000
z=subprocess.run(['ffmpeg','-v','error','-i',str(final),'-f','null','-'],capture_output=True);assert z.returncode==0 and not z.stderr,z.stderr.decode()
def v10(path):
 txt=subprocess.check_output(['ffmpeg','-v','error','-threads','2','-i',str(path),'-vf','trim=start_frame=360:end_frame=840,setpts=PTS-STARTPTS','-an','-f','framemd5','pipe:1'],text=True);return [x.split(',')[-1].strip() for x in txt.splitlines() if x and not x.startswith('#')]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:h=list(ex.map(v10,[base,final]))
assert len(h[0])==len(h[1])==480 and h[0]==h[1],'V10 decoded pictures changed'
(R/'reports/V10_FRAME_PRESERVATION.json').write_text(json.dumps({'baseline':str(base.relative_to(P)),'film':str(final.relative_to(R)),'interval_s':[12,28],'frames':480,'all_decoded_frame_md5_identical':True,'baseline_frame_MD5':h[0],'final_frame_MD5':h[1]},indent=2))
# Stream downsampled frames to bound memory; this checks black/duplicate frames, not animation merit.
cmd=['ffmpeg','-v','error','-threads','2','-i',str(final),'-vf','scale=144:256','-an','-pix_fmt','rgb24','-f','rawvideo','pipe:1'];p=subprocess.Popen(cmd,stdout=subprocess.PIPE);n=0;black=0;identical=0;previous=None;minimum=255;times=[.7,5.2,9.4,13,20,26,29.5,34.5,40,45,48.5,49.9,51.4,53.2,55.4,58.7,62.3,63.8,66.3,68.3,71,74.2,79.5,84];wanted={round(t*30):t for t in times};selected=[]
while True:
 b=p.stdout.read(144*256*3)
 if not b:break
 assert len(b)==144*256*3
 x=np.frombuffer(b,np.uint8);mean=float(x.mean());minimum=min(minimum,mean);black+=int(mean<1);identical+=int(b==previous)
 if n in wanted:selected.append((wanted[n],Image.frombytes('RGB',(144,256),b)))
 previous=b;n+=1
assert p.wait()==0 and n==2580 and black==0
sheet=Image.new('RGB',(864,286*((len(selected)+5)//6)),'#06131e');d=ImageDraw.Draw(sheet)
for j,(t,im) in enumerate(selected):sheet.paste(im,(j%6*144,j//6*286));d.text((j%6*144+6,j//6*286+261),f'{t:.2f}s',fill='white')
sheet.save(R/'reviews/FULL_FILM_CONTACT_SHEET.jpg',quality=94)
m=subprocess.run(['ffmpeg','-v','info','-i',str(final),'-vn','-af','loudnorm=I=-16:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True);meter=json.JSONDecoder().raw_decode(m.stderr[m.stderr.rfind('{'):])[0]
before={} if args.skip_preservation else json.loads((R/'reports/preservation-before.json').read_text());changed=[];missing=[]
for rel,sha in before.items():
 f=P/rel
 if not f.is_file():missing.append(rel)
 elif hashlib.sha256(f.read_bytes()).hexdigest()!=sha:changed.append(rel)
assert not changed and not missing
report={'file':str(final.relative_to(R)),'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'duration_s':float(q['format']['duration']),'frames':n,'width':1080,'height':1920,'fps':30,'video_codec':v['codec_name'],'pixel_format':v['pix_fmt'],'audio_codec':a['codec_name'],'sample_rate':48000,'full_decode':'clean','V10_decoded_frames_identical':480,'black_frames':black,'adjacent_identical_downsampled_frames':identical,'minimum_mean_RGB':minimum,'audio_measured_input':meter,'preservation':{'files_checked':len(before),'skipped':args.skip_preservation,'changed':changed,'missing':missing},'quality':'Best-achievable complete hybrid edit; artistic limitations remain; no approval or score claimed.'};(R/'reports/FINAL_VALIDATION.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
