# ============================================================================
# MONSTER8 — SCRIPT 04: THE BLOCK ASSEMBLY
#
# Fundamental change per Isaiah: the wall is no longer one extruded ribbon.
# It is MANY RECTANGULAR BLOCKS in varied positions.
#
# This is how bedded limestone actually fails: bedding planes cut it
# horizontally, two joint sets cut it vertically, and the rock comes apart
# into rectangular blocks. Two real relationships are built in rather than
# styled in:
#   - JOINT SPACING SCALES WITH BED THICKNESS. Thick beds break into wide
#     blocks, thin beds into narrow ones. Observed, not invented.
#   - DISPLACEMENT GROWS TOWARD THE MOUTH. Blocks near the unsupported span
#     have slipped and rotated; blocks in solid wall have not. That is the
#     collapse, recorded in block positions instead of a noise texture.
#
# All variation is DETERMINISTIC (seeded hash), so the same script always
# produces the same rock. Nothing here is tuned to "look like" anything.
# ============================================================================
import bpy, bmesh, math
from mathutils import Vector

MM = 0.001
PERIM = [(-46, 85), (-46, 76), (-30, 47), (-27, 15), (-8, -6), (-22, -33),
         (1, -46), (27, -61), (56, -72), (80, -80), (90, -83)]
CORNER = Vector((90.0, 85.0))
def base_t(s): return 13.0 + 15.0 * (s ** 1.3)

H_TOTAL = 120.0
STACK_S7 = [
    ("B1_basal_massive",  0.20, 5),
    ("B2_marl_weak",      0.12, 1),
    ("B3_massive_cap",    0.22, 5),
    ("B4_medium_bedded",  0.18, 3),
    ("B5_marl_parting",   0.08, 2),
    ("B6_crest_jointed",  0.20, 4),
]
KEEP = {5: 1.00, 4: 0.93, 3: 0.86, 2: 0.74, 1: 0.55}
PERIM_LEN = 256.0
OPENINGS = [("MOUTH", 0.52, 42.0, 1, 3),
            ("tail_exit", 0.83, 24.0, 1, 2),
            ("upper_vent", 0.17, 20.0, 4, 5)]

def h(*a):
    """Deterministic 0..1 from integers. Same input -> same rock, always."""
    x = 2166136261
    for v in a:
        x = ((x ^ (v & 0xffffffff)) * 16777619) & 0xffffffff
    return x / 0xffffffff

# arc-length parameterisation of the perimeter
pts = [Vector(p) for p in PERIM]
segs, cum = [], [0.0]
for i in range(len(pts)-1):
    L = (pts[i+1]-pts[i]).length; segs.append(L); cum.append(cum[-1]+L)
TOTAL = cum[-1]
def at(dist):
    for i in range(len(segs)):
        if dist <= cum[i+1] or i == len(segs)-1:
            t = (dist-cum[i])/segs[i]
            p = pts[i] + (pts[i+1]-pts[i])*t
            d = (pts[i+1]-pts[i]).normalized()
            n = Vector((d.y, -d.x))
            if (p+n - CORNER).length < (p-n - CORNER).length: n = -n
            return p, d, n, dist/TOTAL
def in_opening(s, bed):
    for nm, cs, w, b0, b1 in OPENINGS:
        if abs(s-cs)*PERIM_LEN <= w/2 and b0 <= bed <= b1: return nm
    return None
MOUTH_S = 0.52

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

made = 0
z = 0.0
for bi, (bedname, frac, hard) in enumerate(STACK_S7, start=1):
    thick = H_TOTAL*frac
    # JOINT SPACING SCALES WITH BED THICKNESS
    spacing = 1.15 * thick + 8.0
    d0, k = 0.0, 0
    while d0 < TOTAL - 1.0:
        L = spacing * (0.75 + 0.5*h(bi, k, 1))        # block length varies
        L = min(L, TOTAL - d0)
        if L < 6.0: break
        mid = d0 + L/2
        p, dirv, n, s = at(mid)
        if in_opening(s, bi) is None and L > 8.0:
            t = base_t(s) * KEEP[hard]
            # collapse: blocks near the mouth have slipped out and dropped
            prox = max(0.0, 1.0 - abs(s - MOUTH_S)/0.22)
            slip_out  = prox * (2.0 + 5.0*h(bi,k,2))
            slip_down = prox * (1.0 + 3.0*h(bi,k,3))
            jitter_n  = (h(bi,k,4)-0.5) * 3.0          # every block sits proud
            jitter_z  = (h(bi,k,5)-0.5) * 1.6          #   or shy by a little
            tilt      = (h(bi,k,6)-0.5) * 0.10 + prox*0.09

            cx = p + n*(t/2 + jitter_n + slip_out)
            cz = z + thick/2 + jitter_z - slip_down
            bpy.ops.mesh.primitive_cube_add(size=1, location=(cx.x*MM, cx.y*MM, cz*MM))
            o = bpy.context.active_object
            o.name = f"{bedname}_blk{k:02d}"
            o.scale = ((L*0.94)*MM, t*MM, (thick*0.95)*MM)
            o.rotation_euler = (0, tilt, math.atan2(dirv.y, dirv.x))
            bpy.ops.object.transform_apply(scale=True)
            o["hardness"] = hard; o["bed"] = bi
            made += 1
        d0 += L; k += 1
    z += thick

print(f"\n--- MONSTER8 block assembly ---")
print(f"blocks built : {made}")
for bi,(bedname,frac,hard) in enumerate(STACK_S7, start=1):
    n = len([o for o in bpy.data.objects if o.name.startswith(bedname)])
    print(f"{bedname:<18} h={hard} thick={H_TOTAL*frac:5.1f}mm "
          f"joint_spacing={1.15*H_TOTAL*frac+8:5.1f}mm  blocks={n}")
