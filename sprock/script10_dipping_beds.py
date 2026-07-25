# ============================================================================
# MONSTER8 — SCRIPT 10: DIPPING BEDS
#
# The reference rock is steeply inclined. Horizontal beds are what made this
# read as a rectilinear ruin -- the grid comes from the bedding, not from the
# blocks being rectangles.
#
# The conflict: a real dip fights the flat print base and the vertical glass
# faces. The resolution is geologically honest -- THE BEDS DIP INSIDE THE
# BLOCK, and the base and glass faces are CUT PLANES through inclined strata.
# That is exactly a sawn block of dipping rock, and it keeps every gate:
# flat base, flat glass faces, dipping bedding.
#
# Blocks carried below the base plane by the dip are removed -- the saw took
# them. Blocks carried above the crest stay: the crest is broken anyway.
#
# The remaining gap to the reference photo is FORM, not surface. Every block
# sat on one curve, so the piece was a slab. Real cliffs have blocks at many
# depths, buttresses that project, and a stack that stands where the rock was
# hardest. That is massing -- machine work -- not decoration.
#
#   BUTTRESSES: at two points along the run the wall projects forward hard.
#               These are where a joint set was widest apart, so more rock
#               survived between the joints.
#   THE STACK:  one end carries extra beds. In the reference photo the sea
#               stacks are simply where the rock resisted longest; here it is
#               where the massive beds are thickest and the marl is thinnest.
#
# Isaiah's note: "this piece has survived history." That is not a mood, it is
# a set of physical consequences, and each one changes the geometry:
#
#   SURVIVORS ARE BIG.   Small blocks were carried away long ago. What is left
#                        skews large, and hard beds keep bigger blocks than
#                        soft ones. So the size range widens AND shifts by
#                        hardness, rather than just getting noisier.
#   THE CREST IS BROKEN. The top has been exposed longest and is attacked from
#                        above and both sides. Plucking rises steeply with
#                        height, so the skyline steps down instead of sitting
#                        flat.
#   EXPOSED EDGES ARE WORN. Long exposure rounds everything it can reach.
#                        Bevel scales with how proud and how high a block sits;
#                        sheltered blocks under the lintel stay crisp. This is
#                        the wear-geometry gate: detail survives in recesses.
#   THE DEBRIS IS STILL THERE. Plucked blocks did not vanish, they fell. They
#                        return as talus at the foot, tumbled and heavily
#                        rounded, half-buried. Also gives the feathered,
#                        dig-stable buried edge the BIO gate asks for.
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

# --- DIP ------------------------------------------------------------------
import math as _m
DIP_DEG = 11.0                      # bedding inclination
DIP = _m.tan(_m.radians(DIP_DEG))
def dip_dz(s):
    """Vertical offset of the bedding at position s along the run."""
    return DIP * (s - 0.45) * TOTAL
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
plucked_n = 0
bed_plucked = {}
bed_kept = {}
bed_total = {}
# pre-count blocks per bed so the quarter-loss cap has something to measure
_z = 0.0
for _bi,(_n,_f,_hd) in enumerate(STACK_S7, start=1):
    _th = H_TOTAL*_f; _sp = 1.15*_th + 8.0; _d = 0.0; _k = 0
    while _d < TOTAL - 1.0:
        _big = {5:1.30,4:1.12,3:1.00,2:0.84,1:0.72}[_hd]
        _L = min(_sp*_big*(0.55 + 1.55*(h(_bi,_k,1)**1.5)), TOTAL-_d)
        if _L < 6.0: break
        bed_total[_bi] = bed_total.get(_bi,0) + 1
        _d += _L; _k += 1
    _z += _th
talus_n = 0
stack_n = 0
fallen = []
z = 0.0
for bi, (bedname, frac, hard) in enumerate(STACK_S7, start=1):
    thick = H_TOTAL*frac
    # JOINT SPACING SCALES WITH BED THICKNESS
    spacing = 1.15 * thick + 8.0
    d0, k = 0.0, 0
    while d0 < TOTAL - 1.0:
        # SURVIVORS ARE BIG. Wider range than before (0.35..2.75) and biased
        # by hardness: massive beds keep large masses, marl fragments small.
        big = {5: 1.30, 4: 1.12, 3: 1.00, 2: 0.84, 1: 0.72}[hard]
        L = spacing * big * (0.55 + 1.55 * (h(bi, k, 1) ** 1.5))
        L = min(L, TOTAL - d0)
        if L < 6.0: break
        mid = d0 + L/2
        p, dirv, n, s = at(mid)
        # FIX 2 - PLUCKING. Weathering removes whole blocks from the middle
        # of a course, not just at the openings. Soft beds lose more (the marl
        # gives its blocks up readily); the undercut zone near the mouth loses
        # more still, because those blocks were unsupported.
        prox_p = max(0.0, 1.0 - abs(s - MOUTH_S)/0.26)
        height_frac = (z + thick/2) / H_TOTAL
        crest_attack = 0.20 * (height_frac ** 3.0)      # crest broken, not erased
        pluck_p = min(0.30, {5: 0.04, 4: 0.07, 3: 0.11, 2: 0.17, 1: 0.26}[hard]
                            + 0.14*prox_p + crest_attack)
        plucked = h(bi, k, 7) < pluck_p
        if bed_plucked.get(bi, 0) >= max(1, int(0.25 * max(1, bed_total.get(bi, 1)))):
            plucked = False                      # this bed has given up enough
        # A stack cannot stand on nothing. The rock beneath its span is, by
        # definition, the rock that resisted -- it is why the stack is there.
        if 0.58 <= s <= 0.78:
            plucked = False

        if in_opening(s, bi) is None and L > 8.0 and not plucked:
            t = base_t(s) * KEEP[hard]
            # collapse: blocks near the mouth have slipped out and dropped
            prox = max(0.0, 1.0 - abs(s - MOUTH_S)/0.22)
            slip_out  = prox * (2.0 + 5.0*h(bi,k,2))
            slip_down = prox * (1.0 + 3.0*h(bi,k,3))
            # FIX 1 - RELIEF. Was +/-1.5mm, so the face was a plane with
            # grooves. Blocks now stand proud or sit back by a real amount,
            # scaled to the wall thickness. Soft beds sit back further.
            relief    = t * (0.62 if hard <= 2 else 0.42)
            jitter_n  = (h(bi,k,4)-0.5) * 2.0 * relief - (0.25*relief if hard<=2 else 0.0)
            jitter_z  = (h(bi,k,5)-0.5) * thick * 0.22
            tilt      = (h(bi,k,6)-0.5) * 0.10 + prox*0.09

            # DEPTH: two buttresses project hard; elsewhere depth still varies
            # far more than the old +/- relief allowed.
            bt = 0.0
            for bs, bw, bd in ((0.30, 0.10, 26.0), (0.68, 0.08, 19.0)):
                if abs(s-bs) < bw:
                    bt += bd * (0.5*(1+math.cos(math.pi*abs(s-bs)/bw)))
            depth_var = (h(bi,k,13)-0.5) * 2.0 * (0.9*t)
            cx = p + n*(t/2 + jitter_n + slip_out + bt + depth_var)
            cz = z + thick/2 + jitter_z - slip_down + dip_dz(s)
            if cz - thick/2 < -2.0:        # the base plane sawed this one off
                d0 += L; k += 1; continue
            bpy.ops.mesh.primitive_cube_add(size=1, location=(cx.x*MM, cx.y*MM, cz*MM))
            o = bpy.context.active_object
            o.name = f"{bedname}_blk{k:02d}"
            o.scale = ((L*1.03)*MM, t*MM, (thick*0.98)*MM)
            # a block sits parallel to its bed, so it tilts with the dip
            o.rotation_euler = (0, tilt - math.radians(DIP_DEG)*0.85,
                                math.atan2(dirv.y, dirv.x))
            bpy.ops.object.transform_apply(scale=True)
            # EXPOSED EDGES ARE WORN. Proud + high = beaten for longer.
            proud = max(0.0, jitter_n) / max(1e-6, relief)
            wear  = 0.35 + 2.1 * (0.45*proud + 0.55*height_frac)
            bev = o.modifiers.new("wear", 'BEVEL')
            bev.width = wear * MM; bev.segments = 3; bev.limit_method = 'ANGLE'
            bev.angle_limit = math.radians(35)
            o["hardness"] = hard; o["bed"] = bi
            made += 1
            bed_kept[bi] = bed_kept.get(bi, 0) + 1
        else:
            if in_opening(s, bi) is None and L > 8.0 and plucked:
                plucked_n += 1
                bed_plucked[bi] = bed_plucked.get(bi, 0) + 1
                # THE DEBRIS IS STILL THERE. It fell outward from where it sat
                # and came to rest at the foot, tumbled and half-buried.
                t2 = base_t(s) * KEEP[hard]
                roll = 8.0 + 26.0*h(bi,k,8)          # how far out it rolled
                cp = p + n*(t2/2 + roll)
                hgt = thick*0.72
                bpy.ops.mesh.primitive_cube_add(
                    size=1, location=(cp.x*MM, cp.y*MM, (hgt*0.34)*MM))  # talus always lands at z=0
                tb = bpy.context.active_object
                tb.name = f"talus_{bi:02d}_{k:02d}"
                tb.scale = ((L*0.66)*MM, t2*0.80*MM, hgt*MM)
                tb.rotation_euler = (
                    (h(bi,k,9)-0.5)*0.55,
                    (h(bi,k,10)-0.5)*0.55,
                    math.atan2(dirv.y, dirv.x) + (h(bi,k,11)-0.5)*2.2)
                bpy.ops.object.transform_apply(scale=True)
                # tumbled for ages -> heavily rounded
                bv = tb.modifiers.new("tumbled", 'BEVEL')
                bv.width = (1.6 + 2.2*h(bi,k,12)) * MM
                bv.segments = 4; bv.limit_method = 'ANGLE'
                bv.angle_limit = math.radians(25)
                tb["talus"] = True
                talus_n += 1
        d0 += L; k += 1
    z += thick

# --- THE SURVIVOR STACK --------------------------------------------------
# Extra courses over one span only, where the massive beds are thickest. In
# the reference photo the sea stacks are simply where the rock resisted
# longest. It narrows as it rises because it is attacked from every side.
STACK_SPAN = (0.60, 0.76)
zs = H_TOTAL
for extra in range(4):
    sthick = 20.0 - 2.4*extra
    shard  = 5 if extra % 2 == 0 else 4
    sspacing = 1.15*sthick + 8.0
    d0, k = STACK_SPAN[0]*TOTAL, 0
    while d0 < STACK_SPAN[1]*TOTAL:
        L = min(sspacing*(0.7+0.7*h(90+extra,k,1)), STACK_SPAN[1]*TOTAL-d0)
        if L < 7.0: break
        mid=d0+L/2; p2,dirv2,n2,s2 = at(mid)
        if h(90+extra,k,2) > 0.16 + 0.12*extra:
            t2 = base_t(s2)*KEEP[shard]*(1.0 - 0.13*extra)
            cx2 = p2 + n2*(t2/2 + (h(90+extra,k,4)-0.5)*0.7*t2)
            bpy.ops.mesh.primitive_cube_add(
                size=1, location=(cx2.x*MM, cx2.y*MM,
                                  (zs+sthick/2+dip_dz(s2))*MM))
            o=bpy.context.active_object; o.name=f"S{extra+1}_stack_blk{k:02d}"
            o.scale=((L*1.03)*MM, t2*MM, (sthick*0.98)*MM)
            o.rotation_euler=(0,(h(90+extra,k,6)-0.5)*0.13
                                - math.radians(DIP_DEG)*0.85,
                              math.atan2(dirv2.y,dirv2.x))
            bpy.ops.object.transform_apply(scale=True)
            bv=o.modifiers.new("wear",'BEVEL')
            bv.width=(1.4+1.4*h(90+extra,k,7))*MM
            bv.segments=3; bv.limit_method='ANGLE'; bv.angle_limit=math.radians(35)
            o["hardness"]=shard; made+=1; stack_n+=1
        d0+=L; k+=1
    zs += sthick

print(f"\n--- MONSTER8 block assembly ---")
print(f"wall blocks  : {made}  (of which survivor stack: {stack_n})")
print(f"stack rises to z = {zs:.0f} mm vs wall crest {H_TOTAL:.0f} mm")
print(f"bedding dip = {DIP_DEG:.0f} deg -> beds climb {DIP*TOTAL:.0f} mm across the run")
print("base + glass faces are CUT PLANES through the dipping strata")
for _b in sorted(bed_total): 
    print(f"   bed B{_b}: total={bed_total[_b]:2d} kept={bed_kept.get(_b,0):2d} "
          f"plucked={bed_plucked.get(_b,0):2d}")
print(f"plucked      : {plucked_n}  -> talus blocks placed: {talus_n}")
for bi,(bedname,frac,hard) in enumerate(STACK_S7, start=1):
    n = len([o for o in bpy.data.objects if o.name.startswith(bedname)])
    print(f"{bedname:<18} h={hard} thick={H_TOTAL*frac:5.1f}mm "
          f"joint_spacing={1.15*H_TOTAL*frac+8:5.1f}mm  blocks={n}")
