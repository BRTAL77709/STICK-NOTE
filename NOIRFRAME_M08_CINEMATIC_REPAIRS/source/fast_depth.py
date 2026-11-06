"""Free local C++ depth raster; same world-space geometry, not image warping."""
from pathlib import Path
import importlib.util,ctypes as C
import numpy as np
from PIL import ImageColor
from functools import lru_cache
_rgb=lru_cache(maxsize=None)(ImageColor.getrgb)
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m07_depth_base',R/'depth_render.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
lib=C.CDLL(str(R/'fast_raster.so'));P=C.POINTER(C.c_float);U=C.POINTER(C.c_uint8)
lib.triangle.argtypes=[U,P,C.c_int,C.c_int,P,P,P,C.c_int,C.c_int,C.c_int,C.c_int];lib.segment.argtypes=[U,P,C.c_int,C.c_int,P,P,C.c_int,C.c_int,C.c_int,C.c_float,C.c_float,C.c_int]
class FastDepth(base.DepthRaster):
 def render(self,w,overlay=None):
  self.projection_cache={}
  return super().render(w,overlay)
 def project(self,p):
  key=tuple(p)
  if key not in self.projection_cache:self.projection_cache[key]=super().project(p)
  return self.projection_cache[key]

 def triangle(self,a,b,c,col):
  if col=='none':return
  aa,bb,cc=[np.ascontiguousarray(q,dtype=np.float32) for q in [a,b,c]];rgb=_rgb(col);lib.triangle(self.color.ctypes.data_as(U),self.depth.ctypes.data_as(P),self.w,self.h,aa.ctypes.data_as(P),bb.ctypes.data_as(P),cc.ctypes.data_as(P),*rgb,int(getattr(self.cam,'is_orthographic',False)))
 def segment(self,a,b,col,width,bias=0):
  aa,bb=[np.ascontiguousarray(q,dtype=np.float32) for q in [a,b]];rgb=_rgb(col);lib.segment(self.color.ctypes.data_as(U),self.depth.ctypes.data_as(P),self.w,self.h,aa.ctypes.data_as(P),bb.ctypes.data_as(P),*rgb,float(width),float(bias),int(getattr(self.cam,'is_orthographic',False)))
