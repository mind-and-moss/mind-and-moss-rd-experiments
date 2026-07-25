import bpy, bmesh, sys, math, mathutils
from mathutils import Vector
MM=0.001
exec(open(sys.argv[-2]).read())

rock=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith("talus")
      and len(o.data.polygons)>0]
tal =[o for o in bpy.data.objects if o.name.startswith("talus")]
print(f"\nrock laminae {len(rock)}, talus {len(tal)}")

# join copies of the rock into one mass, then voxel remesh (canon order)
bpy.ops.object.select_all(action='DESELECT')
copies=[]
for o in rock+tal:
    d=o.copy(); d.data=o.data.copy(); bpy.context.collection.objects.link(d); copies.append(d)
for d in copies:
    bpy.context.view_layer.objects.active=d
    for m in list(d.modifiers): bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.select_all(action='DESELECT')
for d in copies: d.select_set(True)
bpy.context.view_layer.objects.active=copies[0]
bpy.ops.object.join()
mass=bpy.context.active_object; mass.name="M8_PREVIEW"
mass.data.remesh_voxel_size=0.0022
bpy.ops.object.voxel_remesh()
print(f"after remesh: {len(mass.data.vertices)} verts, {len(mass.data.polygons)} faces")

bm=bmesh.new(); bm.from_mesh(mass.data)
bad=[e for e in bm.edges if not e.is_manifold]
print(f"MANIFOLD after remesh: {len(bad)} non-manifold edges   "
      f"{'PASS' if not bad else 'FAIL'}")
seen=set(); comps=[]
for v in bm.verts:
    if v in seen: continue
    n=0; st=[v]; seen.add(v)
    while st:
        c=st.pop(); n+=1
        for e in c.link_edges:
            o2=e.other_vert(c)
            if o2 not in seen: seen.add(o2); st.append(o2)
    comps.append(n)
comps.sort(reverse=True)
print(f"components after remesh: {len(comps)}  sizes {comps[:5]}")
bm.free()
for o in rock+tal: o.hide_render=True

# displacement LAST, preview only
broad=bpy.data.textures.new("broad",'CLOUDS'); broad.noise_scale=0.075; broad.noise_depth=2
grain=bpy.data.textures.new("grain",'CLOUDS'); grain.noise_scale=0.026; grain.noise_depth=3
d1=mass.modifiers.new("form",'DISPLACE'); d1.texture=broad; d1.strength=0.0042; d1.mid_level=0.5
d2=mass.modifiers.new("grain",'DISPLACE'); d2.texture=grain; d2.strength=0.0016; d2.mid_level=0.5
sm=mass.modifiers.new("s",'SMOOTH'); sm.iterations=1; sm.factor=0.35
bpy.ops.object.shade_smooth()

m=bpy.data.materials.new("ls"); m.use_nodes=True
b=m.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value=(0.24,0.238,0.228,1); b.inputs["Roughness"].default_value=0.72
mass.data.materials.append(m)
bpy.ops.object.light_add(type='AREA', location=(-0.24,-0.50,0.46))
k=bpy.context.active_object; k.data.energy=26; k.data.size=0.42
k.data.color=(1.0,0.80,0.66); k.rotation_euler=(0.66,-0.14,-0.30)
bpy.ops.object.light_add(type='AREA', location=(0.40,-0.24,0.30))
f=bpy.context.active_object; f.data.energy=2.2; f.data.size=0.7
f.data.color=(0.62,0.74,1.0); f.rotation_euler=(1.1,0,1.0)
bpy.ops.mesh.primitive_plane_add(size=4)
gp=bpy.context.active_object
gm=bpy.data.materials.new("sand"); gm.use_nodes=True
gb=gm.node_tree.nodes["Principled BSDF"]
gb.inputs["Base Color"].default_value=(0.17,0.15,0.13,1); gb.inputs["Roughness"].default_value=0.55
gp.data.materials.append(gm)
s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.device='CPU'
s.cycles.samples=52; s.cycles.use_denoising=False
s.render.resolution_x,s.render.resolution_y=1200,830
s.view_settings.look='AgX - Medium High Contrast'
w=bpy.data.worlds.new("w"); s.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[0].default_value=(0.10,0.13,0.20,1)
w.node_tree.nodes["Background"].inputs[1].default_value=0.35
CEN=(0.0,0.0,0.082)
def shoot(loc,path,lens=48):
    bpy.ops.object.camera_add(location=loc); c=bpy.context.active_object
    c.data.lens=lens
    v=mathutils.Vector(CEN)-mathutils.Vector(loc)
    c.rotation_euler=v.to_track_quat('-Z','Y').to_euler()
    s.camera=c; s.render.filepath=path; bpy.ops.render.render(write_still=True)
out=sys.argv[-1]
shoot((-0.36,-0.50,0.20), out+"_hero.png", 46)
shoot((0.30,-0.44,0.13), out+"_right.png", 48)
