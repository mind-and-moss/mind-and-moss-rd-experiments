# -*- coding: utf-8 -*-
"""
06_create_drivetrain_placeholders.py
====================================

Creates the remaining drivetrain part .FCStd files as PLACEHOLDERS:
- idler_pulley.FCStd       3" crowned PETG (no crown yet, just cylinder)
- stage2_pinion.FCStd      8T machined-metal pinion (no teeth, just disk)
- stage2_large.FCStd       25T PETG sprocket (no teeth, just disk)
- stage1_cog.FCStd         13T donor steel cog (no teeth, just disk)
- chainring.FCStd          42T donor steel chainring (no teeth)
- intermediate_shaft.FCStd 12 mm stainless rod
- grinder_shaft.FCStd      8 mm stainless rod

V1 SCOPE: each is a solid of revolution (cylinder ± center bore). NO
gear teeth, NO keyways, NO set-screw holes. Goal is to get every drive-
train element represented in the parts/ folder so an assembly file can
be built and visualized. Refinement comes later (sprocket teeth via the
PartDesign Gear workbench or external macros).

For shafts (donor or stock steel rod, won't be 3D printed):
the .FCStd is for assembly representation, not for printing.

For sprockets/cog/chainring (also stock steel parts on this build):
same — these are donor parts harvested from the bike. .FCStd is for
clearance checks during assembly modeling.

SHARED PATTERN
--------------
Each part is a PartDesign Body + Sketch on XZ plane + Revolution about
the V_Axis. Profile is a rectangle (right half of cross-section).
Solid shafts use bore_dia=0 (just a filled rectangle from origin).

DIMENSIONS sourced from master Grinder_Params.FCStd at macro-build time
(same convention as macro 05 — hardcoded values, master is source of
truth for next regeneration).
"""

import os
import math
import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "parts"))

os.makedirs(PARTS_DIR, exist_ok=True)


# ====================================================================
# Read master values
# ====================================================================

master_doc = App.getDocument("Grinder_Params")
if master_doc is None:
    raise RuntimeError("Grinder_Params not loaded. Wrapper must open it first.")


def q(qty):
    return qty.Value if hasattr(qty, "Value") else float(qty)


CHAIN_PITCH = q(master_doc.Drivetrain.chain_pitch)
RUNNING_FIT = q(master_doc.Fits.fit_clearance_running)
INT_SHAFT_DIA = q(master_doc.Bearings.intermediate_shaft_dia)
GRINDER_SHAFT_DIA = q(master_doc.Bearings.grinder_shaft_dia)
IDLER_DIA = q(master_doc.Pulleys.idler_pulley_dia)
PULLEY_FACE = q(master_doc.Pulleys.pulley_face_width)


def chain_pitch_dia(teeth):
    """Chain sprocket pitch diameter from tooth count and chain pitch."""
    return CHAIN_PITCH / math.sin(math.pi / teeth)


# ====================================================================
# Part configurations
# ====================================================================
# Each tuple: (filename, body_name, outer_dia, bore_dia, height, comment)
# bore_dia=0 means solid cylinder (shafts).
#
# Sprocket OD = pitch_diameter (where chain rollers ride). Real sprockets
# have addendum-extended teeth above this, but for placeholder cylinders
# we use the pitch dia as the OD — gives accurate chain-engagement
# clearance for assembly modeling.

CHAINRING_TEETH = 42
COG_TEETH = 13
LARGE_TEETH = 25
PINION_TEETH = 8

CROWN = q(master_doc.Pulleys.pulley_crown_depth)  # 0.75 mm — non-negotiable for horizontal layout

# Each tuple: (name, body_name, OD, bore, height, crown_depth, comment)
# crown_depth > 0  -> crowned pulley (right edge is an arc bulging out)
# crown_depth == 0 -> straight cylinder (sprockets, shafts)
PARTS = [
    ("idler_pulley", "IdlerBody",
        IDLER_DIA, GRINDER_SHAFT_DIA + RUNNING_FIT, PULLEY_FACE, CROWN,
        "3in CROWNED idler pulley (matches drive pulley belt-tracking)"),

    ("stage2_pinion", "PinionBody",
        chain_pitch_dia(PINION_TEETH), GRINDER_SHAFT_DIA + RUNNING_FIT, 16.0, 0.0,
        "8T machined metal pinion on grinder shaft (placeholder disk)"),

    ("stage2_large", "LargeSprocketBody",
        chain_pitch_dia(LARGE_TEETH), INT_SHAFT_DIA + RUNNING_FIT, 12.0, 0.0,
        "25T PETG large sprocket on intermediate shaft (placeholder)"),

    ("stage1_cog", "CogBody",
        chain_pitch_dia(COG_TEETH), INT_SHAFT_DIA + RUNNING_FIT, 5.0, 0.0,
        "13T donor steel cog on intermediate shaft (placeholder)"),

    ("chainring", "ChainringBody",
        chain_pitch_dia(CHAINRING_TEETH), 16.0, 5.0, 0.0,
        "42T donor steel chainring on crank/BB (placeholder; bore=BB axle)"),

    ("intermediate_shaft", "ShaftBody",
        INT_SHAFT_DIA, 0.0, 150.0, 0.0,
        "12mm 304 stainless rod, ~150mm length (donor stock)"),

    ("grinder_shaft", "ShaftBody",
        GRINDER_SHAFT_DIA, 0.0, 150.0, 0.0,
        "8mm 304 stainless rod, ~150mm length (donor stock)"),
]

App.Console.PrintMessage(
    f"Will create {len(PARTS)} parts in {PARTS_DIR}\n"
)


# ====================================================================
# Helper: create or open a part doc, wipe it, build a hollow cylinder,
# save and close.
# ====================================================================

def wipe_doc(doc):
    safety = 100
    while doc.Objects and safety > 0:
        safety -= 1
        leaves = [o for o in doc.Objects if not o.InList]
        if not leaves:
            for o in list(doc.Objects):
                try: doc.removeObject(o.Name)
                except Exception: pass
            break
        for o in leaves:
            try: doc.removeObject(o.Name)
            except Exception: pass


def build_hollow_cylinder(part_name, body_name, outer_dia, bore_dia, height,
                          crown_depth=0.0):
    """Create or refresh parts/<part_name>.FCStd containing a (possibly
    crowned) hollow cylinder (or solid if bore_dia <= 0). If crown_depth
    > 0, the right edge of the cross-section becomes a circular arc
    bulging outward from edge_r to peak_r at midheight (locked-spec
    crowned pulley). Returns the saved file path."""
    part_path = os.path.join(PARTS_DIR, f"{part_name}.FCStd")

    # Open or create
    if os.path.exists(part_path):
        part_doc = App.openDocument(part_path)
    else:
        part_doc = App.newDocument(part_name)

    App.setActiveDocument(part_doc.Name)
    wipe_doc(part_doc)

    body = part_doc.addObject("PartDesign::Body", body_name)
    sketch = body.newObject("Sketcher::SketchObject", "ProfileSketch")

    # Sketch on XZ plane (V_Axis becomes global Y for revolution — same
    # quirk as macro 05; axis-convention fix is a follow-up).
    sketch.Placement = App.Placement(
        App.Vector(0, 0, 0),
        App.Rotation(App.Vector(1, 0, 0), 90)
    )

    peak_r = outer_dia / 2.0
    bore_r = bore_dia / 2.0 if bore_dia > 0 else 0.0
    inner_x = bore_r

    crowned = crown_depth > 0
    edge_r = peak_r - crown_depth if crowned else peak_r

    # Bottom edge: bore -> edge_r at z=0
    L_BOT = sketch.addGeometry(
        Part.LineSegment(Vector(inner_x, 0, 0), Vector(edge_r, 0, 0)), False)

    # Right edge — arc if crowned, line otherwise
    if crowned:
        # Arc through (edge_r, 0), (peak_r, height/2), (edge_r, height)
        # Center on z = height/2 by symmetry; solve for arc_cx
        arc_cx = ((edge_r**2 - peak_r**2 + (height / 2.0)**2)
                  / (2.0 * (edge_r - peak_r)))
        arc_r = peak_r - arc_cx
        ang_a = math.atan2(0 - height / 2.0, edge_r - arc_cx)
        ang_b = math.atan2(height - height / 2.0, edge_r - arc_cx)
        L_RIGHT = sketch.addGeometry(
            Part.ArcOfCircle(
                Part.Circle(Vector(arc_cx, height / 2.0, 0),
                            Vector(0, 0, 1), arc_r),
                ang_a, ang_b
            ), False
        )
    else:
        L_RIGHT = sketch.addGeometry(
            Part.LineSegment(Vector(edge_r, 0, 0), Vector(edge_r, height, 0)),
            False)

    # Top edge: edge_r -> bore at z=height
    L_TOP = sketch.addGeometry(
        Part.LineSegment(Vector(edge_r, height, 0), Vector(inner_x, height, 0)), False)
    L_LEFT = sketch.addGeometry(
        Part.LineSegment(Vector(inner_x, height, 0), Vector(inner_x, 0, 0)), False)

    # Constraints
    def add(c):
        try: sketch.addConstraint(c)
        except Exception as e: App.Console.PrintError(f"  ! {c.Type}: {e}\n")

    add(Sketcher.Constraint("Horizontal", L_BOT))
    add(Sketcher.Constraint("Horizontal", L_TOP))
    add(Sketcher.Constraint("Vertical", L_LEFT))
    if not crowned:
        add(Sketcher.Constraint("Vertical", L_RIGHT))
    add(Sketcher.Constraint("Coincident", L_BOT, 2, L_RIGHT, 1))
    add(Sketcher.Constraint("Coincident", L_RIGHT, 2, L_TOP, 1))
    add(Sketcher.Constraint("Coincident", L_TOP, 2, L_LEFT, 1))
    add(Sketcher.Constraint("Coincident", L_LEFT, 2, L_BOT, 1))
    add(Sketcher.Constraint("DistanceY", -1, 1, L_BOT, 1, 0))
    add(Sketcher.Constraint("DistanceX", -1, 1, L_BOT, 2, edge_r))
    add(Sketcher.Constraint("DistanceX", -1, 1, L_LEFT, 1, inner_x))
    add(Sketcher.Constraint("DistanceY", -1, 1, L_TOP, 1, height))
    if crowned:
        # Lock the arc center; radius implicit from center + endpoint coincidences
        add(Sketcher.Constraint("DistanceX", -1, 1, L_RIGHT, 3, arc_cx))
        add(Sketcher.Constraint("DistanceY", -1, 1, L_RIGHT, 3, height / 2.0))

    sketch.recompute()

    revolution = body.newObject("PartDesign::Revolution", "Revolution")
    revolution.Profile = sketch
    revolution.ReferenceAxis = (sketch, ["V_Axis"])
    revolution.Angle = 360.0

    part_doc.recompute()

    # Save with explicit path
    if part_doc.FileName:
        part_doc.save()
    else:
        part_doc.saveAs(part_path)

    # Close to free resources before processing next part
    App.closeDocument(part_doc.Name)

    return part_path


# ====================================================================
# Build each part
# ====================================================================

results = []
for (name, body_name, OD, bore, height, crown_d, comment) in PARTS:
    crown_label = f" crown={crown_d}" if crown_d > 0 else ""
    App.Console.PrintMessage(
        f"\n--- {name}: OD={OD:.2f} bore={bore:.2f} height={height:.2f}{crown_label} mm ---\n"
        f"    {comment}\n"
    )
    try:
        path = build_hollow_cylinder(name, body_name, OD, bore, height, crown_d)
        size_kb = os.path.getsize(path) / 1024.0
        results.append((name, "OK", size_kb))
        App.Console.PrintMessage(f"    saved: {path} ({size_kb:.1f} KB)\n")
    except Exception as e:
        results.append((name, f"FAIL: {e}", 0))
        App.Console.PrintError(f"    FAILED: {e}\n")


# ====================================================================
# Summary
# ====================================================================

App.Console.PrintMessage(
    "\n================================================================\n"
    f"Macro 06 complete. Built {len(results)} part placeholders.\n"
)
for name, status, kb in results:
    App.Console.PrintMessage(f"  {name:25s} {status:20s} {kb:6.1f} KB\n")
App.Console.PrintMessage(
    "================================================================\n"
    "Run export_stl.py <partname> for each to generate STLs.\n"
)
