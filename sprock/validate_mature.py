import bpy, bmesh, sys
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())
solids=[o for o in bpy.data.objects if o.type=='MESH' and len(o.data.polygons)>0]
rock=[o for o in solids if not o.name.startswith("talus")]
tal =[o for o in solids if o.name.startswith("talus")]
print(f"\n--- MATURE VALIDATION ---")
print(f"rock objects {len(rock)}, talus {len(tal)}")
bad=0; loose=0
for o in solids:
    bm=bmesh.new(); bm.from_mesh(o.data)
    b=[e for e in bm.edges if not e.is_manifold]
    l=[v for v in bm.verts if not v.link_edges]
    bad+=len(b); loose+=len(l); bm.free()
print(f"non-manifold edges {bad}, loose verts {loose}   "
      f"{'PASS' if bad==0 and loose==0 else 'FAIL'}")
def inside(ob,p):
    h=0; o=ob.matrix_world.inverted() @ p; d=Vector((0,0,1))
    for _ in range(16):
        ok,loc,nor,idx=ob.ray_cast(o,d)
        if not ok: break
        h+=1; o=loc+d*1e-5
    return h%2==1
RES=6.0
xs=[];ys=[];zs=[]
for o in rock:
    for c in o.bound_box:
        w=o.matrix_world @ Vector(c); xs.append(w.x/MM);ys.append(w.y/MM);zs.append(w.z/MM)
x0,x1=min(xs)-RES,max(xs)+RES; y0,y1=min(ys)-RES,max(ys)+RES; z0,z1=min(zs)-RES,max(zs)+RES
nx=int((x1-x0)/RES);ny=int((y1-y0)/RES);nz=int((z1-z0)/RES)
sol=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
tot=0
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            p=Vector(((x0+(i+.5)*RES)*MM,(y0+(j+.5)*RES)*MM,(z0+(k+.5)*RES)*MM))
            if any(inside(o,p) for o in rock): sol[i][j][k]=True; tot+=1
seen=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
comps=[]
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            if sol[i][j][k] and not seen[i][j][k]:
                st=[(i,j,k)]; seen[i][j][k]=True; n=0
                while st:
                    a,b2,c=st.pop(); n+=1
                    for da,db,dc in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                        p2,q2,r2=a+da,b2+db,c+dc
                        if 0<=p2<nx and 0<=q2<ny and 0<=r2<nz and sol[p2][q2][r2] and not seen[p2][q2][r2]:
                            seen[p2][q2][r2]=True; st.append((p2,q2,r2))
                comps.append(n)
comps.sort(reverse=True)
print(f"rock volume {tot*RES**3/1000:.0f} cm3")
print(f"solid components {len(comps)}, sizes {comps[:6]}")
print(f"connectivity: {'PASS - one mass' if len(comps)==1 else 'REVIEW - free-standing fragments'}")
