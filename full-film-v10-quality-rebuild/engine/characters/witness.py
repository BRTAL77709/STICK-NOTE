from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"animation"))
from actor import actor,gait,stair_gait
from driver_rig import head,pose,driver
