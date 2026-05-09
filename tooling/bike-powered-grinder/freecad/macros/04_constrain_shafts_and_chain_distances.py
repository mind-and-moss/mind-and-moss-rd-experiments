# -*- coding: utf-8 -*-
"""
04_constrain_shafts_and_chain_distances.py
==========================================

Locks the intermediate shaft and crank/BB shaft positions in MasterSketch
via DistanceX/DistanceY constraints bound to four new Drivetrain VarSet
properties. Also adds two computed VarSet properties for stage-1 and
stage-2 chain center distances (expression-bound, auto-update).

DEFAULTS (Path B from Session 7 — "Claude picks reasonable bike geometry")
-------------------------------------------------------------------------
  intermediate_shaft = (0, 500)  mm  — straight back from grinder shaft, ~20"
  crank_bb           = (0, 1100) mm  — 600 mm further back (chainstay-equiv)

Resulting chain center distances:
  stage 2 (intermediate -> grinder) = 500 mm
  stage 1 (crank        -> intermediate) = 600 mm

Both are inside the 380-635 mm sweet spot (30-50 chain pitches) and well
clear of sum-of-radii minimums (67.3 and 111.5 mm).

Total grinder-shaft to crank-shaft = 1100 mm = 43" linear. Combined with
~900 mm of grinder module (drive pulley to idler + structure) and ~400 mm
behind the crank for saddle, total machine length ~7.9 ft. Matches the
Q4-locked "~7 feet" estimate.

THIS MACRO SUPERSEDES MACRO 03
==============================
Like macro 03 wiped + rebuilt macro 02's geometry, macro 04 wipes both
geometry AND constraints and rebuilds the COMPLETE state — macro 03's
bindings PLUS the new shaft constraints. Re-running macro 03 alone after
this would undo macro 04's additions.

IDEMPOTENT
==========
- VarSet properties added only if missing (preserves any later edits)
- VarSet expressions re-bound every run (cheap and safe)
- Sketch geometry + constraints wiped and rebuilt fully each run
"""

import math
import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector


# ====================================================================
# Sanity
# ====================================================================
doc = App.ActiveDocument
if doc is None:
    raise RuntimeError("No active document. Open Grinder_Params.FCStd first.")

drivetrain = doc.getObject("Drivetrain")
sketch = doc.getObject("MasterSketch")
if drivetrain is None:
    raise RuntimeError("Drivetrain VarSet missing. Run macro 01 first.")
if sketch is None:
    raise RuntimeError("MasterSketch missing. Run macro 01 first.")


# ====================================================================
# Add new VarSet properties (data only)
# ====================================================================

DEFAULTS = {
    "intermediate_shaft_x": 0.0,
    "intermediate_shaft_y": 500.0,
    "crank_bb_x":           0.0,
    "crank_bb_y":           1100.0,
}


def add_property_if_missing(varset, prop_name, prop_type, group, doc_str,
                            default_value=None):
    """Add a property only if it doesn't already exist. Returns True if new."""
    if prop_name in varset.PropertiesList:
        App.Console.PrintMessage(f"  property exists: {prop_name}\n")
        return False
    full_type = "App::Property" + prop_type
    varset.addProperty(full_type, prop_name, group, doc_str)
    if default_value is not None:
        setattr(varset, prop_name, default_value)
    App.Console.PrintMessage(
        f"  property added:  {prop_name} = {default_value}\n"
    )
    return True


App.Console.PrintMessage("Adding shaft position properties...\n")

add_property_if_missing(
    drivetrain, "intermediate_shaft_x", "Length", "Drivetrain",
    "Intermediate shaft center X coordinate in MasterSketch (mm). "
    "Default 0 (on Y axis behind grinder shaft).",
    DEFAULTS["intermediate_shaft_x"]
)
add_property_if_missing(
    drivetrain, "intermediate_shaft_y", "Length", "Drivetrain",
    "Intermediate shaft center Y coordinate in MasterSketch (mm). "
    "Default 500 (~20 inches back from grinder shaft).",
    DEFAULTS["intermediate_shaft_y"]
)
add_property_if_missing(
    drivetrain, "crank_bb_x", "Length", "Drivetrain",
    "Crank/BB shaft center X coordinate in MasterSketch (mm). "
    "Default 0 (on Y axis).",
    DEFAULTS["crank_bb_x"]
)
add_property_if_missing(
    drivetrain, "crank_bb_y", "Length", "Drivetrain",
    "Crank/BB shaft center Y coordinate in MasterSketch (mm). "
    "Default 1100 (600 mm behind intermediate shaft).",
    DEFAULTS["crank_bb_y"]
)

App.Console.PrintMessage("Adding computed chain center distance properties...\n")

add_property_if_missing(
    drivetrain, "stage1_chain_center_distance", "Length", "Drivetrain",
    "Stage 1 chain center distance (crank to intermediate). "
    "COMPUTED from crank_bb_* and intermediate_shaft_* via expression."
)
add_property_if_missing(
    drivetrain, "stage2_chain_center_distance", "Length", "Drivetrain",
    "Stage 2 chain center distance (intermediate to grinder shaft at origin). "
    "COMPUTED from intermediate_shaft_* via expression."
)

# Bind expressions every run (idempotent — reassigns to same expression).
# Note: FreeCAD expression engine supports `^` for exponentiation (different
# from Python's XOR). sqrt() is built in. Units propagate: mm * mm = mm²,
# sum of mm² is mm², sqrt(mm²) = mm — clean for a Length property.
drivetrain.setExpression(
    "stage1_chain_center_distance",
    "sqrt((<<Drivetrain>>.crank_bb_x - <<Drivetrain>>.intermediate_shaft_x) ^ 2 "
    "+ (<<Drivetrain>>.crank_bb_y - <<Drivetrain>>.intermediate_shaft_y) ^ 2)"
)
drivetrain.setExpression(
    "stage2_chain_center_distance",
    "sqrt(<<Drivetrain>>.intermediate_shaft_x ^ 2 "
    "+ <<Drivetrain>>.intermediate_shaft_y ^ 2)"
)


# ====================================================================
# Read shaft position values (so initial geometry sits where we want it)
# ====================================================================

def q_to_mm(qty):
    """Coerce App.Quantity (mm) to plain float in mm."""
    return qty.Value if hasattr(qty, "Value") else float(qty)

INT_X = q_to_mm(drivetrain.intermediate_shaft_x)
INT_Y = q_to_mm(drivetrain.intermediate_shaft_y)
CRANK_X = q_to_mm(drivetrain.crank_bb_x)
CRANK_Y = q_to_mm(drivetrain.crank_bb_y)


# ====================================================================
# Initial geometry constants (same as macro 03)
# ====================================================================

CHAIN_PITCH = 12.7

def chain_pitch_radius(teeth, pitch=CHAIN_PITCH):
    return pitch / (2.0 * math.sin(math.pi / teeth))

DRIVE_R = 76.2
IDLER_R = 38.1
BELT_CENTER = 734.9
PLATEN_LEN = 558.8
PLATEN_W = 60.0
PINION_R = chain_pitch_radius(8)
COG_R = chain_pitch_radius(13)
LARGE_R = chain_pitch_radius(25)
CHAINRING_R = chain_pitch_radius(42)


# ====================================================================
# Wipe sketch (constraints first, then geometry)
# ====================================================================

while sketch.ConstraintCount > 0:
    sketch.delConstraint(0)
while sketch.GeometryCount > 0:
    sketch.delGeometry(0)
App.Console.PrintMessage("Cleared sketch geometry and constraints.\n")


# ====================================================================
# Helpers
# ====================================================================

def add_circle(cx, cy, r):
    return sketch.addGeometry(
        Part.Circle(Vector(cx, cy, 0), Vector(0, 0, 1), r), True
    )

def add_line(x1, y1, x2, y2):
    return sketch.addGeometry(
        Part.LineSegment(Vector(x1, y1, 0), Vector(x2, y2, 0)), True
    )

def add_constraint_safe(constraint, label):
    try:
        sketch.addConstraint(constraint)
        return sketch.ConstraintCount - 1
    except Exception as e:
        App.Console.PrintError(f"  ! {label}: {e}\n")
        return None

def bind_expression(constraint_idx, expr, label):
    if constraint_idx is None:
        return False
    try:
        sketch.setExpression(f".Constraints[{constraint_idx}]", expr)
        App.Console.PrintMessage(f"  bound {label}: {expr}\n")
        return True
    except Exception as e:
        App.Console.PrintError(f"  ! {label}: failed to bind expression: {e}\n")
        return False


# ====================================================================
# Build geometry
# ====================================================================

App.Console.PrintMessage("Building geometry...\n")

DRIVE_IDX = add_circle(0.0, 0.0, DRIVE_R)
PINION_IDX = add_circle(0.0, 0.0, PINION_R)
IDLER_IDX = add_circle(-BELT_CENTER, 0.0, IDLER_R)

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


# ====================================================================
# Constraints + bindings (macro 03 baseline)
# ====================================================================
# Sketcher origin reference: GeoId = -1, PosId = 1 (root point)
# Circle vertex codes: PosId = 3 is the center
# Line vertex codes:   PosId = 1 = start, 2 = end

App.Console.PrintMessage("Adding constraints (macro 03 baseline)...\n")

# Drive pulley
add_constraint_safe(
    Sketcher.Constraint("Coincident", DRIVE_IDX, 3, -1, 1),
    "drive pulley center to origin"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", DRIVE_IDX, DRIVE_R * 2),
    "drive pulley diameter"
)
bind_expression(idx, "<<Pulleys>>.drive_pulley_dia", "drive_pulley_dia")

# Stage-2 pinion (co-axial with drive pulley)
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
    "stage2_pinion diameter"
)

# Idler
add_constraint_safe(
    Sketcher.Constraint("DistanceY", -1, 1, IDLER_IDX, 3, 0),
    "idler Y = 0"
)
idx = add_constraint_safe(
    Sketcher.Constraint("DistanceX", -1, 1, IDLER_IDX, 3, -BELT_CENTER),
    "idler X = -belt_center"
)
bind_expression(idx, "-<<Belt>>.belt_path_center_distance", "idler X")
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", IDLER_IDX, IDLER_R * 2),
    "idler diameter"
)
bind_expression(idx, "<<Pulleys>>.idler_pulley_dia", "idler_pulley_dia")

# Platen
add_constraint_safe(Sketcher.Constraint("Horizontal", PL_BOT), "PL bottom H")
add_constraint_safe(Sketcher.Constraint("Vertical", PL_RIGHT), "PL right V")
add_constraint_safe(Sketcher.Constraint("Horizontal", PL_TOP), "PL top H")
add_constraint_safe(Sketcher.Constraint("Vertical", PL_LEFT), "PL left V")
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_BOT, 2, PL_RIGHT, 1), "PL corner 1"
)
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_RIGHT, 2, PL_TOP, 1), "PL corner 2"
)
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_TOP, 2, PL_LEFT, 1), "PL corner 3"
)
add_constraint_safe(
    Sketcher.Constraint("Coincident", PL_LEFT, 2, PL_BOT, 1), "PL corner 4"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Distance", PL_BOT, PLATEN_LEN), "platen length"
)
bind_expression(idx, "<<Platen>>.platen_length", "platen_length")
idx = add_constraint_safe(
    Sketcher.Constraint("Distance", PL_RIGHT, PLATEN_W), "platen width"
)
bind_expression(idx, "<<Platen>>.platen_width", "platen_width")

# Stage-1 cog + stage-2 large sprocket co-axial at intermediate shaft
add_constraint_safe(
    Sketcher.Constraint("Coincident", LARGE_IDX, 3, COG_IDX, 3),
    "large sprocket co-axial with cog"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", COG_IDX, COG_R * 2), "stage-1 cog dia"
)
bind_expression(
    idx,
    "<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage1_cog_teeth)",
    "stage1_cog diameter"
)
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", LARGE_IDX, LARGE_R * 2), "stage-2 large dia"
)
bind_expression(
    idx,
    "<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage2_large_teeth)",
    "stage2_large diameter"
)

# Chainring at crank/BB
idx = add_constraint_safe(
    Sketcher.Constraint("Diameter", CHAINRING_IDX, CHAINRING_R * 2),
    "chainring diameter"
)
bind_expression(
    idx,
    "<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage1_chainring_teeth)",
    "stage1_chainring diameter"
)


# ====================================================================
# NEW IN MACRO 04 — shaft position constraints
# ====================================================================
# Lock the intermediate shaft and crank/BB centers to the VarSet values.
# The cog circle's center IS the intermediate shaft (the large-sprocket
# circle follows via the Coincident-with-cog constraint already in place).
# The chainring circle's center IS the crank/BB.

App.Console.PrintMessage("Adding shaft position constraints (NEW in macro 04)...\n")

# Intermediate shaft X
idx = add_constraint_safe(
    Sketcher.Constraint("DistanceX", -1, 1, COG_IDX, 3, INT_X),
    "intermediate shaft X"
)
bind_expression(idx, "<<Drivetrain>>.intermediate_shaft_x",
                "intermediate_shaft_x")

# Intermediate shaft Y
idx = add_constraint_safe(
    Sketcher.Constraint("DistanceY", -1, 1, COG_IDX, 3, INT_Y),
    "intermediate shaft Y"
)
bind_expression(idx, "<<Drivetrain>>.intermediate_shaft_y",
                "intermediate_shaft_y")

# Crank/BB X
idx = add_constraint_safe(
    Sketcher.Constraint("DistanceX", -1, 1, CHAINRING_IDX, 3, CRANK_X),
    "crank/BB X"
)
bind_expression(idx, "<<Drivetrain>>.crank_bb_x", "crank_bb_x")

# Crank/BB Y
idx = add_constraint_safe(
    Sketcher.Constraint("DistanceY", -1, 1, CHAINRING_IDX, 3, CRANK_Y),
    "crank/BB Y"
)
bind_expression(idx, "<<Drivetrain>>.crank_bb_y", "crank_bb_y")


# ====================================================================
# Recompute and report
# ====================================================================

sketch.recompute()
doc.recompute()

cd1 = drivetrain.stage1_chain_center_distance
cd2 = drivetrain.stage2_chain_center_distance

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 04 complete. Sketch fully constrained.\n"
    f"  geometry elements: {sketch.GeometryCount}\n"
    f"  constraints:       {sketch.ConstraintCount}\n"
    f"  intermediate shaft = ({INT_X}, {INT_Y}) mm\n"
    f"  crank/BB           = ({CRANK_X}, {CRANK_Y}) mm\n"
    f"  stage 1 chain CD   = {cd1}\n"
    f"  stage 2 chain CD   = {cd2}\n"
    "Edit <<Drivetrain>>.intermediate_shaft_x/y or .crank_bb_x/y in the\n"
    "VarSet and the geometry + chain center distances reflow automatically.\n"
    "================================================================\n"
)
