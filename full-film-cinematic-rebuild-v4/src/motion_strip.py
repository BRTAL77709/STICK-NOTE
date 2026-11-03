"""Quarter-second encoded driver/contact sequences, labelled with exact requested seek time."""
from pathlib import Path
from PIL import Image,ImageDraw
import subprocess
R=Path(__file__).resolve().parents[1];v=R/'THE_PRICE_OF_SILENCE_CINEMATIC_REBUILD_V4_15s.mp4'
out=Image.new('RGB',(1512,820),'#07131f');d=ImageDraw.Draw(out)
for row,times in enumerate([[2,2.25,2.5,2.75,3,3.25,3.3],[11.7,11.95,12.2,12.45,12.7,12.95,13.2]]):
 for j,t in enumerate(times):
  b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(v),'-frames:v','1','-vf','scale=216:384','-pix_fmt','rgb24','-f','rawvideo','pipe:1']);im=Image.frombytes('RGB',(216,384),b);out.paste(im,(j*216,row*410));d.text((j*216+5,row*410+387),f'{t:.2f}s',fill='white')
out.save(R/'DRIVER_MOTION_STRIP.jpg',quality=94)
