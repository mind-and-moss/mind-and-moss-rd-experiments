# -*- coding: utf-8 -*-
"""
verify_parametric_binding.py
============================

Headless verification that the parametric expression chain in
Grinder_Params.FCStd is actually working end-to-end.

PROCEDURE
---------
1. Open Grinder_Params.FCStd
2. Read the current Pulleys.drive_pulley_dia (expect 152.4 mm)
3. Read the drive pulley circle's radius from MasterSketch (expect 76.2 mm)
4. Change Pulleys.drive_pulley_dia to 180.0 and recompute
5. Re-read the circle radius (expect 90.0 mm if binding works)
6. Revert the VarSet to its original value, recompute, exit
7. Do NOT save — leaves the on-disk file pristine

Output goes through App.Console.PrintMessage AND a side-channel report
file (verify_parametric_binding.report.txt next to the macro) so we get
the verdict regardless of stdout buffering quirks under freecadcmd.exe.

Exit code: 0 = pass, 1 = fail.
"""

import os
import sys
import FreeCAD as App


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "Grinder_Params.FCStd"))
REPORT_PATH = os.path.join(SCRIPT_DIR, "verify_parametric_binding.report.txt")

_lines = []

def report(msg):
    """Send the line to FreeCAD's console AND buffer for the report file."""
    App.Console.PrintMessage(msg + "\n")
    _lines.append(msg)

def write_report():
    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(_lines) + "\n")


if not os.path.exists(DOC_PATH):
    report(f"FAIL: doc not found at {DOC_PATH}")
    write_report()
    sys.exit(1)

doc = App.openDocument(DOC_PATH)

pulleys = doc.getObject("Pulleys")
sketch = doc.getObject("MasterSketch")

if pulleys is None:
    report("FAIL: Pulleys VarSet not found in document")
    write_report()
    sys.exit(1)
if sketch is None:
    report("FAIL: MasterSketch not found in document")
    write_report()
    sys.exit(1)

# Drive pulley = the largest-radius circle whose center is at the origin.
# (Stage-2 pinion is also at origin but smaller; cog/large/chainring are at
# the placeholder shaft positions, not the origin.)
candidates = []
for i, geom in enumerate(sketch.Geometry):
    if hasattr(geom, "Center") and hasattr(geom, "Radius"):
        c = geom.Center
        if abs(c.x) < 1e-6 and abs(c.y) < 1e-6:
            candidates.append((i, float(geom.Radius)))

if not candidates:
    report("FAIL: no circle centered at origin found")
    write_report()
    sys.exit(1)

candidates.sort(key=lambda t: t[1], reverse=True)
drive_idx = candidates[0][0]

# --- Step 1: read initial state ---
# pulleys.drive_pulley_dia is an App.Quantity with units; coerce to float (mm)
raw_dia = pulleys.drive_pulley_dia
initial_dia = raw_dia.Value if hasattr(raw_dia, "Value") else float(raw_dia)
initial_radius = float(sketch.Geometry[drive_idx].Radius)

report(f"Initial Pulleys.drive_pulley_dia = {raw_dia} ({initial_dia} mm)")
report(f"Initial drive pulley circle radius = {initial_radius:.4f}")

expected_initial_radius = initial_dia / 2.0
if abs(initial_radius - expected_initial_radius) > 0.001:
    report(f"WARN: pre-test radius {initial_radius:.4f} != dia/2 = "
           f"{expected_initial_radius:.4f}")

# --- Step 2: mutate ---
NEW_DIA = 180.0
report(f"")
report(f"Setting Pulleys.drive_pulley_dia = {NEW_DIA} ...")
pulleys.drive_pulley_dia = NEW_DIA
sketch.touch()
doc.recompute()

# --- Step 3: re-read ---
new_radius = float(sketch.Geometry[drive_idx].Radius)
report(f"After-change drive pulley circle radius = {new_radius:.4f}")
expected_new_radius = NEW_DIA / 2.0

# --- Verdict ---
report("")
report("================ VERDICT ================")
if abs(new_radius - expected_new_radius) < 0.001:
    report("PASS: parametric binding is live.")
    report(f"  drive_pulley_dia {initial_dia:.1f} -> radius {initial_radius:.4f}")
    report(f"  drive_pulley_dia {NEW_DIA:.1f} -> radius {new_radius:.4f}")
    report(f"  delta vs expected {expected_new_radius:.4f}: "
           f"{abs(new_radius - expected_new_radius):.6f}")
    verdict = 0
else:
    report("FAIL: parametric binding did NOT propagate.")
    report(f"  expected radius {expected_new_radius:.4f}")
    report(f"  got radius      {new_radius:.4f}")
    report(f"  delta           {abs(new_radius - expected_new_radius):.4f}")
    report("  (the Diameter constraint expression isn't being honored)")
    verdict = 1
report("=========================================")

# --- Step 4: revert ---
pulleys.drive_pulley_dia = initial_dia
sketch.touch()
doc.recompute()
report(f"")
report(f"Reverted Pulleys.drive_pulley_dia to {initial_dia}.")
report("Document NOT saved — on-disk file is untouched.")

write_report()
sys.exit(verdict)
