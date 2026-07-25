import bpy, sys, math, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
exec(open(sys.argv[-3]).read())
MODE = sys.argv[-2]          # "clay" or "zones"

def emit(name, rgb):
    m=bpy.data.materials.new(name); m.use_nodes=True
    nt=m.node_tree; nt.nodes.clear()
    e=nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value=(*rgb,1)
    e.inputs[1].default_value=1.0
    o=nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0],o.inputs[0])
    return m

# --- the nine zones -------------------------------------------------------
ZC = [
 ("1 hard face",    (0.86,0.24,0.20)),
 ("2 soft band",    (0.96,0.68,0.14)),
 ("3 ledge top",    (0.20,0.65,0.95)),
 ("4 mouth rim",    (0.95,0.36,0.80)),
 ("5 cave inside",  (0.13,0.13,0.16)),
 ("6 undercut",     (0.55,0.25,0.85)),
 ("7 medium face",  (0.20,0.78,0.42)),
 ("8 perch top",    (0.98,0.93,0.30)),
 ("9 buried edge",  (0.52,0.40,0.28)),
]
mats=[emit(n,c) for n,c in ZC]
clay=bpy.data.materials.new("clay"); clay.use_nodes=True
_cb=clay.node_tree.nodes["Principled BSDF"]
_cb.inputs["Base Color"].default_value=(0.56,0.55,0.52,1)
_cb.inputs["Roughness"].default_value=0.85

for ob in [o for o in bpy.data.objects if o.type=='MESH']:
    hard = ob.get("hardness",3)
    ob.data.materials.clear()
    if MODE=="clay":
        ob.data.materials.append(clay); continue
    for m in mats: ob.data.materials.append(m)
    for f in ob.data.polygons:
        c = ob.matrix_world @ f.center
        n = f.normal
        x,y,zc = c.x/MM, c.y/MM, c.z/MM
        near_mouth = (MOUTH_X-MOUTH_W/2-30 < x < MOUTH_X+MOUTH_W/2+30) and y < 0
        if zc < 14:                       z_i = 8      # 9 buried edge
        elif near_mouth and 30 < zc < 70: z_i = 3      # 4 mouth rim
        elif near_mouth and n.z < -0.35:  z_i = 4      # 5 cave inside
        elif n.z < -0.35:                 z_i = 5      # 6 undercut
        elif n.z > 0.70:
            z_i = 7 if zc > 175 else 2                 # 8 perch top / 3 ledge
        elif hard >= 4:                   z_i = 0      # 1 hard face
        elif hard <= 2:                   z_i = 1      # 2 soft band
        else:                             z_i = 6      # 7 medium face
        f.material_index = z_i

s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.device='CPU'; s.cycles.samples=16
s.cycles.use_denoising=False
s.render.resolution_x,s.render.resolution_y=1200,820
w=bpy.data.worlds.new("w"); s.world=w; w.use_nodes=True
w.node_tree.nodes["Background"].inputs[1].default_value=(0.0 if MODE=="zones" else 0.12)
if MODE=="clay":
    bpy.ops.object.light_add(type='AREA', location=(-0.10,-0.45,0.55))
    k=bpy.context.active_object; k.data.energy=38; k.data.size=0.55
    k.rotation_euler=(0.62,-0.10,-0.18)
    bpy.ops.object.light_add(type='AREA', location=(0.40,-0.30,0.16))
    f2=bpy.context.active_object; f2.data.energy=3; f2.data.size=0.7
    f2.rotation_euler=(1.4,0,0.9)
CEN=(0.0,0.0,0.085)
def shoot(loc,path,lens=52):
    bpy.ops.object.camera_add(location=loc); c=bpy.context.active_object
    c.data.lens=lens
    v=mathutils.Vector(CEN)-mathutils.Vector(loc)
    c.rotation_euler=v.to_track_quat('-Z','Y').to_euler()
    s.camera=c; s.render.filepath=path; bpy.ops.render.render(write_still=True)
out=sys.argv[-1]
shoot((-0.34,-0.52,0.24), out+"_3q.png", 46)
shoot((-0.46,-0.40,0.10), out+"_cave.png", 50)
