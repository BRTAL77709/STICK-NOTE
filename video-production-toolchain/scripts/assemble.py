"""Composite the local transparent HF layer over Remotion and mix measured speech."""
from pathlib import Path
import subprocess,json,os,hashlib
R=Path(__file__).resolve().parents[1];T=json.loads((R/'shared/timeline.json').read_text());D=Path(os.environ.get('NOIRFRAME_RUN_DIR',R/'renders'));D=D if D.is_absolute() else R/D;out=D/'NOIRFRAME_TOOLCHAIN_INTEGRATION_DEMO.mp4';assert not out.exists(),'Refusing to overwrite existing demo'
# Only generated-by-Whisper files may be called ASR. A measured script reference is explicit fallback.
asr=R/'subtitles/whisper.json'
if asr.exists():
 proof=json.loads((R/'reports/whisper-transcription.json').read_text());assert proof['inference_executed'] and proof['audio_sha256']==hashlib.sha256((R/'shared/narration.wav').read_bytes()).hexdigest() and abs(proof['offset']-T['speechStartFrame']/T['fps'])<1e-8,'Stale ASR transcript; transcribe actual current narration again'
segments=json.loads(asr.read_text())['segments'] if asr.exists() else json.loads((R/'subtitles/script-reference.json').read_text());origin='Whisper ASR' if asr.exists() else 'Measured source-script reference; Whisper inference blocked'
def stamp(t):
 n=round(t*100);return f'{n//360000}:{n//6000%60:02}:{n//100%60:02}.{n%100:02}'
ass='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,46,&H00EAEDEF,&H00EAEDEF,&H00130902,&H8A130902,-1,0,0,0,100,100,0,0,3,10,0,2,108,108,120,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
for s in segments:ass+=f"Dialogue: 0,{stamp(s['start'])},{stamp(s['end'])},Default,,0,0,0,,{s['text'].strip()}\n"
(R/'subtitles/demo.ass').write_text(ass)
h=T['hud'];box=h['region'];offset=h['startFrame']/T['fps'];filters=f"[1:v]setpts=PTS-STARTPTS+{offset}/TB,format=rgba[hud];[0:v][hud]overlay={box['x']}:{box['y']}:eof_action=pass:repeatlast=0:format=auto[visual];[visual]ass=subtitles/demo.ass:fontsdir=shared/fonts,format=yuv420p[v]"
cmd=['ffmpeg','-v','warning','-n','-i',str(D/'remotion-scene.mp4'),'-i',str(D/'hyperframes-hud.mov'),'-i','shared/demo-audio.wav','-filter_complex',filters,'-map','[v]','-map','2:a','-c:v','libx264','-preset','medium','-crf','20','-r',str(T['fps']),'-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-t',str(T['duration']),'-movflags','+faststart',str(out)]
subprocess.run(cmd,cwd=R,check=True);(R/'reports/assembly.json').write_text(json.dumps({'command':cmd,'shared_timeline':T,'subtitle_origin':origin,'cloud':False,'paid_services':False},indent=2));print(out)
