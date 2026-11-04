"""One explicit official checkpoint download; never retry or disable TLS."""
from pathlib import Path
import urllib.request,hashlib,json
import whisper
R=Path(__file__).resolve().parents[1];url=whisper._MODELS['tiny.en'];target=R/'.models/tiny.en.pt';target.parent.mkdir(exist_ok=True);report={'model':'tiny.en','source':url,'official':True,'attempts':1,'available':False}
try:
 with urllib.request.urlopen(url,timeout=35) as response:b=response.read()
 actual=hashlib.sha256(b).hexdigest();expected=url.split('/')[-2];assert actual==expected,'Checkpoint SHA mismatch';target.write_bytes(b);report.update(available=True,sha256=actual,bytes=len(b))
except Exception as e:report.update(error_type=type(e).__name__,error=str(e))
(R/'reports/whisper-model.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
