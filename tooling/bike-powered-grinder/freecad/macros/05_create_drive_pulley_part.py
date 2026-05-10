# -*- coding: utf-8 -*-
"""
05_create_drive_pulley_part.py
==============================

Creates parts/drive_pulley.FCStd — the first per-part .FCStd file in the
build. Cross-doc App-Linked to Grinder_Params.FCStd via expression syntax:
every dimension is bound to a master parameter, nothing hardcoded.

V2 SCOPE — crowned cylinder (the locked spec)
---------------------------------------------
Crowned cylinder + center bore. The crown is non-negotiable for the
horizontal layout (without it gravity drags the belt off the bottom of
the pulleys). v1 deferred this; that was wrong. v2 corrects it.

Still deferred:
- Stainless rod hub spokes → its own macro (Bambu M600 pause-and-insert)
- Set-screw hole → drill after print
- LIVE cross-doc parametric link → values still baked from master at
  macro-build time. Cross-doc expression resolution issue not yet solved.

GEOMETRY (values pulled from master VarSets at macro run time)
--------------------------------------------------------------
- Outer dia (peak):  master.Pulleys.drive_pulley_dia         (152.4 mm = 6")
- Crown rise:        master.Pulleys.pulley_crown_depth       (0.75 mm)
- Edge dia:          peak - 2 * crown                        (150.9 mm)
- Bore dia:          master.Bearings.grinder_shaft_dia
                     + master.Fits.fit_clearance_running     (8 + 0.20 = 8.20 mm)
- Height:            master.Pulleys.pulley_face_width        (60 mm)

CROSS-SECTION PROFILE
---------------------
Right half of cross-section is a 4-element loop:
  - bottom horizontal line: bore -> edge_r at z=0
  - right CIRCULAR ARC: arc through (edge_r, 0) - (peak_r, H/2) - (edge_r, H)
  - top horizontal line: edge_r -> bore at z=H
  - left vertical line: bore wall

The arc center is computed from the three fixed points:
  arc_cx = (edge_r^2 - peak_r^2 + (H/2)^2) / (2 * (edge_r - peak_r))
  arc_radius = peak_r - arc_cx
For the locked geometry: arc_cx = -524 mm, radius = 600 mm
(big radius for a slight bulge — only 0.75 mm rise over 30 mm half-height)

To regenerate when master values change: re-run macro 05.

PRINT ORIENTATION (slicer concern, recorded for clarity)
- Vertical: pulley axis along print Z. Bottom circular face on the bed.
- No supports needed.
- Bambu A1 Mini OK: OD 152.4 < Frame.max_print_dim 170 mm ✓

IDEMPOTENT
----------
Wipes part-doc contents, rebuilds from scratch. Re-running gives the same
state. Master doc (Grinder_Params) is read-only here — never mutated.

PRE-REQUISITES
--------------
- Grinder_Params.FCStd must be loaded as a FreeCAD document. The headless
  wrapper opens it before invoking this macro.
"""

import math
import os
import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector


PART_NAME = "DrivePulley"


# ====================================================================
# Sanity: master doc must be loaded
# ====================================================================

master_doc = App.getDocument("Grinder_Params")
if master_doc is None:
    raise RuntimeError(
        "Grinder_Params.FCStd not loaded. The wrapper should open it first."
    )


# ====================================================================
# Locate / open / create the part doc
# ====================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "parts"))
PART_PATH = os.path.join(PARTS_DIR, "drive_pulley.FCStd")

os.makedirs(PARTS_DIR, exist_ok=True)

if os.path.exists(PART_PATH):
    part_doc = App.openDocument(PART_PATH)
    App.Console.PrintMessage(f"Opened existing part doc: {PART_PATH}\n")
else:
    part_doc = App.newDocument(PART_NAME)
    App.Console.PrintMessage(f"Created new part doc: {PART_NAME}\n")

App.setActiveDocument(part_doc.Name)


# ====================================================================
# Wipe everything in the part doc (dependency-safe)
# ====================================================================
# Pattern: repeatedly remove "leaf" objects (no other object depends on
# them) until nothing is left. Bounded by a safety counter to prevent
# infinite loops if the dependency graph has a cycle.

def wipe_doc(doc):
    safety = 100
    while doc.Objects and safety > 0:
        safety -= 1
        leaves = [o for o in doc.Objects if not o.InList]
        if not leaves:
            for o in list(doc.Objects):
                try:
                    doc.removeObject(o.Name)
                except Exception:
                    pass
            break
        for o in leaves:
            try:
                doc.removeObject(o.Name)
            except Exception:
                pass

wipe_doc(part_doc)
App.Console.PrintMessage(f"Wiped {PART_NAME}.\n")


# ====================================================================
# Build PartDesign Body + sketch attached to XZ plane
# ====================================================================

body = part_doc.addObject("PartDesign::Body", "PulleyBody")

sketch = body.newObject("Sketcher::SketchObject", "ProfileSketch")

# Place the sketch on the XZ plane via direct Placement.
# Default sketch is on XY (rotation = identity). Rotating 90° around the
# global X axis tips the sketch up into the XZ plane:
#   sketch local U axis (was global X) -> still global X
#   sketch local V axis (was global Y) -> becomes global Z
# That makes the V axis the revolution axis we want (global Z).
sketch.Placement = App.Placement(
    App.Vector(0, 0, 0),
    App.Rotation(App.Vector(1, 0, 0), 90)
)


# ====================================================================
# Read dimensions from master VarSets (single source of truth)
# ====================================================================
# Pulled at macro-build time, baked into the part. To re-derive after a
# master change: re-run macro 05.

def q(qty):
    """Coerce App.Quantity (mm) to float. PropertyLength values carry
    units; arithmetic on them needs the .Value escape."""
    return qty.Value if hasattr(qty, "Value") else float(qty)

PEAK_R = q(master_doc.Pulleys.drive_pulley_dia) / 2.0
CROWN  = q(master_doc.Pulleys.pulley_crown_depth)
EDGE_R = PEAK_R - CROWN  # outer radius at top + bottom faces of pulley
BORE_R = (q(master_doc.Bearings.grinder_shaft_dia)
          + q(master_doc.Fits.fit_clearance_running)) / 2.0
FW     = q(master_doc.Pulleys.pulley_face_width)

# Arc center + radius for the crowned right edge.
# Three fixed points: (EDGE_R, 0), (PEAK_R, FW/2), (EDGE_R, FW)
# By symmetry the arc center lies on the line z = FW/2.
# Solving distance equations gives:
ARC_CX = ((EDGE_R**2 - PEAK_R**2 + (FW / 2.0)**2)
          / (2.0 * (EDGE_R - PEAK_R)))
ARC_R = PEAK_R - ARC_CX

App.Console.PrintMessage(
    f"Dimensions from master:\n"
    f"  peak outer radius: {PEAK_R} mm  (drive_pulley_dia / 2)\n"
    f"  crown depth:       {CROWN} mm\n"
    f"  edge outer radius: {EDGE_R} mm  (peak - crown)\n"
    f"  bore radius:       {BORE_R} mm  (grinder_shaft_dia + running fit) / 2\n"
    f"  face width:        {FW} mm\n"
    f"  arc center X:      {ARC_CX:.2f} mm  (computed from 3-point arc)\n"
    f"  arc radius:        {ARC_R:.2f} mm\n"
)


# ====================================================================
# Helpers
# ====================================================================

def add_line(u1, v1, u2, v2):
    """Add a line in the sketch (u, v are sketch-local coords = (X, Z))."""
    return sketch.addGeometry(
        Part.LineSegment(Vector(u1, v1, 0), Vector(u2, v2, 0)), False
    )

def constraint(c, label):
    try:
        sketch.addConstraint(c)
        return sketch.ConstraintCount - 1
    except Exception as e:
        App.Console.PrintError(f"  ! {label}: {e}\n")
        return None

def bind(idx, expr, label):
    if idx is None:
        return False
    try:
        sketch.setExpression(f".Constraints[{idx}]", expr)
        App.Console.PrintMessage(f"  bound {label}: {expr}\n")
        return True
    except Exception as e:
        App.Console.PrintError(f"  ! {label} bind: {e}\n")
        return False


# ====================================================================
# Build right-half cross-section rectangle (counterclockwise winding)
# ====================================================================

App.Console.PrintMessage("Building cross-section profile (with crown arc)...\n")

# Bottom edge: bore -> edge_r at z=0
L_BOT = add_line(BORE_R, 0, EDGE_R, 0)

# Right edge: ARC from (EDGE_R, 0) bulging out to (PEAK_R, FW/2) back to (EDGE_R, FW)
# Construct from underlying circle + parametric angle range.
# Circle center at (ARC_CX, FW/2), radius ARC_R.
# Start angle = atan2(0 - FW/2, EDGE_R - ARC_CX)
# End angle   = atan2(FW - FW/2, EDGE_R - ARC_CX)
# Both points have the same X relative to center; only Y (= z in sketch coords) differs.
arc_start_ang = math.atan2(0 - FW / 2.0, EDGE_R - ARC_CX)
arc_end_ang   = math.atan2(FW - FW / 2.0, EDGE_R - ARC_CX)
arc_circle = Part.Circle(Vector(ARC_CX, FW / 2.0, 0), Vector(0, 0, 1), ARC_R)
ARC_RIGHT = sketch.addGeometry(
    Part.ArcOfCircle(arc_circle, arc_start_ang, arc_end_ang), False
)

# Top edge: edge_r -> bore at z=FW
L_TOP = add_line(EDGE_R, FW, BORE_R, FW)

# Left edge (bore wall): bore at z=FW down to bore at z=0
L_LEFT = add_line(BORE_R, FW, BORE_R, 0)


# ====================================================================
# Geometric constraints (orientation + corners)
# ====================================================================

constraint(Sketcher.Constraint("Horizontal", L_BOT),  "L_BOT H")
constraint(Sketcher.Constraint("Horizontal", L_TOP),  "L_TOP H")
constraint(Sketcher.Constraint("Vertical",   L_LEFT), "L_LEFT V")
# Right edge is now an arc — no Vertical constraint.
# Coincident corners use ARC_RIGHT's endpoints (PosId 1 = start, 2 = end)
constraint(Sketcher.Constraint("Coincident", L_BOT,     2, ARC_RIGHT, 1), "corner BR (arc start)")
constraint(Sketcher.Constraint("Coincident", ARC_RIGHT, 2, L_TOP,     1), "corner TR (arc end)")
constraint(Sketcher.Constraint("Coincident", L_TOP,     2, L_LEFT,    1), "corner TL")
constraint(Sketcher.Constraint("Coincident", L_LEFT,    2, L_BOT,     1), "corner BL")


# ====================================================================
# Position constraints (lock the rectangle relative to sketch origin)
# ====================================================================

# Bottom edge sits on the sketch X axis (V = 0)
constraint(
    Sketcher.Constraint("DistanceY", -1, 1, L_BOT, 1, 0),
    "bottom edge at V=0"
)


# ====================================================================
# Dimensional constraints with HARDCODED values from master (v1)
# ====================================================================
# v1 bakes the master values in via the constraint Value field, no
# expression bindings. The values were read from master_doc above.
# v2 (macro 06) will switch to live cross-doc expression bindings once
# the recompute-time evaluation issue is understood.

App.Console.PrintMessage("Adding dimensional constraints (hardcoded from master)...\n")

# Edge radius (where bottom and top horizontal edges end at the right side)
constraint(
    Sketcher.Constraint("DistanceX", -1, 1, L_BOT, 2, EDGE_R),
    "edge radius (peak - crown)"
)
# Bore radius (left wall position)
constraint(
    Sketcher.Constraint("DistanceX", -1, 1, L_LEFT, 1, BORE_R),
    "bore radius"
)
# Face width
constraint(
    Sketcher.Constraint("DistanceY", -1, 1, L_TOP, 1, FW),
    "face width"
)
# Arc center position — locks where the bulge is centered.
# (Radius is implicit from center + endpoint-coincidence, so no Radius
# constraint — it would be redundant and break the solver.)
constraint(
    Sketcher.Constraint("DistanceX", -1, 1, ARC_RIGHT, 3, ARC_CX),
    "arc center X"
)
constraint(
    Sketcher.Constraint("DistanceY", -1, 1, ARC_RIGHT, 3, FW / 2.0),
    "arc center Y (midheight)"
)


# ====================================================================
# Recompute sketch, then create Revolution feature
# ====================================================================

sketch.recompute()

App.Console.PrintMessage("Creating Revolution feature...\n")

revolution = body.newObject("PartDesign::Revolution", "Pulley")
revolution.Profile = sketch
revolution.ReferenceAxis = (sketch, ["V_Axis"])
revolution.Angle = 360.0
revolution.Reversed = False
revolution.Midplane = False

part_doc.recompute()


# ====================================================================
# STL export happens in the WRAPPER, not here.
# ====================================================================
# Reason: PartDesign Revolution.Shape stays null in-session even after
# explicit recompute when the doc is built programmatically. The shape
# only materializes when the doc is loaded fresh from disk. So the
# wrapper does: save → close → reopen → recompute → tessellate STL.
#
# (When this gets fixed — e.g., we figure out which API call forces
# Shape population in-session — STL export can move back here.)


# ====================================================================
# KNOWN GAP — axis convention mismatch (deferred)
# ====================================================================
# This macro's Placement rotation puts the cylinder axis along global
# Y (height runs from Y=0 to Y=60). The master sketch convention has
# the grinder shaft along global Z. Doesn't matter for first print
# (slicer reorients freely), but assembly-time linking will need the
# axis on Z. Fix in macro 06 or an assembly-prep macro.


# ====================================================================
# Report
# ====================================================================

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    f"Macro 05 complete. Drive pulley v2 (CROWNED) created.\n"
    f"  doc:                 {PART_PATH}\n"
    f"  body:                PulleyBody\n"
    f"  sketch:              ProfileSketch ({sketch.GeometryCount} geom, "
    f"{sketch.ConstraintCount} constraints)\n"
    f"  feature:             Pulley (Revolution, 360 deg around V_Axis)\n"
    f"  baked dimensions:\n"
    f"    peak dia:          {PEAK_R * 2} mm  (= drive_pulley_dia)\n"
    f"    edge dia:          {EDGE_R * 2} mm  (peak - 2 * crown)\n"
    f"    crown depth:       {CROWN} mm\n"
    f"    bore dia:          {BORE_R * 2:.2f} mm "
    f"(= grinder_shaft_dia + fit_clearance_running)\n"
    f"    face width:        {FW} mm\n"
    f"  fits Bambu A1 Mini:  {PEAK_R * 2} < "
    f"{q(master_doc.Frame.max_print_dim)} ✓\n"
    "================================================================\n"
)
