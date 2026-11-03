"""Role-matched encoded frames, preserving each version's actual timing."""
from pathlib import Path
import subprocess,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BEFORE=ROOT.parent/'full-film-cinematic-rebuild-v3/THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V3_15s.mp4';AFTER=ROOT/'THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4'
def frame(path,t):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=180:320','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);return Image.frombytes('RGB',(180,320),raw)
def main():
 roles=['DEPARTURE','DRIVER','PEDAL','CLUSTER','ACCELERATION','REARVIEW','CORNER']
 times=[[1.,2.7,3.6,5.5,8.5,11.4,14.5],[1.,2.65,3.9,5.4,7.5,10.5,14.5]]
 out=Image.new('RGB',(1260,740),'#081621');d=ImageDraw.Draw(out)
 for row,path in enumerate([BEFORE,AFTER]):
  for j,(lab,t) in enumerate(zip(roles,times[row])):
   x=j*180;y=row*370;out.paste(frame(path,t),(x,y+25));d.text((x+6,y+6),f'{"V3" if row==0 else "V4"} / {lab}',fill='#e6bb7d');d.text((x+6,y+349),f'{t:.2f}s encoded frame',fill='white')
 dest=ROOT/'V3_V4_COMPARISON.jpg';assert not dest.exists();out.save(dest,quality=94);print(dest)
if __name__=='__main__':main()
