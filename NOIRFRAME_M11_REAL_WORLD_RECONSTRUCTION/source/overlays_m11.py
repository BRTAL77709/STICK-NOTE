from bootstrap import ROOT as R
from PIL import ImageDraw,ImageFont
from dialogue_m11 import CUES
import wave,textwrap
DUR={}
def duration(name):
 if name not in DUR:
  with wave.open(str(R/'sound/voices'/name)) as w:DUR[name]=w.getnframes()/w.getframerate()
 return DUR[name]
def apply(im,shot,t):
 dr=ImageDraw.Draw(im);s=im.width/1080
 if shot=='PHONE_CALL' and t<3.9:
  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',round(38*s));dr.rounded_rectangle((180*s,150*s,900*s,245*s),radius=18*s,fill='#0b2939',outline='#77a5ae',width=max(1,round(2*s)));dr.text((540*s,197*s),'UNKNOWN NUMBER',font=font,fill='#e2e8df',anchor='mm')
 for start,name,txt in CUES.get(shot,[]):
  if not start<=t<start+duration(name):continue
  rows=textwrap.wrap(txt,width=30);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',round(43*s));y=1690-(len(rows)-1)*30;dr.rounded_rectangle((80*s,(y-50)*s,1000*s,(y+len(rows)*58)*s),radius=15*s,fill='#071923')
  for k,row in enumerate(rows):dr.text((540*s,(y+k*58)*s),row,font=font,fill='#e9dfc8',anchor='mm')
 return im
