from pathlib import Path
import sys,math,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'))
import house_site as car,physical_proofs as proof,film_performance as film,v10_trunk as trunk
FPS=30;events=[]
def add(t,name,kind='click',gain=.025,duration=.12,source='choreography'):
 frame=math.ceil(t*FPS-1e-7);e={'time':frame/FPS,'frame':frame,'source_time':t,'name':name,'kind':kind,'gain':gain,'duration':duration,'source':source}
 if 'foot' in name and 'plant' in name:e['material']='wet' if 'wet' in name or name.startswith('V10') else 'wood'
 events.append(e)
def foot_state(t):
 if t<car.RUN_START:return 'wet pavement',car.exit_feet(t)
 if t<51:return 'wet pavement',car.run_feet(t)
 if t<film.STAIR_START:return 'porch/hall',proof.door_state(t-51)['feet_world']
 if t<film.CURTAIN_START:return 'wood stairs',proof.stair_state(t-film.STAIR_START,2.16)['feet']
 if t<film.PHONE_START:return 'wood room',film.curtain_state(t)['feet']
 return 'wood room',film.call_state(t)['feet']
a=48.;last=foot_state(a)
for i in range(1,round((film.CHOICE-a)*120)+1):
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
for t,n,k in [(28.75,'boot acquires pedal contact','cloth'),(29.9,'accelerator reaches full pressure','cloth'),(38.6,'steering load','cloth'),(48.05,'driver door opens','click'),(48.3,'exit clothing','cloth'),(49.14,'driver door latch','click'),(51.6,'house handle grip','cloth'),(52.03,'locked handle pull','click'),(53.15,'keys retrieved','key'),(54.65,'key inserted','key'),(51+proof.remap(1.99,[(b,a) for a,b in proof.DOOR_KNOTS]),'lock released','click'),(56.1,'key withdrawn','key'),(56.45,'keys return to pocket','key'),(57.1,'house hinge opens','click'),(59.5,'house door closes under grip','cloth'),(60.15,'house door thump','thud'),(60.15,'house latch','click'),(60.7,'inside lock engages','click'),(51+proof.remap(5.98,[(b,a) for a,b in proof.DOOR_KNOTS]),'locked handle check','click'),(66.55,'curtain grip','cloth'),(65.4+proof.remap(61.8,[(b,a) for a,b in proof.CLOTH_KNOTS]),'curtain folds slide','cloth'),(68.35,'curtain released / folds settle','cloth'),(70.65,'phone grasp','cloth'),(70.75,'phone leaves support','click'),(72.4,'call answered at ear','click')]:add(t,n,k,.035 if n=='house door thump' else .022,.3 if 'folds' in n else .12,'actual proof/controller phase')
for t in [69.6,70.25]:add(t,'incoming phone ring','ring',.024,.30,'retimed fixed-device vibration interval')
events.sort(key=lambda e:(e['time'],e['name']));(R/'CONTACT_SOUND_CUES.json').write_text(json.dumps(events,indent=2));(R/'AUDIO_CUE_SHEET.md').write_text('# Contact-derived audio cue sheet\n\nStatus: event plan exported from actual choreography; mixing/listening review pending. Foot events are resolved from planted-state transitions, then placed on the first corresponding visible 30 FPS frame. Engine RPM/velocity remain driven by motion_state. Device buzz must follow device_rest() vibration envelope, not an unrelated loop.\n\n| Time | Frame | Event | Source |\n|---:|---:|---|---|\n'+'\n'.join(f"| {e['time']:.3f} | {e['frame']} | {e['name']} | {e['source']} |" for e in events)+'\n');print('Exported',len(events),'contact-timed cues; mix remains pending')
