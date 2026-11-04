from pathlib import Path
import sys,math,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'))
import house_site as car,house_actions as door,stairs_actions as stairs,room_actions as room,v10_trunk as trunk
FPS=30;events=[]
def add(t,name,kind='click',gain=.025,duration=.12,source='choreography'):
 frame=math.ceil(t*FPS-1e-7);e={'time':frame/FPS,'frame':frame,'source_time':t,'name':name,'kind':kind,'gain':gain,'duration':duration,'source':source}
 if 'foot' in name and 'plant' in name:e['material']='wet' if 'wet' in name or name.startswith('V10') else 'wood'
 events.append(e)
def foot_state(t):
 if t<car.RUN_START:return 'wet pavement',car.exit_feet(t)
 if t<51:return 'wet pavement',car.run_feet(t)
 if t<stairs.T0:return 'porch/hall',door.feet(t-51)
 if t<stairs.END:return 'wood stairs',stairs.feet(t)
 return 'wood room',room.feet(t)
a=48.;last=foot_state(a)
for i in range(1,round((80-a)*120)+1):
 t=a+i/120;now=foot_state(t)
 for j in [0,1]:
  if not last[1][j][1] and now[1][j][1]:
   lo=t-1/120;hi=t
   for _ in range(40):
    mid=(lo+hi)/2
    if foot_state(mid)[1][j][1]:hi=mid
    else:lo=mid
   material,fs=foot_state(hi);p=fs[j][0]
   if material=='porch/hall':material='wet porch' if p[2]<0 else 'wood hall'
   add(hi,f'{material} foot {j+1} plant','thud',.024 if 'wet' in material else .017,.09,'actual held-foot transition')
 last=now
# Preserve V10's picture clock and derive its own actual foot-plan contacts.
def trunk_time(q):return 12+q/1.95*6 if q<1.95 else (18+(q-1.95)/4.75*6 if q<6.7 else 24+(q-6.7)/3.3*4)
for actor in [0,1]:
 for leg in [0,1]:
  for start,end,x,y,lift in trunk.PLANS[actor][leg][2]:add(trunk_time(end),f'V10 criminal {actor+1} foot {leg+1} plant','thud',.021,.09,'unchanged V10 world foot plan')
for q,n,k in [(1.95,'trunk hinge opening','click'),(2.6,'grip reposition','cloth'),(3.05,'coordinated lift effort','cloth'),(6.25,'victim rests inside trunk','thud'),(6.7,'hands withdraw','cloth'),(7.5,'trunk closes','thud'),(7.5,'trunk latch','click')]:add(trunk_time(q),n,k,.05 if k=='thud' else .03,.14,'unchanged V10 action clock')
for t,n,k in [(28.55,'boot contact','cloth'),(30,'accelerator reaches modeled pressure','cloth'),(38.6,'steering load','cloth'),(48.05,'driver door opens','click'),(48.3,'exit clothing','cloth'),(49.14,'driver door latch','click'),(51.22,'house handle grip','cloth'),(51.45,'locked handle pull','click'),(52.12,'keys retrieved','key'),(52.72,'key inserted','key'),(52.99,'lock released','click'),(53.3,'key withdrawn','key'),(53.55,'keys return to pocket','key'),(53.85,'house hinge opens','click'),(55.35,'house door closes under grip','cloth'),(55.95,'house door thump','thud'),(55.95,'house latch','click'),(56.55,'inside lock engages','click'),(56.98,'locked handle check','click'),(61.6,'curtain grip','cloth'),(61.8,'curtain folds slide','cloth'),(62.25,'curtain settles','cloth'),(64.15,'phone grasp','cloth'),(64.2,'phone leaves support','click'),(65.8,'call answered at ear','click')]:add(t,n,k,.035 if n=='house door thump' else .022,.3 if 'folds' in n else .12)
for t in [63.1,63.75]:add(t,'incoming phone ring','ring',.024,.30,'same fixed-device vibration interval')
events.sort(key=lambda e:(e['time'],e['name']));(R/'CONTACT_SOUND_CUES.json').write_text(json.dumps(events,indent=2));(R/'AUDIO_CUE_SHEET.md').write_text('# Contact-derived audio cue sheet\n\nStatus: event plan exported from actual choreography; mixing/listening review pending. Foot events are resolved from planted-state transitions, then placed on the first corresponding visible 30 FPS frame. Engine RPM/velocity remain driven by motion_state. Device buzz must follow device_rest() vibration envelope, not an unrelated loop.\n\n| Time | Frame | Event | Source |\n|---:|---:|---|---|\n'+'\n'.join(f"| {e['time']:.3f} | {e['frame']} | {e['name']} | {e['source']} |" for e in events)+'\n');print('Exported',len(events),'contact-timed cues; mix remains pending')
