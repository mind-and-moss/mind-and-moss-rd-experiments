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
def base_t(s): return 13.0 + 15.0*(s**1.3)     # wall thickness along the run

H_TOTAL = 190.0
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
def resample(poly, step=3.0):
    pts=[Vector(poly[0])]
    for i in range(len(poly)-1):
        a,b=Vector(poly[i]),Vector(poly[i+1])
        L=(b-a).length; n=max(1,int(L/step))
        for k in range(1,n+1): pts.append(a+(b-a)*(k/n))
    return pts
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
def joint_id(p):
    return (math.floor((p.dot(N1)-J1_PHASE)/J1_SPACE),
            math.floor((p.dot(N2)-J2_PHASE)/J2_SPACE))

cuts=[0]
for i in range(1,len(P)):
    if joint_id(P[i]) != joint_id(P[i-1]): cuts.append(i)
if cuts[-1] != len(P)-1: cuts.append(len(P)-1)
# drop slivers: a block shorter than 14 mm is not a block
merged=[cuts[0]]
for c in cuts[1:]:
    if (P[c]-P[merged[-1]]).length < 11.0 and c != cuts[-1]: continue
    merged.append(c)
cuts=merged
print(f"perimeter run {RUN:.0f} mm, joint crossings -> {len(cuts)-1} blocks per bed")

# --- OPENINGS: where the green passes the blue (Isaiah's rule) ------------
OPENINGS=[("upper_vent",0.17,20.0,4,5),("MOUTH",0.52,42.0,1,3),
          ("tail_exit",0.83,24.0,1,2)]
def in_opening(s, bed):
    for nm,cs,w,b0,b1 in OPENINGS:
        if abs(s-cs)*RUN <= w/2 and b0<=bed<=b1: return nm
    return None

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

made=0; z=0.0
for bi,(bname,frac,hard) in enumerate(BEDS, start=1):
    thick=H_TOTAL*frac
    for ci in range(len(cuts)-1):
        i0,i1 = cuts[ci], cuts[ci+1]
        smid = 0.5*(S[i0]+S[i1])
        if in_opening(smid, bi):        # no wall here -- that is an opening
            continue
        # each block gets its own small offsets so it reads as a loose block
        jitter_out = (fnv(bi,ci,1)-0.5)*3.4
        drop       = (fnv(bi,ci,2)-0.5)*2.2
        bm=bmesh.new()
        lo=[]; hi=[]
        for i in range(i0, i1+1):
            n = inward(i)
            t = base_t(S[i])*KEEP[hard]
            outer = P[i] - n*jitter_out           # erodes on the OUTER face
            innr  = P[i] + n*t
            lo.append((bm.verts.new((outer.x*MM,outer.y*MM,(z+drop)*MM)),
                       bm.verts.new((innr.x*MM, innr.y*MM, (z+drop)*MM))))
            hi.append((bm.verts.new((outer.x*MM,outer.y*MM,(z+drop+thick)*MM)),
                       bm.verts.new((innr.x*MM, innr.y*MM, (z+drop+thick)*MM))))
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
        # origin at the block's own centre so it rotates about itself
        bpy.context.view_layer.objects.active=ob
        ob.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        ob.select_set(False)
        made+=1
    z += thick

print(f"UNBONDED BLOCKS: {made} separate objects")
print(f"  {len(BEDS)} beds x up to {len(cuts)-1} blocks, minus openings")
for bi,(bname,frac,hard) in enumerate(BEDS,start=1):
    n=len([o for o in bpy.data.objects if o.name.startswith(bname)])
    print(f"  {bname:<13} h={hard} thick={H_TOTAL*frac:5.1f}mm  blocks={n}")
