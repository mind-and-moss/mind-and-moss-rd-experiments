import bpy, bmesh, sys, math
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())
rock=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith("talus")
      and len(o.data.polygons)>0]
tal=[o for o in bpy.data.objects if o.name.startswith("talus")]

def inside(ob,p):
    h=0; o=ob.matrix_world.inverted() @ p; d=Vector((0,0,1))
    for _ in range(18):
        ok,loc,nor,idx=ob.ray_cast(o,d)
        if not ok: break
        h+=1; o=loc+d*1e-5
    return h%2==1

print("\n=== FINAL GATE RUN (story-conformant build) ===")

# --- flat base -----------------------------------------------------------
zs=[(o.matrix_world @ v.co).z/MM for o in rock for v in o.data.vertices]
base=min(zs); onbase=sum(1 for z in zs if z<base+0.5)
print(f"[BASE ] lowest z {base:.2f} mm, {onbase} verts on plane   "
      f"{'PASS' if abs(base)<0.6 and onbase>20 else 'REVIEW'}")

# --- wall thickness ------------------------------------------------------
worst=(1e9,None); thin=0; n=0
for ob in rock:
    polys=list(ob.data.polygons); step=max(1,len(polys)//200)
    for f in polys[::step]:
        c=ob.matrix_world @ f.center
        nr=(ob.matrix_world.to_3x3() @ f.normal).normalized()
        ok,loc,nor,idx=ob.ray_cast(ob.matrix_world.inverted() @ (c-nr*0.0002),
                                   ob.matrix_world.inverted().to_3x3() @ (-nr))
        if not ok: continue
        d=((ob.matrix_world @ loc)-c).length/MM; n+=1
        if d<1.2: thin+=1
        if d<worst[0]: worst=(d,ob.name)
print(f"[WALL ] {n} samples, {thin} under 1.2mm, thinnest {worst[0]:.2f}mm ({worst[1]})   "
      f"{'PASS' if thin==0 else 'REVIEW'}")

# --- sealed pockets ------------------------------------------------------
RES=6.0
xs=[];ys=[];zz=[]
for o in rock:
    for c in o.bound_box:
        w=o.matrix_world @ Vector(c); xs.append(w.x/MM);ys.append(w.y/MM);zz.append(w.z/MM)
x0,x1=min(xs)-2*RES,max(xs)+2*RES; y0,y1=min(ys)-2*RES,max(ys)+2*RES
z0,z1=min(zz)-2*RES,max(zz)+2*RES
nx=int((x1-x0)/RES);ny=int((y1-y0)/RES);nz=int((z1-z0)/RES)
free=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            p=Vector(((x0+(i+.5)*RES)*MM,(y0+(j+.5)*RES)*MM,(z0+(k+.5)*RES)*MM))
            free[i][j][k]= not any(inside(o,p) for o in rock)
def flood(seeds):
    seen=[[[False]*nz for _ in range(ny)] for _ in range(nx)]; st=[]
    for s2 in seeds:
        if free[s2[0]][s2[1]][s2[2]] and not seen[s2[0]][s2[1]][s2[2]]:
            seen[s2[0]][s2[1]][s2[2]]=True; st.append(s2)
    n2=0
    while st:
        i,j,k=st.pop(); n2+=1
        for di,dj,dk in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            a,b,c=i+di,j+dj,k+dk
            if 0<=a<nx and 0<=b<ny and 0<=c<nz and free[a][b][c] and not seen[a][b][c]:
                seen[a][b][c]=True; st.append((a,b,c))
    return seen,n2
border=[(i,j,nz-1) for i in range(nx) for j in range(ny)]
border+=[(i,0,k) for i in range(nx) for k in range(nz)]
border+=[(i,ny-1,k) for i in range(nx) for k in range(nz)]
border+=[(0,j,k) for j in range(ny) for k in range(nz)]
border+=[(nx-1,j,k) for j in range(ny) for k in range(nz)]
ext,ne=flood(border)
tot=sum(free[i][j][k] for i in range(nx) for j in range(ny) for k in range(nz))
sealed=tot-ne
print(f"[VOID ] sealed pockets {sealed} cells ({sealed*RES**3/1000:.1f} cm3)   "
      f"{'PASS - no dead ends' if sealed==0 else 'FAIL'}")

# --- solid connectivity per print layer ----------------------------------
LAYERS=[("L1_base",["A1_platform","A2_marl"]),
        ("L2_mid", ["A3_cap","A4_bench","A5_parting"]),
        ("L3_crest",["A6_perch"])]
print("[SOLID] connectivity per print layer:")
allok=True
for lname,beds in LAYERS:
    objs=[o for o in rock if any(o.name.startswith(b) for b in beds)]
    if not objs: continue
    xs2=[];ys2=[];zs2=[]
    for o in objs:
        for c in o.bound_box:
            w=o.matrix_world @ Vector(c); xs2.append(w.x/MM);ys2.append(w.y/MM);zs2.append(w.z/MM)
    a0,a1=min(xs2)-RES,max(xs2)+RES; b0,b1=min(ys2)-RES,max(ys2)+RES; c0,c1=min(zs2)-RES,max(zs2)+RES
    mx=int((a1-a0)/RES);my=int((b1-b0)/RES);mz=int((c1-c0)/RES)
    sol=[[[False]*mz for _ in range(my)] for _ in range(mx)]
    for i in range(mx):
        for j in range(my):
            for k in range(mz):
                p=Vector(((a0+(i+.5)*RES)*MM,(b0+(j+.5)*RES)*MM,(c0+(k+.5)*RES)*MM))
                if any(inside(o,p) for o in objs): sol[i][j][k]=True
    seen=[[[False]*mz for _ in range(my)] for _ in range(mx)]; comps=[]
    for i in range(mx):
        for j in range(my):
            for k in range(mz):
                if sol[i][j][k] and not seen[i][j][k]:
                    st=[(i,j,k)]; seen[i][j][k]=True; cnt=0
                    while st:
                        a,b2,c=st.pop(); cnt+=1
                        for da,db,dc in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                            p2,q2,r2=a+da,b2+db,c+dc
                            if 0<=p2<mx and 0<=q2<my and 0<=r2<mz and sol[p2][q2][r2] and not seen[p2][q2][r2]:
                                seen[p2][q2][r2]=True; st.append((p2,q2,r2))
                    comps.append(cnt)
    comps.sort(reverse=True)
    ok=len(comps)==1
    if not ok: allok=False
    print(f"         {lname:<9} components={len(comps)} sizes={comps[:3]}  {'PASS' if ok else 'REVIEW'}")
print(f"[SOLID] overall {'PASS' if allok else 'REVIEW'}")
print(f"[COUNT] rock laminae {len(rock)}, talus {len(tal)}")
