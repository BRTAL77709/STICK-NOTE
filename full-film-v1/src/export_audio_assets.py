"""Lossless phrase/narration assets and a compact mastered mix for delivery."""
from pathlib import Path
import subprocess,json
r=Path(__file__).resolve().parents[1];out=r/'audio';(out/'voices').mkdir(parents=True,exist_ok=True);mapping=[]
for seg in json.loads((r/'narration-timing.json').read_text()):
 src=r/seg['asset'];dest=out/'voices'/src.with_suffix('.flac').name
 if not dest.exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(src),'-c:a','flac',str(dest)],check=True)
 mapping.append({'source_wav':seg['asset'],'delivered':str(dest.relative_to(r)),'speaker':seg['speaker'],'start':seg['start'],'end':seg['end']})
for name in ['narration_stem']:
 dest=out/(name+'.flac')
 if not dest.exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(r/'assets/audio'/f'{name}.wav'),'-c:a','flac',str(dest)],check=True)
dest=out/'master_mix.m4a'
if not dest.exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(r/'assets/audio/master_mix.wav'),'-c:a','aac','-b:a','160k','-t','86','-movflags','+faststart',str(dest)],check=True)
# Recover the original pre-master sound-design stem, with no narration samples.
import wave,numpy as np
with wave.open(str(r/'assets/audio/final_mix.wav'),'rb') as w:mix=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(np.int32)
with wave.open(str(r/'assets/audio/narration_stem.wav'),'rb') as w:voice=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.int32)
stem=np.clip(mix-voice[:,None],-32768,32767).astype('<i2');dest=out/'sound_design_stem.flac'
if not dest.exists():subprocess.run(['ffmpeg','-v','error','-n','-f','s16le','-ar','48000','-ac','2','-i','pipe:0','-c:a','flac',str(dest)],input=stem.tobytes(),check=True)
(out/'voice-assets.json').write_text(json.dumps(mapping,indent=2));print('Delivered audio assets:',len(mapping),'phrases plus stems/mix')
