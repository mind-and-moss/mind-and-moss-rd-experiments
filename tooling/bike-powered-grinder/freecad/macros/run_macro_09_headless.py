# -*- coding: utf-8 -*-
"""
run_macro_09_headless.py — runs macro 09 via freecadcmd.exe.

Loads Grinder_Params.FCStd, executes 09_add_chain_plane_prop.py to add
the Drivetrain.chain_plane_x property, saves the params doc.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_PATH = os.path.join(SCRIPT_DIR, "09_add_chain_plane_prop.py")
PARAMS_PATH = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd")
)

print(f"[wrapper] Macro:  {MACRO_PATH}")
print(f"[wrapper] Params: {PARAMS_PATH}")

import FreeCAD as App  # noqa: E402

if not os.path.exists(PARAMS_PATH):
    print(f"[wrapper] ERROR: Grinder_Params.FCStd not found at {PARAMS_PATH}")
    sys.exit(1)

doc = App.openDocument(PARAMS_PATH)
App.setActiveDocument(doc.Name)
print(f"[wrapper] Opened {doc.Name}")

with open(MACRO_PATH, encoding="utf-8") as fh:
    exec(fh.read(), {"__name__": "__main__"})

doc.save()
print(f"[wrapper] SAVED: {PARAMS_PATH}")
