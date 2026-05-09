# -*- coding: utf-8 -*-
"""
export_drive_pulley_stl.py
==========================

KNOWN BUG (Session 7): MeshPart.meshFromShape + mesh.write hangs under
freecadcmd.exe on Windows for this part. Two separate invocations were
tried (build FCStd in invocation 1, this script in invocation 2);
in-session save+close+reopen+export was also tried. Both hang on the
mesh-write step. Root cause not yet identified — possibly a GUI-binding
dependency in MeshPart that doesn't satisfy under freecadcmd.

WORKAROUND for first physical print: export STL manually from the GUI.
  1. Open parts/drive_pulley.FCStd in FreeCAD 1.1.1
  2. Right-click 'Pulley' (the Revolution feature) -> Export...
  3. Save as drive_pulley.stl in the same folder
  4. Load STL in your slicer (Bambu Studio for A1 Mini)

Once the headless hang is fixed, this script's intended behavior:
- Open master + part
- Recompute (shape populates from fresh load)
- Tessellate Revolution.Shape (MaxLength 0.5 mm -> ~480 tri per face)
- Write parts/drive_pulley.stl
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PART_PATH = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "parts", "drive_pulley.FCStd")
)
STL_PATH = os.path.join(os.path.dirname(PART_PATH), "drive_pulley.stl")
GRINDER_PARAMS = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd")
)

if not os.path.exists(PART_PATH):
    print(f"[export] ERROR: part not found: {PART_PATH}")
    print(f"[export] Run macro 05 first.")
    sys.exit(1)

import FreeCAD as App  # noqa: E402
import MeshPart  # noqa: E402

# Open master first so any cross-doc references in the part doc resolve
# (currently macro 05 v1 has no live cross-doc refs, but macro 06 will)
if os.path.exists(GRINDER_PARAMS):
    App.openDocument(GRINDER_PARAMS)
    print("[export] Master loaded.")

print(f"[export] Loading part: {PART_PATH}")
part_doc = App.openDocument(PART_PATH)
part_doc.recompute()

revolution = part_doc.getObject("Pulley")
if revolution is None:
    print("[export] ERROR: 'Pulley' Revolution feature not found in part doc")
    sys.exit(1)

shape = revolution.Shape
print(f"[export] Shape: isNull={shape.isNull()}, "
      f"Volume={shape.Volume if not shape.isNull() else 'N/A'}")

if shape.isNull() or shape.Volume <= 0:
    print("[export] ERROR: Shape is null/empty - can't export STL")
    sys.exit(1)

print(f"[export] Tessellating (MaxLength=0.5 mm)...")
mesh = MeshPart.meshFromShape(Shape=shape, MaxLength=0.5)

print(f"[export] Writing STL: {STL_PATH}")
mesh.write(STL_PATH)
stl_size_kb = os.path.getsize(STL_PATH) / 1024.0
print(f"[export] STL: {stl_size_kb:.1f} KB, {mesh.CountFacets} triangles")

print("[export] Done.")
