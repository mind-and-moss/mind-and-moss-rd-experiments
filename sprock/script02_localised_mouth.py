# ============================================================================
# MONSTER8 — SCRIPT 02: LOCALISED MOUTH + FLAT-CEILINGED ARCH
#
# Changes from script 01, both driven by Isaiah's constraint
# "no overhang falling into the mouth":
#
#  1. The retreat is now LOCALISED on the RIGHT face (the locked mouth face).
#     Script 01 retreated the whole perimeter, which gave a continuous slot
#     all the way round. Now it is a notch in one place, with general
#     weathering everywhere else.
#
#  2. The mouth CEILING is B3's flat underside, and it stays flat. The arch
#     reads from the flared, rounded ENDS of the notch, not from a curved
#     roof. Three reasons that is the right call:
#       - nothing droops into the opening (no wedge, BIO gate)
#       - the flat face is the peg/socket mating face for the segmented build
#       - a flat face prints face-down with no supports
#     Geologically this is exactly a wave-cut notch: the sea removes the
#     collapse debris, and the clean span is what survives.
# ============================================================================
import bpy, bmesh, math
from mathutils import Vector

MM = 0.001
H_TOTAL = 120 * MM
W       = 180 * MM
D       = 140 * MM

STACK_S7 = [
    ("B1_basal_massive",  0.20, 5, "well-cemented grainstone - floor + plinth"),
    ("B2_marl_weak",      0.12, 1, "THE ROTTEN ONE - becomes the gallery"),
    ("B3_massive_cap",    0.22, 5, "the span - its flat underside is the ceiling"),
    ("B4_medium_bedded",  0.18, 3, "ordinary biomicrite"),
    ("B5_marl_parting",   0.08, 2, "thin recess - a ledge, not a collapse"),
    ("B6_crest_jointed",  0.20, 4, "takes the crest joint - rain enters here"),
]
RETREAT = {5: 0.02, 4: 0.05, 3: 0.10, 2: 0.18, 1: 0.45}

# Mouth sits on the RIGHT face (+X), pushed toward the front so the piece is
# lopsided rather than centred (ART gate: never symmetrical).
MOUTH_Y    = -0.18 * D          # where along the right face the notch centres
MOUTH_HALF =  0.34 * D          # half-width of the notch along the face
BACKGROUND =  0.08              # general weathering everywhere else
EPS        =  0.0004

def bump(dist, half):
    """Smooth 1->0 falloff. Gives the notch flared ends instead of a slot."""
    if dist >= half:
        return 0.0
    return 0.5 * (1.0 + math.cos(math.pi * dist / half))

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

z = 0.0
for name, frac, hard, note in STACK_S7:
    thick = H_TOTAL * frac
    z_bot, z_top = z, z + thick

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z + thick/2))
    bed = bpy.context.active_object
    bed.name = name
    bed.scale = (W, D, thick)                # size=1 cube spans 1 unit already
    bpy.ops.object.transform_apply(scale=True)

    me = bed.data
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=18, use_grid_fill=True)
    bm.to_mesh(me); bm.free()

    r_max = RETREAT[hard] * D

    for v in me.vertices:
        wp = bed.matrix_world @ v.co
        # locked: back (+Y) and left (-X) glass faces, and the z=0 print base
        if (wp.y > D/2 - EPS) or (wp.x < -W/2 + EPS) or (wp.z < EPS):
            continue

        # RIGHT FACE -- the mouth face. Notch is localised here.
        if wp.x > W/2 - EPS:
            k = bump(abs(wp.y - MOUTH_Y), MOUTH_HALF)
            v.co.x -= r_max * (BACKGROUND + (1.0 - BACKGROUND) * k)

        # FRONT FACE -- background weathering only, so bedding still reads.
        if wp.y < -D/2 + EPS:
            v.co.y += r_max * BACKGROUND * 1.6

    bed["hardness"] = hard
    bed["note"] = note
    z = z_top

# --- measure the notch where it actually is -------------------------------
print("\n--- STACK_S7 / script 02  (measured across the mouth) ---")
prev = None
for name, frac, hard, note in STACK_S7:
    o = bpy.data.objects[name]
    pts = [o.matrix_world @ v.co for v in o.data.vertices]
    zs  = [p.z for p in pts]
    # right-face vertices sitting within the notch window
    inzone = [p for p in pts if abs(p.y - MOUTH_Y) < MOUTH_HALF * 0.35]
    face_x = max(p.x for p in inzone)
    line = (f"{name:<18} h={hard} thick={(max(zs)-min(zs))/MM:5.1f}mm "
            f"mouth_face_x={face_x/MM:6.1f}mm")
    if prev is not None:
        line += f"   UNDERCUT={(prev - face_x)/MM:+6.1f}mm"
    print(line)
    prev = face_x
print("--- B3 minus B2 is the mouth: cap stands proud, weak bed is gone ---\n")
