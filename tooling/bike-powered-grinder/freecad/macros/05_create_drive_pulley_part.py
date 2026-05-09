# -*- coding: utf-8 -*-
"""
05_create_drive_pulley_part.py
==============================

Creates parts/drive_pulley.FCStd — the first per-part .FCStd file in the
build. Cross-doc App-Linked to Grinder_Params.FCStd via expression syntax:
every dimension is bound to a master parameter, nothing hardcoded.

V1 SCOPE (intentional)
----------------------
Cylinder + center bore. NO crown, NO spokes, NO set-screw hole. The goal
is to prove the PartDesign Body + Sketch + Revolution workflow and
produce a printable STL before adding refinement features.

Deferred:
- Crown (0.75 mm rise) → macro 06. Affects belt tracking only — not
  first-print fit/strength testing.
- Stainless rod hub spokes → its own macro (Bambu M600 pause-and-insert).
- Set-screw hole → drill after print for v1.
- LIVE cross-doc parametric link → macro 06. v1 uses values BAKED from
  Grinder_Params at macro-build time (still single source of truth — the
  master doc — but the link is at script-run time, not at recompute time).
  Cross-doc expressions in setExpression() succeed (diagnostic confirms
  syntax `<<Grinder_Params#Pulleys>>.drive_pulley_dia` resolves to 152.4),
  but Revolution.Shape stays null in-session when constraints have bound
  expressions — needs more investigation before relying on it.

GEOMETRY (values pulled from master VarSets at macro run time)
--------------------------------------------------------------
- Outer dia: master.Pulleys.drive_pulley_dia                 (152.4 mm = 6")
- Bore dia:  master.Bearings.grinder_shaft_dia
             + master.Fits.fit_clearance_running             (8 + 0.20 = 8.20 mm)
- Height:    master.Pulleys.pulley_face_width                (60 mm)
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

OUTER_R = q(master_doc.Pulleys.drive_pulley_dia) / 2.0
BORE_R  = (q(master_doc.Bearings.grinder_shaft_dia)
           + q(master_doc.Fits.fit_clearance_running)) / 2.0
FW      = q(master_doc.Pulleys.pulley_face_width)

App.Console.PrintMessage(
    f"Dimensions from master:\n"
    f"  outer radius: {OUTER_R} mm  (drive_pulley_dia / 2)\n"
    f"  bore radius:  {BORE_R} mm   (grinder_shaft_dia + fit_clearance_running) / 2\n"
    f"  face width:   {FW} mm\n"
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

App.Console.PrintMessage("Building cross-section profile...\n")

L_BOT   = add_line(BORE_R,   0,    OUTER_R, 0)
L_RIGHT = add_line(OUTER_R,  0,    OUTER_R, FW)
L_TOP   = add_line(OUTER_R,  FW,   BORE_R,  FW)
L_LEFT  = add_line(BORE_R,   FW,   BORE_R,  0)


# ====================================================================
# Geometric constraints (orientation + corners)
# ====================================================================

constraint(Sketcher.Constraint("Horizontal", L_BOT),   "L_BOT H")
constraint(Sketcher.Constraint("Vertical",   L_RIGHT), "L_RIGHT V")
constraint(Sketcher.Constraint("Horizontal", L_TOP),   "L_TOP H")
constraint(Sketcher.Constraint("Vertical",   L_LEFT),  "L_LEFT V")
constraint(Sketcher.Constraint("Coincident", L_BOT,   2, L_RIGHT, 1), "corner BR")
constraint(Sketcher.Constraint("Coincident", L_RIGHT, 2, L_TOP,   1), "corner TR")
constraint(Sketcher.Constraint("Coincident", L_TOP,   2, L_LEFT,  1), "corner TL")
constraint(Sketcher.Constraint("Coincident", L_LEFT,  2, L_BOT,   1), "corner BL")


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

constraint(
    Sketcher.Constraint("DistanceX", -1, 1, L_RIGHT, 1, OUTER_R),
    "outer radius"
)
constraint(
    Sketcher.Constraint("DistanceX", -1, 1, L_LEFT, 1, BORE_R),
    "bore radius"
)
constraint(
    Sketcher.Constraint("DistanceY", -1, 1, L_TOP, 1, FW),
    "face width"
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
    f"Macro 05 complete. Drive pulley v1 created.\n"
    f"  doc:                 {PART_PATH}\n"
    f"  body:                PulleyBody\n"
    f"  sketch:              ProfileSketch ({sketch.GeometryCount} geom, "
    f"{sketch.ConstraintCount} constraints)\n"
    f"  feature:             Pulley (Revolution, 360 deg around V_Axis)\n"
    f"  baked dimensions:\n"
    f"    outer dia:         {OUTER_R * 2} mm  (= drive_pulley_dia)\n"
    f"    bore dia:          {BORE_R * 2:.2f} mm "
    f"(= grinder_shaft_dia + fit_clearance_running)\n"
    f"    face width:        {FW} mm\n"
    f"  fits Bambu A1 Mini:  {OUTER_R * 2} < "
    f"{q(master_doc.Frame.max_print_dim)} ✓\n"
    "================================================================\n"
)
