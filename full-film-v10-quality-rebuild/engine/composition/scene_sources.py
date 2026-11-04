"""Load each editable scene entry point for picture rendering."""
from functools import lru_cache
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]

@lru_cache(maxsize=18)
def _module(scene_id):
    if not 1 <= scene_id <= 18:
        raise ValueError('Scene ID must be 1 through 18')
    path = ROOT / 'scenes' / f'scene_{scene_id:02d}' / 'scene.py'
    spec = importlib.util.spec_from_file_location(f'noirframe_scene_{scene_id:02d}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def evaluate(scene_id, local_time):
    return _module(scene_id).render(local_time)
