"""Extend House17 room floor without touching the inherited rig or its animation."""
import bpy,bmesh
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(R/'assets/STAIRCASE_M05_A02.blend'));scene=bpy.context.scene
faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box(n,x,y,z,dx,dy,dz,col):
 vv=[(x+i*dx,y+j*dy,z+k*dz) for i,j,k in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]];m=bpy.data.meshes.new(n);m.from_pydata(vv,[],faces);m.update();o=bpy.data.objects.new(n,m);scene.collection.objects.link(o);o['base_color']=col;mat=bpy.data.materials.new(n+'_CEL');mat.diffuse_color=tuple(int(col[i:i+2],16)/255 for i in [1,3,5])+(1,);m.materials.append(mat)
box('HOUSE17_ROOM_FLOOR',-1.50,-2.8,-.12,4.2,3.25,.12,'#2d4046')
for i,y in enumerate([-.65,-.98,-1.31,-1.64,-1.97,-2.30,-2.63]):
 box('FLOOR_BOARD_SEAM_'+str(i),-1.5,y,.0002,4.2,.003,.0002,'#1f3039')
 for j,x in enumerate([-.85+i%2*.35,.15+i%2*.35,1.15+i%2*.35]):box('FLOOR_BOARD_JOIN_'+str(i)+'_'+str(j),x,y,.0003,.003,.32,.0002,'#21343c')
scene.frame_set(0);out=R/'assets/M05_SET_FINISHED.blend';assert not out.exists();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
