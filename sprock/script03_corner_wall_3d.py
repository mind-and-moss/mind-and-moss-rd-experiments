# ============================================================================
# MONSTER8 — SCRIPT 03: THE CORNER WALL IN 3D
#
# Builds Isaiah's plan as a real wall standing in the tank corner, one
# separate object per bed of STACK_S7.
#
# Two things this does NOT do, on purpose:
#   - no booleans. The openings are gaps in the wall by construction, so
#     there is nothing to cut. (Stack-order law: booleans would come first
#     anyway, but here we simply never need them.)
#   - no displacement. That is the LAST step and preview-only. Not here.
#
# The erosion mechanism: a bed's wall THICKNESS is set by its hardness. Soft
# beds are thin, hard beds are fat, so the hard beds stand proud and the soft
# beds are recessed. The overhang is an output. (Law 1)
# ============================================================================
import bpy, bmesh, math
from mathutils import Vector

MM = 0.001

# --- the plan, same trace as plan_corner_wall.py -------------------------
PERIM = [(-46, 85), (-46, 76), (-30, 47), (-27, 15), (-8, -6), (-22, -33),
         (1, -46), (27, -61), (56, -72), (80, -80), (90, -83)]
CORNER = Vector((90.0, 85.0))            # the glass corner; void lies this side
def base_t(s): return 13.0 + 15.0 * (s ** 1.3)     # nominal wall thickness, mm

# --- STACK_S7 ------------------------------------------------------------
H_TOTAL = 120.0
STACK_S7 = [
    ("B1_basal_massive",  0.20, 5),
    ("B2_marl_weak",      0.12, 1),
    ("B3_massive_cap",    0.22, 5),
    ("B4_medium_bedded",  0.18, 3),
    ("B5_marl_parting",   0.08, 2),
    ("B6_crest_jointed",  0.20, 4),
]
# hardness -> how much of the nominal thickness survives
KEEP = {5: 1.00, 4: 0.93, 3: 0.86, 2: 0.74, 1: 0.55}

# --- openings: (name, centre s, width mm, first bed, last bed) -----------
# The fish enters at substrate level, so openings start at bed 1. The bed
# ABOVE the last one is the lintel -- its ceiling is a bedding plane, which
# is why the mouth never needs boring.
PERIM_LEN = 256.0
OPENINGS = [
    ("MOUTH",      0.52, 42.0, 1, 3),    # lintel = B4
    ("tail_exit",  0.83, 24.0, 1, 2),    # lintel = B3, smaller than the mouth
    ("upper_vent", 0.17, 20.0, 4, 5),    # high draught hole, rock below it
]

# resample the perimeter so offsetting is smooth
def resample(poly, step=2.0):
    out=[Vector(poly[0])]
    for i in range(len(poly)-1):
        a,b = Vector(poly[i]), Vector(poly[i+1])
        L=(b-a).length; n=max(1,int(L/step))
        for k in range(1,n+1): out.append(a+(b-a)*(k/n))
    return out
P = resample(PERIM)
S = [i/(len(P)-1) for i in range(len(P))]

def normal_at(i):
    a = P[max(0,i-1)]; b = P[min(len(P)-1,i+1)]
    d = (b-a)
    if d.length == 0: d = Vector((1,0))
    d.normalize()
    n = Vector((d.y, -d.x))
    # point it AWAY from the glass corner
    if (P[i] + n*1.0 - CORNER).length < (P[i] - n*1.0 - CORNER).length:
        n = -n
    return n

def opening_at(s, bed_index):
    for name, cs, w, b0, b1 in OPENINGS:
        if abs(s-cs)*PERIM_LEN <= w/2 and b0 <= bed_index <= b1:
            return name
    return None

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

z = 0.0
for bi, (name, frac, hard) in enumerate(STACK_S7, start=1):
    thick = H_TOTAL*frac
    bm = bmesh.new()
    # walk the perimeter, emitting a wall segment wherever there is no opening
    run = []
    def flush(run):
        if len(run) < 2: return
        top=[]; bot=[]
        for (i) in run:
            n = normal_at(i)
            t = base_t(S[i]) * KEEP[hard]
            inner = P[i]                        # void side
            outer = P[i] + n*t                  # outside
            bot.append((bm.verts.new((inner.x*MM, inner.y*MM, z*MM)),
                        bm.verts.new((outer.x*MM, outer.y*MM, z*MM))))
            top.append((bm.verts.new((inner.x*MM, inner.y*MM, (z+thick)*MM)),
                        bm.verts.new((outer.x*MM, outer.y*MM, (z+thick)*MM))))
        for k in range(len(run)-1):
            bi0,bo0 = bot[k];   bi1,bo1 = bot[k+1]
            ti0,to0 = top[k];   ti1,to1 = top[k+1]
            bm.faces.new((bi0,bi1,bo1,bo0))       # bottom
            bm.faces.new((ti0,to0,to1,ti1))       # top
            bm.faces.new((bi0,bo0,to0,ti0)) if k==0 else None
            bm.faces.new((bi0,ti0,ti1,bi1))       # inner wall
            bm.faces.new((bo0,bo1,to1,to0))       # outer wall
        bi0,bo0 = bot[0];  ti0,to0 = top[0]
        bi1,bo1 = bot[-1]; ti1,to1 = top[-1]
        bm.faces.new((bi1,bo1,to1,ti1))           # end cap
    for i in range(len(P)):
        if opening_at(S[i], bi) is None:
            run.append(i)
        else:
            flush(run); run=[]
    flush(run)

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob["hardness"] = hard
    z += thick

print("\n--- MONSTER8 corner wall ---")
for name, frac, hard in STACK_S7:
    o = bpy.data.objects[name]
    print(f"{name:<18} h={hard} keep={KEEP[hard]:.2f}  verts={len(o.data.vertices):5d} "
          f"faces={len(o.data.polygons):5d}")
print("openings:", ", ".join(f"{n}(B{a}-B{b})" for n,_,_,a,b in OPENINGS))
