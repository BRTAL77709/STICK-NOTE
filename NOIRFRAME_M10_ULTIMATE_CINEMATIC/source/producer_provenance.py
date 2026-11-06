from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];core=['render_clips.py','sets.py','cameras.py','cameras_base_R07.py','view_head.py','approved_head_view.py','vehicle_system.py','native_style.py','stair_style.py','fast_depth.py','fast_raster.cpp'];rows={}
for p in (R/'reports').glob('M07_*_1080_RENDER.json'):
 d=json.loads(p.read_text());diff=[]
 for n in core:
  key='source/'+n
  if key in d['source_sha256'] and hashlib.sha256((R/key).read_bytes()).hexdigest()!=d['source_sha256'][key]:diff.append(key)
 rows[d['shot']]={'render_report':str(p.relative_to(R)),'recorded_controller_snapshot':d.get('controller_snapshot'),'selected_native_tag':d.get('selected_native_tag','INHERITED_M05'),'core_producer_changes_since_render':diff,'source_frame_hashes':len(d['source_frame_sha256'])}
# Road/stair were deliberately retained from an earlier reviewed pass: later face-view/POV edits are not active for those outputs.
for s in ['ROAD_BUILDINGS','STAIRS']:
 if s in rows:rows[s]['explanation']='Retained prior M07 pass. Later actor-face/POV overrides are not used by this shot. Exact recorded producer hashes remain in its render report.'
(R/'reports/PRODUCER_PROVENANCE.json').write_text(json.dumps(rows,indent=2));print(rows)
