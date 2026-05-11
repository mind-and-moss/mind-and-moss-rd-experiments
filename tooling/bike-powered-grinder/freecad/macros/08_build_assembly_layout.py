# -*- coding: utf-8 -*-
"""
08_build_assembly_layout.py
===========================

Builds the bike-powered glass grinder ASSEMBLY LAYOUT into a fresh
Grinder_Assembly.FCStd file, in the world frame defined by macro 07.

SESSION 9 RE-ARCHITECTURE — drivetrain change
=============================================
This macro replaces the Session 8 layout (TWO chain stages: chainring →
chain → stage1_cog ; stage2_large → chain → stage2_pinion) with:

    chainring (BB, horizontal X axis)
        → chain
        → stage1_cog (jackshaft, horizontal X axis)
        → bevel right-angle gearbox  [RA_Drive_Placeholder, real component TBD]
        → vertical drive shaft (Z axis)
        → drive pulley (Z axis, top of desk)
        → flat belt
        → idler pulley (Z axis, top of desk)

ONE chain stage, not two. The bevel gearbox replaces what used to be
chain stage 2. Chain runs in a vertical YZ plane at world X =
chain_plane_x (Drivetrain VarSet, default 75 mm — rider's right side,
just outboard of the BB axle's right end).

UNUSED IN THIS ASSEMBLY (FCStd files preserved on disk, NOT deleted):
- parts/stage2_pinion.FCStd     — was the 8T grinder-shaft pinion
- parts/stage2_large.FCStd      — was the 25T jackshaft sprocket
Their reason for being dropped: with one chain stage + bevel gearbox,
there is no second chain-driven sprocket pair. The bevel gearbox's input
gear is INSIDE the gearbox housing (not a sprocket), so neither legacy
part has a place in the new topology. Files stay on disk in case the
two-chain topology resurfaces in a future variant.

WORLD FRAME (defined by macro 07; repeated here for safety)
===========================================================
    Origin = rider seat reference point on the floor.
    +Y     = forward (away from rider, toward the desk's far edge).
    +Z     = up.
    +X     = rider's right (left/right axis across the body).
    Belt   = horizontal, long axis along X, centerline at
             (Y = belt_centerline_y = desk_depth, Z = desk_height).

ERGONOMIC ASSUMPTIONS (Session 9 redesign)
==========================================
- Rider sits in a SEPARATE school chair pulled up to the desk's Y=0
  face. Not modeled here — RiderSeatRef sphere at world origin marks the
  intended seat position only.
- No integrated saddle, no seatpost, no handlebars or grab handles.
  Rider's hands grip the glass at the desk's far edge against the belt.
- No wheels. Stationary shop tool. Frame = 4 legs + 3 rails (back + L +
  R), front (Y=0) face open so legs fit under from the seat side.
- A chair-with-arms or backrest is a future chair-shopping decision —
  not modeled.
- Minimal bike-inspired bracing: ONE diagonal "downtube-equivalent" tube
  from the BB area up to the back rail centerline, sized for typical
  donor-bike tubing so a real donor frame can later slot in with
  parameter tweaks. No chainstays, seatstays, or top tube.

WHAT GETS BUILT
===============
Reference + structural:
  RiderSeatRef            sphere at origin (assembly anchor)
  DeskPlate               panel; top at desk_height
  FrameLeg_FL/FR/BL/BR    four corner legs, floor → desk underside
  FrameRail_Back/Left/Right  3 top rails (front open for rider's legs)
  Downtube_Brace          diagonal tube, BB area → back rail centerline
  GlassPlatenRef          thin platen-line reference at desk far edge

Drivetrain — App::Linked real parts pulled from parts/:
  CrankBB_ShaftLink       crank_bb_shaft (16mm OD, 140mm long, axis X)
  Jackshaft_Link          intermediate_shaft (12mm OD, 150mm long, axis X)
  VerticalDriveShaft_Link grinder_shaft (8mm OD, 150mm long, axis Z)
  IdlerShaft_Link         idler_shaft (8mm OD, 80mm long, axis Z)
  Chainring_Link          chainring (170mm OD, axis X, in chain plane)
  Stage1Cog_Link          stage1_cog (53mm OD, axis X, in chain plane)
  DrivePulley_Link        drive_pulley (152mm OD, axis Z)
  IdlerPulley_Link        idler_pulley (76mm OD, axis Z)

Drivetrain — placeholder geometry:
  RA_Drive_Placeholder    LABELED block bridging jackshaft end → vertical
                          drive shaft. Real component is a bevel-gear or
                          spiral-bevel right-angle gearbox; not yet spec'd.

Loop visualization — solid extruded racetrack rings:
  ChainLoop               actual chain envelope (chainring → stage1_cog),
                          extruded along X, in YZ plane at chain_plane_x.
  BeltLoop                actual belt envelope (drive ↔ idler pulleys),
                          extruded along Z, in XY plane at desk_height.

KNOWN LIMITATION — shaft donor-stock lengths
=============================================
The shaft FCStd files in parts/ represent DONOR-STOCK SYMBOLS at fixed
lengths (140-150 mm). The actual machine needs:
  - jackshaft span: ~chain_plane_x to RA_Drive at X=DRIVE_X (~290 mm)
  - vertical drive shaft span: jackshaft Z to desk_height (~310 mm)
The 150 mm parts are linked AS-IS per the brief. There WILL be visible
gaps in the assembly between sprockets/pulleys and the linked rod ends.
The real shafts will be cut from stock to assembly span when fabricated;
this assembly is for layout fidelity, not bill-of-materials.

PRE-REQUISITES
==============
- Grinder_Params.FCStd loaded (headless wrapper does this).
- Macro 07 must have run at least once (WorldFrame VarSet).
- Macro 09 must have run at least once (Drivetrain.chain_plane_x).
- All parts/*.FCStd referenced below must exist (built by macros 05+06).

IDEMPOTENT
==========
Wipes any objects this macro previously created (matched by name) before
rebuilding. Re-runnable any number of times without piling up duplicates.
Old Session-8 placeholder names (e.g. CrankBB_Placeholder) are also in
the wipe list so the migration is clean.
"""

import os
import math
import FreeCAD as App
import Part
from FreeCAD import Vector


# ====================================================================
# Sanity — locate both docs
# ====================================================================
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
    """Coerce App.Quantity (mm) to plain float (mm)."""
    return qty.Value if hasattr(qty, "Value") else float(qty)


# World frame (macro 07)
RIDER_SEAT_Y = q(params.WorldFrame.rider_seat_y)
DESK_DEPTH = q(params.WorldFrame.desk_depth)
DESK_HEIGHT = q(params.WorldFrame.desk_height)
BELT_CENTERLINE_Y = q(params.WorldFrame.belt_centerline_y)

# Chain plane (macro 09 — the load-bearing X position both sprockets share)
CHAIN_PLANE_X = q(params.Drivetrain.chain_plane_x)

# Belt + pulleys
BELT_CENTER_DISTANCE = q(params.Belt.belt_path_center_distance)
DRIVE_PULLEY_DIA = q(params.Pulleys.drive_pulley_dia)
IDLER_PULLEY_DIA = q(params.Pulleys.idler_pulley_dia)
PULLEY_FACE = q(params.Pulleys.pulley_face_width)
BELT_WIDTH = q(params.Belt.belt_width)

# Chain (for sprocket pitch diameters)
CHAIN_PITCH = q(params.Drivetrain.chain_pitch)
CHAINRING_TEETH = int(params.Drivetrain.stage1_chainring_teeth)
COG_TEETH = int(params.Drivetrain.stage1_cog_teeth)
STAGE2_LARGE_TEETH = int(params.Drivetrain.stage2_large_teeth)
STAGE2_PINION_TEETH = int(params.Drivetrain.stage2_pinion_teeth)
TOTAL_RATIO_TARGET = q(params.Drivetrain.total_ratio)

# Platen
MAX_GLASS_EDGE = q(params.Platen.max_glass_edge)

# Derived
DRIVE_R = DRIVE_PULLEY_DIA / 2.0
IDLER_R = IDLER_PULLEY_DIA / 2.0
DRIVE_X = +BELT_CENTER_DISTANCE / 2.0
IDLER_X = -BELT_CENTER_DISTANCE / 2.0
CHAINRING_PITCH_R = CHAIN_PITCH / (2.0 * math.sin(math.pi / CHAINRING_TEETH))
COG_PITCH_R = CHAIN_PITCH / (2.0 * math.sin(math.pi / COG_TEETH))
STAGE2_LARGE_PITCH_R = CHAIN_PITCH / (2.0 * math.sin(math.pi / STAGE2_LARGE_TEETH))
STAGE2_PINION_PITCH_R = CHAIN_PITCH / (2.0 * math.sin(math.pi / STAGE2_PINION_TEETH))


# ====================================================================
# Open all parts/ docs we'll App::Link to. Closing them later would
# break the link resolution; they stay loaded for the rest of the
# headless run. The assembly's saved file records each link by file
# path + body name so reopening the assembly auto-loads dependencies.
# ====================================================================

# Anchor parts/ directory to the Grinder_Params.FCStd location rather
# than __file__ (which is undefined when this macro is executed via
# exec() from the headless wrapper).
_params_dir = os.path.dirname(params.FileName) if params.FileName else os.getcwd()
PARTS_DIR = os.path.abspath(os.path.join(_params_dir, "parts"))


def open_part(filename):
    """Open parts/<filename> if not already open. Return the doc.
    NOTE: App.getDocument(name) raises NameError when the doc is not
    loaded — it does NOT return None — so we check via listDocuments()."""
    name = os.path.splitext(filename)[0]
    if name in App.listDocuments():
        return App.getDocument(name)
    return App.openDocument(os.path.join(PARTS_DIR, filename))


# Each entry: (filename, body_name, native_height_mm). Heights are for
# placement-centering math; sourced from macros 05+06 build records.
PART_SPECS = {
    "chainring":          ("chainring.FCStd",          "ChainringBody",         5.0),
    "stage1_cog":         ("stage1_cog.FCStd",         "CogBody",               5.0),
    "stage2_large":       ("stage2_large.FCStd",       "LargeSprocketBody",    12.0),
    "stage2_pinion":      ("stage2_pinion.FCStd",      "PinionBody",           16.0),
    "drive_pulley":       ("drive_pulley.FCStd",       "PulleyBody",           60.0),
    "idler_pulley":       ("idler_pulley.FCStd",       "IdlerBody",            60.0),
    "crank_bb_shaft":     ("crank_bb_shaft.FCStd",     "CrankBBShaftBody",    140.0),
    "intermediate_shaft": ("intermediate_shaft.FCStd", "IntermediateShaftBody", 150.0),
    "grinder_shaft":      ("grinder_shaft.FCStd",      "GrinderShaftBody",    150.0),
    "idler_shaft":        ("idler_shaft.FCStd",        "IdlerShaftBody",       80.0),
    "bevel_gear":         ("bevel_gear.FCStd",         "BevelGearBody",         8.0),
    # Session-10 Phase-2 new parts
    "bb_shell":           ("bb_shell.FCStd",           "BBShellBody",          68.0),
    "crank_arm":          ("crank_arm.FCStd",          "CrankArmBody",         10.0),
    "pedal":              ("pedal.FCStd",              "PedalBody",            12.0),
    "pillow_block":       ("pillow_block.FCStd",       "PillowBlockBody",      38.0),
    "bevel_mount_bracket":("bevel_mount_bracket.FCStd","BevelMountBracketBody", 200.0),
    "chain_link":         ("chain_link.FCStd",         "ChainLinkBody",        12.7),
}

PART_BODIES = {}
for key, (fname, body_name, _) in PART_SPECS.items():
    pdoc = open_part(fname)
    body = pdoc.getObject(body_name)
    if body is None:
        raise RuntimeError(f"Body '{body_name}' missing in {fname}")
    PART_BODIES[key] = body


def native_h(key):
    return PART_SPECS[key][2]


# ====================================================================
# Layout choices (assembly-level constants; promote to VarSet when a
# real donor bike or chair is selected)
# ====================================================================

# Frame dims
DESK_THICKNESS = 30.0
DESK_WIDTH_X = 900.0
LEG_DIA = 30.0
LEG_INSET_FROM_EDGE = 25.0
RAIL_THICKNESS = 30.0
RAIL_HEIGHT = 50.0

# Drivetrain shaft positions (Session 9 — TODO: promote to AssemblyLayout VarSet
# when a donor bike is selected; the parametric model should follow donor geom)
CRANK_Y = 250.0
CRANK_Z = 290.0
JACKSHAFT_Y = 400.0
JACKSHAFT_Z = 450.0

# ---------------------------------------------------------------
# Session 10 Q2 — visible bevel-gear pair + restored stage 2 chain
# ---------------------------------------------------------------
# Decision (Session 10, Q2): RA_Drive_Placeholder REMOVED. Replaced with
# two visible 1:1 bevel-gear placeholders (cone frustums) and the
# previously-dropped stage 2 chain restored. Total ratio still 10.10:1
# (chain stages do all reduction; bevel just turns the corner).
#
# Topology:
#   chainring (BB, X) → chain1 → stage1_cog (jackshaft, X) →
#   bevel_input (X) ⟂ bevel_output (Z) →
#   stage2_large (bevel-out shaft, Z) → chain2 → stage2_pinion (grinder shaft, Z) →
#   drive pulley → belt → idler pulley
#
# Ratio: (42/13) × 1.0 × (25/8) = 10.096 ≈ 10:1 ✓

# Bevel-pair meets at a single apex point. Bevel input cone axis is
# world X (jackshaft direction), output cone axis is world Z (vertical).
# Session-10 upgrade (post-Q2 clarification): real involute teeth via the
# freecad.gears workbench — see macro 10. Both gears App::Link to the
# same parts/bevel_gear.FCStd (1:1 ratio, identical part).
BEVEL_MEETING_X = 300.0           # apex along jackshaft, past stage1_cog
BEVEL_MEETING_Y = JACKSHAFT_Y     # = 400 (must lie on jackshaft axis)
BEVEL_MEETING_Z = JACKSHAFT_Z     # = 450 (must lie on jackshaft axis)
# Bevel gear params — keep in sync with macro 10:
BEVEL_GEAR_MODULE = 3.0
BEVEL_GEAR_TEETH = 16
BEVEL_GEAR_HEIGHT = 8.0           # face width along cone axis
BEVEL_GEAR_PITCH_ANGLE_DEG = 45.0 # 1:1 mesh at 90°
# Apex distance (along axis from large face to extrapolated apex):
#   scale = (module * num_teeth / 2) / tan(pitch_angle)
BEVEL_GEAR_APEX_DISTANCE = (
    (BEVEL_GEAR_MODULE * BEVEL_GEAR_TEETH / 2.0)
    / math.tan(math.radians(BEVEL_GEAR_PITCH_ANGLE_DEG))
)  # = 24.0 mm for the locked params

# Stage 2 chain plane (horizontal XY at this Z)
CHAIN2_PLANE_Z = 580.0

# Vertical bevel-output shaft (between bevel output and stage2_large)
BEVEL_OUT_SHAFT_X = BEVEL_MEETING_X
BEVEL_OUT_SHAFT_Y = BEVEL_MEETING_Y

# ---------------------------------------------------------------
# Session 10 — ground-anchored BB support (replaces Downtube_Brace)
# ---------------------------------------------------------------
# Decision (Session 10, Q1): BB shell is supported from below by a
# vertical post planted on a concrete floor block (rider-side, "behind"
# the BB). Cantilever bending at the joint is mitigated by:
#   (1) fat 50mm post (vs. 30mm donor-bike tubing)
#   (2) split-collar clamp wrapping full BB shell circumference
#   (3) post extends above the BB so clamp loads in shear, not bending
#   (4) diagonal strut from post-base to BB-front side, forming a triangle
# All assembly-level constants for now; promote to VarSet when donor
# tubing + concrete-block source are confirmed (Q3 still open).

# Main vertical post (rider-side of BB, runs from block top up past BB)
GROUND_POST_OFFSET_Y = -50.0       # 50mm behind BB axle (rider side)
GROUND_POST_OD = 50.0              # 50mm OD steel tube
GROUND_POST_TOP_Z_OVER_BB = 60.0   # post extends 60mm above BB top

# Concrete block under the post — Q3 (Session 10): SELF-CAST pyramidal
# frustum with WIDER BASE for spike resistance. Sits on floor; post bottom
# mounts to its top.
#
# BACK-CALCULATION of footprint (Session-10 design notes):
# ========================================================
# Design loads at the BB:
#   - Pedal force peak (rider standing on pedal):    ~ 800 N
#   - Dynamic spike (kickback / chain jam):          2-3x sustained = ~2400 N peak
#   - Lateral force (rider body twitch):             ~ 300 N
# Tipping moment about block edge (worst case):
#   M_tip = F_lat × (BB_height - block_top) ≈ 300 N × 0.20 m ≈ 60 N·m
# Required tipping resistance with 2x safety factor: 120 N·m
# Resistance comes from block weight × half-base-width:
#   M_resist = ρ_concrete × g × V × (b/2)
# where ρ_concrete = 2400 kg/m³, g = 9.81 m/s².
#
# PEDAL-CLEARANCE constraint (this is what set the X dimension):
#   Right pedal traces a YZ circle at world X = +170 mm (crank arm length).
#   Rider's foot (shoe) extends INWARD from pedal to ankle at ~X = +140 mm.
#   At pedal bottom-of-stroke (Y=250, Z=120), foot intrudes into the
#   region above the block.
#   So block half-width in X MUST be < 140 mm.  Picked 120 mm → 20 mm
#   foot clearance at the inner edge.
#
# Final block: base 240 × 400 × 200 mm pyramidal frustum, top 200 × 200.
#   Volume = (h/3)(A_base + A_top + √(A_base·A_top))
#          = (0.20/3)(0.096 + 0.04 + 0.062) ≈ 0.0132 m³
#   Mass   ≈ 32 kg
#   Tip resist (X edge, fore-aft pedaling spike):  32×9.81×0.20 ≈ 63 N·m  ← ~52% of target
#   Tip resist (Y edge, side spike):               32×9.81×0.12 ≈ 38 N·m  ← lower (X is narrow by design)
# The remaining tipping margin comes from the truss + chain + desk-frame
# being a connected structural system — block is one node, not standalone.
# Re-tune if real bench testing shows wobble.
CONCRETE_BLOCK_BASE_X = 240.0
CONCRETE_BLOCK_BASE_Y = 400.0
CONCRETE_BLOCK_TOP_X = 200.0
CONCRETE_BLOCK_TOP_Y = 200.0
CONCRETE_BLOCK_Z_HEIGHT = 200.0

# Split-collar clamp wrapping the BB shell (axis X, sleeve geometry)
BB_CLAMP_OD = 60.0                 # outer dia of clamp
BB_CLAMP_LENGTH = 40.0             # axial length along X

# Diagonal strut: post-base → BB-front-side. Converts cantilever to truss.
STRUT_OD = 30.0
STRUT_FORWARD_OFFSET_Y = +50.0     # strut top-end attaches 50mm forward of BB axle

# Chain visualization (envelope, not real link geometry)
CHAIN_BAND_RADIAL = 11.0   # ~plate height of #40 chain
CHAIN_EXTRUDE_X = 8.0      # ~chain width across plates+rollers

# Belt visualization
BELT_THICKNESS = 2.0       # ~Sackorange SiC sanding belt thickness


# ====================================================================
# Idempotency — wipe any objects this macro previously created
# ====================================================================
# Includes both Session-9 names AND the older Session-8 placeholder
# names so re-runs after the migration leave no orphans.

MANAGED_NAMES = [
    # Reference / frame
    "RiderSeatRef",
    "DeskPlate",
    "FrameLeg_FL", "FrameLeg_FR", "FrameLeg_BL", "FrameLeg_BR",
    "FrameRail_Back", "FrameRail_Left", "FrameRail_Right",
    "Downtube_Brace",  # Session-9 element, removed in Session 10 — kept here for cleanup on re-run
    "GlassPlatenRef",

    # Session-10 BB ground support
    "ConcreteBlock_Anchor",
    "GroundPost_Main",
    "GroundPost_DiagonalStrut",
    "BB_SplitCollar",

    # Session-9 RA-drive placeholder (removed in Session 10 — kept for cleanup on re-run)
    "RA_Drive_Placeholder",

    # Session-9 App::Link names
    "CrankBB_ShaftLink",
    "Jackshaft_Link",
    "VerticalDriveShaft_Link",
    "IdlerShaft_Link",
    "Chainring_Link",
    "Stage1Cog_Link",
    "DrivePulley_Link",
    "IdlerPulley_Link",

    # Session-10 bevel pair + restored stage-2 chain
    "BevelGear_Input",
    "BevelGear_Output",
    "BevelOutputShaft_Link",
    "Stage2Large_Link",
    "Stage2Pinion_Link",
    "ChainLoop2",

    # Loops (Session-9 envelope solids; replaced by chain-link arrays in
    # Session-10 Phase 2, but names kept here for cleanup on re-run)
    "ChainLoop",
    "BeltLoop",

    # Session-10 Phase-2: gaps + supports
    "BBShell_Link",
    "CrankArmLeft_Link", "CrankArmRight_Link",
    "PedalLeft_Link", "PedalRight_Link",
    "PillowBlock_Jackshaft_L", "PillowBlock_Jackshaft_R",
    "PillowBlock_BevelOut_Bot", "PillowBlock_BevelOut_Top",
    "PillowBlock_Grinder_Bot", "PillowBlock_Grinder_Top",
    "PillowBlock_Idler_Top",
    "BevelMountBracket_Link",
    # Belt loop kept (real belts are continuous, not discrete links).
    # Chain loops removed in favor of chain_link arrays — wiped by prefix below.

    # Legacy Session-8 placeholder names (left in for migration cleanup)
    "CrankBB_Placeholder",
    "Jackshaft_Placeholder",
    "VerticalDriveShaft",
    "DrivePulley",
    "IdlerPulley",
    "BeltPath_Front",
    "BeltPath_Back",
]

removed = 0
for name in MANAGED_NAMES:
    if assembly.getObject(name) is not None:
        assembly.removeObject(name)
        removed += 1
# Prefix-based wipe for variable-length arrays (chain links).
prefix_managed = ("Chain1Link_", "Chain2Link_")
for o in list(assembly.Objects):
    if o.Name.startswith(prefix_managed):
        assembly.removeObject(o.Name)
        removed += 1
App.Console.PrintMessage(
    f"Idempotency: removed {removed} pre-existing managed objects.\n"
)


# ====================================================================
# Helper builders
# ====================================================================

def add_box(name, length_x, length_y, length_z, position, label=None):
    obj = assembly.addObject("Part::Box", name)
    obj.Length = length_x
    obj.Width = length_y
    obj.Height = length_z
    obj.Placement = App.Placement(position, App.Rotation())
    obj.Label = label or name
    return obj


def add_cyl_z(name, dia, height, position, label=None):
    obj = assembly.addObject("Part::Cylinder", name)
    obj.Radius = dia / 2.0
    obj.Height = height
    obj.Placement = App.Placement(position, App.Rotation())
    obj.Label = label or name
    return obj


def add_cyl_x(name, dia, length, start_position, label=None):
    """Parametric Part::Cylinder with axis along world +X.
    start_position is the world point at one end of the shaft.
    Native cylinder axis is local +Z. Rotate +90° about world +Y so
    local +Z → world +X (confirmed empirically vs add_link_axis_x)."""
    obj = assembly.addObject("Part::Cylinder", name)
    obj.Radius = dia / 2.0
    obj.Height = length
    obj.Placement = App.Placement(
        start_position, App.Rotation(Vector(0, 1, 0), 90)
    )
    obj.Label = label or name
    return obj


def make_rotation_from_basis(x_dir, y_dir, z_dir):
    """Build an App.Rotation mapping local +X → x_dir, +Y → y_dir, +Z → z_dir.
    Input vectors must be unit-length and mutually perpendicular."""
    m = App.Matrix()
    m.A11 = x_dir.x; m.A21 = x_dir.y; m.A31 = x_dir.z
    m.A12 = y_dir.x; m.A22 = y_dir.y; m.A32 = y_dir.z
    m.A13 = z_dir.x; m.A23 = z_dir.y; m.A33 = z_dir.z
    return App.Rotation(m)


def add_sphere(name, radius, position, label=None):
    obj = assembly.addObject("Part::Sphere", name)
    obj.Radius = radius
    obj.Placement = App.Placement(position, App.Rotation())
    obj.Label = label or name
    return obj


def add_link_axis_x(name, part_key, center_world, label=None):
    """App::Link to a parts/ body whose native axis is local +Z, placed
    so its axis runs along world +X with the part centered on `center_world`.
    Achieves this by rotating +90° about world +Y (maps local Z → world X)
    and shifting position so local-Z=H/2 lands at center_world.x."""
    h = native_h(part_key)
    link = assembly.addObject("App::Link", name)
    link.LinkedObject = PART_BODIES[part_key]
    base_pos = Vector(center_world.x - h / 2.0, center_world.y, center_world.z)
    link.Placement = App.Placement(base_pos, App.Rotation(Vector(0, 1, 0), 90))
    link.Label = label or name
    return link


def add_link_axis_z(name, part_key, position_world_base, label=None):
    """App::Link to a parts/ body whose native axis is local +Z, placed
    on world +Z with no rotation. `position_world_base` is the world
    location of the local origin (= the cylinder's BOTTOM face center)."""
    link = assembly.addObject("App::Link", name)
    link.LinkedObject = PART_BODIES[part_key]
    link.Placement = App.Placement(position_world_base, App.Rotation())
    link.Label = label or name
    return link


def _tangent_data(P1, R1, P2, R2):
    """For two coplanar circles in 2D (centers P1, P2 as 2-tuples; radii
    R1 > R2), return (T1u, T2u, T1l, T2l, mid1, mid2) — the four tangent
    points and the two far-side arc midpoints. All in the same 2D plane."""
    dx, dy = P2[0] - P1[0], P2[1] - P1[1]
    d = math.hypot(dx, dy)
    vx, vy = dx / d, dy / d                         # unit P1→P2
    nx, ny = -vy, vx                                # 90° CCW perpendicular
    sin_a = (R1 - R2) / d
    cos_a = math.sqrt(max(0.0, 1.0 - sin_a * sin_a))

    # u_upper = sin_a*v + cos_a*n ; u_lower = sin_a*v - cos_a*n
    ux_u = sin_a * vx + cos_a * nx
    uy_u = sin_a * vy + cos_a * ny
    ux_l = sin_a * vx - cos_a * nx
    uy_l = sin_a * vy - cos_a * ny

    T1u = (P1[0] + R1 * ux_u, P1[1] + R1 * uy_u)
    T2u = (P2[0] + R2 * ux_u, P2[1] + R2 * uy_u)
    T1l = (P1[0] + R1 * ux_l, P1[1] + R1 * uy_l)
    T2l = (P2[0] + R2 * ux_l, P2[1] + R2 * uy_l)
    mid1 = (P1[0] - R1 * vx, P1[1] - R1 * vy)        # far side from P2
    mid2 = (P2[0] + R2 * vx, P2[1] + R2 * vy)        # far side from P1
    return T1u, T2u, T1l, T2l, mid1, mid2


def _racetrack_wire_yz(P1, R1, P2, R2, x_const):
    """Build a closed racetrack Wire around two circles in the YZ plane
    at world X=x_const. Returns Part.Wire."""
    T1u, T2u, T1l, T2l, m1, m2 = _tangent_data(P1, R1, P2, R2)
    to3 = lambda yz: Vector(x_const, yz[0], yz[1])
    arc1 = Part.Arc(to3(T1u), to3(m1), to3(T1l)).toShape()
    line1 = Part.LineSegment(to3(T1l), to3(T2l)).toShape()
    arc2 = Part.Arc(to3(T2l), to3(m2), to3(T2u)).toShape()
    line2 = Part.LineSegment(to3(T2u), to3(T1u)).toShape()
    return Part.Wire([arc1, line1, arc2, line2])


def _racetrack_wire_xy(P1, R1, P2, R2, z_const):
    """Build a closed racetrack Wire around two circles in the XY plane
    at world Z=z_const. Returns Part.Wire."""
    T1u, T2u, T1l, T2l, m1, m2 = _tangent_data(P1, R1, P2, R2)
    to3 = lambda xy: Vector(xy[0], xy[1], z_const)
    arc1 = Part.Arc(to3(T1u), to3(m1), to3(T1l)).toShape()
    line1 = Part.LineSegment(to3(T1l), to3(T2l)).toShape()
    arc2 = Part.Arc(to3(T2l), to3(m2), to3(T2u)).toShape()
    line2 = Part.LineSegment(to3(T2u), to3(T1u)).toShape()
    return Part.Wire([arc1, line1, arc2, line2])


def _hollow_band_solid(outer_wire, inner_wire, extrude_vec):
    """Outer-minus-inner extrusion. Both wires must be coplanar and
    closed; extrude_vec is perpendicular to that plane."""
    outer_solid = Part.Face(outer_wire).extrude(extrude_vec)
    inner_solid = Part.Face(inner_wire).extrude(extrude_vec)
    return outer_solid.cut(inner_solid)


def add_chain_loop(name, label=None):
    """Build chain envelope: extruded racetrack ring in YZ plane at
    X = CHAIN_PLANE_X - CHAIN_EXTRUDE_X/2 (so it's centered on the
    chain plane), thickness CHAIN_BAND_RADIAL radially, width
    CHAIN_EXTRUDE_X axially along world X.
    Order P1 P2 with R1 > R2: chainring is P1, cog is P2."""
    P1 = (CRANK_Y, CRANK_Z)
    P2 = (JACKSHAFT_Y, JACKSHAFT_Z)
    R1 = CHAINRING_PITCH_R
    R2 = COG_PITCH_R
    x_face = CHAIN_PLANE_X - CHAIN_EXTRUDE_X / 2.0
    outer = _racetrack_wire_yz(P1, R1 + CHAIN_BAND_RADIAL / 2.0,
                               P2, R2 + CHAIN_BAND_RADIAL / 2.0, x_face)
    inner = _racetrack_wire_yz(P1, R1 - CHAIN_BAND_RADIAL / 2.0,
                               P2, R2 - CHAIN_BAND_RADIAL / 2.0, x_face)
    solid = _hollow_band_solid(outer, inner, Vector(CHAIN_EXTRUDE_X, 0, 0))
    obj = assembly.addObject("Part::Feature", name)
    obj.Shape = solid
    obj.Label = label or name
    return obj


def add_chain_link_array_along_wire(prefix, wire, plane_normal_dir,
                                     n_links_override=None):
    """Walk a closed wire (chain path) at chain_pitch arc-length steps and
    place a chain_link App::Link at each point with appropriate rotation.
    prefix:           name prefix (e.g., 'Chain1Link_'). Each link is named
                      prefix + zero-padded index.
    wire:             Part.Wire — typically built by the racetrack helpers.
    plane_normal_dir: Vector — unit normal of the chain plane (out-of-plane
                      direction). For a YZ-plane chain, pass Vector(1,0,0);
                      for an XY-plane chain, pass Vector(0,0,1).
    Returns the number of links placed."""
    total_length = wire.Length
    n_links = n_links_override or int(round(total_length / CHAIN_PITCH))
    # Discretize to n_links uniformly spaced points around the closed wire.
    points = wire.discretize(Number=n_links + 1)
    chain_part_body = PART_BODIES["chain_link"]

    for i in range(n_links):
        pos = points[i]
        nxt = points[(i + 1) % n_links]
        tangent = Vector(nxt.sub(pos))
        if tangent.Length < 1e-6:
            continue
        tangent.normalize()
        # Chain link local frame:
        #   +X = chain run direction (tangent)
        #   +Z = out-of-plane (= plane_normal_dir)
        #   +Y = +Z × +X (right-hand)
        z_dir = Vector(plane_normal_dir)
        z_dir.normalize()
        y_dir = z_dir.cross(tangent)
        y_dir.normalize()
        rot = make_rotation_from_basis(tangent, y_dir, z_dir)
        link = assembly.addObject("App::Link", f"{prefix}{i:03d}")
        link.LinkedObject = chain_part_body
        link.Placement = App.Placement(pos, rot)
    return n_links


def add_chain_loop_2(name, label=None):
    """Stage-2 chain envelope: extruded racetrack ring in XY plane at
    Z = CHAIN2_PLANE_Z, around stage2_large (P1) and stage2_pinion (P2).
    Both sprockets are on Z-axis shafts so the chain runs horizontally."""
    P1 = (BEVEL_OUT_SHAFT_X, BEVEL_OUT_SHAFT_Y)
    P2 = (DRIVE_X, BELT_CENTERLINE_Y)
    R1 = STAGE2_LARGE_PITCH_R
    R2 = STAGE2_PINION_PITCH_R
    z_face = CHAIN2_PLANE_Z - CHAIN_EXTRUDE_X / 2.0
    outer = _racetrack_wire_xy(P1, R1 + CHAIN_BAND_RADIAL / 2.0,
                               P2, R2 + CHAIN_BAND_RADIAL / 2.0, z_face)
    inner = _racetrack_wire_xy(P1, R1 - CHAIN_BAND_RADIAL / 2.0,
                               P2, R2 - CHAIN_BAND_RADIAL / 2.0, z_face)
    solid = _hollow_band_solid(outer, inner, Vector(0, 0, CHAIN_EXTRUDE_X))
    obj = assembly.addObject("Part::Feature", name)
    obj.Shape = solid
    obj.Label = label or name
    return obj


def add_belt_loop(name, label=None):
    """Build belt envelope: extruded racetrack ring in XY plane,
    centered vertically on Z = DESK_HEIGHT (extruded ± BELT_WIDTH/2).
    Drive pulley = P1 (larger); idler = P2."""
    P1 = (DRIVE_X, BELT_CENTERLINE_Y)
    P2 = (IDLER_X, BELT_CENTERLINE_Y)
    R1 = DRIVE_R
    R2 = IDLER_R
    z_face = DESK_HEIGHT - BELT_WIDTH / 2.0
    outer = _racetrack_wire_xy(P1, R1 + BELT_THICKNESS,
                               P2, R2 + BELT_THICKNESS, z_face)
    inner = _racetrack_wire_xy(P1, R1, P2, R2, z_face)
    solid = _hollow_band_solid(outer, inner, Vector(0, 0, BELT_WIDTH))
    obj = assembly.addObject("Part::Feature", name)
    obj.Shape = solid
    obj.Label = label or name
    return obj


def add_square_frustum_block(name, base_x, base_y, top_x, top_y,
                              height, center_xy, base_z, label=None):
    """Build a SQUARE PYRAMIDAL FRUSTUM (truncated rectangular pyramid) solid.
    Two horizontal rectangular wires are lofted: base at Z=base_z and top at
    Z=base_z+height, both centered on center_xy (X,Y).
    Wider base + narrower top — for the cast concrete BB-support block."""
    cx, cy = center_xy
    bhx = base_x / 2.0
    bhy = base_y / 2.0
    base_pts = [
        Vector(cx - bhx, cy - bhy, base_z),
        Vector(cx + bhx, cy - bhy, base_z),
        Vector(cx + bhx, cy + bhy, base_z),
        Vector(cx - bhx, cy + bhy, base_z),
        Vector(cx - bhx, cy - bhy, base_z),
    ]
    base_wire = Part.makePolygon(base_pts)

    thx = top_x / 2.0
    thy = top_y / 2.0
    top_z = base_z + height
    top_pts = [
        Vector(cx - thx, cy - thy, top_z),
        Vector(cx + thx, cy - thy, top_z),
        Vector(cx + thx, cy + thy, top_z),
        Vector(cx - thx, cy + thy, top_z),
        Vector(cx - thx, cy - thy, top_z),
    ]
    top_wire = Part.makePolygon(top_pts)
    solid = Part.makeLoft([base_wire, top_wire], True, False)  # solid=True, ruled=False
    obj = assembly.addObject("Part::Feature", name)
    obj.Shape = solid
    obj.Label = label or name
    return obj


def add_diagonal_brace(name, p_start, p_end, dia, label=None):
    """Cylindrical tube from p_start to p_end with given OD. Local Z
    axis maps to the (p_end - p_start) direction via a rotation derived
    from the FreeCAD Rotation(start, end) constructor — but for safety
    we compute the axis-angle ourselves from local +Z to the line dir."""
    direction = p_end.sub(p_start)
    length = direction.Length
    if length < 1e-6:
        raise RuntimeError(f"{name}: zero-length brace requested.")
    obj = assembly.addObject("Part::Cylinder", name)
    obj.Radius = dia / 2.0
    obj.Height = length
    # Rotation that maps local +Z to direction:
    rot = App.Rotation(Vector(0, 0, 1), direction)
    obj.Placement = App.Placement(p_start, rot)
    obj.Label = label or name
    return obj


# ====================================================================
# Build the assembly
# ====================================================================
App.Console.PrintMessage("Building assembly geometry...\n")

# --- Reference: rider seat ---
add_sphere("RiderSeatRef", 25.0, Vector(0, 0, 0),
           label="RiderSeatRef_origin_seat_a_school_chair_here")

# --- Desk plate ---
desk_z_bottom = DESK_HEIGHT - DESK_THICKNESS
add_box(
    "DeskPlate",
    DESK_WIDTH_X, DESK_DEPTH, DESK_THICKNESS,
    Vector(-DESK_WIDTH_X / 2.0, RIDER_SEAT_Y, desk_z_bottom),
    label=f"DeskPlate_{int(DESK_DEPTH)}x{int(DESK_WIDTH_X)}_top@{int(DESK_HEIGHT)}"
)

# --- Frame legs (4 corners; front face open for rider's legs) ---
leg_x_outer = DESK_WIDTH_X / 2.0 - LEG_INSET_FROM_EDGE - LEG_DIA / 2.0
leg_y_front = RIDER_SEAT_Y + LEG_INSET_FROM_EDGE
leg_y_back = RIDER_SEAT_Y + DESK_DEPTH - LEG_INSET_FROM_EDGE
leg_height = desk_z_bottom

for (lname, lx, ly) in [
    ("FrameLeg_FL", -leg_x_outer, leg_y_front),
    ("FrameLeg_FR", +leg_x_outer, leg_y_front),
    ("FrameLeg_BL", -leg_x_outer, leg_y_back),
    ("FrameLeg_BR", +leg_x_outer, leg_y_back),
]:
    add_cyl_z(lname, LEG_DIA, leg_height, Vector(lx, ly, 0),
              label=f"{lname}_floor_to_desk_underside")

# --- Frame top rails (back + L + R; front open for rider's legs) ---
rail_top_z = desk_z_bottom
rail_bottom_z = rail_top_z - RAIL_HEIGHT
back_rail_x_min = -leg_x_outer - LEG_DIA / 2.0
back_rail_x_max = +leg_x_outer + LEG_DIA / 2.0
back_rail_length = back_rail_x_max - back_rail_x_min
side_rail_y_min = leg_y_front - LEG_DIA / 2.0
side_rail_y_max = leg_y_back + LEG_DIA / 2.0
side_rail_length = side_rail_y_max - side_rail_y_min
back_rail_y = leg_y_back - RAIL_THICKNESS / 2.0

add_box(
    "FrameRail_Back",
    back_rail_length, RAIL_THICKNESS, RAIL_HEIGHT,
    Vector(back_rail_x_min, back_rail_y, rail_bottom_z),
    label="FrameRail_Back"
)
add_box(
    "FrameRail_Left",
    RAIL_THICKNESS, side_rail_length, RAIL_HEIGHT,
    Vector(-leg_x_outer - RAIL_THICKNESS / 2.0,
           side_rail_y_min, rail_bottom_z),
    label="FrameRail_Left"
)
add_box(
    "FrameRail_Right",
    RAIL_THICKNESS, side_rail_length, RAIL_HEIGHT,
    Vector(+leg_x_outer - RAIL_THICKNESS / 2.0,
           side_rail_y_min, rail_bottom_z),
    label="FrameRail_Right"
)

# --- Session 10: BB ground-anchored support (replaces Downtube_Brace) ---
# Four pieces — see constants block above for the engineering rationale:
#   (a) ConcreteBlock_Anchor — floor-resting block, post mounting plate sits on top
#   (b) GroundPost_Main      — fat 50mm post, block-top → above BB
#   (c) BB_SplitCollar       — clamp wrapping full BB shell circumference
#   (d) GroundPost_DiagonalStrut — diagonal post-base → BB front, makes a truss

# (a) Concrete block: pyramidal frustum, wider base, narrow top.
# Centered in X on post centerline (X=0), centered in Y on post centerline
# (Y = CRANK_Y + GROUND_POST_OFFSET_Y), sitting on floor.
block_center_y = CRANK_Y + GROUND_POST_OFFSET_Y
add_square_frustum_block(
    "ConcreteBlock_Anchor",
    CONCRETE_BLOCK_BASE_X, CONCRETE_BLOCK_BASE_Y,
    CONCRETE_BLOCK_TOP_X, CONCRETE_BLOCK_TOP_Y,
    CONCRETE_BLOCK_Z_HEIGHT,
    (0.0, block_center_y), 0.0,
    label=(
        f"ConcreteBlock_Anchor_cast_frustum_"
        f"base{int(CONCRETE_BLOCK_BASE_X)}x{int(CONCRETE_BLOCK_BASE_Y)}_"
        f"top{int(CONCRETE_BLOCK_TOP_X)}x{int(CONCRETE_BLOCK_TOP_Y)}_"
        f"h{int(CONCRETE_BLOCK_Z_HEIGHT)}_pedal_clearance_aware"
    )
)

# (b) Main vertical post: from block top up to past the BB.
post_top_z = CRANK_Z + GROUND_POST_TOP_Z_OVER_BB
post_height = post_top_z - CONCRETE_BLOCK_Z_HEIGHT
add_cyl_z(
    "GroundPost_Main",
    GROUND_POST_OD, post_height,
    Vector(0.0, block_center_y, CONCRETE_BLOCK_Z_HEIGHT),
    label=f"GroundPost_Main_OD{int(GROUND_POST_OD)}_h{int(post_height)}_steel_tube"
)

# (c) Split-collar clamp wrapping the BB shell. Modeled as a short cylinder
# along world X axis, centered on the BB axle. Real component is a two-piece
# bolted clamp; here it's a solid stand-in showing volume + position.
collar = assembly.addObject("Part::Cylinder", "BB_SplitCollar")
collar.Radius = BB_CLAMP_OD / 2.0
collar.Height = BB_CLAMP_LENGTH
# Rotate local +Z to world +X, then position so the collar is X-centered on 0
collar.Placement = App.Placement(
    Vector(-BB_CLAMP_LENGTH / 2.0, CRANK_Y, CRANK_Z),
    App.Rotation(Vector(0, 1, 0), 90)
)
collar.Label = f"BB_SplitCollar_OD{int(BB_CLAMP_OD)}_L{int(BB_CLAMP_LENGTH)}_wraps_full_shell"

# (d) Diagonal strut: from post base (at block-top height) up to a point
# 50mm forward of the BB axle. Forms a triangle with the vertical post —
# main post sees compression, strut sees tension, BB joint sees axial only.
strut_start = Vector(0.0, block_center_y, CONCRETE_BLOCK_Z_HEIGHT)
strut_end = Vector(0.0, CRANK_Y + STRUT_FORWARD_OFFSET_Y, CRANK_Z)
add_diagonal_brace(
    "GroundPost_DiagonalStrut", strut_start, strut_end, STRUT_OD,
    label=f"GroundPost_DiagonalStrut_OD{int(STRUT_OD)}_truss_anti_bending"
)

# --- Crank/BB shaft (App::Link, axis X) ---
# 140mm donor symbol. Will be visible at the ends where the crank arms
# attach (BB shell hides the middle portion).
add_link_axis_x(
    "CrankBB_ShaftLink", "crank_bb_shaft",
    Vector(0, CRANK_Y, CRANK_Z),
    label="CrankBB_ShaftLink_140mm_donor_stock_axis_X"
)

# --- BB shell (App::Link, axis X, wraps the BB shaft) ---
# Session-10 Phase-2: real BB housing — 68mm BSA-standard shell with
# 34mm ID bore. Bevel-shaped local +Z → world +X via -90° rotation about
# world +Y. Centered on the BB axle at (0, CRANK_Y, CRANK_Z).
bbshell_h = native_h("bb_shell")
bbshell_link = assembly.addObject("App::Link", "BBShell_Link")
bbshell_link.LinkedObject = PART_BODIES["bb_shell"]
bbshell_link.Placement = App.Placement(
    Vector(-bbshell_h / 2.0, CRANK_Y, CRANK_Z),
    App.Rotation(Vector(0, 1, 0), 90)  # +90° about +Y maps local +Z → world +X
)
bbshell_link.Label = f"BBShell_Link_BSA68mm_wraps_crank_axle"

# --- Jackshaft (parametric Part::Cylinder, axis X) ---
# Session-10 Phase-2: replaces the 150mm donor App::Link with a span-
# correct parametric cylinder. Runs from just inboard of the left
# pillow block (X=70) to just past the bevel input gear's back face
# (X=BEVEL_MEETING_X - BEVEL_LARGE_RADIUS = 275 plus a few mm of bearing
# seat margin). Uses intermediate_shaft_dia from the Bearings VarSet.
JACKSHAFT_LEFT_X = 70.0
JACKSHAFT_RIGHT_X = BEVEL_MEETING_X + 10.0  # past gear back face for bearing
JACKSHAFT_LEN = JACKSHAFT_RIGHT_X - JACKSHAFT_LEFT_X
JACKSHAFT_DIA = q(params.Bearings.intermediate_shaft_dia)
add_cyl_x(
    "Jackshaft_Link", JACKSHAFT_DIA, JACKSHAFT_LEN,
    Vector(JACKSHAFT_LEFT_X, JACKSHAFT_Y, JACKSHAFT_Z),
    label=(
        f"Jackshaft_parametric_OD{int(JACKSHAFT_DIA)}_"
        f"L{int(JACKSHAFT_LEN)}_X{int(JACKSHAFT_LEFT_X)}to{int(JACKSHAFT_RIGHT_X)}"
    )
)

# --- Chainring (App::Link, axis X, in chain plane) ---
add_link_axis_x(
    "Chainring_Link", "chainring",
    Vector(CHAIN_PLANE_X, CRANK_Y, CRANK_Z),
    label=f"Chainring_Link_42T_at_X{int(CHAIN_PLANE_X)}"
)

# --- Stage 1 cog (App::Link, axis X, in chain plane) ---
add_link_axis_x(
    "Stage1Cog_Link", "stage1_cog",
    Vector(CHAIN_PLANE_X, JACKSHAFT_Y, JACKSHAFT_Z),
    label=f"Stage1Cog_Link_13T_at_X{int(CHAIN_PLANE_X)}"
)

# --- Session 10 Q2 (real gears): visible bevel-gear pair via App::Link ---
# Both gears App::Link to parts/bevel_gear.FCStd (16T module-3 involute
# straight bevel — see macro 10). 1:1 ratio means both gears are identical;
# placement differs only in orientation.
#
# Source-part frame (bevel_gear.FCStd, reset_origin=True):
#   Local Z=0     large (outer/heel) face — at the local origin
#   Local Z=H     small (inner/toe) face  — at H = BEVEL_GEAR_HEIGHT (8)
#   Local Z=apex  extrapolated apex       — at BEVEL_GEAR_APEX_DISTANCE (24)
# We orient each gear so its apex sits on the world meeting point.

bevel_meeting_pt = Vector(BEVEL_MEETING_X, BEVEL_MEETING_Y, BEVEL_MEETING_Z)

# --- BevelGear_Input: cone axis along world +X (jackshaft direction) ---
# Apex points in +X (toward meeting_x). Body extends back in -X.
# Rotation: local +Z → world +X (= +90° about world +Y; Phase-3 fix).
bevel_input_link = assembly.addObject("App::Link", "BevelGear_Input")
bevel_input_link.LinkedObject = PART_BODIES["bevel_gear"]
bevel_input_link.Placement = App.Placement(
    Vector(BEVEL_MEETING_X - BEVEL_GEAR_APEX_DISTANCE,
           BEVEL_MEETING_Y, BEVEL_MEETING_Z),
    App.Rotation(Vector(0, 1, 0), 90)
)
bevel_input_link.Label = (
    f"BevelGear_Input_real_involute_16T_m{int(BEVEL_GEAR_MODULE)}_axisX_jackshaft"
)

# --- BevelGear_Output: cone axis along world +Z (vertical) ---
# Apex points in -Z (downward, toward meeting_z). Body extends UP in +Z
# from meeting_pt, so the vertical bevel-output shaft sits ABOVE the gear.
# Rotation: local +Z → world -Z  (= 180° rotation about world +X).
bevel_output_link = assembly.addObject("App::Link", "BevelGear_Output")
bevel_output_link.LinkedObject = PART_BODIES["bevel_gear"]
bevel_output_link.Placement = App.Placement(
    Vector(BEVEL_MEETING_X, BEVEL_MEETING_Y,
           BEVEL_MEETING_Z + BEVEL_GEAR_APEX_DISTANCE),
    App.Rotation(Vector(1, 0, 0), 180)
)
bevel_output_link.Label = (
    f"BevelGear_Output_real_involute_16T_m{int(BEVEL_GEAR_MODULE)}_axisZ_vert_shaft"
)

# --- Bevel-output vertical shaft (parametric Part::Cylinder, axis Z) ---
# Session-10 Phase-2: replaces 150mm donor stock with a span-correct
# parametric cylinder. Runs from 10 mm BELOW the bevel output gear's
# large face (Z = BEVEL_MEETING_Z + APEX_DISTANCE - 10) through and
# past stage2_large to a bearing seat above.
bevel_out_shaft_z_bot = BEVEL_MEETING_Z + BEVEL_GEAR_APEX_DISTANCE - 10.0
bevel_out_shaft_z_top = CHAIN2_PLANE_Z + 25.0
bevel_out_shaft_len = bevel_out_shaft_z_top - bevel_out_shaft_z_bot
add_cyl_z(
    "BevelOutputShaft_Link", JACKSHAFT_DIA, bevel_out_shaft_len,
    Vector(BEVEL_OUT_SHAFT_X, BEVEL_OUT_SHAFT_Y, bevel_out_shaft_z_bot),
    label=(
        f"BevelOutputShaft_parametric_OD{int(JACKSHAFT_DIA)}_"
        f"L{int(bevel_out_shaft_len)}_Z{int(bevel_out_shaft_z_bot)}to{int(bevel_out_shaft_z_top)}"
    )
)

# --- Stage 2 large sprocket (App::Link, axis Z, on bevel-output shaft) ---
stage2_large_z_base = CHAIN2_PLANE_Z - native_h("stage2_large") / 2.0
add_link_axis_z(
    "Stage2Large_Link", "stage2_large",
    Vector(BEVEL_OUT_SHAFT_X, BEVEL_OUT_SHAFT_Y, stage2_large_z_base),
    label=f"Stage2Large_Link_25T_axisZ_at_chain2_plane_Z{int(CHAIN2_PLANE_Z)}"
)

# --- Stage 2 pinion (App::Link, axis Z, on grinder shaft) ---
stage2_pinion_z_base = CHAIN2_PLANE_Z - native_h("stage2_pinion") / 2.0
add_link_axis_z(
    "Stage2Pinion_Link", "stage2_pinion",
    Vector(DRIVE_X, BELT_CENTERLINE_Y, stage2_pinion_z_base),
    label=f"Stage2Pinion_Link_8T_axisZ_at_chain2_plane_Z{int(CHAIN2_PLANE_Z)}"
)

# --- Vertical drive shaft (parametric Part::Cylinder, axis Z) ---
# Session-10 Phase-2: replaces 150mm donor stock. Spans below
# stage2_pinion (Z = CHAIN2_PLANE_Z - 20) to above the drive pulley top
# (Z = DESK_HEIGHT + PULLEY_FACE/2 + 25).
GRINDER_SHAFT_DIA = q(params.Bearings.grinder_shaft_dia)
vert_drive_z_bot = CHAIN2_PLANE_Z - 20.0
vert_drive_z_top = DESK_HEIGHT + PULLEY_FACE / 2.0 + 25.0
vert_drive_len = vert_drive_z_top - vert_drive_z_bot
add_cyl_z(
    "VerticalDriveShaft_Link", GRINDER_SHAFT_DIA, vert_drive_len,
    Vector(DRIVE_X, BELT_CENTERLINE_Y, vert_drive_z_bot),
    label=(
        f"VerticalDriveShaft_parametric_OD{int(GRINDER_SHAFT_DIA)}_"
        f"L{int(vert_drive_len)}_Z{int(vert_drive_z_bot)}to{int(vert_drive_z_top)}"
    )
)

# --- Drive pulley (App::Link, axis Z, straddles desk top) ---
# Native cylinder runs Z=0..PULLEY_FACE; place base so center sits on
# Z=DESK_HEIGHT (matches Session 8 placement convention).
add_link_axis_z(
    "DrivePulley_Link", "drive_pulley",
    Vector(DRIVE_X, BELT_CENTERLINE_Y, DESK_HEIGHT - PULLEY_FACE / 2.0),
    label=f"DrivePulley_Link_dia{int(DRIVE_PULLEY_DIA)}"
)

# --- Idler pulley (App::Link, axis Z, mirror at -X) ---
add_link_axis_z(
    "IdlerPulley_Link", "idler_pulley",
    Vector(IDLER_X, BELT_CENTERLINE_Y, DESK_HEIGHT - PULLEY_FACE / 2.0),
    label=f"IdlerPulley_Link_dia{int(IDLER_PULLEY_DIA)}"
)

# --- Idler shaft (App::Link, axis Z, supports idler pulley) ---
# 80mm shaft, centered on the pulley vertically (40mm above + below
# pulley center plane, which sits at Z=DESK_HEIGHT).
idler_shaft_h = native_h("idler_shaft")
add_link_axis_z(
    "IdlerShaft_Link", "idler_shaft",
    Vector(IDLER_X, BELT_CENTERLINE_Y, DESK_HEIGHT - idler_shaft_h / 2.0),
    label="IdlerShaft_Link_80mm_donor_stock_axis_Z"
)

# --- Chain 1 link array (replaces ChainLoop solid) ---
# Stage 1 chain runs in the YZ plane at X = CHAIN_PLANE_X around the
# chainring and stage1_cog. Build the pitch-circle racetrack wire as
# the chain's centerline path, then walk it placing chain_link instances.
chain1_wire = _racetrack_wire_yz(
    (CRANK_Y, CRANK_Z), CHAINRING_PITCH_R,
    (JACKSHAFT_Y, JACKSHAFT_Z), COG_PITCH_R,
    CHAIN_PLANE_X
)
chain1_count = add_chain_link_array_along_wire(
    "Chain1Link_", chain1_wire, Vector(1, 0, 0)
)
App.Console.PrintMessage(f"Chain 1: placed {chain1_count} chain links.\n")

# --- Chain 2 link array (replaces ChainLoop2 solid) ---
# Stage 2 chain runs in the XY plane at Z = CHAIN2_PLANE_Z.
chain2_wire = _racetrack_wire_xy(
    (BEVEL_OUT_SHAFT_X, BEVEL_OUT_SHAFT_Y), STAGE2_LARGE_PITCH_R,
    (DRIVE_X, BELT_CENTERLINE_Y), STAGE2_PINION_PITCH_R,
    CHAIN2_PLANE_Z
)
chain2_count = add_chain_link_array_along_wire(
    "Chain2Link_", chain2_wire, Vector(0, 0, 1)
)
App.Console.PrintMessage(f"Chain 2: placed {chain2_count} chain links.\n")

# --- Belt loop (visualization solid — kept; real flat belts are continuous) ---
add_belt_loop(
    "BeltLoop",
    label=f"BeltLoop_drive_to_idler_at_Z{int(DESK_HEIGHT)}"
)

# ====================================================================
# Session-10 Phase-2: crank arms + pedals + pillow blocks + bevel bracket
# ====================================================================

# --- Crank arms (App::Links at BB shaft ends, 180° opposed) ---
# crank_arm part: local origin = BB-end bore center; local +X = arm
# length direction; local +Z = arm thickness up.
# Crank arms attach AT THE BB AXLE ENDS (real cranks mount via square-
# taper / spline on the axle stubs that protrude beyond the BB shell).
# BB axle (crank_bb_shaft) is 140mm long centered at X=0, so axle ends
# are at X=±70. Phase-3 fix: was X=±44 (against the BB shell face),
# now X=±70 to match the axle.
left_crank_x = -70.0
right_crank_x = +70.0

# Left crank: local +X → world -Z. local +Y → world +Y. local +Z → world +X.
left_crank = assembly.addObject("App::Link", "CrankArmLeft_Link")
left_crank.LinkedObject = PART_BODIES["crank_arm"]
left_crank.Placement = App.Placement(
    Vector(left_crank_x, CRANK_Y, CRANK_Z),
    make_rotation_from_basis(
        Vector(0, 0, -1),  # +X → -Z (down)
        Vector(0, 1, 0),   # +Y → +Y
        Vector(1, 0, 0)    # +Z → +X
    )
)
left_crank.Label = "CrankArmLeft_170mm_pointing_down"

# Right crank: local +X → world +Z. local +Y → world +Y. local +Z → world -X.
right_crank = assembly.addObject("App::Link", "CrankArmRight_Link")
right_crank.LinkedObject = PART_BODIES["crank_arm"]
right_crank.Placement = App.Placement(
    Vector(right_crank_x, CRANK_Y, CRANK_Z),
    make_rotation_from_basis(
        Vector(0, 0, 1),    # +X → +Z (up)
        Vector(0, 1, 0),    # +Y → +Y
        Vector(-1, 0, 0)    # +Z → -X
    )
)
right_crank.Label = "CrankArmRight_170mm_pointing_up"

# --- Pedals (App::Links at crank-arm pedal-bore ends) ---
# crank_arm length = 170mm. Pedal sits at the far end of each crank.
# pedal part: local origin = spindle center, local +Y = spindle axis,
# local +X = platform extends in this direction, +Z = platform thickness.
CRANK_LEN = 170.0
# Pedal spindle center coincides with the crank-arm's pedal-bore so the
# spindle (25mm each side) passes through the crank-arm and the platform
# sits outboard. Phase-3 fix: was 30mm offset, gap was too large.
PEDAL_SPINDLE_REACH = 0.0

# Left pedal: at end of left crank, which is at world (left_crank_x - PEDAL_SPINDLE_REACH, CRANK_Y, CRANK_Z - CRANK_LEN)
# Spindle axis (local +Y) → world -X (outboard left). Platform (local +X) → world horizontal direction (let's pick world +Y, away from rider).
left_pedal = assembly.addObject("App::Link", "PedalLeft_Link")
left_pedal.LinkedObject = PART_BODIES["pedal"]
left_pedal.Placement = App.Placement(
    Vector(left_crank_x - PEDAL_SPINDLE_REACH, CRANK_Y, CRANK_Z - CRANK_LEN),
    make_rotation_from_basis(
        Vector(0, 1, 0),   # +X → +Y (platform extends forward)
        Vector(-1, 0, 0),  # +Y → -X (spindle axis outboard left)
        Vector(0, 0, 1)    # +Z → +Z
    )
)
left_pedal.Label = "PedalLeft_platform_spindle_outboard_left"

right_pedal = assembly.addObject("App::Link", "PedalRight_Link")
right_pedal.LinkedObject = PART_BODIES["pedal"]
right_pedal.Placement = App.Placement(
    Vector(right_crank_x + PEDAL_SPINDLE_REACH, CRANK_Y, CRANK_Z + CRANK_LEN),
    make_rotation_from_basis(
        Vector(0, 1, 0),   # +X → +Y (platform extends forward toward desk)
        Vector(1, 0, 0),   # +Y → +X (spindle axis outboard right)
        Vector(0, 0, -1)   # +Z → -Z  (right-handed: cross(+Y,+X)=-Z)
    )
)
right_pedal.Label = "PedalRight_platform_spindle_outboard_right"

# --- Pillow blocks ---
# pillow_block part: local +Z = shaft axis; base sits at local Z=0..BASE_H (=8mm).
# For X-axis shafts, rotate local +Z → world +X (= rotation about world +Y, -90°).
# For Z-axis shafts, no rotation needed.

def add_pillow_block_z(name, world_pos_base, label=None):
    """Pillow block with shaft axis along world +Z. world_pos_base = base
    plate's bottom face center in world coords."""
    obj = assembly.addObject("App::Link", name)
    obj.LinkedObject = PART_BODIES["pillow_block"]
    obj.Placement = App.Placement(world_pos_base, App.Rotation())
    obj.Label = label or name
    return obj


def add_pillow_block_x(name, world_pos_base_center, label=None):
    """Pillow block with shaft axis along world +X. world_pos_base_center =
    where the base-plate underside face center sits in world coords.
    Rotation +90° about world +Y maps local +Z → world +X (matches
    add_link_axis_x convention)."""
    obj = assembly.addObject("App::Link", name)
    obj.LinkedObject = PART_BODIES["pillow_block"]
    obj.Placement = App.Placement(
        world_pos_base_center, App.Rotation(Vector(0, 1, 0), 90)
    )
    obj.Label = label or name
    return obj


# Jackshaft pillow blocks (axis X). The pillow-block geometry occupies
# local Z=0..38 along the shaft axis; we want the bearing-bore center
# (at local Z = BASE_H + (BOSS_H - 11)/2 + 11/2 = 8 + 9.5 + 5.5 = 23
# approximately) to align with the jackshaft Y, Z position. Simplest:
# place the base center at (Jackshaft endpoint X, Y=400-25, Z=450-23)
# so the bearing bore goes through the shaft. For visual clarity we
# park the pillow blocks just outboard of where bearings would sit.
PILLOW_BORE_OFFSET = 23.0  # roughly center-of-bearing-bore from base
# Left jackshaft pillow block: base center at X = JACKSHAFT_LEFT_X - 5 (just outboard),
# YZ shifted so the bearing bore center aligns with the shaft.
add_pillow_block_x(
    "PillowBlock_Jackshaft_L",
    Vector(JACKSHAFT_LEFT_X, JACKSHAFT_Y, JACKSHAFT_Z - PILLOW_BORE_OFFSET),
    label="PillowBlock_Jackshaft_L_left_end_bearing_housing"
)
add_pillow_block_x(
    "PillowBlock_Jackshaft_R",
    Vector(JACKSHAFT_RIGHT_X - 38.0,  # base length is 38 along shaft axis
           JACKSHAFT_Y, JACKSHAFT_Z - PILLOW_BORE_OFFSET),
    label="PillowBlock_Jackshaft_R_right_end_bearing_housing"
)

# Bevel-output pillow blocks (axis Z)
add_pillow_block_z(
    "PillowBlock_BevelOut_Bot",
    Vector(BEVEL_OUT_SHAFT_X, BEVEL_OUT_SHAFT_Y, bevel_out_shaft_z_bot - 8.0),
    label="PillowBlock_BevelOut_Bot_below_bevel_gear"
)
add_pillow_block_z(
    "PillowBlock_BevelOut_Top",
    Vector(BEVEL_OUT_SHAFT_X, BEVEL_OUT_SHAFT_Y, bevel_out_shaft_z_top - 38.0),
    label="PillowBlock_BevelOut_Top_above_stage2_large"
)

# Grinder shaft pillow blocks (axis Z)
add_pillow_block_z(
    "PillowBlock_Grinder_Bot",
    Vector(DRIVE_X, BELT_CENTERLINE_Y, vert_drive_z_bot),
    label="PillowBlock_Grinder_Bot_below_stage2_pinion"
)
add_pillow_block_z(
    "PillowBlock_Grinder_Top",
    Vector(DRIVE_X, BELT_CENTERLINE_Y, vert_drive_z_top - 38.0),
    label="PillowBlock_Grinder_Top_above_drive_pulley"
)

# Idler shaft single pillow block at top (idler shaft is short, single bearing OK)
add_pillow_block_z(
    "PillowBlock_Idler_Top",
    Vector(IDLER_X, BELT_CENTERLINE_Y, DESK_HEIGHT + PULLEY_FACE / 2.0 + 5.0),
    label="PillowBlock_Idler_Top_above_pulley"
)

# --- Bevel mount bracket (App::Link) ---
# L-bracket tying the bevel-output shaft area to the back rail. Vertical
# leg next to the bevel-out shaft (X=BEVEL_OUT_SHAFT_X, Y just behind it),
# horizontal flange extending toward +Y to bolt to the back rail.
bevel_bracket_link = assembly.addObject("App::Link", "BevelMountBracket_Link")
bevel_bracket_link.LinkedObject = PART_BODIES["bevel_mount_bracket"]
# Bracket native frame: vertical leg along local +Z, flange along local +Y.
# Place vertical leg at (X=BEVEL_OUT_SHAFT_X, Y=BEVEL_OUT_SHAFT_Y + 15) so
# it sits 15mm behind the shaft. Base at Z=bevel_out_shaft_z_bot - 5.
bevel_bracket_link.Placement = App.Placement(
    Vector(BEVEL_OUT_SHAFT_X, BEVEL_OUT_SHAFT_Y + 15.0,
           bevel_out_shaft_z_bot - 5.0),
    App.Rotation()
)
bevel_bracket_link.Label = (
    "BevelMountBracket_L_bracket_vertical_leg_at_bevel_shaft_"
    "flange_toward_back_rail"
)

# --- Glass platen reference at desk's far edge ---
PLATEN_REF_X_LENGTH = MAX_GLASS_EDGE + 80.0
PLATEN_REF_Y_DEPTH = 50.8
PLATEN_REF_Z_THICKNESS = 1.0
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

# Verify drivetrain ratio still hits the 10:1 target after Session-10 changes
stage1_ratio = CHAINRING_TEETH / float(COG_TEETH)
bevel_ratio = 1.0  # 1:1 bevel pair
stage2_ratio = STAGE2_LARGE_TEETH / float(STAGE2_PINION_TEETH)
total_ratio = stage1_ratio * bevel_ratio * stage2_ratio
ratio_status = "OK" if abs(total_ratio - TOTAL_RATIO_TARGET) / TOTAL_RATIO_TARGET < 0.05 else "MISMATCH"
App.Console.PrintMessage(
    f"Drivetrain ratio check: stage1={stage1_ratio:.3f} × bevel={bevel_ratio:.2f} "
    f"× stage2={stage2_ratio:.3f} = {total_ratio:.3f}  "
    f"(target {TOTAL_RATIO_TARGET:.2f})  [{ratio_status}]\n"
)

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 08 (Session 10 Phase 2) complete. Real-geometry assembly\n"
    "with BB shell, crank arms, pedals, parametric shafts, bearings,\n"
    "real chain links, and gear-support brackets.\n"
    "================================================================\n"
    f"  WORLD FRAME (origin = rider seat on floor)\n"
    f"    rider_seat_y      = {RIDER_SEAT_Y:>8.1f} mm\n"
    f"    desk_depth        = {DESK_DEPTH:>8.1f} mm\n"
    f"    desk_height       = {DESK_HEIGHT:>8.1f} mm\n"
    f"    belt_centerline_y = {BELT_CENTERLINE_Y:>8.1f} mm\n"
    f"    chain_plane_x     = {CHAIN_PLANE_X:>8.1f} mm  (rider's right)\n"
    f"\n"
    f"  KEY POSITIONS (X, Y, Z) in mm — App::Linked parts in []\n"
    f"    rider seat ref   = (    0,     0,     0)\n"
    f"    crank/BB shaft   = (    0, {CRANK_Y:>5.0f}, {CRANK_Z:>5.0f}) axis=X  [crank_bb_shaft]\n"
    f"    jackshaft        = (X={JACKSHAFT_LEFT_X:>.0f}..{JACKSHAFT_RIGHT_X:>.0f}, Y={JACKSHAFT_Y:.0f}, Z={JACKSHAFT_Z:.0f}) axis=X  [parametric]\n"
    f"    chainring        = ({CHAIN_PLANE_X:>5.0f}, {CRANK_Y:>5.0f}, {CRANK_Z:>5.0f}) axis=X  [chainring]\n"
    f"    stage1 cog       = ({CHAIN_PLANE_X:>5.0f}, {JACKSHAFT_Y:>5.0f}, {JACKSHAFT_Z:>5.0f}) axis=X  [stage1_cog]\n"
    f"    bevel meeting pt = ({BEVEL_MEETING_X:>5.0f}, {BEVEL_MEETING_Y:>5.0f}, {BEVEL_MEETING_Z:>5.0f}) — apex of both bevel cones\n"
    f"    bevel-out shaft  = ({BEVEL_OUT_SHAFT_X:>5.0f}, {BEVEL_OUT_SHAFT_Y:>5.0f}, {bevel_out_shaft_z_bot:.0f}..{bevel_out_shaft_z_top:.0f}) axis=Z  [parametric]\n"
    f"    vertical drive shaft\n"
    f"                     = ({DRIVE_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {vert_drive_z_bot:.0f}..{vert_drive_z_top:.0f}) axis=Z  [parametric]\n"
    f"    drive pulley     = ({DRIVE_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z  [drive_pulley]\n"
    f"    idler pulley     = ({IDLER_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z  [idler_pulley]\n"
    f"    idler shaft      = ({IDLER_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z  [idler_shaft]\n"
    f"    glass platen ref = (X=±{PLATEN_REF_X_LENGTH/2.0:.0f}, Y={DESK_DEPTH:.0f}, Z={DESK_HEIGHT:.0f})\n"
    f"\n"
    f"  Belt span (drive↔idler CD): {BELT_CENTER_DISTANCE:.1f} mm  belt_width={BELT_WIDTH:.1f}\n"
    f"  Chain span (chainring↔cog): "
    f"{math.hypot(JACKSHAFT_Y-CRANK_Y, JACKSHAFT_Z-CRANK_Z):.1f} mm\n"
    "================================================================\n"
    "REMINDER: bevel gears are REAL INVOLUTE TEETH via freecad.gears workbench\n"
    "(macro 10 builds parts/bevel_gear.FCStd). Straight bevel, 16T module-3,\n"
    "45° pitch angle — both App::Links to the same source part (1:1 mesh).\n"
    "Shaft App::Links are 140-150mm donor-stock symbols — visible gaps\n"
    "between sprockets and shaft ends are intentional; real shafts get\n"
    "cut to assembly span at fabrication.\n"
    "----------------------------------------------------------------\n"
    f"  Session-10 Q2 — real bevel pair + restored stage 2 chain:\n"
    f"    BevelGear_Input         apex@({BEVEL_MEETING_X:.0f},{BEVEL_MEETING_Y:.0f},{BEVEL_MEETING_Z:.0f}) axisX  16T m{BEVEL_GEAR_MODULE:.1f} pitch_dia={BEVEL_GEAR_MODULE*BEVEL_GEAR_TEETH:.0f}\n"
    f"    BevelGear_Output        apex@({BEVEL_MEETING_X:.0f},{BEVEL_MEETING_Y:.0f},{BEVEL_MEETING_Z:.0f}) axisZ  16T m{BEVEL_GEAR_MODULE:.1f} pitch_dia={BEVEL_GEAR_MODULE*BEVEL_GEAR_TEETH:.0f}\n"
    f"    BevelOutputShaft_Link   12mm OD donor symbol  axisZ at (X={BEVEL_OUT_SHAFT_X:.0f}, Y={BEVEL_OUT_SHAFT_Y:.0f})\n"
    f"    Stage2Large_Link        25T  axisZ at (X={BEVEL_OUT_SHAFT_X:.0f}, Y={BEVEL_OUT_SHAFT_Y:.0f}, Z={CHAIN2_PLANE_Z:.0f})\n"
    f"    Stage2Pinion_Link       8T   axisZ at (X={DRIVE_X:.0f}, Y={BELT_CENTERLINE_Y:.0f}, Z={CHAIN2_PLANE_Z:.0f})\n"
    f"    ChainLoop2              horizontal at Z={CHAIN2_PLANE_Z:.0f}\n"
    f"    Drivetrain ratio        {stage1_ratio:.3f} × {bevel_ratio:.2f} × {stage2_ratio:.3f} = {total_ratio:.3f}  [{ratio_status}]\n"
    "----------------------------------------------------------------\n"
    f"  Session-10 BB ground support (cast frustum block + truss):\n"
    f"    ConcreteBlock_Anchor    base {CONCRETE_BLOCK_BASE_X:.0f}×{CONCRETE_BLOCK_BASE_Y:.0f}  top {CONCRETE_BLOCK_TOP_X:.0f}×{CONCRETE_BLOCK_TOP_Y:.0f}  h={CONCRETE_BLOCK_Z_HEIGHT:.0f}  (~32 kg cast)\n"
    f"    GroundPost_Main         OD={GROUND_POST_OD:.0f} h={post_top_z - CONCRETE_BLOCK_Z_HEIGHT:.0f}  at (X=0, Y={block_center_y:.0f})\n"
    f"    BB_SplitCollar          OD={BB_CLAMP_OD:.0f} L={BB_CLAMP_LENGTH:.0f}  wraps BB shell axis-X\n"
    f"    GroundPost_DiagonalStrut OD={STRUT_OD:.0f}  post-base → BB front  (truss)\n"
    "----------------------------------------------------------------\n"
    f"  Session-10 Phase-2 — gaps closed + gear supports:\n"
    f"    BBShell_Link            BSA 68mm wraps BB axle (real housing)\n"
    f"    CrankArmLeft/Right_Link  170mm cranks at BB ends, 180° opposed\n"
    f"    PedalLeft/Right_Link     90×60 flat pedals, spindles outboard ±X\n"
    f"    Jackshaft_Link           PARAMETRIC OD={JACKSHAFT_DIA:.0f}  L={JACKSHAFT_LEN:.0f}  X={JACKSHAFT_LEFT_X:.0f}..{JACKSHAFT_RIGHT_X:.0f}\n"
    f"    BevelOutputShaft_Link    PARAMETRIC OD={JACKSHAFT_DIA:.0f}  L={bevel_out_shaft_len:.0f}  Z={bevel_out_shaft_z_bot:.0f}..{bevel_out_shaft_z_top:.0f}\n"
    f"    VerticalDriveShaft_Link  PARAMETRIC OD={GRINDER_SHAFT_DIA:.0f}  L={vert_drive_len:.0f}  Z={vert_drive_z_bot:.0f}..{vert_drive_z_top:.0f}\n"
    f"    PillowBlock_Jackshaft    L+R (2)   axis X\n"
    f"    PillowBlock_BevelOut     Bot+Top (2) axis Z\n"
    f"    PillowBlock_Grinder      Bot+Top (2) axis Z\n"
    f"    PillowBlock_Idler        Top (1)   axis Z\n"
    f"    BevelMountBracket_Link   L-bracket tying bevel-out to back rail\n"
    f"    Chain1Link_NNN           {chain1_count} real chain links along stage-1 path\n"
    f"    Chain2Link_NNN           {chain2_count} real chain links along stage-2 path\n"
    "================================================================\n"
)
