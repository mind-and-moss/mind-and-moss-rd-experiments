# -*- coding: utf-8 -*-
"""
07_add_world_frame_props.py
===========================

Maintains the WorldFrame VarSet on Grinder_Params.FCStd — the assembly-level
parameters that define the new (Session 8) rider-anchored world frame.

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

WHAT THIS MAINTAINS — WorldFrame VarSet
========================================
    rider_seat_y         Length, default 0.0    mm  (origin-Y, definitional)
    desk_depth           Length, default 610.0  mm  (24in school-desk depth)
    desk_height          Length, default 762.0  mm  (30in school-desk top)
    belt_centerline_y    Length, EXPRESSION = rider_seat_y + desk_depth

WHY ITS OWN VARSET (not on Drivetrain)
======================================
First commit of this work put these on the Drivetrain VarSet because the
brief said so and proximity-to-shaft-positions seemed convenient. They're
moved here because they're not drivetrain parameters — they describe the
human/desk physical setup that the drivetrain mounts into. Cleaner to
keep concerns separated.

MIGRATION FROM DRIVETRAIN
=========================
If a previous run of this macro put the four properties on Drivetrain
(versions before today), copy current values over to WorldFrame, then
remove the Drivetrain copies. Cleanly idempotent:
- First run on a fresh doc: creates WorldFrame, sets defaults.
- Run after the old Drivetrain version: migrates values, removes old props.
- Subsequent runs: properties already on WorldFrame, leave values alone,
  re-bind the expression (cheap and safe).

PRE-REQUISITES
==============
- Grinder_Params.FCStd must be the active document (or loaded via the
  headless wrapper, which opens it before exec).

IDEMPOTENT
==========
- WorldFrame VarSet created only if missing
- Properties added only if missing — re-running preserves user-edited values
- The expression on belt_centerline_y is re-bound on every run
- Drivetrain copies (if present from older versions) are removed
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


# ====================================================================
# Get or create the WorldFrame VarSet
# ====================================================================
worldframe = doc.getObject("WorldFrame")
if worldframe is None:
    worldframe = doc.addObject("App::VarSet", "WorldFrame")
    App.Console.PrintMessage("Created VarSet 'WorldFrame'.\n")
else:
    App.Console.PrintMessage("VarSet 'WorldFrame' already exists.\n")


# ====================================================================
# Helper: idempotent property add
# ====================================================================

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


def q(qty):
    """Coerce App.Quantity (mm) to plain float in mm."""
    return qty.Value if hasattr(qty, "Value") else float(qty)


# ====================================================================
# Migration — pull values off Drivetrain if they live there from the
# previous version of this macro. Capture before adding to WorldFrame
# so we can preserve any user edits made in the GUI.
# ====================================================================

MIGRATING_PROPS = ("rider_seat_y", "desk_depth", "desk_height",
                   "belt_centerline_y")
migrated_values = {}

drivetrain = doc.getObject("Drivetrain")
if drivetrain is not None:
    for name in MIGRATING_PROPS:
        if name in drivetrain.PropertiesList:
            try:
                # belt_centerline_y was expression-bound on Drivetrain too;
                # we don't migrate its numeric value (the new expression
                # on WorldFrame will recompute it). Migrate the inputs only.
                if name != "belt_centerline_y":
                    migrated_values[name] = q(getattr(drivetrain, name))
                    App.Console.PrintMessage(
                        f"  migrating from Drivetrain: "
                        f"{name} = {migrated_values[name]} mm\n"
                    )
            except Exception as e:
                App.Console.PrintWarning(
                    f"  could not read Drivetrain.{name}: {e}\n"
                )


# ====================================================================
# Add the four world-frame properties to WorldFrame
# ====================================================================
App.Console.PrintMessage("Ensuring WorldFrame properties...\n")

add_property_if_missing(
    worldframe, "rider_seat_y", "Length", "WorldFrame",
    "Rider seat reference point Y coordinate, in world frame (mm). "
    "DEFINITIONAL: this is the origin of the assembly coordinate system. "
    "Default 0.",
    migrated_values.get("rider_seat_y", 0.0)
)
add_property_if_missing(
    worldframe, "desk_depth", "Length", "WorldFrame",
    "Desk depth along world Y axis (mm). 610 mm = 24in, standard school-"
    "desk depth. Far edge (Y = desk_depth) is the platen line where glass "
    "meets belt.",
    migrated_values.get("desk_depth", 610.0)
)
add_property_if_missing(
    worldframe, "desk_height", "Length", "WorldFrame",
    "Desk top surface height above floor in world Z (mm). 762 mm = 30in, "
    "standard school-desk top — chosen because Isaiah uses school chairs "
    "and is adult-sized.",
    migrated_values.get("desk_height", 762.0)
)
# belt_centerline_y is computed — added without a default so the expression
# below is the source of truth.
add_property_if_missing(
    worldframe, "belt_centerline_y", "Length", "WorldFrame",
    "World-frame Y of the belt centerline (mm). COMPUTED: "
    "rider_seat_y + desk_depth (the belt sits along the desk's far edge)."
)


# ====================================================================
# Bind the belt_centerline_y expression every run (idempotent)
# ====================================================================
worldframe.setExpression(
    "belt_centerline_y",
    "<<WorldFrame>>.rider_seat_y + <<WorldFrame>>.desk_depth"
)
App.Console.PrintMessage(
    "  bound expression: belt_centerline_y = rider_seat_y + desk_depth\n"
)


# ====================================================================
# Migration cleanup — remove the old Drivetrain copies if any survived.
# Done AFTER the WorldFrame copies are populated, so values are safe.
# Note: removing a property that has an expression bound to it is fine
# in FreeCAD — the expression is dropped with the property.
# ====================================================================
if drivetrain is not None:
    removed = []
    for name in MIGRATING_PROPS:
        if name in drivetrain.PropertiesList:
            try:
                # Clear any expression first (safer than relying on remove
                # to drop it).
                try:
                    drivetrain.setExpression(name, None)
                except Exception:
                    pass
                drivetrain.removeProperty(name)
                removed.append(name)
            except Exception as e:
                App.Console.PrintWarning(
                    f"  could not remove Drivetrain.{name}: {e}\n"
                )
    if removed:
        App.Console.PrintMessage(
            f"  removed from Drivetrain (migrated to WorldFrame): "
            f"{', '.join(removed)}\n"
        )


# ====================================================================
# Recompute and report
# ====================================================================
doc.recompute()

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 07 complete. World-frame properties live on WorldFrame VarSet.\n"
    f"  rider_seat_y      = {worldframe.rider_seat_y}\n"
    f"  desk_depth        = {worldframe.desk_depth}\n"
    f"  desk_height       = {worldframe.desk_height}\n"
    f"  belt_centerline_y = {worldframe.belt_centerline_y}  (expression-bound)\n"
    "World frame is now defined in Grinder_Params. Macro 08 reads from\n"
    "WorldFrame to build the assembly geometry.\n"
    "================================================================\n"
)
