# MINIMUM-FEATURE CLEANUP for print prep.
# Voxel remesh alone does NOT remove thin flanges -- it faithfully reproduces
# them as thin shells. What removes them is a morphological OPENING: shrink the
# solid, remesh (features thinner than the shrink vanish because there is no
# solid left there), then grow it back.
import bpy, bmesh, sys
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-1]).read())
src=[o for o in bpy.data.objects if o.type=='MESH' and len(o.data.polygons)>0]
bpy.ops.object.select_all(action='DESELECT')
cp=[]
for o in src:
    d=o.copy(); d.data=o.data.copy(); bpy.context.collection.objects.link(d); cp.append(d)
for d in cp:
    bpy.context.view_layer.objects.active=d
    for m in list(d.modifiers): bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.select_all(action='DESELECT')
for d in cp: d.select_set(True)
bpy.context.view_layer.objects.active=cp[0]
bpy.ops.object.join()
mass=bpy.context.active_object; mass.name="M8_PRINT"

def probe(tag):
    bm=bmesh.new(); bm.from_mesh(mass.data)
    bad=[e for e in bm.edges if not e.is_manifold]; bm.free()
    worst=1e9; thin=0; n=0
    polys=list(mass.data.polygons); step=max(1,len(polys)//2200)
    for f in polys[::step]:
        c=mass.matrix_world @ f.center
        nr=(mass.matrix_world.to_3x3() @ f.normal).normalized()
        ok,loc,nor,idx=mass.ray_cast(mass.matrix_world.inverted() @ (c-nr*0.0002),
                                     mass.matrix_world.inverted().to_3x3() @ (-nr))
        if not ok: continue
        d2=((mass.matrix_world @ loc)-c).length/MM; n+=1
        if d2<1.2: thin+=1
        worst=min(worst,d2)
    print(f"[{tag:<22}] verts={len(mass.data.vertices):7d} nm={len(bad):3d} "
          f"thin={thin:3d}/{n} thinnest={worst:.2f}mm")
    return thin

SHRINK = 1.10        # must exceed half the minimum wall we want to keep
mass.data.remesh_voxel_size=0.0022
bpy.ops.object.voxel_remesh(); probe("remesh only")

d=mass.modifiers.new("shrink",'DISPLACE'); d.strength=-SHRINK*MM; d.mid_level=0.0
bpy.ops.object.modifier_apply(modifier="shrink")
mass.data.remesh_voxel_size=0.0020
bpy.ops.object.voxel_remesh(); probe("after shrink+remesh")

g=mass.modifiers.new("grow",'DISPLACE'); g.strength=SHRINK*MM; g.mid_level=0.0
bpy.ops.object.modifier_apply(modifier="grow")
mass.data.remesh_voxel_size=0.0020
bpy.ops.object.voxel_remesh(); thin=probe("after grow (OPENED)")
print(f"MIN-FEATURE GATE: {'PASS' if thin==0 else 'REVIEW'}")
