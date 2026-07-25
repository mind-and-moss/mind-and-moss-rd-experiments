# ============================================================================
# MONSTER8 — STRUCTURAL BASE FROM ISAIAH'S PLAN
#
# The footprint is now HIS traced perimeter, seen from above. The rock is the
# band between that blue line and the green void; the tank glass closes the
# void on back and right.
#
# Blocks are UNBONDED: each joint-bounded block of each bed is its own object,
# so every one can be moved, rotated and sculpted independently. Nothing is
# joined -- the preview join happens only at render time, on copies.
# ============================================================================
import bpy, bmesh, math, sys
from mathutils import Vector
MM=0.001

# --- Isaiah's plan, traced ------------------------------------------------
PERIM = [(-46,85),(-46,76),(-30,47),(-27,15),(-8,-6),(-22,-33),
         (1,-46),(27,-61),(56,-72),(80,-80),(90,-83)]
CORNER = Vector((90.0, 85.0))          # the glass corner: back +Y, right +X
def base_t(s): return 9.0 + 11.0*(s**1.3)   # scaled with the part     # wall thickness along the run

# Session 6, block 2 (THE STUMP): 141.3 x 121.7 x 114.4 mm, fits the A1 mini
# 180 bed WHOLE -- no segmenting, no pins. This retires the 18-piece / 99-peg
# segmentation derived earlier for a 420 mm object.
H_TOTAL = 114.4
TARGET_W, TARGET_D = 141.3, 121.7
BEDS = [("A1_platform",0.20,5),("A2_marl",0.11,1),("A3_cap",0.21,5),
        ("A4_bench",0.16,3),("A5_parting",0.09,2),("A6_perch",0.23,4)]
KEEP  = {5:1.00, 4:0.92, 3:0.84, 2:0.70, 1:0.50}   # soft beds keep less wall

# --- joints ---------------------------------------------------------------
J1_DEG, J1_SPACE, J1_PHASE = 68.0, 34.0, 11.0
J2_DEG, J2_SPACE, J2_PHASE = 152.0, 44.0, -23.0
J1 = Vector((math.cos(math.radians(J1_DEG)), math.sin(math.radians(J1_DEG))))
J2 = Vector((math.cos(math.radians(J2_DEG)), math.sin(math.radians(J2_DEG))))
N1 = Vector((-J1.y, J1.x)); N2 = Vector((-J2.y, J2.x))

def fnv(*a):
    x=2166136261
    for v in a: x=((x ^ (int(v)&0xffffffff))*16777619)&0xffffffff
    return x/0xffffffff

# --- resample the perimeter ----------------------------------------------
def resample(poly, step=1.2):
    pts=[Vector(poly[0])]
    for i in range(len(poly)-1):
        a,b=Vector(poly[i]),Vector(poly[i+1])
        L=(b-a).length; n=max(1,int(L/step))
        for k in range(1,n+1): pts.append(a+(b-a)*(k/n))
    return pts
# fit the traced plan into the real part's footprint
_xs=[p[0] for p in PERIM]; _ys=[p[1] for p in PERIM]
_sx = TARGET_W/(max(_xs)-min(_xs)); _sy = TARGET_D/(max(_ys)-min(_ys))
PERIM = [((x-min(_xs))*_sx - TARGET_W/2, (y-min(_ys))*_sy - TARGET_D/2)
         for (x,y) in PERIM]
CORNER = Vector((TARGET_W/2, TARGET_D/2))
P = resample(PERIM)
RUN = sum((P[i+1]-P[i]).length for i in range(len(P)-1))
S = []
acc=0.0
for i,pt in enumerate(P):
    if i>0: acc += (P[i]-P[i-1]).length
    S.append(acc/RUN)

def inward(i):
    """Unit vector from the perimeter toward the glass corner."""
    a=P[max(0,i-1)]; b=P[min(len(P)-1,i+1)]
    d=(b-a)
    if d.length==0: d=Vector((1,0))
    d.normalize()
    n=Vector((-d.y,d.x))
    if (P[i]+n - CORNER).length > (P[i]-n - CORNER).length: n=-n
    return n

# --- where do the joints cross the perimeter? -----------------------------
def joint_id(p, ph1, ph2):
    return (math.floor((p.dot(N1)-ph1)/J1_SPACE),
            math.floor((p.dot(N2)-ph2)/J2_SPACE))

def spacing_for_bed(bi, thick, hf):
    """LAW 1: joint spacing is 0.8-1.2x THE THICKNESS OF THE BED being
    cracked. Tighter than 0.8x reads fake -- each joint casts a stress shadow
    about one bed-thickness wide where no new joint can form.
    LAW 2 falls out for free: thin beds crack dense, thick beds sparse.
    LAW 6: relief tightens upward, so spacing gets finer toward the scar."""
    ratio = 0.9 + 0.45*fnv(bi,207,3)         # 0.90 .. 1.35 before relief
    relief = 1.0 - 0.22*(hf**1.6)            # Law 6: finer near the top
    # HARD CLAMP at 0.8x. Law 1 is not a preference: below 0.8x the rock
    # physically cannot over-crack, so anything tighter reads fake. Law 6 may
    # tighten spacing toward the scar but may never breach Law 1's floor.
    eff = max(0.80, min(1.20, ratio*relief))
    return max(5.0, thick*eff)

def cuts_for_bed(bi, thick=None, hf=0.5):
    """Joint crossings for ONE bed. Each bed carries its own phase, because
    joints step between beds rather than running straight through the whole
    stack -- which is what stops the wall reading as vertical columns."""
    sp1 = spacing_for_bed(bi, thick, hf) if thick else J1_SPACE
    sp2 = sp1*1.28                            # conjugate set, slightly sparser
    ph1 = J1_PHASE + (fnv(bi,101,1)-0.5)*sp1*0.9
    ph2 = J2_PHASE + (fnv(bi,103,2)-0.5)*sp2*0.9
    cu=[0]
    for i in range(1,len(P)):
        if (math.floor((P[i].dot(N1)-ph1)/sp1), math.floor((P[i].dot(N2)-ph2)/sp2)) != \
           (math.floor((P[i-1].dot(N1)-ph1)/sp1), math.floor((P[i-1].dot(N2)-ph2)/sp2)):
            cu.append(i)
    if cu[-1] != len(P)-1: cu.append(len(P)-1)
    mg=[cu[0]]
    for c in cu[1:]:
        if (P[c]-P[mg[-1]]).length < max(5.0,sp1*0.55) and c != cu[-1]: continue
        mg.append(c)
    return mg
print(f"perimeter run {RUN:.0f} mm, samples {len(P)}")

# --- OPENINGS: where the green passes the blue (Isaiah's rule) ------------
OPENINGS=[("upper_vent",0.17,20.0,4,5),("MOUTH",0.52,42.0,1,3),
          ("tail_exit",0.83,24.0,1,2)]
def in_opening(s, bed):
    for nm,cs,w,b0,b1 in OPENINGS:
        if abs(s-cs)*RUN <= w/2 and b0<=bed<=b1: return nm
    return None

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

# DIP: bedding is inclined, so beds climb along the run (script10)
DIP_DEG = 9.0
DIP = math.tan(math.radians(DIP_DEG))
def dip_dz(sv): return DIP*(sv-0.45)*RUN

made=0; plucked_n=0; z=0.0
fallen=[]
for bi,(bname,frac,hard) in enumerate(BEDS, start=1):
    thick=H_TOTAL*frac
    cuts = cuts_for_bed(bi, thick, (z+thick/2)/H_TOTAL)
    # 1. LENGTH: merge adjacent joint segments sometimes, so a few blocks are
    #    long masses and others are short. Real jointed rock has both; equal
    #    lengths are what read as brickwork.
    spans=[]; ci=0
    while ci < len(cuts)-1:
        grow = 1
        r = fnv(bi, ci, 21)
        if   r > 0.80: grow = 3
        elif r > 0.55: grow = 2
        grow = min(grow, len(cuts)-1-ci)
        spans.append((ci, cuts[ci], cuts[ci+grow]))
        ci += grow
    for (ci, i0, i1) in spans:
        smid = 0.5*(S[i0]+S[i1])
        if in_opening(smid, bi):        # no wall here -- that is an opening
            continue
        # PLUCKING + BROKEN CREST (script05/06): weathering removes whole
        # blocks, more from soft beds, more near the mouth, more with height.
        hf = (z + thick/2)/H_TOTAL
        prox = max(0.0, 1.0 - abs(smid-0.52)/0.26)
        pluck_p = min(0.20, {5:0.02,4:0.04,3:0.06,2:0.10,1:0.15}[hard]
                            + 0.09*prox + 0.17*(hf**3.2))
        if fnv(bi,ci,7) < pluck_p:
            fallen.append((0.5*(P[i0]+P[i1]), thick, hard, bi, ci))
            plucked_n += 1
            continue
        # each block stands on its own: aperture at the joints, its own
        # outward set, its own drop, its own tilt.
        jitter_out = (fnv(bi,ci,1)-0.5)*4.2       # a SET, not a gap
        drop       = (fnv(bi,ci,2)-0.5)*1.1
        shrink_z   = 0.995 + 0.020*fnv(bi,ci,8)   # full height: beds stay in contact
        # trim the ends: half the aperture off each, so adjacent blocks part
        # 2. DEPTH varies per block -- some stand out of the face, some are
        #    set deep into it.
        t_mul = 0.72 + 0.66*fnv(bi,ci,22)
        # 3. HEIGHT: sometimes a bedding plane failed to separate, so one block
        #    spans two beds as a single mass. Strongly biased to hard beds.
        span2 = (hard >= 4 and fnv(bi,ci,23) > 0.74)
        h_mul = 1.9 if span2 else 1.0
        # 4. ANGLE: its own yaw, so no two blocks are parallel.
        yaw = (fnv(bi,ci,24)-0.5)*0.22
        APER = 0.8 + 1.0*fnv(bi,ci,9)   # a fracture is a line, not a canyon
        seg=[]
        acc=0.0
        for i in range(i0, i1+1):
            if i>i0: acc += (P[i]-P[i-1]).length
            seg.append((i,acc))
        L=seg[-1][1]
        keep=[i for (i,a) in seg if a >= APER/2 and a <= L-APER/2]
        if len(keep) < 2: keep=[i0, i1]
        bm=bmesh.new()
        lo=[]; hi=[]
        for i in keep:
            n = inward(i)
            t = base_t(S[i])*KEEP[hard]*t_mul
            outer = P[i] - n*jitter_out           # erodes on the OUTER face
            innr  = P[i] + n*t
            zb = z + drop + dip_dz(S[i])
            zt = zb + thick*shrink_z*h_mul
            lo.append((bm.verts.new((outer.x*MM,outer.y*MM,zb*MM)),
                       bm.verts.new((innr.x*MM, innr.y*MM, zb*MM))))
            hi.append((bm.verts.new((outer.x*MM,outer.y*MM,zt*MM)),
                       bm.verts.new((innr.x*MM, innr.y*MM, zt*MM))))
        for k in range(len(lo)-1):
            (bo0,bi0),(bo1,bi1_) = lo[k], lo[k+1]
            (to0,ti0),(to1,ti1)  = hi[k], hi[k+1]
            bm.faces.new((bo0,bo1,bi1_,bi0))     # bottom
            bm.faces.new((to0,ti0,ti1,to1))      # top
            bm.faces.new((bo0,to0,to1,bo1))      # outer wall
            bm.faces.new((bi0,bi1_,ti1,ti0))     # inner wall (the cave side)
        (bo,bin_)=lo[0]; (to,tin)=hi[0]
        bm.faces.new((bo,bin_,tin,to))
        (bo,bin_)=lo[-1]; (to,tin)=hi[-1]
        bm.faces.new((bo,to,tin,bin_))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me=bpy.data.meshes.new(f"{bname}_b{ci:02d}")
        bm.to_mesh(me); bm.free()
        ob=bpy.data.objects.new(f"{bname}_b{ci:02d}", me)
        bpy.context.collection.objects.link(ob)
        ob["hardness"]=hard; ob["bed"]=bi; ob["block"]=ci
        ob["spans2beds"]=span2; ob["t_mul"]=round(t_mul,3)
        # SURFACE CLASSES (session 6): the FRONT + ends are OLD-ANCIENT, fully
        # rounded arrises. The TUNNEL INTERIOR is sheltered and KEEPS SHARP
        # EDGES -- sheltered rock does not round. So the bevel is limited to a
        # vertex group of outward-facing verts only.
        vg = ob.vertex_groups.new(name="weathered_flank")
        ctr = sum(((ob.matrix_world @ v.co) for v in ob.data.vertices),
                  Vector((0,0,0)))/len(ob.data.vertices)
        for v in ob.data.vertices:
            wp = ob.matrix_world @ v.co
            outward = (wp - ctr)
            faces_room = outward.xy.dot((ctr.xy - Vector((CORNER.x*MM, CORNER.y*MM)))) > 0
            vg.add([v.index], 1.0 if faces_room else 0.0, 'REPLACE')
        wear = 0.4 + 1.5*(0.45*max(0.0,jitter_out)/7.5 + 0.55*hf)
        bv=ob.modifiers.new("wear",'BEVEL'); bv.width=max(0.3,wear)*MM
        bv.segments=3; bv.limit_method='VGROUP'; bv.vertex_group="weathered_flank"
        # origin at the block's own centre so it rotates about itself
        bpy.context.view_layer.objects.active=ob
        ob.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        ob.rotation_euler=((fnv(bi,ci,4)-0.5)*0.045,
                           (fnv(bi,ci,5)-0.5)*0.045,
                           yaw)
        ob.select_set(False)
        made+=1
    z += thick

tal=0
for idx,(pt, th, hard, bi_, ci_) in enumerate(fallen):
    n = inward(min(range(len(P)), key=lambda q:(P[q]-pt).length))
    roll = 12.0 + 40.0*fnv(bi_,ci_,10)
    cp = pt - n*roll                       # it fell OUTWARD, away from the cave
    sz = th*(0.34 + 0.30*fnv(bi_,ci_,11))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cp.x*MM, cp.y*MM, (sz*0.30)*MM))
    o=bpy.context.active_object; o.name=f"talus_{bi_:02d}_{ci_:02d}"
    o.scale=(sz*(1.3+0.6*fnv(bi_,ci_,12))*MM, sz*(1.0+0.5*fnv(bi_,ci_,13))*MM, sz*MM)
    o.rotation_euler=((fnv(bi_,ci_,14)-0.5)*0.8,(fnv(bi_,ci_,15)-0.5)*0.8,
                      fnv(bi_,ci_,16)*6.28)
    bpy.ops.object.transform_apply(scale=True)
    bv=o.modifiers.new("tumbled",'BEVEL'); bv.width=(1.4+2.0*fnv(bi_,ci_,17))*MM
    bv.segments=3; bv.limit_method='ANGLE'; bv.angle_limit=math.radians(24)
    tal+=1
print(f"plucked {plucked_n} -> talus {tal}")
print(f"bedding dip {DIP_DEG:.0f} deg -> beds climb {DIP*RUN:.0f} mm across the run")
tall=len([o for o in bpy.data.objects if o.get("spans2beds")])
print(f"UNBONDED BLOCKS: {made} separate objects")
print(f"  variables per block: length (1-3 joint spans), depth (0.72-1.38x),")
print(f"    height ({tall} blocks span two beds), yaw (+/-0.11 rad)")
print(f"  LAW 1: spacing = 0.8-1.2x bed thickness (per bed, not global)")
print(f"  LAW 2: thin beds dense, thick sparse -- falls out of Law 1")
print(f"  LAW 5: joints STAGGERED per bed (offset at every boundary)")
print(f"  LAW 6: relief tightens upward -- finer spacing toward the scar")
print(f"  surface classes: flanks bevelled, TUNNEL EDGES KEPT SHARP")
for _bi,(_n,_f,_h) in enumerate(BEDS,start=1):
    _t=H_TOTAL*_f; _z=sum(H_TOTAL*b[1] for b in BEDS[:_bi-1])
    _sp=spacing_for_bed(_bi,_t,(_z+_t/2)/H_TOTAL)
    print(f"    {_n:<13} thick={_t:5.1f}mm -> spacing {_sp:5.1f}mm "
          f"({_sp/_t:.2f}x)")
for bi,(bname,frac,hard) in enumerate(BEDS,start=1):
    n=len([o for o in bpy.data.objects if o.name.startswith(bname)])
    print(f"  {bname:<13} h={hard} thick={H_TOTAL*frac:5.1f}mm  blocks={n}")
