# ============================================================================
# MONSTER8 — SCRIPT 08: PREVIEW MESH (remesh -> displace)
#
# STACK-ORDER LAW, obeyed exactly:
#     all geometry/booleans FIRST -> voxel remesh -> displacement LAST
# Displacement is PREVIEW ONLY. It never touches the print core.
#
# The block objects from script 06 stay untouched as the source of truth.
# This builds a SEPARATE object, M8_preview, so "everything stays separate
# objects" still holds.
# ============================================================================
import bpy, sys, math

exec(open(sys.argv[-2]).read())          # build the blocks (script 06)

src = [o for o in bpy.data.objects if o.type=='MESH' and
       (o.name.startswith("B") or o.name.startswith("talus"))]
print(f"source blocks: {len(src)}")

# --- duplicate + join into one mass -------------------------------------
bpy.ops.object.select_all(action='DESELECT')
copies=[]
for o in src:
    d = o.copy(); d.data = o.data.copy()
    bpy.context.collection.objects.link(d); copies.append(d)
for d in copies: d.select_set(True)
bpy.context.view_layer.objects.active = copies[0]
# bake the wear bevels before joining, or the remesh ignores them
for d in copies:
    bpy.context.view_layer.objects.active = d
    for m in list(d.modifiers): bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.select_all(action='DESELECT')
for d in copies: d.select_set(True)
bpy.context.view_layer.objects.active = copies[0]
bpy.ops.object.join()
mass = bpy.context.active_object
mass.name = "M8_preview"

# --- VOXEL REMESH: welds the blocks into one rock body -------------------
mass.data.remesh_voxel_size = 0.0020        # 2.0 mm
mass.data.remesh_voxel_adaptivity = 0.0
bpy.context.view_layer.objects.active = mass
bpy.ops.object.voxel_remesh()
print(f"after remesh: {len(mass.data.vertices)} verts, {len(mass.data.polygons)} faces")

# --- DISPLACEMENT: last, preview only -----------------------------------
# two scales: broad form break-up, then surface grain.
broad = bpy.data.textures.new("broad", 'CLOUDS')
broad.noise_scale = 0.070; broad.noise_depth = 2
grain = bpy.data.textures.new("grain", 'CLOUDS')
grain.noise_scale = 0.028; grain.noise_depth = 3

d1 = mass.modifiers.new("form", 'DISPLACE')
d1.texture = broad; d1.strength = 0.0115; d1.mid_level = 0.5
d2 = mass.modifiers.new("grain", 'DISPLACE')
d2.texture = grain; d2.strength = 0.0034; d2.mid_level = 0.5
sm = mass.modifiers.new("smooth", 'SMOOTH'); sm.iterations = 1; sm.factor = 0.4
bpy.ops.object.shade_smooth()

for o in src: o.hide_render = True          # show the preview mass only
print("preview mesh built")
