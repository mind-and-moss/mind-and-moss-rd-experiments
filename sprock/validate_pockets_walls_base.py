# ============================================================================
# MONSTER8 — FULL GATE RUN
#   A. sealed-pocket test  (exterior air masked off, so "no dead ends" is real)
#   B. wall-thickness ray probe (>= 1.2 mm at print scale)
#   C. flat-base check
# ============================================================================
import bpy, sys, math
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())

BEDS3=[bpy.data.objects[n] for n in
       ("A1_platform","A2_marl","A3_cap","A4_bench","A5_parting","A6_perch")]

def inside(ob,p):
    hits=0; o=ob.matrix_world.inverted() @ p; d=Vector((0,0,1))
    for _ in range(16):
        ok,loc,nor,idx=ob.ray_cast(o,d)
        if not ok: break
        hits+=1; o=loc+d*1e-5
    return hits%2==1

# ---------- A. sealed pockets --------------------------------------------
RES=5.0
x0,x1=-235.0,235.0; y0,y1=-150.0,150.0; z0,z1=0.0,196.0
nx=int((x1-x0)/RES); ny=int((y1-y0)/RES); nz=int((z1-z0)/RES)
free=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            p=Vector(((x0+(i+.5)*RES)*MM,(y0+(j+.5)*RES)*MM,(z0+(k+.5)*RES)*MM))
            free[i][j][k]= not any(inside(o,p) for o in BEDS3)

def flood(seeds):
    seen=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
    st=[]
    for s in seeds:
        if free[s[0]][s[1]][s[2]] and not seen[s[0]][s[1]][s[2]]:
            seen[s[0]][s[1]][s[2]]=True; st.append(s)
    n=0
    while st:
        i,j,k=st.pop(); n+=1
        for di,dj,dk in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            a,b,c=i+di,j+dj,k+dk
            if 0<=a<nx and 0<=b<ny and 0<=c<nz and free[a][b][c] and not seen[a][b][c]:
                seen[a][b][c]=True; st.append((a,b,c))
    return seen,n

# exterior = everything reachable from the grid boundary
border=[]
for i in range(nx):
    for j in range(ny):
        border += [(i,j,nz-1)]
for i in range(nx):
    for k in range(nz):
        border += [(i,0,k),(i,ny-1,k)]
for j in range(ny):
    for k in range(nz):
        border += [(0,j,k),(nx-1,j,k)]
ext,next_ = flood(border)
total=sum(free[i][j][k] for i in range(nx) for j in range(ny) for k in range(nz))
sealed=total-next_
print("--- A. SEALED POCKETS ---")
print(f"grid {nx}x{ny}x{nz} @ {RES:.0f}mm   free cells {total}")
print(f"reachable from outside : {next_}")
print(f"SEALED POCKETS         : {sealed} cells "
      f"({sealed*RES**3/1000:.1f} cm3)   "
      f"{'PASS - no dead ends' if sealed==0 else 'FAIL'}")

# ---------- B. wall thickness ray probe ----------------------------------
print("\n--- B. WALL THICKNESS (ray probe) ---")
import random
random.seed(7)
worst=(1e9,None,None)
samples=0; thin=0
for ob in BEDS3:
    polys=list(ob.data.polygons)
    if not polys: continue
    step=max(1,len(polys)//220)
    for f in polys[::step]:
        c=ob.matrix_world @ f.center
        n=(ob.matrix_world.to_3x3() @ f.normal).normalized()
        o=c - n*0.0002                      # step just inside the surface
        ok,loc,nor,idx = ob.ray_cast(ob.matrix_world.inverted() @ o,
                                     ob.matrix_world.inverted().to_3x3() @ (-n))
        if not ok: continue
        d=((ob.matrix_world @ loc)-c).length/MM
        samples+=1
        if d < 1.2: thin+=1
        if d < worst[0]: worst=(d, ob.name, tuple(round(v/MM) for v in c))
print(f"samples probed : {samples}")
print(f"below 1.2 mm   : {thin}")
print(f"thinnest       : {worst[0]:.2f} mm on {worst[1]} at {worst[2]}")
print(f"VERDICT        : {'PASS' if thin==0 else 'REVIEW'}")

# ---------- C. flat base --------------------------------------------------
print("\n--- C. FLAT BASE ---")
zs=[]
for ob in BEDS3:
    for v in ob.data.vertices:
        zs.append((ob.matrix_world @ v.co).z/MM)
base=min(zs)
onbase=sum(1 for z in zs if z < base+0.5)
print(f"lowest z = {base:.2f} mm, {onbase} verts on the base plane")
print(f"VERDICT  : {'PASS - flat base for supportless printing' if abs(base)<0.6 and onbase>20 else 'REVIEW'}")
