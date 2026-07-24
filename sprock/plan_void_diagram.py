import bpy, sys, math
bpy.ops.wm.read_factory_settings(use_empty=True)
MM=0.001; W=180*MM; D=140*MM

def emit(name, rgb):
    m=bpy.data.materials.new(name); m.use_nodes=True
    nt=m.node_tree; nt.nodes.clear()
    e=nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value=(*rgb,1); e.inputs[1].default_value=1.0
    o=nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0])
    return m
BLUE=emit("blue",(0.15,0.42,0.95)); RED=emit("red",(0.92,0.13,0.13))
GREEN=emit("green",(0.16,0.80,0.30)); DARK=emit("dark",(0.13,0.13,0.15))
YELL=emit("yellow",(0.98,0.80,0.10))

def slab(name, x, y, sx, sy, z, mat, rot=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x,y,z))
    o=bpy.context.active_object; o.name=name; o.scale=(sx,sy,0.001)
    o.rotation_euler=(0,0,rot); bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(mat); return o
def disc(name, x, y, r, z, mat, sy=1.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=r, depth=0.001, location=(x,y,z))
    o=bpy.context.active_object; o.name=name; o.scale=(1,sy,1)
    bpy.ops.object.transform_apply(scale=True); o.data.materials.append(mat); return o

# BLUE perimeter (slightly larger plate reads as an outline)
slab("perimeter", 0,0, W+8*MM, D+8*MM, 0.000, BLUE)
slab("body",      0,0, W,       D,      0.001, DARK)

# RED = the two glass faces: back (+Y) and left (-X). Locked corner format.
slab("glass_back", 0,      D/2-3*MM, W,      6*MM, 0.002, RED)
slab("glass_left", -W/2+3*MM, 0,     6*MM,   D,    0.002, RED)

# GREEN = fish-usable space. One connected void, mouth-in -> gallery -> tail-out.
disc("chamber", 22*MM, -14*MM, 42*MM, 0.003, GREEN, sy=0.72)   # the den
slab("throat_mouth", 74*MM, -25*MM, 42*MM, 24*MM, 0.003, GREEN) # in from RIGHT face
slab("gallery", -39.5*MM, -34.5*MM, 62*MM, 17*MM, 0.003, GREEN, rot=math.radians(25))
# FAULT 2: exit was 13 mm -- neither clearly passable nor clearly impossible,
# which is the exact "no wedges" in-between the BIO gate forbids. Now 18 mm:
# passable, still visibly smaller than the 24 mm mouth (front door / back door).
slab("throat_exit", -64*MM, -60*MM, 18*MM, 30*MM, 0.003, GREEN, rot=math.radians(-8))

# YELLOW = skylight, over the GALLERY only (never over the chamber)
slab("skylight", -38*MM, -34*MM, 28*MM, 6*MM, 0.004, YELL, rot=math.radians(25))

s=bpy.context.scene
bpy.ops.object.camera_add(location=(0,0,0.5), rotation=(0,0,0))
c=bpy.context.active_object; c.data.type='ORTHO'; c.data.ortho_scale=0.21
s.camera=c
s.render.engine='CYCLES'; s.cycles.device='CPU'; s.cycles.samples=8
s.cycles.use_denoising=False
s.render.resolution_x, s.render.resolution_y = 900, 740
s.world=bpy.data.worlds.new("w"); s.world.use_nodes=True
s.world.node_tree.nodes["Background"].inputs[1].default_value=0.0
s.render.filepath=sys.argv[-1]
bpy.ops.render.render(write_still=True)

# --- gate check in numbers (slab args are FULL dimensions, not half) ---
floor_x, floor_y = 2*42, 2*42*0.72      # disc() takes a true radius
mouth_w, exit_w  = 24, 18
print(f"\nchamber clear floor : {floor_x:.0f} x {floor_y:.0f} mm")
print(f"mouth width         : {mouth_w} mm  (RIGHT face)")
print(f"exit width          : {exit_w} mm  (FRONT-left)   exit<mouth: {exit_w<mouth_w}")
print(f"turn-room 1.5x rule : fish up to {floor_y/1.5:.0f} mm long (~{floor_y/1.5/25.4:.1f} in)")
print(f"passable-or-impossible: exit {exit_w} mm vs ~15 mm body depth -> passable, not a wedge")
