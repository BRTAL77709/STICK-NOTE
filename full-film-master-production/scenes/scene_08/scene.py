"""Scene 08: Pursuit; 32.0–37.0 seconds."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import scene_svg
def render(t):
 return scene_svg(8,t)
