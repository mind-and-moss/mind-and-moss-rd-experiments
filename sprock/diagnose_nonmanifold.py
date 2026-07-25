import bpy, bmesh, sys
MM=0.001
exec(open(sys.argv[-1]).read())
print("\n--- NON-MANIFOLD BY OBJECT ---")
tot=0
for o in sorted([x for x in bpy.data.objects if x.type=='MESH'], key=lambda a:a.name):
    bm=bmesh.new(); bm.from_mesh(o.data)
    bad=[e for e in bm.edges if not e.is_manifold]
    boundary=[e for e in bm.edges if len(e.link_faces)==1]
    multi=[e for e in bm.edges if len(e.link_faces)>2]
    if bad:
        print(f"{o.name:<20} nm={len(bad):4d}  boundary={len(boundary):4d}  "
              f"multi-face={len(multi):4d}  faces={len(o.data.polygons)}")
        tot+=len(bad)
    bm.free()
print(f"total non-manifold edges: {tot}")
