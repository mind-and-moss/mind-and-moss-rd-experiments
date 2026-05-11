# -*- coding: utf-8 -*-
"""
10_create_bevel_gear_part.py
============================

Builds parts/bevel_gear.FCStd — a REAL involute-toothed bevel gear,
3D-printable, replacing the cone-frustum placeholders from Session 10 Q2.

Why a real gear and not a placeholder?
--------------------------------------
Isaiah's call (Session 10, post-Q2 clarification): "I thought we were
doing a gear system... eventually we're going to be 3D printing this in
real life, and I want it to work well." So this part is the actual
machine geometry, not a visualization stand-in.

Tool used: freecad.gears workbench (looooo/freecad.gears), cloned into
the user's FreeCAD Mod folder. The macro extends freecad.__path__ at
runtime so the workbench is importable in headless freecadcmd.exe.

Gear spec (1:1 — both gears identical, same FCStd App::Linked twice):
  module          = 3.0 mm   (chosen for 3D-printability on Bambu A1 Mini,
                              0.4mm nozzle — tooth thickness ~4.7mm)
  num_teeth       = 16       (small but printable; 1:1 mesh symmetric)
  pitch_dia       = 48 mm    (module × num_teeth)
  pitch_angle     = 45°      (cone half-angle — 1:1 bevel mesh at 90°)
  pressure_angle  = 20°      (standard involute)
  height          = 8 mm     (face width)
  backlash        = 0.10 mm  (printed-gear allowance)
  clearance       = 0.1      (top-land/root clearance fraction)
  beta            = 0°       (STRAIGHT bevel — not spiral. Easier print.)

Output orientation (freecad.gears with reset_origin=True):
  Local Z=0       large (outer/heel) face at the local origin
  Local Z=+8      small (inner/toe) face
  Local Z=+24     extrapolated apex (= pitch_dia/2/tan(pitch_angle))
  Cone axis       local +Z

Shape baking: after recompute, the gear's Shape is extracted and copied
into a plain Part::Feature so the saved FCStd has no dependency on the
freecad.gears Proxy class. App::Link consumers in macro 08 don't need
the workbench installed.

PRINTABILITY NOTES
==================
- Straight (non-spiral) bevel teeth print well on FDM with the cone axis
  vertical to the build plate. Supports needed only on the underside of
  the outer rim.
- Tooth thickness at the small end is ~module × (1 - height/pitch_dia *
  tan(pitch_angle)) ≈ 1.9 mm — printable with a 0.4 mm nozzle.
- For 16T at module 3, addendum diameter ~ 54 mm, fits the A1 Mini's
  180 × 180 mm bed easily.
"""

import os
import sys

# ----------------------------------------------------------------
# Bootstrap freecad.gears workbench into the path (headless-safe)
# ----------------------------------------------------------------
GEARS_ROOT = r"C:\Users\Isaia\AppData\Roaming\FreeCAD\Mod\freecad.gears"
if GEARS_ROOT not in sys.path:
    sys.path.insert(0, GEARS_ROOT)

import FreeCAD as App  # noqa: E402
import Part  # noqa: E402

if "freecad" in sys.modules:
    _fc = sys.modules["freecad"]
    _gears_path = os.path.join(GEARS_ROOT, "freecad")
    if _gears_path not in _fc.__path__:
        _fc.__path__.append(_gears_path)

from freecad.gears.bevelgear import BevelGear  # noqa: E402

# Bore size: drilled through the gear's axis so the shaft can pass.
# Matches the 12 mm intermediate_shaft used for both jackshaft (carries
# bevel_input) AND the new bevel-output vertical shaft (carries bevel_output).
BEVEL_GEAR_BORE_DIA = 12.0  # mm

# ----------------------------------------------------------------
# Locate output path (parts/ relative to this macro)
# ----------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
FREECAD_DIR = os.path.dirname(HERE)
PARTS_DIR = os.path.join(FREECAD_DIR, "parts")
PART_PATH = os.path.join(PARTS_DIR, "bevel_gear.FCStd")

# Close any stale instance
if "bevel_gear" in App.listDocuments():
    App.closeDocument("bevel_gear")

doc = App.newDocument("bevel_gear")

# ----------------------------------------------------------------
# Generate the gear via freecad.gears (Part::FeaturePython)
# ----------------------------------------------------------------
feature = doc.addObject("Part::FeaturePython", "BevelGear_raw")
BevelGear(feature)
feature.num_teeth = 16
feature.module = "3.0 mm"
feature.pressure_angle = "20 deg"
feature.pitch_angle = "45 deg"
feature.height = "8.0 mm"
feature.beta = "0 deg"            # straight bevel (not spiral)
feature.backlash = "0.10 mm"
feature.clearance = 0.1
feature.numpoints = 20
feature.reset_origin = True

doc.recompute()

if feature.Shape is None or feature.Shape.isNull():
    raise RuntimeError("BevelGear shape generation failed — null Shape")

# ----------------------------------------------------------------
# Bake into a static Part::Feature
# Removes dependency on freecad.gears Proxy at reload time. App::Link
# consumers see a plain Part::Feature with a baked Shape.
# ----------------------------------------------------------------
bbox = feature.Shape.BoundBox
App.Console.PrintMessage(
    f"BevelGear shape: volume={feature.Shape.Volume:.1f} mm^3  "
    f"bbox X[{bbox.XMin:.2f},{bbox.XMax:.2f}] "
    f"Y[{bbox.YMin:.2f},{bbox.YMax:.2f}] "
    f"Z[{bbox.ZMin:.2f},{bbox.ZMax:.2f}]\n"
)

# Subtract a cylindrical bore through the gear's axis (local +Z). The bore
# runs from a bit below the large face up to well above the apex so it
# definitely punches all the way through.
gear_shape = feature.Shape.copy()
bore_height = max(60.0, bbox.ZMax + 40.0)
bore_cylinder = Part.makeCylinder(
    BEVEL_GEAR_BORE_DIA / 2.0, bore_height,
    App.Vector(0, 0, bbox.ZMin - 10.0),  # start below the large face
    App.Vector(0, 0, 1),                 # axis = local +Z
)
gear_with_bore = gear_shape.cut(bore_cylinder)

static_body = doc.addObject("Part::Feature", "BevelGearBody")
static_body.Shape = gear_with_bore
static_body.Label = (
    f"BevelGearBody_16T_m3_pitch45deg_pa20deg_h8mm_bore{int(BEVEL_GEAR_BORE_DIA)}"
)

# Drop the Proxy feature now that we have the baked shape
doc.removeObject(feature.Name)
doc.recompute()

App.Console.PrintMessage(
    f"Bored {BEVEL_GEAR_BORE_DIA} mm through gear axis. "
    f"Final volume = {static_body.Shape.Volume:.1f} mm^3\n"
)

# ----------------------------------------------------------------
# Save the part file
# ----------------------------------------------------------------
doc.FileName = PART_PATH
doc.save()

App.Console.PrintMessage(f"Wrote {PART_PATH}\n")
App.Console.PrintMessage(
    "Spec: 16T module 3.0 mm, pitch_angle 45 deg, pressure 20 deg, height 8 mm, "
    "pitch_dia 48 mm, straight bevel.\n"
)
