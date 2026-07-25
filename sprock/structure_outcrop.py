# ============================================================================
# MONSTER8 — BASIC STRUCTURE (big forms only)
#
# Read off the reference product: a flat-lying limestone outcrop TERRACED BY
# BEDDING PLANES, cave at the front-left, perch on top. Every step in that
# photo is a bed edge -- which is why the bed stack drives the whole shape.
#
# This is ARMATURE ONLY. No detail, no texture. Detail, colour and magic are
# Isaiah's. Nine big forms, nothing else.
# ============================================================================
import bpy, bmesh, math
from mathutils import Vector
MM = 0.001

# BIGGER than the shelf product (~300mm). This is the custom build.
W, D, H = 420.0, 250.0, 190.0

# bottom -> top. (name, frac of H, hardness, plan inset from the one below)
# Hardness drives INSET: soft beds retreat further, so the terrace steps are
# an OUTPUT of the stack, not drawn in.
BEDS = [
    ("A1_platform",  0.20, 5,   0.0),   # the plinth, sits on substrate
    ("A2_marl",      0.11, 1,  34.0),   # THE ROTTEN ONE -> the cave
    ("A3_cap",       0.21, 5,   6.0),   # roof of the cave, overhangs A2
    ("A4_bench",     0.16, 3,  22.0),   # the wide mid terrace
    ("A5_parting",   0.09, 2,  27.0),   # thin recessive step
    ("A6_perch",     0.23, 4,  16.0),   # the flat top the animal sits on
]
MOUTH_X, MOUTH_W = -0.30*W, 0.30*W     # cave at the FRONT-LEFT, per the photo

def outline(inset, wob, cx, cy, seed):
    """Plan outline of a bed. Irregular and OFF-CENTRE: as the outcrop wears
    back the terraces migrate, so higher beds sit back and to the right.
    Concentric rings read as a wedding cake, which is the one thing rock
    never looks like."""
    pts=[]; n=56
    for i in range(n):
        a = 2*math.pi*i/n
        rx = W/2 - inset; ry = D/2 - inset
        k = (1.0
             + 0.16*math.cos(a + 0.4*seed)
             - 0.09*math.cos(2*a - 0.7*seed)
             + 0.07*math.sin(3*a + 1.1*seed)
             + wob*math.sin(5*a + seed))
        pts.append(Vector((cx + rx*math.cos(a)*k, cy + ry*math.sin(a)*k)))
    return pts

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

z = 0.0
inset = 0.0
for bi,(name, frac, hard, step) in enumerate(BEDS, start=1):
    thick = H*frac
    inset += step
    # soft beds retreat further -> the terrace step is an output of hardness
    retreat = {5:0.0, 4:5.0, 3:11.0, 2:19.0, 1:38.0}[hard]
    # migrate back (+y) and right (+x) with height
    cx = 0.16*W * (bi-1)/(len(BEDS)-1)
    cy = 0.20*D * (bi-1)/(len(BEDS)-1)
    ring = outline(inset + retreat, 0.045, cx, cy, bi*1.7)

    bm = bmesh.new()
    bot=[bm.verts.new((p.x*MM, p.y*MM, z*MM)) for p in ring]
    top=[bm.verts.new((p.x*MM, p.y*MM, (z+thick)*MM)) for p in ring]
    for i in range(len(ring)):
        j=(i+1)%len(ring)
        bm.faces.new((bot[i],bot[j],top[j],top[i]))
    bmesh.ops.contextual_create(bm, geom=bot)
    bmesh.ops.contextual_create(bm, geom=top)
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    ob["hardness"]=hard; ob["bed"]=bi
    z += thick

# --- THE CAVE: a gap in the low beds, roofed by the hard cap --------------
# Not bored. The marl A2 is simply absent across the mouth span, and A3 above
# it is not -- so A3 becomes the lintel. Law 1.
for name in ("A2_marl", "A1_platform"):
    ob = bpy.data.objects[name]
    bm = bmesh.new(); bm.from_mesh(ob.data)
    lim = MOUTH_W/2 if name=="A2_marl" else MOUTH_W/2*0.62
    kill=[f for f in bm.faces
          if MOUTH_X-lim < f.calc_center_median().x/MM < MOUTH_X+lim
          and f.calc_center_median().y/MM < 0
          and f.normal.z > -0.5]
    bmesh.ops.delete(bm, geom=kill, context='FACES')
    bm.to_mesh(ob.data); bm.free()

print("\n--- BASIC STRUCTURE ---")
print(f"overall {W:.0f} x {D:.0f} x {H:.0f} mm  (reference product ~300mm long)")
zz=0.0
for name, frac, hard, step in BEDS:
    t=H*frac
    print(f"{name:<13} h={hard}  thickness {t:5.1f} mm   z {zz:5.1f} -> {zz+t:5.1f}")
    zz+=t
print(f"cave mouth: x {MOUTH_X-MOUTH_W/2:.0f} -> {MOUTH_X+MOUTH_W/2:.0f} mm, front-left")
print(f"forms total: {len(BEDS)}")
