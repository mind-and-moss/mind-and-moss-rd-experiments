# -*- coding: utf-8 -*-
"""
02_scaffold_drivetrain_geometry.py
==================================

Adds construction geometry to the MasterSketch inside Grinder_Params.FCStd.
This is the 2D drivetrain layout — pulley centers, sprocket pitch circles,
platen extent, all visible at once in a top-down view.

WHAT GETS ADDED
===============
All geometry is "construction" (orange dashed in the GUI) — it doesn't
become part of any printed/manufactured shape. It's reference geometry
that downstream part files will external-link to.

  origin (0, 0)            ← drive pulley shaft (drive pulley + stage-2 pinion)
  (-belt_center_distance, 0)  ← idler shaft
  rectangle between pulleys   ← platen 22"x60mm
  (0, 200)                 ← intermediate shaft (stage-1 cog + stage-2 large sprocket co-axial)
  (0, 650)                 ← crank / BB (chainring + freewheel co-axial)

PREREQUISITES
=============
Grinder_Params.FCStd must be the active document with a sketch named
"MasterSketch" already present (created by macro 01).

IDEMPOTENT
==========
This macro clears the MasterSketch before adding geometry, so you can
re-run it as many times as you want without piling up duplicate circles.

NEXT STEP
=========
Macro 03 (when written) will bind these geometric values to expression
references against the VarSets, so changing a parameter automatically
moves the geometry. For now the values are hardcoded to match the
current locked spec.
"""

import math
import FreeCAD as App
import Part
from FreeCAD import Vector


# =====================================================================
# Sanity-check: we have an active Grinder_Params doc with a MasterSketch
# =====================================================================

doc = App.ActiveDocument
if doc is None:
    raise RuntimeError("No active document. Open Grinder_Params.FCStd first.")

if doc.Name != "Grinder_Params":
    App.Console.PrintWarning(
        f"Active doc is '{doc.Name}', expected 'Grinder_Params'. "
        "Continuing — but check you're in the right file.\n"
    )

sketch = doc.getObject("MasterSketch")
if sketch is None:
    raise RuntimeError(
        "MasterSketch not found. Run macro 01 first to create it."
    )


# =====================================================================
# Geometry values (hardcoded to match the current locked spec)
# =====================================================================
# These values mirror the VarSets in Grinder_Params. Macro 03 will bind
# them to live expressions; for this first pass they're static literals.

DRIVE_PULLEY_RADIUS = 76.2       # 6" / 2
IDLER_PULLEY_RADIUS = 38.1       # 3" / 2
BELT_CENTER_DISTANCE = 734.9     # derived from 72" belt + pulley sizes
PLATEN_LENGTH = 558.8            # 22"
PLATEN_WIDTH = 60.0              # mm, slightly wider than 2" belt
CHAIN_PITCH = 12.7               # 1/2" bicycle chain

# Sprocket pitch radius for a chain sprocket: PD = pitch / sin(pi / N)
def chain_pitch_radius(teeth, pitch=CHAIN_PITCH):
    """Compute sprocket pitch-circle radius for a chain sprocket."""
    return pitch / (2.0 * math.sin(math.pi / teeth))

CHAINRING_R = chain_pitch_radius(42)        # ~85.0 mm
COG_R = chain_pitch_radius(13)              # ~26.5 mm
LARGE_SPROCKET_R = chain_pitch_radius(25)   # ~50.7 mm
PINION_R = chain_pitch_radius(8)            # ~16.6 mm

# Off-axis shaft positions (tentative — Isaiah can move these in the GUI)
INTERMEDIATE_POS = (0.0, 200.0)
CRANK_POS = (0.0, 650.0)


# =====================================================================
# Helpers — add construction geometry to the sketch
# =====================================================================

def add_circle(cx, cy, r):
    """Add a construction circle. Returns the geometry index in the sketch."""
    circle = Part.Circle()
    circle.Center = Vector(cx, cy, 0)
    circle.Radius = r
    return sketch.addGeometry(circle, True)  # True = construction

def add_line(x1, y1, x2, y2):
    """Add a construction line segment. Returns the geometry index."""
    line = Part.LineSegment(Vector(x1, y1, 0), Vector(x2, y2, 0))
    return sketch.addGeometry(line, True)


# =====================================================================
# Idempotent: wipe the sketch's existing geometry before adding
# =====================================================================
# This means re-running the macro replaces the geometry rather than
# stacking duplicates.

while sketch.GeometryCount > 0:
    sketch.delGeometry(0)
App.Console.PrintMessage("Cleared existing sketch geometry.\n")


# =====================================================================
# Build the drivetrain layout
# =====================================================================

# --- Drive pulley shaft (origin) ---
add_circle(0.0, 0.0, DRIVE_PULLEY_RADIUS)
App.Console.PrintMessage(
    f"Added drive pulley circle (R={DRIVE_PULLEY_RADIUS:.1f}mm) at origin.\n"
)

# Co-axial stage-2 pinion (smaller circle at the same shaft)
add_circle(0.0, 0.0, PINION_R)
App.Console.PrintMessage(
    f"Added stage-2 pinion (R={PINION_R:.1f}mm) co-axial with drive pulley.\n"
)


# --- Idler shaft (at -X) ---
idler_x = -BELT_CENTER_DISTANCE
add_circle(idler_x, 0.0, IDLER_PULLEY_RADIUS)
App.Console.PrintMessage(
    f"Added idler pulley circle (R={IDLER_PULLEY_RADIUS:.1f}mm) at "
    f"({idler_x:.1f}, 0).\n"
)


# --- Platen rectangle (between pulleys, centered on belt path) ---
platen_cx = idler_x / 2.0  # midpoint between the two pulley centers
px1 = platen_cx - PLATEN_LENGTH / 2.0
px2 = platen_cx + PLATEN_LENGTH / 2.0
py1 = -PLATEN_WIDTH / 2.0
py2 = PLATEN_WIDTH / 2.0

add_line(px1, py1, px2, py1)  # bottom edge
add_line(px2, py1, px2, py2)  # right edge
add_line(px2, py2, px1, py2)  # top edge
add_line(px1, py2, px1, py1)  # left edge
App.Console.PrintMessage(
    f"Added platen rectangle ({PLATEN_LENGTH:.1f}x{PLATEN_WIDTH:.1f}mm) "
    f"centered at ({platen_cx:.1f}, 0).\n"
)


# --- Intermediate shaft (stage-1 cog + stage-2 large sprocket co-axial) ---
ix, iy = INTERMEDIATE_POS
add_circle(ix, iy, COG_R)
add_circle(ix, iy, LARGE_SPROCKET_R)
App.Console.PrintMessage(
    f"Added stage-1 cog (R={COG_R:.1f}mm) and stage-2 large sprocket "
    f"(R={LARGE_SPROCKET_R:.1f}mm) co-axial at ({ix:.1f}, {iy:.1f}).\n"
)


# --- Crank / BB (chainring) ---
cx, cy = CRANK_POS
add_circle(cx, cy, CHAINRING_R)
App.Console.PrintMessage(
    f"Added chainring (R={CHAINRING_R:.1f}mm) at crank/BB ({cx:.1f}, {cy:.1f}).\n"
)


# =====================================================================
# Recompute and finish
# =====================================================================

sketch.recompute()
doc.recompute()

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 02 complete. MasterSketch now contains:\n"
    "  - Drive pulley + co-axial stage-2 pinion at origin\n"
    "  - Idler pulley at -X (belt center distance from drive)\n"
    "  - Platen rectangle between the pulleys\n"
    "  - Intermediate shaft sprockets (cog + large sprocket co-axial)\n"
    "  - Chainring at crank/BB\n"
    f"  - Total construction elements: {sketch.GeometryCount}\n"
    "Open the sketch in the GUI to inspect.\n"
    "================================================================\n"
)
