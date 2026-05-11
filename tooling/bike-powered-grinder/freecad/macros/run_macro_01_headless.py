# -*- coding: utf-8 -*-
"""
run_macro_01_headless.py — runs macro 01 via freecadcmd.exe and saves the doc.

This wrapper exists so Claude Code can produce Grinder_Params.FCStd without
Isaiah having to open the FreeCAD GUI. It executes the user-facing macro,
then saves the resulting document to the canonical path.

USAGE
=====
    "C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe" run_macro_01_headless.py

The user-facing macro 01_create_grinder_params.py is unchanged — it remains
the path Isaiah follows in the GUI. This wrapper just calls it programmatically.
"""

import os
import sys

# Paths are relative to this wrapper's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_PATH = os.path.join(SCRIPT_DIR, "01_create_grinder_params.py")
SAVE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd"))

print(f"[wrapper] Macro:    {MACRO_PATH}")
print(f"[wrapper] Save to:  {SAVE_PATH}")
print(f"[wrapper] Executing macro...")

# Execute the user-facing macro. In freecadcmd.exe context, FreeCAD as App
# is already importable.
with open(MACRO_PATH, encoding="utf-8") as fh:
    exec(fh.read(), {"__name__": "__main__"})

# Save the document the macro created.
import FreeCAD as App  # noqa: E402

doc = App.ActiveDocument
if doc is None:
    print("[wrapper] ERROR: no active document after macro run")
    sys.exit(1)

print(f"[wrapper] Saving {doc.Name} to {SAVE_PATH}")
doc.saveAs(SAVE_PATH)
print(f"[wrapper] SAVED: {SAVE_PATH}")
