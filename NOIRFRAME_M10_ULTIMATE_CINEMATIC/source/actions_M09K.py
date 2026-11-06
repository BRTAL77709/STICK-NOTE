"""Exact saved M09D contact/acting states; no re-solve or motion substitution."""
from actions_M09D import *
from pathlib import Path
import json,gzip,numpy as np
_DATA=None
_BASE=state
def restore(q):
 if isinstance(q,dict):return {k:restore(v) for k,v in q.items()}
 if isinstance(q,list):
  try:
   a=np.asarray(q)
   if a.size and a.dtype.kind in 'fiu':return a
  except (ValueError,TypeError):pass
  return [restore(v) for v in q]
 return q
def state(shot,t):
 global _DATA
 if shot!='CAR_EXIT_RUNNING':return _BASE(shot,t)
 if _DATA is None:_DATA=json.load(gzip.open(Path(__file__).resolve().parents[1]/'scenes/CAR_EXIT_RUNNING_M09D.json.gz','rt'))
 return restore(_DATA['state'][min(len(_DATA['state'])-1,max(0,round(t*30)))])
