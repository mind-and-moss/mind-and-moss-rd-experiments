# -*- coding: utf-8 -*-
"""
run_macro_06_headless.py — opens master, runs macro 06 (creates 7 part
placeholder .FCStd files), exits. Each part is saved + closed within
the macro itself, so the wrapper doesn't need to know which docs to save.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GRINDER_PARAMS = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd")
)
MACRO_PATH = os.path.join(SCRIPT_DIR, "06_create_drivetrain_placeholders.py")

print(f"[wrapper] Opening master: {GRINDER_PARAMS}")

import FreeCAD as App  # noqa: E402

if not os.path.exists(GRINDER_PARAMS):
    print(f"[wrapper] ERROR: master not found at {GRINDER_PARAMS}")
    sys.exit(1)

App.openDocument(GRINDER_PARAMS)
print("[wrapper] Master loaded")

print(f"[wrapper] Running macro: {MACRO_PATH}")
with open(MACRO_PATH, encoding="utf-8") as fh:
    exec(fh.read(), {"__name__": "__main__", "__file__": MACRO_PATH})

print("[wrapper] Done.")
