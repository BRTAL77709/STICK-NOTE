"""Scene 16: Phone acquisition / lift / million-dollar offer; 69.4–77.3 seconds."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import scene_svg
def render(t):
 return scene_svg(16,t)
