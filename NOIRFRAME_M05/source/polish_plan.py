"""M05 pose offsets over verified M04 control data; foot schedule/targets unchanged."""
from pathlib import Path
import json,math,hashlib
import numpy as np
from scipy.interpolate import CubicSpline
R=Path(__file__).resolve().parents[1];base=R.parent/'NOIRFRAME_M04/assets/CONTROLS_R06.json';p=json.loads(base.read_text());oldkeys=p['root_keys'];spline=CubicSpline([k['time'] for k in oldkeys],[k['value'] for k in oldkeys],bc_type=((1,oldkeys[0]['derivative']),(1,oldkeys[-1]['derivative'])))
def s5(u):u=float(np.clip(u,0,1));return u**3*(10-15*u+6*u*u)
def envelope(t):return s5(t/.30)*(1-s5((t-4.25)/.70))
def offset(t):
 anticipation=math.sin(math.pi*np.clip(t/.35,0,1))**2 if t<.35 else 0
 settle=sum(-.005*math.exp(-((t-(s['land']+.095))/.085)**2)+.0015*math.exp(-((t-(s['land']+.24))/.13)**2) for s in p['steps'])
 return np.array([-.010*anticipation,.004*math.sin(math.pi*(t-.55)/1.03)*envelope(t),-.012*anticipation+settle])
times=sorted(set(round(float(t),9) for t in [k['time'] for k in oldkeys]+list(np.linspace(0,5,201))));values=[spline(t)+offset(t) for t in times];root=CubicSpline(times,values,bc_type=((1,[0,0,0]),(1,[0,0,0])))
p['root_keys']=[{'time':t,'value':root(t).tolist(),'derivative':root(t,1).tolist()} for t in times]
for f in p['frames']:
 t=f['time'];e=envelope(t);phase=math.pi*(t-.35)/1.03;arm=.40*math.cos(phase-.12)*e;anticipation=math.sin(math.pi*np.clip(t/.35,0,1))**2 if t<.35 else 0
 f['root']=root(t).tolist();f['pelvis_roll']*=1.10;f['pelvis_twist']=-.040*math.cos(phase)*e
 f['spine_pitch']=math.radians(7)*s5(t/.23)*(1-s5((t-4.4)/.6))+math.radians(5)*e+math.radians(2)*anticipation
 f['chest_pitch']=f['spine_pitch']*.74;f['chest_twist']=.075*math.cos(phase-.12)*e
 f['arm_swing']=[arm+.12*anticipation,-arm+.19*anticipation]
 f['elbow_extra']=[.13*e+.12*math.sin(phase-.45)*e+.16*anticipation,.13*e-.12*math.sin(phase-.45)*e+.12*anticipation]
 f['head_pitch']=math.radians(-2)*s5(t/.35)*(1-s5((t-4.3)/.7));f['head_yaw']=math.radians(-5)*math.sin(math.pi*np.clip(t/.6,0,1))**2+math.radians(3)*s5((t-3.6)/.5)*(1-s5((t-4.5)/.5))
 f['face']={'yaw':.94-.34*(math.sin(math.pi*np.clip(t/.60,0,1))**2), 'gaze':.70-.8*math.sin(math.pi*np.clip(t/.6,0,1))**2,'fear':.70,'blink':max(0,1-abs(t-.27)/.065)}
p['method']='M05 artistic offsets on verified M04 control plan, same foot trajectory and stair schedule. Native IK retained; authored kinematics, not forces.';p['baseline_sha256']=hashlib.sha256(base.read_bytes()).hexdigest();out=R/'assets/CONTROLS_POLISH_A02.json';assert not out.exists();out.write_text(json.dumps(p,separators=(',',':')))
old=json.loads(base.read_text());assert p['steps']==old['steps'];assert all(a['feet']==b['feet'] for a,b in zip(p['frames'],old['frames']))
(R/'reports/FOOT_PLAN_PRESERVATION.json').write_text(json.dumps({'baseline_sha256':p['baseline_sha256'],'same_contact_schedule':True,'identical_601_two_foot_targets':True,'new_poses_only':True},indent=2));print(out)
