"""Compare actual encoded frames; timings are action comparisons, not exact pose matches."""
from pathlib import Path
import subprocess,json,io
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];old=R.parent/'full-film-real-motion-rebuild/renders/final/THE_PRICE_OF_SILENCE_REAL_MOTION_REBUILD_86s.mp4';shots=json.loads((R/'CURRENT_SHOTS.json').read_text());plans={'A':([32.8,35.5,38.8,40.8],[.5,1.8,2.8,4.3]),'B':([49.6,51.7,54.5,57.7],[.9,2.2,3.9,6.4]),'C':([62.3,64.0,66.6,68.8],[.9,2.4,5.7,7.7])};font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def frame(path,t):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=216:384','-f','image2pipe','-vcodec','png','-threads','1','pipe:1']);return Image.open(io.BytesIO(b)).convert('RGB')
for k,(before,after) in plans.items():
 sheet=Image.new('RGB',(864,870),'#06131e');draw=ImageDraw.Draw(sheet);draw.text((10,8),f'{k} · REJECTED BASELINE — action comparison, different timing',font=font,fill='white')
 for j,t in enumerate(before):sheet.paste(frame(old,t),(j*216,40));draw.text((j*216+6,425),f'Old {t:.2f}s',font=font,fill='white')
 for j,t in enumerate(after):sheet.paste(frame(R/shots[k]['final'],t),(j*216,480));draw.text((j*216+6,845),f'Native {t:.2f}s',font=font,fill='white')
 draw.text((10,452),'NEW BLENDER PROOF — not artistic approval',font=font,fill='#edac57');sheet.save(R/f'reviews/BEFORE_AFTER_{k}.jpg',quality=94)
(R/'reports/comparison-frame-times.json').write_text(json.dumps({'baseline':str(old),'plans':plans,'exact_pose_alignment':False},indent=2))
print('Actual encoded before/after frames extracted')
