"""Actual local Whisper inference; fail clearly when verified weights are absent."""
from pathlib import Path
import argparse,json,re,sys,difflib,hashlib
import whisper,torch
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('audio',type=Path);p.add_argument('--model',type=Path,default=R/'.models/tiny.en.pt');p.add_argument('--script',type=Path,default=R/'shared/narration-script.txt');p.add_argument('--offset',type=float,default=0);p.add_argument('--words',action='store_true');a=p.parse_args()
report={'audio_sha256':hashlib.sha256(a.audio.read_bytes()).hexdigest(),'offset':a.offset,'engine':'openai-whisper','inference_executed':False,'audio':str(a.audio),'model':str(a.model),'word_timing':'Whisper estimates are not forced alignment; inspect before publishing.'}
if not a.model.is_file():
 report['blocker']='Missing checkpoint. Official download returned CONNECT tunnel failed HTTP403; no fabricated ASR captions.';(R/'reports/whisper-transcription.json').write_text(json.dumps(report,indent=2));print(report['blocker']);sys.exit(3)
torch.set_num_threads(4);model=whisper.load_model(str(a.model),device='cpu');result=model.transcribe(str(a.audio),language='en',fp16=False,temperature=0,word_timestamps=a.words)
for s in result['segments']:
 s['start']+=a.offset;s['end']+=a.offset
 for w in s.get('words',[]):w['start']+=a.offset;w['end']+=a.offset
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'
lines=[]
for i,s in enumerate(result['segments'],1):lines.append(f"{i}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['text'].strip()}\n")
(R/'subtitles/whisper.srt').write_text('\n'.join(lines));(R/'subtitles/whisper.json').write_text(json.dumps(result,indent=2));norm=lambda s:re.findall(r"[a-z0-9']+",s.lower());expected=norm(a.script.read_text());actual=norm(result['text']);report.update(inference_executed=True,transcript=result['text'],script_match=expected==actual,script_diff=list(difflib.ndiff(expected,actual)),model_sha256=hashlib.sha256(a.model.read_bytes()).hexdigest());(R/'reports/whisper-transcription.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
