"""Scene 06: They saw him; 24.0–28.0 seconds."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'engine/composition'))
from scene_builder import scene_svg
def render(t):
 return scene_svg(6,t)
