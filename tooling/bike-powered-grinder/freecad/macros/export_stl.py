# -*- coding: utf-8 -*-
"""
export_stl.py — generic per-part STL exporter

Loads a single part .FCStd, finds its top-level Body or named feature,
tessellates the shape, writes an ASCII STL alongside the FCStd.

Bypasses MeshPart.meshFromShape (which hangs under freecadcmd) by using
TopoShape.tessellate() + manual ASCII STL writing. shape.tessellate(tol)
returns (vertices, triangle_indices) — pure compute, no GUI binding.

USAGE
-----
Edit PART_BASENAME below (or pass via argv) to pick a different part.
Run via:
    "C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" export_stl.py [partname]

Where partname is the basename without .FCStd, e.g. "drive_pulley".
Looks for parts/<partname>.FCStd and writes parts/<partname>.stl.
"""

import os
import sys
import math
import FreeCAD as App


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "parts"))

# Allow CLI override: freecadcmd export_stl.py drive_pulley
PART_BASENAME = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith(".py") else "drive_pulley"

PART_PATH = os.path.join(PARTS_DIR, f"{PART_BASENAME}.FCStd")
STL_PATH = os.path.join(PARTS_DIR, f"{PART_BASENAME}.stl")
GRINDER_PARAMS = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd")
)

if not os.path.exists(PART_PATH):
    App.Console.PrintError(f"[export] part not found: {PART_PATH}\n")
    sys.exit(1)

# Open master first so cross-doc references resolve (if any)
if os.path.exists(GRINDER_PARAMS):
    App.openDocument(GRINDER_PARAMS)

App.Console.PrintMessage(f"[export] Loading: {PART_PATH}\n")
part_doc = App.openDocument(PART_PATH)
part_doc.recompute()

# Find the shape to export. Strategy: use the Body if present, else use
# the named feature, else the first object with a non-null Shape.
shape = None
for obj_name in ("PulleyBody", "Body", "Pulley"):
    o = part_doc.getObject(obj_name)
    if o and hasattr(o, "Shape") and not o.Shape.isNull() and o.Shape.Volume > 0:
        shape = o.Shape
        App.Console.PrintMessage(f"[export] Using shape from: {obj_name}\n")
        break

if shape is None:
    # Fallback: scan all objects
    for o in part_doc.Objects:
        if hasattr(o, "Shape") and not o.Shape.isNull() and o.Shape.Volume > 0:
            shape = o.Shape
            App.Console.PrintMessage(f"[export] Fallback shape from: {o.Name}\n")
            break

if shape is None:
    App.Console.PrintError("[export] No usable Shape found in part doc\n")
    sys.exit(1)

App.Console.PrintMessage(
    f"[export] Shape volume: {shape.Volume:.1f} mm³, "
    f"{len(shape.Faces)} faces\n"
)

# Tessellate. tolerance = max chord deviation from true surface.
# 0.1 mm gives plenty of detail on a 152mm pulley.
TOLERANCE = 0.1
verts, tris = shape.tessellate(TOLERANCE)
App.Console.PrintMessage(
    f"[export] Tessellated: {len(verts)} verts, {len(tris)} triangles\n"
)


def normal(v1, v2, v3):
    """Compute outward facet normal via cross product of edges."""
    ax, ay, az = v2.x - v1.x, v2.y - v1.y, v2.z - v1.z
    bx, by, bz = v3.x - v1.x, v3.y - v1.y, v3.z - v1.z
    nx = ay * bz - az * by
    ny = az * bx - ax * bz
    nz = ax * by - ay * bx
    mag = math.sqrt(nx * nx + ny * ny + nz * nz)
    if mag < 1e-12:
        return (0.0, 0.0, 0.0)
    return (nx / mag, ny / mag, nz / mag)


# Write ASCII STL
App.Console.PrintMessage(f"[export] Writing ASCII STL: {STL_PATH}\n")
with open(STL_PATH, "w") as f:
    f.write(f"solid {PART_BASENAME}\n")
    for tri in tris:
        v1 = verts[tri[0]]
        v2 = verts[tri[1]]
        v3 = verts[tri[2]]
        n = normal(v1, v2, v3)
        f.write(f"  facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n")
        f.write("    outer loop\n")
        f.write(f"      vertex {v1.x:.6e} {v1.y:.6e} {v1.z:.6e}\n")
        f.write(f"      vertex {v2.x:.6e} {v2.y:.6e} {v2.z:.6e}\n")
        f.write(f"      vertex {v3.x:.6e} {v3.y:.6e} {v3.z:.6e}\n")
        f.write("    endloop\n")
        f.write("  endfacet\n")
    f.write(f"endsolid {PART_BASENAME}\n")

stl_kb = os.path.getsize(STL_PATH) / 1024.0
App.Console.PrintMessage(
    f"[export] STL: {stl_kb:.1f} KB, {len(tris)} triangles\n"
)
