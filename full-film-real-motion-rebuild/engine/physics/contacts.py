from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"animation"))
from illustration_engine import ik,limb
from v10_trunk import ik3,foot_world,contacts
from house17 import doorPoint,hardware
