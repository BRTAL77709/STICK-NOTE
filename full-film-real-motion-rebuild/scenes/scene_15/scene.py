"""Scene 15: Curtain grip / reveal / reaction; 65.4–69.4 seconds."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import scene_svg
def render(t):
 return scene_svg(15,t)
