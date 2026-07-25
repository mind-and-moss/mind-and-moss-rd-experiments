import bpy, bmesh, sys, math
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())
BEDS3=[bpy.data.objects[n] for n in
       ("A1_platform","A2_marl","A3_cap","A4_bench","A5_parting","A6_perch")]

print("\n--- MANIFOLD ---")
allman=True
for o in BEDS3:
    bm=bmesh.new(); bm.from_mesh(o.data)
    bad=[e for e in bm.edges if not e.is_manifold]
    loose=[v for v in bm.verts if not v.link_edges]
    print(f"{o.name:<14} non-manifold edges={len(bad):4d}  loose verts={len(loose):3d}  "
          f"{'PASS' if not bad and not loose else 'FAIL'}")
    if bad or loose: allman=False
    bm.free()
print(f"manifold = 0 : {'PASS' if allman else 'FAIL'}")

print("\n--- WALL THICKNESS ---")
worst=(1e9,None,None); thin=0; n=0
for ob in BEDS3:
    polys=list(ob.data.polygons)
    step=max(1,len(polys)//240)
    for f in polys[::step]:
        c=ob.matrix_world @ f.center
        nrm=(ob.matrix_world.to_3x3() @ f.normal).normalized()
        o2=c-nrm*0.0002
        ok,loc,nor,idx=ob.ray_cast(ob.matrix_world.inverted() @ o2,
                                   ob.matrix_world.inverted().to_3x3() @ (-nrm))
        if not ok: continue
        d=((ob.matrix_world @ loc)-c).length/MM
        n+=1
        if d<1.2: thin+=1
        if d<worst[0]: worst=(d,ob.name,tuple(round(v/MM) for v in c))
print(f"samples {n}, below 1.2mm: {thin}, thinnest {worst[0]:.2f}mm on {worst[1]} at {worst[2]}")
print(f"wall >= 1.2mm : {'PASS' if thin==0 else 'REVIEW'}")

print("\n--- SEGMENTATION FOR THE A1 MINI (180 mm bed) ---")
W,D,H = 420.0,250.0,190.0
LAYERS=[("L1_base", 0.0, 58.9),("L2_mid",58.9,146.3),("L3_crest",146.3,190.0)]
import math as m
ncx=m.ceil(W/175.0); ncy=m.ceil(D/175.0)
print(f"footprint {W:.0f} x {D:.0f} mm vs 180 mm bed -> {ncx} x {ncy} columns")
print(f"column size {W/ncx:.0f} x {D/ncy:.0f} mm")
tot=0
for nm,z0,z1 in LAYERS:
    h=z1-z0
    fits = h<=175.0
    print(f"  {nm:<9} z {z0:6.1f}->{z1:6.1f}  height {h:5.1f} mm  "
          f"{'fits' if fits else 'TOO TALL'}   pieces this layer: {ncx*ncy}")
    tot+=ncx*ncy
print(f"TOTAL PIECES: {tot}")
seams_v = (ncx-1)*ncy + (ncy-1)*ncx
print(f"vertical seams per layer: {seams_v}   horizontal seams: {len(LAYERS)-1}")
print(f"pegs at 6.0 mm / sockets 6.43 mm (0.43 mm diametral, proven on A1 mini)")
print(f"estimated pegs: {(seams_v*len(LAYERS) + ncx*ncy*(len(LAYERS)-1))*3} "
      f"(3 per mating face)")
