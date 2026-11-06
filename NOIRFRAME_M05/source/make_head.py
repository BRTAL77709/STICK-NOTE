from pathlib import Path
from svg import Art
from approved_head import head
from depth_render import DepthRaster
R=Path(__file__).resolve().parents[1];out=R/'assets/APPROVED_HEAD.png';assert not out.exists();a=Art();head(a,0,0,0,.94,.94,.35,0,blink_override=0);DepthRaster(512).native(''.join(a.s),(-300,-300,600,600),512,512).save(out);print(out)
