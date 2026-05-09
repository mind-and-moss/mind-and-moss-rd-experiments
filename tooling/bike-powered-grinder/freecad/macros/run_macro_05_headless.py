# -*- coding: utf-8 -*-
"""
run_macro_05_headless.py
========================

Wrapper for macro 05. More involved than wrappers 01-04 because macro
05 creates a SECOND document (the part file). Saves the part doc
(not the master).

STL export does NOT happen in this wrapper — the in-session
PartDesign Revolution.Shape stays null when built programmatically,
so STL export is a separate freecadcmd invocation that loads the
saved FCStd fresh. See export_drive_pulley_stl.py.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GRINDER_PARAMS = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd")
)
PARTS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "parts"))
PART_PATH = os.path.join(PARTS_DIR, "drive_pulley.FCStd")
MACRO_PATH = os.path.join(SCRIPT_DIR, "05_create_drive_pulley_part.py")

print(f"[wrapper] Opening master: {GRINDER_PARAMS}")

import FreeCAD as App  # noqa: E402

if not os.path.exists(GRINDER_PARAMS):
    print(f"[wrapper] ERROR: Grinder_Params.FCStd not found at {GRINDER_PARAMS}")
    sys.exit(1)

App.openDocument(GRINDER_PARAMS)
print("[wrapper] Master doc loaded: Grinder_Params")

print(f"[wrapper] Running macro: {MACRO_PATH}")
with open(MACRO_PATH, encoding="utf-8") as fh:
    exec(fh.read(), {"__name__": "__main__", "__file__": MACRO_PATH})

part_doc = App.ActiveDocument
if part_doc.Name == "Grinder_Params":
    print("[wrapper] ERROR: macro left master as active doc - aborting save")
    sys.exit(1)

if part_doc.FileName:
    print(f"[wrapper] Saving: {part_doc.FileName}")
    part_doc.save()
else:
    os.makedirs(PARTS_DIR, exist_ok=True)
    print(f"[wrapper] First save -> {PART_PATH}")
    part_doc.saveAs(PART_PATH)

print("[wrapper] Done. Run export_drive_pulley_stl.py next for STL.")
