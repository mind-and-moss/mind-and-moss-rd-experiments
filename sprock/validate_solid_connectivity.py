# Solid connectivity by voxel. Vertex adjacency cannot see face-to-face
# contact between separately-built beds, so it reported stacked beds as
# disconnected. Voxels test the actual solid.
import bpy, sys
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())
PIECES=[("P1_base",["A1_platform","A2_marl"]),
        ("P2_mid", ["A3_cap","A4_bench","A5_parting"]),
        ("P3_crest",["A6_perch"]),
        ("WHOLE",  ["A1_platform","A2_marl","A3_cap","A4_bench","A5_parting","A6_perch"])]
def inside(ob,p):
    hits=0; o=ob.matrix_world.inverted() @ p; d=Vector((0,0,1))
    for _ in range(16):
        ok,loc,nor,idx=ob.ray_cast(o,d)
        if not ok: break
        hits+=1; o=loc+d*1e-5
    return hits%2==1
RES=5.0
print("\n--- SOLID CONNECTIVITY (voxel, 5 mm) ---")
allok=True
for pname,beds in PIECES:
    objs=[bpy.data.objects[b] for b in beds]
    zs=[]; xs=[]; ys=[]
    for o in objs:
        for c in o.bound_box:
            w=o.matrix_world @ Vector(c); xs.append(w.x/MM); ys.append(w.y/MM); zs.append(w.z/MM)
    x0,x1=min(xs)-RES,max(xs)+RES; y0,y1=min(ys)-RES,max(ys)+RES; z0,z1=min(zs)-RES,max(zs)+RES
    nx=int((x1-x0)/RES); ny=int((y1-y0)/RES); nz=int((z1-z0)/RES)
    sol=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
    tot=0
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                p=Vector(((x0+(i+.5)*RES)*MM,(y0+(j+.5)*RES)*MM,(z0+(k+.5)*RES)*MM))
                if any(inside(o,p) for o in objs):
                    sol[i][j][k]=True; tot+=1
    seen=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
    comps=0; sizes=[]
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if sol[i][j][k] and not seen[i][j][k]:
                    comps+=1; st=[(i,j,k)]; seen[i][j][k]=True; n=0
                    while st:
                        a,b,c=st.pop(); n+=1
                        for da,db,dc in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                            p2,q2,r2=a+da,b+db,c+dc
                            if 0<=p2<nx and 0<=q2<ny and 0<=r2<nz and sol[p2][q2][r2] and not seen[p2][q2][r2]:
                                seen[p2][q2][r2]=True; st.append((p2,q2,r2))
                    sizes.append(n)
    sizes.sort(reverse=True)
    ok = comps==1
    if not ok: allok=False
    vol=tot*RES**3/1000
    print(f"{pname:<9} vol={vol:7.1f} cm3  components={comps}  "
          f"sizes={sizes[:4]}   {'PASS' if ok else 'FAIL'}")
print(f"OVERALL: {'PASS - every print piece is one solid' if allok else 'FAIL'}")
