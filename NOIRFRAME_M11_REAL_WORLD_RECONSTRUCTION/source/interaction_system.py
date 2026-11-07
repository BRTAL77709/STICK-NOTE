"""Shared contact-phase registry. Targets are enforced by native Blender IK, not claimed physics."""
import numpy as np
PHASES=('APPROACH','CONTACT','GRIP','MANIPULATION','RELEASE','RECOVERY')
SCHEDULES={
 'DRIVING_COCKPIT':[(0,'GRIP'),(1.6,'MANIPULATION'),(10.5,'RECOVERY')],
 'DRIVER_CHASE':[(0,'GRIP'),(1.6,'MANIPULATION'),(10.5,'RECOVERY')],
 'KEY_LOCK':[(0,'APPROACH'),(1.35,'CONTACT'),(1.5,'GRIP'),(2.9,'MANIPULATION'),(7.4,'RELEASE'),(8.4,'RECOVERY')],
 'DOOR_ENTRY':[(0,'APPROACH'),(.52,'CONTACT'),(.65,'GRIP'),(.85,'MANIPULATION'),(9.9,'RELEASE'),(13,'RECOVERY')],
 'CAR_EXIT_RUNNING':[(0,'GRIP'),(1.5,'RELEASE'),(2.1,'APPROACH'),(2.55,'CONTACT'),(2.65,'GRIP'),(2.7,'MANIPULATION'),(3.,'RELEASE'),(3.2,'RECOVERY')],
 'WINDOW_CURTAIN':[(0,'APPROACH'),(4.6,'CONTACT'),(4.8,'GRIP'),(5.,'MANIPULATION'),(8.0,'RELEASE'),(8.5,'RECOVERY')]}
def phase(shot,t):
 current='APPROACH'
 for at,name in SCHEDULES.get(shot,[]):
  if t<at:break
  current=name
 return current

def restore(q):
 if isinstance(q,dict):return {k:restore(v) for k,v in q.items()}
 if isinstance(q,list):
  try:
   a=np.asarray(q)
   if a.size and a.dtype.kind in 'fiu':return a
  except (ValueError,TypeError):pass
  return [restore(v) for v in q]
 return q
