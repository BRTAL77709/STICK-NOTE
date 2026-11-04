from pathlib import Path
import json,argparse
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('scene',type=int);p.add_argument('--note',required=True);p.add_argument('--status',default='motion-reviewed-HD-candidate');args=p.parse_args();f=R/'SCENE_REPAIR_REGISTER.json';rows=json.loads(f.read_text());s=rows[args.scene-1]
 for stage in ['previews','final']:
  m=json.loads((R/'scenes'/f'scene_{args.scene:02d}'/f'{stage}-cache.json').read_text());report=R/'reports'/f'scene_{args.scene:02d}_{stage}_{m["fingerprint"]}_playback.json';r=json.loads(report.read_text());assert r['ended'] and r['rate']==1 and r['corruptedFrames']==0 and r['frames']==s['frames'];s[stage+'_evidence']=str(report.relative_to(R))
 s.update(status=args.status,source_gate=True,preview_gate=True,normal_playback_gate=True,frame_review_gate=True,technical_gate=True,artistic_approval='not approved by user',review_note=args.note,replacement=json.loads((R/'scenes'/f'scene_{args.scene:02d}'/'final-cache.json').read_text())['path'])
 f.write_text(json.dumps(rows,indent=2));(R/'SCENE_REPAIR_REGISTER.md').write_text('# Scene repair register\n\nTechnical checks never confer artistic approval. No new final master may be published until every replacement passes its individual gates.\n\n'+'\n\n'.join(f"## {s['scene']:02d} — {s['title']} ({s['start']:g}–{s['end']:g}s)\n\nBaseline: {s['baseline_problem']}\n\nRepair: {s['repair']}\n\nStatus: **{s['status']}**. {s.get('review_note','Not yet repaired or reviewed.')}\n\nReplacement: {s.get('replacement') or 'none'}. Artistic approval: {s['artistic_approval']}." for s in rows))
 timeline=[{'scene':s['scene'],'start':s['start'],'end':s['end'],'duration':s['duration'],'path':s['replacement'] or str(Path('../full-film-master-production')/json.loads((R/'scenes'/f'scene_{s["scene"]:02d}'/'final-cache.json').read_text())['path']),'replacement_validated':bool(s['replacement']),'status':s['status']} for s in rows];(R/'REPLACEMENT_TIMELINE.json').write_text(json.dumps({'duration':86,'fps':30,'final_export_allowed':False,'scenes':timeline},indent=2));print('Checkpoint scene',args.scene)
if __name__=='__main__':main()
