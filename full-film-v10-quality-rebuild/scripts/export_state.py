from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'engine/animation'))
from motion_state import vehicleState
records=[{'frame':f,**vehicleState(f/30)} for f in range(2581)]
(R/'hyperframes/assets/vehicle-state.js').write_text('window.VEHICLE_FRAMES='+json.dumps(records,separators=(',',':'))+';')
