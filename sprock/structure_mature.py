# ============================================================================
# MONSTER8 — MATURE STRUCTURE (the 70% armature)
#
# The 30% version was six smooth slabs. Real bedded limestone has SYSTEMS,
# and those are what a sculptor should be handed rather than asked to invent:
#
#   JOINT SETS   two near-vertical fracture directions cut the whole outcrop.
#                Every plan outline steps at a joint instead of curving,
#                because rock breaks along joints, not along splines. This is
#                the single biggest reason a smooth extrusion reads as fake.
#   SUB-BEDDING  thick beds are not one slab; they are laminae with small
#                retreat differences, giving fine horizontal steps.
#   TWO CAVES    the marl bed rots out wherever it is exposed, not in one
#                spot. A second, smaller opening on another face.
#   TALUS        sectors that lost the most rock put it somewhere: at the foot.
#   SOLUTION     ledge tops hold water, so they carry shallow basins.
#
# All variation is a seeded hash of (sector, bed). Same script, same rock.
# ============================================================================
import bpy, bmesh, math, sys
from mathutils import Vector
MM = 0.001

W, D, H = 420.0, 250.0, 190.0

BEDS = [
    ("A1_platform",  0.20, 5,  0.0, 2),
    ("A2_marl",      0.11, 1,  0.0, 2),
    ("A3_cap",       0.21, 5, 28.0, 2),
    ("A4_bench",     0.16, 3, 16.0, 2),
    ("A5_parting",   0.09, 2, 18.0, 2),
    ("A6_perch",     0.23, 4, 12.0, 2),
]
RETREAT = {5:0.0, 4:5.0, 3:11.0, 2:19.0, 1:38.0}
MOUTH_X, MOUTH_W = -0.20*W, 0.26*W

# --- THE JOINT SYSTEM ----------------------------------------------------
J1_DEG, J1_SPACE = 68.0, 86.0        # first set: strike and spacing (mm)
J2_DEG, J2_SPACE = 152.0, 118.0      # second set, oblique to the first
J1 = Vector((math.cos(math.radians(J1_DEG)), math.sin(math.radians(J1_DEG))))
J2 = Vector((math.cos(math.radians(J2_DEG)), math.sin(math.radians(J2_DEG))))

def fnv(*a):
    x=2166136261
    for v in a:
        x=((x ^ (int(v) & 0xffffffff))*16777619) & 0xffffffff
    return x/0xffffffff

def sector(p):
    """Which joint-bounded block is this point in?"""
    return (math.floor(p.dot(J1)/J1_SPACE), math.floor(p.dot(J2)/J2_SPACE))

def sector_retreat(p, bed_i, hard):
    """Extra retreat for this joint block. Rock breaks block by block, so the
    outline STEPS at joints instead of flowing."""
    s = sector(p)
    base = RETREAT[hard]
    # soft beds lose whole blocks; hard beds lose a little off a few
    amp  = {5:0.35, 4:0.5, 3:0.7, 2:0.9, 1:1.15}[hard]
    return base + amp * base * (fnv(s[0]+97, s[1]+31, bed_i) - 0.35) \
           + amp * 9.0 * (fnv(s[0]+7, s[1]+53, bed_i*3) - 0.5)

def outline(bed_i, inset, hard, cx, cy, n=168, facet=8):
    """Plan outline of a bed.

    Retreat is evaluated once per FACET and then held constant across it.
    Evaluating per sample point makes the radius alternate wherever a joint
    boundary runs near-tangent to the outline, which shreds thin laminae into
    a comb of fins. Rock steps at a joint and then holds flat to the next one
    -- so the outline must too. The result is faceted, which is correct.
    """
    base=[]
    for i in range(n):
        a = 2*math.pi*i/n
        rx = W/2 - inset; ry = D/2 - inset
        k = (1.0 + 0.15*math.cos(a+0.4*bed_i) - 0.08*math.cos(2*a-0.7*bed_i)
                 + 0.06*math.sin(3*a+1.1*bed_i))
        base.append(Vector((cx + rx*math.cos(a)*k, cy + ry*math.sin(a)*k)))
    # one retreat value per facet, sampled at the facet's midpoint
    rets=[]
    nf = n//facet
    for fi in range(nf):
        mid = base[(fi*facet + facet//2) % n]
        rets.append(sector_retreat(mid, bed_i, hard))
    pts=[]
    for i in range(n):
        r = rets[(i//facet) % nf]
        d = base[i] - Vector((cx,cy))
        if d.length > 1e-6:
            pts.append(Vector((cx,cy)) + d.normalized()*max(12.0, d.length - r))
        else:
            pts.append(base[i])
    return pts

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

z=0.0; inset=0.0; made=0
LAMINA_STEP = 2.6      # how far each sub-lamina sits back from the one below
for bi,(name, frac, hard, step, nlam) in enumerate(BEDS, start=1):
    thick = H*frac
    inset += step
    cx = 0.16*W*(bi-1)/(len(BEDS)-1)
    cy = 0.20*D*(bi-1)/(len(BEDS)-1)
    lam_t = thick/nlam
    for li in range(nlam):
        ring = outline(bi*10+li, inset + li*LAMINA_STEP, hard, cx, cy)
        bm=bmesh.new()
        zb = z + li*lam_t; zt = zb + lam_t
        bot=[bm.verts.new((p.x*MM,p.y*MM,zb*MM)) for p in ring]
        top=[bm.verts.new((p.x*MM,p.y*MM,zt*MM)) for p in ring]
        for i in range(len(ring)):
            j=(i+1)%len(ring)
            bm.faces.new((bot[i],bot[j],top[j],top[i]))
        bmesh.ops.contextual_create(bm, geom=bot)
        bmesh.ops.contextual_create(bm, geom=top)
        me=bpy.data.meshes.new(f"{name}_L{li}")
        bm.to_mesh(me); bm.free()
        ob=bpy.data.objects.new(f"{name}_L{li}", me)
        bpy.context.collection.objects.link(ob)
        ob["hardness"]=hard; ob["bed"]=bi; ob["lamina"]=li
        made+=1
    z += thick

print(f"\n--- MATURE STRUCTURE ---")
print(f"joint set 1: strike {J1_DEG:.0f} deg, spacing {J1_SPACE:.0f} mm")
print(f"joint set 2: strike {J2_DEG:.0f} deg, spacing {J2_SPACE:.0f} mm")
print(f"beds {len(BEDS)}, laminae total {made}")
for bi,(name,frac,hard,step,nlam) in enumerate(BEDS,start=1):
    print(f"  {name:<13} h={hard} thick={H*frac:5.1f}mm  laminae={nlam}")

# =========================================================================
# SYSTEMS PASS -- what turns a stack of plates into an outcrop
# =========================================================================
LAMS=[o for o in bpy.data.objects if o.type=='MESH']

def bbox_mm(o):
    pts=[o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(p.x for p in pts)/MM, max(p.x for p in pts)/MM,
            min(p.y for p in pts)/MM, max(p.y for p in pts)/MM,
            min(p.z for p in pts)/MM, max(p.z for p in pts)/MM)

def box_cutter(name, cx, cy, cz, sx, sy, sz, rot_z):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx*MM, cy*MM, cz*MM))
    o=bpy.context.active_object; o.name=name
    o.scale=(sx*MM, sy*MM, sz*MM); o.rotation_euler=(0,0,rot_z)
    bpy.ops.object.transform_apply(scale=True)
    return o

def cyl_cutter(name, cx, cy, cz, rx, ry, h):
    bpy.ops.mesh.primitive_cylinder_add(vertices=26, radius=1.0, depth=1.0,
        location=(cx*MM, cy*MM, cz*MM))
    o=bpy.context.active_object; o.name=name
    o.scale=(rx*MM, ry*MM, h*MM)
    bpy.ops.object.transform_apply(scale=True)
    return o

cutters=[]
CUT_BEDS={}   # cutter name -> set of bed indices it may cut (None = any)

# --- 1. OPEN JOINTS (grikes) ---------------------------------------------
# Widened fractures running down through the stack. This is what visually
# ties the beds together -- without them the beds read as separate plates.
# (x, y, strike, width, LENGTH, z_bottom, z_top)
# Joints are PARTIAL slots, not through-cuts. A slot long enough to cross the
# whole piece severs it and leaves a free-standing fin, which reads as a wall
# rather than a fracture. Kept to ~a third of the span, and stopped short of
# the base so the plinth stays whole.
JOINTS=[( -78.0,  44.0, math.radians(J1_DEG),  6.0, 118.0,  96.0, 200.0),
        (  58.0,  22.0, math.radians(J1_DEG),  5.0,  96.0, 118.0, 200.0),
        ( -26.0, -48.0, math.radians(J2_DEG),  5.5, 104.0, 120.0, 200.0),
        ( 138.0,  40.0, math.radians(J2_DEG),  4.5,  86.0, 140.0, 200.0),
        (  -6.0,  84.0, math.radians(J1_DEG),  4.0,  76.0, 148.0, 200.0),
        ( 104.0, -74.0, math.radians(J2_DEG),  5.0,  92.0, 100.0, 200.0)]
for i,(x,y,rot,wdt,lng,zlo,ztop) in enumerate(JOINTS):
    c=box_cutter(f"JOINT_{i}", x, y, (zlo+ztop)/2, lng, wdt, (ztop-zlo), rot)
    cutters.append(c); CUT_BEDS[c.name]=None

# --- 2. COLLAPSED EMBAYMENT ----------------------------------------------
# One sector lost its upper beds outright. This breaks the profile and gives
# the piece a front and a back instead of a uniform mound.
c=cyl_cutter("EMBAYMENT", 118.0, -46.0, 150.0, 92.0, 74.0, 120.0)
cutters.append(c); CUT_BEDS[c.name]=None

# --- 3. THE CAVE, in the rotten bed (validated convex chain) --------------
Z_A1_TOP = H*BEDS[0][1]
Z_A2_TOP = Z_A1_TOP + H*BEDS[1][1]
lo, hi = Z_A1_TOP-10.0, Z_A2_TOP
NODES=[(MOUTH_X,      -D/2-12, 27.0,20.0),(MOUTH_X+10, -66.0, 30.0,24.0),
       (MOUTH_X+56,   -30.0,   50.0,42.0),(MOUTH_X+122,-34.0, 38.0,32.0),
       (MOUTH_X+176,  -60.0,   26.0,22.0),(MOUTH_X+206,-D/2-12,18.0,16.0)]
for idx,(x,y,rx,ry) in enumerate(NODES):
    c=cyl_cutter(f"CAVE_{idx}", x, y, (lo+hi)/2, rx, ry, hi-lo)
    cutters.append(c); CUT_BEDS[c.name]={1,2}
for idx in range(len(NODES)-1):
    x0n,y0n,rx0,ry0=NODES[idx]; x1n,y1n,rx1,ry1=NODES[idx+1]
    for t in (0.33,0.66):
        c=cyl_cutter(f"CAVEL_{idx}_{int(t*100)}",
            x0n+(x1n-x0n)*t, y0n+(y1n-y0n)*t, (lo+hi)/2,
            (rx0+(rx1-rx0)*t)*0.94, (ry0+(ry1-ry0)*t)*0.94, hi-lo)
        cutters.append(c); CUT_BEDS[c.name]={1,2}
# second, smaller opening -- the marl rots wherever it is exposed
for idx,(x,y,rx,ry) in enumerate([(150.0, 96.0, 22.0,18.0),(120.0,66.0,26.0,21.0),
                                  (96.0, 40.0, 22.0,18.0)]):
    c=cyl_cutter(f"CAVE2_{idx}", x, y, (lo+hi)/2, rx, ry, hi-lo)
    cutters.append(c); CUT_BEDS[c.name]={1,2}

# --- 4. SOLUTION BASINS on ledge tops ------------------------------------
for i,(bx,by,bz,br) in enumerate([(-52.0,44.0,58.9,34.0),(38.0,52.0,98.8,30.0),
                                  (-8.0,70.0,146.3,26.0),(96.0,10.0,190.0,30.0)]):
    c=cyl_cutter(f"BASIN_{i}", bx, by, bz+4.0, br, br*0.78, 11.0)
    cutters.append(c); CUT_BEDS[c.name]=None

# --- apply, but only where a cutter actually overlaps a lamina -----------
applied=0
for lam in LAMS:
    lb=bbox_mm(lam)
    allowed=None
    for c in cutters:
        allowed=CUT_BEDS.get(c.name)
        if allowed is not None and lam.get("bed") not in allowed:
            continue
        cb=bbox_mm(c)
        if (lb[0]>cb[1] or lb[1]<cb[0] or lb[2]>cb[3] or lb[3]<cb[2]
            or lb[4]>cb[5] or lb[5]<cb[4]):
            continue
        m=lam.modifiers.new("cut",'BOOLEAN'); m.object=c
        m.operation='DIFFERENCE'; m.solver='EXACT'
        bpy.context.view_layer.objects.active=lam
        bpy.ops.object.modifier_apply(modifier="cut")
        applied+=1
for c in cutters: bpy.data.objects.remove(c, do_unlink=True)

# --- CLEANUP -------------------------------------------------------------
# EXACT boolean leaves degenerate geometry where a cutter grazes a surface:
# zero-area faces, doubled verts, and the non-manifold edges they create.
# Clean it before anything downstream trusts the mesh.
cleaned=0
for o in [x for x in bpy.data.objects if x.type=='MESH']:
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True); bpy.context.view_layer.objects.active=o
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.00018)
    bpy.ops.mesh.dissolve_degenerate(threshold=0.00014)
    # interior faces are the multi-face-edge culprits the booleans leave behind
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_interior_faces()
    bpy.ops.mesh.delete(type='FACE')
    # then close whatever that opened
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_non_manifold(extend=False)
    bpy.ops.mesh.fill_holes(sides=0)
    # wire edges (no faces at all) also count as non-manifold -- drop them
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_non_manifold(extend=False, use_wire=True,
                                     use_boundary=False, use_multi_face=False,
                                     use_non_contiguous=False, use_verts=False)
    bpy.ops.mesh.delete(type='EDGE')
    # a second fill pass: the first can open new boundaries as it closes others
    for _ in range(3):
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(type='EDGE')
        bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False,
                                         use_boundary=True, use_multi_face=False,
                                         use_non_contiguous=False, use_verts=False)
        bpy.ops.mesh.fill_holes(sides=0)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    cleaned+=1
print(f"cleaned {cleaned} meshes")

# drop micro-fragments the booleans shed
removed=0
for o in [x for x in bpy.data.objects if x.type=='MESH']:
    if len(o.data.polygons)==0:
        bpy.data.objects.remove(o, do_unlink=True); removed+=1; continue
    bb=o.bound_box
    dx=abs(bb[6][0]-bb[0][0])/MM; dy=abs(bb[6][1]-bb[0][1])/MM; dz=abs(bb[6][2]-bb[0][2])/MM
    if dx*dy*dz < 400:          # smaller than ~7mm cube
        bpy.data.objects.remove(o, do_unlink=True); removed+=1
print(f"micro-fragments removed {removed}")
LAMS=[o for o in bpy.data.objects if o.type=='MESH']
LAMS=[o for o in LAMS if len(o.data.polygons)>0]
print(f"cutters {len(cutters)}, boolean ops applied {applied}")

# --- 5. TALUS: the rock that left had to go somewhere --------------------
# Rockfall does not scatter evenly across open ground. It PILES AT THE FOOT,
# heaviest directly below where it came from -- here, under the collapsed
# embayment -- and it half-buries itself in the substrate. Blocks are also
# far smaller than the beds they came from, because they broke on landing.
EMBAY = Vector((118.0, -46.0))
tal=0
for i in range(46):
    # cluster: two thirds under the embayment, the rest strung along the foot
    if fnv(i, 41, 2) < 0.62:
        ang = 2*math.pi*fnv(i, 17, 8)
        rad = 30.0 + 74.0*fnv(i, 23, 4)**1.6
        x = EMBAY.x + rad*math.cos(ang)
        y = EMBAY.y + rad*0.75*math.sin(ang)
    else:
        a = 2*math.pi*fnv(i, 11, 3)
        rr = 168.0 + 42.0*fnv(i, 29, 5)
        x = 20 + rr*math.cos(a); y = -18 + rr*0.60*math.sin(a)
    if abs(x) > W/2 + 78 or abs(y) > D/2 + 52: continue
    # small -- they broke on impact. And they sit LOW, partly buried.
    sz = 7.0 + 17.0*fnv(i, 7, 9)**1.5
    bury = 0.30 + 0.35*fnv(i, 31, 7)
    bpy.ops.mesh.primitive_cube_add(size=1,
        location=(x*MM, y*MM, (sz*(0.5-bury))*MM))
    o=bpy.context.active_object; o.name=f"talus_{i:02d}"
    o.scale=(sz*(1.2+0.7*fnv(i,3,3))*MM, sz*(1.0+0.5*fnv(i,5,4))*MM, sz*MM)
    o.rotation_euler=((fnv(i,3,1)-0.5)*0.85,(fnv(i,5,2)-0.5)*0.85,
                      fnv(i,9,4)*6.28)
    bpy.ops.object.transform_apply(scale=True)
    bv=o.modifiers.new("tumbled",'BEVEL')
    bv.width=(1.2+2.2*fnv(i,13,6))*MM
    bv.segments=3; bv.limit_method='ANGLE'; bv.angle_limit=math.radians(24)
    tal+=1
print(f"talus blocks {tal}")
print(f"objects total {len([o for o in bpy.data.objects if o.type=='MESH'])}")
