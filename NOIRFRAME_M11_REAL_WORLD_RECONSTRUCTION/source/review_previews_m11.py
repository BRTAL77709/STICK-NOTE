from bootstrap import ROOT as R
import json,time,subprocess,sys
import actions
rows={};selected=json.loads((R/'configuration/selected_native.json').read_text());revision=json.loads((R/'configuration/render_revision.json').read_text())['revision']
for shot,duration in actions.DURATIONS.items():
 if shot=='DRIVER_CHASE':continue
 rev=revision;rows[shot]={'duration':duration,'preview':f'renders/M11_{shot}_{rev}_PREVIEW_360.mp4','final':f'renders/M11_{shot}_{rev}_FINAL.mp4'}
(R/'CURRENT_SHOTS.json').write_text(json.dumps(rows,indent=2))
# Independent groups write results as soon as each review group is done.
for g,shots in enumerate([['DRIVING_COCKPIT','ROAD_BUILDINGS','CAR_CHASE','CAR_EXIT_RUNNING','KEY_LOCK'],['DOOR_ENTRY','STAIRS','WINDOW_CURTAIN','PHONE_CALL'],['UNKNOWN_CALLER','DISCOVERY','PANIC','ARRIVAL','FINAL_POLL']],1):
 for shot in shots:
  rev=revision
  while not (R/'reports'/f'M11_{shot}_{rev}_PREVIEW_360_RENDER.json').exists():time.sleep(2)
 subprocess.run([sys.executable,str(R/'source/review_playback.py'),'--stage','preview','--tag','M11_REVIEW_'+str(g),'--shots',*shots,'--rates','1','.5'],check=True)
