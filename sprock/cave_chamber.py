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

# The cutter is a CHAIN OF CLEAN CONVEX SOLIDS, differenced one at a time.
# The previous version capped every lozenge and then bridged between them,
# which left internal faces inside the cutter. EXACT boolean on
# self-overlapping geometry produced 444 cm3 of phantom void inside A1 --
# a failure that only a volumetric check would ever have found.
lo = Z_A1_TOP - FLOOR_DISH
hi = CEIL
cutters=[]
for idx,(x,y,rx,ry) in enumerate(NODES):
    bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=1.0, depth=1.0,
        location=(x*MM, y*MM, ((lo+hi)/2)*MM))
    c=bpy.context.active_object
    c.name=f"CUT_{idx:02d}"
    c.scale=(rx*MM, ry*MM, (hi-lo)*MM)
    bpy.ops.object.transform_apply(scale=True)
    cutters.append(c)
# bridge the gaps between consecutive nodes with an extra solid at the midpoint
for idx in range(len(NODES)-1):
    x0n,y0n,rx0,ry0 = NODES[idx]; x1n,y1n,rx1,ry1 = NODES[idx+1]
    for t in (0.33, 0.66):
        mx=x0n+(x1n-x0n)*t; my=y0n+(y1n-y0n)*t
        mrx=rx0+(rx1-rx0)*t; mry=ry0+(ry1-ry0)*t
        bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=1.0, depth=1.0,
            location=(mx*MM, my*MM, ((lo+hi)/2)*MM))
        c=bpy.context.active_object
        c.name=f"CUT_link_{idx:02d}_{int(t*100)}"
        c.scale=(mrx*0.94*MM, mry*0.94*MM, (hi-lo)*MM)
        bpy.ops.object.transform_apply(scale=True)
        cutters.append(c)

before={}
for t in ("A1_platform","A2_marl","A3_cap"):
    before[t]=len(bpy.data.objects[t].data.polygons)
for tname in ("A1_platform","A2_marl","A3_cap"):
    t=bpy.data.objects[tname]
    for c in cutters:
        b=t.modifiers.new("cave",'BOOLEAN'); b.object=c
        b.operation='DIFFERENCE'; b.solver='EXACT'
        bpy.context.view_layer.objects.active=t
        bpy.ops.object.modifier_apply(modifier="cave")
for c in cutters:
    bpy.data.objects.remove(c, do_unlink=True)

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
