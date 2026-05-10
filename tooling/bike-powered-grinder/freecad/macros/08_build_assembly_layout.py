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

# Platen
MAX_GLASS_EDGE = q(params.Platen.max_glass_edge)

# Derived
DRIVE_R = DRIVE_PULLEY_DIA / 2.0
IDLER_R = IDLER_PULLEY_DIA / 2.0
DRIVE_X = +BELT_CENTER_DISTANCE / 2.0
IDLER_X = -BELT_CENTER_DISTANCE / 2.0
CHAINRING_PITCH_R = CHAIN_PITCH / (2.0 * math.sin(math.pi / CHAINRING_TEETH))
COG_PITCH_R = CHAIN_PITCH / (2.0 * math.sin(math.pi / COG_TEETH))


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
    "drive_pulley":       ("drive_pulley.FCStd",       "PulleyBody",           60.0),
    "idler_pulley":       ("idler_pulley.FCStd",       "IdlerBody",            60.0),
    "crank_bb_shaft":     ("crank_bb_shaft.FCStd",     "CrankBBShaftBody",    140.0),
    "intermediate_shaft": ("intermediate_shaft.FCStd", "IntermediateShaftBody", 150.0),
    "grinder_shaft":      ("grinder_shaft.FCStd",      "GrinderShaftBody",    150.0),
    "idler_shaft":        ("idler_shaft.FCStd",        "IdlerShaftBody",       80.0),
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

# Right-angle drive placeholder block dims
RA_DRIVE_X_HALF = 60.0
RA_DRIVE_Z_HEIGHT = 100.0
RA_DRIVE_Z_BOTTOM = JACKSHAFT_Z - RA_DRIVE_Z_HEIGHT / 2.0

# Diagonal "downtube" brace — TODO: promote to Frame VarSet on donor pick
DOWNTUBE_OUTER_DIA = 30.0          # typical donor-bike downtube OD
DOWNTUBE_ATTACH_OFFSET_FROM_BACK = 25.0  # back-rail centerline distance from back-leg edge

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
    "Downtube_Brace",
    "GlassPlatenRef",

    # Right-angle drive placeholder block
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

    # Loops
    "ChainLoop",
    "BeltLoop",

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

# --- Diagonal brace (BB area → back rail centerline) ---
# Single tube, X=0 centerline. Carries pedal-load bending forces from
# the BB up into the rear of the frame structure. Donor-bike-typical OD
# (~30 mm) and length determined by start/end points; if a real donor
# is selected, swap dimensions and the geometry follows.
brace_start = Vector(0, CRANK_Y, CRANK_Z)
brace_end = Vector(0,
                   leg_y_back + LEG_DIA / 2.0,
                   rail_bottom_z + RAIL_HEIGHT / 2.0)
add_diagonal_brace(
    "Downtube_Brace", brace_start, brace_end, DOWNTUBE_OUTER_DIA,
    label="Downtube_Brace_BB_to_BackRail_donor_bike_OD"
)

# --- Crank/BB shaft (App::Link, axis X) ---
add_link_axis_x(
    "CrankBB_ShaftLink", "crank_bb_shaft",
    Vector(0, CRANK_Y, CRANK_Z),
    label="CrankBB_ShaftLink_140mm_donor_stock_axis_X"
)

# --- Jackshaft (App::Link, axis X) ---
# Anchored so its left end sits at the chain plane; the 150mm part
# extends rightward toward the bevel gearbox column. Real shaft will be
# cut to assembly span; this is donor-stock symbol only.
js_left_x = CHAIN_PLANE_X
js_center_x = js_left_x + native_h("intermediate_shaft") / 2.0
add_link_axis_x(
    "Jackshaft_Link", "intermediate_shaft",
    Vector(js_center_x, JACKSHAFT_Y, JACKSHAFT_Z),
    label="Jackshaft_Link_150mm_donor_stock_axis_X_anchored_at_chain_plane"
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

# --- Right-angle drive placeholder block ---
ra_y_min = min(JACKSHAFT_Y, BELT_CENTERLINE_Y)
ra_y_max = max(JACKSHAFT_Y, BELT_CENTERLINE_Y)
ra_y_depth = (ra_y_max - ra_y_min) + 40.0
add_box(
    "RA_Drive_Placeholder",
    RA_DRIVE_X_HALF * 2.0, ra_y_depth, RA_DRIVE_Z_HEIGHT,
    Vector(DRIVE_X - RA_DRIVE_X_HALF,
           ra_y_min - 20.0,
           RA_DRIVE_Z_BOTTOM),
    label="RA_Drive_PLACEHOLDER_BevelGearOrSpiralBevel_TBD_spec_required"
)

# --- Vertical drive shaft (App::Link, axis Z) ---
# Anchored at JACKSHAFT_Z (bevel-box output level), extends 150 mm up.
# Falls short of belt plane (Z=DESK_HEIGHT) — gap is intentional;
# real shaft will be cut to length when fabricated.
add_link_axis_z(
    "VerticalDriveShaft_Link", "grinder_shaft",
    Vector(DRIVE_X, BELT_CENTERLINE_Y, JACKSHAFT_Z),
    label="VerticalDriveShaft_Link_150mm_donor_stock_axis_Z"
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

# --- Chain loop (visualization solid) ---
add_chain_loop(
    "ChainLoop",
    label=f"ChainLoop_chainring_to_stage1_cog_at_X{int(CHAIN_PLANE_X)}"
)

# --- Belt loop (visualization solid) ---
add_belt_loop(
    "BeltLoop",
    label=f"BeltLoop_drive_to_idler_at_Z{int(DESK_HEIGHT)}"
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

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 08 (Session 9) complete. Assembly built with App::Linked\n"
    "real parts, chain + belt loop solids, and diagonal brace.\n"
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
    f"    jackshaft        = ({js_center_x:>5.0f}, {JACKSHAFT_Y:>5.0f}, {JACKSHAFT_Z:>5.0f}) axis=X  [intermediate_shaft]\n"
    f"    chainring        = ({CHAIN_PLANE_X:>5.0f}, {CRANK_Y:>5.0f}, {CRANK_Z:>5.0f}) axis=X  [chainring]\n"
    f"    stage1 cog       = ({CHAIN_PLANE_X:>5.0f}, {JACKSHAFT_Y:>5.0f}, {JACKSHAFT_Z:>5.0f}) axis=X  [stage1_cog]\n"
    f"    RA-drive (placeholder housing center)\n"
    f"                     = ({DRIVE_X:>5.0f}, {(JACKSHAFT_Y + BELT_CENTERLINE_Y) / 2.0:>5.0f}, {JACKSHAFT_Z:>5.0f})\n"
    f"    vertical drive shaft\n"
    f"                     = ({DRIVE_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {JACKSHAFT_Z:>5.0f}..{JACKSHAFT_Z + 150:.0f}) axis=Z  [grinder_shaft]\n"
    f"    drive pulley     = ({DRIVE_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z  [drive_pulley]\n"
    f"    idler pulley     = ({IDLER_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z  [idler_pulley]\n"
    f"    idler shaft      = ({IDLER_X:>5.0f}, {BELT_CENTERLINE_Y:>5.0f}, {DESK_HEIGHT:>5.0f}) axis=Z  [idler_shaft]\n"
    f"    glass platen ref = (X=±{PLATEN_REF_X_LENGTH/2.0:.0f}, Y={DESK_DEPTH:.0f}, Z={DESK_HEIGHT:.0f})\n"
    f"\n"
    f"  Belt span (drive↔idler CD): {BELT_CENTER_DISTANCE:.1f} mm  belt_width={BELT_WIDTH:.1f}\n"
    f"  Chain span (chainring↔cog): "
    f"{math.hypot(JACKSHAFT_Y-CRANK_Y, JACKSHAFT_Z-CRANK_Z):.1f} mm\n"
    "================================================================\n"
    "REMINDER: RA_Drive_Placeholder is a SPATIAL RESERVATION + LABEL.\n"
    "Real bevel/spiral-bevel right-angle gearbox still to be spec'd.\n"
    "Shaft App::Links are 140-150mm donor-stock symbols — visible gaps\n"
    "between sprockets and shaft ends are intentional; real shafts get\n"
    "cut to assembly span at fabrication.\n"
    "================================================================\n"
)
