import bpy, sys
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())
rock=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith("talus")
      and len(o.data.polygons)>0]
hits=[]
for ob in rock:
    polys=list(ob.data.polygons); step=max(1,len(polys)//260)
    for f in polys[::step]:
        c=ob.matrix_world @ f.center
        nr=(ob.matrix_world.to_3x3() @ f.normal).normalized()
        ok,loc,nor,idx=ob.ray_cast(ob.matrix_world.inverted() @ (c-nr*0.0002),
                                   ob.matrix_world.inverted().to_3x3() @ (-nr))
        if not ok: continue
        d=((ob.matrix_world @ loc)-c).length/MM
        if d<1.2:
            hits.append((d, ob.name, c.x/MM, c.y/MM, c.z/MM, abs(nr.z)))
hits.sort()
print(f"\nthin samples: {len(hits)}")
import math
radial=0
for d,nm,x,y,z,nz in hits[:16]:
    r=math.hypot(x/(W/2), y/(D/2))
    tag="OUTER EDGE" if r>0.80 else ("near-vertical face" if nz<0.4 else "flat face")
    if r>0.80: radial+=1
    print(f"  {d:5.2f}mm {nm:<16} ({x:7.1f},{y:7.1f},{z:6.1f}) r={r:.2f} |nz|={nz:.2f}  {tag}")
print(f"\nof the worst 16, {radial} are on the OUTER EDGE of a bed "
      f"(r>0.80 of the footprint)")
