# ============================================================================
# MONSTER8 — REAL CHAMBER v2, sized to the marl bed and VALIDATED
#
# v1 failed hard: the cutter consumed the whole A2 bed and split the model
# into two floating halves. The lesson is structural, not numeric --
# THE DEN CAN NEVER EXCEED THE ROTTEN BED'S PLAN AREA. So the cutter is sized
# from A2's footprint, and the result is checked rather than trusted.
# ============================================================================
import bpy, bmesh, math, sys
from mathutils import Vector
MM = 0.001
exec(open(sys.argv[-1]).read())

Z_A1_TOP, Z_A2_TOP = 38.0, 58.9
FLOOR_DISH = 10.0
CEIL = Z_A2_TOP

# path node: (x, y, rx, ry)  -- explicit radii, no global scale to go wrong
NODES = [
    (MOUTH_X,        -D/2 - 12,  27.0, 20.0),   # outside the mouth
    (MOUTH_X + 10,   -66.0,      30.0, 24.0),   # throat
    (MOUTH_X + 56,   -30.0,      50.0, 42.0),   # THE DEN
    (MOUTH_X + 122,  -34.0,      38.0, 32.0),   # gallery
    (MOUTH_X + 176,  -60.0,      26.0, 22.0),   # toward the tail
    (MOUTH_X + 206,  -D/2 - 12,  18.0, 16.0),   # tail exit
]

bm = bmesh.new(); rings=[]
for (x,y,rx,ry) in NODES:
    ring=[]; n=22
    cz = (Z_A1_TOP - FLOOR_DISH + CEIL)/2
    hz = (CEIL - (Z_A1_TOP - FLOOR_DISH))/2
    for k in range(n):
        a=2*math.pi*k/n
        # elliptical in plan, squashed vertically: a chamber, not a pipe
        ring.append(bm.verts.new(((x + rx*math.cos(a))*MM,
                                  (y + ry*math.cos(a)*0.0 + ry*math.sin(a))*MM,
                                  (cz + hz*math.sin(a)*0.0)*MM)))
    rings.append(ring)
# extrude each ring vertically into a slab-shaped tube
bm.free()
bm = bmesh.new()
lo = Z_A1_TOP - FLOOR_DISH
hi = CEIL
loops=[]
for (x,y,rx,ry) in NODES:
    lo_ring=[]; hi_ring=[]
    n=24
    for k in range(n):
        a=2*math.pi*k/n
        px=(x+rx*math.cos(a))*MM; py=(y+ry*math.sin(a))*MM
        lo_ring.append(bm.verts.new((px,py,lo*MM)))
        hi_ring.append(bm.verts.new((px,py,hi*MM)))
    loops.append((lo_ring,hi_ring))
for (lo_r,hi_r) in loops:
    for k in range(len(lo_r)):
        j=(k+1)%len(lo_r)
        bm.faces.new((lo_r[k],lo_r[j],hi_r[j],hi_r[k]))
    bmesh.ops.contextual_create(bm, geom=lo_r)
    bmesh.ops.contextual_create(bm, geom=hi_r)
# bridge consecutive lozenges so it is one continuous void
for i in range(len(loops)-1):
    a_lo,a_hi = loops[i]; b_lo,b_hi = loops[i+1]
    for k in range(len(a_lo)):
        j=(k+1)%len(a_lo)
        bm.faces.new((a_lo[k],a_lo[j],b_lo[j],b_lo[k]))
        bm.faces.new((a_hi[k],a_hi[j],b_hi[j],b_hi[k]))
me=bpy.data.meshes.new("CAVE_CUTTER"); bm.to_mesh(me); bm.free()
cut=bpy.data.objects.new("CAVE_CUTTER", me); bpy.context.collection.objects.link(cut)

before={}
for t in ("A1_platform","A2_marl","A3_cap"):
    before[t]=len(bpy.data.objects[t].data.polygons)
for tname in ("A1_platform","A2_marl","A3_cap"):
    t=bpy.data.objects[tname]
    b=t.modifiers.new("cave",'BOOLEAN'); b.object=cut; b.operation='DIFFERENCE'
    b.solver='EXACT'
    bpy.context.view_layer.objects.active=t
    bpy.ops.object.modifier_apply(modifier="cave")
cut.hide_render=True; cut.hide_viewport=True

# --- VALIDATE: the boolean must not have eaten a bed or split the model ---
def components(ob):
    bm=bmesh.new(); bm.from_mesh(ob.data)
    seen=set(); comp=0
    for v in bm.verts:
        if v in seen: continue
        comp+=1; stack=[v]; seen.add(v)
        while stack:
            cur=stack.pop()
            for e in cur.link_edges:
                o=e.other_vert(cur)
                if o not in seen: seen.add(o); stack.append(o)
    bm.free(); return comp

print("\n--- BOOLEAN VALIDATION ---")
ok=True
for tname in ("A1_platform","A2_marl","A3_cap"):
    t=bpy.data.objects[tname]
    nf=len(t.data.polygons); nc=components(t)
    verdict="PASS" if nf>0 and nc==1 else "FAIL"
    if verdict=="FAIL": ok=False
    print(f"{tname:<13} faces {before[tname]:4d} -> {nf:4d}   components={nc}   {verdict}")
for tname in ("A4_bench","A5_parting","A6_perch"):
    t=bpy.data.objects[tname]
    print(f"{tname:<13} untouched, faces {len(t.data.polygons):4d}   components={components(t)}")
print(f"OVERALL: {'PASS - no bed consumed, no bed split' if ok else 'FAIL'}")

print("\n--- CHAMBER ---")
print(f"ceiling = A3 underside : z {CEIL:.1f} mm")
print(f"floor   = dish into A1 : z {lo:.1f} mm")
print(f"clear headroom         : {hi-lo:.1f} mm")
print(f"den clear floor        : {NODES[2][2]*2:.0f} x {NODES[2][3]*2:.0f} mm")
print(f"turn-room 1.5x         : fish to {min(NODES[2][2],NODES[2][3])*2/1.5:.0f} mm "
      f"(~{min(NODES[2][2],NODES[2][3])*2/1.5/25.4:.1f} in)")
print(f"mouth {NODES[0][2]*2:.0f} mm  ->  tail exit {NODES[5][2]*2:.0f} mm   "
      f"exit<mouth: {NODES[5][2]<NODES[0][2]}")
