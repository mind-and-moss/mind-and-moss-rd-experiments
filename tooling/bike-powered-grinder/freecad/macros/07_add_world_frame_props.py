# -*- coding: utf-8 -*-
"""
07_add_world_frame_props.py
===========================

Adds the assembly-level WORLD FRAME parameters to Grinder_Params.FCStd.

The assembly redesign (macro 08) abandons the old MasterSketch axis convention
(which had the drive pulley at the origin and the rider far off-axis on +Y)
in favor of a rider-anchored world frame:

    Origin = rider seat reference point on the floor.
    +Y     = forward (away from rider, toward the desk's far edge).
    +Z     = up.
    +X     = rider's right (left/right axis across the body).
    Belt   = horizontal, long axis along X, centerline at
             Y = desk_depth, Z = desk_height.

Existing part-level sketches keep their LOCAL frames — only the assembly
layer uses this convention. MasterSketch (in Grinder_Params) is unchanged.

WHAT THIS ADDS TO Drivetrain VarSet
====================================
    rider_seat_y         Length, default 0.0    mm  (origin-Y, definitional)
    desk_depth           Length, default 610.0  mm  (24in school-desk depth)
    desk_height          Length, default 762.0  mm  (30in school-desk top)
    belt_centerline_y    Length, EXPRESSION = rider_seat_y + desk_depth

These live on the Drivetrain VarSet (per the redesign brief) for proximity
to the existing shaft-position properties. A future cleanup may split them
into a dedicated WorldFrame VarSet.

PRE-REQUISITES
==============
- Grinder_Params.FCStd must be the active document (or loaded via the
  headless wrapper, which opens it before exec).
- A "Drivetrain" VarSet must already exist (created by macro 01).

IDEMPOTENT
==========
- Properties are added only if missing — re-running preserves values
  Isaiah may have edited in the GUI.
- The expression on belt_centerline_y is re-bound on every run (cheap
  and safe — assigns to the same expression each time).
"""

import FreeCAD as App


# ====================================================================
# Sanity
# ====================================================================
doc = App.ActiveDocument
if doc is None:
    raise RuntimeError("No active document. Open Grinder_Params.FCStd first.")

if doc.Name != "Grinder_Params":
    App.Console.PrintWarning(
        f"Active doc is '{doc.Name}', expected 'Grinder_Params'. "
        "Continuing — but check you're in the right file.\n"
    )

drivetrain = doc.getObject("Drivetrain")
if drivetrain is None:
    raise RuntimeError("Drivetrain VarSet missing. Run macro 01 first.")


# ====================================================================
# Helper: idempotent property add
# ====================================================================
# Mirrors the pattern from macro 04 — add only if absent, set value
# only when adding (so user edits in the GUI survive re-runs).

def add_property_if_missing(varset, prop_name, prop_type, group, doc_str,
                            default_value=None):
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


# ====================================================================
# Add the four world-frame properties
# ====================================================================
App.Console.PrintMessage("Adding world-frame properties to Drivetrain VarSet...\n")

add_property_if_missing(
    drivetrain, "rider_seat_y", "Length", "WorldFrame",
    "Rider seat reference point Y coordinate, in world frame (mm). "
    "DEFINITIONAL: this is the origin of the assembly coordinate system. "
    "Default 0.",
    0.0
)
add_property_if_missing(
    drivetrain, "desk_depth", "Length", "WorldFrame",
    "Desk depth along world Y axis (mm). 610 mm = 24in, standard school-"
    "desk depth. Far edge (Y = desk_depth) is the platen line where glass "
    "meets belt.",
    610.0
)
add_property_if_missing(
    drivetrain, "desk_height", "Length", "WorldFrame",
    "Desk top surface height above floor in world Z (mm). 762 mm = 30in, "
    "standard school-desk top — chosen because Isaiah uses school chairs "
    "and is adult-sized.",
    762.0
)
# belt_centerline_y is computed — added without a default so the expression
# below is the source of truth. Don't pass default_value.
add_property_if_missing(
    drivetrain, "belt_centerline_y", "Length", "WorldFrame",
    "World-frame Y of the belt centerline (mm). COMPUTED: "
    "rider_seat_y + desk_depth (the belt sits along the desk's far edge)."
)


# ====================================================================
# Bind the belt_centerline_y expression every run (idempotent)
# ====================================================================
# Same pattern macro 04 uses for stage1/stage2_chain_center_distance:
# expressions are reassigned on every run to keep them current even if
# someone tried to edit the property by hand.
drivetrain.setExpression(
    "belt_centerline_y",
    "<<Drivetrain>>.rider_seat_y + <<Drivetrain>>.desk_depth"
)
App.Console.PrintMessage(
    "  bound expression: belt_centerline_y = rider_seat_y + desk_depth\n"
)


# ====================================================================
# Recompute and report
# ====================================================================
doc.recompute()

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 07 complete. World-frame properties live on Drivetrain.\n"
    f"  rider_seat_y      = {drivetrain.rider_seat_y}\n"
    f"  desk_depth        = {drivetrain.desk_depth}\n"
    f"  desk_height       = {drivetrain.desk_height}\n"
    f"  belt_centerline_y = {drivetrain.belt_centerline_y}  (expression-bound)\n"
    "World frame is now defined in Grinder_Params. Macro 08 will build\n"
    "the assembly geometry against these values.\n"
    "================================================================\n"
)
