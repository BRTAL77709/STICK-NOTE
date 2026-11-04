from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];normal=json.loads((R/'reports/REAL_MOTION_NORMAL_playback.json').read_text());slow=json.loads((R/'reports/REAL_MOTION_SLOW_playback.json').read_text())
for d,rate in [(normal,1),(slow,.5)]:assert d['ended'] and d['rate']==rate and d['corruptedFrames']==0 and d['duration']==86
video=R/'renders/final/THE_PRICE_OF_SILENCE_REAL_MOTION_REBUILD_86s.mp4';fidelity=json.loads((R/'reports/encoded-subject-fidelity.json').read_text());assert fidelity['ok'] and fidelity['file_sha256']==hashlib.sha256(video.read_bytes()).hexdigest()
p=R/'TECHNICAL_VALIDATION.md';p.write_text(p.read_text()+f"\nFull half-speed playback also ended normally at86 s, rate0.5, wall time{slow['wallTime']:.3f} s, with{slow['droppedFrames']} dropped presentation frames and{slow['corruptedFrames']} corrupted frames. Both complete presentation sheets were inspected. Artistic approval and voice listening remain pending.\n")
status={'technical_review_complete':True,'artistic_approval':'pending user review','voice_listening_verified':False,'full_film':str(video.relative_to(R)),'bytes':video.stat().st_size,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'normal_playback':normal,'slow_playback':slow,'downloads':'verification pending publication','production_stopped_for_user_review':True};(R/'FINAL_DELIVERY_STATUS.json').write_text(json.dumps(status,indent=2))
(R/'PROGRESS.md').write_text('''# Real-motion rebuild — review candidate complete

Five physical proofs A3/B4/C9/D4/E4 seconds and the integrated86-second film are rendered. Source/contact gates,2580-frame full decode, exact format checks,57 encoded subject comparisons, and full normal/half-speed browser playback passed. Actual presentation drops are retained in the reports. Contact sheets, joint/trajectory data, events, source and audit accompany the clips.

V10 clips and1039 baseline files remain unchanged. Three upper stairs are shown; twelve lower stairs are elided. Existing voices remain listening-unverified. No artistic approval is claimed. Publication/download verification is the only remaining delivery step; production stops for user review.
''')
(R/'CHECKPOINT.md').write_text('''# Delivery checkpoint

All production and technical reviews are complete. The new film exists at renders/final/THE_PRICE_OF_SILENCE_REAL_MOTION_REBUILD_86s.mp4; never regenerate or overwrite it. Final delivery status and proof/scene/current-source/composite/audio/encoding/playback/fidelity evidence are saved.

Publish the current curated package with scripts/publish_review.py (prior blobs cached; expected work head202eff93a966b08f6d70baea86e39cf325db35da), then scripts/verify_downloads.py. These append a new prefix and preserve every previous tree entry. Verify actual anonymous download bytes before claiming links. Record final verification separately if needed. All production stops for user review; artistic approval and voice listening remain pending. Lower stair flight is elided. V10 and previous work remain preserved.
''')
print(json.dumps({k:v for k,v in status.items() if 'playback' not in k},indent=2))
