# -*- coding: utf-8 -*-
"""
run_macro_08_headless.py — runs macro 08 via freecadcmd.exe.

USAGE
=====
    "C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe" run_macro_08_headless.py

Loads Grinder_Params.FCStd (read-only source of truth), creates or opens
Grinder_Assembly.FCStd, executes 08_build_assembly_layout.py, saves the
assembly. Grinder_Params is NOT saved (we only read from it).
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_PATH = os.path.join(SCRIPT_DIR, "08_build_assembly_layout.py")
PARAMS_PATH = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd")
)
ASSEMBLY_PATH = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Grinder_Assembly.FCStd")
)

print(f"[wrapper] Macro:    {MACRO_PATH}")
print(f"[wrapper] Params:   {PARAMS_PATH}")
print(f"[wrapper] Assembly: {ASSEMBLY_PATH}")

import FreeCAD as App  # noqa: E402

if not os.path.exists(PARAMS_PATH):
    print(f"[wrapper] ERROR: Grinder_Params.FCStd not found at {PARAMS_PATH}")
    sys.exit(1)

# Open Grinder_Params first so the user-facing macro can read its VarSets.
params_doc = App.openDocument(PARAMS_PATH)
print(f"[wrapper] Opened {params_doc.Name}")

# Open or create Grinder_Assembly.
if os.path.exists(ASSEMBLY_PATH):
    assembly_doc = App.openDocument(ASSEMBLY_PATH)
    print(f"[wrapper] Opened existing {assembly_doc.Name}")
else:
    assembly_doc = App.newDocument("Grinder_Assembly")
    print(f"[wrapper] Created new {assembly_doc.Name}")

App.setActiveDocument(assembly_doc.Name)

with open(MACRO_PATH, encoding="utf-8") as fh:
    exec(fh.read(), {"__name__": "__main__"})

# Save the assembly to the canonical path.
if assembly_doc.FileName:
    assembly_doc.save()
else:
    assembly_doc.saveAs(ASSEMBLY_PATH)
print(f"[wrapper] SAVED: {ASSEMBLY_PATH}")
