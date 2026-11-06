import ctypes as C,ctypes.util,math
from PIL import Image
from functools import lru_cache
@lru_cache(maxsize=None)
def _library(name):return C.CDLL(ctypes.util.find_library(name))
OUTLINE="#030b12"
def pt(p):return f"{p[0]:.3f},{p[1]:.3f}"
class Art:
 def __init__(self):self.s=[]
 def add(self,s):self.s.append(s)
 def path(self,d,fill='none',stroke=OUTLINE,w=5,extra=''):
  self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
 def poly(self,ps,fill,stroke=OUTLINE,w=5):self.add(f'<polygon points="{" ".join(pt(p) for p in ps)}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>')
 def line(self,ps,color,w):self.path('M'+' L'.join(pt(p) for p in ps),'none',color,w)
 def ellipse(self,x,y,rx,ry,fill,stroke='none',w=3,extra=''):self.add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>')
 def rect(self,x,y,w,h,fill,stroke='none',sw=3,rx=0):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

class Raster:
 def __init__(self,w,h):
  self.w=w;self.h=h;self.r=_library('rsvg-2');self.c=_library('cairo');self.g=_library('gobject-2.0')
  self.r.rsvg_handle_new_from_data.argtypes=[C.c_char_p,C.c_size_t,C.c_void_p];self.r.rsvg_handle_new_from_data.restype=C.c_void_p
  self.r.rsvg_handle_render_cairo.argtypes=[C.c_void_p,C.c_void_p];self.r.rsvg_handle_render_cairo.restype=C.c_int
  for name,args,ret in [('cairo_image_surface_create',[C.c_int,C.c_int,C.c_int],C.c_void_p),('cairo_create',[C.c_void_p],C.c_void_p),('cairo_scale',[C.c_void_p,C.c_double,C.c_double],None),('cairo_image_surface_get_data',[C.c_void_p],C.c_void_p),('cairo_surface_flush',[C.c_void_p],None),('cairo_destroy',[C.c_void_p],None),('cairo_surface_destroy',[C.c_void_p],None)]:
   f=getattr(self.c,name);f.argtypes=args;f.restype=ret
  self.g.g_object_unref.argtypes=[C.c_void_p]
 def render(self,svg):
  b=svg.encode();handle=self.r.rsvg_handle_new_from_data(b,len(b),None)
  surf=self.c.cairo_image_surface_create(0,self.w,self.h);ctx=self.c.cairo_create(surf);self.c.cairo_scale(ctx,self.w/1080,self.h/1920)
  if not self.r.rsvg_handle_render_cairo(handle,ctx):raise RuntimeError('SVG render failed')
  self.c.cairo_surface_flush(surf);buf=C.string_at(self.c.cairo_image_surface_get_data(surf),self.w*self.h*4)
  im=Image.frombytes('RGBA',(self.w,self.h),buf,'raw','BGRA').convert('RGB')
  self.c.cairo_destroy(ctx);self.c.cairo_surface_destroy(surf);self.g.g_object_unref(handle);return im
