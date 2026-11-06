"""Per-pixel perspective depth rasterizer for illustrated polygons and ink lines.
Fixes painter-sort failures at hands/door, furniture/window and stair contacts.
"""
import numpy as np,math,ctypes as C
from PIL import Image,ImageColor
from svg import Art,Raster
class DepthRaster:
 def __init__(self,width=540,height=None):
  self.w=width;self.h=round(width*16/9) if height is None else height;self.s=width/1080;self.glyphcache={};self.backgrounds={}
 def render(self,w,overlay=None):
  self.cam=w.cam;self.color=np.full((self.h,self.w,3),[9,27,42],np.uint8);self.depth=np.full((self.h,self.w),1e7,np.float32)
  glyph=[];key=getattr(w,'cache_key',None);prefix=getattr(w,'cache_prefix',0);cached=self.backgrounds.get(key) if key is not None else None
  start=0
  if cached is not None:self.color=cached[0].copy();self.depth=cached[1].copy();glyph=list(cached[2]);start=prefix
  for idx,op in enumerate(w.ops[start:],start):
   if op[0]=='face':
    _,pts,col,stroke,sw=op;pp=[self.project(p) for p in pts]
    for k in range(1,len(pp)-1):self.triangle(pp[0],pp[k],pp[k+1],col)
    if stroke!='none':
     for a,b in zip(pp,pp[1:]+pp[:1]):self.segment(a,b,stroke,sw*self.s,-.0015)
   elif op[0]=='line':
    _,pts,col,sw,bias=op;pp=[self.project(p) for p in pts]
    for a,b in zip(pp,pp[1:]):self.segment(a,b,col,sw*self.s,bias-.003)
   else:glyph.append(op)
   if key is not None and idx+1==prefix and cached is None:
    if len(self.backgrounds)>=2:self.backgrounds.clear()
    self.backgrounds[key]=(self.color.copy(),self.depth.copy(),list(glyph))
  for op in sorted(glyph,key=lambda op:-sum(self.cam.depth(p) for p in op[1])/len(op[1])):self.glyph(op)
  im=Image.fromarray(self.color)
  # Atmospheric overlay only; never changes character/world positions.
  if overlay:
   a=Art();overlay(a);tile=self.native(''.join(a.s),(0,0,1080,1920),self.w,self.h);im=Image.alpha_composite(im.convert('RGBA'),tile).convert('RGB')
  return im
 def project(self,p):
  x,y=self.cam(p);return np.array([x*self.s,y*self.s,self.cam.depth(p)],dtype=np.float32)
 def roi(self,points,pad=0):
  x0=max(0,int(min(p[0] for p in points)-pad));y0=max(0,int(min(p[1] for p in points)-pad));x1=min(self.w,int(max(p[0] for p in points)+pad)+2);y1=min(self.h,int(max(p[1] for p in points)+pad)+2)
  if x1<=x0 or y1<=y0:return None
  xx=np.arange(x0,x1,dtype=np.float32)[None,:]+.5;yy=np.arange(y0,y1,dtype=np.float32)[:,None]+.5;return x0,y0,x1,y1,xx,yy
 def paint(self,roi,z,mask,col):
  x0,y0,x1,y1,xx,yy=roi;dep=self.depth[y0:y1,x0:x1];mask=mask&(z<=dep+.00005)&(z>.08)
  self.color[y0:y1,x0:x1][mask]=ImageColor.getrgb(col);dep[mask]=z[mask] if isinstance(z,np.ndarray) else z
 def triangle(self,a,b,c,col):
  roi=self.roi([a,b,c]);
  if roi is None or col=='none':return
  x0,y0,x1,y1,xx,yy=roi
  if min(a[2],b[2],c[2])>float(self.depth[y0:y1,x0:x1].max()):return
  den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);
  if abs(den)<1e-8:return
  u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den;v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;z=(u*a[2]+v*b[2]+(1-u-v)*c[2]) if getattr(self.cam,'is_orthographic',False) else np.divide(1.,u/a[2]+v/b[2]+(1-u-v)/c[2],out=np.full_like(u+v,np.inf),where=np.abs(u/a[2]+v/b[2]+(1-u-v)/c[2])>1e-12);self.paint(roi,z,(u>=0)&(v>=0)&(u+v<=1),col)
 def segment(self,a,b,col,width,bias=0):
  roi=self.roi([a,b],width/2+1)
  if roi is None:return
  *_,xx,yy=roi;dx=b[0]-a[0];dy=b[1]-a[1];den=dx*dx+dy*dy
  t=np.clip(((xx-a[0])*dx+(yy-a[1])*dy)/max(den,1e-8),0,1);dist=(xx-a[0]-t*dx)**2+(yy-a[1]-t*dy)**2;z=((1-t)*a[2]+t*b[2] if getattr(self.cam,'is_orthographic',False) else 1/((1-t)/a[2]+t/b[2]))+bias;self.paint(roi,z,dist<max(.55,width/2)**2,col)
 def native(self,body,box,width,height):
  x,y,bw,bh=box;svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{x} {y} {bw} {bh}"><defs><linearGradient id="face"><stop stop-color="#f1ede4"/><stop offset="1" stop-color="#a6b7bd"/></linearGradient><radialGradient id="amber"><stop stop-color="#efb96b" stop-opacity=".25"/><stop offset="1" stop-color="#efb96b" stop-opacity="0"/></radialGradient></defs>{body}</svg>'
  r=Raster(width,height);bb=svg.encode();handle=r.r.rsvg_handle_new_from_data(bb,len(bb),None);surf=r.c.cairo_image_surface_create(0,width,height);ctx=r.c.cairo_create(surf);r.r.rsvg_handle_render_cairo(handle,ctx);r.c.cairo_surface_flush(surf);buf=C.string_at(r.c.cairo_image_surface_get_data(surf),width*height*4);im=Image.frombytes('RGBA',(width,height),buf,'raw','BGRA');r.c.cairo_destroy(ctx);r.c.cairo_surface_destroy(surf);r.g.g_object_unref(handle);return im
 def glyph(self,op):
  _,pts,fn,bias=op;p=np.mean(pts,axis=0);x,y=self.cam(p);ss=self.cam.scale(p);rad=max(20,ss*.56);box=(x-rad,y-rad,rad*2,rad*2);x0=round(box[0]*self.s);y0=round(box[1]*self.s);size=max(1,round(rad*2*self.s));a=Art();fn(a);body=''.join(a.s);tile=self.native(body,box,size,size);rgba=np.array(tile);z=self.cam.depth(p)+bias
  xx0=max(0,x0);yy0=max(0,y0);xx1=min(self.w,x0+size);yy1=min(self.h,y0+size)
  if xx1<=xx0 or yy1<=yy0:return
  rgba=rgba[yy0-y0:yy1-y0,xx0-x0:xx1-x0];alpha=rgba[:,:,3:4]/255.;dep=self.depth[yy0:yy1,xx0:xx1];alpha*= (z<=dep+.02)[:,:,None];dst=self.color[yy0:yy1,xx0:xx1];dst[:]=(rgba[:,:,:3]+dst*(1-alpha)).clip(0,255).astype(np.uint8) if False else (rgba[:,:,:3]*alpha+dst*(1-alpha)).astype(np.uint8)
