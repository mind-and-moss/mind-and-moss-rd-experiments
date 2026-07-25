import bpy, sys
MM=0.001
exec(open(sys.argv[-1]).read())
print("\n--- OBJECTS IN SCENE ---")
for o in sorted([x for x in bpy.data.objects if x.type=='MESH'], key=lambda a:a.name):
    bb=o.bound_box
    dx=abs(bb[6][0]-bb[0][0])/MM; dy=abs(bb[6][1]-bb[0][1])/MM; dz=abs(bb[6][2]-bb[0][2])/MM
    if not o.name.startswith("talus"):
        print(f"  {o.name:<22} {dx:6.0f} x {dy:6.0f} x {dz:6.0f} mm  faces={len(o.data.polygons)}")
print(f"talus count: {len([x for x in bpy.data.objects if x.name.startswith('talus')])}")
