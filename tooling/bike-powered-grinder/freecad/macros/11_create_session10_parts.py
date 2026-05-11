# -*- coding: utf-8 -*-
"""
11_create_session10_parts.py
============================

Builds the Phase-2 "gaps + supports" parts in one macro run:

    parts/bb_shell.FCStd            BB shell housing (hollow cylinder, axis X)
    parts/crank_arm.FCStd           170mm crank arm (BB end + pedal end)
    parts/pedal.FCStd               Flat pedal platform
    parts/pillow_block.FCStd        Generic bearing pillow block w/ bolt holes
    parts/bevel_mount_bracket.FCStd L-bracket tying bevel-out shaft to frame
    parts/chain_link.FCStd          Single chain-link unit (2 plates + roller)

All parts use a baked-Shape Part::Feature (no PartDesign Proxy), so the
saved files are self-contained and App::Link consumers don't need any
addon beyond plain FreeCAD.

Coordinates: every part is built in its OWN local frame with the
"natural" axis along local +Z when applicable, matching the convention
the assembly's add_link_axis_x / add_link_axis_z helpers already expect.

Idempotent: each part file is wiped and rebuilt on every run.
"""

import os
import math
import FreeCAD as App
import Part
from FreeCAD import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
FREECAD_DIR = os.path.dirname(HERE)
PARTS_DIR = os.path.join(FREECAD_DIR, "parts")


def write_part(part_name, body_name, label, shape):
    """Open or create parts/<part_name>.FCStd, wipe contents, place the
    given Part.Shape into a Part::Feature with `body_name`/`label`, save."""
    part_path = os.path.join(PARTS_DIR, f"{part_name}.FCStd")
    if part_name in App.listDocuments():
        App.closeDocument(part_name)
    if os.path.exists(part_path):
        doc = App.openDocument(part_path)
        for o in list(doc.Objects):
            try:
                doc.removeObject(o.Name)
            except Exception:
                pass
    else:
        doc = App.newDocument(part_name)
    obj = doc.addObject("Part::Feature", body_name)
    obj.Shape = shape
    obj.Label = label
    doc.recompute()
    if doc.FileName:
        doc.save()
    else:
        doc.saveAs(part_path)
    App.Console.PrintMessage(
        f"Wrote {part_path} (volume={shape.Volume:.1f} mm^3, "
        f"bbox X[{shape.BoundBox.XMin:.1f},{shape.BoundBox.XMax:.1f}] "
        f"Y[{shape.BoundBox.YMin:.1f},{shape.BoundBox.YMax:.1f}] "
        f"Z[{shape.BoundBox.ZMin:.1f},{shape.BoundBox.ZMax:.1f}])\n"
    )
    App.closeDocument(part_name)


# ====================================================================
# 1) BB SHELL — hollow cylinder, axis local +Z
#    English-standard BSA: 68 mm width × 40 mm OD × 34 mm ID.
#    In the assembly this part rotates so local +Z → world +X.
# ====================================================================
def build_bb_shell():
    OD, ID, L = 40.0, 34.0, 68.0
    outer = Part.makeCylinder(OD / 2.0, L)
    bore = Part.makeCylinder(ID / 2.0, L + 2.0, Vector(0, 0, -1))
    shape = outer.cut(bore)
    write_part(
        "bb_shell", "BBShellBody",
        f"BBShellBody_BSA_L{int(L)}mm_OD{int(OD)}_ID{int(ID)}",
        shape
    )


# ====================================================================
# 2) CRANK ARM — 170mm lever between BB and pedal
#    Local origin = center of BB-end bore. Length runs along local +X
#    (so when App::Linked at the BB shaft's end, the arm extends radially
#    in world XY/YZ depending on rotation).
#    Modeled as: flat bar 170 × 25 × 10 with a 14 mm hole at the BB end
#    (square-taper-ish placeholder) and a 9 mm hole at the pedal end.
# ====================================================================
def build_crank_arm():
    LEN, W, T = 170.0, 25.0, 10.0
    BB_HOLE = 14.0
    PEDAL_HOLE = 9.0
    # Bar from local (-W/2, -W/2, 0) to (LEN+W/2, +W/2, T) but with
    # rounded ends. Simplest: extrude a 2D wire with end fillets.
    # Even simpler: union a center rectangle with two end disks.
    body = Part.makeBox(LEN, W, T, Vector(0, -W / 2.0, 0))
    disc_bb = Part.makeCylinder(W / 2.0, T, Vector(0, 0, 0))
    disc_pedal = Part.makeCylinder(W / 2.0, T, Vector(LEN, 0, 0))
    bar = body.fuse([disc_bb, disc_pedal]).removeSplitter()
    # Drill the holes
    bb_bore = Part.makeCylinder(
        BB_HOLE / 2.0, T + 2.0, Vector(0, 0, -1)
    )
    pedal_bore = Part.makeCylinder(
        PEDAL_HOLE / 2.0, T + 2.0, Vector(LEN, 0, -1)
    )
    shape = bar.cut([bb_bore, pedal_bore])
    write_part(
        "crank_arm", "CrankArmBody",
        f"CrankArmBody_L{int(LEN)}_W{int(W)}_T{int(T)}_BB{int(BB_HOLE)}_pedal{int(PEDAL_HOLE)}",
        shape
    )


# ====================================================================
# 3) PEDAL — flat pedal platform
#    Local origin = center of the pedal spindle bore. Platform extends
#    along local +X (away from the crank arm).
#    Spindle bore axis = local +Y. Platform: 90 × 60 × 12 plate.
# ====================================================================
def build_pedal():
    PLAT_X, PLAT_Y, PLAT_T = 90.0, 60.0, 12.0
    SPINDLE_OD = 14.0  # boss around the spindle
    SPINDLE_BORE = 9.0
    SPINDLE_L = 25.0   # spindle length on each side of the boss
    # Platform centered around (X=PLAT_X/2, 0, 0), axis-aligned
    plate = Part.makeBox(
        PLAT_X, PLAT_Y, PLAT_T,
        Vector(0, -PLAT_Y / 2.0, -PLAT_T / 2.0)
    )
    # Spindle boss (axis along local +Y, through plate's near edge)
    boss = Part.makeCylinder(
        SPINDLE_OD / 2.0, SPINDLE_L * 2.0,
        Vector(0, -SPINDLE_L, 0),
        Vector(0, 1, 0)
    )
    # Spindle bore through the boss
    bore = Part.makeCylinder(
        SPINDLE_BORE / 2.0, SPINDLE_L * 2.0 + 2.0,
        Vector(0, -SPINDLE_L - 1.0, 0),
        Vector(0, 1, 0)
    )
    shape = plate.fuse(boss).cut(bore).removeSplitter()
    write_part(
        "pedal", "PedalBody",
        f"PedalBody_platform_{int(PLAT_X)}x{int(PLAT_Y)}_spindleBore{int(SPINDLE_BORE)}",
        shape
    )


# ====================================================================
# 4) PILLOW BLOCK — parametric bearing housing with bolt-hole pattern
#    Local frame: shaft axis is local +Z (goes through the bearing bore).
#    Base sits in local XY plane (bolted down). Bolt-hole pattern at the
#    corners of the base footprint.
#    Geometry:
#      - base footprint:    BASE_X × BASE_Y rectangle
#      - boss above base:   cylinder around the shaft, BORE_OD ID
#      - bolt holes:        4 holes at the base corners
#    Default: sized for 12mm bearing housing on a 35mm OD bearing
#    (6202-2RS), with M5 bolt holes 70mm × 30mm pattern.
# ====================================================================
def build_pillow_block():
    BORE = 12.0       # default — matches intermediate_shaft
    BEARING_OD = 35.0 # 6202-2RS OD (housing seat)
    BASE_X = 70.0
    BASE_Y = 50.0
    BASE_H = 8.0      # base plate thickness
    BOSS_H = 30.0     # height of bearing-housing boss above base
    BOLT_HOLE = 5.5   # clearance for M5
    BOLT_SPAN_X = 55.0
    BOLT_SPAN_Y = 35.0
    # Base plate
    base = Part.makeBox(
        BASE_X, BASE_Y, BASE_H,
        Vector(-BASE_X / 2.0, -BASE_Y / 2.0, 0)
    )
    # Boss above base, centered on origin
    boss_outer_dia = BEARING_OD + 8.0   # 4mm wall around bearing
    boss = Part.makeCylinder(
        boss_outer_dia / 2.0, BOSS_H, Vector(0, 0, BASE_H)
    )
    body = base.fuse(boss).removeSplitter()
    # Shaft bore through the whole thing (along +Z)
    shaft_bore = Part.makeCylinder(
        BORE / 2.0, BASE_H + BOSS_H + 2.0, Vector(0, 0, -1)
    )
    # Bearing seat: counter-bore from the top down BEARING_W=11mm
    bearing_seat = Part.makeCylinder(
        BEARING_OD / 2.0, 11.0,
        Vector(0, 0, BASE_H + BOSS_H - 11.0)
    )
    # 4 bolt holes through the base
    bolt_holes = []
    for sx in (-1, +1):
        for sy in (-1, +1):
            bolt_holes.append(
                Part.makeCylinder(
                    BOLT_HOLE / 2.0, BASE_H + 2.0,
                    Vector(sx * BOLT_SPAN_X / 2.0,
                           sy * BOLT_SPAN_Y / 2.0,
                           -1.0)
                )
            )
    shape = body.cut([shaft_bore, bearing_seat] + bolt_holes)
    write_part(
        "pillow_block", "PillowBlockBody",
        f"PillowBlockBody_bore{int(BORE)}_bearing{int(BEARING_OD)}_M5x4",
        shape
    )


# ====================================================================
# 5) BEVEL MOUNT BRACKET — L-bracket tying bevel-output pillow blocks
#    to the desk back rail. Vertical leg holds the pillow blocks;
#    horizontal leg bolts to the rail underside.
#    Local frame: vertical leg along local +Z, horizontal leg along +Y.
# ====================================================================
def build_bevel_mount_bracket():
    H_VERTICAL = 200.0     # height of vertical leg
    H_HORIZONTAL = 80.0    # length of horizontal flange (Y extent)
    W = 80.0               # width (X extent — perpendicular to chain plane)
    T = 6.0                # plate thickness (sheet steel)
    BOLT_HOLE = 5.5
    # Vertical leg: a thin box standing along +Z
    vert = Part.makeBox(W, T, H_VERTICAL,
                        Vector(-W / 2.0, -T / 2.0, 0))
    # Horizontal flange at top: box extending in +Y
    horiz = Part.makeBox(W, H_HORIZONTAL, T,
                         Vector(-W / 2.0, T / 2.0, H_VERTICAL - T))
    body = vert.fuse(horiz).removeSplitter()
    # 4 bolt holes through the horizontal flange (mount to rail underside)
    hole_z_top = H_VERTICAL  # holes drilled through the flange from above
    holes = []
    for sx in (-1, +1):
        for fy in (20.0, H_HORIZONTAL - 20.0):
            holes.append(
                Part.makeCylinder(
                    BOLT_HOLE / 2.0, T + 2.0,
                    Vector(sx * (W / 2.0 - 15.0),
                           T / 2.0 + fy,
                           hole_z_top - T - 1.0)
                )
            )
    # Plus 4 bolt holes in the vertical leg for attaching pillow blocks
    for fz in (40.0, 160.0):
        for sx in (-1, +1):
            holes.append(
                Part.makeCylinder(
                    BOLT_HOLE / 2.0, T + 2.0,
                    Vector(sx * (W / 2.0 - 15.0),
                           -T / 2.0 - 1.0, fz),
                    Vector(0, 1, 0)
                )
            )
    shape = body.cut(holes)
    write_part(
        "bevel_mount_bracket", "BevelMountBracketBody",
        f"BevelMountBracketBody_L_h{int(H_VERTICAL)}_flange{int(H_HORIZONTAL)}_M5",
        shape
    )


# ====================================================================
# 6) CHAIN LINK — single chain-link unit (one pitch span)
#    A bicycle chain alternates inner/outer plate pairs at half-pitch
#    spacing. For visualization we use a simplified one-pitch unit
#    consisting of two side plates (figure-8 profile flattened to
#    rounded-rectangle) and a roller at one end. When App::Linked at
#    every other half-pitch along the chain path, the array reads as
#    a real chain at viewing distance.
#
#    Local frame: chain runs along local +X (between pitches).
#                 plates lie in the XY plane (Y = side direction).
#                 roller axis is local +Y.
#    Dimensions: 12.7 mm pitch (= CHAIN_PITCH); plate ~3.7 × 8 × 0.8 mm;
#                roller OD ~7.75 mm × W ~5 mm.
# ====================================================================
def build_chain_link():
    PITCH = 12.7
    PLATE_THICK = 0.8
    PLATE_HEIGHT = 8.0
    PLATE_GAP = 5.0   # inside width between plates (roller fits here)
    ROLLER_OD = 7.75
    ROLLER_W = 5.0
    PIN_OD = 3.66
    # Build one side plate as a rounded rectangle (capsule shape):
    # rectangle (PITCH × PLATE_HEIGHT) + half-disks at each end.
    rect = Part.makeBox(PITCH, PLATE_HEIGHT, PLATE_THICK,
                        Vector(0, -PLATE_HEIGHT / 2.0, 0))
    end1 = Part.makeCylinder(
        PLATE_HEIGHT / 2.0, PLATE_THICK, Vector(0, 0, 0)
    )
    end2 = Part.makeCylinder(
        PLATE_HEIGHT / 2.0, PLATE_THICK, Vector(PITCH, 0, 0)
    )
    plate_outer = rect.fuse([end1, end2]).removeSplitter()
    # Plate has two pin holes
    hole1 = Part.makeCylinder(PIN_OD / 2.0, PLATE_THICK + 2.0,
                              Vector(0, 0, -1))
    hole2 = Part.makeCylinder(PIN_OD / 2.0, PLATE_THICK + 2.0,
                              Vector(PITCH, 0, -1))
    plate = plate_outer.cut([hole1, hole2])
    # Two plates: one at Y = -(PLATE_GAP/2 + PLATE_THICK), one at +(...)
    plate_left = plate.copy()
    plate_left.translate(Vector(0, -(PLATE_GAP / 2.0 + PLATE_THICK / 2.0), 0))
    plate_right = plate.copy()
    plate_right.translate(Vector(0, +(PLATE_GAP / 2.0 + PLATE_THICK / 2.0), 0))
    # Roller (axis local +Y) at the leading pitch endpoint
    roller_axis_y = 0.0
    roller = Part.makeCylinder(
        ROLLER_OD / 2.0, ROLLER_W,
        Vector(0, -ROLLER_W / 2.0, 0),
        Vector(0, 1, 0)
    )
    # Pin (axis local +Y) at leading pitch endpoint
    pin = Part.makeCylinder(
        PIN_OD / 2.0, PLATE_GAP + 2 * PLATE_THICK,
        Vector(0, -(PLATE_GAP / 2.0 + PLATE_THICK), 0),
        Vector(0, 1, 0)
    )
    shape = plate_left.fuse([plate_right, roller, pin]).removeSplitter()
    write_part(
        "chain_link", "ChainLinkBody",
        f"ChainLinkBody_pitch{PITCH}_h{PLATE_HEIGHT}_rollerOD{ROLLER_OD}",
        shape
    )


# ====================================================================
# Build all the parts
# ====================================================================

App.Console.PrintMessage("Building Session-10 Phase-2 parts...\n")
build_bb_shell()
build_crank_arm()
build_pedal()
build_pillow_block()
build_bevel_mount_bracket()
build_chain_link()
App.Console.PrintMessage("All six parts written to parts/.\n")
