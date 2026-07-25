import bpy, sys, math, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
exec(open(sys.argv[-3]).read())

# --- limestone, faintly damp -------------------------------------------
m = bpy.data.materials.new("limestone"); m.use_nodes=True
nt=m.node_tree; b=nt.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value=(0.115,0.113,0.108,1)
b.inputs["Roughness"].default_value=0.52
noise=nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value=140
ramp=nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position=0.36; ramp.color_ramp.elements[1].position=0.68
ramp.color_ramp.elements[0].color=(0.055,0.055,0.052,1)
ramp.color_ramp.elements[1].color=(0.235,0.230,0.215,1)
nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
bump=nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.62
nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
mass = bpy.data.objects["M8_preview"]; mass.data.materials.append(m)

# --- lighting, matched to the reference: low warm horizon key, cool sky --
bpy.ops.object.light_add(type='AREA', location=(-0.55,-0.52,0.085))
key=bpy.context.active_object; key.data.energy=18; key.data.size=0.30
key.data.color=(1.0,0.62,0.46)                       # sunset off the water
key.rotation_euler=mathutils.Vector((0.03,0.005,0.055)).to_track_quat('-Z','Y').to_euler()
key.rotation_euler=(math.radians(80), 0, math.radians(-46))
bpy.ops.object.light_add(type='AREA', location=(0.10,-0.10,0.62))
sky=bpy.context.active_object; sky.data.energy=1.6; sky.data.size=1.6
sky.data.color=(0.55,0.68,1.0); sky.rotation_euler=(0,0,0)   # cool zenith

w=bpy.data.worlds.new("w"); bpy.context.scene.world=w; w.use_nodes=True
wnt=w.node_tree; bg=wnt.nodes["Background"]
bg.inputs[0].default_value=(0.10,0.14,0.24,1); bg.inputs[1].default_value=0.30

# wet sand
bpy.ops.mesh.primitive_plane_add(size=4)
gp=bpy.context.active_object
gm=bpy.data.materials.new("sand"); gm.use_nodes=True
gb=gm.node_tree.nodes["Principled BSDF"]
gb.inputs["Base Color"].default_value=(0.105,0.092,0.078,1)
gb.inputs["Roughness"].default_value=0.10
gp.data.materials.append(gm)

s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.device='CPU'; s.cycles.samples=90
s.cycles.use_denoising=False
s.render.resolution_x, s.render.resolution_y = 1100, 760
s.view_settings.look = 'AgX - Medium High Contrast'
CEN=(0.012,0.005,0.052)
def shoot(loc, path, lens=50):
    bpy.ops.object.camera_add(location=loc); c=bpy.context.active_object
    c.data.lens=lens
    v=mathutils.Vector(CEN)-mathutils.Vector(loc)
    c.rotation_euler=v.to_track_quat('-Z','Y').to_euler()
    s.camera=c; s.render.filepath=path; bpy.ops.render.render(write_still=True)
out=sys.argv[-1]
shoot((-0.265,-0.375,0.052), out+"_hero.png", 40)
shoot((-0.05,-0.30,0.030), out+"_low.png", 34)
