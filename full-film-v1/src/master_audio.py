"""Free two-pass loudness mastering; original generated mix remains untouched."""
from pathlib import Path
import subprocess,json,re,wave
r=Path(__file__).resolve().parents[1];src=r/'assets/audio/final_mix.wav';dest=r/'assets/audio/master_mix.wav'
if dest.exists():raise SystemExit('Refusing master overwrite')
base='loudnorm=I=-16:LRA=9:TP=-1.5'
p=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
block=re.findall(r'\{[^{}]+\}',p.stderr,re.S)[-1];m=json.loads(block)
filt=base+f':measured_I={m["input_i"]}:measured_LRA={m["input_lra"]}:measured_TP={m["input_tp"]}:measured_thresh={m["input_thresh"]}:offset={m["target_offset"]}:linear=true:print_format=json'
p=subprocess.run(['ffmpeg','-hide_banner','-n','-i',str(src),'-af',filt,'-ar','48000','-ac','2','-c:a','pcm_s16le','-t','86',str(dest)],capture_output=True,text=True,check=True)
second=json.loads(re.findall(r'\{[^{}]+\}',p.stderr,re.S)[-1]);(r/'audio-master-verification.json').write_text(json.dumps({'target_lufs':-16,'target_true_peak_dbtp':-1.5,'first_pass':m,'master_pass':second},indent=2))
with wave.open(str(dest),'rb') as w:assert w.getnframes()==48000*86
print(json.dumps(second,indent=2))
