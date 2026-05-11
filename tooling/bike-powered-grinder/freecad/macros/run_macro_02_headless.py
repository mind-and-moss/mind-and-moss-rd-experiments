# -*- coding: utf-8 -*-
"""
run_macro_02_headless.py — opens Grinder_Params.FCStd, runs macro 02, saves.

USAGE
=====
    "C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe" run_macro_02_headless.py
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd"))
MACRO_PATH = os.path.join(SCRIPT_DIR, "02_scaffold_drivetrain_geometry.py")

print(f"[wrapper] Opening: {DOC_PATH}")

import FreeCAD as App  # noqa: E402

if not os.path.exists(DOC_PATH):
    print(f"[wrapper] ERROR: Grinder_Params.FCStd not found at {DOC_PATH}")
    print("[wrapper] Run macro 01 first to create the params file.")
    sys.exit(1)

App.openDocument(DOC_PATH)
print(f"[wrapper] Active doc: {App.ActiveDocument.Name}")

print(f"[wrapper] Running macro: {MACRO_PATH}")
with open(MACRO_PATH, encoding="utf-8") as fh:
    exec(fh.read(), {"__name__": "__main__"})

print("[wrapper] Saving document...")
App.ActiveDocument.save()
print("[wrapper] Done.")
