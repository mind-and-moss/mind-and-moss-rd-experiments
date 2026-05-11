# -*- coding: utf-8 -*-
"""
01_create_grinder_params.py — Master Parameter File for Bike-Powered Glass Grinder

WHAT THIS DOES
==============
Creates a FreeCAD document called "Grinder_Params" containing six VarSets that
hold every locked design parameter for the bike-powered glass grinder.

A VarSet is a FreeCAD 1.0+ object that exposes named properties as a single
parameter group. Other FreeCAD files (sketches, parts, the assembly) can
reference these properties via expressions like:
    <<Grinder_Params#Drivetrain>>.cadence_rpm
That means: change a value here, every downstream geometry that uses it
recomputes automatically. Single source of truth.

The macro also creates an empty MasterSketch on the XY plane. You'll draw the
2D drivetrain layout (pulley centers, platen position, frame footprint)
into that sketch interactively — using the VarSet values as expression
references so the layout stays parametric.

HOW TO RUN
==========
  1. Open FreeCAD 1.1.1
  2. Macro menu → Macros... → click "Add" or paste this file's path
  3. Select this macro → click "Execute"
  4. When prompted, save the resulting document to:
       <repo>/tooling/bike-powered-grinder/freecad/Grinder_Params.FCStd

WHY THIS APPROACH
=================
The FreeCAD 1.1 community pattern is: one VarSet per logical group of
parameters (drivetrain, pulleys, frame, etc.) inside a dedicated parameters
file, then every part .FCStd file App-Links to this file and external-
references the VarSet values. Mid-project changes propagate cleanly.

SOURCES
=======
Locked decisions: tooling/bike-powered-grinder/README.md (v3, 2026-05-08)
Stress analysis: tooling/bike-powered-grinder/research/sprocket-stress-corrected.md
FreeCAD readiness: tooling/bike-powered-grinder/research/freecad-1.1-readiness.md

NOTES FOR ISAIAH
================
You are a Python beginner — every block below has a comment explaining what
it does. The actual FreeCAD-specific calls are short. Most of the file is
just data (the parameter values) and explanation.

If a block fails (FreeCAD API quirks happen), the macro will print which
step failed in the FreeCAD report panel. Most failures are recoverable by
running the macro again on a fresh document.
"""

import FreeCAD as App


# =====================================================================
# STEP 1 — Create a new FreeCAD document.
# =====================================================================
# This is the equivalent of File > New in the FreeCAD GUI. The document
# is an in-memory object until you save it (which you do at the end).

doc = App.newDocument("Grinder_Params")
App.Console.PrintMessage("Step 1: created document 'Grinder_Params'.\n")


# =====================================================================
# STEP 2 — Define the parameter groups (VarSets).
# =====================================================================
# Each VarSet is a named bag of properties. We organize parameters into
# logical groups so Isaiah can find them: Drivetrain holds RPM and gear
# ratios, Pulleys holds diameters and crown depth, etc.
#
# The data structure below is a list of (varset_name, properties) tuples.
# Each property is a tuple: (property_name, type, value, units, description)
# - property_name: short, lowercase, used in expressions later
# - type: FreeCAD property type ("Float" for plain numbers, "Length" for
#   millimeter dimensions, "Integer" for tooth counts)
# - value: the numeric value
# - units: text label (informational; FreeCAD handles units via the type)
# - description: tooltip shown when hovering over the property

PARAMETER_GROUPS = [
    (
        "Drivetrain",
        [
            ("cadence_rpm", "Float", 75.0, "rpm",
             "Pedal cadence target (conversational pace, talk-while-pedaling)"),
            ("target_belt_rpm", "Float", 750.0, "rpm",
             "Target drive pulley RPM at the belt"),
            ("total_ratio", "Float", 10.0, "",
             "Total speed-up ratio: cadence_rpm * total_ratio = target_belt_rpm"),
            ("stage1_chainring_teeth", "Integer", 42, "teeth",
             "Stage 1 chainring (donor bike, steel)"),
            ("stage1_cog_teeth", "Integer", 13, "teeth",
             "Stage 1 cassette cog (donor bike, steel)"),
            ("stage1_ratio", "Float", 3.23, "",
             "Stage 1 ratio = chainring / cog = 42 / 13"),
            ("stage2_large_teeth", "Integer", 25, "teeth",
             "Stage 2 large sprocket (PETG print)"),
            ("stage2_pinion_teeth", "Integer", 8, "teeth",
             "Stage 2 pinion (machined steel/aluminum, ~$15)"),
            ("stage2_ratio", "Float", 3.125, "",
             "Stage 2 ratio = 25 / 8 = 3.125"),
            ("chain_pitch", "Length", 12.7, "mm",
             "Chain pitch — 1/2 inch bicycle chain (12.7 mm)"),
        ],
    ),
    (
        "Pulleys",
        [
            ("drive_pulley_dia", "Length", 152.4, "mm",
             "Drive pulley diameter (6 inches, crowned)"),
            ("idler_pulley_dia", "Length", 76.2, "mm",
             "Idler pulley diameter (3 inches, crowned)"),
            ("pulley_crown_depth", "Length", 0.75, "mm",
             "Crown rise from edge to center (~0.030 inch, refine after belt arrives)"),
            ("pulley_face_width", "Length", 60.0, "mm",
             "Pulley face width — slightly wider than 2 inch belt for tracking margin"),
        ],
    ),
    (
        "Belt",
        [
            ("belt_width", "Length", 50.8, "mm",
             "Belt width — 2 inches (Sackorange 2x72 SiC)"),
            ("belt_length", "Length", 1828.8, "mm",
             "Belt length — 72 inches"),
            ("belt_path_center_distance", "Length", 734.9, "mm",
             "Drive-to-idler center distance derived from belt geometry "
             "(L = 2C + pi*(r1+r2) + small term)"),
        ],
    ),
    (
        "Platen",
        [
            ("platen_length", "Length", 558.8, "mm",
             "Platen usable length (22 inches)"),
            ("platen_width", "Length", 60.0, "mm",
             "Platen width — matches pulley face width"),
            ("platen_thickness", "Length", 12.0, "mm",
             "Platen thickness — TBD, 12 mm starting point for stainless-faced PETG"),
            ("max_glass_edge", "Length", 457.2, "mm",
             "HARD CONSTRAINT: longest single glass edge any Mind and Moss panel "
             "can have. Platen 22 inches minus 4 inches approach/exit margin = 18 inches."),
        ],
    ),
    (
        "Frame",
        [
            ("max_print_dim", "Length", 170.0, "mm",
             "HARD CONSTRAINT: max dimension any printable part may have in any axis. "
             "Bambu A1 Mini build volume is 180 mm cube; 170 leaves margin for first-layer adhesion."),
            ("module_target_length", "Length", 762.0, "mm",
             "Target module length (~30 inches, fits through 30 inch interior door)"),
            ("door_clearance", "Length", 762.0, "mm",
             "30 inch interior door — portability constraint"),
        ],
    ),
    (
        "Fits",
        [
            ("fit_clearance_loose", "Length", 0.30, "mm",
             "Loose fit (slip with finger pressure)"),
            ("fit_clearance_running", "Length", 0.20, "mm",
             "Running fit (slides freely, no slop) — calibrate via test coupon"),
            ("fit_clearance_press", "Length", 0.10, "mm",
             "Press fit (assembly with pressure, no slip in use)"),
        ],
    ),
    (
        "Bearings",
        [
            ("intermediate_shaft_dia", "Length", 12.0, "mm",
             "Intermediate shaft (304 stainless rod) diameter"),
            ("intermediate_bearing_OD", "Length", 35.0, "mm",
             "SKF 6202-2RS outer diameter"),
            ("intermediate_bearing_ID", "Length", 15.0, "mm",
             "SKF 6202-2RS inner diameter (note: shaft is 12 mm; "
             "use a sleeve/adapter to step up to 15 mm bearing bore, "
             "OR switch to 6201-2RS which has 12 mm ID)"),
            ("intermediate_bearing_W", "Length", 11.0, "mm",
             "SKF 6202-2RS width"),
            ("grinder_shaft_dia", "Length", 8.0, "mm",
             "Grinder pulley shaft (304 stainless rod) diameter"),
            ("grinder_bearing_OD", "Length", 22.0, "mm",
             "NSK 608-2RS outer diameter"),
            ("grinder_bearing_ID", "Length", 8.0, "mm",
             "NSK 608-2RS inner diameter (matches shaft)"),
            ("grinder_bearing_W", "Length", 7.0, "mm",
             "NSK 608-2RS width"),
        ],
    ),
]


# =====================================================================
# STEP 3 — Create each VarSet and populate it.
# =====================================================================
# A VarSet is a FreeCAD object of type "App::VarSet". We add custom
# properties to it via addProperty(). Property types:
#   App::PropertyFloat   — plain decimal number, no units
#   App::PropertyLength  — millimeter dimension (FreeCAD handles units)
#   App::PropertyInteger — whole number (tooth counts, etc.)

for (varset_name, props) in PARAMETER_GROUPS:
    # Create the VarSet object inside our document
    varset = doc.addObject("App::VarSet", varset_name)
    App.Console.PrintMessage(f"Step 2: creating VarSet '{varset_name}'...\n")

    for (prop_name, prop_type, value, units, description) in props:
        # Build the full FreeCAD property type name
        full_type = "App::Property" + prop_type

        # addProperty signature: (type, name, group, doc, attr, ro)
        # group is the section header in the property panel
        # doc is the tooltip shown on hover
        try:
            varset.addProperty(full_type, prop_name, varset_name, description)
        except Exception as e:
            App.Console.PrintError(
                f"  ! Failed to add property {prop_name}: {e}\n"
            )
            continue

        # Set the value. Length properties accept a number directly
        # (FreeCAD interprets it as millimeters because the property
        # is type Length).
        try:
            setattr(varset, prop_name, value)
        except Exception as e:
            App.Console.PrintError(
                f"  ! Failed to set value of {prop_name}: {e}\n"
            )

    App.Console.PrintMessage(f"  Done. {len(props)} properties on {varset_name}.\n")


# =====================================================================
# STEP 4 — Create an empty MasterSketch on the XY plane.
# =====================================================================
# This is where you'll draw the 2D drivetrain layout interactively in
# the Sketcher workbench. The sketch starts empty so we don't fight
# with the API trying to add geometry programmatically (Sketcher's
# Python API is fiddly; manual sketching with the GUI is easier).

# Make sure the document has the standard origin (XY/XZ/YZ planes).
# In FreeCAD 1.1, origin is created automatically for some workflows
# but not always — we explicitly add one.
try:
    origin = doc.addObject("App::Origin", "Origin")
except Exception:
    origin = None  # If it already exists, that's fine

sketch = doc.addObject("Sketcher::SketchObject", "MasterSketch")

# Attach the sketch to the XY plane. The simplest reliable way: leave
# the default placement (which IS the XY plane in the global coord
# system). When you open the sketch you'll be looking down at XY.
sketch.Placement = App.Placement(
    App.Vector(0, 0, 0),
    App.Rotation(0, 0, 0, 1)
)

App.Console.PrintMessage("Step 3: empty MasterSketch on XY plane.\n")


# =====================================================================
# STEP 5 — Recompute and remind the user what to do next.
# =====================================================================
# recompute() updates all expressions and dependencies. It's a no-op
# for a fresh doc but good hygiene before save.

doc.recompute()

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Grinder_Params document created.\n"
    "================================================================\n"
    "Next steps:\n"
    "  1. File > Save As...\n"
    "     Save to: <repo>/tooling/bike-powered-grinder/freecad/Grinder_Params.FCStd\n"
    "  2. Inspect the VarSets in the model tree (left panel). Each\n"
    "     VarSet has properties listed in the panel below — verify\n"
    "     the values look right.\n"
    "  3. Switch to the Sketcher workbench, double-click MasterSketch,\n"
    "     and start drawing the drivetrain layout. Reference the\n"
    "     VarSets via expressions like:\n"
    "       Drivetrain.cadence_rpm\n"
    "       Pulleys.drive_pulley_dia\n"
    "  4. When you're ready for the next macro (which scaffolds the\n"
    "     drivetrain geometry into the sketch), tell Claude Code.\n"
    "================================================================\n"
)
