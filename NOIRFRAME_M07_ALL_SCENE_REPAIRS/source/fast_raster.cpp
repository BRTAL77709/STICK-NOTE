#include <cmath>
#include <algorithm>
#include <cstdint>
extern "C" void triangle(uint8_t*rgb,float*depth,int W,int H,const float*a,const float*b,const float*c,int r,int g,int bl,int ortho){
 int x0=std::max(0,(int)std::floor(std::min({a[0],b[0],c[0]}))),x1=std::min(W-1,(int)std::ceil(std::max({a[0],b[0],c[0]})));int y0=std::max(0,(int)std::floor(std::min({a[1],b[1],c[1]}))),y1=std::min(H-1,(int)std::ceil(std::max({a[1],b[1],c[1]})));float den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);if(std::abs(den)<1e-8)return;
 for(int y=y0;y<=y1;y++)for(int x=x0;x<=x1;x++){float u=((b[1]-c[1])*(x+.5f-c[0])+(c[0]-b[0])*(y+.5f-c[1]))/den,v=((c[1]-a[1])*(x+.5f-c[0])+(a[0]-c[0])*(y+.5f-c[1]))/den;if(u<0||v<0||u+v>1)continue;float z=ortho?u*a[2]+v*b[2]+(1-u-v)*c[2]:1/(u/a[2]+v/b[2]+(1-u-v)/c[2]);int i=y*W+x;if(z>.08f&&z<=depth[i]+.00005f){depth[i]=z;rgb[3*i]=r;rgb[3*i+1]=g;rgb[3*i+2]=bl;}}
}
extern "C" void segment(uint8_t*rgb,float*depth,int W,int H,const float*a,const float*b,int r,int g,int bl,float width,float bias,int ortho){
 float rad=std::max(.55f,width*.5f);int x0=std::max(0,(int)std::floor(std::min(a[0],b[0])-rad)),x1=std::min(W-1,(int)std::ceil(std::max(a[0],b[0])+rad));int y0=std::max(0,(int)std::floor(std::min(a[1],b[1])-rad)),y1=std::min(H-1,(int)std::ceil(std::max(a[1],b[1])+rad));float dx=b[0]-a[0],dy=b[1]-a[1],den=std::max(1e-8f,dx*dx+dy*dy);
 for(int y=y0;y<=y1;y++)for(int x=x0;x<=x1;x++){float t=std::clamp(((x+.5f-a[0])*dx+(y+.5f-a[1])*dy)/den,0.f,1.f);float xx=x+.5f-a[0]-t*dx,yy=y+.5f-a[1]-t*dy;if(xx*xx+yy*yy>=rad*rad)continue;float z=(ortho?(1-t)*a[2]+t*b[2]:1/((1-t)/a[2]+t/b[2]))+bias;int i=y*W+x;if(z>.08f&&z<=depth[i]+.00005f){depth[i]=z;rgb[3*i]=r;rgb[3*i+1]=g;rgb[3*i+2]=bl;}}
}
