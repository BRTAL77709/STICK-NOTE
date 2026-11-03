from pathlib import Path
import json
from motion_state import state,pursuit_distance
R=Path(__file__).resolve().parents[1]
a=[{'frame':f,'t':f/30,**state(f/30),'pursuit_distance_m':pursuit_distance(f/30)} for f in range(451)]
s='window.VEHICLE_FRAMES='+json.dumps(a,separators=(',',':'))+';'
(R/'hyperframes/assets/vehicle-state.js').write_text(s)
(R/'hyperframes-demo/assets/vehicle-state.js').write_text(s)
