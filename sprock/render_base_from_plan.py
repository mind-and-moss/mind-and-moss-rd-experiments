import bpy, sys, math, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
exec(open(sys.argv[-2]).read())
m=bpy.data.materials.new("clay"); m.use_nodes=True
b=m.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value=(0.52,0.51,0.49,1); b.inputs["Roughness"].default_value=0.88
for o in [x for x in bpy.data.objects if x.type=='MESH']: o.data.materials.append(m)
bpy.ops.object.light_add(type='AREA', location=(-0.16,-0.34,0.42))
k=bpy.context.active_object; k.data.energy=30; k.data.size=0.42; k.rotation_euler=(0.62,-0.14,-0.30)
bpy.ops.object.light_add(type='AREA', location=(0.30,-0.26,0.14))
f=bpy.context.active_object; f.data.energy=2.6; f.data.size=0.6; f.rotation_euler=(1.36,0,0.9)
bpy.ops.mesh.primitive_plane_add(size=2)
s=bpy.context.scene; s.render.engine='CYCLES'; s.cycles.device='CPU'
s.cycles.samples=34; s.cycles.use_denoising=False
s.render.resolution_x,s.render.resolution_y=1100,800
w=bpy.data.worlds.new("w"); s.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[1].default_value=0.06
CEN=(0.012,0.010,0.085)
def shoot(loc,path,lens=46,ortho=None):
    bpy.ops.object.camera_add(location=loc); c=bpy.context.active_object
    if ortho: c.data.type='ORTHO'; c.data.ortho_scale=ortho
    else: c.data.lens=lens
    v=mathutils.Vector(CEN)-mathutils.Vector(loc)
    c.rotation_euler=v.to_track_quat('-Z','Y').to_euler()
    s.camera=c; s.render.filepath=path; bpy.ops.render.render(write_still=True)
out=sys.argv[-1]
shoot((0.012,0.010,0.62), out+"_top.png", ortho=0.30)   # LOOKING DOWNWARDS
shoot((-0.28,-0.34,0.16), out+"_3q.png", 44)
