import bpy, sys, math
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())
rock=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith("talus")]
xs=[];ys=[];zs=[]
for o in rock:
    for c in o.bound_box:
        w=o.matrix_world @ Vector(c); xs.append(w.x/MM);ys.append(w.y/MM);zs.append(w.z/MM)
EW=max(xs)-min(xs); ED=max(ys)-min(ys); EH=max(zs)-min(zs)
BED=180.0; USABLE=172.0
print(f"\n=== SEGMENTATION (A1 mini, {BED:.0f} mm bed) ===")
print(f"actual extents {EW:.0f} x {ED:.0f} x {EH:.0f} mm")
LAYERS=[("L1_base",0.0,58.9,"A1+A2 - the cave layer"),
        ("L2_mid",58.9,146.3,"A3+A4+A5 - the lintel and benches"),
        ("L3_crest",146.3,190.0,"A6 - the perch")]
ncx=math.ceil(EW/USABLE); ncy=math.ceil(ED/USABLE)
print(f"columns needed: {ncx} x {ncy}  ->  column footprint {EW/ncx:.0f} x {ED/ncy:.0f} mm")
tot=0
for nm,z0,z1,note in LAYERS:
    h=z1-z0
    print(f"  {nm:<9} z {z0:6.1f}->{z1:6.1f}  h={h:5.1f}mm  "
          f"{'fits' if h<=USABLE else 'TOO TALL'}  x{ncx*ncy} pieces   {note}")
    tot+=ncx*ncy
print(f"TOTAL PIECES: {tot}")
# seams that follow joint planes read as natural fractures
print(f"\nseam placement: vertical seams are put ON JOINT PLANES so they read as")
print(f"fractures rather than saw cuts (Ep3/Ep7). Candidate planes crossing the piece:")
shown=0
for which,N,sp,deg,ph in ((1,N1,J1_SPACE,J1_DEG,J1_PHASE),(2,N2,J2_SPACE,J2_DEG,J2_PHASE)):
    for k in range(-6,7):
        base=N*(k*sp+ph)
        if abs(base.x)>EW/2*0.8 or abs(base.y)>ED/2*0.8: continue
        print(f"   J{which} k={k:+d}  passes through ({base.x:7.1f},{base.y:7.1f})  strike {deg:.0f} deg")
        shown+=1
        if shown>=6: break
    if shown>=6: break
print(f"\npegs 6.0 mm / sockets 6.43 mm (0.43 mm diametral, proven on A1 mini)")
hseams=len(LAYERS)-1
vseams=(ncx-1)*ncy+(ncy-1)*ncx
print(f"seams: {vseams} vertical per layer x {len(LAYERS)} layers + {hseams} horizontal")
print(f"pegs needed (3 per mating face): {(vseams*len(LAYERS)+ncx*ncy*hseams)*3}")
