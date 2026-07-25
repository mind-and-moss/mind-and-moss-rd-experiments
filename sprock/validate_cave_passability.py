# ============================================================================
# 3D PASSABILITY VALIDATOR  -- the volumetric form of iron rule 4.
#
# Voxelises the cave void, floods from the mouth, and checks:
#   - the tail exit is reachable from the mouth
#   - there are no sealed pockets
#   - the NARROWEST constriction on the route, so "passable-or-impossible"
#     is measured rather than assumed
# ============================================================================
import bpy, sys, math
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())

BEDS3=[bpy.data.objects[n] for n in
       ("A1_platform","A2_marl","A3_cap","A4_bench","A5_parting","A6_perch")]

def inside(ob, p):
    """Parity test: cast up, count crossings."""
    hits=0; origin=ob.matrix_world.inverted() @ p; d=Vector((0,0,1))
    o=origin.copy()
    for _ in range(16):
        ok,loc,nor,idx = ob.ray_cast(o, d)
        if not ok: break
        hits+=1; o = loc + d*1e-5
    return hits % 2 == 1

RES=4.0
x0,x1 = MOUTH_X-60, MOUTH_X+240
y0,y1 = -D/2-20, 60.0
z0,z1 = 26.0, 61.0
nx=int((x1-x0)/RES); ny=int((y1-y0)/RES); nz=int((z1-z0)/RES)
print(f"grid {nx} x {ny} x {nz} = {nx*ny*nz} cells at {RES:.0f} mm")

free=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            p=Vector(((x0+(i+.5)*RES)*MM,(y0+(j+.5)*RES)*MM,(z0+(k+.5)*RES)*MM))
            free[i][j][k] = not any(inside(o,p) for o in BEDS3)

# seed: free cells on the front plane near the mouth
seed=None
for i in range(nx):
    for k in range(nz):
        if free[i][0][k] and abs((x0+(i+.5)*RES)-MOUTH_X) < 40:
            seed=(i,0,k); break
    if seed: break
print("seed at mouth:", "found" if seed else "NOT FOUND")

seen=[[[False]*nz for _ in range(ny)] for _ in range(nx)]
n=0
if seed:
    st=[seed]; seen[seed[0]][seed[1]][seed[2]]=True
    while st:
        i,j,k=st.pop(); n+=1
        for di,dj,dk in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            a,b,c=i+di,j+dj,k+dk
            if 0<=a<nx and 0<=b<ny and 0<=c<nz and free[a][b][c] and not seen[a][b][c]:
                seen[a][b][c]=True; st.append((a,b,c))

total=sum(free[i][j][k] for i in range(nx) for j in range(ny) for k in range(nz))
# does the flood reach the far end (tail exit region)?
tail_x = MOUTH_X+206
reach_tail=any(seen[i][j][k] for i in range(nx) for j in range(ny) for k in range(nz)
               if abs((x0+(i+.5)*RES)-tail_x)<25 and (y0+(j+.5)*RES) < -D/2+6)
print(f"free cells        : {total}")
print(f"reached from mouth: {n}")
print(f"MOUTH -> TAIL     : {'PASS' if reach_tail else 'FAIL'}")

# narrowest constriction along the route: per x-slice, count free reachable cells
print("\nconstriction profile (free area per 4mm slice along the run):")
worst=(1e9,None)
for i in range(0,nx,3):
    cnt=sum(1 for j in range(ny) for k in range(nz) if seen[i][j][k])
    if cnt==0: continue
    area=cnt*RES*RES
    xx=x0+(i+.5)*RES
    if area<worst[0]: worst=(area,xx)
    bar="#"*max(1,int(area/120))
    print(f"  x={xx:7.0f} mm  area={area:7.0f} mm2  {bar}")
a,xx=worst
eq=2*math.sqrt(a/math.pi)
print(f"\nNARROWEST: {a:.0f} mm2 at x={xx:.0f} mm  (~{eq:.0f} mm circular equivalent)")
print(f"passable-or-impossible: {'PASS - clearly passable' if eq>28 else 'REVIEW - ambiguous width'}")
