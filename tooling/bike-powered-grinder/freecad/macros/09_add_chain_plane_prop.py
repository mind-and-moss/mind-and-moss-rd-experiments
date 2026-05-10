# -*- coding: utf-8 -*-
"""
09_add_chain_plane_prop.py
==========================

Adds ONE new property to the existing Drivetrain VarSet on Grinder_Params:

    Drivetrain.chain_plane_x   default 75 mm

Why: Session 9's drivetrain has a single chain stage running in a vertical
YZ plane at one X value. Both the chainring (on BB) and stage1_cog (on the
jackshaft) must mount at the SAME X for the chain to be coplanar. That X
is "load-bearing" geometric data — it determines where the cog sits on
the jackshaft and the chain solid geometry — so it lives in the VarSet,
not as a hardcoded number in macro 08.

Default 75 mm rationale: the BB shaft (CrankBBShaftBody, 16 mm OD) is
140 mm long centered at world X=0, so its right end is at X=+70. Chain
plane at X=+75 puts the chainring just outboard of the right end of the
BB axle on the rider's right side (bike convention). When a real donor
bike is selected, this value will likely shift slightly to match its
chainline; flexible because it's parametric.

PRE-REQUISITES
==============
- Grinder_Params.FCStd must be the active document (the headless wrapper
  opens it).

IDEMPOTENT
==========
- Adds the property only if missing
- Re-running preserves any user-edited value
"""

import FreeCAD as App


doc = App.ActiveDocument
if doc is None or doc.Name != "Grinder_Params":
    raise RuntimeError(
        f"Expected Grinder_Params as active doc; got {doc.Name if doc else None}"
    )

drivetrain = doc.getObject("Drivetrain")
if drivetrain is None:
    raise RuntimeError("Drivetrain VarSet missing — run macro 01 first.")


prop = "chain_plane_x"
if prop in drivetrain.PropertiesList:
    App.Console.PrintMessage(f"  Drivetrain.{prop} already exists — leaving as-is.\n")
else:
    drivetrain.addProperty(
        "App::PropertyLength", prop, "Drivetrain",
        "World-frame X coordinate of the single chain stage's vertical "
        "plane (mm). Both chainring and stage1_cog mount in this plane. "
        "Default 75 mm = rider's right, just outboard of the 140 mm BB "
        "axle's right end at X=+70."
    )
    drivetrain.chain_plane_x = 75.0
    App.Console.PrintMessage(f"  added Drivetrain.{prop} = 75.0 mm\n")


doc.recompute()

App.Console.PrintMessage(
    "\n"
    "================================================================\n"
    "Macro 09 complete. Drivetrain.chain_plane_x is set.\n"
    f"  chain_plane_x = {drivetrain.chain_plane_x}\n"
    "Macro 08 (assembly layout) will read this when placing the\n"
    "chainring, stage1_cog, and chain-loop solid.\n"
    "================================================================\n"
)
