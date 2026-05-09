# -*- coding: utf-8 -*-
"""
03_bind_geometry_to_varsets.py
==============================

Rebuilds the MasterSketch with full parametric bindings — every shape's
size and (where applicable) position is tied to a VarSet expression.
Change a value in the Drivetrain / Pulleys / Belt / Platen VarSet, and
the geometry recomputes automatically.

WHAT THIS DOES vs MACRO 02
==========================
Macro 02 added geometry with hardcoded values; the circles and lines
were free to drift if Sketcher's solver moved them.

Macro 03 wipes everything and rebuilds with constraints + expressions:
- Drive pulley center fixed to the origin (Coincident constraint)
- Drive pulley diameter bound to <<Pulleys>>.drive_pulley_dia
- Stage-2 pinion co-axial with drive pulley, diameter from chain-pitch formula
- Idler locked to the X axis with DistanceX = -<<Belt>>.belt_path_center_distance
- Idler diameter bound to <<Pulleys>>.idler_pulley_dia
- Platen rectangle: 4 corners coincident, length and width bound to VarSets
- Stage-1 cog and stage-2 large sprocket co-axial; diameters from chain-pitch
- Chainring diameter from chain-pitch formula

After this runs, changing e.g. <<Pulleys>>.drive_pulley_dia from 152.4 to
180 should make the drive pulley circle visibly larger on next recompute.

PRE-REQUISITES
==============
- Grinder_Params.FCStd is the active document (or run via headless wrapper)
- A sketch named "MasterSketch" exists in the document

IDEMPOTENT
==========
Wipes both geometry AND constraints before rebuilding. Re-running gives
the same result every time.

KNOWN GAPS (deferred to future macros)
=======================================
- Intermediate-shaft and crank/BB positions remain unconstrained — they're
  placeholders Isaiah moves interactively. Future macro can constrain those
  once chain-center-distance values are locked.
- Each circle's center isn't shown as a separate "point" feature; we rely
  on Sketcher's built-in center vertex (PosId=3) for coincidence work.
"""

import math
import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector


# =====================================================================
# Sanity-check: doc + sketch exist
# =====================================================================

doc = App.ActiveDocument
if doc is None:
    raise RuntimeError("No active document. Open Grinder_Params.FCStd first.")

sketch = doc.getObject("MasterSketch")
if sketch is None:
    raise RuntimeError(
        "MasterSketch not found. Run macro 01 first to create it."
    )


# =====================================================================
# Initial values (for geometry creation; bindings override after)
# =====================================================================
# Pitch radius for chain sprockets: r = pitch / (2 * sin(pi / N))

CHAIN_PITCH = 12.7  # mm (1/2" bicycle chain)

def chain_pitch_radius(teeth, pitch=CHAIN_PITCH):
    return pitch / (2.0 * math.sin(math.pi / teeth))

DRIVE_R = 76.2          # 6" / 2
IDLER_R = 38.1          # 3" / 2
BELT_CENTER = 734.9     # mm — drive-to-idler center distance
PLATEN_LEN = 558.8      # 22"
PLATEN_W = 60.0
PINION_R = chain_pitch_radius(8)        # ~16.59
COG_R = chain_pitch_radius(13)          # ~26.50
LARGE_R = chain_pitch_radius(25)        # ~50.71
CHAINRING_R = chain_pitch_radius(42)    # ~84.99

# Tentative shaft positions (left unconstrained — Isaiah moves them in GUI)
INT_X, INT_Y = 0.0, 200.0
CRANK_X, CRANK_Y = 0.0, 650.0


# =====================================================================
# Wipe everything for idempotency
# =====================================================================

while sketch.ConstraintCount > 0:
    sketch.delConstraint(0)
while sketch.GeometryCount > 0:
    sketch.delGeometry(0)
App.Console.PrintMessage("Cleared sketch geometry and constraints.\n")


# =====================================================================
# Helpers
# =====================================================================

def add_circle(cx, cy, r):
    return sketch.addGeometry(
        Part.Circle(Vector(cx, cy, 0), Vector(0, 0, 1), r), True
    )

def add_line(x1, y1, x2, y2):
    return sketch.addGeometry(
        Part.LineSegment(Vector(x1, y1, 0), Vector(x2, y2, 0)), True
    )

def add_constraint_safe(constraint, label):
    """Add a constraint and return its index. Catches errors and prints them."""
    try:
        sketch.addConstraint(constraint)
        idx = sketch.ConstraintCount - 1
        return idx
    except Exception as e:
        App.Console.PrintError(f"  ! {label}: failed to add constraint: {e}\n")
        return None

def bind_expression(constraint_idx, expr, label):
    """Bind an expression to a constraint. Returns True on success."""
    if constraint_idx is None:
        return False
    try:
        sketch.setExpression(f".Constraints[{constraint_idx}]", expr)
        App.Console.PrintMessage(f"  bound {label}: {expr}\n")
        return True
    except Exception as e:
        App.Console.PrintError(f"  ! {label}: failed to bind expression: {e}\n")
        return False


# =====================================================================
# Build geometry (record indexes for constraint targeting)
# =====================================================================

App.Console.PrintMessage("Building geometry...\n")

DRIVE_IDX = add_circle(0.0, 0.0, DRIVE_R)
PINION_IDX = add_circle(0.0, 0.0, PINION_R)
IDLER_IDX = add_circle(-BELT_CENTER, 0.0, IDLER_R)

# Platen rectangle (4 lines, ordered: bottom, right, top, left)
px1 = -BELT_CENTER / 2 - PLATEN_LEN / 2
px2 = -BELT_CENTER / 2 + PLATEN_LEN / 2
py1 = -PLATEN_W / 2
py2 = PLATEN_W / 2

PL_BOT = add_line(px1, py1, px2, py1)
PL_RIGHT = add_line(px2, py1, px2, py2)
PL_TOP = add_line(px2, py2, px1, py2)
PL_LEFT = add_line(px1, py2, px1, py1)

COG_IDX = add_circle(INT_X, INT_Y, COG_R)
LARGE_IDX = add_circle(INT_X, INT_Y, LARGE_R)
CHAINRING_IDX = add_circle(CRANK_X, CRANK_Y, CHAINRING_R)

App.Console.PrintMessage(f"  geometry indexes: drive={DRIVE_IDX}, pinion={PINION_IDX}, "
                         f"idler={IDLER_IDX}, platen=[{PL_BOT},{PL_RIGHT},{PL_TOP},{PL_LEFT}], "
                         f"cog={COG_IDX}, large={LARGE_IDX}, chainring={CHAINRING_IDX}\n")


# =====================================================================
# Constraints + bindings
# =====================================================================
# Sketcher origin reference: GeoId = -1, PosId = 1 (root point)
# Circle vertex codes: PosId = 3 is the center
# Line vertex codes:   PosId = 1 is the start, 2 is the end

App.Console.PrintMessage("Adding constraints...\n")


# --- Drive pulley: center to origin, diameter bound ---
add_constraint_safe(
    Sketcher.Constraint("Coincident", DRIVE_IDX, 3, -1, 1),
    "drive pulley center to origin"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", DRIVE_IDX, DRIVE_R * 2),
    "drive pulley diameter"
)
bind_expression(idx, "<<Pulleys>>.drive_pulley_dia", "drive_pulley_dia")


# --- Stage-2 pinion: co-axial with drive pulley, diameter from chain-pitch ---
add_constraint_safe(
    Sketcher.Constraint("Coincident", PINION_IDX, 3, DRIVE_IDX, 3),
    "stage-2 pinion co-axial with drive pulley"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", PINION_IDX, PINION_R * 2),
    "stage-2 pinion diameter"
)
bind_expression(
    idx,
    "<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage2_pinion_teeth)",
    "stage2_pinion diameter (chain-pitch formula)"
)


# --- Idler: on X axis at -BELT_CENTER, diameter bound ---
add_constraint_safe(
    Sketcher.Constraint("DistanceY", -1, 1, IDLER_IDX, 3, 0),
    "idler Y = 0 (locked on X axis)"
)
idx = add_constraint_safe(
    Sketcher.Constraint("DistanceX", -1, 1, IDLER_IDX, 3, -BELT_CENTER),
    "idler X = -belt_path_center_distance"
)
bind_expression(
    idx, "-<<Belt>>.belt_path_center_distance", "idler X position"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", IDLER_IDX, IDLER_R * 2),
    "idler diameter"
)
bind_expression(idx, "<<Pulleys>>.idler_pulley_dia", "idler_pulley_dia")


# --- Platen rectangle: H/V orientations + corner coincidences + length/width ---
add_constraint_safe(
    Sketcher.Constraint("Horizontal", PL_BOT), "platen bottom horizontal"
)
add_constraint_safe(
    Sketcher.Constraint("Vertical", PL_RIGHT), "platen right vertical"
)
add_constraint_safe(
    Sketcher.Constraint("Horizontal", PL_TOP), "platen top horizontal"
)
add_constraint_safe(
    Sketcher.Constraint("Vertical", PL_LEFT), "platen left vertical"
)
# Corner coincidences (close the rectangle)
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_BOT, 2, PL_RIGHT, 1),
    "platen bottom.end = right.start"
)
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_RIGHT, 2, PL_TOP, 1),
    "platen right.end = top.start"
)
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_TOP, 2, PL_LEFT, 1),
    "platen top.end = left.start"
)
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_LEFT, 2, PL_BOT, 1),
    "platen left.end = bottom.start"
)
# Length and width
idx = add_constraint_safe(
    Sketcher.Constraint("Distance", PL_BOT, PLATEN_LEN),
    "platen length"
)
bind_expression(idx, "<<Platen>>.platen_length", "platen_length")
idx = add_constraint_safe(
    Sketcher.Constraint("Distance", PL_RIGHT, PLATEN_W),
    "platen width"
)
bind_expression(idx, "<<Platen>>.platen_width", "platen_width")


# --- Stage-1 cog + stage-2 large sprocket co-axial at intermediate shaft ---
add_constraint_safe(
    Sketcher.Constraint("Coincident", LARGE_IDX, 3, COG_IDX, 3),
    "large sprocket co-axial with cog"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", COG_IDX, COG_R * 2),
    "stage-1 cog diameter"
)
bind_expression(
    idx,
    "<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage1_cog_teeth)",
    "stage1_cog diameter (chain-pitch formula)"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", LARGE_IDX, LARGE_R * 2),
    "stage-2 large sprocket diameter"
)
bind_expression(
    idx,
    "<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage2_large_teeth)",
    "stage2_large diameter (chain-pitch formula)"
)


# --- Chainring at crank/BB ---
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", CHAINRING_IDX, CHAINRING_R * 2),
    "chainring diameter"
)
bind_expression(
    idx,
    "<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage1_chainring_teeth)",
    "stage1_chainring diameter (chain-pitch formula)"
)


# =====================================================================
# Recompute and report
# =====================================================================

sketch.recompute()
doc.recompute()

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 03 complete. MasterSketch is now fully parametric:\n"
    f"  geometry elements: {sketch.GeometryCount}\n"
    f"  constraints:       {sketch.ConstraintCount}\n"
    "Try changing a value in any VarSet (e.g. Pulleys.drive_pulley_dia\n"
    "from 152.4 to 180) and watch the geometry recompute.\n"
    "Intermediate-shaft and crank/BB positions are still unconstrained\n"
    "placeholders — drag them in Sketcher to set their physical positions.\n"
    "================================================================\n"
)
