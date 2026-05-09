---
name: freecad-headless-pipeline
description: Use when running FreeCAD macros from Claude Code without making Isaiah open the FreeCAD GUI. Drives FreeCAD 1.1's `freecadcmd.exe` (the headless console build) via a wrapper script pattern. Unlocks rapid iteration — Claude Code edits a macro, runs it, verifies output, commits, all without GUI interaction. Documents the Sketcher constraint API, VarSet expression syntax, and idempotent macro patterns observed working in FreeCAD 1.1.1.
---

# FreeCAD headless pipeline

Claude Code can drive FreeCAD entirely without GUI interaction by invoking
`freecadcmd.exe` (the headless console build, shipped alongside `freecad.exe`).
This pattern unlocks rapid iteration: edit a macro file, run it, inspect output,
fix, re-run.

Discovered and validated during Session 6 of Mind and Moss while building out
`Grinder_Params.FCStd` for the bike-powered glass grinder.

## When to use

- You need to create or modify a `.FCStd` file from Claude Code without
  asking Isaiah to open the GUI for routine work
- You're iterating on a macro and want to test it programmatically
- You want to verify a parametric model recomputes correctly under
  different VarSet values
- You need to generate STL files for printing in an automated way

Don't use it for:
- Tasks that genuinely need the GUI (sketcher visual inspection, manual
  geometry placement)
- Operations that depend on the 3D viewport (rendering, screenshot)

## Folder structure

```
<feature>/freecad/
├── <Feature>_Params.FCStd       ← binary FreeCAD doc, version-controlled
├── README.md                    ← document the GUI workflow alongside
├── .gitignore                   ← exclude *.FCStd1 *.FCBak *.FCLock
└── macros/
    ├── 01_<purpose>.py          ← user-facing macro 1 (GUI-runnable)
    ├── 02_<purpose>.py          ← user-facing macro 2
    ├── 03_<purpose>.py          ← user-facing macro 3
    ├── run_macro_01_headless.py ← wrapper for freecadcmd.exe
    ├── run_macro_02_headless.py
    └── run_macro_03_headless.py
```

User-facing macros document the GUI workflow (Macro menu → Macros → Execute)
so Isaiah can run them manually if he wants. Headless wrappers are pure
automation.

## Wrapper template (for `run_macro_NN_headless.py`)

```python
# -*- coding: utf-8 -*-
"""
run_macro_NN_headless.py — opens <Feature>_Params.FCStd, runs macro NN, saves.
"""
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "<Feature>_Params.FCStd"))
MACRO_PATH = os.path.join(SCRIPT_DIR, "NN_<purpose>.py")

import FreeCAD as App

if not os.path.exists(DOC_PATH):
    # Macro 01 special-cases this — creates a fresh doc if none exists
    App.newDocument("<Feature>_Params")
else:
    App.openDocument(DOC_PATH)

with open(MACRO_PATH, encoding="utf-8") as fh:
    exec(fh.read(), {"__name__": "__main__"})

# Macro 01 uses saveAs(DOC_PATH); macros 02+ just save() the already-named doc
App.ActiveDocument.save()
```

## Invocation from Claude Code

```bash
"C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" path/to/run_macro_NN_headless.py
```

The Bash tool's stdout captures all `App.Console.PrintMessage` output plus
the wrapper's `print()` statements. Errors print to stderr.

## Idempotent macro pattern

Every macro should start by wiping any state it's going to recreate:

```python
# Wipe constraints first (constraints reference geometry; can't delete
# geometry while a constraint references it)
while sketch.ConstraintCount > 0:
    sketch.delConstraint(0)
while sketch.GeometryCount > 0:
    sketch.delGeometry(0)
```

Then rebuild from scratch. Result: re-running a macro any number of times
produces the same state. Safe for iteration.

## VarSet expression syntax (FreeCAD 1.1)

VarSets are FreeCAD 1.0+ objects that hold typed properties. In FreeCAD 1.1,
expressions inside the same document reference VarSet properties via:

```
<<VarSetName>>.property_name
```

Example: `<<Pulleys>>.drive_pulley_dia`.

Trig with degree interpretation: `sin(180 deg / N)` works.
Pi as a constant: `pi` is available.

Full chain-pitch formula (sprocket pitch diameter for chain drive):
```
<<Drivetrain>>.chain_pitch / sin(180 deg / <<Drivetrain>>.stage1_chainring_teeth)
```

To bind an expression to a Sketcher constraint:
```python
sketch.setExpression(f".Constraints[{constraint_idx}]", "<<VarSet>>.prop")
```

## Sketcher constraint API patterns

Origin reference: `GeoId = -1, PosId = 1` (root point at sketch origin).
Circle vertex codes:
- `PosId = 1, 2, 3` — three points on the circumference
- `PosId = 3` — center

Line vertex codes:
- `PosId = 1` — start
- `PosId = 2` — end

Common constraints used:

```python
# Circle center to origin (Coincident)
Sketcher.Constraint("Coincident", circle_idx, 3, -1, 1)

# Circle diameter (binds cleanly to expressions)
Sketcher.Constraint("Diameter", circle_idx, value_in_mm)

# Distance from origin along X (signed — negative if to the left)
Sketcher.Constraint("DistanceX", -1, 1, target_idx, 3, value)

# Distance from origin along Y
Sketcher.Constraint("DistanceY", -1, 1, target_idx, 3, value)

# Line orientations
Sketcher.Constraint("Horizontal", line_idx)
Sketcher.Constraint("Vertical", line_idx)

# Line lengths
Sketcher.Constraint("Distance", line_idx, length)

# Coincident endpoints (close a rectangle)
Sketcher.Constraint("Coincident", line_a, 2, line_b, 1)  # line_a.end = line_b.start
```

Add a circle as construction geometry:
```python
import Part
from FreeCAD import Vector
circle = Part.Circle()
circle.Center = Vector(cx, cy, 0)
circle.Radius = r
geo_idx = sketch.addGeometry(circle, True)  # True = construction
```

Add a line as construction geometry:
```python
line = Part.LineSegment(Vector(x1, y1, 0), Vector(x2, y2, 0))
geo_idx = sketch.addGeometry(line, True)
```

## VarSet creation pattern

```python
varset = doc.addObject("App::VarSet", "VarSetName")

# Add a Length property (FreeCAD handles mm units automatically)
varset.addProperty("App::PropertyLength", "prop_name", "GroupName", "Description")
varset.prop_name = 152.4  # mm

# Add a Float property (no units)
varset.addProperty("App::PropertyFloat", "prop_name", "GroupName", "Description")
varset.prop_name = 10.0

# Add an Integer property (tooth counts, counts of things)
varset.addProperty("App::PropertyInteger", "prop_name", "GroupName", "Description")
varset.prop_name = 42
```

## Error handling pattern

Wrap each constraint addition in try/except so partial failures don't kill
the whole macro. Print which step failed:

```python
def add_constraint_safe(constraint, label):
    try:
        sketch.addConstraint(constraint)
        return sketch.ConstraintCount - 1
    except Exception as e:
        App.Console.PrintError(f"  ! {label}: failed: {e}\n")
        return None

def bind_expression(constraint_idx, expr, label):
    if constraint_idx is None:
        return False
    try:
        sketch.setExpression(f".Constraints[{constraint_idx}]", expr)
        return True
    except Exception as e:
        App.Console.PrintError(f"  ! {label}: bind failed: {e}\n")
        return False
```

## File-format note

`.FCStd` files saved in FreeCAD 1.1 are NOT backward-compatible with FreeCAD
1.0 because of datum-orientation changes. **Pin everyone on the same major
version.** Don't open a 1.1-saved file in 1.0 — datums break.

`.FCStd1` and `.FCBak` are backup files FreeCAD creates on save. Add them to
`.gitignore`. The actual `.FCStd` should be version-controlled (it's a SQLite
database — diffs are opaque, but file history is useful).

## What this pattern unlocks

- Iterate FreeCAD models the way you iterate code: edit, run, observe, fix
- Generate `Grinder_Params.FCStd` from a single command — reproducible
- Test parametric model behavior by setting different VarSet values and
  checking the recomputed geometry
- Generate STL files from FreeCAD assemblies as part of a build pipeline
- Validate manufacturability constraints (bbox < print volume, overhangs,
  minimum wall thickness) via macros that walk the assembly programmatically

## What this pattern doesn't unlock

- Visual inspection (still need GUI to look at the 3D viewport)
- Sketcher's interactive constraint UI (better for some manual work)
- Workbenches that depend on Qt/GUI infrastructure (rare)

## Concrete example from this project

`tooling/bike-powered-grinder/freecad/macros/` has three working macros plus
their headless wrappers. Macro 03 alone produces:
- 10 construction geometry elements (3 circles + 4-line rectangle + 3 more circles)
- 21 constraints (positioning + sizing + corner coincidences)
- 9 expression bindings to VarSet properties
- All in a single `freecadcmd.exe` invocation, ~2 seconds

Walking that macro is the fastest way to learn the Sketcher API patterns.

## When the GUI still wins

Open the resulting `.FCStd` in the GUI and:
- Verify geometry visually
- Drag tentative-position elements (intermediate-shaft and crank/BB centers in
  the bike grinder example are placeholders Isaiah moves manually)
- Test parametric updates by changing a VarSet value and pressing F5
- Inspect constraints panel for which are bound to expressions

The headless pipeline is for *iteration*. The GUI is for *verification* and
*decision-making*.
