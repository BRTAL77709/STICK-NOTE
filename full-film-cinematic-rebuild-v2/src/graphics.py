"""Compact story-driven HUD and phrase captions. No fabricated CASH/SUSPICION stats."""
import math
from approved_components import text
from motion_state import *
WHITE='#f3f1e8';AMBER='#f5aa4f'
def panel(a,x,y,w,h,label,value,u=1,bar=None,unit=''):
 a.add(f'<g opacity="{u}" transform="translate({14*(1-u)} 0)">')
 a.path(f'M{x+12} {y} H{x+w} V{y+h-12} L{x+w-12} {y+h} H{x} V{y+12}Z','#07131d','#4b6470',1.8,'fill-opacity=".83"')
 a.path(f'M{x} {y+29} V{y+4} H{x+31}','none',AMBER,3)
 text(a,x+23,y+28,label,18,'#acbbc0',anchor='start',weight='bold')
 text(a,x+22,y+78,str(value),47,WHITE,anchor='start');text(a,x+w-18,y+76,unit,18,'#afc0c7',anchor='end')
 if bar is not None:
  a.rect(x+23,y+h-16,w-46,3,'#334b58');a.rect(x+23,y+h-16,(w-46)*clamp(bar),3,AMBER)
 a.add('</g>')
def hud(a,t,mode):
 if t<1.9:panel(a,88,235,270,100,'CEDAR DISTRICT','2:17',ease(t,.05,.3)*(1-ease(t,1.6,1.9)),unit='AM')
 if mode=='Street acceleration':
  u=ease(t,7,7.3)*(1-ease(t,9.7,10));v=state(t)['speed_kmh'];panel(a,88,235,274,113,'VELOCITY',f'{v:04.1f}',u,bar=v/100,unit='km/h')
 if mode=='Mirror threat':
  d=pursuit_distance(t);u=ease(t,10.1,10.35);panel(a,88,239,274,113,'VEHICLE BEHIND',f'{d:04.1f}',u,bar=1-d/40,unit='m')
def captions(a,t,segments,mode):
 import textwrap
 seg=next((s for s in segments if s['start']<=t<s['end']),None)
 if not seg:return
 fade=ease(t,seg['start'],seg['start']+.11)*(1-ease(t,seg['end']-.08,seg['end']))
 y=360 if mode=='Pedal' else 1510
 # Keep focal hierarchy: short phrase, small underline, emphasized action word only.
 a.add(f'<g opacity="{fade}" transform="translate(0 {10*(1-fade)})">')
 line=seg['text'];words=line.split();size=56
 from PIL import ImageFont
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',size);space=font.getlength(' ');widths=[font.getlength(w) for w in words];total=sum(widths)+(len(words)-1)*space;x=540-total/2
 a.rect(x-22,y-52,total+44,77,'#050f18',rx=9);a.path(f'M{x} {y+19} H{x+min(total,95)}','none',AMBER,2.5)
 for w,ww in zip(words,widths):
  color=AMBER if w.lower().strip('.,') in ['gas','followed','turn'] else WHITE
  text(a,x,y,w,size,color,anchor='start',stroke=1.5);x+=ww+space
 a.add('</g>')
