# -*- coding: utf-8 -*-
"""
08_build_assembly_layout.py
===========================

Builds the bike-powered glass grinder ASSEMBLY LAYOUT into a fresh
Grinder_Assembly.FCStd file, in the new world frame defined by macro 07.

This is a clean redesign — it replaces the previous off-to-the-side platen
geometry (deleted in Session 8) with a horizontal-belt, desk-front layout
that matches how Isaiah will actually use the machine.

WORLD FRAME (as defined by macro 07 + repeated here for safety)
================================================================
    Origin = rider seat reference point on the floor.
    +Y     = forward (away from rider, toward the desk's far edge).
    +Z     = up.
    +X     = rider's right (left/right axis across the body).
    Belt   = horizontal, long axis along X, centerline at
             (Y = belt_centerline_y = desk_depth, Z = desk_height).

WHAT GETS BUILT
================
Reference + structural:
  RiderSeatRef            small sphere at origin (assembly anchor)
  DeskPlate               610mm (Y) x 900mm (X) x 30mm panel; top at desk_height
  FrameLeg_FL/FR/BL/BR    four corner legs, floor to desk underside.
                          NOTE: front (Y=0) face is OPEN — no cross-rail —
                          so the rider's legs fit under from the seat side.

Drivetrain placeholders (positions are the redesign brief defaults):
  CrankBB_Placeholder     horizontal cyl along X, Y=250, Z=290 (~bike BB height)
  Jackshaft_Placeholder   horizontal cyl along X, Y=400, Z=450 (chosen for
                          clean chain runs — see comment at construction)
  RA_Drive_Placeholder    LABELED block from jackshaft to vertical shaft.
                          Real component: bevel-gear or spiral-bevel right-
                          angle gearbox. NOT hand-waved — must be spec'd later.
  VerticalDriveShaft      vertical cyl, Z = jackshaft_z .. desk_height,
                          at X = +belt_path_center_distance/2, Y = belt_centerline_y
  DrivePulley             axis Z, at (+belt_CD/2, belt_centerline_y, desk_height)
  IdlerPulley             axis Z, at (-belt_CD/2, belt_centerline_y, desk_height)

Reference geometry (in the belt plane, Z = desk_height):
  BeltPath_Front          line along X at Y = belt_centerline_y - drive_R
  BeltPath_Back           line along X at Y = belt_centerline_y + drive_R
                          (Approximation — actual external tangent lines for
                          unequal pulley radii are slightly angled. Acceptable
                          at assembly-layout fidelity.)
  GlassPlatenRef          thin rectangle in belt plane at Y=desk_depth, sized
                          to accept up to max_glass_edge (=18in=457.2mm) glass.
                          18in is project-wide hard constraint; cannot shrink.

PARAMETRIC TEST
===============
Re-running this macro with a different value of <<Drivetrain>>.desk_height
should move the desk plate, leg tops, vertical drive shaft top, pulleys, and
belt-plane references all together. Brief calls for testing two values; see
bottom of this docstring for the verification recipe.

PRE-REQUISITES
==============
- Grinder_Params.FCStd must be loaded BEFORE this macro runs (the headless
  wrapper handles that). All values come from there — single source of truth.
- Macro 07 must have run at least once on Grinder_Params, so the world-frame
  properties exist on the Drivetrain VarSet.

IDEMPOTENT
==========
Wipes any objects this macro previously created (matched by name) before
rebuilding. Re-runnable any number of times without piling up duplicates.

VERIFY PARAMETRIC RECIPE
========================
Run from Bash:
    1. freecadcmd run_macro_08_headless.py        (build at default 762mm)
    2. set desk_height to 850mm in Grinder_Params VarSet (via micro-script
       or GUI), save Grinder_Params, re-run #1 — geometry should regen.
"""

import os
import FreeCAD as App
import Part
from FreeCAD import Vector


# ====================================================================
# Sanity — locate both docs
# ====================================================================
# The headless wrapper opens Grinder_Params first (read-only source of
# truth), then opens or creates Grinder_Assembly (the doc we build into).
# This macro reads from the first and writes to the second.

params = App.getDocument("Grinder_Params")
if params is None:
    raise RuntimeError(
        "Grinder_Params not loaded. The headless wrapper must open it first."
    )

assembly = App.getDocument("Grinder_Assembly")
if assembly is None:
    raise RuntimeError(
        "Grinder_Assembly not loaded. The headless wrapper must create or "
        "open it before exec."
    )

App.setActiveDocument(assembly.Name)


# ====================================================================
# Read all parameters from Grinder_Params (single source of truth)
# ====================================================================

def q(qty):
    """Coerce App.Quantity (mm) to plain float (mm). Same helper as macros 04, 06."""
    return qty.Value if hasattr(qty, "Value") else float(qty)


# World-frame (lives on its own WorldFrame VarSet, maintained by macro 07).
# These describe the human/desk physical setup the drivetrain mounts into,
# so they're separated from Drivetrain (which is shafts/ratios/sprockets).
RIDER_SEAT_Y = q(params.WorldFrame.rider_seat_y)
DESK_DEPTH = q(params.WorldFrame.desk_depth)
DESK_HEIGHT = q(params.WorldFrame.desk_height)
BELT_CENTERLINE_Y = q(params.WorldFrame.belt_centerline_y)

# Belt + pulleys (from macro 01)
BELT_CENTER_DISTANCE = q(params.Belt.belt_path_center_distance)
DRIVE_PULLEY_DIA = q(params.Pulleys.drive_pulley_dia)
IDLER_PULLEY_DIA = q(params.Pulleys.idler_pulley_dia)
PULLEY_FACE = q(params.Pulleys.pulley_face_width)

# Platen / glass constraint
MAX_GLASS_EDGE = q(params.Platen.max_glass_edge)  # 457.2 mm = 18in HARD limit

# Shafts
CRANK_SHAFT_DIA = 16.0       # crank/BB axle (matches parts/crank_bb_shaft.FCStd)
JACKSHAFT_DIA = q(params.Bearings.intermediate_shaft_dia)  # 12 mm
VERT_DRIVE_SHAFT_DIA = q(params.Bearings.grinder_shaft_dia)  # 8 mm

# Derived
DRIVE_R = DRIVE_PULLEY_DIA / 2.0
IDLER_R = IDLER_PULLEY_DIA / 2.0
DRIVE_X = +BELT_CENTER_DISTANCE / 2.0
IDLER_X = -BELT_CENTER_DISTANCE / 2.0


# ====================================================================
# Layout choices (assembly-level, not in VarSet — flagged via comments)
# ====================================================================
# These are first-pass design assumptions. If any becomes load-bearing
# enough that the rest of the design depends on it, promote to a VarSet.

DESK_THICKNESS = 30.0        # arbitrary — typical school desk top is 19-30 mm
DESK_WIDTH_X = 900.0         # along world X. Wider than belt span (734.9) so
                             # both pulleys sit comfortably on the desk plate.
LEG_DIA = 30.0
LEG_INSET_FROM_EDGE = 25.0   # legs pulled in from desk corners for clean look

# Crank / BB placeholder (per redesign brief)
CRANK_Y = 250.0
CRANK_Z = 290.0              # ASSUMPTION: ~290 mm above floor is a typical
                             # bike-BB-to-pedal-axle height for a 170 mm crank
                             # arm at low position. Refine when we pick the
                             # actual crank length.
CRANK_LENGTH_X = 140.0       # matches parts/crank_bb_shaft.FCStd

# Jackshaft placeholder
JACKSHAFT_Y = 400.0
JACKSHAFT_Z = 450.0          # CHOSEN for clean chain runs:
                             # - chain from chainring (Y=250, Z=290) up to
                             #   jackshaft (Y=400, Z=450): ΔY=150, ΔZ=160 ⇒
                             #   ~47° rise, well within standard chain limits
                             # - vertical drive shaft from JS_Z=450 up to
                             #   belt plane Z=desk_height: 312 mm of clean
                             #   vertical run (at default 762mm desk).
JACKSHAFT_LENGTH_X = 800.0   # long enough to span from rider's center to
                             # the drive-pulley X column (DRIVE_X ≈ 367 mm).

# Right-angle drive placeholder block — bridges the (X=0, Y=400) jackshaft
# end to the (X=DRIVE_X, Y=BELT_CL) vertical drive shaft. Real component is
# a bevel-gear or spiral-bevel right-angle gearbox; this block is just a
# spatial reservation + a label for future component spec.
RA_DRIVE_X_HALF = 60.0
RA_DRIVE_Z_HEIGHT = 100.0
RA_DRIVE_Z_BOTTOM = JACKSHAFT_Z - RA_DRIVE_Z_HEIGHT / 2.0


# ====================================================================
# Idempotency — wipe any objects this macro previously created
# ====================================================================
# We track our names in MANAGED_NAMES. Anything else in the doc is left
# alone. Safe re-run.

MANAGED_NAMES = [
    "RiderSeatRef",
    "DeskPlate",
    "FrameLeg_FL", "FrameLeg_FR", "FrameLeg_BL", "FrameLeg_BR",
    "CrankBB_Placeholder",
    "Jackshaft_Placeholder",
    "RA_Drive_Placeholder",
    "VerticalDriveShaft",
    "DrivePulley",
    "IdlerPulley",
    "BeltPath_Front",
    "BeltPath_Back",
    "GlassPlatenRef",
]

removed = 0
for name in MANAGED_NAMES:
    obj = assembly.getObject(name)
    if obj is not None:
        assembly.removeObject(name)
        removed += 1
App.Console.PrintMessage(
    f"Idempotency: removed {removed} pre-existing managed objects.\n"
)


# ====================================================================
# Helper builders (return the FreeCAD object so we can label/track it)
# ====================================================================

def add_box(name, length_x, length_y, length_z, position, label=None):
    """Add a Part::Box. Position is the corner with smallest x/y/z."""
    obj = assembly.addObject("Part::Box", name)
    obj.Length = length_x
    obj.Width = length_y
    obj.Height = length_z
    obj.Placement = App.Placement(position, App.Rotation())
    obj.Label = label or name
    return obj


def add_cyl_z(name, dia, height, position, label=None):
    """Cylinder with axis along world +Z. Position is the base center."""
    obj = assembly.addObject("Part::Cylinder", name)
    obj.Radius = dia / 2.0
    obj.Height = height
    obj.Placement = App.Placement(position, App.Rotation())
    obj.Label = label or name
    return obj


def add_cyl_x(name, dia, length, center, label=None):
    """Cylinder with axis along world +X, centered at `center` (Vector)."""
    # Default cylinder grows along its local Z. To put axis on world X,
    # rotate +90° about world Y. After rotation, the cylinder's base
    # (which was at Placement.Position) sits at the X-low end of the
    # cylinder. So we pre-shift by -length/2 along X to get a cylinder
    # centered at `center`.
    obj = assembly.addObject("Part::Cylinder", name)
    obj.Radius = dia / 2.0
    obj.Height = length
    base_pos = Vector(center.x - length / 2.0, center.y, center.z)
    obj.Placement = App.Placement(
        base_pos, App.Rotation(Vector(0, 1, 0), 90)
    )
    obj.Label = label or name
    return obj


def add_sphere(name, radius, position, label=None):
    obj = assembly.addObject("Part::Sphere", name)
    obj.Radius = radius
    obj.Placement = App.Placement(position, App.Rotation())
    obj.Label = label or name
    return obj


def add_line_segment(name, p1, p2, label=None):
    """Add a Part::Feature wrapping a single line edge from p1 to p2."""
    edge = Part.makeLine(p1, p2)
    obj = assembly.addObject("Part::Feature", name)
    obj.Shape = edge
    obj.Label = label or name
    return obj


# ====================================================================
# Build the assembly
# ====================================================================

App.Console.PrintMessage("Building assembly geometry...\n")

# --- Rider reference: small sphere at origin (assembly anchor) ---
add_sphere("RiderSeatRef", 25.0, Vector(0, 0, 0),
           label="RiderSeatRef_origin")

# --- Desk plate ---
# Top surface at Z = DESK_HEIGHT, plate sits below by DESK_THICKNESS.
desk_z_bottom = DESK_HEIGHT - DESK_THICKNESS
add_box(
    "DeskPlate",
    DESK_WIDTH_X, DESK_DEPTH, DESK_THICKNESS,
    Vector(-DESK_WIDTH_X / 2.0, RIDER_SEAT_Y, desk_z_bottom),
    label=f"DeskPlate_{int(DESK_DEPTH)}x{int(DESK_WIDTH_X)}_top@{int(DESK_HEIGHT)}"
)

# --- Frame legs (4 corners, no front cross-rail — seat-side open) ---
leg_x_outer = DESK_WIDTH_X / 2.0 - LEG_INSET_FROM_EDGE - LEG_DIA / 2.0
leg_y_front = RIDER_SEAT_Y + LEG_INSET_FROM_EDGE
leg_y_back = RIDER_SEAT_Y + DESK_DEPTH - LEG_INSET_FROM_EDGE
leg_height = desk_z_bottom  # floor (Z=0) up to underside of desk

leg_positions = [
    ("FrameLeg_FL", -leg_x_outer, leg_y_front),  # Front-Left
    ("FrameLeg_FR", +leg_x_outer, leg_y_front),  # Front-Right
    ("FrameLeg_BL", -leg_x_outer, leg_y_back),   # Back-Left
    ("FrameLeg_BR", +leg_x_outer, leg_y_back),   # Back-Right
]
for (name, lx, ly) in leg_positions:
    add_cyl_z(name, LEG_DIA, leg_height, Vector(lx, ly, 0),
              label=f"{name}_floor_to_desk_underside")

# --- Crank/BB placeholder (horizontal X-axis cylinder) ---
add_cyl_x(
    "CrankBB_Placeholder",
    CRANK_SHAFT_DIA, CRANK_LENGTH_X,
    Vector(0, CRANK_Y, CRANK_Z),
    label=f"CrankBB_Y{int(CRANK_Y)}_Z{int(CRANK_Z)}_assumed_BB_height"
)

# --- Jackshaft placeholder (horizontal X-axis cylinder) ---
add_cyl_x(
    "Jackshaft_Placeholder",
    JACKSHAFT_DIA, JACKSHAFT_LENGTH_X,
    Vector(0, JACKSHAFT_Y, JACKSHAFT_Z),
    label=f"Jackshaft_Y{int(JACKSHAFT_Y)}_Z{int(JACKSHAFT_Z)}"
)

# --- Right-angle drive placeholder block ---
# Bridges from the jackshaft (at Y=JACKSHAFT_Y) to the vertical drive
# shaft column (at X=DRIVE_X, Y=BELT_CENTERLINE_Y). Box spans the gap.
ra_y_min = min(JACKSHAFT_Y, BELT_CENTERLINE_Y)
ra_y_max = max(JACKSHAFT_Y, BELT_CENTERLINE_Y)
ra_y_depth = (ra_y_max - ra_y_min) + 40.0  # +40mm housing margin
add_box(
    "RA_Drive_Placeholder",
    RA_DRIVE_X_HALF * 2.0, ra_y_depth, RA_DRIVE_Z_HEIGHT,
    Vector(DRIVE_X - RA_DRIVE_X_HALF,
           ra_y_min - 20.0,
           RA_DRIVE_Z_BOTTOM),
    label="RA_Drive_PLACEHOLDER_BevelGearOrSpiralBevel_TBD_spec_required"
)

# --- Vertical drive shaft (Z-axis cylinder) ---
vert_shaft_height = DESK_HEIGHT - JACKSHAFT_Z
add_cyl_z(
    "VerticalDriveShaft",
    VERT_DRIVE_SHAFT_DIA, vert_shaft_height,
    Vector(DRIVE_X, BELT_CENTERLINE_Y, JACKSHAFT_Z),
    label=f"VerticalDriveShaft_X{int(DRIVE_X)}_Y{int(BELT_CENTERLINE_Y)}"
)

# --- Drive pulley (axis Z, at top of vertical drive shaft) ---
# Cylinder placed so it straddles Z = DESK_HEIGHT (sits ON the belt plane).
# Bottom of the pulley body at DESK_HEIGHT - PULLEY_FACE/2 so the belt
# wraps around it through Z=DESK_HEIGHT.
add_cyl_z(
    "DrivePulley",
    DRIVE_PULLEY_DIA, PULLEY_FACE,
    Vector(DRIVE_X, BELT_CENTERLINE_Y, DESK_HEIGHT - PULLEY_FACE / 2.0),
    label=f"DrivePulley_dia{int(DRIVE_PULLEY_DIA)}"
)

# --- Idler pulley (axis Z, mirrored at -X) ---
add_cyl_z(
    "IdlerPulley",
    IDLER_PULLEY_DIA, PULLEY_FACE,
    Vector(IDLER_X, BELT_CENTERLINE_Y, DESK_HEIGHT - PULLEY_FACE / 2.0),
    label=f"IdlerPulley_dia{int(IDLER_PULLEY_DIA)}"
)

# --- Belt path reference (two parallel lines along X in belt plane) ---
# Approximation: tangent lines for unequal pulley radii are NOT actually
# parallel, but the deviation is small (atan((DRIVE_R - IDLER_R) /
# BELT_CENTER_DISTANCE) ~= 3°). For assembly-layout fidelity this is fine.
# Lines run from idler pulley to drive pulley, offset front/back by DRIVE_R.
belt_z = DESK_HEIGHT
add_line_segment(
    "BeltPath_Front",
    Vector(IDLER_X, BELT_CENTERLINE_Y - DRIVE_R, belt_z),
    Vector(DRIVE_X, BELT_CENTERLINE_Y - DRIVE_R, belt_z),
    label="BeltPath_Front_approxParallelToX"
)
add_line_segment(
    "BeltPath_Back",
    Vector(IDLER_X, BELT_CENTERLINE_Y + DRIVE_R, belt_z),
    Vector(DRIVE_X, BELT_CENTERLINE_Y + DRIVE_R, belt_z),
    label="BeltPath_Back_approxParallelToX"
)

# --- Glass platen reference at desk's far edge ---
# Thin rectangle in the belt plane (Z=DESK_HEIGHT) at Y=DESK_DEPTH.
# X-length sized to accept up to MAX_GLASS_EDGE (=457.2 mm = 18 in) glass
# edges with margin. 18in is a project-wide HARD constraint until tooling
# grows.
PLATEN_REF_X_LENGTH = MAX_GLASS_EDGE + 80.0  # +40mm margin per side
PLATEN_REF_Y_DEPTH = 50.8                    # = belt_width, contact-zone
PLATEN_REF_Z_THICKNESS = 1.0                 # paper-thin reference plate
add_box(
    "GlassPlatenRef",
    PLATEN_REF_X_LENGTH, PLATEN_REF_Y_DEPTH, PLATEN_REF_Z_THICKNESS,
    Vector(-PLATEN_REF_X_LENGTH / 2.0,
           DESK_DEPTH - PLATEN_REF_Y_DEPTH / 2.0,
           DESK_HEIGHT),
    label=f"GlassPlatenRef_max{int(MAX_GLASS_EDGE)}mm_18in_HARD_constraint"
)


# ====================================================================
# Recompute and report
# ====================================================================
assembly.recompute()

# Sanity snapshot for the console — Isaiah can scan key positions
# without opening the GUI.
App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 08 complete. Grinder_Assembly built in new world frame.\n"
    "================================================================\n"
    f"  WORLD FRAME (origin = rider seat on floor)\n"
    f"    rider_seat_y      = {RIDER_SEAT_Y:>8.1f} mm\n"
    f"    desk_depth        = {DESK_DEPTH:>8.1f} mm\n"
    f"    desk_height       = {DESK_HEIGHT:>8.1f} mm\n"
    f"    belt_centerline_y = {BELT_CENTERLINE_Y:>8.1f} mm\n"
    f"\n"
    f"  KEY POSITIONS (X, Y, Z) in mm\n"
    f"    rider seat          = (    0,     0,     0)\n"
    f"    crank/BB            = (    0, {CRANK_Y:>5.0f}, {CRANK_Z:>5.0f})  axis=X\n"
    f"    jackshaft           = (    0, {JACKSHAFT_Y:>5.0f}, {JACKSHAFT_Z:>5.0f})  axis=X\n"
    f"    RA-drive (placeholder housing center)\n"
    f"                        = ({DRIVE_X:>5.0f}, {(JACKSHAFT_Y + BELT_CENTERLINE_Y) / 2.0:>5.0f}, {JACKSHAFT_Z:>5.0f})\n"
    f"    vertical drive shaft= ({DRIVE_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {JACKSHAFT_Z:>5.0f}..{DESK_HEIGHT:.0f}) axis=Z\n"
    f"    drive pulley center = ({DRIVE_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z dia={DRIVE_PULLEY_DIA:.1f}\n"
    f"    idler pulley center = ({IDLER_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z dia={IDLER_PULLEY_DIA:.1f}\n"
    f"    glass platen ref    = (X=±{PLATEN_REF_X_LENGTH/2.0:.0f}, Y={DESK_DEPTH:.0f}, Z={DESK_HEIGHT:.0f})  "
    f"max edge {MAX_GLASS_EDGE:.1f}mm (18in HARD)\n"
    f"\n"
    f"  Belt span (drive-to-idler center distance): {BELT_CENTER_DISTANCE:.1f} mm\n"
    f"  Belt path lines at Y = {BELT_CENTERLINE_Y:.0f} ± {DRIVE_R:.1f}, Z = {DESK_HEIGHT:.0f}\n"
    "================================================================\n"
    "REMINDER: RA_Drive_Placeholder is a SPATIAL RESERVATION + LABEL.\n"
    "It must be replaced with a real bevel-gear or spiral-bevel right-\n"
    "angle gearbox component, spec'd separately. Don't ship without it.\n"
    "================================================================\n"
)
