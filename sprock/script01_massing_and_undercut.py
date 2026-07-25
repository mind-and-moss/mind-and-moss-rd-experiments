# ============================================================================
# MONSTER8 — SCRIPT 01: THE MASSING + THE UNDERCUT
# Stack: STACK_S7 (replaces the invented STACK_B2)
#
# Paste into Blender: Scripting tab -> New -> paste -> Run Script (Alt+P)
#
# WHAT THIS DOES: builds six named limestone beds and lets each one retreat
# by an amount set ONLY by its hardness. The soft bed eats back far; the hard
# bed above it barely moves. The overhang that leaves is the start of the
# mouth. Nothing is bored. No boolean is used. (Law 1)
#
# Python note (Isaiah): lines starting with # are comments, ignored by Blender.
# ============================================================================
import bpy, bmesh
from mathutils import Vector

# --- scale ---------------------------------------------------------------
# Blender works in metres. We think in millimetres, so 1 unit = 1 mm here by
# building at metre-scale numbers /1000 and exporting with global_scale=1000
# later (that's the STL rule already in the canon).
MM = 0.001
H_TOTAL = 120 * MM          # overall height. Change this one number to rescale.
W       = 180 * MM          # width  (X) - A1 mini bed limit is 180 mm
D       = 140 * MM          # depth  (Y)

# --- STACK_S7 ------------------------------------------------------------
# (name, fraction of total height, hardness 1-5, note)
# Hardness 1 = argillaceous/marly, rots out.  5 = well-cemented, holds.
STACK_S7 = [
    ("B1_basal_massive",  0.20, 5, "well-cemented grainstone - floor + plinth"),
    ("B2_marl_weak",      0.12, 1, "THE ROTTEN ONE - becomes the gallery"),
    ("B3_massive_cap",    0.22, 5, "the overhang - collapses to form the mouth"),
    ("B4_medium_bedded",  0.18, 3, "ordinary biomicrite"),
    ("B5_marl_parting",   0.08, 2, "thin recess - a ledge, not a collapse"),
    ("B6_crest_jointed",  0.20, 4, "takes the crest joint - rain enters here"),
]

# How far a bed retreats, as a fraction of depth D, by hardness.
# THIS TABLE IS THE WHOLE DESIGN. The mouth is the difference between rows.
RETREAT = {5: 0.02, 4: 0.05, 3: 0.10, 2: 0.18, 1: 0.45}

MOUTH = Vector((W/2, -D/2, 0))   # mouth on the RIGHT face (locked decision)
EPS   = 0.0004

# --- clean slate ---------------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

z = 0.0
for name, frac, hard, note in STACK_S7:
    thick = H_TOTAL * frac
    z_bot, z_top = z, z + thick

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z + thick/2))
    bed = bpy.context.active_object
    bed.name = name                      # separate, named objects. Always.
    # A size=1 cube already spans 1 unit -- scale by the FULL dimension.
    bed.scale = (W, D, thick)
    bpy.ops.object.transform_apply(scale=True)

    me = bed.data
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=14, use_grid_fill=True)
    bm.to_mesh(me); bm.free()

    r_max = RETREAT[hard] * D

    for v in me.vertices:
        wp = bed.matrix_world @ v.co
        # Faces that must never move:
        #  - back (+Y) and left (-X) are flat against tank glass
        #  - base (z=0) is the flat print base
        #  - top/bottom of each bed are BURIED against its neighbours
        # Locked: back (+Y) and left (-X) are the glass faces; z=0 is the
        # flat print base. NOTE: we deliberately do NOT lock a bed's top and
        # bottom vertex rows. A bed's top SURFACE stays at its z, but its
        # FRONT FACE must retreat at every height -- otherwise the face pinches
        # in the middle and no bed can ever overhang its neighbour, which is
        # the entire mechanism we are building.
        if (wp.y > D/2 - EPS) or (wp.x < -W/2 + EPS) or (wp.z < EPS):
            continue

        # Retreat is strongest at the mouth, tapering away along the face.
        d = (Vector((wp.x, wp.y, 0.0)) - MOUTH).length
        near = max(0.0, 1.0 - d / (0.85 * D))
        amt  = r_max * (0.45 + 0.55 * near ** 2)   # some retreat everywhere

        # Push the exposed faces inward: front (-Y) goes +Y, right (+X) goes -X.
        if wp.y < -D/2 + EPS:
            v.co.y += amt
        if wp.x >  W/2 - EPS:
            v.co.x -= amt

    bed["hardness"] = hard              # stored on the object for later steps
    bed["note"] = note
    z = z_top

# --- report -------------------------------------------------------------
# Measure at the MOUTH END only. A global min() would just report the
# front-left corner, which is welded to the glass face and never moves.
print("\n--- STACK_S7  (measured at the mouth end) ---")
prev_y = prev_x = None
for name, frac, hard, note in STACK_S7:
    o = bpy.data.objects[name]
    pts = [o.matrix_world @ v.co for v in o.data.vertices]
    zs  = [p.z for p in pts]
    mouth_end = [p for p in pts if p.x > 0.30 * W]      # right-hand third
    fy = min(p.y for p in mouth_end)                     # front face there
    rx = max(p.x for p in pts)                           # right face
    line = (f"{name:<18} h={hard} thick={(max(zs)-min(zs))/MM:5.1f}mm "
            f"front={fy/MM:7.1f}mm right={rx/MM:6.1f}mm")
    if prev_y is not None:
        line += (f"  OVERHANG front={(prev_y-fy)/MM:+6.1f}mm"
                 f" right={(rx-prev_x)/MM:+6.1f}mm")
    print(line)
    prev_y, prev_x = fy, rx
print("--- a big positive OVERHANG = an undercut = the mouth forming ---\n")
