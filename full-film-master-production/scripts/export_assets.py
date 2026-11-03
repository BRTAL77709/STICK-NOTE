from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import *
from actor import actor
from house17 import HOUSE,doorState
# Actual editable vector source assets, rendered by the same production rigs.
a=Art();begin(a)
for x,yaw,fear in [(220,0,0),(540,.8,.8),(860,-.8,.4)]:actor(a,x,1450,0,scale=1.45,yaw=yaw,fear=fear)
a.add('</svg>');(R/'assets/characters/WITNESS_MODEL_SHEET.svg').write_text(''.join(a.s))
for black,n in [(False,'WITNESS_SEDAN'),(True,'BLACK_SEDAN')]:
 a=Art();begin(a);p=state(35,black);c=Camera(p['x']-5,p['z']-9,1.4,.48,1440,760);sedan(a,c,35,black);a.add('</svg>');(R/'assets/vehicles'/(n+'.svg')).write_text(''.join(a.s))
(R/'assets/vehicles/rig.json').write_text(json.dumps({'tire_radius_m':.32,'wheelbase_m':2.7,'track_half_width_m':1.02,'source':'engine/animation/vehicle.py','state':'engine/animation/motion_state.py'},indent=2))
(R/'assets/environments/HOUSE17_GEOMETRY.json').write_text(json.dumps(HOUSE,indent=2))
(R/'assets/props/DOOR_LOCK_RIG.json').write_text(json.dumps({'source':'engine/animation/house17.py','hinge':[0,0,0],'handle':[.84,.95],'lock':[.84,1.12],'key_depth_m':.035,'events':'sound-cues.json'},indent=2))
(R/'assets/characters/V10_RIGS.json').write_text(json.dumps({'source':'engine/animation/v10_trunk.py','actors':['Criminal 01','Criminal 02','Injured victim'],'world':'orthographic shared ground plane','preserved_choreography':True},indent=2))
(R/'assets/fonts/README.md').write_text('Fonts and full license are delivered in hyperframes/assets/: FilmSans-Bold.ttf, FilmSans-Regular.ttf, FONT_LICENSE.txt. These are local DejaVu Sans faces.\n')
print('Editable witness/vehicle assets and rig metadata exported')
