# ============================================================================
# MONSTER8 — SCRIPT 07: SEGMENTATION + PEGS AND SOCKETS
#
# Splits the block assembly into printable pieces at BEDDING PLANES, and adds
# the pin joints. Two reasons the split goes on bedding planes:
#   - the seam has somewhere to hide: there is already a line there
#   - each piece then prints flat-side-down, so the undercut is created by
#     ASSEMBLY rather than by a printed overhang. No supports anywhere.
#
# Clearance is 0.43 mm diametral, the figure already proven on the A1 mini.
# ============================================================================
import bpy, math
from mathutils import Vector
MM = 0.001

H_TOTAL = 120.0
STACK_S7 = [("B1_basal_massive",0.20,5), ("B2_marl_weak",0.12,1),
            ("B3_massive_cap",0.22,5),   ("B4_medium_bedded",0.18,3),
            ("B5_marl_parting",0.08,2),  ("B6_crest_jointed",0.20,4)]

# three pieces, split where the undercut is, so no piece prints an overhang
PIECES = [("P1_base",  [1, 2]),      # top face is the retreated marl ledge
          ("P2_mid",   [3, 4, 5]),   # prints on B3's flat underside
          ("P3_crest", [6])]

PEG_D      = 6.0        # peg diameter, mm
CLEARANCE  = 0.43       # diametral, proven on the A1 mini
PEG_LEN    = 10.0
SOCKET_D   = PEG_D + CLEARANCE

def bed_z(idx):
    z = 0.0
    for i,(n,f,h) in enumerate(STACK_S7, start=1):
        if i == idx: return z, z + H_TOTAL*f
        z += H_TOTAL*f
    return z, z

# seam heights = top of the last bed in each piece (except the topmost)
seams = []
for name, beds in PIECES[:-1]:
    seams.append((name, bed_z(beds[-1])[1]))

# peg positions: in solid rock, well back from the void, spread along the run
PERIM = [(-46,85),(-46,76),(-30,47),(-27,15),(-8,-6),(-22,-33),
         (1,-46),(27,-61),(56,-72),(80,-80),(90,-83)]
pts=[Vector(p) for p in PERIM]
cum=[0.0]
for i in range(len(pts)-1): cum.append(cum[-1]+(pts[i+1]-pts[i]).length)
TOTAL=cum[-1]
def at(d):
    for i in range(len(cum)-1):
        if d<=cum[i+1] or i==len(cum)-2:
            t=(d-cum[i])/max(1e-9,(cum[i+1]-cum[i]))
            return pts[i]+(pts[i+1]-pts[i])*t
OPEN_S = [0.52, 0.83, 0.17]          # keep pegs away from the openings
def peg_spots(n=4):
    out=[]
    for i in range(n):
        s = 0.10 + 0.80*i/(n-1)
        if min(abs(s-o) for o in OPEN_S) < 0.09:   # too close to an opening
            # nudge whichever way keeps it ON the wall -- a peg pushed past
            # s=1.0 lands outside the piece, in the glass.
            s = s - 0.11 if s > 0.5 else s + 0.11
        s = max(0.08, min(0.92, s))
        out.append((s, at(s*TOTAL)))
    return out

print("\n--- SEGMENTATION ---")
for name, beds in PIECES:
    z0 = bed_z(beds[0])[0]; z1 = bed_z(beds[-1])[1]
    print(f"{name:<10} beds {beds}  z {z0:5.1f} -> {z1:5.1f} mm  "
          f"height {z1-z0:5.1f} mm   prints flat-side-down, no supports")
print("\n--- PIN JOINTS ---")
print(f"peg dia {PEG_D} mm / socket dia {SOCKET_D} mm  "
      f"(clearance {CLEARANCE} mm diametral, proven on A1 mini)")
for nm, zc in seams:
    print(f"seam above {nm} at z={zc:.1f} mm:")
    for s, p in peg_spots():
        print(f"    peg at s={s:.2f}  x={p.x:7.1f}  y={p.y:7.1f}  "
              f"peg {PEG_LEN} mm long, {PEG_LEN/2:.0f} mm each side")
print("\nfoam fills the remaining gap and locks the stack (Option C).")
